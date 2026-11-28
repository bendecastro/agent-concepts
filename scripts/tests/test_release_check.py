#!/usr/bin/env python3
"""Tests for the release version check: every description carries the version from package.json."""

from __future__ import annotations

import json
import io
import os
import re
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

from hypothesis import example, given, strategies as st

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import plugin_manifests  # noqa: E402
import release_check  # noqa: E402
import lint  # noqa: E402


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

    def test_release_personal_terms_and_opt_out(self):
        config = self.root / "denylist"
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "README.md"], cwd=self.root, check=True)
        with patch.dict(os.environ, {"AGENT_CONCEPTS_PERSONAL_TERMS": str(config)}):
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(release_check.main(["v1.2.3"], self.root), 1)
            self.assertIn("--no-personal-terms", output.getvalue())
            self.assertEqual(release_check.main(["--no-personal-terms", "v1.2.3"], self.root), 0)
            config.write_text("uniquefixturesecret\n")
            self.assertEqual(release_check.main(["v1.2.3"], self.root), 0)
            with (self.root / "README.md").open("a") as f:
                f.write("uniquefixturesecret\n")
            subprocess.run(["git", "add", "README.md"], cwd=self.root, check=True)
            self.assertEqual(release_check.main(["v1.2.3"], self.root), 1)

    @given(st.booleans(), st.lists(st.sampled_from(("--no-personal-terms", "--unknown")), max_size=4),
           st.booleans())
    @example(tagged=True, options=["--no-personal-terms"], reverse=False)
    def test_only_one_explicit_opt_out_is_accepted(self, tagged, options, reverse):
        args = (["v1.2.3"] if tagged else []) + options
        if reverse:
            args.reverse()
        expected = 1 if not options else 0 if options == ["--no-personal-terms"] else 2
        with patch.dict(os.environ, {"AGENT_CONCEPTS_PERSONAL_TERMS": str(self.root / "missing")}), \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(release_check.main(args, self.root), expected)

    def test_personal_terms_warning_only_hit_does_not_block_release(self):
        config = self.root / "denylist"
        config.write_text("uniquefixturesecret\n")
        body = self.root / "concepts/example/body/SKILL.md"
        body.parent.mkdir(parents=True)
        body.write_text("uniquefixturesecret\n")
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "concepts/example/body/SKILL.md"], cwd=self.root, check=True)
        with patch.dict(os.environ, {"AGENT_CONCEPTS_PERSONAL_TERMS": str(config)}):
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(release_check.main(["v1.2.3"], self.root), 0)
            self.assertIn("uniquefixturesecret", output.getvalue())

    @given(st.lists(st.sampled_from(("warning-hit", "error-hit", "warning-failure", "error-failure")), max_size=8))
    @example(["warning-failure"])
    def test_only_warning_matches_are_nonblocking(self, outcomes):
        scan_results = {
            "warning-hit": lint.Issue("WARN", "personal term in body.md:1: 'fixture'"),
            "error-hit": lint.Issue("ERROR", "personal term in README.md:1: 'fixture'"),
            "warning-failure": lint.Issue("WARN", "personal terms: cannot list tracked files with git"),
            "error-failure": lint.Issue("ERROR", "personal terms: cannot read tracked file a.md"),
        }

        warnings, problems = release_check.classify_scan([scan_results[outcome] for outcome in outcomes])
        self.assertEqual((len(problems), len(warnings)),
                         (sum(outcome != "warning-hit" for outcome in outcomes), outcomes.count("warning-hit")))

    def test_release_fails_when_git_cannot_list_the_snapshot(self):
        config = self.root / "denylist"
        config.write_text("uniquefixturesecret\n")
        output = io.StringIO()  # self.root is not a git repository, so the real scanner's git call fails.
        with patch.dict(os.environ, {"AGENT_CONCEPTS_PERSONAL_TERMS": str(config),
                                     "GIT_CEILING_DIRECTORIES": str(self.root.parent)}), redirect_stdout(output):
            self.assertEqual(release_check.main(["v1.2.3"], self.root), 1)
        self.assertIn("release check: personal terms: cannot list", output.getvalue())

    def test_publish_job_inputs_are_pinned(self):
        text = (release_check.ROOT / ".github/workflows/release.yml").read_text()
        job = text.split("  publish-npm:\n", 1)[1].split("\n  github-release:", 1)[0]
        actions = re.findall(r"^[ \t]*(?:-[ \t]+)?uses:[ \t]*(.*)$", job, re.M)
        self.assertTrue(actions)
        for action in actions:
            self.assertRegex(action, r"^[^@]+@[0-9a-f]{40} # v\d+\.\d+\.\d+$")
        commands = re.sub(r"(?m)^[ \t]*#.*$", "", job)
        installs = re.findall(r"\bnpm\s+install\b", commands)
        exact_installs = re.findall(
            r'''(?m)^[ \t]*(?:-[ \t]+)?run:[ \t]+npm install -g (["']?)npm@11\.\d+\.\d+\1[ \t]*$''', commands)
        self.assertEqual((len(installs), len(exact_installs)), (1, 1),
                         "publish-npm must have exactly one npm install, at an exact npm version")

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
        self.assertEqual(release_check.main(["--no-personal-terms", "v1.2.3"], self.root), 0)
        self.assertEqual(release_check.main(["--no-personal-terms", "v9.9.9"], self.root), 1)

    def test_missing_previous_skill_requires_alias_or_removed_entry(self):
        previous = {"bc-old", "bc-a"}
        current = {"bc-new", "bc-a"}
        self.assertEqual(release_check.removed_skill_problems(previous, current, ""),
                         ["skill `bc-old` disappeared without an alias or CHANGELOG Removed entry"])
        self.assertEqual(release_check.removed_skill_problems(previous, current | {"bc-old"}, ""), [])
        self.assertEqual(release_check.removed_skill_problems(
            previous, current, "## [Unreleased]\n### Removed\n- `bc-old`: removed.\n"), [])

    def test_hidden_removed_entries_do_not_exempt(self):
        previous = {"bc-old", "bc-a"}
        current = {"bc-a"}
        expected = ["skill `bc-old` disappeared without an alias or CHANGELOG Removed entry"]
        for hidden in ("<!--\n- `bc-old`: replaced.\n-->\n",
                       "<!-- - `bc-old`: replaced. -->\n",
                       "```\n- `bc-old`: replaced.\n```\n",
                       "~~~md\n- `bc-old`: replaced.\n~~~\n"):
            with self.subTest(hidden=hidden):
                self.assertEqual(release_check.removed_skill_problems(
                    previous, current, "### Removed\n" + hidden), expected)
        self.assertEqual(release_check.removed_skill_problems(
            previous, current, "### Removed\n<!-- note -->\n- `bc-old`: replaced.\n"), [])

    @given(st.dictionaries(st.from_regex(r"bc-[a-z]{1,8}", fullmatch=True), st.tuples(
        st.booleans(), st.booleans(),
        st.sampled_from(("none", "valid", "mention", "wrong-release", "wrong-heading")),
    ), max_size=12))
    @example({"bc-old": (True, False, "mention")})
    @example({"bc-old": (True, False, "wrong-release")})
    @example({"bc-old": (True, False, "wrong-heading")})
    @example({"bc-old": (True, False, "valid")})
    def test_only_current_release_removed_entries_exempt_disappearances(self, skills):
        previous = {name: [] for name, (old, _, _) in skills.items() if old}
        current = {name: [] for name, (_, new, _) in skills.items() if new}
        entries = {kind: "" for kind in ("valid", "mention", "wrong-release", "wrong-heading")}
        for name, (_, _, kind) in skills.items():
            if kind != "none":
                entries[kind] += (f"- Removed screenshots; see `{name}` for context.\n" if kind == "mention"
                                  else f"- `{name}`: replaced.\n")
        self.tag_previous_release(previous)
        self.write_json("concepts/public-skills.json", {"skills": current})
        (self.root / "CHANGELOG.md").write_text(
            "## [1.2.3] - 2026-11-25\n### Removed\n" + entries["valid"] + entries["mention"]
            + "### Changed\n" + entries["wrong-heading"]
            + "## [1.2.2] - 2026-11-24\n### Removed\n" + entries["wrong-release"])
        self.assertEqual(set(release_check.previous_release_problems(self.root, "v1.2.3")), {
            f"skill `{name}` disappeared without an alias or CHANGELOG Removed entry"
            for name in previous.keys() - current.keys() if skills[name][2] != "valid"
        })

    def tag_previous_release(self, skills):
        def git(*args):
            return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True, text=True)
        git("init", "-q")
        git("config", "user.email", "test@example.invalid")
        git("config", "user.name", "Test")
        self.write_json("concepts/public-skills.json", {"skills": skills})
        git("add", "concepts/public-skills.json")
        git("commit", "--allow-empty", "-qm", "previous release")
        git("tag", "-f", "v1.2.2")

    def test_previous_tag_comparison_uses_current_release_removed_section(self):
        self.tag_previous_release({"bc-old": []})
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
