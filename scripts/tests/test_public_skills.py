#!/usr/bin/env python3
"""Fixture tests for the generated public skill list and its load-reference check."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("public_skills_under_test", SCRIPTS / "public_skills.py")
public_skills = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = public_skills
spec.loader.exec_module(public_skills)


class PublicSkillsTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.edges: list[dict] = []

    def concept(self, name: str, body: str = "Body.\n", *, deployed: str = "yes", skill: bool = True) -> None:
        cdir = self.root / "concepts" / name
        (cdir / "body").mkdir(parents=True)
        (cdir / "CONCEPT.md").write_text(f"---\ndeployed: {deployed}\n---\n# {name}\n", encoding="utf-8")
        (cdir / "body" / ("SKILL.md" if skill else "KERNEL.md")).write_text(body, encoding="utf-8")

    def loads(self, owner: str, target: str) -> None:
        self.edges.append({"from": owner, "to": target, "relation": "loads", "required": True,
                           "source": f"concepts/{owner}/body/SKILL.md", "reason": "test"})

    def write_graph(self) -> None:
        (self.root / "concepts" / "relationships.json").write_text(
            json.dumps({"schema": 1, "edges": self.edges}), encoding="utf-8")

    def test_public_skill_without_bc_prefix_is_reported(self):
        self.concept("bc-alpha")
        self.concept("beta")
        self.concept("hidden", deployed="no")
        self.concept("kernel", skill=False)

        errors = public_skills.unprefixed_names(self.root)

        self.assertEqual(len(errors), 1)
        self.assertIn("`beta`", errors[0])

    def test_list_excludes_kernels_and_undeployed_and_keeps_public_needs(self):
        self.concept("alpha", "load `beta`\n")
        self.concept("beta")
        self.concept("hidden", deployed="no")
        self.concept("kernel", skill=False)
        self.loads("alpha", "beta")
        self.loads("alpha", "hidden")
        self.loads("kernel", "alpha")
        self.write_graph()

        listing = public_skills.public_skill_list(self.root)

        self.assertEqual(listing, {"alpha": ["beta"], "beta": []})

    def test_body_loading_an_unlisted_public_skill_is_reported(self):
        self.concept("alpha", "When docs change, load `beta` first.\n")
        self.concept("beta")
        self.write_graph()

        errors = public_skills.unlisted_load_references(self.root)

        self.assertEqual(len(errors), 1)
        self.assertIn("alpha", errors[0])
        self.assertIn("beta", errors[0])

    def test_listed_negated_self_and_private_references_pass(self):
        self.concept("alpha", "Load the `beta` skill. Do not load `gamma`. invoke `alpha`. load `hidden`.\n")
        self.concept("beta")
        self.concept("gamma")
        self.concept("hidden", deployed="no")
        self.loads("alpha", "beta")
        self.write_graph()

        self.assertEqual(public_skills.unlisted_load_references(self.root), [])

    def test_committed_list_staleness(self):
        self.concept("alpha")
        self.write_graph()
        self.assertEqual(len(public_skills.check_list(self.root)), 1)
        public_skills.write_list(self.root)
        self.assertEqual(public_skills.check_list(self.root), [])


if __name__ == "__main__":
    unittest.main()
