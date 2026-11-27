#!/usr/bin/env python3
"""Tests for the release version check: every description carries the version from package.json."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import plugin_manifests  # noqa: E402
import release_check  # noqa: E402


class ReleaseCheckTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / "concepts").mkdir()
        (self.root / "concepts" / "public-skills.json").write_text(
            json.dumps({"skills": {"bc-a": []}}), encoding="utf-8")
        self.write_json("package.json", {"name": "agent-concepts", "version": "1.2.3"})
        plugin_manifests.write_manifests(self.root)
        (self.root / "CHANGELOG.md").write_text("# Changelog\n\n## [1.2.3] - 2026-11-25\n", encoding="utf-8")
        (self.root / "README.md").write_text(
            "# Readme\n\n## Install\n\npi install npm:agent-concepts\n"
            "pi install npm:agent-concepts@1.2.3\nclaude o/r#v1.2.3\n\n## Next\n\nv0.0.1\n",
            encoding="utf-8")

    def write_json(self, relative: str, document: dict) -> None:
        (self.root / relative).write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")

    def test_generated_manifests_carry_the_package_version(self):
        self.assertEqual(set(release_check.declared_versions(self.root).values()), {"1.2.3"})
        self.assertEqual(release_check.version_problems(self.root), [])

    def test_hand_edited_plugin_version_is_a_mismatch(self):
        manifest = json.loads((self.root / plugin_manifests.CODEX_PLUGIN).read_text(encoding="utf-8"))
        manifest["version"] = "1.2.4"
        self.write_json(plugin_manifests.CODEX_PLUGIN, manifest)
        problems = release_check.version_problems(self.root)
        self.assertEqual(len(problems), 1)
        self.assertIn(plugin_manifests.CODEX_PLUGIN, problems[0])

    def test_tag_must_match_the_version(self):
        self.assertEqual(release_check.version_problems(self.root, "v1.2.3"), [])
        problems = release_check.version_problems(self.root, "v1.2.4")
        self.assertTrue(problems)
        self.assertIn("v1.2.4", problems[0])

    def test_tag_must_have_a_changelog_entry(self):
        (self.root / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
        self.assertEqual(release_check.version_problems(self.root), [])
        problems = release_check.version_problems(self.root, "v1.2.3")
        self.assertEqual(len(problems), 1)
        self.assertIn("CHANGELOG.md", problems[0])

    def test_tag_must_look_like_vmajor_minor_patch(self):
        problems = release_check.version_problems(self.root, "1.2.3")
        self.assertIn("vMAJOR.MINOR.PATCH", problems[0])

    def test_readme_install_must_name_the_tag(self):
        (self.root / "README.md").write_text(
            "# Readme\n\n## Install\n\npi install npm:agent-concepts\nclaude o/r#v1.2.2\n", encoding="utf-8")
        self.assertEqual(release_check.version_problems(self.root), [])
        problems = release_check.version_problems(self.root, "v1.2.3")
        self.assertEqual(len(problems), 2)
        self.assertIn("README.md", problems[0])
        self.assertIn("v1.2.2", problems[1])

    def test_readme_pi_install_must_be_the_unpinned_npm_package(self):
        (self.root / "README.md").write_text(
            "# Readme\n\n## Install\n\npi install git:github.com/o/r@v1.2.3\n", encoding="utf-8")
        problems = release_check.version_problems(self.root, "v1.2.3")
        self.assertEqual(problems, ["README.md section `## Install` does not show `pi install npm:agent-concepts`"])

    def test_readme_npm_pin_example_must_name_the_version(self):
        (self.root / "README.md").write_text(
            "# Readme\n\n## Install\n\npi install npm:agent-concepts\n"
            "pi install npm:agent-concepts@1.2.2\nclaude o/r#v1.2.3\n", encoding="utf-8")
        problems = release_check.version_problems(self.root, "v1.2.3")
        self.assertEqual(problems, ["README.md section `## Install` pins npm:agent-concepts@1.2.2, not 1.2.3"])

    def test_main_exits_nonzero_on_mismatch(self):
        self.assertEqual(release_check.main(["v1.2.3"], self.root), 0)
        self.assertEqual(release_check.main(["v9.9.9"], self.root), 1)

    def test_repository_versions_agree(self):
        self.assertEqual(release_check.version_problems(release_check.ROOT), [])


if __name__ == "__main__":
    unittest.main()
