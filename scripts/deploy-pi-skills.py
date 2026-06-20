#!/usr/bin/env python3
"""Deploy canonical CONFIG agent concepts as Pi-discoverable skills.

For each concepts/<name>/body/SKILL.md, create/update symlinks:
  ~/.agents/skills/<name> -> ~/Sync/CONFIG/agents/concepts/<name>/body
  ~/.pi/agent/skills/<name> -> ~/Sync/CONFIG/agents/concepts/<name>/body

Non-symlink destinations are skipped unless --force is supplied.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
CONCEPTS = REPO / "concepts"
HOME = Path.home()
GLOBAL_SKILLS = HOME / ".agents" / "skills"
PI_SKILLS = HOME / ".pi" / "agent" / "skills"


def rel_target(target: Path, link_parent: Path) -> str:
    # Symlink targets are interpreted relative to the real directory containing
    # the link. `~/.pi` is itself a symlink into `~/Sync/CONFIG/.pi`, so compute
    # from the resolved parent to avoid creating links that only work logically.
    return os.path.relpath(target.resolve(), start=link_parent.resolve())


def link_dir(link: Path, target: Path, *, force: bool, dry_run: bool) -> str:
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
            return f"skip     {link} exists and is not a symlink"
        action = f"replace  {link} -> {target_text}"
        if not dry_run:
            if link.is_dir():
                raise SystemExit(f"Refusing to replace non-symlink directory without manual cleanup: {link}")
            link.unlink()
            link.symlink_to(target_text)
        return action

    action = f"create   {link} -> {target_text}"
    if not dry_run:
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(target_text)
    return action


def discover() -> list[tuple[str, Path]]:
    skills: list[tuple[str, Path]] = []
    for skill_file in sorted(CONCEPTS.glob("*/body/SKILL.md")):
        name = skill_file.parents[1].name
        skills.append((name, skill_file.parent))
    return skills


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="show changes without writing symlinks")
    parser.add_argument("--force", action="store_true", help="replace existing non-symlink files only; directories still require manual cleanup")
    args = parser.parse_args()

    skills = discover()
    if not skills:
        raise SystemExit(f"No concept skills found under {CONCEPTS}")

    for name, body in skills:
        global_link = GLOBAL_SKILLS / name
        print(link_dir(global_link, body, force=args.force, dry_run=args.dry_run))
        pi_link = PI_SKILLS / name
        print(link_dir(pi_link, body, force=args.force, dry_run=args.dry_run))

    print(f"Deployed {len(skills)} concept skill(s). Restart Pi sessions to refresh the advertised skill list.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
