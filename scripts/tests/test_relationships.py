#!/usr/bin/env python3
"""Fixture tests for the bilateral relationship graph."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = REPO_ROOT / "scripts" / "relationships.py"


def load_module():
    spec = importlib.util.spec_from_file_location("relationships_under_test", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


relationships = load_module()


class RelationshipFixtures(unittest.TestCase):
    def workspace(
        self,
        names: tuple[str, ...] = ("source", "target"),
        source_files: dict[str, str] | None = None,
    ):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        source_files = source_files or {}
        for name in names:
            concept = root / "concepts" / name
            (concept / "body").mkdir(parents=True)
            (concept / "CONCEPT.md").write_text(f"# {name}\n", encoding="utf-8")
            body = source_files.get(name, f"This file mentions target and {name}.\n")
            (concept / "body" / "SKILL.md").write_text(body, encoding="utf-8")
        (root / "concepts" / "relationships.json").write_text(
            json.dumps({"schema": 1, "edges": []}), encoding="utf-8"
        )
        self.addCleanup(temp.cleanup)
        return root

    def write_graph(self, root: Path, graph: dict[str, Any]) -> None:
        (root / "concepts" / "relationships.json").write_text(
            json.dumps(graph), encoding="utf-8"
        )

    def edge(self, **overrides: Any) -> dict[str, Any]:
        edge = {
            "from": "source",
            "to": "target",
            "relation": "loads",
            "required": True,
            "source": "concepts/source/body/SKILL.md",
            "reason": "The source uses the target contract.",
        }
        edge.update(overrides)
        return edge

    def errors(self, root: Path) -> list[str]:
        edges, load_errors = relationships.load_graph(root)
        return load_errors + relationships.validate_graph(root, edges)

    def test_valid_unconditional_edge(self) -> None:
        root = self.workspace()
        self.write_graph(root, {"schema": 1, "edges": [self.edge()]})

        edges, load_errors = relationships.load_graph(root)

        self.assertEqual(load_errors, [])
        self.assertEqual(relationships.validate_graph(root, edges), [])
        self.assertEqual(edges[0].when, None)
        self.assertEqual(edges[0].owner, "source")
        self.assertEqual(edges[0].target, "target")

    def test_valid_optional_edge(self) -> None:
        root = self.workspace()
        self.write_graph(root, {"schema": 1, "edges": [self.edge(required=False)]})

        edges, load_errors = relationships.load_graph(root)

        self.assertEqual(load_errors, [])
        self.assertEqual(relationships.validate_graph(root, edges), [])
        self.assertFalse(edges[0].required)

    def test_valid_conditional_concrete_drain_to_tdd_edge(self) -> None:
        root = self.workspace(
            names=("bc-drain-issues", "tdd"),
            source_files={
                "bc-drain-issues": (
                    "## Build loop\n"
                    "For feature/enhancement work, load and follow the tdd discipline.\n"
                )
            },
        )
        self.write_graph(
            root,
            {
                "schema": 1,
                "edges": [
                    {
                        "from": "bc-drain-issues",
                        "to": "tdd",
                        "relation": "loads",
                        "required": True,
                        "when": "feature/enhancement work",
                        "source": "concepts/bc-drain-issues/body/SKILL.md#build-loop",
                        "reason": "Feature workers follow red-green-refactor.",
                    }
                ],
            },
        )

        edges, load_errors = relationships.load_graph(root)

        self.assertEqual(load_errors, [])
        self.assertEqual(relationships.validate_graph(root, edges), [])

    def test_each_relation_value_is_valid(self) -> None:
        for relation in relationships.RELATIONS:
            with self.subTest(relation=relation):
                root = self.workspace()
                self.write_graph(
                    root,
                    {"schema": 1, "edges": [self.edge(relation=relation)]},
                )
                self.assertEqual(self.errors(root), [])

    def test_unknown_top_level_key_is_rejected(self) -> None:
        root = self.workspace()
        self.write_graph(root, {"schema": 1, "edges": [], "extra": True})
        _, load_errors = relationships.load_graph(root)
        self.assertTrue(any("unknown top-level key" in error for error in load_errors))

    def test_unsupported_schema_is_rejected(self) -> None:
        root = self.workspace()
        self.write_graph(root, {"schema": 2, "edges": []})
        _, load_errors = relationships.load_graph(root)
        self.assertTrue(any("schema" in error for error in load_errors))

    def test_missing_edges_is_rejected(self) -> None:
        root = self.workspace()
        self.write_graph(root, {"schema": 1})
        _, load_errors = relationships.load_graph(root)
        self.assertTrue(any("edges" in error for error in load_errors))

    def test_unknown_edge_key_is_rejected(self) -> None:
        root = self.workspace()
        self.write_graph(root, {"schema": 1, "edges": [self.edge(extra=True)]})
        _, load_errors = relationships.load_graph(root)
        self.assertTrue(any("unknown edge key" in error for error in load_errors))

    def test_unknown_concept_names_are_rejected(self) -> None:
        root = self.workspace()
        self.write_graph(root, {"schema": 1, "edges": [self.edge(to="missing")]})
        errors = self.errors(root)
        self.assertTrue(any("missing" in error and "concept" in error for error in errors))

    def test_deployment_aliases_are_rejected_as_noncanonical_names(self) -> None:
        for alias in ("implement", "to-issues", "to-prd"):
            with self.subTest(alias=alias):
                root = self.workspace()
                # ``from`` is a reserved keyword in Python, so construct this one directly.
                self.write_graph(
                    root,
                    {
                        "schema": 1,
                        "edges": [
                            {
                                **self.edge(),
                                "from": alias,
                            }
                        ],
                    },
                )
                errors = self.errors(root)
                self.assertTrue(any(alias in error and "canonical" in error for error in errors))

    def test_absolute_and_parent_sources_are_rejected(self) -> None:
        for source in ("/tmp/source.md", "../source.md"):
            with self.subTest(source=source):
                root = self.workspace()
                self.write_graph(root, {"schema": 1, "edges": [self.edge(source=source)]})
                errors = self.errors(root)
                self.assertTrue(any("repository-relative" in error for error in errors))

    def test_source_outside_owner_concept_is_rejected(self) -> None:
        root = self.workspace(names=("source", "target", "other"))
        self.write_graph(
            root,
            {
                "schema": 1,
                "edges": [self.edge(source="concepts/other/body/SKILL.md")],
            },
        )
        errors = self.errors(root)
        self.assertTrue(any("from concept" in error for error in errors))

    def test_source_must_mention_target(self) -> None:
        root = self.workspace(
            source_files={"source": "This source mentions another concept only.\n"}
        )
        self.write_graph(root, {"schema": 1, "edges": [self.edge()]})
        errors = self.errors(root)
        self.assertTrue(any("does not mention target" in error for error in errors))

    def test_target_mention_is_bounded_not_a_prefix(self) -> None:
        root = self.workspace(source_files={"source": "The tdd-lite variant is unrelated.\n"})
        self.write_graph(
            root,
            {
                "schema": 1,
                "edges": [self.edge(to="tdd", source="concepts/source/body/SKILL.md")],
            },
        )
        # Add the canonical target while retaining only the tdd-lite mention in the source.
        target = root / "concepts" / "tdd"
        target.mkdir(parents=True)
        (target / "CONCEPT.md").write_text("# tdd\n", encoding="utf-8")
        (target / "body").mkdir()
        (target / "body" / "SKILL.md").write_text("# tdd\n", encoding="utf-8")
        errors = self.errors(root)
        self.assertTrue(any("does not mention target `tdd`" in error for error in errors))

    def test_anchor_matching_zero_headings_is_rejected(self) -> None:
        root = self.workspace(source_files={"source": "target appears here.\n"})
        self.write_graph(
            root,
            {"schema": 1, "edges": [self.edge(source="concepts/source/body/SKILL.md#missing")]},
        )
        errors = self.errors(root)
        self.assertTrue(any("matches no heading" in error for error in errors))

    def test_anchor_matching_two_headings_is_rejected(self) -> None:
        root = self.workspace(
            source_files={"source": "## Target\ntarget\n### Target\ntarget\n"}
        )
        self.write_graph(
            root,
            {"schema": 1, "edges": [self.edge(source="concepts/source/body/SKILL.md#target")]},
        )
        errors = self.errors(root)
        self.assertTrue(any("matches 2 headings" in error for error in errors))

    def test_self_edge_is_rejected(self) -> None:
        root = self.workspace()
        self.write_graph(
            root,
            {"schema": 1, "edges": [self.edge(to="source", source="concepts/source/body/SKILL.md")]},
        )
        errors = self.errors(root)
        self.assertTrue(any("self-edge" in error for error in errors))

    def test_duplicate_edge_identity_treats_omitted_and_null_when_as_equal(self) -> None:
        root = self.workspace()
        first = self.edge()
        second = self.edge(when=None)
        self.write_graph(root, {"schema": 1, "edges": [first, second]})
        errors = self.errors(root)
        self.assertTrue(any("duplicate" in error for error in errors))

    def test_blank_when_is_rejected(self) -> None:
        root = self.workspace()
        self.write_graph(root, {"schema": 1, "edges": [self.edge(when=" ")]})
        errors = self.errors(root)
        self.assertTrue(any("when" in error and "blank" in error for error in errors))

    def test_invalid_relation_is_rejected(self) -> None:
        root = self.workspace()
        self.write_graph(root, {"schema": 1, "edges": [self.edge(relation="requires")]})
        errors = self.errors(root)
        self.assertTrue(any("relation" in error for error in errors))

    def test_required_must_be_boolean(self) -> None:
        root = self.workspace()
        self.write_graph(root, {"schema": 1, "edges": [self.edge(required="yes")]})
        errors = self.errors(root)
        self.assertTrue(any("required" in error and "boolean" in error for error in errors))

    def test_reason_must_not_be_empty(self) -> None:
        root = self.workspace()
        self.write_graph(root, {"schema": 1, "edges": [self.edge(reason=" ")]})
        errors = self.errors(root)
        self.assertTrue(any("reason" in error and "empty" in error for error in errors))

    def test_required_load_cycle_is_rejected_with_full_path(self) -> None:
        root = self.workspace(names=("a", "b"), source_files={
            "a": "b\n",
            "b": "a\n",
        })
        self.write_graph(
            root,
            {
                "schema": 1,
                "edges": [
                    {
                        "from": "a",
                        "to": "b",
                        "relation": "loads",
                        "required": True,
                        "source": "concepts/a/body/SKILL.md",
                        "reason": "a loads b.",
                    },
                    {
                        "from": "b",
                        "to": "a",
                        "relation": "loads",
                        "required": True,
                        "source": "concepts/b/body/SKILL.md",
                        "reason": "b loads a.",
                    },
                ],
            },
        )
        errors = self.errors(root)
        self.assertTrue(any("a -> b -> a" in error for error in errors))

    def test_non_load_cycles_are_accepted(self) -> None:
        root = self.workspace(source_files={"target": "source\n"})
        self.write_graph(
            root,
            {
                "schema": 1,
                "edges": [
                    self.edge(relation="adapts", reason="source adapts target."),
                    {
                        **self.edge(),
                        "from": "target",
                        "to": "source",
                        "relation": "hands_off",
                        "source": "concepts/target/body/SKILL.md",
                        "reason": "target hands off to source.",
                    },
                ],
            },
        )
        self.assertEqual(self.errors(root), [])


if __name__ == "__main__":
    unittest.main()
