#!/usr/bin/env python3
"""Deploy the workspace's concepts as local harness-discoverable skills.

For each concepts/<name>/body/SKILL.md, create/update relative symlinks:
  ~/.agents/skills/<name>     -> <this repo>/concepts/<name>/body
  ~/.pi/agent/skills/<name>   -> <this repo>/concepts/<name>/body
  ~/.claude/skills/<name>     -> <this repo>/concepts/<name>/body

The repository location is derived from this file, so the workspace can live
anywhere. Links are relative, which keeps them valid across machines with
different home directories.

The ~/.agents/skills/ bus is also the Composer (Cursor), Grok, and OpenCode
discovery path: those harnesses scan it alongside their native skill dirs. No
extra symlink targets are required for them.

Some concepts assume software that may not be installed (see "Requires" in
index.md). They self-gate through their descriptions, so deploying them is
harmless; use --skip to leave them out anyway.

Non-symlink destinations are skipped unless --force is supplied.

Examples:
  deploy-local-skills.py --dry-run
  deploy-local-skills.py --harness claude
  deploy-local-skills.py --skip omarchy --skip herdr
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
CLAUDE_SKILLS = HOME / ".claude" / "skills"

# Public vocabulary can evolve without breaking existing user muscle memory. Alias
# destinations must be canonical concept names; aliases never gain their own body.
DEPLOY_ALIASES = {
    "implement": "bc-drain-issues",
    "to-issues": "to-tickets",
    "to-prd": "to-spec",
}


def rel_target(target: Path, link_parent: Path) -> str:
    # Symlink targets are interpreted relative to the real directory containing
    # the link. A harness dir such as `~/.pi` may itself be a symlink, so compute
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
    canonical = {
        skill_file.parents[1].name: skill_file.parent
        for skill_file in sorted(CONCEPTS.glob("*/body/SKILL.md"))
    }
    missing = sorted(set(DEPLOY_ALIASES.values()) - canonical.keys())
    if missing:
        raise SystemExit(f"Alias target(s) missing from concepts: {', '.join(missing)}")

    skills = list(canonical.items())
    skills.extend((alias, canonical[target]) for alias, target in DEPLOY_ALIASES.items())
    return sorted(skills)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="show changes without writing symlinks")
    parser.add_argument("--force", action="store_true", help="replace existing non-symlink files only; directories still require manual cleanup")
    parser.add_argument("--harness", choices=["all", "pi", "claude"], default="all", help="which harness-specific skill dir to update (default: all)")
    parser.add_argument("--skip", action="append", default=[], metavar="NAME",
                        help="concept to leave undeployed (repeatable)")
    args = parser.parse_args()

    skills = discover()
    if not skills:
        raise SystemExit(f"No concept skills found under {CONCEPTS}")

    if args.skip:
        known = {name for name, _ in skills}
        unknown = sorted(set(args.skip) - known)
        if unknown:
            raise SystemExit(f"--skip names no such concept: {', '.join(unknown)}")
        skipped = sorted(set(args.skip))
        skills = [(name, body) for name, body in skills if name not in set(args.skip)]
        print(f"Skipping {len(skipped)} concept(s): {', '.join(skipped)}")

    for name, body in skills:
        global_link = GLOBAL_SKILLS / name
        print(link_dir(global_link, body, force=args.force, dry_run=args.dry_run))
        if args.harness in {"all", "pi"}:
            pi_link = PI_SKILLS / name
            print(link_dir(pi_link, body, force=args.force, dry_run=args.dry_run))
        if args.harness in {"all", "claude"}:
            claude_link = CLAUDE_SKILLS / name
            print(link_dir(claude_link, body, force=args.force, dry_run=args.dry_run))

    print(f"Deployed {len(skills)} concept skill(s). Restart agent sessions to refresh advertised skill lists.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
