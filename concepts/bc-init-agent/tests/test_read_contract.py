"""Deterministic checks for the generated vault read contract."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
SCAFFOLD_PATH = ROOT / "concepts/bc-init-agent/body/scaffold.py"
SKILL_PATH = ROOT / "concepts/bc-wiki-maintain/body/SKILL.md"
SPEC = importlib.util.spec_from_file_location("bc_init_scaffold", SCAFFOLD_PATH)
assert SPEC and SPEC.loader
SCAFFOLD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SCAFFOLD
SPEC.loader.exec_module(SCAFFOLD)

BEGIN = "<!-- BEGIN canonical vault read path -->"
END = "<!-- END canonical vault read path -->"


def canonical_block_from_skill() -> str:
    text = SKILL_PATH.read_text(encoding="utf-8")
    start = text.index(BEGIN)
    end = text.index(END, start) + len(END)
    return text[start:end]


class GeneratedReadContractTests(unittest.TestCase):
    def test_scaffold_and_skill_use_the_same_canonical_block(self) -> None:
        self.assertEqual(SCAFFOLD.CANONICAL_VAULT_READ_PATH.rstrip("\n"), canonical_block_from_skill())
        self.assertIn(SCAFFOLD.CANONICAL_VAULT_READ_PATH, SCAFFOLD.VAULT_AGENTS)
        self.assertIn("tracked Markdown only", SCAFFOLD.CANONICAL_VAULT_READ_PATH)
        self.assertIn("git add", SCAFFOLD.CANONICAL_VAULT_READ_PATH)


if __name__ == "__main__":
    unittest.main()
