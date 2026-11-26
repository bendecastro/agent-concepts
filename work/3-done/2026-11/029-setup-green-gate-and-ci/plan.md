# Setup leaves a passing gate and a working CI job

Why: On an existing repository without CI, setup has no rule for filling `./scripts/gate`, so it stays red and blocks landing; the generated CI job leaves its toolchain as a TODO, so a locally green gate fails in CI; `conventions/validation.md` and `file-layout.md` stay stubs.
Done when: Setting up an existing repository ends with a gate that passes locally, a CI job that installs the project's toolchain, and filled validation and file-layout conventions, or names each gap as an owner action in the close-out; requirements in [requirements.md](requirements.md).
Stage: now
Blocked by: nothing
Kind: build
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state
Planned: bc-plan-to-pipeline 2026-11-26
Ready for agent: yes

## Steps

- [x] Gate without CI and filled conventions: reword setup steps 2 and 7 for the no-CI path and the conventions; pressure scenario on the Python fixture. Blocked by: nothing. Stories 1, 3, 4. Done when the with-change run leaves a passing gate and filled conventions while the baseline does not, results recorded beside the scenario in `concepts/bc-setup-project/tests/`. Out of scope: CI toolchain.
  - Review: changes requested by tier-1 2026-11-26
  - Review: changes requested by tier-1 2026-11-26
  - Gate: pass ./scripts/gate at ac96cac 2026-11-26
  - Landed in `ac96cac`. The second review's one finding (a stale log line) was fixed with the reviewer's exact wording and not re-reviewed. Pressure: one run per arm; revised body ran its portable gate, old body wrote the same gate but did not run it.
- [x] CI toolchain from existing CI or markers: reword the CI part of setup and the scaffold TODO comment; pressure scenario on the Node fixture. Blocked by: Gate without CI and filled conventions. Stories 2, 4. Done when the with-change run's workflow installs Node and dependencies before `scripts/gate` while the baseline does not; CONCEPT status, `index.md`, `.bc-agent/log.md` updated; lint has 0 ERROR and the gate passes. Out of scope: running CI remotely.
  - Owner 2026-11-26: the Node fixture with existing CI showed no defect (old and new text both set up Node and the gate runs `npm ci`). Run one more pair on a fixture with no CI that uses uv or Rust; land the wording only if the old text fails there.
  - Review: changes requested by tier-1 2026-11-26
  - Review: approved by tier-1 2026-11-26
  - Gate: pass ./scripts/gate at 8d4871c 2026-11-26
  - Landed in `8d4871c`. The old text also provisioned CI on the uv no-CI fixture (setup-uv and Python before the gate), so per the owner's decision the setup wording is unchanged; only the generated workflow's TODO comment changed. The revised arm of that pair died at startup on a provider usage limit and is not counted.

## Outcome

Landed in `ac96cac` (setup on an existing repo without CI verifies a portable gate locally and fills validation and file-layout conventions; unknowns become owner actions) and `8d4871c` (clearer TODO in the generated CI workflow; pressure on a Node project with CI and a uv project without CI found the old setup wording already provisions CI, so it is unchanged). Pressure: Terra low, one run per arm; results beside the scenarios in `concepts/bc-setup-project/tests/`. Full gate: 577 passed, 4 skipped at `8d4871c`.
Spent: 1h 32m active, 25.5M tokens, $12.67 (estimated; pi 16 sessions, claude-code 0 sessions, codex 0 sessions; other tools not counted)

