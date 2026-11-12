#!/usr/bin/env python3
"""Read-only Markdown wiki lint (stdlib only); qmd paths use a narrow YAML line parser."""
from __future__ import annotations
import argparse
from collections import Counter
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
INLINE_CODE_RE = re.compile(r"(`+)([^`\n]*?)\1")
FENCE_RE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")
LOG_HEADING_RE = re.compile(r"^## (.+?)\s*$")
LOG_DATED_HEADING_RE = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})\](?:\s|$)")


def without_code(value: str) -> str:
    """Mask fenced blocks and inline code while preserving line structure."""
    visible: list[str] = []
    fence_char: str | None = None
    fence_length = 0
    for line in value.splitlines(keepends=True):
        match = FENCE_RE.match(line)
        if fence_char is not None:
            if match and match.group(1)[0] == fence_char and len(match.group(1)) >= fence_length:
                fence_char = None
                fence_length = 0
            visible.append("\n" if line.endswith("\n") else "")
            continue
        if match:
            fence_char = match.group(1)[0]
            fence_length = len(match.group(1))
            visible.append("\n" if line.endswith("\n") else "")
            continue
        visible.append(INLINE_CODE_RE.sub(lambda match: "".join("\n" if char == "\n" else " " for char in match.group(0)), line))
    return "".join(visible)


def log_headings(value: str) -> list[tuple[str, str | None]]:
    headings = []
    for line in without_code(value).splitlines():
        line = line.rstrip()
        if not LOG_HEADING_RE.match(line):
            continue
        dated = LOG_DATED_HEADING_RE.match(line)
        date = None
        if dated:
            try:
                dt.date.fromisoformat(dated.group(1))
            except ValueError:
                pass
            else:
                date = dated.group(1)
        headings.append((line, date))
    return headings

def rel(path: Path, vault: Path) -> str:
    return path.relative_to(vault).as_posix()

def text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""

def links(value: str):
    value = without_code(value)
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
    current_headings = log_headings(text(log_path))
    result = {
        "count": None,
        "range": None,
        "last_promotion": None,
        "note": None,
        "headings": [],
        "undatable_headings": [],
    }
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

    # Promotion commits do not touch log.md, so scope the subject search by the
    # vault directory instead of using a path-limited git log.
    promotion_log = git(repo, "log", "--format=%H%x00%cs%x00%s", "--grep=^wiki: promote")
    promotion_record = None
    vault_prefix = str(Path(relative).parent)
    if promotion_log and promotion_log.returncode == 0:
        for record in promotion_log.stdout.splitlines():
            fields = record.split("\x00", 2)
            if len(fields) != 3:
                continue
            commit, date, subject = fields
            touched = git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", commit, "--", vault_prefix)
            if touched and touched.returncode == 0 and touched.stdout.strip():
                promotion_record = (commit, date, subject)
                break

    if promotion_record is None:
        unpromoted = current_headings
        result["count"] = len(unpromoted)
        result["note"] = "no wiki: promote log entries commit found; all current log entries are unpromoted"
    else:
        commit, date, subject = promotion_record
        result["last_promotion"] = {"commit": commit, "date": date, "subject": subject}
        previous = git(repo, "show", f"{commit}:{relative}")
        if not previous or previous.returncode != 0:
            result["note"] = "unknown: could not compare log.md with last promotion commit"
            unpromoted = []
        else:
            previous_headings = log_headings(previous.stdout)
            unpromoted = [
                heading
                for heading, remaining in Counter(current_headings).items()
                for _ in range(max(0, remaining - Counter(previous_headings)[heading]))
            ]
            result["count"] = len(unpromoted)
    result["headings"] = [heading for heading, _date in unpromoted]
    result["undatable_headings"] = [heading for heading, date in unpromoted if date is None]
    if result["count"] is not None and result["count"] > 0:
        dates = [date for _heading, date in unpromoted if date is not None]
        if dates:
            result["range"] = f"{min(dates)}..{max(dates)}"
    return result

def qmd_paths(registry: Path) -> list[Path]:
    path_re = re.compile(r"^\s+path:\s*(?:\"([^\"]+)\"|'([^']+)'|(\S.*?))\s*$")
    paths = []
    for line in text(registry).splitlines():
        match = path_re.match(line)
        if not match:
            continue
        value = next(group for group in match.groups() if group is not None)
        paths.append(Path(os.path.expandvars(value).strip()).expanduser().resolve())
    return paths


def qmd_collections(registry: Path) -> list[dict]:
    """Collections of a qmd collections file as {name, path, pattern}; narrow line parser."""
    name_re = re.compile(r"^  ([^\s#][^:]*):\s*$")
    field_re = re.compile(r"^    (path|pattern):\s*(?:\"([^\"]+)\"|'([^']+)'|(\S.*?))\s*$")
    found: list[dict] = []
    for line in text(registry).splitlines():
        name = name_re.match(line)
        if name:
            found.append({"name": name.group(1).strip().strip("\"'"), "path": None, "pattern": "**/*.md"})
            continue
        field = field_re.match(line)
        if field and found:
            value = next(group for group in field.groups()[1:] if group is not None)
            if field.group(1) == "path":
                found[-1]["path"] = Path(os.path.expandvars(value).strip()).expanduser().resolve()
            else:
                found[-1]["pattern"] = value.strip()
    return [collection for collection in found if collection["path"] is not None]


def qmd_covering_path(vault: Path, paths: list[Path]) -> Path | None:
    for registered in paths:
        try:
            vault.relative_to(registered)
        except ValueError:
            continue
        return registered
    return None


def qmd_status(
    vault: Path,
    registry: Path | None = None,
    machine_index: Path | None = None,
) -> dict:
    registry = registry or Path.home() / "Sync" / "Scripts" / "config" / "qmd-collections.yml"
    machine_index = machine_index or Path.home() / ".config" / "qmd" / "index.yml"
    result = {
        "registered": False,
        "unindexed": False,
        "intentional_exclusion": False,
        "registry": str(registry),
        "machine_index": str(machine_index),
        "canonical_path": None,
        "machine_path": None,
        "reason": None,
    }
    if not registry.exists():
        result["reason"] = "registry file is missing; skipped"
        return result

    canonical_path = qmd_covering_path(vault, qmd_paths(registry))
    result["canonical_path"] = str(canonical_path) if canonical_path else None
    if canonical_path is None:
        for line in text(vault / "project" / "overview.md").splitlines():
            if "excluded from the global qmd index" in line.lower():
                result.update(intentional_exclusion=True, reason=line.strip())
                return result
        if machine_index.exists():
            machine_path = qmd_covering_path(vault, qmd_paths(machine_index))
            result["machine_path"] = str(machine_path) if machine_path else None
            result["reason"] = (
                f"vault path is absent from canonical qmd registry; machine index covers {machine_path}"
                if machine_path
                else "vault path is absent from qmd registry"
            )
        else:
            result["reason"] = (
                "vault path is absent from qmd registry; "
                f"machine index unavailable at {machine_index}"
            )
        return result

    if not machine_index.exists():
        result["registered"] = True
        result["reason"] = (
            f"covered by canonical path {canonical_path}; machine index unavailable at {machine_index}; "
            "reporting canonical-only coverage"
        )
        return result

    machine_path = qmd_covering_path(vault, qmd_paths(machine_index))
    result["machine_path"] = str(machine_path) if machine_path else None
    if machine_path:
        result["registered"] = True
        result["reason"] = f"covered by canonical path {canonical_path} and machine index path {machine_path}"
    else:
        result["unindexed"] = True
        result["reason"] = (
            f"covered by canonical path {canonical_path}; machine index lacks a covering path at {machine_index}"
        )
    return result

QMD_EXCLUSION_TEXT = "excluded from the global qmd index"


def visible_qmd_status(vault: Path, table: dict[str, str], registry: Path, machine_index: Path) -> dict:
    """Registration of a visible-layout project: the two collections `--qmd-entry` prints.

    qmd skips every hidden path part, so one collection rooted at the repository cannot
    index `.bc-agent/`; the mechanics need their own collection rooted there.
    """
    project, pattern = vault.parent, knowledge_pattern(table)
    result = {
        "registered": False, "unindexed": False, "intentional_exclusion": False,
        "registry": str(registry), "machine_index": str(machine_index),
        "canonical_path": None, "machine_path": None, "reason": None,
        "knowledge_pattern": pattern,
    }
    if not registry.exists():
        result["reason"] = "registry file is missing; skipped"
        return result

    def missing(collections: list[dict]) -> list[str]:
        problems = []
        rooted = [collection for collection in collections if collection["path"] == project]
        if not any(collection["pattern"] == pattern for collection in rooted):
            problems.append(
                f"collection {rooted[0]['name']} at {project} has pattern {rooted[0]['pattern']}; "
                f"the table expects {pattern}" if rooted else
                f"no collection rooted at {project} with pattern {pattern}")
        if not any(collection["path"] == vault for collection in collections):
            problems.append(f"no collection rooted at {vault}")
        return problems

    canonical = missing(qmd_collections(registry))
    if canonical:
        for line in text(vault / "AGENTS.md").splitlines():
            if QMD_EXCLUSION_TEXT in line.lower():
                result.update(intentional_exclusion=True, reason=line.strip())
                return result
        result["reason"] = ("; ".join(canonical) + "; print the entry with "
                            "`wiki_lint.py <vault-root> --qmd-entry <slug>`")
        return result
    result["canonical_path"] = str(project)
    if not machine_index.exists():
        result["registered"] = True
        result["reason"] = (f"both collections are in the canonical registry; machine index unavailable at "
                            f"{machine_index}; reporting canonical-only coverage")
        return result
    machine = missing(qmd_collections(machine_index))
    if machine:
        result["unindexed"] = True
        result["reason"] = "both collections are in the canonical registry; machine index: " + "; ".join(machine)
    else:
        result["registered"] = True
        result["machine_path"] = str(project)
        result["reason"] = f"knowledge collection at {project} and mechanics collection at {vault} in both registries"
    return result


# --- visible layout ------------------------------------------------------------
# Copied verbatim from concepts/bc-init-agent/body/scaffold.py, which owns the
# "Where things go" table contract. Copied rather than imported because a skill
# body can be deployed as a copy without its sibling concept;
# tests/test_visible_layout_lint.py fails when the two copies differ.
WHERE_THINGS_GO_HEADING = "## Where things go"
_WHERE_THINGS_GO_LINE = re.compile(r"^" + re.escape(WHERE_THINGS_GO_HEADING) + r"[ \t]*\r?$", re.M)
_UNDECIDED_PATH_CELLS = {"", "—", "-"}


def parse_where_things_go(text: str) -> dict[str, str]:
    """Map each role key of a "Where things go" table to its path.

    Paths are relative to the project root. A backticked path is unwrapped; a plain
    path is returned stripped; only `—`, `-` or an empty cell means "no decided path"
    and maps to an empty string. Raises ValueError when the heading line is missing,
    when the section has no table rows, or when a role appears twice.
    """
    match = _WHERE_THINGS_GO_LINE.search(text)
    if not match:
        raise ValueError(f"no {WHERE_THINGS_GO_HEADING!r} section")
    section = re.split(r"^## ", text[match.end():], maxsplit=1, flags=re.M)[0]
    result: dict[str, str] = {}
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 2 or cells[0] == "Role" or set(cells[0]) <= {"-", ":", " "}:
            continue
        role, path = cells[0], cells[1]
        if role in result:
            raise ValueError(f"role {role!r} appears twice in {WHERE_THINGS_GO_HEADING!r}")
        if path.count("`") >= 2:
            path = path.split("`")[1].strip()
        result[role] = "" if path in _UNDECIDED_PATH_CELLS else path
    if not result:
        raise ValueError(f"{WHERE_THINGS_GO_HEADING!r} section has no table rows")
    return result


def layout_table(vault: Path) -> dict[str, str] | None:
    """Return the role table when VAULT is the `.bc-agent/` of a visible-layout project."""
    # Locate the heading outside code fences, so a vault AGENTS.md that quotes the
    # visible protocol in a fence stays a vault. The copied parser itself stays
    # verbatim (the drift test compares it), so it is handed the text from that line.
    raw = text(vault / "AGENTS.md").splitlines(keepends=True)
    masked = without_code("".join(raw)).splitlines(keepends=True)
    start = next((index for index, line in enumerate(masked) if _WHERE_THINGS_GO_LINE.match(line)), None)
    if start is None:
        return None
    try:
        return parse_where_things_go("".join(raw[start:]))
    except ValueError:
        return None


WORK_STAGE_ROLES = ("work-planned", "work-active", "work-done", "work-dropped")
# Roles whose paths the project's search collection indexes, in pattern order, with the
# authority context a search hit carries for a folder role (None: a single file).
SEARCH_ROLE_CONTEXTS = (
    ("glossary", None),
    ("decisions", "Decision records — binding unless superseded"),
    ("research", "Dated investigations and architecture reviews — evidence, not authoritative"),
    ("requirements", None),
    ("architecture", None),
    ("components", "Verified state of real systems, dated"),
    ("ideas", None),
    ("work-planned", "Work items agreed but not started; the folder is the status"),
    ("work-active", "Work items in progress"),
    ("work-done", "Finished work items by month, each with its Outcome"),
    ("work-dropped", "Dropped work and rejected requests with the reason — check before proposing similar work"),
)


def search_paths(table: dict[str, str]) -> list[tuple[str, str, str | None]]:
    """(glob, role path, context) for each searchable role with a visible path."""
    found: list[tuple[str, str, str | None]] = []
    for role, context in SEARCH_ROLE_CONTEXTS:
        path = table.get(role, "").strip().removeprefix("./")
        if not path or path.startswith("."):
            continue  # undecided, or hidden: qmd skips hidden paths, and `.bc-agent/` has its own collection
        folder = path.endswith("/") or not Path(path).suffix
        glob = path.rstrip("/") + "/**/*.md" if folder else path
        if glob not in (item[0] for item in found):
            found.append((glob, path.rstrip("/"), context if folder else None))
    return found


def knowledge_pattern(table: dict[str, str]) -> str:
    """The qmd pattern of the project's knowledge collection, built from the table."""
    globs = [glob for glob, _path, _context in search_paths(table)]
    return "{" + ",".join(globs) + "}" if len(globs) > 1 else (globs[0] if globs else "")


def registry_path(path: Path) -> str:
    """A path as the synced collections file writes it: `~/` under the home folder."""
    try:
        return "~/" + path.relative_to(Path.home().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def qmd_entry(vault: Path, table: dict[str, str], slug: str) -> str:
    """Collections-file entries for a visible-layout project: knowledge, then mechanics."""
    project = vault.parent
    mechanics = [
        f"  {slug}:", f"    path: {registry_path(vault)}", '    pattern: "**/*.md"', "    ignore: []", "    contexts:",
        f'      "/": "Agent mechanics for {slug}: session protocol and Where things go table, map, journal log"',
        '      "/conventions": "Validation, git, layout and workflow norms — follow these"',
        '      "/references": "Recurring commands, paths, gotchas"',
    ]
    knowledge = [
        f"  {slug}-project:", f"    path: {registry_path(project)}", f'    pattern: "{knowledge_pattern(table)}"',
        "    ignore: []", "    contexts:",
        f'      "/": "Project knowledge for {slug}: glossary, work items (the folder is the status), decisions, research"',
    ]
    knowledge += [f'      "/{path}": "{context}"' for _glob, path, context in search_paths(table) if context]
    return "\n".join(mechanics + [""] + knowledge) + "\n"
# Three or more digits, never all zeros: numbering starts at 001 and continues past 999.
WORK_ITEM_NAME_RE = re.compile(r"^(?!0+-)(\d{3,})-[A-Za-z0-9][A-Za-z0-9._-]*$")
MONTH_FOLDER_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
STATUS_LINE_RE = re.compile(r"^[ \t]*(?:[-*][ \t]+)?\**Status\**[ \t]*:", re.M | re.I)


def finding(severity: str, check: str, path: Path, project: Path, problem: str, fix: str) -> dict:
    return {"severity": severity, "check": check, "path": rel(path, project), "problem": problem, "fix": fix}


def folder_entries(folder: Path, project: Path, found: list[dict]) -> list[Path]:
    """Candidate items directly in a stage or month folder.

    `README.md` documents the folder and is not an item. Any other non-Markdown file is
    reported as a warning and not scanned, since it can be neither an item nor read as one.
    """
    entries: list[Path] = []
    for entry in sorted(folder.iterdir()):
        if entry.name.startswith(".") or entry.name == "README.md":
            continue
        if entry.is_file() and entry.suffix != ".md":
            found.append(finding("warning", "non-markdown", entry, project,
                                 "non-Markdown file sits directly in a work stage folder.",
                                 "move it into the folder item it belongs to, or out of the work folders"))
            continue
        entries.append(entry)
    return entries


def stage_items(stage: Path, done: bool, project: Path, found: list[dict]) -> list[Path]:
    """Items in one stage folder; in the done folder, items sit inside month folders."""
    entries = folder_entries(stage, project, found) if stage.is_dir() else []
    if not done:
        return entries
    items: list[Path] = []
    for entry in entries:
        if entry.is_dir() and MONTH_FOLDER_RE.match(entry.name):
            items.extend(folder_entries(entry, project, found))
        elif entry.is_dir() and not WORK_ITEM_NAME_RE.match(entry.name):
            found.append(finding("error", "done-month-folder", entry, project,
                                 "month folder name is not YYYY-MM.", "rename it to the item's finishing month, e.g. 2026-03"))
            items.extend(folder_entries(entry, project, found))
        else:
            found.append(finding("error", "done-month-folder", entry, project,
                                 "item sits directly in the done folder.", "git mv it into a <year>-<month>/ folder"))
            items.append(entry)
    return items


def role_notes(agents_text: str, role: str) -> str:
    """Notes cell of ROLE's table row; the shared parser returns paths only."""
    match = re.search(r"^\|\s*" + re.escape(role) + r"\s*\|[^|\n]*\|(.*)$", agents_text, re.M)
    return match.group(1) if match else ""


def outcome_filled(content: str) -> bool:
    """True when `## Outcome` has text other than comments or the template's `<...>` placeholder."""
    match = re.search(r"^## Outcome[ \t]*$", content, re.M)
    if not match:
        return False
    section = re.split(r"^#{1,2} ", content[match.end():], maxsplit=1, flags=re.M)[0]
    section = re.sub(r"<!--.*?-->", "", section, flags=re.S)
    return any(line.strip() and not re.fullmatch(r"<[^>]*>", line.strip()) for line in section.splitlines())


def item_name_number(item: Path) -> int | None:
    name = item.name if item.is_dir() else item.stem if item.suffix == ".md" else ""
    match = WORK_ITEM_NAME_RE.match(name)
    return int(match.group(1)) if match else None


def work_findings(project: Path, table: dict[str, str], agents_text: str) -> list[dict]:
    """Check the work folders named by the table; errors break the layout's rules."""
    found: list[dict] = []
    numbered: dict[int, list[Path]] = {}
    seen_stages: set[Path] = set()
    for role in WORK_STAGE_ROLES:
        if not table.get(role):
            continue
        stage = (project / table[role]).resolve()
        if stage in seen_stages:
            continue  # two roles hand-edited to one path: count its items once
        seen_stages.add(stage)
        for item in stage_items(project / table[role], role == "work-done", project, found):
            number = item_name_number(item)
            if number is not None:
                numbered.setdefault(number, []).append(item)
            if number is None:
                found.append(finding("warning", "item-name", item, project,
                                     "item name is not <number of three or more digits, from 001>-<slug>.",
                                     "git mv it to NNN-slug.md (or NNN-slug/) using the next free number"))
            body = item / "plan.md" if item.is_dir() else item
            if item.is_dir() and not body.is_file():
                found.append(finding("warning", "missing-plan", item, project,
                                     "folder item has no plan.md.",
                                     "add plan.md from the work-item template"))
            content = without_code(text(body)) if body.is_file() else ""
            for page in sorted(item.rglob("*.md")) if item.is_dir() else [item]:
                if STATUS_LINE_RE.search(without_code(text(page))):
                    found.append(finding("error", "status-line", page, project,
                                         "item has a Status: line; the folder is the status.",
                                         "delete the Status: line"))
            if role in {"work-done", "work-dropped"} and not outcome_filled(content):
                found.append(finding("error", "missing-outcome", body, project,
                                     "finished or dropped item has no filled ## Outcome section.",
                                     "write what happened, or why it was dropped, under ## Outcome"))
    for role, path in table.items():
        if role == AGENT_EXTRAS_ROLE:
            continue  # a list of `.bc-agent/` entries, checked by agent_mechanics_findings
        if not path or (project / path).exists() or "created on first need" in role_notes(agents_text, role).lower():
            continue
        found.append(finding("warning", "role-path", project / path, project,
                             f"the {role} path in the Where things go table does not exist.",
                             "create it, or correct the path in .bc-agent/AGENTS.md"))
    found.extend(agent_mechanics_findings(project, table, agents_text))
    for number, items in sorted(numbered.items()):
        if len(items) > 1:
            for item in items:
                found.append(finding("error", "duplicate-number", item, project,
                                     f"number {number:03d} is used by {len(items)} items.",
                                     "renumber the later item to the highest number in any stage plus one"))
    return found


# `.bc-agent/` holds agent mechanics only (owner decision 2026-11-12, after `prototype`
# kept writing to a scratch folder the user named). Every other direct entry is an error.
AGENT_MECHANICS_ENTRIES = {"AGENTS.md", "map.md", "log.md", "conventions", "references", "templates"}
# Folders a hosted teach workspace owns under `.bc-agent/` (bc-init-agent's
# teach-workspace row); its index.md catalogs these and nothing else.
TEACH_OWNED_DIRS = {"learning", "sources", "concepts", "sessions", "questions"}
# What bc-init-agent's scaffold writes under `.bc-agent/` for the hosted teach workspace of
# a hybrid project; tests/test_visible_layout_lint.py fails when the scaffold differs.
HYBRID_TEACH_ENTRIES = TEACH_OWNED_DIRS | {"index.md"}
AGENT_EXTRAS_ROLE = "agent-extras"
TEACH_WORKSPACE_ROLE = "teach-workspace"


def agent_extras(agents_text: str) -> set[str]:
    """Entry names a project declares in its optional agent-extras row.

    Read from the raw Path cell, because the shared parser keeps only the first
    backticked path and this cell lists several, comma-separated.
    """
    match = re.search(r"^\|\s*" + re.escape(AGENT_EXTRAS_ROLE) + r"\s*\|([^|\n]*)\|", agents_text, re.M)
    if not match:
        return set()
    names = set()
    for item in match.group(1).split(","):
        item = item.strip().strip("`").strip().removeprefix("./").removeprefix(".bc-agent/").strip("/")
        if item:
            names.add(item.split("/", 1)[0])
    return names


def agent_mechanics_findings(project: Path, table: dict[str, str], agents_text: str) -> list[dict]:
    """Errors for entries directly under `.bc-agent/` that are not agent mechanics.

    Hidden entries are skipped (`.gitkeep`, `.DS_Store`), except `.obsidian/`: the
    Obsidian settings are retired in this layout, so a leftover one is reported.
    """
    vault = project / ".bc-agent"
    allowed = AGENT_MECHANICS_ENTRIES | agent_extras(agents_text)
    if table.get(TEACH_WORKSPACE_ROLE):
        allowed |= HYBRID_TEACH_ENTRIES
    found = []
    for entry in sorted(vault.iterdir()) if vault.is_dir() else []:
        if entry.name in allowed or (entry.name.startswith(".") and entry.name != ".obsidian"):
            continue
        found.append(finding("error", "agent-mechanics", entry, project,
                             "not agent mechanics: project knowledge lives at the table's role paths; "
                             "`.bc-agent/` holds agent mechanics only.",
                             "move it to the role path in the Where things go table (for example the research "
                             "folder), delete it, or list it in an agent-extras row if a tool reads it there"))
    return found


SKIP_DIR_NAMES = {".git", ".obsidian", "scratch", "temp", "node_modules", "vendor"}

def maintenance_report(path: Path, vault: Path) -> bool:
    item = path.relative_to(vault)
    return len(item.parts) >= 2 and item.parts[0] == "_meta" and item.name.startswith(("lint-", "health-check-", "semantic-consolidation-"))

def ignored_path(path: Path, vault: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.relative_to(vault).parts)

def lint(
    vault: Path,
    stale_days: int,
    *,
    qmd_registry: Path | None = None,
    qmd_machine_index: Path | None = None,
) -> dict:
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
        # log.md is append-only evidence, not a graph source; its links may be historical or cross-vault.
        if path.name == "log.md":
            continue
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
    table = layout_table(vault)
    index_text, index_path = text(vault / "index.md"), (vault / "index.md").resolve()
    # A visible-layout project has no vault catalog; only a hosted teach workspace
    # keeps an index.md, and it catalogs teach's own folders, not agent mechanics.
    index_scope = [
        path for path in pages_list
        if table is None or (index_path.exists() and path.relative_to(vault).parts[0] in TEACH_OWNED_DIRS)
    ]
    missing = [rel(path, vault) for path in index_scope if path != index_path and not maintenance_report(path, vault) and rel(path, vault) not in index_text and path.stem not in index_text]
    orphans = [rel(path, vault) for path, count in incoming.items() if count == 0 and path.name not in {"index.md", "log.md"} and "templates" not in path.parts and not maintenance_report(path, vault)]

    stale, unknown, active, repo = [], [], vault / "tasks" / "active.md", git_root(vault)
    if table is None and active.exists():
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
    return {"vault": str(vault), "layout": "vault" if table is None else "visible",
            "work_findings": [] if table is None else work_findings(vault.parent, table, text(vault / "AGENTS.md")),
            "pages": len(pages_list), "broken_links": broken, "ambiguous_links": ambiguous,
            "orphans": orphans, "missing_index": missing, "stale_active_references": stale,
            "unknown_active_references": unknown, "stale_days": stale_days,
            # Promotion moved log entries into vault pages; in the visible layout agents write to
            # the role folders directly and log.md is a plain journal, so there is nothing to promote.
            "unpromoted_log": promotion_status(vault, repo) if table is None else None,
            "qmd": qmd_status(vault, registry=qmd_registry, machine_index=qmd_machine_index) if table is None
            else visible_qmd_status(vault, table,
                                    qmd_registry or Path.home() / "Sync" / "Scripts" / "config" / "qmd-collections.yml",
                                    qmd_machine_index or Path.home() / ".config" / "qmd" / "index.yml"),
        }

CLASSIFY_VERDICTS = {"promote", "skip", "conflict"}


def verify_classification(path: Path, promotion: dict) -> tuple[list[str], list[dict]]:
    """Return errors and rows for FILE against every unpromoted heading, exactly once."""
    if promotion["count"] is None:
        note = promotion["note"] or "the unpromoted heading list could not be computed"
        return ([f"cannot verify classification: {note}"], [])
    headings = promotion["headings"]
    if not path.is_file():
        return ([f"classification file does not exist: {path}"], [])
    errors: list[str] = []
    seen: list[str] = []
    rows: list[dict] = []
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        return ([f"could not read classification file: {exc}"], [])
    for lineno, line in enumerate(raw.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {lineno}: invalid JSON ({exc})")
            continue
        if not isinstance(row, dict):
            errors.append(f"line {lineno}: expected a JSON object")
            continue
        heading = row.get("heading")
        verdict = row.get("verdict")
        reason = row.get("reason")
        page = row.get("page")
        if not isinstance(heading, str) or not heading.strip():
            errors.append(f"line {lineno}: heading must be a non-empty string")
            heading = None
        if verdict not in CLASSIFY_VERDICTS:
            errors.append(f"line {lineno}: verdict must be promote, skip, or conflict")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"line {lineno}: reason must be a non-empty string")
        if verdict in {"promote", "conflict"} and (not isinstance(page, str) or not page.strip()):
            errors.append(f"line {lineno}: page is required for {verdict}")
        if heading is not None:
            seen.append(heading)
            rows.append({"heading": heading, "verdict": verdict, "reason": reason, "page": page})
    expected = Counter(headings)
    found = Counter(seen)
    if expected != found:
        missing = list((expected - found).elements())
        extra = list((found - expected).elements())
        if missing:
            errors.append("missing headings:")
            errors.extend(f"- {item}" for item in missing)
        if extra:
            errors.append("unexpected headings:")
            errors.extend(f"- {item}" for item in extra)
    return errors, rows


def classification_summary(rows: list[dict]) -> str:
    """Render verdicts for the promotion commit body, so skip reasons outlive the temp file."""
    counts = Counter(row["verdict"] for row in rows)
    header = "Classification: " + ", ".join(
        f"{counts[verdict]} {verdict}" for verdict in sorted(CLASSIFY_VERDICTS)
    )
    lines = [header, ""]
    for row in rows:
        flat = {key: " ".join(str(value).split()) for key, value in row.items() if value is not None}
        target = f" -> {flat['page']}" if flat.get("page") else ""
        lines.append(f"{flat['verdict']} {flat['heading']}{target}: {flat['reason']}")
    return "\n".join(lines)


def print_report(report: dict) -> None:
    print("# Wiki lint report")
    visible = report["layout"] == "visible"
    print(f"Vault: {report['vault']}\nLayout: {report['layout']}\nPages: {report['pages']}")
    checks = [("broken_links", "Broken links"), ("ambiguous_links", "Ambiguous links"), ("orphans", "Orphan pages")]
    if not visible or (Path(report["vault"]) / "index.md").exists():
        checks.append(("missing_index", "Possibly missing from index" if not visible else "Teach pages possibly missing from index"))
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
    if visible:
        for severity, label in (("error", "Work-folder errors"), ("warning", "Work-folder warnings")):
            entries = [entry for entry in report["work_findings"] if entry["severity"] == severity]
            print(f"{label}: {len(entries)}")
            for entry in entries:
                print(f"- {entry['path']} — {entry['problem']} Fix: {entry['fix']}")
    else:
        stale = report["stale_active_references"]
        print(f"Stale pages referenced from tasks/active.md (>{report['stale_days']} days): {len(stale)}")
        for entry in stale:
            print(f"- {entry['page']} — {entry['last_modified']} ({entry['age_days']} days)")
        unknown = report["unknown_active_references"]
        print(f"Unknown active references: {len(unknown)}")
        for entry in unknown:
            print(f"- {entry['page']} — {entry['reason']}")
    promotion = report["unpromoted_log"]
    if promotion is None:
        print(f"Promotion: {PROMOTION_NOT_APPLICABLE}")
    else:
        print_promotion(promotion)
    qmd = report["qmd"]
    status = (
        "registered"
        if qmd["registered"]
        else "unindexed"
        if qmd["unindexed"]
        else "intentional exclusion"
        if qmd["intentional_exclusion"]
        else "unregistered"
    )
    print(f"qmd registration: {status}")
    if qmd["reason"]:
        print(f"- {qmd['reason']}")
    if promotion is None:
        return
    # Machine-readable contract consumed by runner/run-promotion.sh. Fails closed:
    # an unknown count means git could not answer, so do not license an unattended write.
    required = 1 if promotion["count"] is None or promotion["count"] > 0 else 0
    promotion_range = promotion["range"] if promotion["range"] else "invalid" if required else "none"
    print(f"PROMOTION_REQUIRED={required}")
    print(f"PROMOTION_RANGE={promotion_range}")
    for heading in promotion.get("headings") or []:
        print(f"PROMOTION_HEADING\t{heading}")


PROMOTION_NOT_APPLICABLE = (
    "not applicable (visible layout: agents write decisions and research to the table's role "
    "folders, and log.md is a plain journal)"
)


def print_promotion(promotion: dict) -> None:
    print(f"Unpromoted log entries: {promotion['count'] if promotion['count'] is not None else 'unknown'}")
    if promotion["last_promotion"]:
        print(f"- Last promotion: {promotion['last_promotion']['date']} {promotion['last_promotion']['subject']}")
    if promotion["note"]:
        print(f"- {promotion['note']}")
    for heading in promotion.get("headings") or []:
        print(f"- {heading}")
    undatable = promotion.get("undatable_headings") or []
    if undatable:
        print(f"Warning: undatable unpromoted log headings: {len(undatable)}")
        for heading in undatable:
            print(f"- {heading}")

def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Markdown wiki lint")
    parser.add_argument("vault_root", help="wiki/vault directory to inspect")
    parser.add_argument("--stale-days", type=int, default=90, help="staleness threshold (default: 90)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    mode.add_argument(
        "--verify-classify",
        metavar="FILE",
        help="require FILE to classify every unpromoted heading (JSONL); print the verdict"
             " summary on success, or errors and exit 1 on mismatch",
    )
    mode.add_argument(
        "--qmd-entry",
        metavar="SLUG",
        help="print the qmd collections-file entries for a visible-layout project named SLUG",
    )
    args = parser.parse_args()
    if args.stale_days < 0:
        parser.error("--stale-days must be non-negative")
    vault = Path(args.vault_root).expanduser().resolve()
    if not vault.is_dir():
        parser.error(f"vault root is not a directory: {vault}")
    report = lint(vault, args.stale_days)
    promotion = report["unpromoted_log"]
    report["promotion_required"] = promotion is not None and (promotion["count"] is None or bool(promotion["count"]))
    if args.qmd_entry:
        table = layout_table(vault)
        if table is None:
            parser.error("--qmd-entry applies to a visible-layout project (a .bc-agent/ with a Where things go table)")
        print(qmd_entry(vault, table, args.qmd_entry), end="")
        return 0
    if args.verify_classify and promotion is None:
        print(f"bc-wiki-maintain: promotion is {PROMOTION_NOT_APPLICABLE}", file=sys.stderr)
        return 1
    if args.verify_classify:
        errors, rows = verify_classification(Path(args.verify_classify).expanduser(), report["unpromoted_log"])
        if errors:
            print("bc-wiki-maintain: classification does not cover every unpromoted heading", file=sys.stderr)
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print(classification_summary(rows))
        return 0
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_report(report)
    invalid_required_range = report["promotion_required"] and not promotion["range"]
    work_errors = any(entry["severity"] == "error" for entry in report["work_findings"])
    return 1 if report["broken_links"] or report["ambiguous_links"] or invalid_required_range or work_errors else 0

if __name__ == "__main__":
    sys.exit(main())
