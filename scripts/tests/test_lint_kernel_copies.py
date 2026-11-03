"""Isolated fixtures for machine-local copied kernel-delta warnings."""

import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("lint_under_test", SCRIPTS / "lint.py")
lint = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lint
spec.loader.exec_module(lint)


class KernelCopiesTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.home = Path(temp.name)
        home = patch.dict(os.environ, {"HOME": str(self.home)})
        home.start()
        self.addCleanup(home.stop)
        self.config = self.home / ".config/agent-concepts/kernel-copies.json"

    def configure(self):
        self.config.parent.mkdir(parents=True)
        self.config.write_text(json.dumps({"copies": [{
            "name": "fixture", "source": "~/source", "runtime": "~/runtime"
        }]}))
        (self.home / "source").write_bytes(b"kernel\r\n")
        (self.home / "runtime").write_bytes(b"kernel\r\n")

    def check(self):
        issues = []
        lint.lint_kernel_copies(issues)
        self.assertTrue(all(issue.severity == "WARN" for issue in issues))
        return issues

    def test_absent_config(self):
        self.assertEqual(self.check(), [])

    def test_identical(self):
        self.configure()
        self.assertEqual(self.check(), [])

    def test_differing_bytes(self):
        self.configure()
        (self.home / "runtime").write_bytes(b"kernel\n")
        issues = self.check()
        self.assertEqual(len(issues), 1)
        for text in ("~/source", "~/runtime", "re-copy source to runtime", "bc-setup-config-symlinks"):
            self.assertIn(text, issues[0].message)
        self.assertNotIn(str(self.home), issues[0].message)

    def test_missing_runtime(self):
        self.configure()
        (self.home / "runtime").unlink()
        self.assertIn("missing or unreadable", self.check()[0].message)

    def test_missing_source(self):
        self.configure()
        (self.home / "source").unlink()
        self.assertIn("missing or unreadable", self.check()[0].message)

    def test_malformed_json(self):
        self.configure()
        self.config.write_text("{broken")
        self.assertIn("cannot read ~/.config/agent-concepts/kernel-copies.json", self.check()[0].message)

    def test_invalid_shape(self):
        self.configure()
        for data in ([], {"copies": {}}, {"copies": [None]}, {"copies": [{"name": "x"}]}):
            with self.subTest(data=data):
                self.config.write_text(json.dumps(data))
                self.assertEqual(len(self.check()), 1)


if __name__ == "__main__":
    unittest.main()
