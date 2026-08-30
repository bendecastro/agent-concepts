#!/usr/bin/env python3
"""Tests for the no-index wiki search fallback."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "concepts/bc-wiki-maintain/body/wiki_search.py"
SPEC = importlib.util.spec_from_file_location("wiki_search", SCRIPT)
assert SPEC and SPEC.loader
WIKI_SEARCH = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = WIKI_SEARCH
SPEC.loader.exec_module(WIKI_SEARCH)


def run(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=check)


class WikiSearchTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        vault = root / "vault"
        vault.mkdir()
        (vault / "index.md").write_text("# Index\n", encoding="utf-8")
        (vault / "alpha.md").write_text(
            "# Alpha\n\nThe durable widget contract is documented here.\n", encoding="utf-8"
        )
        (vault / "beta.md").write_text(
            "# Beta\n\nThe widget contract has a short note.\n", encoding="utf-8"
        )
        (vault / "temp").mkdir()
        (vault / "temp" / "ignored-by-directory.md").write_text("# Ignored\n", encoding="utf-8")
        (root / ".gitignore").write_text("vault/ignored-by-rule.md\n", encoding="utf-8")
        (vault / "ignored-by-rule.md").write_text("# Ignored\n", encoding="utf-8")
        run("git", "init", "-q", cwd=root)
        run("git", "config", "user.name", "Test", cwd=root)
        run("git", "config", "user.email", "test@example.invalid", cwd=root)
        run("git", "add", ".", cwd=root)
        run("git", "commit", "-qm", "initial", cwd=root)
        # A tracked path matching .gitignore must still be excluded by check-ignore --no-index.
        run("git", "add", "-f", "vault/ignored-by-rule.md", cwd=root)
        run("git", "commit", "-qm", "track ignored fixture", cwd=root)
        return temp, root, vault

    def test_eligibility_is_tracked_markdown_and_honors_ignore_rules(self) -> None:
        temp, root, vault = self.make_repo()
        with temp:
            paths = WIKI_SEARCH.tracked_markdown_paths(vault, root)
            self.assertEqual([relative for relative, _ in paths], ["vault/alpha.md", "vault/beta.md", "vault/index.md"])
            self.assertEqual(len(WIKI_SEARCH.load_documents(vault)), 3)

    def test_untracked_markdown_is_invisible_until_git_added(self) -> None:
        temp, root, vault = self.make_repo()
        with temp:
            new_page = vault / "new-page.md"
            new_page.write_text(
                "# New page\n\nThe freshly created visibility contract is here.\n", encoding="utf-8"
            )
            before_add = WIKI_SEARCH.rank_documents(
                WIKI_SEARCH.load_documents(vault), "freshly created visibility", limit=15
            )
            self.assertNotIn("new-page.md", [item.relative for item in before_add])

            run("git", "add", str(new_page), cwd=root)
            after_add = WIKI_SEARCH.rank_documents(
                WIKI_SEARCH.load_documents(vault), "freshly created visibility", limit=15
            )
            self.assertIn("new-page.md", [item.relative for item in after_add])

    def test_bm25_ranks_matching_specific_page_and_ties_by_path(self) -> None:
        documents = [
            WIKI_SEARCH.Document("z.md", WIKI_SEARCH.Counter({"needle": 1}), 1),
            WIKI_SEARCH.Document("a.md", WIKI_SEARCH.Counter({"needle": 1}), 1),
            WIKI_SEARCH.Document("none.md", WIKI_SEARCH.Counter(), 1),
        ]
        ranked = WIKI_SEARCH.rank_documents(documents, "needle", limit=10)
        self.assertEqual([item.relative for item in ranked], ["a.md", "z.md"])
        self.assertGreater(ranked[0].score, 0)

    def test_cli_is_compact_and_supports_unquoted_terms(self) -> None:
        temp, root, vault = self.make_repo()
        with temp:
            result = run("python3", str(SCRIPT), str(vault), "durable", "widget", "-n", "2", cwd=ROOT)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.splitlines(), ["alpha.md", "beta.md"])
            self.assertNotIn("score", result.stdout.lower())

    def test_cli_rejects_empty_query(self) -> None:
        temp, root, vault = self.make_repo()
        with temp:
            result = run("python3", str(SCRIPT), str(vault), "...", cwd=ROOT, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("at least one alphanumeric term", result.stderr)


if __name__ == "__main__":
    unittest.main()
