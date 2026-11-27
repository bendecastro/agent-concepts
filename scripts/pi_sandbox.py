"""Run Pi with the harness's global instruction files emptied, after checking the session's system prompt.

Usage: pi_sandbox.py [--check-only] [--prompt-out FILE] -- pi [PI_ARGS...]

Masks, for the whole run (bwrap over the real filesystem, only for paths that exist):
  - every global instruction file Pi 1.6.1 reads from its agent directory ($PI_CODING_AGENT_DIR,
    default ~/.pi/agent): GLOBAL_INSTRUCTION_FILES, each replaced by an empty file;
  - deployed skill folders, private overlays, and `.agents/skills` in the working directory's
    ancestors (Pi reads those too), each replaced by an empty folder.
The project's own AGENTS.md files stay; no `-nc` is added. Nothing is masked when none of
these paths exists (a sandbox with a fresh home), so the helper can also run inside one.

Before the run, a check starts the same command in RPC mode without a session, sends one
prompt, takes the system message Pi records before its first model request, aborts, and fails
(exit 3) when the prompt holds a term from the private denylist ($AGENT_CONCEPTS_PERSONAL_TERMS
or ~/.config/agent-concepts/personal-terms.txt, same format as scripts/lint.py; skipped with a
note when absent) or when a project AGENTS.md between the working directory and its repository
root has text that is missing from the prompt's project context.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

# Pi 1.6.1 resource-loader: context files (first match per directory), then SYSTEM.md and
# APPEND_SYSTEM.md. An empty SYSTEM.md is ignored, so masking it keeps Pi's default prompt.
CONTEXT_FILE_NAMES = ("AGENTS.override.md", "AGENTS.md", "AGENTS.MD", "CLAUDE.md", "CLAUDE.MD")
GLOBAL_INSTRUCTION_FILES = CONTEXT_FILE_NAMES + ("SYSTEM.md", "APPEND_SYSTEM.md")
HIDDEN_HOME_DIRS = (".agents/skills", ".pi/agent/skills", ".claude/skills", ".config/agent-concepts/overlays")
CHECK_PROMPT = "Reply with the single word OK."
CHECK_TIMEOUT = 120


def agent_dir():
    return Path(os.environ.get("PI_CODING_AGENT_DIR") or Path.home() / ".pi/agent").expanduser()


def mask_plan(cwd):
    """Return (files, dirs) to mask: real paths, because bwrap refuses to mount on a symlink."""
    files = sorted({os.path.realpath(agent_dir() / name) for name in GLOBAL_INSTRUCTION_FILES
                    if (agent_dir() / name).is_file()})
    candidates = [Path.home() / d for d in HIDDEN_HOME_DIRS]
    candidates += [parent / ".agents/skills" for parent in [Path(cwd).resolve(), *Path(cwd).resolve().parents]]
    dirs = sorted({os.path.realpath(d) for d in candidates if d.is_dir()})
    return files, dirs


def sandboxed(command, cwd):
    """Wrap command in bwrap with the mask plan; return (argv, fds the child must inherit)."""
    files, dirs = mask_plan(cwd)
    if not files and not dirs:
        return list(command), []
    argv, fds = ["bwrap", "--dev-bind", "/", "/"], []
    for d in dirs:
        argv += ["--tmpfs", d]
    for f in files:  # one fd per mask: bwrap closes each after reading it
        fd = os.open(os.devnull, os.O_RDONLY)
        os.set_inheritable(fd, True)
        fds.append(fd)
        argv += ["--ro-bind-data", str(fd), f]
    return argv + ["--", *command], fds


def personal_terms():
    """Compiled denylist pattern, or None when the private list is absent or empty."""
    config = Path(os.environ.get("AGENT_CONCEPTS_PERSONAL_TERMS")
                  or Path.home() / ".config/agent-concepts/personal-terms.txt").expanduser()
    try:
        lines = config.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return None
    alternatives = []
    for line in lines:
        term = line.strip()
        if term and not term.startswith("#"):
            alternatives.append(term[3:] if term.startswith("re:") else re.escape(term))
    if not alternatives:
        return None
    return re.compile(r"(?<!\w)(?:" + "|".join(alternatives) + r")(?!\w)", re.IGNORECASE)


def read_system_sections(command, cwd):
    """Start command in RPC mode, prompt once, and return the first system message's sections."""
    argv, fds = sandboxed([*command, "--mode", "rpc", "--no-session"], cwd)
    stderr = tempfile.TemporaryFile()
    pi = subprocess.Popen(argv, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=stderr, pass_fds=fds)
    for fd in fds:
        os.close(fd)
    timer = threading.Timer(CHECK_TIMEOUT, pi.kill)
    timer.start()
    sections = None
    try:
        pi.stdin.write((json.dumps({"id": "check", "type": "prompt", "message": CHECK_PROMPT}) + "\n").encode())
        pi.stdin.flush()
        for line in pi.stdout:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            message = event.get("message") or {}
            if event.get("type") == "message_start" and message.get("role") == "system":
                sections = message.get("sections") or {"content": str(message.get("content", ""))}
                pi.stdin.write(b'{"id": "stop", "type": "abort"}\n')
                pi.stdin.flush()
                break
    except BrokenPipeError:
        pass
    finally:
        timer.cancel()
        pi.kill()
        pi.wait()
    if sections is None:
        stderr.seek(0)
        sys.stderr.write(stderr.read()[-2000:].decode("utf-8", "replace"))
    return sections


def project_context_files(cwd):
    """The AGENTS.md (or CLAUDE.md) Pi loads from cwd up to the repository root, non-empty only."""
    cwd = Path(cwd).resolve()
    top = subprocess.run(["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    root = Path(top.stdout.strip()).resolve() if top.returncode == 0 else cwd
    found = []
    for directory in [cwd, *cwd.parents]:
        for name in CONTEXT_FILE_NAMES:
            path = directory / name
            if path.is_file():
                text = path.read_text(encoding="utf-8", errors="replace").lstrip("\ufeff").strip()
                if text:
                    found.append((path, text))
                break
        if directory == root:
            break
    return found


def check_system_prompt(command, cwd):
    """Return (problems, sections). An empty problem list means the prompt passed."""
    sections = read_system_sections(command, cwd)
    if sections is None:
        return ["no system prompt arrived from the RPC stream"], None
    problems = []
    project_context = str(sections.get("project_context", ""))
    for path, text in project_context_files(cwd):
        if text not in project_context:
            problems.append(f"project instructions did not load: {path}")
    pattern = personal_terms()
    if pattern is None:
        print("pi_sandbox: no private denylist; personal-term check skipped", file=sys.stderr)
    else:
        # Machine paths (skill locations, Pi's docs, cwd) are not instructions; the home and
        # working-directory prefixes are replaced so only leaked text can match.
        text = json.dumps(sections, ensure_ascii=False)
        for prefix in sorted({str(Path(cwd).resolve()), str(Path.home())}, key=len, reverse=True):
            text = text.replace(prefix, "<path>")
        for term in sorted({m.group(0) for m in pattern.finditer(text)}):
            problems.append(f"personal term in system prompt: {term!r}")
    return problems, sections


def main(argv):
    check_only, prompt_out = False, None
    while argv and argv[0] != "--":
        flag = argv.pop(0)
        if flag == "--check-only":
            check_only = True
        elif flag == "--prompt-out" and argv:
            prompt_out = argv.pop(0)
        else:
            sys.exit(__doc__)
    command = argv[1:]
    if not command:
        sys.exit(__doc__)
    cwd = os.getcwd()
    problems, sections = check_system_prompt(command, cwd)
    if prompt_out and sections is not None:
        Path(prompt_out).write_text(json.dumps(sections, ensure_ascii=False, indent=1), encoding="utf-8")
    if problems:
        for problem in problems:
            print(f"pi_sandbox: {problem}", file=sys.stderr)
        return 3
    print("pi_sandbox: system prompt check passed", file=sys.stderr)
    if check_only:
        return 0
    argv, _fds = sandboxed(command, cwd)
    os.execvp(argv[0], argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
