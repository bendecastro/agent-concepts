#!/usr/bin/env python3
"""Fixture tests for the Pi package manifest generated from the public skill list."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("pi_package_under_test", SCRIPTS / "pi_package.py")
pi_package = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = pi_package
spec.loader.exec_module(pi_package)


class PiPackageTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / "concepts").mkdir()
        self.write_list(["bc-a", "bc-b"])

    def write_list(self, names: list[str]) -> None:
        document = {"note": "x", "skills": {name: [] for name in names}}
        (self.root / "concepts" / "public-skills.json").write_text(json.dumps(document), encoding="utf-8")

    def manifest(self) -> dict:
        return json.loads((self.root / "package.json").read_text(encoding="utf-8"))

    def test_write_points_pi_skills_at_each_public_body(self):
        pi_package.write_manifest(self.root)
        self.assertEqual(self.manifest()["pi"]["skills"], ["./concepts/bc-a/body", "./concepts/bc-b/body"])
        self.assertIn("pi-package", self.manifest()["keywords"])
        self.assertEqual(pi_package.check_manifest(self.root), [])

    def test_write_ships_only_the_skill_bodies_and_kernel_extension(self):
        pi_package.write_manifest(self.root)
        manifest = self.manifest()
        self.assertEqual(manifest["files"], ["concepts/bc-a/body/", "concepts/bc-b/body/",
                                             "packages/agent-kernel-pi/"])
        self.assertNotIn("private", manifest)

    def test_check_fails_when_files_drift_from_the_skill_list(self):
        pi_package.write_manifest(self.root)
        manifest = self.manifest()
        manifest["files"] = ["concepts/"]
        (self.root / "package.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.assertEqual(len(pi_package.check_manifest(self.root)), 1)

    def test_write_keeps_other_fields(self):
        (self.root / "package.json").write_text(json.dumps({"name": "x", "version": "1.2.3"}), encoding="utf-8")
        pi_package.write_manifest(self.root)
        self.assertEqual(self.manifest()["version"], "1.2.3")
        self.assertEqual(self.manifest()["name"], "x")

    def test_check_fails_when_list_gains_a_skill(self):
        pi_package.write_manifest(self.root)
        self.write_list(["bc-a", "bc-b", "bc-c"])
        self.assertEqual(len(pi_package.check_manifest(self.root)), 1)

    def test_check_fails_when_manifest_missing(self):
        self.assertEqual(len(pi_package.check_manifest(self.root)), 1)


if __name__ == "__main__":
    unittest.main()
