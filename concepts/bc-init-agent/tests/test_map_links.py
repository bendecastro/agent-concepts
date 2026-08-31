"""Checks that the generated context map participates in wiki graph linting."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
SCAFFOLD_PATH = ROOT / "concepts/bc-init-agent/body/scaffold.py"
LINTER_PATH = ROOT / "concepts/bc-wiki-maintain/body/wiki_lint.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SCAFFOLD = load_module("bc_init_scaffold_map_links", SCAFFOLD_PATH)
WIKI_LINT = load_module("bc_wiki_maintain_map_links", LINTER_PATH)


class GeneratedMapLinkTests(unittest.TestCase):
    @staticmethod
    def scaffold(root: Path) -> Path:
        result = subprocess.run(
            [
                sys.executable,
                str(SCAFFOLD_PATH),
                "--root",
                str(root),
                "--slug",
                "demo-project",
                "--date",
                "2026-08-31",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise AssertionError(f"scaffold failed:\n{result.stdout}\n{result.stderr}")
        return root / ".bc-agent"

    def test_generated_map_rows_are_real_links_seen_by_production_parser(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            vault = self.scaffold(Path(directory))
            map_text = (vault / "map.md").read_text(encoding="utf-8")
            rows = [line for line in map_text.splitlines() if line.startswith("- ")]
            parsed = list(WIKI_LINT.links(map_text))

            self.assertGreater(len(rows), 0)
            self.assertEqual(len(parsed), len(rows))
            self.assertTrue(
                all(re.fullmatch(r"- \[[^\]\n]+\]\([^ )\n]+\)", row) for row in rows),
                rows,
            )
            self.assertFalse(any(row.startswith("- `") for row in rows), rows)
            self.assertIn("Link only targets that resolve inside this vault", map_text)

    def test_every_generated_map_target_is_a_scaffolded_vault_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            vault = self.scaffold(root)
            parsed = list(WIKI_LINT.links((vault / "map.md").read_text(encoding="utf-8")))
            scaffolded = {
                path.relative_to(vault).as_posix()
                for path, _content, _is_root in SCAFFOLD.targets(
                    root, "demo-project", "2026-08-31"
                )
                if path.is_relative_to(vault)
            }

            self.assertGreater(len(parsed), 0)
            for target, _display in parsed:
                self.assertNotIn("..", Path(target).parts)
                self.assertIn(target, scaffolded)
                self.assertTrue((vault / target).is_file(), target)

    def test_existing_inline_code_map_gets_upgrade_note(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            vault = root / ".bc-agent"
            vault.mkdir()
            (vault / "map.md").write_text(
                "# Context Map\n\n- `project/overview.md`\n", encoding="utf-8"
            )

            notes = SCAFFOLD.upgrade_notes(root, "code")

            self.assertTrue(
                any("map.md" in note and "real Markdown links" in note for note in notes),
                notes,
            )

    def test_new_map_does_not_emit_its_own_upgrade_note(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.scaffold(root)

            notes = SCAFFOLD.upgrade_notes(root, "code")

            self.assertFalse(any("map.md" in note for note in notes), notes)


if __name__ == "__main__":
    unittest.main()
