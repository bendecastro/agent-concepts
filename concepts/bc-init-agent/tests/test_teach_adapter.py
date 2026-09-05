"""Regression checks for the generated teach host adapter and layout."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
SCAFFOLD = ROOT / "concepts/bc-init-agent/body/scaffold.py"
DUE = ROOT / "concepts/teach/body/scripts/due.py"


class TeachAdapterTests(unittest.TestCase):
    def run_scaffold(self, root: Path, archetype: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCAFFOLD),
                "--root",
                str(root),
                "--slug",
                "demo-project",
                "--date",
                "2026-09-05",
                "--archetype",
                archetype,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_learning_scaffold_emits_exact_host_map_and_no_parallel_sessions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.run_scaffold(root, "learning")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            vault = root / ".bc-agent"
            marker = (vault / "references/teach-skill.md").read_text(encoding="utf-8")
            self.assertTrue(marker.startswith("<!-- teach-host-adapter: v1 -->"))
            for path in (
                "learning/plan.md",
                "learning/review.md",
                "learning/notes.md",
                "learning/records/.gitkeep",
                "sources/README.md",
                "concepts/README.md",
                "sessions/README.md",
                "references/teach-resources.md",
            ):
                self.assertTrue((vault / path).is_file(), path)
            for expected in (
                "`learning/plan.md`",
                "`learning/review.md`",
                "`learning/records/`",
                "existing `sessions/` (never `learning/sessions/`)",
                "`learning/notes.md`",
                "existing `sources/`",
                "existing `concepts/`",
                "`references/teach-resources.md`",
                "Glossary section of `project/overview.md`",
                "shared `index.md` and `log.md`",
            ):
                self.assertIn(expected, marker)
            self.assertFalse((vault / "learning/sessions").exists())
            self.assertFalse((root / "MISSION.md").exists())
            self.assertFalse((root / "REVIEW.md").exists())

    def test_hybrid_scaffold_reuses_the_same_adapter_and_shared_session_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.run_scaffold(root, "hybrid")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            vault = root / ".bc-agent"
            marker = (vault / "references/teach-skill.md").read_text(encoding="utf-8")
            self.assertIn("<!-- teach-host-adapter: v1 -->", marker)
            self.assertIn("existing `sessions/` (never `learning/sessions/`)", marker)
            self.assertTrue((vault / "conventions/architecture-runway.md").is_file())
            self.assertTrue((vault / "references/teach-resources.md").is_file())
            self.assertTrue((vault / "concepts/entities/README.md").is_file())
            self.assertTrue((vault / "concepts/syntheses/README.md").is_file())
            self.assertFalse((vault / "learning/sessions").exists())
            self.assertFalse((vault / "raw").exists())
            self.assertFalse((vault / "wiki").exists())

    def test_existing_standalone_state_is_preserved_and_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            standalone = {
                "MISSION.md": "# Existing mission\n",
                "REVIEW.md": "# Existing queue\n",
                "GLOSSARY.md": "# Existing glossary\n",
                "NOTES.md": "# Existing notes\n",
            }
            for name, content in standalone.items():
                (root / name).write_text(content, encoding="utf-8")

            result = self.run_scaffold(root, "learning")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for name, content in standalone.items():
                self.assertEqual((root / name).read_text(encoding="utf-8"), content)
            self.assertIn("standalone teach state exists", result.stdout)
            self.assertIn("competing homes", result.stdout)

    def test_old_marker_is_left_untouched_and_gets_bounded_upgrade_note(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            marker_path = root / ".bc-agent/references/teach-skill.md"
            marker_path.parent.mkdir(parents=True)
            old_marker = "# Teach Skill\n\nUse teach here.\n"
            marker_path.write_text(old_marker, encoding="utf-8")

            result = self.run_scaffold(root, "learning")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(marker_path.read_text(encoding="utf-8"), old_marker)
            self.assertIn("not the explicit v1 teach adapter", result.stdout)

    def test_due_script_uses_the_hosted_review_path_without_behavior_change(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.run_scaffold(root, "learning")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            review = root / ".bc-agent/learning/review.md"
            review.write_text(
                "# Review Queue\n\n"
                "| # | Prompt | Source | Last reviewed | Interval | Due |\n"
                "|---|---|---|---|---|---|\n"
                "| 1 | Explain the host adapter | LR-0001 | 2020-01-01 | 2d | 2020-01-03 |\n",
                encoding="utf-8",
            )
            due = subprocess.run(
                [sys.executable, str(DUE), str(review)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(due.returncode, 0, due.stdout + due.stderr)
            self.assertIn("Explain the host adapter", due.stdout)
            self.assertIn("if recalled:", due.stdout)


if __name__ == "__main__":
    unittest.main()
