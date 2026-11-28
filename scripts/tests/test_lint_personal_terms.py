"""Isolated fixtures for the optional private personal-terms denylist."""

import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from hypothesis import example, given, strategies as st


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("lint_under_test", SCRIPTS / "lint.py")
lint = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lint
spec.loader.exec_module(lint)


class PersonalTermsTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.home = Path(temp.name) / "home"
        self.repo = Path(temp.name) / "repo"
        self.home.mkdir()
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        env = patch.dict(os.environ, {"HOME": str(self.home)})
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop("AGENT_CONCEPTS_PERSONAL_TERMS", None)
        self.config = self.home / ".config/agent-concepts/personal-terms.txt"

    def track(self, name, text):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        subprocess.run(["git", "-C", str(self.repo), "add", name], check=True)

    def deny(self, text, path=None):
        path = path or self.config
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def check(self):
        issues = []
        lint.lint_personal_terms(issues, self.repo)
        return issues

    def test_evidence_skipped_and_body_warned(self):
        self.deny("fakehost\n")
        for name in ("docs/research/raw/a.md", "docs/research/topic/evidence/a.md", "concepts/x/body/a.md", "other.md"):
            self.track(name, "fakehost\n")
        issues = self.check()
        self.assertEqual([(i.severity, i.message.split(":")[0]) for i in issues], [
            ("WARN", "personal term in concepts/x/body/a.md"),
            ("ERROR", "personal term in other.md")])

    def test_non_git_repository_warns(self):
        self.deny("fakehost\n")
        issues = []
        lint.lint_personal_terms(issues, self.home)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "WARN")

    def test_empty_matching_regex_warns_and_other_terms_still_work(self):
        self.deny("re:x*\nfakehost\n")
        self.track("a.md", "fakehost ! !\n")
        issues = self.check()
        self.assertEqual([i.severity for i in issues], ["WARN", "ERROR"])
        self.assertIn("a.md:1", issues[1].message)

    def test_transcripts_skipped_and_mixed_results_warn(self):
        self.deny("fakehost\n")
        self.track("concepts/agent-kernel/tests/pressure-concurrent-sessions/with.txt", "fakehost\n")
        self.track("concepts/agent-kernel/tests/pressure-full-suite-owner.md", "fakehost\n")
        issues = self.check()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "WARN")
        self.assertIn("pressure-full-suite-owner.md", issues[0].message)

    def test_mixed_smoke_result_warns(self):
        self.deny("fakehost\n")
        self.track("concepts/agent-kernel/tests/codex-smoke-2026-06-12.md", "fakehost\n")
        self.assertEqual([i.severity for i in self.check()], ["WARN"])

    def test_absent_denylist_is_skipped(self):
        self.track("a.md", "fakehost is here\n")
        self.assertEqual(self.check(), [])

    @given(st.one_of(st.none(), st.lists(st.sampled_from(("", " \t", "# comment", "  # comment"))).map("\n".join)))
    @example(None)  # /dev/null
    @example("")
    @example("  # comment\n")
    def test_only_required_mode_rejects_a_list_with_no_terms(self, contents):
        if contents is not None:
            self.deny(contents)
        with patch.dict(os.environ, {"AGENT_CONCEPTS_PERSONAL_TERMS": os.devnull if contents is None else str(self.config)}):
            required = []
            lint.lint_personal_terms(required, self.repo, required=True)
            self.assertEqual((self.check(), [(i.severity, "no usable terms" in i.message) for i in required]),
                             ([], [("ERROR", True)]))

    def test_only_required_mode_reports_unreadable_tracked_files(self):
        self.deny("fakehost\n")
        for name in ("a.md", "concepts/x/body/a.md", "docs/research/raw/a.md"):
            self.track(name, "fakehost\n")
            (self.repo / name).unlink()  # Still tracked, but reading fails even as root.
        required = []
        lint.lint_personal_terms(required, self.repo, required=True)
        self.assertEqual((self.check(), [(i.severity, i.message.split(": ")[1]) for i in required]),
                         ([], [("ERROR", "cannot read tracked file a.md"),
                               ("ERROR", "cannot read tracked file concepts/x/body/a.md")]))

    def test_hit_reports_file_line_and_matched_term_only(self):
        self.deny("# comment\nfakehost\nsecretthing\n")
        self.track("log.md", "ok\nran on FakeHost today\n")
        issues = self.check()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "ERROR")
        self.assertIn("log.md:2", issues[0].message)
        self.assertIn("FakeHost", issues[0].message)
        self.assertNotIn("secretthing", issues[0].message)

    def test_word_boundaries(self):
        self.deny("fakehost\n~/Fake\n$HOME/Fake\n")
        self.track("a.md", "fakehostname\nunfakehost\n~/Faker\n")
        self.assertEqual(self.check(), [])
        self.track("b.md", "see ~/Fake/x and $HOME/Fake.\n")
        self.assertEqual(len(self.check()), 2)

    def test_regex_prefix(self):
        self.deny("re:fake-[0-9]+\n")
        self.track("a.md", "fake-42\n")
        self.assertEqual(len(self.check()), 1)

    def test_env_override_path(self):
        other = self.home / "elsewhere.txt"
        self.deny("fakehost\n", other)
        self.track("a.md", "fakehost\n")
        with patch.dict(os.environ, {"AGENT_CONCEPTS_PERSONAL_TERMS": str(other)}):
            self.assertEqual(len(self.check()), 1)

    def test_untracked_and_binary_files_ignored(self):
        self.deny("fakehost\n")
        (self.repo / "untracked.md").write_text("fakehost\n")
        (self.repo / "bin.dat").write_bytes(b"\x00fakehost")
        subprocess.run(["git", "-C", str(self.repo), "add", "bin.dat"], check=True)
        self.assertEqual(self.check(), [])


if __name__ == "__main__":
    unittest.main()
