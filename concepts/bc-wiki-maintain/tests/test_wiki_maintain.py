#!/usr/bin/env python3
"""CLI and runner regression tests for bc-wiki-maintain safety contracts."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[3]
LINTER = ROOT / "concepts/bc-wiki-maintain/body/wiki_lint.py"
RUNNER = ROOT / "concepts/bc-wiki-maintain/body/runner/run-promotion.sh"
SKILL = ROOT / "concepts/bc-wiki-maintain/body/SKILL.md"


def run(*args: str, cwd: Path | None = None, env: dict[str, str] | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True, check=check)


def git(repo: Path, *args: str) -> str:
    return run("git", "-C", str(repo), *args).stdout.strip()


def make_repo(log: str) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
    temp = tempfile.TemporaryDirectory()
    repo = Path(temp.name) / "repo"
    repo.mkdir()
    vault = repo / "vault"
    vault.mkdir()
    (vault / "index.md").write_text("# Index\n\n- [page](page.md)\n", encoding="utf-8")
    (vault / "page.md").write_text("# Page\n", encoding="utf-8")
    (vault / "log.md").write_text(log, encoding="utf-8")
    run("git", "init", "-q", cwd=repo)
    run("git", "config", "user.name", "Test", cwd=repo)
    run("git", "config", "user.email", "test@example.invalid", cwd=repo)
    run("git", "add", ".", cwd=repo)
    run("git", "commit", "-qm", "initial", cwd=repo)
    return temp, repo, vault


def runner_env(repo: Path, vault: Path, pi: Path, **extra: str) -> dict[str, str]:
    env = os.environ.copy()
    env.update({
        "AGENT_CONCEPTS": str(ROOT),
        "VAULT_ROOT": str(vault),
        "PI_BIN": str(pi),
        "PROMOTION_SKILL": str(SKILL),
    })
    env.update(extra)
    return env


class WikiLintCliTests(unittest.TestCase):
    def test_code_examples_and_log_links_are_not_graph_findings(self) -> None:
        temp, repo, vault = make_repo("## [2026-08-01] evidence\n\nSee [[missing-log]].\n")
        with temp:
            (vault / "index.md").write_text(
                "# Index\n\n- [page](page.md)\n- [examples](examples.md)\n", encoding="utf-8"
            )
            (vault / "examples.md").write_text(
                """# Examples

Inline `[[missing-inline]]` and `[missing](missing-inline-md.md)`.

```markdown
[[missing-fenced]]
[missing](missing-fenced-md.md)
```

Prose [[missing-prose]].
""",
                encoding="utf-8",
            )
            result = run("python3", str(LINTER), str(vault), cwd=ROOT, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("Broken links: 1", result.stdout)
            self.assertIn("examples.md -> [[missing-prose]]", result.stdout)
            self.assertNotIn("missing-inline", result.stdout)
            self.assertNotIn("missing-fenced", result.stdout)
            self.assertNotIn("missing-log", result.stdout)

    def test_initial_and_subsequent_promotion_ranges(self) -> None:
        temp, repo, vault = make_repo(
            "## [2026-08-01] first\n\n## [2026-08-03] second\n\n```text\n## [2026-09-09] example\n```\n"
        )
        with temp:
            initial = run("python3", str(LINTER), str(vault), "--json", cwd=ROOT)
            report = json.loads(initial.stdout)
            promotion = report["unpromoted_log"]
            self.assertEqual(promotion["count"], 2)
            self.assertEqual(promotion["range"], "2026-08-01..2026-08-03")
            self.assertEqual(promotion["headings"], ["## [2026-08-01] first", "## [2026-08-03] second"])
            rendered = run("python3", str(LINTER), str(vault), cwd=ROOT, check=False)
            self.assertIn("PROMOTION_HEADING\t## [2026-08-01] first", rendered.stdout)
            self.assertIn("PROMOTION_HEADING\t## [2026-08-03] second", rendered.stdout)

            (vault / "promoted.md").write_text("# Promoted\n", encoding="utf-8")
            run("git", "add", str(vault / "promoted.md"), cwd=repo)
            run("git", "commit", "-qm", "wiki: promote log entries 2026-08-01..2026-08-03", cwd=repo)
            with (vault / "log.md").open("a", encoding="utf-8") as handle:
                handle.write("\n## [2026-08-05] third\n")
            run("git", "add", str(vault / "log.md"), cwd=repo)
            run("git", "commit", "-qm", "capture third", cwd=repo)

            subsequent = run("python3", str(LINTER), str(vault), "--json", cwd=ROOT)
            report = json.loads(subsequent.stdout)
            promotion = report["unpromoted_log"]
            self.assertEqual(promotion["count"], 1)
            self.assertEqual(promotion["range"], "2026-08-05..2026-08-05")
            self.assertEqual(promotion["headings"], ["## [2026-08-05] third"])

    def test_newer_promotion_in_another_vault_does_not_reset_boundary(self) -> None:
        temp = tempfile.TemporaryDirectory()
        repo = Path(temp.name) / "repo"
        vault_a = repo / "vault-a"
        vault_b = repo / "vault-b"
        vault_a.mkdir(parents=True)
        vault_b.mkdir()
        for vault, date in ((vault_a, "2026-08-01"), (vault_b, "2026-08-02")):
            (vault / "index.md").write_text("# Index\n", encoding="utf-8")
            (vault / "page.md").write_text("# Page\n", encoding="utf-8")
            (vault / "log.md").write_text(f"## [{date}] initial\n", encoding="utf-8")
        run("git", "init", "-q", cwd=repo)
        run("git", "config", "user.name", "Test", cwd=repo)
        run("git", "config", "user.email", "test@example.invalid", cwd=repo)
        run("git", "add", ".", cwd=repo)
        run("git", "commit", "-qm", "initial", cwd=repo)
        with temp:
            (vault_a / "promoted.md").write_text("# A promoted\n", encoding="utf-8")
            run("git", "add", str(vault_a / "promoted.md"), cwd=repo)
            run("git", "commit", "-qm", "wiki: promote log entries 2026-08-01..2026-08-01", cwd=repo)
            with (vault_a / "log.md").open("a", encoding="utf-8") as handle:
                handle.write("\n## [2026-08-03] A second\n")
            run("git", "add", str(vault_a / "log.md"), cwd=repo)
            run("git", "commit", "-qm", "capture A second", cwd=repo)

            (vault_b / "promoted.md").write_text("# B promoted\n", encoding="utf-8")
            run("git", "add", str(vault_b / "promoted.md"), cwd=repo)
            run("git", "commit", "-qm", "wiki: promote log entries 2026-08-02..2026-08-02", cwd=repo)
            with (vault_a / "log.md").open("a", encoding="utf-8") as handle:
                handle.write("\n## [2026-08-04] A third\n")
            run("git", "add", str(vault_a / "log.md"), cwd=repo)
            run("git", "commit", "-qm", "capture A third", cwd=repo)

            report = json.loads(run("python3", str(LINTER), str(vault_a), "--json", cwd=ROOT).stdout)
            promotion = report["unpromoted_log"]
            self.assertEqual(promotion["count"], 2)
            self.assertEqual(promotion["range"], "2026-08-03..2026-08-04")

    def test_nonstandard_headings_keep_promotion_required_and_invalid_range(self) -> None:
        temp, repo, vault = make_repo("## [2026-08-01] first\n\n## not dated\n")
        with temp:
            initial = run("python3", str(LINTER), str(vault), "--json", cwd=ROOT)
            report = json.loads(initial.stdout)
            promotion = report["unpromoted_log"]
            self.assertEqual(promotion["count"], 2)
            self.assertIsNone(promotion["range"])
            self.assertTrue(report["promotion_required"])

            (vault / "promoted.md").write_text("# Promoted\n", encoding="utf-8")
            run("git", "add", str(vault / "promoted.md"), cwd=repo)
            run("git", "commit", "-qm", "wiki: promote log entries invalid", cwd=repo)
            with (vault / "log.md").open("a", encoding="utf-8") as handle:
                handle.write("\n## newly captured\n")
            run("git", "add", str(vault / "log.md"), cwd=repo)
            run("git", "commit", "-qm", "capture nonstandard", cwd=repo)

            subsequent = run("python3", str(LINTER), str(vault), "--json", cwd=ROOT)
            report = json.loads(subsequent.stdout)
            promotion = report["unpromoted_log"]
            self.assertEqual(promotion["count"], 1)
            self.assertIsNone(promotion["range"])
            self.assertTrue(report["promotion_required"])
            rendered = run("python3", str(LINTER), str(vault), cwd=ROOT, check=False)
            self.assertIn("PROMOTION_REQUIRED=1", rendered.stdout)
            self.assertIn("PROMOTION_RANGE=invalid", rendered.stdout)


class PromotionRunnerTests(unittest.TestCase):
    def write_pi(self, directory: Path, body: str) -> Path:
        pi = directory.parent / "fake-pi.sh"
        pi.write_text("#!/usr/bin/env bash\nset -eu\n" + textwrap.dedent(body), encoding="utf-8")
        pi.chmod(0o755)
        return pi

    def write_classify(self, body: str) -> str:
        return f"cat > \"$CLASSIFY_PATH\" <<'EOF'\n{body.rstrip()}\nEOF\n"

    def test_runner_creates_exact_range_commit(self) -> None:
        temp, repo, vault = make_repo("## [2026-08-10] first\n\n## [2026-08-14] last\n")
        with temp:
            classify = self.write_classify(
                '\n'.join([
                    json.dumps({"heading": "## [2026-08-10] first", "verdict": "promote", "reason": "new page", "page": "promoted.md"}),
                    json.dumps({"heading": "## [2026-08-14] last", "verdict": "skip", "reason": "already on page.md"}),
                ])
            )
            pi = self.write_pi(repo, classify + "printf '# promoted\\n' > \"$VAULT_ROOT/promoted.md\"\n")
            result = run("bash", str(RUNNER), cwd=repo, env=runner_env(repo, vault, pi), check=False)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertEqual(git(repo, "log", "-1", "--format=%s"), "wiki: promote log entries 2026-08-10..2026-08-14")
            self.assertEqual(git(repo, "status", "--porcelain"), "")
            self.assertNotIn("promotion-classification.jsonl", git(repo, "show", "--name-only", "--pretty=", "HEAD"))

    def test_missing_classification_refuses_commit(self) -> None:
        temp, repo, vault = make_repo("## [2026-08-10] first\n")
        with temp:
            pi = self.write_pi(repo, "printf '# promoted\\n' > \"$VAULT_ROOT/promoted.md\"\n")
            base = git(repo, "rev-parse", "HEAD")
            result = run("bash", str(RUNNER), cwd=repo, env=runner_env(repo, vault, pi), check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("classification does not cover every unpromoted heading", result.stderr)
            self.assertEqual(git(repo, "rev-parse", "HEAD"), base)
            self.assertIn("promoted.md", git(repo, "status", "--porcelain"))

    def test_partial_classification_refuses_commit(self) -> None:
        temp, repo, vault = make_repo("## [2026-08-10] first\n\n## [2026-08-14] last\n")
        with temp:
            classify = self.write_classify(
                json.dumps({"heading": "## [2026-08-10] first", "verdict": "promote", "reason": "new page", "page": "promoted.md"})
            )
            pi = self.write_pi(repo, classify + "printf '# promoted\\n' > \"$VAULT_ROOT/promoted.md\"\n")
            base = git(repo, "rev-parse", "HEAD")
            result = run("bash", str(RUNNER), cwd=repo, env=runner_env(repo, vault, pi), check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing headings", result.stderr)
            self.assertEqual(git(repo, "rev-parse", "HEAD"), base)

    def test_verify_classify_accepts_complete_jsonl(self) -> None:
        temp, repo, vault = make_repo("## [2026-08-10] first\n\n## [2026-08-14] last\n")
        with temp:
            classify = repo.parent / "classify.jsonl"
            classify.write_text(
                json.dumps({"heading": "## [2026-08-10] first", "verdict": "skip", "reason": "already represented"}) + "\n"
                + json.dumps({"heading": "## [2026-08-14] last", "verdict": "conflict", "reason": "spike vs ADR", "page": "open-questions/bar.md"}) + "\n",
                encoding="utf-8",
            )
            result = run("python3", str(LINTER), str(vault), "--verify-classify", str(classify), cwd=ROOT)
            self.assertEqual(result.stdout, "")
            self.assertEqual(result.returncode, 0)

    def assert_staged_change_fails_closed(self, stage_body: str, expected_staged_path: str | None = None) -> None:
        temp, repo, vault = make_repo("## [2026-08-10] first\n")
        with temp:
            pi = self.write_pi(repo, stage_body)
            base = git(repo, "rev-parse", "HEAD")
            result = run("bash", str(RUNNER), cwd=repo, env=runner_env(repo, vault, pi), check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("staged", result.stderr)
            self.assertEqual(git(repo, "rev-parse", "HEAD"), base)
            self.assertNotEqual(git(repo, "status", "--porcelain"), "")
            if expected_staged_path is not None:
                self.assertEqual(git(repo, "diff", "--cached", "--name-only"), expected_staged_path)

    def test_staged_inside_vault_fails_before_commit(self) -> None:
        self.assert_staged_change_fails_closed(
            "printf '# inside\\n' > \"$VAULT_ROOT/inside.md\"\n"
            "git -C \"$VAULT_ROOT/..\" add \"$VAULT_ROOT/inside.md\"\n",
            "vault/inside.md",
        )

    def test_staged_outside_vault_fails_before_commit(self) -> None:
        self.assert_staged_change_fails_closed(
            "printf 'outside\\n' > \"$VAULT_ROOT/../outside.md\"\n"
            "git -C \"$VAULT_ROOT/..\" add outside.md\n",
            "outside.md",
        )

    def test_staged_deletion_fails_before_commit(self) -> None:
        self.assert_staged_change_fails_closed("git rm \"$VAULT_ROOT/page.md\"\n")

    def test_invalid_required_range_fails_before_agent(self) -> None:
        temp, repo, vault = make_repo("## [2026-08-10] first\n")
        with temp:
            detector = repo.parent / "detector.py"
            marker = repo / "agent-ran"
            detector.write_text(
                "#!/usr/bin/env python3\nprint('PROMOTION_REQUIRED=1')\nprint('PROMOTION_RANGE=invalid')\n",
                encoding="utf-8",
            )
            detector.chmod(0o755)
            pi = self.write_pi(repo, f"touch {marker}\n")
            env = runner_env(repo, vault, pi, DETECTION_SCRIPT=str(detector))
            base = git(repo, "rev-parse", "HEAD")
            result = run("bash", str(RUNNER), cwd=repo, env=env, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("promotion required but detector did not emit a valid PROMOTION_RANGE", result.stderr)
            self.assertFalse(marker.exists())
            self.assertEqual(git(repo, "rev-parse", "HEAD"), base)


if __name__ == "__main__":
    unittest.main()
