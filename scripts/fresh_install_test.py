#!/usr/bin/env python3
"""Fresh-install test: install this checkout's skills the way a stranger would, then remove them.

For each install method (Pi package, Claude Code plugin, Codex plugin, `npx skills` all-skills
command, one `npx skills` pack) the test runs in a new empty HOME with a scrubbed environment:
install, check the installed skill list equals the expected list (`concepts/public-skills.json`,
or for a pack the pack's skill plus every skill it needs), run one bundled helper from the
installed copy, check that any installed pipeline skill includes its publish checker, update,
check the skill list again, uninstall and check nothing is left listed.

`pi-npm` installs what `npm publish` would ship: it runs `npm pack` on this checkout, checks the
tarball holds the kernel extension, the pipeline roles and the licence and nothing outside
package.json `files`, unpacks it and installs the unpacked folder (Pi 1.6 records a local
`.tgz` path but loads no skills from it). It packs the checkout even with `--ref`; the release
workflow's checkout is the tag, so that is the tarball the release publishes.

No logins, API keys or model calls. The agent CLIs come from PATH (CI installs pinned versions
from npm). `--drop-needed SKILL` installs the pack without one of its needed skills, to show the
check fails when a needed skill is missing. `--ref REF` installs from the GitHub repository at
that tag or commit instead of the local checkout, the way a stranger installs a release; the
expected skill lists still come from the local checkout, so check out the same ref first.

Usage: python3 scripts/fresh_install_test.py [--method M ...] [--ref REF] [--scratch DIR] [--pack NAME]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from install_packs import DOC_PATH, load_listing, packs  # noqa: E402
from pi_package import shipped_files  # noqa: E402

GITHUB_REPO = "bendecastro/agent-concepts"
PLUGIN_ID = "agent-concepts@agent-concepts"
MARKETPLACE = "agent-concepts"
NPX_AGENT = "pi"  # global skills dir ~/.agents/skills, real copies
DEFAULT_PACK = "bc-code-review"
# Helper run from the installed copy: argparse --help, no side effects. bc-tdd is in every
# install the test makes (all skills, and the default pack needs it).
HELPER_SKILL = "bc-tdd"
HELPER_RELPATH = "scripts/confirm-red.py"
PUBLISH_SKILL = "bc-pipeline-to-done"
PUBLISH_RELPATH = "scripts/publish-check.py"
METHODS = ("pi", "pi-npm", "claude", "codex", "npx-all", "npx-pack")
# Files the npm package must carry besides the skill bodies; npm adds README and LICENSE itself.
PACKED_ALWAYS = ("package.json", "README.md", "LICENSE")
PACKED_REQUIRED = ("LICENSE", "packages/agent-kernel-pi/index.js", "packages/agent-kernel-pi/AGENT-KERNEL.md",
                   *sorted(p.relative_to(ROOT).as_posix()
                           for p in (ROOT / "concepts/bc-pipeline-to-done/body/agents").glob("*.md")))

# Lists every skill Pi itself would load, the way a Pi session does (no model call).
PI_LISTER = r"""
import { realpathSync } from "node:fs";
import { dirname, join } from "node:path";
import { pathToFileURL } from "node:url";
const root = join(dirname(realpathSync(process.argv[2])), "..", "..");
const pi = await import(pathToFileURL(join(root, "dist", "index.js")).href);
const loader = new pi.DefaultResourceLoader({
  cwd: process.cwd(), agentDir: join(process.env.HOME, ".pi", "agent"),
  noExtensions: true, packageCommandOutput: "ignore",
});
await loader.reload();
const result = loader.getSkills();
for (const d of result.diagnostics) console.error("pi diagnostic: " + JSON.stringify(d));
for (const s of result.skills) console.log(s.name + "\t" + s.baseDir);
if (result.diagnostics.length) process.exit(3);
"""


# Exercise Pi's own pre-run prompt assembly without starting a provider request.
# _prepareRun is private; a Pi upgrade that changes it must fail this compatibility check.
PI_KERNEL_PROMPT = r"""
import { realpathSync } from "node:fs";
import { dirname, join } from "node:path";
import { pathToFileURL } from "node:url";
const root = join(dirname(realpathSync(process.argv[2])), "..", "..");
const pi = await import(pathToFileURL(join(root, "dist", "index.js")).href);
const { session, extensionsResult } = await pi.createAgentSession({
  cwd: process.cwd(), agentDir: join(process.env.HOME, ".pi", "agent"),
  sessionManager: pi.SessionManager.inMemory(),
});
if (extensionsResult.errors.length) throw new Error(JSON.stringify(extensionsResult.errors));
await session.bindExtensions({});
await session._prepareRun({ messageType: "user", prompt: "check", images: [] });
console.log(JSON.stringify(session.systemPrompt));
"""


class CheckFailed(Exception):
    pass


def install_sources(ref: str | None) -> dict[str, list[str]]:
    """What each method installs from: the local checkout, or the GitHub repository at `ref`.

    Each CLI takes the ref in its own syntax; the ref forms were checked against a pushed
    commit. See the CLI setup in .github/workflows/gate.yml and .github/workflows/release.yml
    for pinned versions, and .github/workflows/latest-agents.yml for the latest-release check.
    """
    if ref is None:
        local = str(ROOT)
        return {"pi": [local], "pi-npm": [local], "claude": [local], "codex": [local], "npx": [local]}
    return {
        "pi": [f"git:github.com/{GITHUB_REPO}@{ref}"],
        "pi-npm": [str(ROOT)],
        "claude": [f"{GITHUB_REPO}#{ref}"],
        "codex": [GITHUB_REPO, "--ref", ref],
        "npx": [f"{GITHUB_REPO}@{ref}"],
    }


def expected_skills(listing: dict[str, list[str]], pack: str | None = None) -> set[str]:
    """All public skills, or one pack: the skill plus everything it needs, transitively."""
    if pack is None:
        return set(listing)
    return set(packs(listing)[pack])


def list_problems(expected: set[str], listed: set[str]) -> list[str]:
    problems = []
    if missing := sorted(expected - listed):
        problems.append("missing: " + " ".join(missing))
    if extra := sorted(listed - expected):
        problems.append("unexpected: " + " ".join(extra))
    return problems


def pack_command(pack: str, drop: str | None = None, source: str = str(ROOT)) -> list[str]:
    """The documented `npx skills add` command for a pack (or `all`), read from the guide."""
    text = (ROOT / DOC_PATH).read_text(encoding="utf-8")
    commands = re.findall(r"^npx skills add .*$", text, re.MULTILINE)
    if pack == "all":
        line = commands[0]
    else:
        heading = text.index(f"### {pack}\n")
        line = re.search(r"^npx skills add .*$", text[heading:], re.MULTILINE).group(0)
    words = line.split()
    if drop is not None:
        if drop not in words:
            raise SystemExit(f"--drop-needed {drop}: not in the {pack} command")
        words.remove(drop)
    words = ["skills", *words[2:]]  # the pinned `skills` CLI on PATH, not whatever npx fetches
    return [source if w == "<source>" else NPX_AGENT if w == "<agent>" else w for w in words]


class Sandbox:
    """A fresh HOME and working folder; every command runs with only these variables."""

    def __init__(self, parent: Path, name: str):
        self.root = Path(tempfile.mkdtemp(prefix=f"fresh-{name}-", dir=parent))
        self.home = self.root / "home"
        self.cwd = self.root / "work"
        for path in (self.home, self.cwd, self.home / "tmp"):
            path.mkdir()
        # Pi reads .agents/skills in every ancestor of the cwd up to the git root; a .git
        # folder here stops it before any real skills folder above the scratch area.
        (self.cwd / ".git").mkdir()
        self.env = {
            "PATH": os.environ["PATH"],
            "HOME": str(self.home),
            "TMPDIR": str(self.home / "tmp"),
            "LANG": os.environ.get("LANG", "C.UTF-8"),
            "TERM": "dumb",
            "CI": "1",
            "DO_NOT_TRACK": "1",
            "DISABLE_TELEMETRY": "1",
        }

    def run(self, *args: str, check: bool = True) -> str:
        print("  $", " ".join(args), flush=True)
        proc = subprocess.run(args, cwd=self.cwd, env=self.env, stdin=subprocess.DEVNULL,
                              capture_output=True, text=True, timeout=600)
        if check and proc.returncode != 0:
            raise CheckFailed(f"{args[0]} exited {proc.returncode}:\n{proc.stdout}\n{proc.stderr}")
        return proc.stdout


def find_helper(base: Path, skill: str, relpath: str) -> Path:
    for skill_md in sorted(base.glob(f"**/{skill}/**/SKILL.md")):
        helper = skill_md.parent / relpath
        if skill_md.is_file() and helper.is_file() and ROOT not in helper.parents:
            return helper
    raise CheckFailed(f"no installed copy of {skill}/{relpath} under {base}")


class PiPackage:
    def __init__(self, box: Sandbox, source: list[str]):
        self.box = box
        self.source = source
        self.lister = box.root / "list-pi-skills.mjs"
        self.lister.write_text(PI_LISTER, encoding="utf-8")

    def install(self):
        self.box.run("pi", "install", *self.source)

    def listed(self) -> dict[str, Path]:
        out = self.box.run("node", str(self.lister), shutil.which("pi") or "pi")
        return {name: Path(base) for name, base in (line.split("\t") for line in out.splitlines())}

    def helper(self, listed: dict[str, Path], skill: str, relpath: str) -> Path:
        # A local-path Pi package is used in place, not copied: the helper runs from that path.
        # A git package is cloned under ~/.pi/agent/git and runs from there.
        return listed[skill] / relpath

    def update(self):
        self.box.run("pi", "update", "--extensions")

    def uninstall(self):
        self.box.run("pi", "remove", *self.source)


def packed_problems(paths: list[str]) -> list[str]:
    """What is wrong with a packed npm package, given its file paths relative to the package."""
    shipped = tuple(shipped_files(ROOT))
    problems = [f"missing from the packed package: {p}" for p in PACKED_REQUIRED if p not in paths]
    problems += [f"outside the shipped files: {p}" for p in sorted(paths)
                 if p not in PACKED_ALWAYS and not p.startswith(shipped)]
    return problems


class PiNpmPackage(PiPackage):
    """The tarball `npm publish` would upload, unpacked and installed as a local Pi package."""

    def check_kernel_prompt(self):
        probe = self.box.root / "check-pi-kernel.mjs"
        probe.write_text(PI_KERNEL_PROMPT, encoding="utf-8")
        try:
            out = self.box.run("node", str(probe), shutil.which("pi") or "pi")
            prompt = json.loads(out)
        except (CheckFailed, json.JSONDecodeError) as exc:
            raise CheckFailed(f"kernel check could not read Pi system prompt: {exc}") from exc
        if not isinstance(prompt, str) or not prompt.strip():
            raise CheckFailed("Pi system prompt is not non-empty text")
        kernel = (self.box.root / "package/packages/agent-kernel-pi/AGENT-KERNEL.md").read_text()
        if not kernel.strip():
            raise CheckFailed("packaged kernel is empty")
        if kernel not in prompt:
            raise CheckFailed("kernel missing from Pi system prompt")
        print("  ok: kernel present in Pi system prompt", flush=True)

    def install(self):
        tarball = self.box.run("npm", "pack", "--silent", "--pack-destination", str(self.box.root),
                               *self.source).strip().splitlines()[-1]
        self.box.run("tar", "xzf", str(self.box.root / tarball), "-C", str(self.box.root))
        package = self.box.root / "package"
        paths = [p.relative_to(package).as_posix() for p in package.rglob("*") if p.is_file()]
        problems = packed_problems(paths)
        if problems:
            raise CheckFailed("npm pack: " + "; ".join(problems))
        print(f"  ok: packed package holds {len(paths)} files, kernel, roles and licence", flush=True)
        self.source = [str(package)]
        super().install()


class ClaudePlugin:
    def __init__(self, box: Sandbox, source: list[str]):
        self.box = box
        self.source = source

    def install(self):
        self.box.run("claude", "plugin", "marketplace", "add", *self.source)
        self.box.run("claude", "plugin", "install", PLUGIN_ID)

    def listed(self) -> dict[str, Path]:
        installed = json.loads(self.box.run("claude", "plugin", "list", "--json"))
        if not installed:
            return {}
        out = self.box.run("claude", "plugin", "details", PLUGIN_ID)
        match = re.search(r"Skills \(\d+\)\s+(.*)", out)
        names = [n.strip() for n in match.group(1).split(",")] if match else []
        return {name: self.box.home / ".claude" for name in names}

    def helper(self, listed: dict[str, Path], skill: str, relpath: str) -> Path:
        return find_helper(self.box.home / ".claude" / "plugins", skill, relpath)

    def update(self):
        self.box.run("claude", "plugin", "marketplace", "update", MARKETPLACE)
        self.box.run("claude", "plugin", "update", PLUGIN_ID)

    def uninstall(self):
        self.box.run("claude", "plugin", "uninstall", PLUGIN_ID)
        self.box.run("claude", "plugin", "marketplace", "remove", MARKETPLACE)


class CodexPlugin:
    def __init__(self, box: Sandbox, source: list[str]):
        self.box = box
        self.source = source

    def install(self):
        self.box.run("codex", "plugin", "marketplace", "add", *self.source)
        self.box.run("codex", "plugin", "add", PLUGIN_ID)

    def listed(self) -> dict[str, Path]:
        # Renders the prompt Codex would send, without sending it: no login, no model call.
        out = self.box.run("codex", "debug", "prompt-input", "hi")
        names = set(re.findall(r"\bagent-concepts:([a-z0-9-]+)", out))
        return {name: self.box.home / ".codex" for name in names}

    def helper(self, listed: dict[str, Path], skill: str, relpath: str) -> Path:
        return find_helper(self.box.home / ".codex" / "plugins", skill, relpath)

    def update(self):
        # Codex has no plugin update command; installing again is the update. A Git
        # marketplace is refreshed first (a local one is read in place).
        if len(self.source) > 1:
            self.box.run("codex", "plugin", "marketplace", "upgrade", MARKETPLACE)
        self.box.run("codex", "plugin", "add", PLUGIN_ID)

    def uninstall(self):
        self.box.run("codex", "plugin", "remove", PLUGIN_ID)
        self.box.run("codex", "plugin", "marketplace", "remove", MARKETPLACE)


class NpxSkills:
    def __init__(self, box: Sandbox, source: list[str], pack: str, drop: str | None = None):
        self.box = box
        self.command = pack_command(pack, drop, *source)

    @property
    def skills_dir(self) -> Path:
        return self.box.home / ".agents" / "skills"

    def install(self):
        self.box.run(*self.command)

    def listed(self) -> dict[str, Path]:
        if not self.skills_dir.is_dir():
            return {}
        return {p.name: p for p in self.skills_dir.iterdir() if (p / "SKILL.md").is_file()}

    def helper(self, listed: dict[str, Path], skill: str, relpath: str) -> Path:
        return listed[skill] / relpath

    def update(self):
        self.box.run("skills", "update", "-g", "-y")

    def uninstall(self):
        names = self.command[self.command.index("--skill") + 1:]
        self.box.run("skills", "remove", "-g", "-a", NPX_AGENT, "-y", *names)


def check_listed(label: str, expected: set[str], listed: dict[str, Path]):
    problems = list_problems(expected, set(listed))
    if problems:
        raise CheckFailed(f"{label}: installed skills differ from the expected list: " + "; ".join(problems))
    print(f"  ok: {label}: {len(listed)} skills listed, as expected", flush=True)


def run_method(method: str, scratch: Path, listing: dict[str, list[str]], pack: str, drop: str | None,
               ref: str | None = None):
    box = Sandbox(scratch, method)
    sources = install_sources(ref)
    if method == "pi":
        agent, expected = PiPackage(box, sources["pi"]), expected_skills(listing)
    elif method == "pi-npm":
        agent, expected = PiNpmPackage(box, sources["pi-npm"]), expected_skills(listing)
    elif method == "claude":
        agent, expected = ClaudePlugin(box, sources["claude"]), expected_skills(listing)
    elif method == "codex":
        agent, expected = CodexPlugin(box, sources["codex"]), expected_skills(listing)
    elif method == "npx-all":
        agent, expected = NpxSkills(box, sources["npx"], "all"), expected_skills(listing)
    else:
        agent, expected = NpxSkills(box, sources["npx"], pack, drop), expected_skills(listing, pack)
    print(f"== {method} (HOME={box.home})", flush=True)
    agent.install()
    if method == "pi-npm":
        agent.check_kernel_prompt()
    listed = agent.listed()
    check_listed("after install", expected, listed)
    if PUBLISH_SKILL in listed:
        checker = agent.helper(listed, PUBLISH_SKILL, PUBLISH_RELPATH)
        if not checker.is_file():
            raise CheckFailed(f"no installed copy of {PUBLISH_SKILL}/{PUBLISH_RELPATH} at {checker}")
        print(f"  ok: publish checker present in the installed skill: {checker}", flush=True)
    helper = agent.helper(listed, HELPER_SKILL, HELPER_RELPATH)
    out = box.run(sys.executable, str(helper), "--help")
    if "usage" not in out.lower():
        raise CheckFailed(f"helper {helper} --help printed no usage")
    print(f"  ok: helper ran from the installed copy: {helper}", flush=True)
    agent.update()
    check_listed("after update", expected, agent.listed())
    agent.uninstall()
    check_listed("after uninstall", set(), agent.listed())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--method", action="append", choices=METHODS,
                        help="install method to test (repeatable; default: all)")
    parser.add_argument("--scratch", type=Path, default=None,
                        help="parent folder for the fresh HOMEs (default: the system temp folder)")
    parser.add_argument("--ref", help=f"install from github.com/{GITHUB_REPO} at this tag or commit "
                        "instead of the local checkout")
    parser.add_argument("--pack", default=DEFAULT_PACK, help="pack tested by npx-pack")
    parser.add_argument("--drop-needed", metavar="SKILL",
                        help="install the pack without this needed skill; the test must then fail")
    parser.add_argument("--keep", action="store_true", help="keep the scratch folders")
    args = parser.parse_args(argv)
    listing = load_listing(ROOT)
    if args.pack not in packs(listing):
        parser.error(f"--pack {args.pack}: not a pack (a public skill with needed skills)")
    scratch = Path(tempfile.mkdtemp(prefix="fresh-install-", dir=args.scratch))
    failures = []
    try:
        for method in args.method or METHODS:
            try:
                run_method(method, scratch, listing, args.pack, args.drop_needed, args.ref)
            except CheckFailed as exc:
                print(f"FAIL {method}: {exc}", flush=True)
                failures.append(method)
    finally:
        if not args.keep:
            shutil.rmtree(scratch, ignore_errors=True)
    print("FAILED: " + " ".join(failures) if failures else "all install methods passed", flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
