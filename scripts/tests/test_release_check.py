#!/usr/bin/env python3
"""Tests for the release version check: every description carries the version from package.json."""

from __future__ import annotations

import json
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

from hypothesis import given, strategies as st

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

    def test_readme_npm_dist_tag_is_not_a_version_pin(self):
        (self.root / "README.md").write_text(
            "# Readme\n\n## Install\n\npi install npm:agent-concepts\n"
            "pi install npm:agent-concepts@next\npi install npm:agent-concepts@1.2.3\nclaude o/r#v1.2.3\n",
            encoding="utf-8")
        self.assertEqual(release_check.version_problems(self.root, "v1.2.3"), [])

    def test_main_exits_nonzero_on_mismatch(self):
        self.assertEqual(release_check.main(["v1.2.3"], self.root), 0)
        self.assertEqual(release_check.main(["v9.9.9"], self.root), 1)

    def test_missing_previous_skill_requires_alias_or_removed_entry(self):
        previous = {"bc-old", "bc-a"}
        current = {"bc-new", "bc-a"}
        self.assertEqual(release_check.removed_skill_problems(previous, current, ""),
                         ["skill `bc-old` disappeared without an alias or CHANGELOG Removed entry"])
        self.assertEqual(release_check.removed_skill_problems(previous, current | {"bc-old"}, ""), [])
        self.assertEqual(release_check.removed_skill_problems(
            previous, current, "## [Unreleased]\n### Removed\n- `bc-old`: removed.\n"), [])

    @given(st.sets(st.from_regex(r"bc-[a-z]{1,8}", fullmatch=True), max_size=12),
           st.sets(st.from_regex(r"bc-[a-z]{1,8}", fullmatch=True), max_size=12))
    def test_unannounced_disappearances_are_exactly_previous_minus_current(self, previous, current):
        problems = release_check.removed_skill_problems(previous, current, "")
        self.assertEqual(set(problems), {
            f"skill `{name}` disappeared without an alias or CHANGELOG Removed entry"
            for name in previous - current
        })

    def test_previous_tag_comparison_uses_current_release_removed_section(self):
        def git(*args):
            return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True, text=True)
        git("init", "-q")
        git("config", "user.email", "test@example.invalid")
        git("config", "user.name", "Test")
        self.write_json("concepts/public-skills.json", {"skills": {"bc-old": []}})
        git("add", "concepts/public-skills.json")
        git("commit", "-qm", "previous release")
        git("tag", "v1.2.2")
        self.write_json("concepts/public-skills.json", {"skills": {"bc-new": []}})
        self.assertIn("bc-old", release_check.previous_release_problems(self.root, "v1.2.3")[0])
        (self.root / "CHANGELOG.md").write_text(
            "## [1.2.3] - 2026-11-25\n### Removed\n- `bc-old`: removed.\n")
        self.assertEqual(release_check.previous_release_problems(self.root, "v1.2.3"), [])
        self.write_json("concepts/public-skills.json", {"skills": {"bc-old": ["bc-new"], "bc-new": []}})
        (self.root / "CHANGELOG.md").write_text("## [1.2.3] - 2026-11-25\n")
        self.assertEqual(release_check.previous_release_problems(self.root, "v1.2.3"), [])

    def test_repository_versions_agree(self):
        self.assertEqual(release_check.version_problems(release_check.ROOT), [])


if __name__ == "__main__":
    unittest.main()
