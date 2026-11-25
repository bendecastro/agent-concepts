#!/usr/bin/env python3
"""Generate the documented `npx skills` install commands from the public skill list.

One command installs every public skill; each ready-made pack is a public skill
that needs other skills, plus the transitive closure of what it needs. Every
command names its skills with `--skill` instead of `--skill '*'`, because the
`skills` CLI also discovers concepts marked `deployed: no` (it reads only
SKILL.md, not CONCEPT.md status).
"""

from __future__ import annotations

import json
from pathlib import Path


DOC_PATH = "docs/guides/install-packs.md"
LIST_PATH = "concepts/public-skills.json"
SOURCE_PLACEHOLDER = "<source>"
AGENT_PLACEHOLDER = "<agent>"


def load_listing(root: Path) -> dict[str, list[str]]:
    return json.loads((root / LIST_PATH).read_text(encoding="utf-8"))["skills"]


def _closure(name: str, listing: dict[str, list[str]]) -> list[str]:
    seen: set[str] = set()
    stack = list(listing.get(name, []))
    while stack:
        need = stack.pop()
        if need == name or need in seen:
            continue
        seen.add(need)
        stack.extend(listing.get(need, []))
    return [name, *sorted(seen)]


def packs(listing: dict[str, list[str]]) -> dict[str, list[str]]:
    return {name: _closure(name, listing) for name in sorted(listing) if listing[name]}


def add_command(skills: list[str], *, source: str = SOURCE_PLACEHOLDER, agent: str = AGENT_PLACEHOLDER) -> str:
    return f"npx skills add {source} -g -a {agent} -y --skill {' '.join(skills)}"


def render_doc(root: Path) -> str:
    listing = load_listing(root)
    lines = [
        "# Install with `npx skills`",
        "",
        f"<!-- GENERATED from {LIST_PATH} by `python3 scripts/lint.py --write-install-packs` -- do not edit by hand. -->",
        "",
        "These commands use the [`skills` CLI](https://github.com/vercel-labs/skills).",
        f"Replace `{SOURCE_PLACEHOLDER}` with this repository at a release tag (`<owner>/<repo>@<tag>`)",
        f"or a local checkout path, and `{AGENT_PLACEHOLDER}` with your agent's id from the CLI's",
        "[agent list](https://github.com/vercel-labs/skills/blob/main/docs/agents.md).",
        "`-g` installs for your user rather than the current project; `-y` skips prompts.",
        "Each command names its skills, so concepts not published as skills are never installed.",
        "",
        "## All public skills",
        "",
        "```bash",
        add_command(sorted(listing)),
        "```",
        "",
        "## Packs",
        "",
        "Each pack is one skill plus every skill it needs, directly or through another needed skill.",
        "",
    ]
    for name, members in packs(listing).items():
        lines += [f"### {name}", "", "```bash", add_command(members), "```", ""]
    return "\n".join(lines)


def write_doc(root: Path) -> Path:
    path = root / DOC_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_doc(root), encoding="utf-8")
    return path


def check_doc(root: Path) -> list[str]:
    path = root / DOC_PATH
    if not path.is_file():
        return [f"missing {DOC_PATH}; run scripts/lint.py --write-install-packs"]
    if path.read_text(encoding="utf-8") != render_doc(root):
        return [f"{DOC_PATH} is stale; run scripts/lint.py --write-install-packs"]
    return []
