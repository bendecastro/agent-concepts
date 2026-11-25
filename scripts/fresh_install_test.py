#!/usr/bin/env python3
"""Fresh-install test: install this checkout's skills the way a stranger would, then remove them.

For each install method (Pi package, Claude Code plugin, Codex plugin, `npx skills` all-skills
command, one `npx skills` pack) the test runs in a new empty HOME with a scrubbed environment:
install, check the installed skill list equals the expected list (`concepts/public-skills.json`,
or for a pack the pack's skill plus every skill it needs), run one bundled helper from the
installed copy, update, check again, uninstall and check nothing is left listed.

No logins, API keys or model calls. The agent CLIs come from PATH (CI installs pinned versions
from npm). `--drop-needed SKILL` installs the pack without one of its needed skills, to show the
check fails when a needed skill is missing.

Usage: python3 scripts/fresh_install_test.py [--method M ...] [--scratch DIR] [--pack NAME]
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

PLUGIN_ID = "agent-concepts@agent-concepts"
MARKETPLACE = "agent-concepts"
NPX_AGENT = "pi"  # global skills dir ~/.agents/skills, real copies
DEFAULT_PACK = "bc-code-review"
# Helper run from the installed copy: argparse --help, no side effects. bc-tdd is in every
# install the test makes (all skills, and the default pack needs it).
HELPER_SKILL = "bc-tdd"
HELPER_RELPATH = "scripts/confirm-red.py"
METHODS = ("pi", "claude", "codex", "npx-all", "npx-pack")

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


class CheckFailed(Exception):
    pass


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


def pack_command(pack: str, drop: str | None = None) -> list[str]:
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
    return [str(ROOT) if w == "<source>" else NPX_AGENT if w == "<agent>" else w for w in words]


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


def find_helper(base: Path) -> Path:
    hits = sorted(base.glob(f"**/{HELPER_SKILL}/**/{HELPER_RELPATH}"))
    hits = [h for h in hits if ROOT not in h.parents]
    if not hits:
        raise CheckFailed(f"no installed copy of {HELPER_SKILL}/{HELPER_RELPATH} under {base}")
    return hits[0]


class PiPackage:
    def __init__(self, box: Sandbox):
        self.box = box
        self.lister = box.root / "list-pi-skills.mjs"
        self.lister.write_text(PI_LISTER, encoding="utf-8")

    def install(self):
        self.box.run("pi", "install", str(ROOT))

    def listed(self) -> dict[str, Path]:
        out = self.box.run("node", str(self.lister), shutil.which("pi") or "pi")
        return {name: Path(base) for name, base in (line.split("\t") for line in out.splitlines())}

    def helper(self, listed: dict[str, Path]) -> Path:
        # A local-path Pi package is used in place, not copied: the helper runs from that path.
        return listed[HELPER_SKILL] / HELPER_RELPATH

    def update(self):
        self.box.run("pi", "update", "--extensions")

    def uninstall(self):
        self.box.run("pi", "remove", str(ROOT))


class ClaudePlugin:
    def __init__(self, box: Sandbox):
        self.box = box

    def install(self):
        self.box.run("claude", "plugin", "marketplace", "add", str(ROOT))
        self.box.run("claude", "plugin", "install", PLUGIN_ID)

    def listed(self) -> dict[str, Path]:
        installed = json.loads(self.box.run("claude", "plugin", "list", "--json"))
        if not installed:
            return {}
        out = self.box.run("claude", "plugin", "details", PLUGIN_ID)
        match = re.search(r"Skills \(\d+\)\s+(.*)", out)
        names = [n.strip() for n in match.group(1).split(",")] if match else []
        return {name: self.box.home / ".claude" for name in names}

    def helper(self, listed: dict[str, Path]) -> Path:
        return find_helper(self.box.home / ".claude" / "plugins")

    def update(self):
        self.box.run("claude", "plugin", "marketplace", "update", MARKETPLACE)
        self.box.run("claude", "plugin", "update", PLUGIN_ID)

    def uninstall(self):
        self.box.run("claude", "plugin", "uninstall", PLUGIN_ID)
        self.box.run("claude", "plugin", "marketplace", "remove", MARKETPLACE)


class CodexPlugin:
    def __init__(self, box: Sandbox):
        self.box = box

    def install(self):
        self.box.run("codex", "plugin", "marketplace", "add", str(ROOT))
        self.box.run("codex", "plugin", "add", PLUGIN_ID)

    def listed(self) -> dict[str, Path]:
        # Renders the prompt Codex would send, without sending it: no login, no model call.
        out = self.box.run("codex", "debug", "prompt-input", "hi")
        names = set(re.findall(r"\bagent-concepts:([a-z0-9-]+)", out))
        return {name: self.box.home / ".codex" for name in names}

    def helper(self, listed: dict[str, Path]) -> Path:
        return find_helper(self.box.home / ".codex" / "plugins")

    def update(self):
        # Codex has no plugin update for a local marketplace; installing again is the update.
        self.box.run("codex", "plugin", "add", PLUGIN_ID)

    def uninstall(self):
        self.box.run("codex", "plugin", "remove", PLUGIN_ID)
        self.box.run("codex", "plugin", "marketplace", "remove", MARKETPLACE)


class NpxSkills:
    def __init__(self, box: Sandbox, pack: str, drop: str | None = None):
        self.box = box
        self.command = pack_command(pack, drop)

    @property
    def skills_dir(self) -> Path:
        return self.box.home / ".agents" / "skills"

    def install(self):
        self.box.run(*self.command)

    def listed(self) -> dict[str, Path]:
        if not self.skills_dir.is_dir():
            return {}
        return {p.name: p for p in self.skills_dir.iterdir() if (p / "SKILL.md").is_file()}

    def helper(self, listed: dict[str, Path]) -> Path:
        return listed[HELPER_SKILL] / HELPER_RELPATH

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


def run_method(method: str, scratch: Path, listing: dict[str, list[str]], pack: str, drop: str | None):
    box = Sandbox(scratch, method)
    if method == "pi":
        agent, expected = PiPackage(box), expected_skills(listing)
    elif method == "claude":
        agent, expected = ClaudePlugin(box), expected_skills(listing)
    elif method == "codex":
        agent, expected = CodexPlugin(box), expected_skills(listing)
    elif method == "npx-all":
        agent, expected = NpxSkills(box, "all"), expected_skills(listing)
    else:
        agent, expected = NpxSkills(box, pack, drop), expected_skills(listing, pack)
    print(f"== {method} (HOME={box.home})", flush=True)
    agent.install()
    listed = agent.listed()
    check_listed("after install", expected, listed)
    helper = agent.helper(listed)
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
                run_method(method, scratch, listing, args.pack, args.drop_needed)
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
