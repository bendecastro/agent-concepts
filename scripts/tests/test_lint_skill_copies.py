"""Skill-copy comparisons with a temporary HOME and canonical tree."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('skill_copy_lint', SCRIPTS / 'lint.py')
lint = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lint
spec.loader.exec_module(lint)


class SkillCopiesTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.home = Path(temp.name)
        for context in (patch.dict(os.environ, HOME=str(self.home)),
                        patch.object(lint, 'ROOT', self.home / 'canon')):
            context.start()
            self.addCleanup(context.stop)
        self.config = self.home / '.config/agent-concepts/skill-copies.json'
        self.config.parent.mkdir(parents=True)
        self.copy = self.home / 'repo/.agents/skills/example'
        self.canon = lint.ROOT / 'concepts/example/body'
        for directory in (self.copy, self.canon):
            directory.mkdir(parents=True)
            (directory / 'SKILL.md').write_text('public')
        self.configure(['~/repo'])

    def configure(self, repos):
        self.config.write_text(json.dumps({'repos': repos}))

    def check(self):
        issues = []
        lint.lint_skill_copies(issues)
        return [issue.message for issue in issues]

    def test_plain_string_and_byte_drift(self):
        self.assertEqual(self.check(), [])
        (self.copy / 'SKILL.md').write_text('changed')
        self.assertEqual(len(self.check()), 1)
        self.assertIn('example', self.check()[0])

    def test_intentional_is_per_repo_and_name(self):
        (self.copy / 'SKILL.md').write_text('adaptation')
        self.configure([{'path': '~/repo', 'intentional': ['example']}])
        self.assertEqual(self.check(), [])
        self.configure([{'path': '~/repo', 'intentional': ['other']}])
        self.assertIn('example', self.check()[0])
        self.configure([{'path': '~/other', 'intentional': ['example']}, '~/repo'])
        self.assertTrue(any('skill copy example' in issue for issue in self.check()))

    def test_private_override_precedes_public(self):
        private = self.config.parent / 'concepts/example/body'
        private.mkdir(parents=True)
        (private / 'SKILL.md').write_text('private')
        (self.copy / 'SKILL.md').write_text('private')
        self.assertEqual(self.check(), [])
        (self.copy / 'SKILL.md').write_text('wrong')
        self.assertIn('~/.config/agent-concepts/concepts/example/body', self.check()[0])

    def test_os_and_sync_debris_ignored(self):
        for name in ('.DS_Store', '.syncthing.SKILL.md.tmp', 'SKILL.sync-conflict-123.md'):
            with self.subTest(name=name):
                path = self.copy / name
                path.write_text('debris')
                self.assertEqual(self.check(), [])
                path.unlink()
        (self.copy / 'extra').write_text('not debris')
        self.assertEqual(len(self.check()), 1)

    def test_invalid_entries_warn(self):
        for entry in ({'path': '~/repo', 'intentional': 'example'},
                      {'path': '~/repo', 'intentional': [1]}, {'intentional': []}, None):
            with self.subTest(entry=entry):
                self.configure([entry])
                self.assertEqual(len(self.check()), 1)
                self.assertIn('repos', self.check()[0])


if __name__ == '__main__':
    unittest.main()
