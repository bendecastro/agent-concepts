#!/usr/bin/env python3
"""Lint the agents workspace for mechanical drift.

Checks are intentionally conservative: this script catches objective problems
(missing files, broken links, stale index entries, dangling deploy symlinks) and
leaves judgment calls to the agent/user.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ROOT_FILES = ["AGENTS.md", "index.md", "log.md", "bootstrap.md", "harnesses.md"]
KNOWN_DEPLOY_DIRS = [Path.home() / ".claude" / "skills", Path.home() / ".pi" / "agent" / "skills"]


@dataclass
class Issue:
    severity: str
    message: str


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="replace")


def strip_fenced_code(text: str) -> str:
    return re.sub(r"^```.*?^```", "", text, flags=re.M | re.S)


def strip_inline_code(text: str) -> str:
    return re.sub(r"`[^`]*`", "", text)


def markdown_links(text: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", strip_inline_code(strip_fenced_code(text)))


def link_target_exists(base: Path, link: str) -> bool:
    if re.match(r"^[a-z]+://", link) or link.startswith("mailto:"):
        return True
    target = link.split("#", 1)[0]
    if not target:
        return True
    return (base / target).resolve().exists()


def concept_names_from_index(index: str) -> set[str]:
    names: set[str] = set()
    in_concepts = False
    for line in index.splitlines():
        if line.startswith("## "):
            in_concepts = line.strip().lower() == "## concepts"
            continue
        if in_concepts:
            m = re.search(r"\]\(concepts/([^/]+)/CONCEPT\.md\)", line)
            if m:
                names.add(m.group(1))
    return names


def idea_entries_from_index(index: str) -> set[str]:
    entries: set[str] = set()
    in_ideas = False
    for line in index.splitlines():
        if line.startswith("## "):
            in_ideas = line.strip().lower() == "## ideas"
            continue
        if in_ideas:
            m = re.search(r"\]\(ideas/([^)]+)\)", line)
            if m:
                entries.add(m.group(1).rstrip("/"))
    return entries


def lint_root(issues: list[Issue]) -> None:
    for name in REQUIRED_ROOT_FILES:
        if not (ROOT / name).is_file():
            issues.append(Issue("ERROR", f"missing root file: {name}"))
    if (ROOT / "build").exists():
        issues.append(Issue("WARN", "build/ exists; AGENTS.md says not to create it until derived outputs are needed"))


def lint_links(issues: list[Issue]) -> None:
    for md in ROOT.rglob("*.md"):
        # Raw ideas are immutable source material; only lint workspace-owned docs.
        if "ideas" in md.relative_to(ROOT).parts:
            continue
        text = read(md)
        for link in markdown_links(text):
            if not link_target_exists(md.parent, link):
                issues.append(Issue("ERROR", f"broken markdown link in {rel(md)}: {link}"))


def lint_concepts(issues: list[Issue], index: str) -> None:
    concept_dirs = {p.name for p in (ROOT / "concepts").iterdir() if p.is_dir()} if (ROOT / "concepts").exists() else set()
    indexed = concept_names_from_index(index)

    for missing in sorted(concept_dirs - indexed):
        issues.append(Issue("ERROR", f"concept directory not listed in index.md: concepts/{missing}/"))
    for stale in sorted(indexed - concept_dirs):
        issues.append(Issue("ERROR", f"index.md lists missing concept: {stale}"))

    for name in sorted(concept_dirs):
        cdir = ROOT / "concepts" / name
        concept = cdir / "CONCEPT.md"
        body_dir = cdir / "body"
        tests = cdir / "tests"
        if not concept.is_file():
            issues.append(Issue("ERROR", f"{rel(cdir)} missing CONCEPT.md"))
            continue
        text = read(concept)
        if "## Provenance" not in text:
            issues.append(Issue("ERROR", f"{rel(concept)} missing ## Provenance"))
        if "## Tests" not in text:
            issues.append(Issue("WARN", f"{rel(concept)} missing ## Tests"))
        if not body_dir.is_dir() or not any(body_dir.glob("*.md")):
            issues.append(Issue("ERROR", f"{rel(cdir)} missing markdown body file"))
        if not tests.is_dir() or not any(tests.glob("*.md")):
            issues.append(Issue("WARN", f"{rel(cdir)} has no markdown tests"))


def lint_ideas(issues: list[Issue], index: str) -> None:
    indexed = idea_entries_from_index(index)
    idea_root = ROOT / "ideas"
    if not idea_root.exists():
        return
    top_level: set[str] = set()
    for child in idea_root.iterdir():
        if child.name.startswith("."):
            continue
        top_level.add(child.name if child.is_file() else child.name)
    indexed_top = {entry.split("/", 1)[0] for entry in indexed}
    for missing in sorted(top_level - indexed_top):
        issues.append(Issue("WARN", f"idea not listed in index.md: ideas/{missing}"))
    for line in index.splitlines():
        if line.lstrip().startswith("-") and "ideas/" in line:
            if not re.search(r"\b(Ingested|Filed|not yet ingested|partial|unused|Gap recorded)\b", line, re.I):
                issues.append(Issue("WARN", f"idea index entry lacks ingest/filed status: {line.strip()}"))


def lint_policies(issues: list[Issue]) -> None:
    policy = ROOT / "policies" / "publish.yaml"
    if not policy.is_file():
        issues.append(Issue("ERROR", "missing user-owned publish policy: policies/publish.yaml"))
        return
    text = read(policy)
    required_fragments = [
        "version: 1",
        "default: deny",
        "config-repo-push-after-agent-commit",
        "~/Sync/CONFIG",
        "https://github.com/bendecastro/CONFIG.git",
        "scripts-repo-push-after-agent-commit",
        "~/Sync/Scripts",
        "https://github.com/bendecastro/SCRIPTS.git",
        "music-repo-push-after-agent-commit",
        "~/Sync/Music",
        "https://github.com/bendecastro/Music.git",
        "wiki-repo-push-after-agent-commit",
        "~/Sync/Wiki",
        "https://github.com/bendecastro/Wiki.git",
        "only_agent_authored_changes",
        "never_include_unrelated_user_changes: true",
        "agents/policies/",  # self-amendment immunity must stay present
    ]
    for fragment in required_fragments:
        if fragment not in text:
            issues.append(Issue("ERROR", f"publish policy missing required fragment: {fragment}"))
    if re.search(r"default:\s*allow\b", text):
        issues.append(Issue("ERROR", "publish policy must not default to allow"))
    try:
        import yaml  # noqa: PLC0415

        yaml.safe_load(text)
    except ImportError:
        issues.append(Issue("WARN", "PyYAML unavailable; publish policy not parse-checked"))
    except Exception as exc:  # malformed YAML silently becomes "no rules match"
        issues.append(Issue("ERROR", f"publish policy is not valid YAML: {exc}"))


def lint_deploy_symlinks(issues: list[Issue]) -> None:
    concepts_root = (ROOT / "concepts").resolve()
    for deploy_dir in KNOWN_DEPLOY_DIRS:
        if not deploy_dir.exists():
            continue
        for link in deploy_dir.iterdir():
            if not link.is_symlink():
                continue
            raw = os.readlink(link)
            target = (link.parent / raw).resolve()
            if not target.exists():
                issues.append(Issue("ERROR", f"dangling deploy symlink: {link} -> {raw}"))
                continue
            try:
                target.relative_to(concepts_root)
            except ValueError:
                # Only warn for skills whose name matches a local concept; other skills may be unrelated.
                if (ROOT / "concepts" / link.name).exists():
                    issues.append(Issue("WARN", f"deploy symlink for local concept points outside concepts/: {link} -> {raw}"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint the agents workspace")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = parser.parse_args()

    issues: list[Issue] = []
    index_path = ROOT / "index.md"
    index = read(index_path) if index_path.exists() else ""

    lint_root(issues)
    lint_links(issues)
    lint_concepts(issues, index)
    lint_ideas(issues, index)
    lint_policies(issues)
    lint_deploy_symlinks(issues)

    if not issues:
        print("agents lint: ok")
        return 0

    for issue in issues:
        print(f"{issue.severity}: {issue.message}")

    has_error = any(i.severity == "ERROR" for i in issues)
    has_warn = any(i.severity == "WARN" for i in issues)
    return 1 if has_error or (args.strict and has_warn) else 0


if __name__ == "__main__":
    sys.exit(main())
