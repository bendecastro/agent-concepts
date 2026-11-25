"""Finished and dropped work items are historical records, so their inline paths are not linted."""

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("lint_historical_work_under_test", SCRIPTS / "lint.py")
lint = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lint
spec.loader.exec_module(lint)


class HistoricalWorkInlinePathTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name)
        root = patch.object(lint, "ROOT", self.repo)
        root.start()
        self.addCleanup(root.stop)
        for name in ("work/3-done/2026-08/009-old.md", "work/4-dropped/012-gone.md", "work/1-planned/030-next.md"):
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("See `concepts/renamed/body/SKILL.md`.\n")

    def test_only_open_work_items_report_stale_inline_paths(self):
        issues = []
        lint.lint_inline_paths(issues)
        self.assertEqual(sorted(i.message for i in issues if i.severity == "ERROR"), [
            "broken inline path in work/1-planned/030-next.md: concepts/renamed/body/SKILL.md"])



class HistoricalRecordTests(unittest.TestCase):
    """Dated test results, dated research and finished work keep the paths that were true when written."""

    STALE = "See `concepts/renamed/body/SKILL.md` and [old](../../renamed/tests/scenario.md).\n"

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name)
        root = patch.object(lint, "ROOT", self.repo)
        root.start()
        self.addCleanup(root.stop)
        for name in ("concepts/kept/tests/results-2026-11-24.md",
                     "concepts/kept/tests/results/grade-A.md",
                     "docs/research/2026-08-27-study/01-matrix.md",
                     "work/3-done/2026-11/006-old/plan.md",
                     "concepts/kept/tests/scenario.md"):
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self.STALE)

    def test_only_current_files_report_stale_paths_and_links(self):
        issues = []
        lint.lint_inline_paths(issues)
        lint.lint_links(issues)
        reported = {i.message.rsplit(": ", 1)[0].split(" in ", 1)[1] for i in issues if i.severity == "ERROR"}
        self.assertEqual(reported, {"concepts/kept/tests/scenario.md"})

if __name__ == "__main__":
    unittest.main()
