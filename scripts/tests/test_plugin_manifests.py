#!/usr/bin/env python3
"""Fixture tests for the generated Claude Code and Codex plugin manifests."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("plugin_manifests_under_test", SCRIPTS / "plugin_manifests.py")
plugin_manifests = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = plugin_manifests
spec.loader.exec_module(plugin_manifests)


class PluginManifestsTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / "concepts").mkdir()
        (self.root / "package.json").write_text(json.dumps({"version": "1.2.3"}), encoding="utf-8")
        self.listing({"bc-a": [], "bc-b": ["bc-a"]})

    def listing(self, skills: dict[str, list[str]]) -> None:
        (self.root / "concepts" / "public-skills.json").write_text(
            json.dumps({"note": "test", "skills": skills}), encoding="utf-8")

    def read(self, relative: str) -> dict:
        return json.loads((self.root / relative).read_text(encoding="utf-8"))

    def test_both_plugin_manifests_list_every_public_skill_body_and_share_the_version(self):
        plugin_manifests.write_manifests(self.root)
        expected = ["./concepts/bc-a/body", "./concepts/bc-b/body"]
        for path in (plugin_manifests.CLAUDE_PLUGIN, plugin_manifests.CODEX_PLUGIN):
            manifest = self.read(path)
            self.assertEqual(manifest["skills"], expected, path)
            self.assertEqual(manifest["version"], "1.2.3", path)
            self.assertEqual(manifest["name"], plugin_manifests.PLUGIN_NAME, path)

    def test_marketplaces_point_at_the_repository_root_plugin(self):
        plugin_manifests.write_manifests(self.root)
        claude = self.read(plugin_manifests.CLAUDE_MARKETPLACE)
        self.assertEqual([(p["name"], p["source"]) for p in claude["plugins"]], [(plugin_manifests.PLUGIN_NAME, "./")])
        codex = self.read(plugin_manifests.CODEX_MARKETPLACE)
        self.assertEqual([(p["name"], p["source"]) for p in codex["plugins"]],
                         [(plugin_manifests.PLUGIN_NAME, {"source": "local", "path": "./"})])

    def test_check_is_clean_after_write(self):
        plugin_manifests.write_manifests(self.root)
        self.assertEqual(plugin_manifests.check_manifests(self.root), [])

    def test_check_reports_missing_manifests(self):
        errors = plugin_manifests.check_manifests(self.root)
        self.assertEqual(len(errors), 4)
        self.assertTrue(all("--write-plugin-manifests" in error for error in errors))

    def test_check_reports_a_manifest_stale_after_the_public_list_changes(self):
        plugin_manifests.write_manifests(self.root)
        self.listing({"bc-a": [], "bc-b": ["bc-a"], "bc-c": []})
        errors = plugin_manifests.check_manifests(self.root)
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("stale" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
