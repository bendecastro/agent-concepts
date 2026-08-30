#!/usr/bin/env python3
"""CLI and runner regression tests for bc-wiki-maintain safety contracts."""
from __future__ import annotations

import contextlib
import importlib.util
import io
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
NOTIFIER = ROOT / "concepts/bc-wiki-maintain/body/runner/notify-failure.sh"
RUNNER_DIR = ROOT / "concepts/bc-wiki-maintain/body/runner"
SKILL = ROOT / "concepts/bc-wiki-maintain/body/SKILL.md"
LINTER_SPEC = importlib.util.spec_from_file_location("bc_wiki_maintain_linter", LINTER)
assert LINTER_SPEC and LINTER_SPEC.loader
WIKI_LINT = importlib.util.module_from_spec(LINTER_SPEC)
LINTER_SPEC.loader.exec_module(WIKI_LINT)


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

    def test_mixed_dated_and_undatable_headings_narrow_promotion_range(self) -> None:
        temp, repo, vault = make_repo("## [2026-08-01] first\n\n## 2026-08-02\n\n## [2026-08-03] last\n")
        with temp:
            report = json.loads(run("python3", str(LINTER), str(vault), "--json", cwd=ROOT).stdout)
            promotion = report["unpromoted_log"]
            self.assertEqual(promotion["count"], 3)
            self.assertEqual(promotion["range"], "2026-08-01..2026-08-03")
            self.assertEqual(
                promotion["headings"],
                ["## [2026-08-01] first", "## 2026-08-02", "## [2026-08-03] last"],
            )
            self.assertEqual(promotion["undatable_headings"], ["## 2026-08-02"])
            self.assertTrue(report["promotion_required"])
            rendered = run("python3", str(LINTER), str(vault), cwd=ROOT, check=False)
            self.assertIn("PROMOTION_REQUIRED=1", rendered.stdout)
            self.assertIn("PROMOTION_RANGE=2026-08-01..2026-08-03", rendered.stdout)
            self.assertIn("PROMOTION_HEADING\t## 2026-08-02", rendered.stdout)
            self.assertIn("Warning: undatable unpromoted log headings: 1", rendered.stdout)
            self.assertIn("- ## 2026-08-02", rendered.stdout)

    def test_nonstandard_headings_keep_promotion_required_and_invalid_range(self) -> None:
        temp, repo, vault = make_repo("## 2026-08-01\n\n## not dated\n")
        with temp:
            initial = run("python3", str(LINTER), str(vault), "--json", cwd=ROOT, check=False)
            self.assertEqual(initial.returncode, 1)
            report = json.loads(initial.stdout)
            promotion = report["unpromoted_log"]
            self.assertEqual(promotion["count"], 2)
            self.assertIsNone(promotion["range"])
            self.assertEqual(promotion["undatable_headings"], ["## 2026-08-01", "## not dated"])
            self.assertTrue(report["promotion_required"])

            (vault / "promoted.md").write_text("# Promoted\n", encoding="utf-8")
            run("git", "add", str(vault / "promoted.md"), cwd=repo)
            run("git", "commit", "-qm", "wiki: promote log entries invalid", cwd=repo)
            with (vault / "log.md").open("a", encoding="utf-8") as handle:
                handle.write("\n## newly captured\n")
            run("git", "add", str(vault / "log.md"), cwd=repo)
            run("git", "commit", "-qm", "capture nonstandard", cwd=repo)

            subsequent = run("python3", str(LINTER), str(vault), "--json", cwd=ROOT, check=False)
            self.assertEqual(subsequent.returncode, 1)
            report = json.loads(subsequent.stdout)
            promotion = report["unpromoted_log"]
            self.assertEqual(promotion["count"], 1)
            self.assertIsNone(promotion["range"])
            self.assertTrue(report["promotion_required"])
            rendered = run("python3", str(LINTER), str(vault), cwd=ROOT, check=False)
            self.assertIn("PROMOTION_REQUIRED=1", rendered.stdout)
            self.assertIn("PROMOTION_RANGE=invalid", rendered.stdout)
            self.assertIn("Warning: undatable unpromoted log headings: 1", rendered.stdout)

    def test_all_undatable_required_range_exits_nonzero(self) -> None:
        temp, repo, vault = make_repo("## 2026-08-01\n\n## not dated\n")
        with temp:
            result = run("python3", str(LINTER), str(vault), cwd=ROOT, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("PROMOTION_REQUIRED=1", result.stdout)
            self.assertIn("PROMOTION_RANGE=invalid", result.stdout)
            self.assertIn("PROMOTION_HEADING\t## 2026-08-01", result.stdout)
            self.assertIn("PROMOTION_HEADING\t## not dated", result.stdout)

    def test_mixed_backlog_exits_zero_and_lists_undatable_heading(self) -> None:
        temp, repo, vault = make_repo(
            "## [2026-08-01] first\n\n## 2026-08-02\n\n## [2026-08-03] last\n"
        )
        with temp:
            result = run("python3", str(LINTER), str(vault), cwd=ROOT, check=False)
            self.assertEqual(result.returncode, 0)
            self.assertIn("PROMOTION_REQUIRED=1", result.stdout)
            self.assertIn("PROMOTION_RANGE=2026-08-01..2026-08-03", result.stdout)
            self.assertIn("PROMOTION_HEADING\t## 2026-08-02", result.stdout)
            self.assertIn("Warning: undatable unpromoted log headings: 1", result.stdout)


class QmdStatusTests(unittest.TestCase):
    def make_qmd_fixture(
        self,
        canonical_paths: list[Path],
        machine_paths: list[Path] | None = None,
        exclusion: bool = False,
    ) -> tuple[tempfile.TemporaryDirectory[str], Path, Path, Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        vault = root / "vault"
        (vault / "project").mkdir(parents=True)
        (vault / "index.md").write_text("# Index\n", encoding="utf-8")
        (vault / "log.md").write_text("", encoding="utf-8")
        if exclusion:
            (vault / "project" / "overview.md").write_text(
                "This vault is excluded from the global qmd index because it contains personal data.\n",
                encoding="utf-8",
            )
        canonical = root / "qmd-collections.yml"
        canonical.write_text(
            "collections:\n"
            + "".join(f"  collection-{index}:\n    path: {path}\n" for index, path in enumerate(canonical_paths)),
            encoding="utf-8",
        )
        machine = root / "index.yml"
        if machine_paths is not None:
            machine.write_text(
                "collections:\n"
                + "".join(f"  collection-{index}:\n    path: {path}\n" for index, path in enumerate(machine_paths)),
                encoding="utf-8",
            )
        return temp, vault, canonical, machine

    def render(self, vault: Path, canonical: Path, machine: Path) -> str:
        report = WIKI_LINT.lint(
            vault,
            90,
            qmd_registry=canonical,
            qmd_machine_index=machine,
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            WIKI_LINT.print_report(report)
        return output.getvalue()

    def test_registered_requires_canonical_and_machine_coverage(self) -> None:
        temp, vault, canonical, machine = self.make_qmd_fixture([])
        with temp:
            canonical.write_text(f"collections:\n  fixture:\n    path: {vault}\n", encoding="utf-8")
            machine.write_text(f"collections:\n  fixture:\n    path: {vault}\n", encoding="utf-8")
            status = WIKI_LINT.qmd_status(vault, canonical, machine)
            self.assertTrue(status["registered"])
            self.assertFalse(status["unindexed"])
            self.assertEqual(status["canonical_path"], str(vault))
            self.assertEqual(status["machine_path"], str(vault))

    def test_canonical_only_is_unindexed_and_renderer_names_drift(self) -> None:
        temp, vault, canonical, machine = self.make_qmd_fixture([], machine_paths=[])
        with temp:
            canonical.write_text(f"collections:\n  fixture:\n    path: {vault}\n", encoding="utf-8")
            output = self.render(vault, canonical, machine)
            self.assertIn("qmd registration: unindexed", output)
            self.assertIn(f"covered by canonical path {vault}", output)
            self.assertIn(f"machine index lacks a covering path at {machine}", output)
            status = WIKI_LINT.qmd_status(vault, canonical, machine)
            self.assertFalse(status["registered"])
            self.assertTrue(status["unindexed"])

    def test_documented_exclusion_remains_intentional_exclusion(self) -> None:
        temp, vault, canonical, machine = self.make_qmd_fixture([], machine_paths=[], exclusion=True)
        with temp:
            status = WIKI_LINT.qmd_status(vault, canonical, machine)
            self.assertFalse(status["registered"])
            self.assertFalse(status["unindexed"])
            self.assertTrue(status["intentional_exclusion"])

    def test_absent_from_both_registries_is_unregistered(self) -> None:
        temp, vault, canonical, machine = self.make_qmd_fixture([], machine_paths=[])
        with temp:
            status = WIKI_LINT.qmd_status(vault, canonical, machine)
            self.assertFalse(status["registered"])
            self.assertFalse(status["unindexed"])
            self.assertFalse(status["intentional_exclusion"])
            self.assertEqual(status["reason"], "vault path is absent from qmd registry")

    def test_missing_machine_index_falls_back_to_canonical_only(self) -> None:
        temp, vault, canonical, machine = self.make_qmd_fixture([])
        with temp:
            canonical.write_text(f"collections:\n  fixture:\n    path: {vault}\n", encoding="utf-8")
            status = WIKI_LINT.qmd_status(vault, canonical, machine)
            self.assertTrue(status["registered"])
            self.assertFalse(status["unindexed"])
            self.assertIn("machine index unavailable", status["reason"])
            self.assertIn("reporting canonical-only coverage", status["reason"])

    def test_nested_vault_below_registered_collection_is_covered(self) -> None:
        temp, vault, canonical, machine = self.make_qmd_fixture([])
        with temp:
            parent = vault.parent / "collection-root"
            nested = parent / "nested" / "vault"
            nested.mkdir(parents=True)
            canonical.write_text(f"collections:\n  fixture:\n    path: {parent}\n", encoding="utf-8")
            machine.write_text(f"collections:\n  fixture:\n    path: {parent}\n", encoding="utf-8")
            status = WIKI_LINT.qmd_status(nested, canonical, machine)
            self.assertTrue(status["registered"])
            self.assertFalse(status["unindexed"])
            self.assertEqual(status["canonical_path"], str(parent.resolve()))
            self.assertEqual(status["machine_path"], str(parent.resolve()))


class FailureNotificationTests(unittest.TestCase):
    def write_command(self, directory: Path, name: str, body: str) -> Path:
        command = directory / name
        command.write_text("#!/usr/bin/env bash\nset -eu\n" + textwrap.dedent(body), encoding="utf-8")
        command.chmod(0o755)
        return command

    def test_runner_services_start_the_failure_notifier(self) -> None:
        expected = "OnFailure=bc-wiki-notify@%n.service"
        for filename in ("bc-wiki-maintain.service", "bc-wiki-lint.service"):
            self.assertIn(expected, (RUNNER_DIR / filename).read_text(encoding="utf-8"))

    def test_notifier_fails_when_desktop_display_is_unavailable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            result = run(
                "/usr/bin/bash",
                str(NOTIFIER),
                "bc-wiki-maintain.service",
                cwd=ROOT,
                env={"PATH": temp},
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("notify-send is unavailable", result.stderr)

    def test_notifier_includes_vault_and_journal_reason(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            args_file = directory / "notify-args"
            self.write_command(
                directory,
                "systemctl",
                """
                case "$*" in
                  *SyslogIdentifier*) printf '%s\\n' 'SyslogIdentifier=bc-wiki-maintain' ;;
                  *Environment*) printf '%s\\n' 'Environment=AGENT_CONCEPTS=/tmp/concepts VAULT_ROOT=/tmp/example-vault' ;;
                  *) exit 1 ;;
                esac
                """,
            )
            self.write_command(
                directory,
                "journalctl",
                """
                case "$*" in
                  *"-u bc-wiki-maintain.service"*) ;;
                  *) exit 1 ;;
                esac
                case "$*" in
                  *"-t bc-wiki-maintain"*) printf '%s\\n' 'detector failed: example reason' ;;
                  *) exit 1 ;;
                esac
                """,
            )
            self.write_command(
                directory,
                "notify-send",
                "printf '%s\\n' \"$@\" > \"$NOTIFY_ARGS_FILE\"\n",
            )
            env = os.environ.copy()
            env.update({
                "PATH": f"{directory}{os.pathsep}{env['PATH']}",
                "NOTIFY_ARGS_FILE": str(args_file),
            })
            result = run(
                "/usr/bin/bash",
                str(NOTIFIER),
                "bc-wiki-maintain.service",
                cwd=ROOT,
                env=env,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            args = args_file.read_text(encoding="utf-8")
            self.assertIn("--urgency=critical", args)
            self.assertIn("/tmp/example-vault", args)
            self.assertIn("detector failed: example reason", args)

    def test_notifier_fails_when_notify_send_reports_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            self.write_command(directory, "systemctl", "exit 1\n")
            self.write_command(directory, "journalctl", "exit 1\n")
            self.write_command(directory, "notify-send", "exit 1\n")
            env = os.environ.copy()
            env["PATH"] = f"{directory}{os.pathsep}{env['PATH']}"
            result = run(
                "/usr/bin/bash",
                str(NOTIFIER),
                "bc-wiki-maintain.service",
                cwd=ROOT,
                env=env,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("could not display failure", result.stderr)

    def test_notifier_reads_the_journal_at_the_priority_systemd_actually_uses(self) -> None:
        # systemd logs unit stderr at notice; a -p err..emerg query matches nothing.
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            args_file = directory / "notify-args"
            self.write_command(
                directory,
                "systemctl",
                """
                case "$*" in
                  *SyslogIdentifier*) printf '%s\\n' 'SyslogIdentifier=bc-wiki-maintain' ;;
                  *) printf '%s\\n' 'Environment=VAULT_ROOT=/tmp/example-vault' ;;
                esac
                """,
            )
            self.write_command(
                directory,
                "journalctl",
                """
                for arg in "$@"; do
                  case "$arg" in
                    *err..emerg*|*err..alert*) exit 0 ;;
                  esac
                done
                printf '%s\\n' 'refusing to run: the git worktree is dirty'
                """,
            )
            self.write_command(
                directory,
                "notify-send",
                "printf '%s\\n' \"$@\" > \"$NOTIFY_ARGS_FILE\"\n",
            )
            env = os.environ.copy()
            env.update({
                "PATH": f"{directory}{os.pathsep}{env['PATH']}",
                "NOTIFY_ARGS_FILE": str(args_file),
            })
            result = run(
                "/usr/bin/bash",
                str(NOTIFIER),
                "bc-wiki-maintain.service",
                cwd=ROOT,
                env=env,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            args = args_file.read_text(encoding="utf-8")
            self.assertIn("the git worktree is dirty", args)
            self.assertNotIn("no error output found", args)

    def test_promotion_noop_exits_zero_without_notification(self) -> None:
        temp, repo, vault = make_repo("")
        with temp:
            directory = Path(temp.name) / "bin"
            directory.mkdir()
            marker = Path(temp.name) / "notify-called"
            self.write_command(directory, "notify-send", "printf 'called\\n' > \"$NOTIFY_MARKER\"\n")
            env = runner_env(repo, vault, repo / "missing-pi")
            env.update({
                "PATH": f"{directory}{os.pathsep}{env['PATH']}",
                "NOTIFY_MARKER": str(marker),
            })
            result = run(
                "/usr/bin/bash",
                str(RUNNER),
                cwd=repo,
                env=env,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("PROMOTION_REQUIRED=0", result.stdout)
            self.assertFalse(marker.exists())


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
            body = git(repo, "log", "-1", "--format=%b")
            self.assertIn("Classification: 0 conflict, 1 promote, 1 skip", body)
            self.assertIn("promote ## [2026-08-10] first -> promoted.md: new page", body)
            self.assertIn("skip ## [2026-08-14] last: already on page.md", body)

    def test_purely_additive_append_commits(self) -> None:
        temp, repo, vault = make_repo("## [2026-08-10] first\n")
        with temp:
            classify = self.write_classify(
                json.dumps({"heading": "## [2026-08-10] first", "verdict": "promote", "reason": "append", "page": "page.md"})
            )
            pi = self.write_pi(repo, classify + "printf 'Added evidence\\n' >> \"$VAULT_ROOT/page.md\"\n")
            base = git(repo, "rev-parse", "HEAD")
            result = run("bash", str(RUNNER), cwd=repo, env=runner_env(repo, vault, pi), check=False)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertNotEqual(git(repo, "rev-parse", "HEAD"), base)
            self.assertEqual(git(repo, "status", "--porcelain"), "")
            self.assertIn("Added evidence", (vault / "page.md").read_text(encoding="utf-8"))

    def test_in_place_rewrite_refuses_commit_and_leaves_nothing_staged(self) -> None:
        temp, repo, vault = make_repo("## [2026-08-10] first\n")
        with temp:
            classify = self.write_classify(
                json.dumps({"heading": "## [2026-08-10] first", "verdict": "promote", "reason": "rewrite", "page": "page.md"})
            )
            pi = self.write_pi(repo, classify + "printf '# Rewritten\\n' > \"$VAULT_ROOT/page.md\"\n")
            base = git(repo, "rev-parse", "HEAD")
            result = run("bash", str(RUNNER), cwd=repo, env=runner_env(repo, vault, pi), check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("page.md", result.stderr)
            self.assertIn("deleted lines", result.stderr)
            self.assertEqual(git(repo, "rev-parse", "HEAD"), base)
            self.assertEqual(git(repo, "diff", "--cached", "--name-only"), "")
            self.assertIn("M vault/page.md", git(repo, "status", "--porcelain"))

    def test_new_page_and_additive_append_commit(self) -> None:
        temp, repo, vault = make_repo("## [2026-08-10] first\n")
        with temp:
            classify = self.write_classify(
                json.dumps({"heading": "## [2026-08-10] first", "verdict": "promote", "reason": "new page", "page": "new-page.md"})
            )
            pi = self.write_pi(
                repo,
                classify
                + "printf '# New page\\n' > \"$VAULT_ROOT/new-page.md\"\n"
                + "printf 'Added evidence\\n' >> \"$VAULT_ROOT/page.md\"\n",
            )
            base = git(repo, "rev-parse", "HEAD")
            result = run("bash", str(RUNNER), cwd=repo, env=runner_env(repo, vault, pi), check=False)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertNotEqual(git(repo, "rev-parse", "HEAD"), base)
            self.assertEqual(git(repo, "status", "--porcelain"), "")
            self.assertTrue((vault / "new-page.md").exists())
            self.assertIn("Added evidence", (vault / "page.md").read_text(encoding="utf-8"))

    def test_append_to_file_without_trailing_newline_commits(self) -> None:
        temp, repo, vault = make_repo("## [2026-08-10] first\n")
        with temp:
            (vault / "page.md").write_bytes(b"# Page")
            run("git", "add", str(vault / "page.md"), cwd=repo)
            run("git", "commit", "-qm", "seed page without trailing newline", cwd=repo)
            classify = self.write_classify(
                json.dumps({"heading": "## [2026-08-10] first", "verdict": "promote", "reason": "append", "page": "page.md"})
            )
            pi = self.write_pi(repo, classify + "printf '\\nAdded evidence\\n' >> \"$VAULT_ROOT/page.md\"\n")
            result = run("bash", str(RUNNER), cwd=repo, env=runner_env(repo, vault, pi), check=False)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertEqual(git(repo, "status", "--porcelain"), "")
            self.assertEqual((vault / "page.md").read_bytes(), b"# Page\nAdded evidence\n")

    def test_missing_classification_refuses_commit(self) -> None:
        temp, repo, vault = make_repo("## [2026-08-10] first\n")
        with temp:
            pi = self.write_pi(repo, "printf '# promoted\\n' > \"$VAULT_ROOT/promoted.md\"\n")
            base = git(repo, "rev-parse", "HEAD")
            result = run("bash", str(RUNNER), cwd=repo, env=runner_env(repo, vault, pi), check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("classification does not cover every unpromoted heading", result.stderr)
            self.assertIn("kept classification file for review", result.stderr)
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
            self.assertEqual(result.returncode, 0)
            self.assertEqual(
                result.stdout,
                "Classification: 1 conflict, 0 promote, 1 skip\n\n"
                "skip ## [2026-08-10] first: already represented\n"
                "conflict ## [2026-08-14] last -> open-questions/bar.md: spike vs ADR\n",
            )

    def test_verify_classify_refuses_an_unknown_heading_list(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            vault.mkdir()
            (vault / "log.md").write_text("## [2026-08-10] first\n", encoding="utf-8")
            classify = Path(temp) / "classify.jsonl"
            classify.write_text("", encoding="utf-8")
            result = run("python3", str(LINTER), str(vault), "--verify-classify", str(classify), cwd=ROOT, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("cannot verify classification", result.stderr)

    def test_new_non_markdown_vault_file_refuses_commit(self) -> None:
        temp, repo, vault = make_repo("## [2026-08-10] first\n")
        with temp:
            classify = self.write_classify(
                json.dumps({"heading": "## [2026-08-10] first", "verdict": "promote", "reason": "new page", "page": "promoted.md"})
            )
            pi = self.write_pi(
                repo,
                classify
                + "printf '# promoted\\n' > \"$VAULT_ROOT/promoted.md\"\n"
                + "printf '{}\\n' > \"$VAULT_ROOT/classify.jsonl\"\n",
            )
            base = git(repo, "rev-parse", "HEAD")
            result = run("bash", str(RUNNER), cwd=repo, env=runner_env(repo, vault, pi), check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-Markdown file in the vault", result.stderr)
            self.assertEqual(git(repo, "rev-parse", "HEAD"), base)

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
