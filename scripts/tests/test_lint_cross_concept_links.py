"""A public skill body must not link into another concept's folder."""

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("lint_under_test", SCRIPTS / "lint.py")
lint = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lint
spec.loader.exec_module(lint)


class CrossConceptLinkTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for name in ("alpha", "beta"):
            (self.root / "concepts" / name / "body").mkdir(parents=True)
            (self.root / "concepts" / name / "body" / "SKILL.md").write_text("# body\n")

    def write(self, rel_path, text):
        path = self.root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def check(self):
        issues = []
        lint.lint_cross_concept_links(issues, self.root)
        return issues

    def test_markdown_link_into_other_concept_is_error(self):
        self.write("concepts/alpha/body/SKILL.md", "See [tdd](../../beta/body/SKILL.md#levels).\n")
        issues = self.check()
        self.assertEqual(["ERROR"], [i.severity for i in issues])
        self.assertIn("concepts/alpha/body/SKILL.md", issues[0].message)
        self.assertIn("../../beta/body/SKILL.md#levels", issues[0].message)

    def test_link_from_supporting_file_in_subfolder_is_error(self):
        self.write("concepts/alpha/body/refs/pi.md", "[x](../../../beta/CONCEPT.md)\n")
        self.assertEqual(1, len(self.check()))

    def test_inline_relative_path_into_other_concept_is_error(self):
        self.write("concepts/alpha/body/SKILL.md", "Read `../../beta/body/SKILL.md` first.\n")
        self.assertEqual(1, len(self.check()))

    def test_links_within_same_concept_pass(self):
        self.write("concepts/alpha/body/SKILL.md", "[a](./x.md) [b](x.md) [c](../tests/r.md) `../CONCEPT.md`\n")
        self.write("concepts/alpha/body/sub/y.md", "[up](../../SKILL.md)\n")
        self.assertEqual([], self.check())

    def test_links_outside_concepts_are_not_this_checks_concern(self):
        self.write("concepts/alpha/body/SKILL.md", "[src](../../../docs/raw/a.md) [web](https://x.test/a)\n")
        self.assertEqual([], self.check())


if __name__ == "__main__":
    unittest.main()
