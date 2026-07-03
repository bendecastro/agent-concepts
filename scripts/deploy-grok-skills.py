#!/usr/bin/env python3
"""Deploy CONFIG agents concepts into ~/.grok/skills/ (Grok consumes canon from here).

All symlinks point from Grok's skill directory into ~/Sync/CONFIG/agents/concepts/.
Re-run after editing concept bodies. Use --force to replace non-symlink directories.

Restart Grok sessions (or wait for filesystem reload) to refresh advertised skills.
"""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CONCEPTS = REPO / "concepts"
HOME = Path.home()
GROK_SKILLS = HOME / ".grok" / "skills"

# Grok skill directory name -> CONFIG concept body (must contain SKILL.md)
DEPLOYS: list[tuple[str, Path]] = [
    ("design", CONCEPTS / "design-doc-loop" / "body"),
    ("execute-plan", CONCEPTS / "execute-plan" / "body"),
    ("implement", CONCEPTS / "implement-loop" / "body"),
    ("pr-babysit", CONCEPTS / "pr-babysit" / "body"),
    ("review", CONCEPTS / "review-changes" / "body"),
    ("shared", CONCEPTS / "grok-shared" / "shared"),
    ("code-review", CONCEPTS / "strict-code-review" / "body"),
    ("strict-code-review", CONCEPTS / "strict-code-review" / "body"),
    ("check-work", CONCEPTS / "check-work" / "body"),
    ("create-skill", CONCEPTS / "create-skill" / "body"),
]


def rel_target(target: Path, link_parent: Path) -> str:
    return os.path.relpath(target.resolve(), start=link_parent.resolve())


def link_dir(link: Path, target: Path, *, force: bool, dry_run: bool) -> str:
    if not target.exists():
        return f"missing  {link} (target {target} does not exist)"

    target_text = rel_target(target, link.parent)

    if link.is_symlink():
        current = os.readlink(link)
        if current == target_text:
            return f"ok       {link} -> {current}"
        action = f"update   {link} -> {target_text} (was {current})"
        if not dry_run:
            link.unlink()
            link.symlink_to(target_text)
        return action

    if link.exists():
        if not force:
            return f"skip     {link} exists and is not a symlink (use --force)"
        action = f"replace  {link} -> {target_text}"
        if not dry_run:
            if link.is_dir():
                shutil.rmtree(link)
            else:
                link.unlink()
            link.symlink_to(target_text)
        return action

    action = f"create   {link} -> {target_text}"
    if not dry_run:
        GROK_SKILLS.mkdir(parents=True, exist_ok=True)
        link.symlink_to(target_text)
    return action


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace existing non-symlink directories with symlinks",
    )
    args = parser.parse_args()

    for name, target in DEPLOYS:
        print(link_dir(GROK_SKILLS / name, target, force=args.force, dry_run=args.dry_run))

    print(f"Deployed {len(DEPLOYS)} Grok skill link(s) from CONFIG concepts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())