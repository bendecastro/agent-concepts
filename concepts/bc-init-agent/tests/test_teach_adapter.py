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
TEACH_SKILL = ROOT / "concepts/teach/body/SKILL.md"


def hosted_map(marker: str) -> list[tuple[str, str, str]]:
    """Parse the generated hosted map so extra or altered rows cannot hide."""
    lines = marker.splitlines()
    heading = next(
        index
        for index, line in enumerate(lines)
        if line in {"## Hosted teach path map", "### Hosted path map"}
    )
    header = "| Teach surface | Hosted path | Owner |"
    start = lines.index(header, heading + 1)
    rows: list[tuple[str, str, str]] = []
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append(tuple(cells))
    return rows


EXPECTED_HOST_MAP = [
    ("Mission", "`learning/plan.md` (no hosted `MISSION.md`)", "`teach`"),
    ("Review queue", "`learning/review.md`", "`teach`"),
    ("Learning records", "`learning/records/`", "`teach`"),
    ("Lessons and session artifacts", "existing `sessions/` (never `learning/sessions/`)", "`teach`"),
    ("Notes", "`learning/notes.md`", "`teach`"),
    ("Raw sources", "existing `sources/`", "`teach`"),
    ("Compiled knowledge / wiki concepts", "existing `concepts/`", "`teach`"),
    ("Resource catalog", "`references/teach-resources.md`", "`teach`"),
    ("Glossary", "the existing Glossary section of `project/overview.md`", "`teach`"),
    ("Catalog and history", "shared `index.md` and `log.md`", "`bc-init-agent` host schema; `teach` updates teach entries"),
]


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
            self.assertEqual(hosted_map(marker), EXPECTED_HOST_MAP)
            self.assertIn("When invoked from the project root", marker)
            vault_agents = (vault / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Host search-first is for knowledge and learning-record", vault_agents)
            self.assertIn("teach` owns the mapped pedagogy,", vault_agents)
            self.assertIn("Glossary section", vault_agents)
            self.assertIn("from inside\nthat vault", marker)
            self.assertIn("the user explicitly asks to **consolidate**", marker)
            self.assertIn("all standalone originals intact", marker)
            self.assertLess(
                marker.index("Verify that every destination is complete"),
                marker.index("Only after every mapped\ndestination passes verification may"),
            )
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

    def test_teach_resolution_checks_project_root_from_vault_context(self) -> None:
        teach = TEACH_SKILL.read_text(encoding="utf-8")
        self.assertIn("marker-owning project root", teach)
        self.assertEqual(hosted_map(teach), EXPECTED_HOST_MAP)
        self.assertIn("invoked from `<project>/.bc-agent`", teach)
        self.assertIn("also inspect its marker-owning project root", teach)
        self.assertIn("For hosted knowledge pages and learning records, use the host's canonical", teach)
        self.assertNotIn("Open knowledge pages and learning records only as the index points", teach)
        self.assertIn("Choosing the host for reading or writing is not approval", teach)

    def test_marker_requires_exact_first_line_and_complete_host_map(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            marker_path = root / ".bc-agent/references/teach-skill.md"
            marker_path.parent.mkdir(parents=True)
            marker_path.write_text(
                "<!-- teach-host-adapter: v1 -->\n# Incomplete\n", encoding="utf-8"
            )

            result = self.run_scaffold(root, "learning")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("not the explicit v1 teach adapter", result.stdout)
            self.assertEqual(
                marker_path.read_text(encoding="utf-8"),
                "<!-- teach-host-adapter: v1 -->\n# Incomplete\n",
            )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.run_scaffold(root, "learning")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            marker_path = root / ".bc-agent/references/teach-skill.md"
            marker = marker_path.read_text(encoding="utf-8")
            marker_path.write_text(
                marker.replace("`learning/review.md`", "`learning/wrong-review.md`", 1),
                encoding="utf-8",
            )

            result = self.run_scaffold(root, "learning")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("not the explicit v1 teach adapter", result.stdout)

    def test_hosted_mission_stub_matches_mission_format(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.run_scaffold(root, "learning")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            mission = (root / ".bc-agent/learning/plan.md").read_text(encoding="utf-8")
            for heading in ("## Why", "## Success looks like", "## Constraints", "## Out of scope"):
                self.assertIn(heading, mission)
            for obsolete in ("## Goal", "## Current level", "## Path", "## Review cadence"):
                self.assertNotIn(obsolete, mission)

    def test_questions_stub_keeps_learning_evidence_in_records(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.run_scaffold(root, "learning")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            questions = (root / ".bc-agent/questions/README.md").read_text(encoding="utf-8")
            self.assertNotIn("misconception", questions.lower())
            self.assertIn("all learning evidence belongs in `learning/records/`", questions)

    def test_parent_collision_is_rejected_before_any_scaffold_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            collision = root / ".bc-agent/learning"
            collision.parent.mkdir(parents=True)
            collision.write_text("not a directory\n", encoding="utf-8")

            result = self.run_scaffold(root, "learning")
            self.assertEqual(result.returncode, 1)
            self.assertIn("parent is not a directory", result.stdout)
            self.assertFalse((root / "AGENTS.md").exists())
            self.assertEqual(collision.read_text(encoding="utf-8"), "not a directory\n")

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
