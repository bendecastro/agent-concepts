#!/usr/bin/env python3
"""Deploy the workspace's concepts as local harness-discoverable skills.

For each concepts/<name>/body/SKILL.md, except concepts whose CONCEPT.md
frontmatter says `deployed: no`, create/update relative symlinks:
  ~/.agents/skills/<name>     -> <this repo>/concepts/<name>/body
  ~/.pi/agent/skills/<name>   -> <this repo>/concepts/<name>/body
  ~/.claude/skills/<name>     -> <this repo>/concepts/<name>/body

The repository location is derived from this file, so the workspace can live
anywhere. Links are relative, which keeps them valid across machines with
different home directories.

The ~/.agents/skills/ bus is also the Composer (Cursor), Grok, OpenCode, and
Muse Code discovery path: those harnesses scan it alongside their native skill
dirs. No extra symlink targets are required for them. Do not muse-skills-import
or install corpus skills into ~/.config/muse/skills/ — that copies files and
freezes bodies. Muse's always-on kernel is a separate regular-file copy of
a machine-local kernel source (see docs/guides/harnesses.md), not a skill deploy.

Some concepts assume software that may not be installed (see "Requires" in
index.md). They self-gate through their descriptions, so deploying them is
harmless; use --skip to leave them out anyway.

Non-symlink destinations are skipped unless --force is supplied. A symlink that
points anywhere other than a concept body this script deploys (this repository's
concepts/ or the private concepts folder) is someone else's skill: it is reported
and left alone, never replaced.

--uninstall removes only the symlinks this script created, from the same folders,
and leaves every other entry alone. Use --dry-run first to see what would go.

Examples:
  deploy-local-skills.py --dry-run
  deploy-local-skills.py --harness claude
  deploy-local-skills.py --skip teach --skip seo
  deploy-local-skills.py --uninstall --dry-run
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

# Private concepts live beside the user's other personal configuration, outside
# this repository. Same shape as concepts/ here, so a concept can move between
# private and public by moving its directory. Nothing here is ever committed to
# this repo, which is the point: some knowledge (infrastructure topology,
# employer-specific process) should not be published to use it.
CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config")).expanduser()
PRIVATE_CONCEPTS = CONFIG_HOME / "agent-concepts" / "concepts"

# Public vocabulary can evolve without breaking existing user muscle memory. Alias
# destinations must be canonical concept names; aliases never gain their own body.
DEPLOY_ALIASES: dict[str, str] = {
    "bc-plan-to-issues": "bc-plan-to-pipeline",
    "issue-slicing": "bc-plan-slicing",
    "bc-agent-reflect": "bc-reflect-on-sessions",
    "bc-drain-issues": "bc-pipeline-to-done",
    # Names before release 0.2.0 (docs/decisions/0004-skill-names-say-what-they-do.md).
    "bc-reflect": "bc-reflect-on-sessions",
    "bc-swarm": "bc-delegate-investigation",
    "bc-autoresearch-loop": "bc-optimize-code",
    "bc-show-me": "bc-explain-visually",
    "bc-init-agent": "bc-setup-project",
    "bc-council-improve-codebase": "bc-council-improve-architecture",
    "bc-guardrails": "bc-performance-guardrails",
    # Names before the bc- prefix (docs/decisions/0001-bc-prefix-for-public-skill-names.md).
    "brainstorming": "bc-brainstorming",
    "code-review": "bc-code-review",
    "codebase-design": "bc-codebase-design",
    "codebase-docs": "bc-codebase-docs",
    "council-chain": "bc-council-chain",
    "council-mode": "bc-council-mode",
    "diagnosing-bugs": "bc-diagnosing-bugs",
    "dispatching-parallel-agents": "bc-dispatching-parallel-agents",
    "domain-modeling": "bc-domain-modeling",
    "executing-plans": "bc-executing-plans",
    "find-bugs": "bc-find-bugs",
    "finishing-development-branch": "bc-finishing-development-branch",
    "grilling": "bc-grilling",
    "guardrails": "bc-performance-guardrails",
    "handoff": "bc-handoff",
    "improve-codebase-architecture": "bc-improve-codebase-architecture",
    "json-canvas": "bc-json-canvas",
    "minimal-solution-ladder": "bc-minimal-solution-ladder",
    "obsidian-bases": "bc-obsidian-bases",
    "obsidian-markdown": "bc-obsidian-markdown",
    "plain-language": "bc-plain-language",
    "plan-slicing": "bc-plan-slicing",
    "prd-drafting": "bc-prd-drafting",
    "prompting-agents": "bc-prompting-agents",
    "prototype": "bc-prototype",
    "qmd": "bc-qmd",
    "research": "bc-research",
    "security-audit": "bc-security-audit",
    "seo": "bc-seo",
    "show-me": "bc-explain-visually",
    "subagent-driven-development": "bc-subagent-driven-development",
    "tdd": "bc-tdd",
    "teach": "bc-teach",
    "to-spec": "bc-to-spec",
    "to-tickets": "bc-to-tickets",
    "triage": "bc-triage",
    "ui-design": "bc-ui-design",
    "unslop": "bc-unslop",
    "using-git-worktrees": "bc-using-git-worktrees",
    "writing-plans": "bc-writing-plans",
}


def rel_target(target: Path, link_parent: Path) -> str:
    # Symlink targets are interpreted relative to the real directory containing
    # the link. A harness dir such as `~/.pi` may itself be a symlink, so compute
    # from the resolved parent to avoid creating links that only work logically.
    return os.path.relpath(target.resolve(), start=link_parent.resolve())


def is_own_link(link: Path) -> bool:
    """True when a symlink points at a concept body this script deploys.

    That is a body under this repository's concepts/ or the private concepts folder,
    even when the concept no longer exists (a renamed concept's stale link is still
    ours). Any other symlink belongs to someone else.
    """
    target = Path(os.path.normpath(link.parent.resolve() / os.readlink(link)))
    return target.name == "body" and target.parent.parent in {CONCEPTS.resolve(), PRIVATE_CONCEPTS.resolve()}


def link_dir(link: Path, target: Path, *, force: bool, dry_run: bool) -> str:
    target_text = rel_target(target, link.parent)

    if link.is_symlink():
        current = os.readlink(link)
        if not is_own_link(link):
            return f"skip     {link} is a symlink this script did not create (-> {current}); left as is"
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


def marked_undeployed(body: Path) -> bool:
    """True when the concept's status frontmatter says `deployed: no`.

    The frontmatter is the record of what is live; deploying a concept marked
    `deployed: no` puts an untested skill in front of every agent. Flip the field
    to `yes` in the same change that deploys it.
    """
    concept = body.parent / "CONCEPT.md"
    if not concept.is_file():
        return False
    lines = concept.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    for line in lines[1:]:
        if line.strip() == "---":
            break
        key, _, value = line.partition(":")
        if key.strip() == "deployed":
            return value.strip() == "no"
    return False


def uninstall_dir(folder: Path, *, dry_run: bool) -> list[str]:
    """Remove the symlinks in folder that this script created; keep every other entry."""
    if not folder.is_dir():
        return []
    lines = []
    for link in sorted(folder.iterdir()):
        if not link.is_symlink():
            continue
        current = os.readlink(link)
        if not is_own_link(link):
            lines.append(f"keep     {link} is a symlink this script did not create (-> {current})")
            continue
        lines.append(f"remove   {link} (-> {current})")
        if not dry_run:
            link.unlink()
    return lines


def discover() -> tuple[list[tuple[str, Path]], list[str], list[str]]:
    """Concepts to deploy, plus the private names and any that shadowed a public one."""
    canonical = {
        skill_file.parents[1].name: skill_file.parent
        for skill_file in sorted(CONCEPTS.glob("*/body/SKILL.md"))
    }
    missing = sorted(set(DEPLOY_ALIASES.values()) - canonical.keys())
    if missing:
        raise SystemExit(f"Alias target(s) missing from concepts: {', '.join(missing)}")

    private = {
        skill_file.parents[1].name: skill_file.parent
        for skill_file in sorted(PRIVATE_CONCEPTS.glob("*/body/SKILL.md"))
    } if PRIVATE_CONCEPTS.is_dir() else {}

    # A private concept of the same name wins: it is the user's own, and they are
    # more likely to mean it than the library's. Shadowing is reported rather than
    # silent, because a name collision is usually accidental.
    shadowed = sorted(private.keys() & canonical.keys())
    canonical.update(private)

    skills = list(canonical.items())
    skills.extend((alias, canonical[target]) for alias, target in DEPLOY_ALIASES.items())
    return sorted(skills), sorted(private), shadowed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="show changes without writing symlinks")
    parser.add_argument("--force", action="store_true", help="replace existing non-symlink files only; directories still require manual cleanup")
    parser.add_argument("--harness", choices=["all", "pi", "claude"], default="all", help="which harness-specific skill dir to update (default: all)")
    parser.add_argument("--skip", action="append", default=[], metavar="NAME",
                        help="concept to leave undeployed (repeatable)")
    parser.add_argument("--uninstall", action="store_true",
                        help="remove the symlinks this script created; other entries are kept (with --dry-run, only show them)")
    args = parser.parse_args()

    if args.uninstall:
        if args.force or args.skip:
            parser.error("--uninstall takes --dry-run and --harness only, not --force or --skip")
        folders = [GLOBAL_SKILLS]
        if args.harness in {"all", "pi"}:
            folders.append(PI_SKILLS)
        if args.harness in {"all", "claude"}:
            folders.append(CLAUDE_SKILLS)
        lines = [line for folder in folders for line in uninstall_dir(folder, dry_run=args.dry_run)]
        for line in lines:
            print(line)
        removed = sum(line.startswith("remove") for line in lines)
        verb = "Would remove" if args.dry_run else "Removed"
        print(f"{verb} {removed} link(s).")
        return 0

    skills, private, shadowed = discover()
    if not skills:
        raise SystemExit(f"No concept skills found under {CONCEPTS}")
    held = sorted({name for name, body in skills if marked_undeployed(body)})
    if held:
        skills = [(name, body) for name, body in skills if name not in held]
        print(f"Holding {len(held)} concept(s) marked `deployed: no`: {', '.join(held)}")
    if private:
        print(f"Including {len(private)} private concept(s) from {PRIVATE_CONCEPTS}: "
              f"{', '.join(private)}")
    if shadowed:
        print(f"NOTE: private concept(s) override the library's: {', '.join(shadowed)}")

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
