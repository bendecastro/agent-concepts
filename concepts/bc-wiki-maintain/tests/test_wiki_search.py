#!/usr/bin/env python3
"""Tests for the no-index wiki search fallback."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import shutil
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


def test_documented_search_runs_from_an_installed_skill(tmp_path, monkeypatch):
    home = tmp_path / "new home"
    installed = home / ".agents/skills/bc-wiki-maintain"
    shutil.copytree(SCRIPT.parent, installed)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("AGENT_CONCEPTS", raising=False)

    vault = tmp_path / "vault with spaces"
    vault.mkdir()
    (vault / "AGENTS.md").write_text("# Vault\n")
    (vault / "answer.md").write_text("# Answer\n\nObsidian quartz is the answer.\n")
    run("git", "init", "-q", cwd=vault)
    run("git", "add", "AGENTS.md", "answer.md", cwd=vault)

    skill = (installed / "SKILL.md").read_text(encoding="utf-8")
    commands = [block for block in re.findall(r"```bash\n(.*?)```", skill, re.S)
                if "wiki_search.py" in block]
    assert len(commands) == 2  # live instructions and pasteable vault block
    for command in commands:
        result = run("bash", "-eu", "-c", command.replace('"term one" "term two"', '"obsidian" "quartz"'),
                     cwd=vault, check=False)
        assert result.returncode == 0, result.stderr
        assert result.stdout.splitlines() == ["answer.md"]


def test_documented_search_uses_the_agent_concepts_checkout(tmp_path, monkeypatch):
    checkout = tmp_path / "checkout"
    shutil.copytree(SCRIPT.parent, checkout / "concepts/bc-wiki-maintain/body")
    monkeypatch.setenv("HOME", str(tmp_path / "home without an install"))
    monkeypatch.setenv("AGENT_CONCEPTS", str(checkout))

    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "AGENTS.md").write_text("# Vault\n")
    (vault / "answer.md").write_text("# Answer\n\nObsidian quartz is the answer.\n")
    run("git", "init", "-q", cwd=vault)
    run("git", "add", "AGENTS.md", "answer.md", cwd=vault)

    skill = SCRIPT.with_name("SKILL.md").read_text(encoding="utf-8")
    commands = [block for block in re.findall(r"```bash\n(.*?)```", skill, re.S)
                if "wiki_search.py" in block]
    assert len(commands) == 2
    for command in commands:
        result = run("bash", "-eu", "-c", command.replace('"term one" "term two"', '"obsidian" "quartz"'),
                     cwd=vault, check=False)
        assert result.returncode == 0, result.stderr
        assert result.stdout.splitlines() == ["answer.md"]


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
