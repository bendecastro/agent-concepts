#!/usr/bin/env python3
"""Fixture tests for the generated Claude Code and Codex plugin manifests."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from shutil import rmtree


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

    def test_check_is_clean_after_write(self):
        plugin_manifests.write_manifests(self.root)
        self.assertEqual(plugin_manifests.check_manifests(self.root), [])

    def test_check_reports_missing_manifests(self):
        errors = plugin_manifests.check_manifests(self.root)
        self.assertEqual(len(errors), 6)
        self.assertTrue(all("--write-plugin-manifests" in error for error in errors))

    def test_check_reports_a_manifest_stale_after_the_public_list_changes(self):
        plugin_manifests.write_manifests(self.root)
        self.listing({"bc-a": [], "bc-b": ["bc-a"], "bc-c": []})
        errors = plugin_manifests.check_manifests(self.root)
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("stale" in error for error in errors))


def test_marketplaces_point_at_separate_kernel_plugins(tmp_path):
    root = tmp_path / "checkout"
    try:
        (root / "concepts").mkdir(parents=True)
        (root / "concepts/public-skills.json").write_text('{"skills": {"bc-a": []}}', encoding="utf-8")
        (root / "package.json").write_text('{"version": "1.2.3"}', encoding="utf-8")
        plugin_manifests.write_manifests(root)

        for marketplace, expected in (
            (plugin_manifests.CLAUDE_MARKETPLACE, ["./", "./packages/agent-kernel-claude"]),
            (plugin_manifests.CODEX_MARKETPLACE, [
                {"source": "local", "path": "./"},
                {"source": "local", "path": "./packages/agent-kernel-codex"},
            ]),
        ):
            entries = json.loads((root / marketplace).read_bytes())["plugins"]
            assert [(entry["name"], entry["source"]) for entry in entries] == list(zip(
                [plugin_manifests.PLUGIN_NAME, "agent-kernel"], expected, strict=True,
            ))
        for manifest in (
            "packages/agent-kernel-claude/.claude-plugin/plugin.json",
            "packages/agent-kernel-codex/.codex-plugin/plugin.json",
        ):
            kernel = json.loads((root / manifest).read_bytes())
            assert kernel["name"] == "agent-kernel"
            assert kernel["version"] == "1.2.3"
            assert "skills" not in kernel
    finally:
        if root.exists():
            rmtree(root)


if __name__ == "__main__":
    unittest.main()
