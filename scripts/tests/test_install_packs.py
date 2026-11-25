#!/usr/bin/env python3
"""Tests for the generated `npx skills` install commands (all skills and ready-made packs)."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

from hypothesis import given, strategies as st


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("install_packs_under_test", SCRIPTS / "install_packs.py")
install_packs = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = install_packs
spec.loader.exec_module(install_packs)


def write_listing(root: Path, skills: dict[str, list[str]]) -> None:
    path = root / "concepts" / "public-skills.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"note": "test", "skills": skills}), encoding="utf-8")


class InstallPacksTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)

    def test_pack_holds_the_transitive_closure_of_needs(self):
        listing = {"bc-a": ["bc-b"], "bc-b": ["bc-c"], "bc-c": [], "bc-d": []}

        self.assertEqual(install_packs.packs(listing), {"bc-a": ["bc-a", "bc-b", "bc-c"], "bc-b": ["bc-b", "bc-c"]})

    def test_command_names_every_skill_explicitly(self):
        command = install_packs.add_command(["bc-a", "bc-b"], source="./checkout", agent="pi")

        self.assertEqual(command, "npx skills add ./checkout -g -a pi -y --skill bc-a bc-b")

    def test_document_lists_all_skills_and_each_pack(self):
        write_listing(self.root, {"bc-a": ["bc-b"], "bc-b": [], "bc-c": []})

        text = install_packs.render_doc(self.root)

        self.assertIn("--skill bc-a bc-b bc-c\n", text)
        self.assertIn("### bc-a\n", text)
        self.assertIn("--skill bc-a bc-b\n", text)
        self.assertNotIn("### bc-b\n", text)

    def test_check_reports_missing_and_stale_document(self):
        write_listing(self.root, {"bc-a": []})
        self.assertEqual(len(install_packs.check_doc(self.root)), 1)

        install_packs.write_doc(self.root)
        self.assertEqual(install_packs.check_doc(self.root), [])

        write_listing(self.root, {"bc-a": [], "bc-b": []})
        self.assertIn("stale", install_packs.check_doc(self.root)[0])


names = st.sampled_from([f"bc-{n}" for n in "abcdefgh"])


@given(st.dictionaries(names, st.lists(names, max_size=4, unique=True), min_size=1))
def test_every_pack_contains_its_skill_and_is_closed_under_needs(raw):
    listing = {name: sorted(n for n in needs if n in raw and n != name) for name, needs in raw.items()}

    for name, members in install_packs.packs(listing).items():
        assert members[0] == name
        assert len(set(members)) == len(members)
        for member in members:
            assert set(listing[member]) <= set(members)


if __name__ == "__main__":
    unittest.main()
