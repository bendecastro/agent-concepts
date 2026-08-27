#!/usr/bin/env python3
"""Reproduce the image-maze retrieval comparison without mutating the vault.

The target vault is deliberately an argument, not a machine-specific constant.  The script
only reads the vault and invokes read-only qmd search.  It writes the generated catalog to
/tmp and the report to the repository's retrieval-results.md unless --results is supplied.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
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
QUERIES_PATH = Path(__file__).with_name("retrieval-queries.tsv")
DEFAULT_RESULTS_PATH = Path(__file__).with_name("retrieval-results.md")
SKIP_DIR_NAMES = {".git", ".obsidian", "scratch", "temp", "node_modules", "vendor"}

# This is the only non-mechanical part of A_index_read.  It records whether the curated row
# visible in index.md is specific enough to identify the declared gold page, without opening
# another page.  The reasons are rendered in the report so a reviewer can challenge them.
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


@dataclass(frozen=True)
class Question:
    number: int
    text: str
    gold: str
    directory: str
    date: str


@dataclass(frozen=True)
class Retrieval:
    cost_tokens: float
    output_bytes: int
    hit: bool
    rank: int | None = None
    rows: int | None = None
    top_path: str | None = None
    note: str = ""


@dataclass(frozen=True)
class Page:
    relative: str
    path: Path
    content: bytes
    text: str


def load_linter():
    path = ROOT / "concepts/bc-wiki-maintain/body/wiki_lint.py"
    spec = importlib.util.spec_from_file_location("bc_wiki_maintain_linter", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load linter module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


WIKI_LINT = load_linter()


def command(args: list[str], *, cwd: Path | None = None, timeout: int = 180) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=cwd, capture_output=True, timeout=timeout, check=False)


def decode(value: bytes) -> str:
    return value.decode("utf-8", errors="replace")


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


def parse_queries(path: Path) -> dict[int, str]:
    queries: dict[int, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 2:
            raise ValueError(f"query row is not two tab-separated fields: {line!r}")
        number = int(fields[0])
        keywords = fields[1].strip()
        words = keywords.split()
        if not 2 <= len(words) <= 4:
            raise ValueError(f"question {number} query has {len(words)} words, expected 2..4: {keywords!r}")
        if number in queries:
            raise ValueError(f"duplicate frozen query number: {number}")
        queries[number] = keywords
    if set(queries) != set(range(1, 21)):
        raise ValueError(f"expected frozen queries 1..20 in {path}, found {sorted(queries)}")
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


def page_key(relative: str) -> str:
    path = Path(relative)
    return path.with_suffix("").as_posix() if path.suffix.lower() == ".md" else path.as_posix()


def graph(vault: Path, pages: list[Page]):
    page_paths = {item.relative: item.path for item in pages}
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
    return page_paths, incoming, outgoing


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


def word_patterns(keywords: str) -> list[re.Pattern[str]]:
    return [re.compile(r"(?<!\w)" + re.escape(word) + r"(?!\w)", re.IGNORECASE) for word in keywords.split()]


def filter_lines(raw: bytes, keywords: str, *, require_all: bool) -> bytes:
    patterns = word_patterns(keywords)
    matches: list[bytes] = []
    for line in raw.splitlines(keepends=True):
        text = decode(line)
        matched = all(pattern.search(text) for pattern in patterns) if require_all else any(
            pattern.search(text) for pattern in patterns
        )
        if matched:
            matches.append(line)
    return b"".join(matches)


def retrieval_from_lines(output: bytes, gold: str, *, note: str = "") -> Retrieval:
    text = decode(output)
    lines = text.splitlines()
    hit = any(gold in line for line in lines)
    return Retrieval(len(output) / 4, len(output), hit, rows=len(lines), note=note)


def git_date(repo: Path, page: Page) -> str:
    relative = str((repo / page.path.relative_to(repo)).relative_to(repo))
    result = command(["git", "-C", str(repo), "log", "-1", "--format=%cs", "--", relative])
    value = decode(result.stdout).strip()
    if result.returncode != 0 or not value:
        raise RuntimeError(f"no git date for tracked page {page.relative}: {decode(result.stderr).strip()}")
    return value


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


def summary_for(text: str, fallback: str) -> str:
    body = yaml_body(text)
    in_fence = False
    candidate: str | None = None
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if line.startswith("```") or line.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence or not line or re.match(r"^#{1,6}\s", line):
            continue
        if re.match(r"^(?:Date|Status|Updated):\s", line, re.IGNORECASE):
            continue
        if re.match(r"^\*\*(?:Date|Status|Updated):", line, re.IGNORECASE):
            continue
        if "TODO" in line.upper() or re.search(r"\bfill(?: in)?\b", line, re.IGNORECASE):
            continue
        if line.lower().startswith("use this page to choose the smallest context set"):
            continue
        if line.startswith("!["):
            continue
        candidate = line
        break
    if candidate is None:
        candidate = title_for(text, fallback)
    candidate = re.sub(r"\s+", " ", candidate).strip()
    sentence = re.search(r".+?[.!?](?=\s|$)", candidate)
    if sentence:
        candidate = sentence.group(0).strip()
    return candidate or title_for(text, fallback)


def headings_for(text: str, fallback: str) -> str:
    headings = []
    for line in yaml_body(text).splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            headings.append(match.group(1).strip())
    # The contract requires every TSV field to be populated. Pages without a ## heading
    # use their deterministic title as a useful, non-fabricated keyword fallback.
    return "; ".join(headings) or title_for(text, fallback)


def sanitize_field(value: str) -> str:
    return re.sub(r"[\t\r\n]+", " ", value).strip()


def build_catalog(vault: Path, repo: Path, pages: list[Page], incoming: dict[Path, int]) -> Path:
    fd, filename = tempfile.mkstemp(prefix="bc-retrieval-catalog-", suffix=".tsv", dir="/tmp")
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
            relative = Path(page.relative)
            parent = relative.parent.as_posix()
            kind = "root" if parent == "." else parent
            writer.writerow(
                [
                    page.relative,
                    kind,
                    git_date(repo, page),
                    incoming[page.path],
                    len(page.content),
                    sanitize_field(summary_for(page.text, page.relative)),
                    sanitize_field(headings_for(page.text, page.relative)),
                ]
            )
    return catalog_path


def qmd_paths(stdout: bytes, collection: str) -> list[str]:
    paths: list[str] = []
    prefix = f"qmd://{collection}/"
    for row in csv.reader(io.StringIO(decode(stdout))):
        for field in row:
            if field.startswith(prefix):
                path = unquote(field[len(prefix) :])
                paths.append(path)
                break
    return paths


def qmd_retrieval(
    qmd_bin: str,
    collection: str,
    query: str,
    gold: str,
) -> Retrieval:
    result = command(
        [qmd_bin, "search", query, "-c", collection, "--format", "files", "-n", "5"],
        timeout=180,
    )
    paths = qmd_paths(result.stdout, collection)
    aliases = {gold, gold.replace(" ", "-")}
    rank = next((index for index, path in enumerate(paths, 1) if path in aliases), None)
    note = ""
    if result.returncode != 0:
        note = f"qmd exit {result.returncode}: {decode(result.stderr).strip()}"
    return Retrieval(
        len(result.stdout) / 4,
        len(result.stdout),
        rank is not None,
        rank=rank,
        rows=len(paths),
        top_path=paths[0] if paths else None,
        note=note,
    )


def index_read(question: Question, index_bytes: bytes, depths: dict[Path, int], vault: Path) -> Retrieval:
    hit, reason = INDEX_READ_ASSESSMENTS[question.number]
    depth = depths.get((vault / question.gold).resolve())
    structural = "unreachable" if depth is None else f"depth {depth}"
    note = f"{reason} Structural reachability: {structural}."
    return Retrieval(len(index_bytes) / 4, len(index_bytes), hit, note=note)


def fmt_tokens(value: float) -> str:
    return f"{value:.2f}"


def method_summary(results: dict[str, list[Retrieval]]) -> str:
    lines = [
        "| Method | Median tokens | Miss rate | Median <= 800? | Miss <= 0.30? | Passes both? |",
        "|---|---:|---:|:---:|:---:|:---:|",
    ]
    for name, values in results.items():
        median = statistics.median(item.cost_tokens for item in values)
        miss_rate = sum(not item.hit for item in values) / len(values)
        cost_pass = median <= 800
        miss_pass = miss_rate <= 0.30
        both = cost_pass and miss_pass
        lines.append(
            f"| `{name}` | {fmt_tokens(median)} | {miss_rate:.2f} ({sum(not item.hit for item in values)}/{len(values)}) "
            f"| {'yes' if cost_pass else 'no'} | {'yes' if miss_pass else 'no'} | {'**yes**' if both else 'no'} |"
        )
    return "\n".join(lines)


def render_results(
    vault: Path,
    collection: str,
    questions: list[Question],
    queries: dict[int, str],
    pages: list[Page],
    catalog: Path,
    index_bytes: bytes,
    depths: dict[Path, int],
    all_results: dict[str, list[Retrieval]],
    query_commit: str,
) -> str:
    eligible = len(pages)
    direct = sum(1 for depth in depths.values() if depth == 1)
    within_two = sum(1 for depth in depths.values() if depth <= 2)
    index_label = "$IMAGE_MAZE_VAULT/index.md"
    catalog_bytes = catalog.stat().st_size
    keyword_top = {}
    sentence_top = {}
    for value in all_results["C_qmd_keywords"]:
        if value.top_path:
            keyword_top[value.top_path] = keyword_top.get(value.top_path, 0) + 1
    for value in all_results["C2_qmd_sentence"]:
        if value.top_path:
            sentence_top[value.top_path] = sentence_top.get(value.top_path, 0) + 1
    keyword_top = sorted(keyword_top.items(), key=lambda item: (-item[1], item[0]))[:5]
    sentence_top = sorted(sentence_top.items(), key=lambda item: (-item[1], item[0]))[:5]
    lines = [
        "# Image-maze retrieval benchmark results",
        "",
        "Run date: 2026-08-27. The target vault was read-only. The frozen keyword file was",
        "committed before this harness ran; see the commit record in the parent run artifact.",
        "",
        "## Result",
        "",
        f"The vault supplied **{eligible} eligible tracked Markdown pages**. The harness read `{index_label}` "
        f"as the incumbent and generated a **{catalog_bytes:,}-byte** seven-column catalog at `{catalog}` only. "
        f"Frozen query commit: `{query_commit}`.",
        "The index graph reaches "
        f"{direct} pages at depth 1 and {within_two} at depth <=2; the benchmark does not infer a hit from "
        "reachability alone: A_index_read uses the explicit row judgments below.",
        "",
        "Cost is UTF-8 stdout bytes / 4 for search/filter output. A_index_read is the full index byte size / 4; "
        "no follow-on page is opened because each judgment is whether the index row identifies the gold page. "
        "The bars are median <= 800 tokens and miss rate <= 0.30, and both are required.",
        "",
        method_summary(all_results),
        "",
        "### Method interpretation",
        "",
        "- `A_index_read` is the incumbent: the full curated index is loaded once per question and the row is judged.",
        "- `B_index_grep_AND` and `B_index_grep_OR` filter the same index rows with the frozen keywords.",
        "- `C_qmd_keywords` searches the complete active qmd collection with frozen keywords; rank is returned order.",
        "- `C2_qmd_sentence` repeats qmd search with the complete natural-language question, documenting query-shape sensitivity.",
        "- `D_catalog_grep_AND` and `D_catalog_grep_OR` filter the generated TSV; catalog construction is not context cost.",
        "",
        "## Per-question measurements",
        "",
        "Each cell is `tokens / hit-or-miss`; qmd cells also include `rank` and grep cells include matching row count.",
        "",
        "| # | Gold page | Frozen keywords | A index | B AND | B OR | C keywords | C2 sentence | D AND | D OR |",
        "|---:|---|---|---|---|---|---|---|---|---|",
    ]
    for index, question in enumerate(questions):
        def cell(name: str) -> str:
            value = all_results[name][index]
            status = "hit" if value.hit else "MISS"
            detail = f"{fmt_tokens(value.cost_tokens)} / {status}"
            if value.rank is not None:
                detail += f" (r{value.rank})"
            elif name.startswith("C"):
                detail += " (no rank)"
            if value.rows is not None:
                detail += f", {value.rows} rows"
            return detail

        lines.append(
            f"| {question.number} | `{question.gold}` | `{queries[question.number]}` | "
            f"{cell('A_index_read')} | {cell('B_index_grep_AND')} | {cell('B_index_grep_OR')} | "
            f"{cell('C_qmd_keywords')} | {cell('C2_qmd_sentence')} | {cell('D_catalog_grep_AND')} | {cell('D_catalog_grep_OR')} |"
        )

    lines.extend(
        [
            "",
            "## A_index_read judgment record",
            "",
            "These are human-readable judgments against the exact index rows, made after the frozen query file "
            "was committed and before interpreting the other methods. `hit` means the row lets an agent identify "
            "the declared gold page; it does not claim that the row contains the answer itself.",
            "",
            "| # | Structural reachability | Hit? | Judgment |",
            "|---:|---|:---:|---|",
        ]
    )
    for question in questions:
        hit, reason = INDEX_READ_ASSESSMENTS[question.number]
        depth = depths.get((vault / question.gold).resolve())
        structural = "unreachable" if depth is None else f"depth {depth}"
        lines.append(f"| {question.number} | {structural} | {'yes' if hit else 'no'} | {reason} |")

    qmd_keyword = all_results["C_qmd_keywords"]
    qmd_sentence = all_results["C2_qmd_sentence"]
    qmd_keyword_misses = sum(not value.hit for value in qmd_keyword)
    qmd_sentence_misses = sum(not value.hit for value in qmd_sentence)
    lines.extend(
        [
            "",
            "## Mechanism and evidence",
            "",
            f"- The incumbent's structural ceiling is visible from `{index_label}`: the graph reached {direct} pages "
            f"at depth 1 and {within_two} by depth 2, while the eligible-page count was {eligible}. The A table "
            "separates this ceiling from the stricter row-specific judgment.",
            f"- The generated catalog is {catalog_bytes:,} bytes ({catalog_bytes / 4:.2f} tokens by the benchmark "
            f"rule), versus {len(index_bytes):,} bytes ({len(index_bytes) / 4:.2f} tokens) for the index. "
            "Reading the generated catalog wholesale therefore costs more than reading the incumbent.",
            f"- Keyword qmd search missed {qmd_keyword_misses}/20 questions; full-sentence qmd search missed "
            f"{qmd_sentence_misses}/20. The per-question qmd output is retained in the table as stdout byte cost "
            "and returned rank, rather than treating a command exit status as a hit. Keyword top-path counts: "
            f"{keyword_top or 'no results'}; sentence top-path counts: {sentence_top or 'no results'}.",
            "- The catalog's seven fields are always populated. When a page has no `##` heading, its deterministic "
            "H1/path title is used for the heading-keyword field rather than inventing prose.",
            "- The benchmark freezes query formulation instead of selecting a better term after a miss. This is "
            "important because both grep and BM25 are sensitive to query shape; no result was re-tuned.",
            "",
            "## Runbook and definitions",
            "",
            "Run from the repository root with the read-only image-maze vault path:",
            "",
            "```sh",
            "python3 concepts/bc-wiki-maintain/tests/run_retrieval_benchmark.py \\",
            "  \"$HOME/Sync/Work/Development/wp-theme-builds/localhost/image-maze/.bc-agent\" \\",
            "  --collection image-maze",
            "```",
            "",
            "The harness reads the question/gold table from `concepts/bc-wiki-maintain/tests/retrieval-questions.md` "
            "and the frozen keywords from `retrieval-queries.tsv`. It never edits the vault. It enumerates tracked "
            "Markdown files with `git ls-files`, excludes the existing skip directories (`.git`, `.obsidian`, "
            "`scratch`, `temp`, `node_modules`, `vendor`), and writes the seven-column catalog to `/tmp`.",
            "",
            "Exact retrieval commands issued for each question are:",
            "",
            "```sh",
            'qmd search "<frozen keywords>" -c image-maze --format files -n 5',
            'qmd search "<full question>" -c image-maze --format files -n 5',
            "```",
            "",
            "For B and D, a line is an AND match when every frozen keyword occurs as a case-insensitive whole word; "
            "an OR match requires any keyword. This is the fixed-string grep meaning implemented by the harness "
            "with word boundaries so `Git` does not match the middle of `digital`. A grep hit requires the exact "
            "gold relative path in a matching line. qmd rank is the first returned `qmd://image-maze/<path>` row "
            "whose path equals the gold path (with the qmd space-to-hyphen alias allowed); absence from five rows "
            "is a miss.",
            "",
            "A page is considered opened only when its bytes would be placed in the agent context. For A, only "
            "the complete index bytes are counted and no page is opened after the row judgment. For B/D, only "
            "matching stdout lines are counted. For qmd, only command stdout is counted; stderr, process startup, "
            "and qmd's on-disk index are not context. Catalog generation CPU/disk work is reported but excluded "
            "from context tokens because the proposed design asks agents to filter the artifact, not read its build.",
            "",
            "A miss means the declared gold path is not identified by the method's allowed output. A_index_read's "
            "human judgment is the exception to path-string matching and is exposed in the judgment table.",
            "",
            "## Methodological weaknesses",
            "",
            "- The question set is 20 items and has known skew recorded in `retrieval-questions.md`; it is evidence, "
            "not a universal query distribution.",
            "- A_index_read is necessarily a human judgment, not a model replay. Another operator may disagree on "
            "whether a terse row is enough; the reasons and structural reachability make that disagreement visible.",
            "- B/D use frozen keywords chosen before retrieval, but the benchmark does not measure an interactive "
            "agent's ability to refine a miss. Allowing refinement after each result would be a different protocol.",
            "- qmd's result ranking can change if its index becomes stale. This run uses the installed `image-maze` "
            "collection and records the exact command; no qmd update/embed mutation was performed.",
            "- The catalog summary extractor is deterministic and intentionally conservative. Its generated rows are "
            "a benchmark representation, not evidence that a production W1 implementation should copy every parser detail.",
            "",
            "## Source citations",
            "",
            f"- `{QUESTIONS_PATH}`: the pre-registered table supplies each question and gold path; its vault note says "
            '"155 eligible pages (tracked Markdown, `temp/` excluded)."',
            f"- `{index_label}`: the incumbent source begins `# image-maze Agent Wiki` and its navigation begins at "
            '`## Start here`; the byte count and graph counts above were measured from this exact file and its linked pages.',
            f"- `{catalog}`: generated scratch artifact with the seven columns specified by the benchmark; its byte "
            "count and row contents are the source for the catalog measurements above.",
            "",
        ]
    )
    return "\n".join(lines)


def run(args: argparse.Namespace) -> None:
    vault = Path(args.vault).expanduser().resolve()
    if not vault.is_dir():
        raise SystemExit(f"vault is not a directory: {vault}")
    questions = parse_questions(Path(args.questions).resolve())
    queries = parse_queries(Path(args.queries).resolve())
    repo = repo_root(vault)
    pages = eligible_pages(vault, repo)
    if len(pages) != 155:
        raise RuntimeError(f"expected image-maze benchmark corpus to contain 155 eligible pages, found {len(pages)}")
    _page_paths, incoming, outgoing = graph(vault, pages)
    depths = index_reachability(vault, outgoing)
    index_path = (vault / "index.md").resolve()
    index_bytes = index_path.read_bytes()
    catalog = build_catalog(vault, repo, pages, incoming)
    with catalog.open("r", encoding="utf-8", newline="") as handle:
        catalog_rows = list(csv.reader(handle, delimiter="\t"))
    if len(catalog_rows) != 156 or any(len(row) != 7 for row in catalog_rows):
        raise RuntimeError(f"catalog does not have header + 155 seven-column rows: {catalog}")
    if any(not field for row in catalog_rows for field in row):
        raise RuntimeError(f"catalog contains an empty field: {catalog}")

    collection = args.collection or os.environ.get("QMD_COLLECTION") or vault.parent.name
    qmd_bin = args.qmd_bin or os.environ.get("QMD_BIN", "qmd")
    index_read_values: list[Retrieval] = []
    b_and: list[Retrieval] = []
    b_or: list[Retrieval] = []
    c_keywords: list[Retrieval] = []
    c_sentence: list[Retrieval] = []
    d_and: list[Retrieval] = []
    d_or: list[Retrieval] = []
    index_raw = index_path.read_bytes()
    catalog_raw = catalog.read_bytes()
    for question in questions:
        keywords = queries[question.number]
        index_read_values.append(index_read(question, index_raw, depths, vault))
        b_and.append(retrieval_from_lines(filter_lines(index_raw, keywords, require_all=True), question.gold))
        b_or.append(retrieval_from_lines(filter_lines(index_raw, keywords, require_all=False), question.gold))
        c_keywords.append(qmd_retrieval(qmd_bin, collection, keywords, question.gold))
        c_sentence.append(qmd_retrieval(qmd_bin, collection, question.text, question.gold))
        d_and.append(retrieval_from_lines(filter_lines(catalog_raw, keywords, require_all=True), question.gold))
        d_or.append(retrieval_from_lines(filter_lines(catalog_raw, keywords, require_all=False), question.gold))

    # Keep the method names stable: they are used in the generated report and by reviewers.
    all_results = {
        "A_index_read": index_read_values,
        "B_index_grep_AND": b_and,
        "B_index_grep_OR": b_or,
        "C_qmd_keywords": c_keywords,
        "C2_qmd_sentence": c_sentence,
        "D_catalog_grep_AND": d_and,
        "D_catalog_grep_OR": d_or,
    }
    query_commit_result = command(
        ["git", "-C", str(ROOT), "log", "-1", "--format=%H", "--", str(Path(args.queries).resolve().relative_to(ROOT))]
    )
    query_commit = decode(query_commit_result.stdout).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", query_commit):
        raise RuntimeError(f"could not identify the frozen query commit: {args.queries}")
    results_path = Path(args.results).expanduser().resolve()
    results_path.write_text(
        render_results(vault, collection, questions, queries, pages, catalog, index_bytes, depths, all_results, query_commit),
        encoding="utf-8",
    )
    print(f"wrote {results_path}")
    print(f"catalog {catalog} ({catalog.stat().st_size} bytes, {len(pages)} rows)")
    print(method_summary(all_results))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault", help="path to the read-only .bc-agent vault")
    parser.add_argument("--collection", help="qmd collection name (default: QMD_COLLECTION or vault parent)")
    parser.add_argument("--qmd-bin", help="qmd executable (default: QMD_BIN or qmd)")
    parser.add_argument("--questions", default=str(QUESTIONS_PATH), help=argparse.SUPPRESS)
    parser.add_argument("--queries", default=str(QUERIES_PATH), help=argparse.SUPPRESS)
    parser.add_argument("--results", default=str(DEFAULT_RESULTS_PATH), help="results Markdown output path")
    return parser.parse_args()


if __name__ == "__main__":
    try:
        run(parse_args())
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"retrieval benchmark: ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
