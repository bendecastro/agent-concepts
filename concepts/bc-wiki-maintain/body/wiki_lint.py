#!/usr/bin/env python3
"""Read-only Markdown wiki lint (stdlib only); qmd paths use a narrow YAML line parser."""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote
WIKI_LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(\s*(?:<([^>\n]+)>|([^\s)\n]+))(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*\)")

def rel(path: Path, vault: Path) -> str:
    return path.relative_to(vault).as_posix()

def text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""

def links(value: str):
    for match in WIKI_LINK_RE.finditer(value):
        target = match.group(1).strip()
        yield target, f"[[{target}]]"
    for match in MD_LINK_RE.finditer(value):
        target = (match.group(1) or match.group(2)).strip()
        yield target, match.group(0)

def skip_link(target: str) -> bool:
    value = target.strip().lower()
    return (not value or value.startswith(("#", "http://", "https://", "mailto:", "//")) or re.match(r"^[a-z][a-z0-9+.-]*:", value) is not None or any(char in target for char in "$`<>{"))

def key(path: Path) -> str:
    return path.with_suffix("").as_posix() if path.suffix.lower() == ".md" else path.as_posix()

def resolve_link(source: Path, target: str, vault: Path, pages: dict[str, Path], stems: dict[str, list[Path]]):
    """Return (page candidates, existing-local-target) or None for skipped links."""
    if skip_link(target):
        return None
    target = unquote(target.strip().split("#", 1)[0].split("?", 1)[0]).strip()
    raw = Path(target)
    variants = [raw] if raw.is_absolute() else [source.parent / raw, vault / raw]
    if target.startswith("wiki/"):
        variants.append(vault / target[5:])
    seen: set[Path] = set()
    local = False
    for candidate in variants:
        candidate = candidate.resolve()
        if candidate in seen:
            continue
        seen.add(candidate)
        found = pages.get(key(candidate.relative_to(vault))) if candidate.is_relative_to(vault) else None
        if found is not None:
            return [found], False
        local |= candidate.exists()
    target_key = key(Path(target.lstrip("/").removeprefix("wiki/")))
    if target_key in pages:
        return [pages[target_key]], False
    if local:
        return [], True
    return stems.get(Path(target_key).name, []), False

def git(repo: Path, *args: str):
    try:
        return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=False)
    except OSError:
        return None

def git_root(vault: Path) -> Path | None:
    result = git(vault, "rev-parse", "--show-toplevel")
    return Path(result.stdout.strip()).resolve() if result and result.returncode == 0 and result.stdout.strip() else None

def git_path(repo: Path, path: Path) -> str | None:
    try:
        return path.resolve().relative_to(repo).as_posix()
    except ValueError:
        return None

def git_date(repo: Path | None, path: Path) -> tuple[str | None, str]:
    if repo is None:
        return None, "not a git repository"
    relative = git_path(repo, path)
    if relative is None:
        return None, "outside git repository"
    result = git(repo, "log", "-1", "--format=%cs", "--", relative)
    value = result.stdout.strip() if result else ""
    return (value, "") if result and result.returncode == 0 and value else (None, "untracked or has no commit")

def promotion_status(vault: Path, repo: Path | None) -> dict:
    log_path = vault / "log.md"
    current_entries = sum(line.startswith("## ") for line in text(log_path).splitlines())
    result = {"count": None, "last_promotion": None, "note": None}
    if repo is None:
        result["note"] = "unknown: not a git repository"
        return result
    relative = git_path(repo, log_path)
    if relative is None:
        result["note"] = "unknown: log.md is outside the git repository"
        return result
    listed = git(repo, "ls-files", "--error-unmatch", "--", relative)
    if not listed or listed.returncode != 0:
        result["note"] = "unknown: log.md is untracked"
        return result
    found = git(repo, "log", "-1", "--format=%H%x00%cs%x00%s", "--grep=^wiki: promote")
    value = found.stdout.strip() if found else ""
    if not value:
        result["count"] = current_entries
        result["note"] = "no wiki: promote commit found; all current log entries are unpromoted"
        return result
    commit, date, subject = value.split("\x00", 2)
    result["last_promotion"] = {"commit": commit, "date": date, "subject": subject}
    diff = git(repo, "diff", "--no-color", "--unified=0", commit, "--", relative)
    if not diff or diff.returncode != 0:
        result["note"] = "unknown: could not compare log.md with last promotion commit"
    else:
        result["count"] = sum(line.startswith("+## ") for line in diff.stdout.splitlines())
    return result

def qmd_status(vault: Path) -> dict:
    registry = Path.home() / "Sync" / "Scripts" / "config" / "qmd-collections.yml"
    result = {"registered": False, "intentional_exclusion": False, "registry": str(registry), "reason": None}
    if not registry.exists():
        result["reason"] = "registry file is missing; skipped"
        return result
    path_re = re.compile(r"^\s+path:\s*(?:\"([^\"]+)\"|'([^']+)'|(\S.*?))\s*$")
    for line in text(registry).splitlines():
        match = path_re.match(line)
        if not match:
            continue
        value = next(group for group in match.groups() if group is not None)
        registered = Path(os.path.expandvars(value).strip()).expanduser().resolve()
        try:
            vault.relative_to(registered)
        except ValueError:
            continue
        result["registered"], result["reason"] = True, f"covered by {registered}"
        return result
    for line in text(vault / "project" / "overview.md").splitlines():
        if "excluded from the global qmd index" in line.lower():
            result.update(intentional_exclusion=True, reason=line.strip())
            return result
    result["reason"] = "vault path is absent from qmd registry"
    return result

SKIP_DIR_NAMES = {".git", ".obsidian", "scratch", "temp", "node_modules", "vendor"}

def maintenance_report(path: Path, vault: Path) -> bool:
    item = path.relative_to(vault)
    return len(item.parts) >= 2 and item.parts[0] == "_meta" and item.name.startswith(("lint-", "health-check-", "semantic-consolidation-"))

def ignored_path(path: Path, vault: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.relative_to(vault).parts)

def lint(vault: Path, stale_days: int) -> dict:
    pages_list = sorted(
        path
        for path in (item.resolve() for item in vault.rglob("*.md"))
        if path.is_relative_to(vault) and not ignored_path(path, vault)
    )
    pages = {key(path.relative_to(vault)): path for path in pages_list}
    stems: dict[str, list[Path]] = {}
    for path in pages_list:
        stems.setdefault(path.stem, []).append(path)
    incoming, broken, ambiguous = dict.fromkeys(pages_list, 0), [], []
    for path in pages_list:
        # Templates hold example links on purpose; do not fail the vault on them.
        if "templates" in path.relative_to(vault).parts:
            continue
        for target, display in links(text(path)):
            resolution = resolve_link(path, target, vault, pages, stems)
            if resolution is None:
                continue
            candidates, local = resolution
            if len(candidates) == 1:
                incoming[candidates[0]] += 1
            elif len(candidates) > 1:
                ambiguous.append({"page": rel(path, vault), "link": display, "candidates": [rel(item, vault) for item in candidates]})
            elif not local:
                broken.append({"page": rel(path, vault), "link": display})
    index_text, index_path = text(vault / "index.md"), (vault / "index.md").resolve()
    missing = [rel(path, vault) for path in pages_list if path != index_path and not maintenance_report(path, vault) and rel(path, vault) not in index_text and path.stem not in index_text]
    orphans = [rel(path, vault) for path, count in incoming.items() if count == 0 and path.name not in {"index.md", "log.md"} and "templates" not in path.parts and not maintenance_report(path, vault)]

    stale, unknown, active, repo = [], [], vault / "tasks" / "active.md", git_root(vault)
    if active.exists():
        referenced = set()
        for target, _display in links(text(active)):
            resolution = resolve_link(active.resolve(), target, vault, pages, stems)
            if resolution and len(resolution[0]) == 1:
                referenced.add(resolution[0][0])
        today = dt.date.today()
        for path in sorted(referenced):
            committed, reason = git_date(repo, path)
            if committed is None:
                unknown.append({"page": rel(path, vault), "reason": reason})
                continue
            age = (today - dt.date.fromisoformat(committed)).days
            if age > stale_days:
                stale.append({"page": rel(path, vault), "last_modified": committed, "age_days": age})
    return {"vault": str(vault), "pages": len(pages_list), "broken_links": broken, "ambiguous_links": ambiguous,
            "orphans": orphans, "missing_index": missing, "stale_active_references": stale,
            "unknown_active_references": unknown, "stale_days": stale_days,
            "unpromoted_log": promotion_status(vault, repo), "qmd": qmd_status(vault)}

def print_report(report: dict) -> None:
    print("# Wiki lint report")
    print(f"Vault: {report['vault']}\nPages: {report['pages']}")
    checks = (("broken_links", "Broken links"), ("ambiguous_links", "Ambiguous links"), ("orphans", "Orphan pages"), ("missing_index", "Possibly missing from index"))
    for name, label in checks:
        entries = report[name]
        print(f"{label}: {len(entries)}")
        for entry in entries:
            if isinstance(entry, str):
                print(f"- {entry}")
            elif name == "ambiguous_links":
                print(f"- {entry['page']} -> {entry['link']} could be {', '.join(entry['candidates'])}")
            else:
                print(f"- {entry['page']} -> {entry['link']}")
    stale = report["stale_active_references"]
    print(f"Stale pages referenced from tasks/active.md (>{report['stale_days']} days): {len(stale)}")
    for entry in stale:
        print(f"- {entry['page']} — {entry['last_modified']} ({entry['age_days']} days)")
    unknown = report["unknown_active_references"]
    print(f"Unknown active references: {len(unknown)}")
    for entry in unknown:
        print(f"- {entry['page']} — {entry['reason']}")
    promotion = report["unpromoted_log"]
    print(f"Unpromoted log entries: {promotion['count'] if promotion['count'] is not None else 'unknown'}")
    if promotion["last_promotion"]:
        print(f"- Last promotion: {promotion['last_promotion']['date']} {promotion['last_promotion']['subject']}")
    if promotion["note"]:
        print(f"- {promotion['note']}")
    qmd = report["qmd"]
    status = "registered" if qmd["registered"] else "intentional exclusion" if qmd["intentional_exclusion"] else "unregistered"
    print(f"qmd registration: {status}")
    if qmd["reason"]:
        print(f"- {qmd['reason']}")
    # Machine-readable contract consumed by runner/run-promotion.sh. Fails closed:
    # an unknown count means git could not answer, so do not licence an unattended write.
    print(f"PROMOTION_REQUIRED={1 if promotion['count'] else 0}")

def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Markdown wiki lint")
    parser.add_argument("vault_root", help="wiki/vault directory to inspect")
    parser.add_argument("--stale-days", type=int, default=90, help="staleness threshold (default: 90)")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()
    if args.stale_days < 0:
        parser.error("--stale-days must be non-negative")
    vault = Path(args.vault_root).expanduser().resolve()
    if not vault.is_dir():
        parser.error(f"vault root is not a directory: {vault}")
    report = lint(vault, args.stale_days)
    report["promotion_required"] = bool(report["unpromoted_log"]["count"])
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_report(report)
    return 1 if report["broken_links"] or report["ambiguous_links"] else 0

if __name__ == "__main__":
    sys.exit(main())
