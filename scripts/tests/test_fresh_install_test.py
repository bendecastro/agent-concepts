#!/usr/bin/env python3
"""Tests for the fresh-install test's list check (the agent CLIs themselves run only in CI)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import fresh_install_test as fit  # noqa: E402
from install_packs import load_listing  # noqa: E402


class FreshInstallCheckTest(unittest.TestCase):
    def setUp(self):
        self.listing = load_listing(fit.ROOT)

    def test_all_skills_is_the_public_list(self):
        self.assertEqual(fit.expected_skills(self.listing), set(self.listing))

    def test_pack_expects_its_needed_skills(self):
        expected = fit.expected_skills(self.listing, fit.DEFAULT_PACK)
        self.assertIn(fit.HELPER_SKILL, expected)
        self.assertTrue(set(self.listing[fit.DEFAULT_PACK]) <= expected)

    def test_missing_needed_skill_fails_the_check(self):
        expected = fit.expected_skills(self.listing, fit.DEFAULT_PACK)
        installed = expected - {fit.HELPER_SKILL}
        self.assertEqual(fit.list_problems(expected, installed), [f"missing: {fit.HELPER_SKILL}"])
        with self.assertRaises(fit.CheckFailed):
            fit.check_listed("after install", expected, dict.fromkeys(installed, Path()))

    def test_extra_skill_fails_the_check(self):
        self.assertEqual(fit.list_problems({"a"}, {"a", "b"}), ["unexpected: b"])

    def test_pack_command_comes_from_the_guide_and_drops_on_request(self):
        command = fit.pack_command(fit.DEFAULT_PACK)
        self.assertEqual(command[:3], ["skills", "add", str(fit.ROOT)])
        self.assertEqual(set(command[command.index("--skill") + 1:]),
                         fit.expected_skills(self.listing, fit.DEFAULT_PACK))
        dropped = fit.pack_command(fit.DEFAULT_PACK, drop=fit.HELPER_SKILL)
        self.assertNotIn(fit.HELPER_SKILL, dropped)
        self.assertEqual(len(dropped), len(command) - 1)

    def test_helper_exists_in_the_source(self):
        self.assertTrue((fit.ROOT / "concepts" / fit.HELPER_SKILL / "body" / fit.HELPER_RELPATH).is_file())


if __name__ == "__main__":
    unittest.main()
