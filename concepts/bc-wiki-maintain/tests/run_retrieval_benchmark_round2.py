#!/usr/bin/env python3
"""Round-two, read-only retrieval benchmark for the image-maze agent vault.

The vault is a positional argument so this harness is portable. It builds the proposed
catalog in /tmp, runs only read-only qmd searches, and writes a separate round-two report.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, field
import datetime as dt
import importlib.util
import io
import os
from pathlib import Path
import re
import statistics
import subprocess
import sys
import tempfile
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
QUESTIONS_PATH = Path(__file__).with_name("retrieval-questions.md")
CURRENT_QUERIES_PATH = Path(__file__).with_name("retrieval-queries.tsv")
ORIGINAL_QUERIES_PATH = Path(__file__).with_name("retrieval-queries-original.tsv")
AGENT_QUERIES_PATH = Path(__file__).with_name("retrieval-queries-round2.tsv")
DEFAULT_RESULTS_PATH = Path(__file__).with_name("retrieval-results-round2.md")
SKIP_DIR_NAMES = {".git", ".obsidian", "scratch", "temp", "node_modules", "vendor"}
FLOOD_LIMIT = 15
QMD_LIMIT = 20
LOG_OVERLAP_MIN_TOKENS = 6
PAGE_KIND_WEIGHTS = {
    "root": 0.50,
    "decisions": 1.20,
    "project": 1.20,
}


def display_path(path: Path) -> str:
    """Render a filesystem path for committed reports without a resolved home prefix."""
    text = str(path)
    home = str(Path.home())
    if text == home or text.startswith(home + os.sep):
        return "$HOME" + text[len(home):]
    return text

# This is the same explicit incumbent judgment table used in round one. It is exposed in
# the report rather than pretending that loading a curated index is a scriptable ranking task.
INDEX_READ_ASSESSMENTS: dict[int, tuple[bool, str]] = {
    1: (True, "Agent maintainer instructions is the only row naming the wiki maintenance protocol."),
    2: (True, "Image SEO agent is the only row naming the image-metadata prompt."),
    3: (True, "Border-radius token scale names the requested corner-size convention."),
    4: (True, "Provider-first subscription architecture names provider/event/entitlement design."),
    5: (True, "Architecture deepening — no rejected designs names the record of discarded approaches."),
    6: (True, "The row explicitly says a mouse click dismisses the fullscreen viewer."),
    7: (True, "The row explicitly says rate_limit_* denies when fraud-sensitive ports are missing."),
    8: (True, "Architecture Adapter Split — architecture review names the requested extraction decision."),
    9: (True, "Automatic Publish Queue PRD names the only page governing v1 publish delay scope."),
    10: (False, "The Round 3 PRD path does not occur in index.md; no row can identify it."),
    11: (True, "Mobile Gesture Suite v2 PRD names the gesture behavior family containing the vibration rule."),
    12: (True, "Pipeline Reliability and Privacy PRD names the page governing lost-response retries."),
    13: (True, "Frontend Modal Accessibility PRD names the page governing nested focus and Escape."),
    14: (True, "LQIP Metadata Hygiene PRD names the cache-refresh policy page."),
    15: (True, "Toolchain and Static Analysis Hardening PRD lists the requested pipeline/theme checks."),
    16: (True, "Pack Download Surface Consolidation PRD names the legacy download-route policy."),
    17: (True, "Launch plan is the indexed page that partitions deployment and content control."),
    18: (False, "The theme-build-flow path does not occur in index.md; no row can identify it."),
    19: (False, "The wordpress-local-env path does not occur in index.md; no row can identify it."),
    20: (True, "Adult-content mode compliance research names the page containing the outstanding compliance inventory."),
}

METADATA_LABEL_RE = re.compile(
    r"^\s*(?:\*\*)?(?:date|status|updated|parent\s+issue|issue|owner|priority|state|seam|created|last\s+updated)"
    r"(?:\*\*)?\s*:\s*",
    re.IGNORECASE,
)
METADATA_SECTION_RE = re.compile(
    r"^(?:date|status|metadata|frontmatter|parent\s+issue|issue|owner|priority|state|seam)$",
    re.IGNORECASE,
)
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^\s*(#{1,6})\s+(.+?)\s*#*\s*$")
BAD_STATUS_VALUES = {
    "accepted",
    "approved",
    "closed",
    "complete",
    "completed",
    "done",
    "draft",
    "in progress",
    "open",
    "pending",
    "rejected",
}


@dataclass(frozen=True)
class Question:
    number: int
    text: str
    gold: str
    directory: str
    date: str


@dataclass(frozen=True)
class Page:
    relative: str
    path: Path
    content: bytes
    text: str


@dataclass(frozen=True)
class Attempt:
    query: str
    output_bytes: int
    rows: int
    hit: bool
    usable: bool
    rank: int | None = None
    top_path: str | None = None
    note: str = ""

    @property
    def tokens(self) -> float:
        return self.output_bytes / 4


@dataclass(frozen=True)
class Outcome:
    cost_tokens: float
    hit: bool
    attempts: tuple[Attempt, ...] = ()
    note: str = ""

    @property
    def output_bytes(self) -> int:
        return int(round(self.cost_tokens * 4))


@dataclass(frozen=True)
class AgentQuery:
    primary: str
    reformulation: str
    log_overlap: bool = False


def command(args: list[str], *, cwd: Path | None = None, timeout: int = 180) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=cwd, capture_output=True, timeout=timeout, check=False)


def decode(value: bytes) -> str:
    return value.decode("utf-8", errors="replace")


def load_linter():
    path = ROOT / "concepts/bc-wiki-maintain/body/wiki_lint.py"
    spec = importlib.util.spec_from_file_location("bc_wiki_maintain_linter_round2", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load linter module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_search():
    path = ROOT / "concepts/bc-wiki-maintain/body/wiki_search.py"
    spec = importlib.util.spec_from_file_location("bc_wiki_maintain_search_round2", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load search module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


WIKI_LINT = load_linter()
WIKI_SEARCH = load_search()


def parse_questions(path: Path) -> list[Question]:
    questions: list[Question] = []
    pattern = re.compile(
        r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$"
    )
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if not match:
            continue
        number, text, gold, directory, date = match.groups()
        questions.append(Question(int(number), text, gold, directory, date))
    if len(questions) != 20 or [item.number for item in questions] != list(range(1, 21)):
        raise ValueError(f"expected question numbers 1..20 in {path}, found {[item.number for item in questions]}")
    return questions


def parse_two_column_queries(path: Path, *, require_width: tuple[int, int] | None = None) -> dict[int, str]:
    queries: dict[int, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 2:
            raise ValueError(f"query row is not two tab-separated fields in {path}: {line!r}")
        number = int(fields[0])
        query = fields[1].strip()
        if require_width is not None and not require_width[0] <= len(query.split()) <= require_width[1]:
            raise ValueError(f"question {number} query width is invalid: {query!r}")
        if number in queries:
            raise ValueError(f"duplicate query number in {path}: {number}")
        queries[number] = query
    if set(queries) != set(range(1, 21)):
        raise ValueError(f"expected query numbers 1..20 in {path}, found {sorted(queries)}")
    return queries


def parse_agent_queries(path: Path) -> dict[int, AgentQuery]:
    queries: dict[int, AgentQuery] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) not in (3, 4):
            raise ValueError(f"query row must have three fields plus an optional marker in {path}: {line!r}")
        number = int(fields[0])
        primary, reformulation = (field.strip() for field in fields[1:3])
        marker = fields[3].strip() if len(fields) == 4 else ""
        if marker not in {"", "log-overlap"}:
            raise ValueError(f"question {number} has an unknown marker in {path}: {marker!r}")
        if not 1 <= len(primary.split()) <= 2 or not 1 <= len(reformulation.split()) <= 2:
            raise ValueError(f"question {number} agent queries must each contain 1..2 words")
        if number in queries:
            raise ValueError(f"duplicate agent query number in {path}: {number}")
        queries[number] = AgentQuery(primary, reformulation, marker == "log-overlap")
    if set(queries) != set(range(1, 21)):
        raise ValueError(f"expected agent query numbers 1..20 in {path}, found {sorted(queries)}")
    return queries


def repo_root(vault: Path) -> Path:
    result = command(["git", "-C", str(vault), "rev-parse", "--show-toplevel"])
    if result.returncode != 0:
        raise RuntimeError(f"target is not inside a git repository: {vault}: {decode(result.stderr).strip()}")
    return Path(decode(result.stdout).strip()).resolve()


def eligible_pages(vault: Path, repo: Path) -> list[Page]:
    result = command(["git", "-C", str(repo), "ls-files", "-z"])
    if result.returncode != 0:
        raise RuntimeError(f"git ls-files failed: {decode(result.stderr).strip()}")
    vault = vault.resolve()
    pages: list[Page] = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        repo_relative = Path(os.fsdecode(raw))
        path = (repo / repo_relative).resolve()
        if path.suffix.lower() != ".md" or not path.is_file():
            continue
        try:
            relative_path = path.relative_to(vault)
        except ValueError:
            continue
        if any(part in SKIP_DIR_NAMES for part in relative_path.parts):
            continue
        content = path.read_bytes()
        pages.append(Page(relative_path.as_posix(), path, content, decode(content)))
    return sorted(pages, key=lambda item: item.relative)


def search_documents(pages: list[Page]):
    return [
        WIKI_SEARCH.Document(
            page.relative,
            WIKI_SEARCH.Counter(WIKI_SEARCH.tokenize(page.text)),
            len(WIKI_SEARCH.tokenize(page.text)),
        )
        for page in pages
    ]


def page_kind(relative: str) -> str:
    path = Path(relative)
    return "root" if path.parent == Path(".") else path.parts[0]


def page_kind_weighted_rank(documents, query: str, limit: int = FLOOD_LIMIT):
    """Apply the one benchmark-only page-kind adjustment to the incumbent BM25 scores."""
    if not documents:
        return []
    baseline = WIKI_SEARCH.rank_documents(documents, query, limit=len(documents))
    weighted = [
        WIKI_SEARCH.RankedDocument(
            item.relative,
            item.score * PAGE_KIND_WEIGHTS.get(page_kind(item.relative), 1.0),
        )
        for item in baseline
    ]
    weighted.sort(key=lambda item: (-item.score, item.relative))
    return weighted[:limit]


def page_key(relative: str) -> str:
    path = Path(relative)
    return path.with_suffix("").as_posix() if path.suffix.lower() == ".md" else path.as_posix()


def graph(vault: Path, pages: list[Page]):
    by_key = {page_key(item.relative): item.path for item in pages}
    stems: dict[str, list[Path]] = {}
    for item in pages:
        stems.setdefault(Path(item.relative).stem, []).append(item.path)
    incoming = {item.path: 0 for item in pages}
    outgoing: dict[Path, set[Path]] = {item.path: set() for item in pages}
    for item in pages:
        relative = Path(item.relative)
        if relative.name == "log.md" or "templates" in relative.parts:
            continue
        for target, _display in WIKI_LINT.links(item.text):
            resolution = WIKI_LINT.resolve_link(item.path, target, vault, by_key, stems)
            if resolution is None:
                continue
            candidates, _local = resolution
            if len(candidates) != 1:
                continue
            candidate = candidates[0]
            incoming[candidate] += 1
            outgoing[item.path].add(candidate)
    return incoming, outgoing


def index_reachability(vault: Path, outgoing: dict[Path, set[Path]]) -> dict[Path, int]:
    index = (vault / "index.md").resolve()
    depths: dict[Path, int] = {index: 0}
    frontier = [index]
    while frontier:
        source = frontier.pop(0)
        for target in sorted(outgoing.get(source, set()), key=str):
            if target in depths:
                continue
            depths[target] = depths[source] + 1
            frontier.append(target)
    return depths


def yaml_body(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() in {"---", "..."}:
                return "\n".join(lines[index + 1 :])
    return text


def title_for(text: str, fallback: str) -> str:
    for line in yaml_body(text).splitlines():
        match = re.match(r"^\s*#\s+(.+?)\s*#*\s*$", line)
        if match:
            return match.group(1).strip()
    return Path(fallback).stem


def metadata_line(line: str) -> bool:
    return bool(METADATA_LABEL_RE.match(line))


def metadata_section(title: str) -> bool:
    return bool(METADATA_SECTION_RE.match(title.strip().strip("#*` ")))


def bad_candidate(value: str) -> bool:
    compact = re.sub(r"\s+", " ", value).strip().strip("*_` ").rstrip(".!?")
    lowered = compact.lower()
    if not compact or lowered in BAD_STATUS_VALUES:
        return True
    if re.match(r"^(?:parent\s+issue|issue|status|date|updated|seam)\b", lowered):
        return True
    if re.match(r"^\(?\s*(?:#\d+|seam\b)", lowered):
        return True
    if "TODO" in compact.upper() or re.search(r"\bfill(?:\s+in)?\b", compact, re.IGNORECASE):
        return True
    if lowered.startswith("use this page to choose the smallest context set"):
        return True
    return False


def first_sentence(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"^(?:[-*+]\s+|\d+[.)]\s+)", "", value).strip()
    match = re.search(r".+?[.!?](?=\s|$)", value)
    return (match.group(0) if match else value).strip()


def summary_for(text: str, fallback: str) -> str:
    """Return the first deterministic prose sentence after metadata/navigation noise.

    Sections are scanned in document order. A heading starts a candidate section; H1 is
    skipped, metadata-only sections are skipped, and a metadata line suppresses its wrapped
    continuation until the next blank line. Fences, badges, navigation-only links, TODO
    placeholders, and status/issue fragments are never candidates. If no candidate survives,
    the H1/path title is returned.
    """
    body = yaml_body(text)
    lines = body.splitlines()
    saw_heading = False
    substantive_section = True
    metadata_continuation = False
    in_fence = False
    fence_char = ""
    fence_len = 0
    paragraph: list[str] = []

    def consider(block: list[str]) -> str | None:
        if not block:
            return None
        candidate_lines: list[str] = []
        for raw in block:
            line = raw.strip()
            if not line or line.startswith("<!--") or line.endswith("-->"):
                continue
            if line.startswith("![") or line.startswith("[!["):
                continue
            if re.match(r"^\s*[-*+]\s*\[[^\]]+\]\([^)]*\)", line):
                continue
            if metadata_line(line):
                continue
            candidate_lines.append(line)
        if not candidate_lines:
            return None
        candidate = first_sentence(" ".join(candidate_lines))
        if bad_candidate(candidate):
            return None
        return candidate

    def flush() -> str | None:
        nonlocal paragraph
        result = consider(paragraph)
        paragraph = []
        return result

    for raw in lines:
        fence = FENCE_RE.match(raw)
        if in_fence:
            if fence and fence.group(1)[0] == fence_char and len(fence.group(1)) >= fence_len:
                in_fence = False
            continue
        if fence:
            in_fence = True
            fence_char = fence.group(1)[0]
            fence_len = len(fence.group(1))
            flush()
            continue
        heading = HEADING_RE.match(raw)
        if heading:
            found = flush()
            if found is not None and substantive_section:
                return found
            level, heading_title = len(heading.group(1)), heading.group(2).strip()
            if level == 1:
                continue
            saw_heading = True
            substantive_section = not metadata_section(heading_title)
            metadata_continuation = False
            continue
        line = raw.strip()
        if not line:
            found = flush()
            if found is not None and substantive_section:
                return found
            metadata_continuation = False
            continue
        if saw_heading and not substantive_section:
            continue
        if metadata_continuation:
            continue
        if metadata_line(line):
            flush()
            metadata_continuation = True
            continue
        if line.startswith("![") or line.startswith("[!["):
            continue
        paragraph.append(raw)

    found = flush()
    if found is not None and substantive_section:
        return found
    return title_for(text, fallback)


def headings_for(text: str, fallback: str) -> str:
    headings: list[str] = []
    for line in yaml_body(text).splitlines():
        match = re.match(r"^\s*##\s+(.+?)\s*$", line)
        if match:
            headings.append(match.group(1).strip())
    return "; ".join(headings) or title_for(text, fallback)


def git_date(repo: Path, page: Page) -> str:
    relative = page.path.relative_to(repo).as_posix()
    result = command(["git", "-C", str(repo), "log", "-1", "--format=%cs", "--", relative])
    value = decode(result.stdout).strip()
    if result.returncode != 0 or not value:
        raise RuntimeError(f"no Git date for tracked page {page.relative}: {decode(result.stderr).strip()}")
    return value


def sanitize_field(value: str) -> str:
    return re.sub(r"[\t\r\n]+", " ", value).strip()


def build_catalog(repo: Path, pages: list[Page], incoming: dict[Path, int]) -> Path:
    fd, filename = tempfile.mkstemp(prefix="bc-retrieval-round2-catalog-", suffix=".tsv", dir="/tmp")
    os.close(fd)
    catalog_path = Path(filename)
    with catalog_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(
            [
                "path",
                "kind",
                "git-date",
                "inbound-link-count",
                "byte-size",
                "one-sentence-summary",
                "keywords-from-##-headings",
            ]
        )
        for page in pages:
            parent = Path(page.relative).parent.as_posix()
            writer.writerow(
                [
                    page.relative,
                    "root" if parent == "." else parent,
                    git_date(repo, page),
                    incoming[page.path],
                    len(page.content),
                    sanitize_field(summary_for(page.text, page.relative)),
                    sanitize_field(headings_for(page.text, page.relative)),
                ]
            )
    return catalog_path


def word_patterns(query: str) -> list[re.Pattern[str]]:
    return [re.compile(r"(?<!\w)" + re.escape(word) + r"(?!\w)", re.IGNORECASE) for word in query.split()]


def filter_lines(raw: bytes, query: str) -> bytes:
    patterns = word_patterns(query)
    matches: list[bytes] = []
    for line in raw.splitlines(keepends=True):
        text = decode(line)
        if any(pattern.search(text) for pattern in patterns):
            matches.append(line)
    return b"".join(matches)


def fixed_filter(raw: bytes, query: str, gold: str) -> Attempt:
    output = filter_lines(raw, query)
    lines = output.splitlines()
    rank = next((index for index, line in enumerate(lines, 1) if gold.encode() in line), None)
    return Attempt(query, len(output), len(lines), rank is not None, bool(lines), rank=rank)


def ranked_filter(ranked, query: str, gold: str) -> Attempt:
    paths = [item.relative for item in ranked]
    output = "".join(f"{path}\\n" for path in paths).encode("utf-8")
    rank = next((index for index, path in enumerate(paths, 1) if path == gold), None)
    return Attempt(query, len(output), len(paths), rank is not None, bool(paths), rank=rank, top_path=paths[0] if paths else None)


def shared_log_excerpt(page_text: str, log_text: str, minimum: int = LOG_OVERLAP_MIN_TOKENS) -> str:
    """Return the longest exact token run shared by a gold page and the append-only log."""
    page_tokens = WIKI_SEARCH.tokenize(page_text)
    log_tokens = WIKI_SEARCH.tokenize(log_text)
    positions: dict[tuple[str, ...], int] = {}
    for index in range(len(log_tokens) - minimum + 1):
        positions.setdefault(tuple(log_tokens[index : index + minimum]), index)
    best: list[str] = []
    for index in range(len(page_tokens) - minimum + 1):
        log_index = positions.get(tuple(page_tokens[index : index + minimum]))
        if log_index is None:
            continue
        length = minimum
        while (
            index + length < len(page_tokens)
            and log_index + length < len(log_tokens)
            and page_tokens[index + length] == log_tokens[log_index + length]
        ):
            length += 1
        if length > len(best):
            best = page_tokens[index : index + length]
    return " ".join(best)


def log_overlap_excerpts(
    questions: list[Question], agent_queries: dict[int, AgentQuery], pages: list[Page], vault: Path
) -> dict[int, str]:
    marked = [question for question in questions if agent_queries[question.number].log_overlap]
    if len(marked) != 8:
        raise ValueError(f"expected exactly eight log-overlap questions, found {len(marked)}")
    by_relative = {page.relative: page for page in pages}
    log_path = vault / "log.md"
    if not log_path.is_file():
        raise ValueError(f"missing log for overlap experiment: {log_path}")
    log_text = log_path.read_text(encoding="utf-8", errors="replace")
    excerpts: dict[int, str] = {}
    for question in marked:
        if page_kind(question.gold) == "root":
            raise ValueError(f"log-overlap question {question.number} must target a compiled page: {question.gold}")
        page = by_relative.get(question.gold)
        if page is None:
            raise ValueError(f"log-overlap gold page is not eligible: {question.gold}")
        excerpt = shared_log_excerpt(page.text, log_text)
        if not excerpt:
            raise ValueError(f"log-overlap question {question.number} has no shared text: {question.gold}")
        excerpts[question.number] = excerpt
    return excerpts


def qmd_paths(stdout: bytes, collection: str) -> list[str]:
    paths: list[str] = []
    prefix = f"qmd://{collection}/"
    for row in csv.reader(io.StringIO(decode(stdout))):
        for field in row:
            if field.startswith(prefix):
                paths.append(unquote(field[len(prefix) :]))
                break
    return paths


def qmd_attempt(qmd_bin: str, collection: str, query: str, gold: str, limit: int = QMD_LIMIT) -> Attempt:
    result = command(
        [qmd_bin, "search", query, "-c", collection, "--format", "files", "-n", str(limit)],
        timeout=180,
    )
    paths = qmd_paths(result.stdout, collection)
    aliases = {gold, gold.replace(" ", "-")}
    rank = next((index for index, path in enumerate(paths, 1) if path in aliases), None)
    note = ""
    if result.returncode != 0:
        note = f"qmd exit {result.returncode}: {decode(result.stderr).strip()}"
    usable = 1 <= len(paths) <= FLOOD_LIMIT
    return Attempt(query, len(result.stdout), len(paths), rank is not None, usable, rank=rank, top_path=paths[0] if paths else None, note=note)


def run_direct_filter(documents, query: AgentQuery, gold: str, *, weighted: bool = False) -> Outcome:
    def attempt(query_text: str) -> Attempt:
        ranked = (
            page_kind_weighted_rank(documents, query_text, limit=FLOOD_LIMIT)
            if weighted
            else WIKI_SEARCH.rank_documents(documents, query_text, limit=FLOOD_LIMIT)
        )
        return ranked_filter(ranked, query_text, gold)

    first = attempt(query.primary)
    attempts = [first]
    if first.rows == 0 or first.rows > FLOOD_LIMIT:
        attempts.append(attempt(query.reformulation))
    final = attempts[-1]
    return Outcome(
        sum(item.output_bytes for item in attempts) / 4,
        final.usable and final.hit,
        tuple(attempts),
        "reformulated after zero/flood" if len(attempts) == 2 else "single usable attempt",
    )


def run_agent_filter(raw: bytes, query: AgentQuery, gold: str) -> Outcome:
    first = fixed_filter(raw, query.primary, gold)
    if first.rows == 0 or first.rows > FLOOD_LIMIT:
        second = fixed_filter(raw, query.reformulation, gold)
        hit = second.usable and second.hit
        return Outcome((first.output_bytes + second.output_bytes) / 4, hit, (first, second), "reformulated after zero/flood")
    return Outcome(first.tokens, first.usable and first.hit, (first,), "single usable attempt")


def run_agent_qmd(qmd_bin: str, collection: str, query: AgentQuery, gold: str) -> Outcome:
    first = qmd_attempt(qmd_bin, collection, query.primary, gold)
    if first.rows == 0 or first.rows > FLOOD_LIMIT:
        second = qmd_attempt(qmd_bin, collection, query.reformulation, gold)
        hit = second.usable and second.hit
        return Outcome(first.tokens + second.tokens, hit, (first, second), "reformulated after zero/flood")
    return Outcome(first.tokens, first.usable and first.hit, (first,), "single usable attempt")


def index_outcome(question: Question, index_bytes: bytes, depths: dict[Path, int], vault: Path) -> Outcome:
    hit, reason = INDEX_READ_ASSESSMENTS[question.number]
    depth = depths.get((vault / question.gold).resolve())
    structural = "unreachable" if depth is None else f"depth {depth}"
    return Outcome(len(index_bytes) / 4, hit, note=f"{reason} Structural reachability: {structural}.")


def fixed_qmd(qmd_bin: str, collection: str, query: str, gold: str) -> Attempt:
    return qmd_attempt(qmd_bin, collection, query, gold, limit=5)


def wilson(misses: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total == 0:
        return 0.0, 1.0
    p = misses / total
    denominator = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denominator
    spread = z * ((p * (1 - p) / total) + (z * z / (4 * total * total))) ** 0.5 / denominator
    return max(0.0, centre - spread), min(1.0, centre + spread)


def fmt(value: float) -> str:
    return f"{value:.2f}"


def uncertainty(ci: tuple[float, float]) -> str:
    low, high = ci
    if high <= 0.30:
        return "safe against the 0.30 bar (CI upper bound <= 0.30)"
    if low > 0.30:
        return "safe failure (CI lower bound > 0.30)"
    return "inside noise (CI crosses 0.30)"


def summary_table(results: dict[str, list[Outcome]]) -> list[str]:
    lines = [
        "| Method | Median tokens | Misses | Miss rate | Wilson 95% CI | Cost bar | Miss bar | Overall observed | Uncertainty |",
        "|---|---:|---:|---:|---|:---:|:---:|:---:|---|",
    ]
    for name, values in results.items():
        misses = sum(not value.hit for value in values)
        median = statistics.median(value.cost_tokens for value in values)
        rate = misses / len(values)
        ci = wilson(misses, len(values))
        cost_pass = median <= 800
        miss_pass = rate <= 0.30
        lines.append(
            f"| `{name}` | {fmt(median)} | {misses}/{len(values)} | {rate:.2f} | [{ci[0]:.2f}, {ci[1]:.2f}] "
            f"| {'pass' if cost_pass else 'fail'} | {'pass' if miss_pass else 'fail'} "
            f"| {'PASS' if cost_pass and miss_pass else 'FAIL'} | {uncertainty(ci)} |"
        )
    return lines


def attempt_cell(outcome: Outcome) -> str:
    statuses: list[str] = []
    for index, attempt in enumerate(outcome.attempts, 1):
        status = "hit" if attempt.hit else "MISS"
        trigger = "flood/zero" if attempt.rows == 0 or attempt.rows > FLOOD_LIMIT else "usable-width"
        rank = f", r{attempt.rank}" if attempt.rank is not None else ""
        statuses.append(f"a{index} {attempt.tokens:.2f}t/{attempt.rows} rows/{status}{rank}/{trigger}")
    final = "hit" if outcome.hit else "MISS"
    return f"{'; '.join(statuses)} => {outcome.cost_tokens:.2f}t/{final}"


def fixed_cell(attempt: Attempt) -> str:
    status = "hit" if attempt.hit else "MISS"
    rank = f", r{attempt.rank}" if attempt.rank is not None else ""
    return f"{attempt.tokens:.2f}t/{status}/{attempt.rows} rows{rank}"


def git_file_commit(path: Path) -> str:
    relative = path.resolve().relative_to(ROOT).as_posix()
    result = command(["git", "-C", str(ROOT), "log", "-1", "--format=%H", "--", relative])
    value = decode(result.stdout).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise RuntimeError(f"could not identify commit for {path}")
    return value


def chain(primary: list[Outcome], fallback: list[Outcome]) -> list[Outcome]:
    values: list[Outcome] = []
    for first, second in zip(primary, fallback):
        if first.hit:
            values.append(first)
        else:
            values.append(Outcome(first.cost_tokens + second.cost_tokens, second.hit, first.attempts + second.attempts, "fallback to index"))
    return values


def chain_stats(values: list[Outcome], primary: list[Outcome]) -> tuple[float, float, int, int]:
    return (
        statistics.median(value.cost_tokens for value in values),
        statistics.mean(value.cost_tokens for value in values),
        sum(not value.hit for value in values),
        sum(not value.hit for value in primary),
    )


def render_report(
    vault: Path,
    collection: str,
    questions: list[Question],
    agent_queries: dict[int, AgentQuery],
    current_queries: dict[int, str],
    original_queries: dict[int, str],
    pages: list[Page],
    catalog: Path,
    index_bytes: bytes,
    depths: dict[Path, int],
    agent_results: dict[str, list[Outcome]],
    fixed_current: dict[str, list[Attempt]],
    fixed_original: dict[str, list[Attempt]],
    affected: list[int],
    query_commit: str,
    original_commit: str,
    log_excerpts: dict[int, str],
) -> str:
    eligible = len(pages)
    direct = sum(depth == 1 for depth in depths.values())
    within_two = sum(depth <= 2 for depth in depths.values())
    a_results = agent_results["A_index_read"]
    c_chain = chain(agent_results["C_qmd_agent_filter"], a_results)
    d_chain = chain(agent_results["D_catalog_agent_filter"], a_results)
    c_median, c_mean, c_chain_misses, c_tail = chain_stats(c_chain, agent_results["C_qmd_agent_filter"])
    d_median, d_mean, d_chain_misses, d_tail = chain_stats(d_chain, agent_results["D_catalog_agent_filter"])
    catalog_rows = list(csv.reader(catalog.read_text(encoding="utf-8", newline="").splitlines(), delimiter="\t"))
    qlabel = QUESTIONS_PATH.relative_to(ROOT).as_posix()
    agent_label = AGENT_QUERIES_PATH.relative_to(ROOT).as_posix()
    original_label = ORIGINAL_QUERIES_PATH.relative_to(ROOT).as_posix()
    vault_display = display_path(vault)
    lines = [
        "# Image-maze retrieval benchmark — round two",
        "",
        f"Run date: {dt.date.today().isoformat()}. The target vault was read-only; no qmd index or vault file was mutated.",
        "",
        "## Answer to the review question",
        "",
        f"The benchmark uses **{eligible} eligible tracked Markdown pages** from `{vault_display}`. The proposed catalog has "
        f"**{catalog.stat().st_size:,} bytes / {catalog.stat().st_size / 4:.2f} tokens** before any filter output. "
        f"The index has {len(index_bytes):,} bytes / {len(index_bytes) / 4:.2f} tokens.",
        "",
        "The answer is based on the agent-style protocol below, not the round-one 3–4-word AND test.",
        "",
    ]
    lines.extend(summary_table(agent_results))
    incumbent = agent_results["E_bm25_direct"]
    candidate = agent_results["F_page_kind_weighted"]
    incumbent_misses = sum(not value.hit for value in incumbent)
    candidate_misses = sum(not value.hit for value in candidate)
    incumbent_rate = incumbent_misses / len(incumbent)
    candidate_rate = candidate_misses / len(candidate)
    incumbent_median = statistics.median(value.cost_tokens for value in incumbent)
    candidate_median = statistics.median(value.cost_tokens for value in candidate)
    incumbent_ci = wilson(incumbent_misses, len(incumbent))
    candidate_ci = wilson(candidate_misses, len(candidate))
    material_improvement = candidate_rate < incumbent_rate and candidate_ci[1] < incumbent_ci[0]
    if candidate_median <= 800 and candidate_rate <= 0.30 and material_improvement:
        experiment_decision = "retain the page-kind weighting in production"
    else:
        experiment_decision = "record a null result and leave production scoring lexical"
    lines.extend(
        [
            "",
            "## W4 page-kind experiment",
            "",
            f"The extended query corpus keeps **20 questions** and marks **{len(log_excerpts)}** compiled-page cases whose gold-page text shares an exact contiguous run of at least {LOG_OVERLAP_MIN_TOKENS} normalized tokens with `log.md`. The harness verifies those overlaps against the live tracked pages before measuring either reader.",
            "",
            "The incumbent `E_bm25_direct` calls the production `wiki_search.py` BM25 scorer. The only experimental candidate, `F_page_kind_weighted`, multiplies those same scores by page kind: `root` = 0.50, `decisions` = 1.20, `project` = 1.20, and every other top-level directory = 1.00. This tests whether compiled pages should outrank root hubs and logs without changing query terms or corpus eligibility.",
            "",
            f"Observed incumbent: **{incumbent_misses}/20 misses ({incumbent_rate:.2f}), median {incumbent_median:.2f} tokens**, Wilson 95% CI [{incumbent_ci[0]:.2f}, {incumbent_ci[1]:.2f}]. Candidate: **{candidate_misses}/20 misses ({candidate_rate:.2f}), median {candidate_median:.2f} tokens**, Wilson 95% CI [{candidate_ci[0]:.2f}, {candidate_ci[1]:.2f}]. The candidate must improve on the 0.15 incumbent miss rate, stay at or below 800 median tokens and 0.30 miss rate, and show a non-overlapping interval before production adoption; n=20 makes a small delta/noisy overlap insufficient.",
            "",
            f"**Decision: {experiment_decision}.** No production weighting is retained unless all three bars and the non-noisy improvement test hold.",
            "",
            "| Q | Gold compiled page | Exact page/log overlap excerpt | Primary → reformulation |",
            "|---:|---|---|---|",
        ]
    )
    for question in questions:
        if question.number not in log_excerpts:
            continue
        query = agent_queries[question.number]
        lines.append(
            f"| {question.number} | `{question.gold}` | `{log_excerpts[question.number]}` | `{query.primary}` → `{query.reformulation}` |"
        )
    lines.extend(
        [
            "",
            "Observed PASS means both observed metrics clear the bars; it is not a claim that a 20-question estimate is certain. "
            "The Wilson column is the required uncertainty statement for each miss rate. A CI crossing 0.30 is explicitly "
            "inside noise, even when the observed row says PASS or FAIL.",
            "",
            "## Protocol",
            "",
            f"The extended agent query file is `{agent_label}` (commit `{query_commit}`). Each primary and reformulation has "
            "one or two concrete terms selected from the question wording before retrieval was run; rows marked `log-overlap` "
            "identify the compiled-page/log cases above. The two attempts are "
            "fixed for all methods. A first result with **zero rows or more than 15 rows is flooded** and triggers exactly "
            "one reformulation. A nonzero result of 1–15 rows is usable; a nonzero miss in that width does not get a third "
            "attempt. Both attempts' UTF-8 output bytes are charged when the second runs.",
            "",
            "`B_index_agent_filter` applies case-insensitive whole-word OR to each line of `index.md`. "
            "`D_catalog_agent_filter` applies the identical OR matcher to each seven-column catalog row. "
            "`C_qmd_agent_filter` runs `qmd search <terms> -c <collection> --format files -n 20`; qmd paths are the rows. "
            "`E_bm25_direct` runs the production stdlib BM25 reader over tracked Markdown; `F_page_kind_weighted` applies "
            "the single page-kind adjustment to those same scores. "
            "A usable hit requires the exact gold relative path in the usable output. The filter output itself, not process "
            "startup or the catalog build, is context and costs bytes/4.",
            "",
            "The incumbent `A_index_read` loads all of `index.md` and uses the explicit row judgment record retained from round "
            "one. It is included as a cost/accuracy comparator, not silently treated as a scriptable filter.",
            "",
            "## Per-question agent-style measurements",
            "",
            "Cells show each attempt as `tokens / rows / initial-hit / trigger`, followed by total charged tokens and final hit. "
            "For a single usable attempt, no reformulation was permitted. `initial-hit` means the gold path was present even "
            "if the result was flooded; the final status requires a usable 1–15-row result after any required reformulation.",
            "",
            "| # | Gold | Primary → reformulation | A index | B index filter | C qmd filter | D catalog filter | E direct BM25 | F page-kind weighted |",
            "|---:|---|---|---:|---|---|---|---|---|",
        ]
    )
    for index, question in enumerate(questions):
        query = agent_queries[question.number]
        lines.append(
            f"| {question.number} | `{question.gold}` | `{query.primary}` → `{query.reformulation}` | "
            f"{a_results[index].cost_tokens:.2f}t/{'hit' if a_results[index].hit else 'MISS'} | "
            f"{attempt_cell(agent_results['B_index_agent_filter'][index])} | "
            f"{attempt_cell(agent_results['C_qmd_agent_filter'][index])} | "
            f"{attempt_cell(agent_results['D_catalog_agent_filter'][index])} | "
            f"{attempt_cell(agent_results['E_bm25_direct'][index])} | "
            f"{attempt_cell(agent_results['F_page_kind_weighted'][index])} |"
        )
    lines.extend(
        [
            "",
            "## Chains",
            "",
            "A chain pays the primary method's total output and reads the full index only when the primary final result misses. "
            "The fallback's hit is then the chain hit. This is separate from the primary method's own median.",
            "",
            f"- **C first, index fallback:** median **{c_median:.2f} tokens**, mean **{c_mean:.2f} tokens**, "
            f"final misses **{c_chain_misses}/{eligible if eligible == 20 else len(c_chain)}**, and **{c_tail}/20** questions pay the ~{len(index_bytes) / 4:.0f}-token index fallback.",
            f"- **D first, index fallback:** median **{d_median:.2f} tokens**, mean **{d_mean:.2f} tokens**, "
            f"final misses **{d_chain_misses}/{len(d_chain)}**, and **{d_tail}/20** questions pay the ~{len(index_bytes) / 4:.0f}-token index fallback.",
            "",
            "The chain medians include fallback cost; they must not be reported as the primary method's median. The means expose "
            "the expensive tail that a median can hide.",
            "",
            "## Content-first catalog extraction",
            "",
            "The catalog is generated at `/tmp` only; its seven columns are `path`, vault-relative `kind`, Git date, inbound-link "
            "count, byte size, deterministic summary, and `##` heading keywords. The summary algorithm is:",
            "",
            "1. Strip a leading YAML frontmatter block.",
            "2. Scan sections in order, skipping H1. Treat metadata-only headings (`Date`, `Status`, `Metadata`, `Parent issue`, "
            "`Issue`, `Owner`, `Priority`, `State`, and `Seam`) as non-substantive.",
            "3. In a substantive section, skip fenced code, badges, blank lines, navigation-only Markdown-link bullets, HTML comments, "
            "and metadata labels (`Date:`, `Status:`, `Updated:`, `Parent issue:`, issue/owner/priority/state/seam labels). A "
            "metadata label suppresses its wrapped continuation until the next blank line.",
            "4. Take the first sentence of the first surviving prose paragraph. Reject bare status values, issue/seam fragments, TODO/fill "
            "placeholders, and the known context-map boilerplate. If no real prose survives, use the H1 title, or the path stem.",
            "",
            "This is deterministic and model-free. It does not use an LLM to manufacture summaries. In this run the catalog has "
            f"{len(catalog_rows) - 1} data rows and every row has seven nonempty fields; its exact byte size is reported above.",
            "",
            "## Original post-freeze query re-score",
            "",
            f"The exact original file is `{original_label}` (commit `{original_commit}`). It preserves the strings from `git show "
            "ea0e1f9:concepts/bc-wiki-maintain/tests/retrieval-queries.tsv`; the current file is not rewritten. The affected "
            f"questions are **{', '.join(map(str, affected))}**. The fixed-method re-score uses the round-one whole-word OR/AND "
            "matchers and qmd `--format files -n 5`, with output bytes/4. A hit means the gold path appears in the method output; "
            "no flood reformulation is applied in this historical comparison.",
            "",
            "| Q | Original query | Current query | Method | Current miss? | Original miss? | Change |",
            "|---:|---|---|---|:---:|:---:|---:|",
        ]
    )
    fixed_names = ["B_index_OR", "B_index_AND", "C_qmd", "D_catalog_OR", "D_catalog_AND"]
    for qnum in affected:
        question = questions[qnum - 1]
        for name in fixed_names:
            current = fixed_current[name][affected.index(qnum)]
            original = fixed_original[name][affected.index(qnum)]
            current_miss = not current.hit
            original_miss = not original.hit
            change = "miss→hit" if current_miss and not original_miss else "hit→miss" if not current_miss and original_miss else "unchanged"
            lines.append(
                f"| {qnum} | `{original_queries[qnum]}` | `{current_queries[qnum]}` | `{name}` | "
                f"{'yes' if current_miss else 'no'} | {'yes' if original_miss else 'no'} | {change} |"
            )
    lines.extend(
        [
            "",
            "### Original-query aggregate",
            "",
            "| Method | Current misses | Original misses | Delta | Wilson 95% CI, original | Interpretation |",
            "|---|---:|---:|---:|---|---|",
        ]
    )
    for name in fixed_names:
        current_values = fixed_current[name]
        original_values = fixed_original[name]
        current_misses = sum(not value.hit for value in current_values)
        original_misses = sum(not value.hit for value in original_values)
        ci = wilson(original_misses, len(original_values))
        lines.append(
            f"| `{name}` | {current_misses}/{len(current_values)} | {original_misses}/{len(original_values)} | "
            f"{original_misses - current_misses:+d} | [{ci[0]:.2f}, {ci[1]:.2f}] | {uncertainty(ci)} |"
        )
    lines.extend(
        [
            "",
            "The incumbent A result is query-independent and therefore unchanged; it is not duplicated in the row table. "
            "The aggregate makes any wording-induced movement visible rather than treating the edited current file as the only freeze.",
            "",
            "## Index structure and limitations",
            "",
            f"The index graph reaches {direct} pages at depth 1 and {within_two} at depth <=2. This benchmark still uses the explicit "
            "A row judgments, so reachability is a structural diagnostic rather than an automatic hit. The question set is n=20 "
            "and has the distribution/skew documented in the pre-registered question file; Wilson intervals are therefore essential.",
            "",
            "The catalog can be better than round one without being the right first move. If its agent-style row filter still misses "
            "the cost and miss bars, that is structural pressure: adding deterministic summary prose can recover terms absent from the "
            "row, but every added byte raises the cost of a whole-row flood. The result must distinguish that squeeze from the old "
            "status-fragment parser and four-word AND protocol.",
            "",
            "## Reproduction",
            "",
            "```sh",
            "python3 concepts/bc-wiki-maintain/tests/run_retrieval_benchmark_round2.py \\",
            '  "$HOME/Sync/Work/Development/wp-theme-builds/localhost/image-maze/.bc-agent" \\',
            "  --collection image-maze",
            "```",
            "",
            "The script takes the vault path as an argument, accepts `--collection` and `--qmd-bin`, writes the catalog under `/tmp`, "
            "and writes this report to `--results` (default `retrieval-results-round2.md`). It never invokes qmd update, embed, init, "
            "cleanup, collection, or context mutation commands.",
            "",
            "## Source citations",
            "",
            f"- `{qlabel}`: the 20 questions and gold paths used by this run.",
            f"- `{agent_label}`: pre-registered one/two-term primary and reformulation pairs, with eight `log-overlap` markers for W4.",
            "- `concepts/bc-wiki-maintain/body/wiki_search.py`: the incumbent tracked-only BM25 scorer used by E.",
            "- `page_kind_weighted_rank` in this benchmark: the one experimental page-kind adjustment used by F; no production scorer change was made.",
            f"- `{original_label}`: exact pre-width-fix query strings from the ea0e1f9 tree.",
            f"- `{catalog}`: this run's generated seven-column catalog; it is disposable and not an in-vault artifact.",
            f"- `{display_path(vault / 'index.md')}`: incumbent index bytes and graph source.",
            "",
        ]
    )
    return "\n".join(lines)


def run(args: argparse.Namespace) -> None:
    vault = Path(args.vault).expanduser().resolve()
    if not vault.is_dir():
        raise SystemExit(f"vault is not a directory: {vault}")
    questions = parse_questions(Path(args.questions).resolve())
    agent_queries = parse_agent_queries(Path(args.agent_queries).resolve())
    current_queries = parse_two_column_queries(Path(args.queries).resolve(), require_width=(2, 4))
    original_queries = parse_two_column_queries(Path(args.original_queries).resolve())
    if set(original_queries) != set(current_queries):
        raise RuntimeError("original and current query files do not cover the same question numbers")
    affected = [number for number in range(1, 21) if original_queries[number] != current_queries[number]]
    if affected != [12, 14, 15, 16, 17, 18, 19]:
        raise RuntimeError(f"expected the seven known post-freeze query changes, found {affected}")
    repo = repo_root(vault)
    pages = eligible_pages(vault, repo)
    if len(pages) != 155:
        raise RuntimeError(f"expected image-maze benchmark corpus to contain 155 eligible pages, found {len(pages)}")
    log_excerpts = log_overlap_excerpts(questions, agent_queries, pages, vault)
    search_docs = search_documents(pages)
    incoming, outgoing = graph(vault, pages)
    depths = index_reachability(vault, outgoing)
    index_path = (vault / "index.md").resolve()
    if not index_path.is_file():
        raise RuntimeError(f"missing incumbent index: {index_path}")
    index_bytes = index_path.read_bytes()
    catalog = build_catalog(repo, pages, incoming)
    catalog_rows = list(csv.reader(catalog.read_text(encoding="utf-8", newline="").splitlines(), delimiter="\t"))
    if len(catalog_rows) != 156 or any(len(row) != 7 for row in catalog_rows):
        raise RuntimeError(f"catalog does not have header + 155 seven-column rows: {catalog}")
    if any(not field for row in catalog_rows for field in row):
        raise RuntimeError(f"catalog contains an empty field: {catalog}")

    collection = args.collection or os.environ.get("QMD_COLLECTION") or vault.parent.name
    qmd_bin = args.qmd_bin or os.environ.get("QMD_BIN", "qmd")
    index_raw = index_bytes
    catalog_raw = catalog.read_bytes()
    agent_results: dict[str, list[Outcome]] = {name: [] for name in (
        "A_index_read", "B_index_agent_filter", "C_qmd_agent_filter", "D_catalog_agent_filter",
        "E_bm25_direct", "F_page_kind_weighted",
    )}
    for question in questions:
        query = agent_queries[question.number]
        agent_results["A_index_read"].append(index_outcome(question, index_bytes, depths, vault))
        agent_results["B_index_agent_filter"].append(run_agent_filter(index_raw, query, question.gold))
        agent_results["C_qmd_agent_filter"].append(run_agent_qmd(qmd_bin, collection, query, question.gold))
        agent_results["D_catalog_agent_filter"].append(run_agent_filter(catalog_raw, query, question.gold))
        agent_results["E_bm25_direct"].append(run_direct_filter(search_docs, query, question.gold))
        agent_results["F_page_kind_weighted"].append(run_direct_filter(search_docs, query, question.gold, weighted=True))

    fixed_names = ["B_index_OR", "B_index_AND", "C_qmd", "D_catalog_OR", "D_catalog_AND"]
    fixed_current: dict[str, list[Attempt]] = {name: [] for name in fixed_names}
    fixed_original: dict[str, list[Attempt]] = {name: [] for name in fixed_names}
    for qnum in affected:
        question = questions[qnum - 1]
        for target, query in ((fixed_current, current_queries[qnum]), (fixed_original, original_queries[qnum])):
            target["B_index_OR"].append(fixed_filter(index_raw, query, question.gold))
            and_output = index_raw
            and_patterns = word_patterns(query)
            and_matches = [line for line in and_output.splitlines(keepends=True) if all(pattern.search(decode(line)) for pattern in and_patterns)]
            and_bytes = b"".join(and_matches)
            and_lines = and_bytes.splitlines()
            and_rank = next((index for index, line in enumerate(and_lines, 1) if question.gold.encode() in line), None)
            target["B_index_AND"].append(Attempt(query, len(and_bytes), len(and_lines), and_rank is not None, bool(and_lines), rank=and_rank))
            target["C_qmd"].append(fixed_qmd(qmd_bin, collection, query, question.gold))
            target["D_catalog_OR"].append(fixed_filter(catalog_raw, query, question.gold))
            catalog_patterns = word_patterns(query)
            catalog_and_matches = [line for line in catalog_raw.splitlines(keepends=True) if all(pattern.search(decode(line)) for pattern in catalog_patterns)]
            catalog_and_bytes = b"".join(catalog_and_matches)
            catalog_and_lines = catalog_and_bytes.splitlines()
            catalog_and_rank = next((index for index, line in enumerate(catalog_and_lines, 1) if question.gold.encode() in line), None)
            target["D_catalog_AND"].append(Attempt(query, len(catalog_and_bytes), len(catalog_and_lines), catalog_and_rank is not None, bool(catalog_and_lines), rank=catalog_and_rank))

    query_commit = git_file_commit(Path(args.agent_queries).resolve())
    original_commit = git_file_commit(Path(args.original_queries).resolve())
    results_path = Path(args.results).expanduser().resolve()
    results_path.write_text(
        render_report(
            vault, collection, questions, agent_queries, current_queries, original_queries, pages, catalog, index_bytes,
            depths, agent_results, fixed_current, fixed_original, affected, query_commit, original_commit, log_excerpts,
        ),
        encoding="utf-8",
    )
    print(f"wrote {results_path}")
    print(f"catalog {catalog} ({catalog.stat().st_size} bytes, {len(pages)} rows)")
    print("\n".join(summary_table(agent_results)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault", help="path to the read-only .bc-agent vault")
    parser.add_argument("--collection", help="qmd collection name (default: QMD_COLLECTION or vault parent)")
    parser.add_argument("--qmd-bin", help="qmd executable (default: QMD_BIN or qmd)")
    parser.add_argument("--questions", default=str(QUESTIONS_PATH), help=argparse.SUPPRESS)
    parser.add_argument("--queries", default=str(CURRENT_QUERIES_PATH), help=argparse.SUPPRESS)
    parser.add_argument("--original-queries", default=str(ORIGINAL_QUERIES_PATH), help=argparse.SUPPRESS)
    parser.add_argument("--agent-queries", default=str(AGENT_QUERIES_PATH), help=argparse.SUPPRESS)
    parser.add_argument("--results", default=str(DEFAULT_RESULTS_PATH), help="round-two results Markdown output path")
    return parser.parse_args()


if __name__ == "__main__":
    try:
        run(parse_args())
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"round-two retrieval benchmark: ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
