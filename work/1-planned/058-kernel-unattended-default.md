# The kernel says what to do when nobody can answer

Why: About six skills restate "when no one can answer (delegated child, headless job, owner away), take the recommended option and record the assumption" in different words, and `bc-security-audit`, `bc-teach` and `bc-seo` have no rule. Owner choice: the kernel owns it.
Done when: AGENT-KERNEL.md has one short rule (which decisions may be assumed and recorded, which must stop: destructive, publishing, owner-only), the skills' restated sentences shrink to skill-specific deltas, and the rule holds under a pressure scenario on the pressure-test model.
Stage: now
Blocked by: nothing
Kind: architecture
Source: modularity scan 2026-11-27 (run ~/.local/state/bc-swarm/2026-11-27-agents-modularity/memo.md), owner pick 1 (candidate E; owner: put it in the kernel)
Planned: bc-plan-to-pipeline 2026-11-27
Waiting on owner: parked after the fourth tuning round failed its pre-set bar (owner answer, 2026-11-28). Round 4 on Haiku: new kernel 5/6, old kernel 0/6; Terra round 3 was 1/6 strict. Decide: accept 5/6, or redesign the rule or the test. Kernel text and results are on branch `058-hold` (`pressure-unattended-default-results-2026-11-28-round4.md`).

## Requirements

- Find copies: `rg -il "unattended|no user can answer|no one to answer|owner is away" concepts/*/body`. Keep skill-specific parts (bc-tdd's behavior-list record, bc-self-improve's headless carry rule).
- Kernel copies outside the repo (`~/.config/agent-concepts/kernel-copies.json`) and the Claude/Codex kernel packages follow per the release steps; account for agent-kernel's RELATIONSHIPS.md edges.

## Steps

- [ ] Add the kernel rule, trim the copies, pressure-test. Done when the scenario (headless run, one judgment call, one destructive step) shows the agent assume-and-record the first and stop on the second, with and without the rule compared, and lint passes.
  - 2026-11-28: rule added, `bc-design`/`bc-tdd` trimmed, packages staged, scenario written (`concepts/agent-kernel/tests/pressure-unattended-default.md`); pressure run pending (Terra low quota).
  - 2026-11-28 round 4 (final tune round, Haiku 5.5 low since Codex quota was out): record worded as an assumption made because no one could answer; FAIL strict, new 5/6 (A 3/3, B 2/3), old 0/6. Owner decides next step.

## Outcome

_To be filled when finished or dropped._
