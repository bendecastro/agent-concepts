"""Files git ignores are local clutter, so lint must not scan them."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("lint_ignored_under_test", SCRIPTS / "lint.py")
lint = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lint
spec.loader.exec_module(lint)


class IgnoredFilesTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name)
        root = patch.object(lint, "ROOT", self.repo)
        root.start()
        self.addCleanup(root.stop)
        (self.repo / ".gitignore").write_text(".handoffs/\n")
        for name in (".handoffs/note.md", "kept.md"):
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("See `scripts/missing.py` and [x](missing.md).\n")

    def errors(self):
        issues = []
        lint.lint_links(issues)
        lint.lint_inline_paths(issues)
        return sorted(i.message for i in issues if i.severity == "ERROR")

    def test_ignored_markdown_is_not_scanned(self):
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.assertEqual(self.errors(), [
            "broken inline path in kept.md: scripts/missing.py",
            "broken markdown link in kept.md: missing.md"])

    def test_outside_git_every_markdown_file_is_scanned(self):
        self.assertEqual(len(self.errors()), 4)


if __name__ == "__main__":
    unittest.main()
