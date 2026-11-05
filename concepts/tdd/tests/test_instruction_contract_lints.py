"""Source-contract lints, not behavioural coverage or pressure certification."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]


class InstructionContractLints(unittest.TestCase):
    def test_kernel_verification_scope_lint(self):
        kernel = (ROOT / 'concepts/agent-kernel/body/AGENT-KERNEL.md').read_text()
        bullet = next(line for line in kernel.splitlines() if line.startswith('- A new or'))
        self.assertLess(len(bullet.split()), 70)
        for phrase in ('behaviour-changing assertions', 'mechanical', '`tdd`'):
            self.assertIn(phrase, bullet)
        self.assertNotIn('network', bullet)

    def test_tdd_scope_and_small_fix_exception_lint(self):
        skill = (ROOT / 'concepts/tdd/body/SKILL.md').read_text()
        description = next(line for line in skill.splitlines() if line.startswith('description:'))
        for phrase in ('regression test', 'bug fix', 'behaviour-changing assertions'):
            self.assertIn(phrase, description)
        for phrase in ('Reading, running', 'mechanical', 'Small bug fixes', 'diagnosing-bugs'):
            self.assertIn(phrase, skill)

    def test_kernel_loads_tdd_edge_lint(self):
        edges = json.loads((ROOT / 'concepts/relationships.json').read_text())['edges']
        self.assertTrue(any(edge['from'] == 'agent-kernel' and edge['to'] == 'tdd'
                            and edge['relation'] == 'loads' for edge in edges))


if __name__ == '__main__':
    unittest.main()
