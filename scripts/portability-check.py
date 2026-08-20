#!/usr/bin/env python3
"""Prove the workspace works for someone who is not its author.

Portability cannot be established by reading a diff: the author's machine
satisfies assumptions a stranger's will not. This exports the repository at HEAD
into a scratch directory under a fake HOME, then runs the things a new user runs
and asserts they succeed without referring to the author's tree.

    python3 scripts/portability-check.py

Exit 0 = portable. Exit 1 = a check failed; the report says which.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Paths that only the author has. A live file naming one of these is a bug,
# because nobody else can follow it.
#
# Deliberately NOT matched: the author's GitHub username. It appears legitimately
# in the clone URL, the licence, and provenance citations crediting where a design
# decision came from. Attribution is not a portability defect, and conflating the
# two would pressure a future maintainer to strip credit to make a check go green.
PERSONAL = re.compile(r"/home/ben|/Users/ben|Sync/CONFIG")

# Historical records: an append-only journal and dated run reports. Their paths
# were accurate on the machine and date they describe, and rewriting them would
# falsify the record.
EXEMPT = {
    "log.md",
    "docs/plans/implemented/portability.md",  # quotes the problem it exists to solve
    "concepts/agent-kernel/CONCEPT.md",  # dated per-harness deploy records
    "concepts/agent-kernel/tests/codex-smoke-2026-06-12.md",
    "scripts/portability-check.py",  # defines the pattern above
}

failures: list[str] = []
notes: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'PASS' if ok else 'FAIL'}  {label}")
    if detail:
        print(f"      {detail}")
    if not ok:
        failures.append(label)


def main() -> int:
    scratch = Path(tempfile.mkdtemp(prefix="portability-"))
    fake_home = scratch / "home"
    clone = scratch / "agent-concepts"
    fake_home.mkdir()
    clone.mkdir()

    try:
        # 1. Export HEAD — only what a stranger would actually receive.
        tar = subprocess.run(["git", "-C", str(REPO), "archive", "HEAD"],
                             capture_output=True, check=True).stdout
        subprocess.run(["tar", "-x", "-C", str(clone)], input=tar, check=True)
        tracked = sorted(p for p in clone.rglob("*") if p.is_file())
        check("exports a non-empty tree at HEAD", len(tracked) > 50,
              f"{len(tracked)} files")

        env = {**os.environ, "HOME": str(fake_home),
               "AGENT_CONCEPTS": str(clone),
               "XDG_CONFIG_HOME": str(fake_home / ".config")}

        # 2. Deploy must work against a home that has never seen this workspace.
        r = subprocess.run([sys.executable, "scripts/deploy-local-skills.py", "--dry-run"],
                           cwd=clone, env=env, capture_output=True, text=True)
        check("deploy --dry-run succeeds under a fresh HOME", r.returncode == 0,
              (r.stderr or r.stdout).strip().splitlines()[-1] if (r.stderr or r.stdout).strip() else "")
        deployed = [l for l in r.stdout.splitlines() if "->" in l]
        check("deploy plans at least one skill link", bool(deployed),
              f"{len(deployed)} link(s)")
        strays = [l for l in deployed if PERSONAL.search(l)]
        check("no planned symlink points into the author's tree", not strays,
              strays[0] if strays else "")
        absolute = [l for l in deployed if "-> /" in l]
        check("planned symlinks are relative", not absolute,
              absolute[0] if absolute else "")

        # 3. Lint must pass on a clean checkout.
        r = subprocess.run([sys.executable, "scripts/lint.py"],
                           cwd=clone, env=env, capture_output=True, text=True)
        errors = [l for l in (r.stdout + r.stderr).splitlines() if l.startswith("ERROR")]
        check("lint reports no errors on a fresh checkout", not errors,
              errors[0] if errors else "")

        # 4. With no policy installed, publishing must not be authorised.
        r = subprocess.run([sys.executable, "scripts/publish-check.py",
                            "--repo", str(clone), "--remote", "git@github.com:someone/thing.git",
                            "--branch", "main"],
                           cwd=clone, env=env, capture_output=True, text=True)
        check("publish is denied when no policy is installed", r.returncode == 2,
              r.stdout.strip())

        # 5. No live file may name a path only the author has.
        offenders = []
        for p in tracked:
            rel = str(p.relative_to(clone))
            if rel in EXEMPT or rel.startswith(".git"):
                continue
            try:
                text = p.read_text()
            except (UnicodeDecodeError, OSError):
                continue
            for i, line in enumerate(text.splitlines(), 1):
                if PERSONAL.search(line):
                    offenders.append(f"{rel}:{i}")
        check("no live file references the author's machine", not offenders,
              f"{len(offenders)} occurrence(s): {', '.join(offenders[:3])}" if offenders else "")

        # 6. The template must exist and the real policy must not be shipped.
        check("ships a policy template", (clone / "policies" / "publish.example.yaml").is_file())
        check("ships no real publish policy", not (clone / "policies" / "publish.yaml").exists())

    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    print()
    if failures:
        print(f"NOT PORTABLE — {len(failures)} check(s) failed:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("PORTABLE — all checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
