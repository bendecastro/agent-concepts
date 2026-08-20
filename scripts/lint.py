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
REQUIRED_ROOT_FILES = ["AGENTS.md", "index.md", "log.md", "README.md", "docs/bootstrap.md", "docs/harnesses.md"]

# CONCEPT.md frontmatter. The test gate used to be honor-system prose spread
# across 43 files in ~10 phrasings, so "what is untested" could not be answered
# without reading all of them. These four keys are the single home for that
# state; index.md and the --status board read from here.
STATUS_KEYS = {
    "test_kind": {"pressure", "accuracy", "none"},
    "test_status": {"pass", "partial", "fail", "not-run"},
}
DATE_OR = re.compile(r"^(\d{4}-\d{2}-\d{2})$")
KNOWN_DEPLOY_DIRS = [
    Path.home() / ".agents" / "skills",
    Path.home() / ".claude" / "skills",
    Path.home() / ".pi" / "agent" / "skills",
]


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


def raw_entries_from_index(index: str) -> set[str]:
    entries: set[str] = set()
    in_raw = False
    for line in index.splitlines():
        if line.startswith("## "):
            in_raw = line.strip().lower() == "## raw"
            continue
        if in_raw:
            m = re.search(r"\]\(raw/([^)]+)\)", line)
            if m:
                entries.add(m.group(1).rstrip("/"))
    return entries


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.split("#", 1)[0].strip()
    return fields


def concept_status(name: str) -> dict[str, str] | None:
    concept = ROOT / "concepts" / name / "CONCEPT.md"
    return parse_frontmatter(read(concept)) if concept.is_file() else None


def lint_root(issues: list[Issue]) -> None:
    for name in REQUIRED_ROOT_FILES:
        if not (ROOT / name).is_file():
            issues.append(Issue("ERROR", f"missing root file: {name}"))
    if (ROOT / "build").exists():
        issues.append(Issue("WARN", "build/ exists; AGENTS.md says not to create it until derived outputs are needed"))


def lint_links(issues: list[Issue]) -> None:
    for md in ROOT.rglob("*.md"):
        # Raw sources are immutable source material; only lint workspace-owned docs.
        if "raw" in md.relative_to(ROOT).parts:
            continue
        text = read(md)
        for link in markdown_links(text):
            if not link_target_exists(md.parent, link):
                issues.append(Issue("ERROR", f"broken markdown link in {rel(md)}: {link}"))


# Repo-relative references are routinely written as inline code rather than
# markdown links (provenance bullets, test steps). Those were invisible to
# lint_links, which only understands [text](target) — 74 of them silently broke
# during the 2026-08 extraction. Only prefixes that unambiguously mean
# "repo-relative path" are checked, so external paths like `~/.claude/skills`
# and bare filenames are left alone.
# "docs/" is deliberately absent: concepts like codebase-docs discuss generic
# docs/ trees in other repositories, so the prefix is not unambiguously
# repo-relative. Markdown links into docs/ are still checked by lint_links.
INLINE_PATH_PREFIXES = ("concepts/", "scripts/", "policies/", "plans/", "raw/")
INLINE_CODE = re.compile(r"`([^`\n]+)`")


def lint_inline_paths(issues: list[Issue]) -> None:
    for md in ROOT.rglob("*.md"):
        parts = md.relative_to(ROOT).parts
        if "raw" in parts:
            continue
        # log.md is a historical journal; its paths were true when written.
        if md.name == "log.md":
            continue
        for match in INLINE_CODE.findall(read(md)):
            ref = match.strip().split()[0] if match.strip() else ""
            ref = ref.rstrip(".,;:)")
            if not ref.startswith(INLINE_PATH_PREFIXES):
                continue
            if "*" in ref or "<" in ref:  # globs and placeholders are not literal paths
                continue
            if not (ROOT / ref.split("#")[0]).exists():
                issues.append(Issue("ERROR", f"broken inline path in {rel(md)}: {ref}"))


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


def lint_status(issues: list[Issue]) -> None:
    concepts_dir = ROOT / "concepts"
    if not concepts_dir.exists():
        return
    for cdir in sorted(p for p in concepts_dir.iterdir() if p.is_dir()):
        concept = cdir / "CONCEPT.md"
        if not concept.is_file():
            continue
        fields = parse_frontmatter(read(concept))
        if fields is None:
            issues.append(Issue("ERROR", f"{rel(concept)} has no status frontmatter"))
            continue
        for key, allowed in STATUS_KEYS.items():
            value = fields.get(key)
            if value is None:
                issues.append(Issue("ERROR", f"{rel(concept)} frontmatter missing {key}"))
            elif value not in allowed:
                issues.append(Issue("ERROR", f"{rel(concept)} {key}={value!r} not one of {sorted(allowed)}"))
        for key, sentinels in (("tested", ("never",)), ("deployed", ("no", "yes"))):
            value = fields.get(key)
            if value is None:
                issues.append(Issue("ERROR", f"{rel(concept)} frontmatter missing {key}"))
            elif value not in sentinels and not DATE_OR.match(value):
                allowed = " or ".join(repr(s) for s in sentinels)
                issues.append(Issue("ERROR", f"{rel(concept)} {key}={value!r} must be YYYY-MM-DD or {allowed}"))

        # The test gate, mechanically. Deploying something never run is exactly
        # the drift the gate exists to prevent, and prose could not surface it.
        deployed = fields.get("deployed", "no")
        test_status = fields.get("test_status", "not-run")
        if deployed != "no":
            if fields.get("tested") == "never" or test_status == "not-run":
                issues.append(Issue("ERROR", f"test gate: {cdir.name} is deployed ({deployed}) but never run"))
            elif test_status == "fail":
                issues.append(Issue("ERROR", f"test gate: {cdir.name} is deployed ({deployed}) with a failing test"))
        if test_status == "partial":
            issues.append(Issue("WARN", f"{cdir.name}: passes with a known gap (see its ## Tests section)"))

        # Disk is authoritative for deployment. deploy-local-skills.py globs every
        # */body/SKILL.md, so a concept ships whether or not its prose says so --
        # which is how 19 CONCEPT.md files came to claim "not deployed yet" while
        # live. Concepts without a body/SKILL.md (agent-kernel) deploy as harness
        # deltas instead and are not symlink-checkable.
        if (cdir / "body" / "SKILL.md").is_file():
            live = any((d / cdir.name).exists() for d in KNOWN_DEPLOY_DIRS)
            if live and deployed == "no":
                issues.append(Issue("ERROR", f"{cdir.name}: deployed:no but a deploy symlink is live"))
            elif not live and deployed != "no":
                issues.append(Issue("ERROR", f"{cdir.name}: deployed:{deployed} but no deploy symlink exists"))


RANK = {"fail": 0, "not-run": 1, "partial": 2, "pass": 3}
STATUS_DOC = ROOT / "docs" / "status.md"
GENERATED_HEADER = "<!-- GENERATED by `scripts/lint.py --write-status` — do not edit by hand. -->"


def all_status() -> list[tuple[str, dict[str, str]]]:
    concepts_dir = ROOT / "concepts"
    if not concepts_dir.exists():
        return []
    out = []
    for cdir in sorted(p for p in concepts_dir.iterdir() if p.is_dir()):
        if (cdir / "CONCEPT.md").is_file():
            out.append((cdir.name, concept_status(cdir.name) or {}))
    return out


def render_status_doc() -> str:
    entries = all_status()

    def link(name: str) -> str:
        return f"[{name}](../concepts/{name}/CONCEPT.md)"

    untested, gaps, undeployed, healthy = [], [], [], []
    for name, f in entries:
        deployed = f.get("deployed", "no")
        status = f.get("test_status", "")
        never_run = f.get("tested") == "never" or status == "not-run"
        if deployed != "no" and (never_run or status == "fail"):
            untested.append((name, f))
        elif status == "partial":
            gaps.append((name, f))
        elif deployed == "no":
            undeployed.append((name, f))
        else:
            healthy.append((name, f))

    lines = [
        GENERATED_HEADER,
        "",
        "# Status",
        "",
        f"{len(entries)} concepts. {len(untested)} need testing, {len(undeployed)} not deployed, "
        f"{len(gaps)} deployed with a known gap.",
        "",
        "Source of truth is the frontmatter in each `CONCEPT.md`. Regenerate this page with",
        "`python3 scripts/lint.py --write-status`; `python3 scripts/lint.py` fails if it is stale.",
        "",
    ]

    lines += [f"## Needs testing ({len(untested)})", ""]
    if untested:
        lines += [
            "Live in your agents right now with no run recorded. Each one violates the test",
            "gate, so `lint.py` exits non-zero until it is tested or undeployed.",
            "",
            "| concept | kind | test status | deployed |",
            "|---|---|---|---|",
        ]
        lines += [
            f"| {link(n)} | {f.get('test_kind','?')} | {f.get('test_status','?')} | {f.get('deployed','?')} |"
            for n, f in untested
        ]
    else:
        lines.append("Nothing. Every deployed concept has a recorded run.")
    lines.append("")

    lines += [f"## Not deployed ({len(undeployed)})", ""]
    if undeployed:
        lines += ["| concept | kind | test status | tested |", "|---|---|---|---|"]
        lines += [
            f"| {link(n)} | {f.get('test_kind','?')} | {f.get('test_status','?')} | {f.get('tested','?')} |"
            for n, f in undeployed
        ]
    else:
        lines.append("Nothing. Every concept is deployed.")
    lines.append("")

    lines += [f"## Deployed with a known gap ({len(gaps)})", ""]
    if gaps:
        lines += [
            "Passing overall, but each names a check that was never run or a target never",
            "tested. See the concept's `## Tests` section for what is missing.",
            "",
            "| concept | kind | tested | deployed |",
            "|---|---|---|---|",
        ]
        lines += [
            f"| {link(n)} | {f.get('test_kind','?')} | {f.get('tested','?')} | {f.get('deployed','?')} |"
            for n, f in gaps
        ]
    else:
        lines.append("None.")
    lines.append("")

    lines += [
        f"## Passing and deployed ({len(healthy)})",
        "",
        ", ".join(link(n) for n, _ in healthy) if healthy else "None.",
        "",
    ]
    return "\n".join(lines)


def lint_status_doc(issues: list[Issue]) -> None:
    if not STATUS_DOC.is_file():
        issues.append(Issue("ERROR", "missing docs/status.md; run scripts/lint.py --write-status"))
        return
    if read(STATUS_DOC) != render_status_doc():
        issues.append(Issue("ERROR", "docs/status.md is stale; run scripts/lint.py --write-status"))


def print_status_board() -> int:
    concepts_dir = ROOT / "concepts"
    rows = []
    for cdir in sorted(p for p in concepts_dir.iterdir() if p.is_dir()):
        fields = concept_status(cdir.name) or {}
        rows.append((
            RANK.get(fields.get("test_status", ""), -1),
            fields.get("deployed", "?") != "no",
            cdir.name,
            fields.get("test_kind", "?"),
            fields.get("test_status", "MISSING"),
            fields.get("tested", "?"),
            fields.get("deployed", "?"),
        ))
    rows.sort()
    width = max((len(r[2]) for r in rows), default=10)
    print(f"{'concept':<{width}}  {'kind':<8} {'status':<8} {'tested':<10} deployed")
    print("-" * (width + 40))
    for _, _, name, kind, status, tested, deployed in rows:
        print(f"{name:<{width}}  {kind:<8} {status:<8} {tested:<10} {deployed}")
    needs = [r[2] for r in rows if r[0] != RANK["pass"]]
    print()
    print(f"{len(rows)} concepts; {len(needs)} need attention" + (f": {', '.join(needs)}" if needs else ""))
    return 0


def lint_raw(issues: list[Issue], index: str) -> None:
    # Upstream material is cited, not redistributed, so raw/ingested/ holds only
    # SOURCE.md notes. The registry of what was ingested is CITATIONS.md — not
    # index.md, which now links to upstream URLs and therefore contains no
    # raw/ paths to match against.
    raw_root = ROOT / "raw"
    if not raw_root.exists():
        return

    def children(d: Path) -> set[str]:
        return {c.name for c in d.iterdir() if not c.name.startswith(".")}

    citations = raw_root / "ingested" / "CITATIONS.md"
    if not citations.is_file():
        issues.append(Issue("ERROR", "missing source registry: raw/ingested/CITATIONS.md"))
        return
    cited = read(citations)

    ingested_dir = raw_root / "ingested"
    ingested = children(ingested_dir) - {"CITATIONS.md"} if ingested_dir.is_dir() else set()
    for name in sorted(ingested):
        if name not in cited:
            issues.append(Issue("WARN", f"ingested source missing from CITATIONS.md: {name}"))

    # Every cited directory should still carry the SOURCE.md describing what was taken.
    for name in sorted(ingested):
        d = ingested_dir / name
        if d.is_dir() and not (d / "SOURCE.md").is_file():
            issues.append(Issue("WARN", f"raw/ingested/{name} has no SOURCE.md"))

    # raw/ top level remains the to-ingest inbox; those still belong in index.md.
    inbox = children(raw_root) - {"ingested"}
    indexed_inbox = {e.split("/", 1)[0] for e in raw_entries_from_index(index)}
    for missing in sorted(inbox - indexed_inbox):
        issues.append(Issue("WARN", f"raw inbox source not listed in index.md: raw/{missing}"))


def lint_policies(issues: list[Issue]) -> None:
    # The real policy is user-owned and lives outside the repo
    # (~/.config/agent-concepts/publish.yaml), so it is deliberately not linted here:
    # it is the user's data, and its contents are none of this repo's business.
    # What must not regress is the *shape* of the example, because that is what a
    # new user copies. Naming specific repositories here is what previously made
    # the linter reject anyone else's policy.
    policy = ROOT / "policies" / "publish.example.yaml"
    if not policy.is_file():
        issues.append(Issue("ERROR", "missing policy template: policies/publish.example.yaml"))
        return
    text = read(policy)
    required_fragments = [
        "version: 1",
        "default: deny",
        "only_agent_authored_changes",
        "never_include_unrelated_user_changes: true",
        "SELF-AMENDMENT IMMUNITY",  # the safety property must stay documented
    ]
    for fragment in required_fragments:
        if fragment not in text:
            issues.append(Issue("ERROR", f"policy template missing required fragment: {fragment}"))
    if re.search(r"default:\s*allow\b", text):
        issues.append(Issue("ERROR", "policy template must not default to allow"))
    if (ROOT / "policies" / "publish.yaml").exists():
        issues.append(Issue("ERROR", "policies/publish.yaml is present in the repo; a real "
                                     "policy belongs in ~/.config/agent-concepts/"))
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
    parser.add_argument("--status", action="store_true", help="print the concept test/deploy board and exit")
    parser.add_argument("--write-status", action="store_true", help="regenerate docs/status.md and exit")
    args = parser.parse_args()

    if args.status:
        return print_status_board()

    if args.write_status:
        STATUS_DOC.parent.mkdir(parents=True, exist_ok=True)
        STATUS_DOC.write_text(render_status_doc(), encoding="utf-8")
        print(f"wrote {rel(STATUS_DOC)}")
        return 0

    issues: list[Issue] = []
    index_path = ROOT / "index.md"
    index = read(index_path) if index_path.exists() else ""

    lint_root(issues)
    lint_links(issues)
    lint_inline_paths(issues)
    lint_concepts(issues, index)
    lint_status(issues)
    lint_status_doc(issues)
    lint_raw(issues, index)
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
