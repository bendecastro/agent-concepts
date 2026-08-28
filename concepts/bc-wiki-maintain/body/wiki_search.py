#!/usr/bin/env python3
"""Search a Markdown agent vault without an index or third-party dependency.

This is the default single-vault reader: it reads tracked Markdown files from the vault's Git
repository at query time, scores them with BM25, and writes only ranked vault-
relative paths to stdout. It never writes the vault or a search artifact.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import math
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Iterable


SKIP_DIR_NAMES = {".git", ".obsidian", "scratch", "temp", "node_modules", "vendor"}
DEFAULT_LIMIT = 15
BM25_K1 = 1.2
BM25_B = 0.75
TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:['\u2019][A-Za-z0-9]+)?")


@dataclass(frozen=True)
class Document:
    relative: str
    term_counts: Counter[str]
    length: int


@dataclass(frozen=True)
class RankedDocument:
    relative: str
    score: float


def git_command(repo: Path, *args: str, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            input=input_bytes,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        raise RuntimeError(f"could not run git: {exc}") from exc


def resolve_repo(vault: Path) -> Path:
    result = git_command(vault, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"vault is not inside a Git repository: {vault}{': ' + detail if detail else ''}")
    value = result.stdout.decode("utf-8", errors="strict").strip()
    if not value:
        raise RuntimeError(f"Git returned no repository root for vault: {vault}")
    return Path(value).resolve()


def tracked_markdown_paths(vault: Path, repo: Path) -> list[tuple[str, Path]]:
    """Return eligible (repository-relative, absolute) tracked Markdown paths.

    The candidate list comes from ``git ls-files``.  ``git check-ignore
    --no-index`` is then applied in one batch so tracked files matching an
    ignore rule are excluded too; ``--no-index`` is intentional because a
    tracked path would otherwise bypass the ignore rules.
    """
    listed = git_command(repo, "ls-files", "-z")
    if listed.returncode != 0:
        detail = listed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git ls-files failed: {detail or 'unknown error'}")

    vault = vault.resolve()
    candidates: list[tuple[str, Path]] = []
    for raw in listed.stdout.split(b"\0"):
        if not raw:
            continue
        relative = os.fsdecode(raw)
        if Path(relative).suffix.lower() != ".md":
            continue
        path = (repo / Path(relative)).resolve()
        try:
            vault_relative = path.relative_to(vault)
        except ValueError:
            continue
        if not path.is_file() or any(part in SKIP_DIR_NAMES for part in vault_relative.parts):
            continue
        candidates.append((relative, path))

    if not candidates:
        return []

    check = git_command(
        repo,
        "check-ignore",
        "--no-index",
        "--stdin",
        "-z",
        input_bytes=b"".join(os.fsencode(relative) + b"\0" for relative, _ in candidates),
    )
    if check.returncode not in (0, 1):
        detail = check.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git check-ignore failed: {detail or 'unknown error'}")
    ignored = {os.fsdecode(raw) for raw in check.stdout.split(b"\0") if raw}
    return [(relative, path) for relative, path in candidates if relative not in ignored]


def tokenize(value: str) -> list[str]:
    """Tokenize text consistently for both query terms and page content."""
    return [match.group(0).casefold() for match in TOKEN_RE.finditer(value)]


def load_documents(vault: Path) -> list[Document]:
    """Read the eligible vault pages at query time; no on-disk state is created."""
    repo = resolve_repo(vault)
    documents: list[Document] = []
    for _repo_relative, path in tracked_markdown_paths(vault, repo):
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            raise RuntimeError(f"could not read eligible page {path}: {exc}") from exc
        terms = tokenize(content)
        documents.append(Document(path.relative_to(vault.resolve()).as_posix(), Counter(terms), len(terms)))
    return sorted(documents, key=lambda document: document.relative)


def rank_documents(documents: Iterable[Document], query: str, limit: int = DEFAULT_LIMIT) -> list[RankedDocument]:
    """Return the top ``limit`` documents using the standard BM25 formula."""
    if limit < 1:
        raise ValueError("limit must be at least 1")
    query_terms = list(dict.fromkeys(tokenize(query)))
    if not query_terms:
        raise ValueError("query must contain at least one alphanumeric term")

    corpus = list(documents)
    if not corpus:
        return []
    average_length = sum(document.length for document in corpus) / len(corpus) or 1.0
    document_frequency = {
        term: sum(term in document.term_counts for document in corpus)
        for term in query_terms
    }
    scores: list[RankedDocument] = []
    for document in corpus:
        score = 0.0
        normalizer = BM25_K1 * (1 - BM25_B + BM25_B * document.length / average_length)
        for term in query_terms:
            term_frequency = document.term_counts.get(term, 0)
            frequency = document_frequency[term]
            if not term_frequency or not frequency:
                continue
            inverse_document_frequency = math.log(1 + (len(corpus) - frequency + 0.5) / (frequency + 0.5))
            score += inverse_document_frequency * (
                term_frequency * (BM25_K1 + 1) / (term_frequency + normalizer)
            )
        if score > 0:
            scores.append(RankedDocument(document.relative, score))
    scores.sort(key=lambda item: (-item.score, item.relative))
    return scores[:limit]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault", help="path to the agent vault")
    parser.add_argument("query", nargs="+", help="one or more search terms")
    parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"maximum ranked paths to print (default: {DEFAULT_LIMIT})",
    )
    parser.add_argument(
        "--scores",
        action="store_true",
        help="include the BM25 score before each path (default output is paths only)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    vault = Path(args.vault).expanduser().resolve()
    if not vault.is_dir():
        print(f"wiki-search: vault is not a directory: {vault}", file=sys.stderr)
        return 2
    try:
        results = rank_documents(load_documents(vault), " ".join(args.query), args.limit)
    except (RuntimeError, ValueError) as exc:
        print(f"wiki-search: {exc}", file=sys.stderr)
        return 2
    for result in results:
        if args.scores:
            print(f"{result.score:.6f}\t{result.relative}")
        else:
            print(result.relative)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
