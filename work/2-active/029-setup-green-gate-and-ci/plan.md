# Setup leaves a passing gate and a working CI job

Why: On an existing repository without CI, setup has no rule for filling `./scripts/gate`, so it stays red and blocks landing; the generated CI job leaves its toolchain as a TODO, so a locally green gate fails in CI; `conventions/validation.md` and `file-layout.md` stay stubs.
Done when: Setting up an existing repository ends with a gate that passes locally, a CI job that installs the project's toolchain, and filled validation and file-layout conventions, or names each gap as an owner action in the close-out; requirements in [requirements.md](requirements.md).
Stage: now
Blocked by: nothing
Kind: build
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state
Planned: bc-plan-to-pipeline 2026-11-26
Ready for agent: yes
Held by: pi 01a218e4 since 2026-11-26 18:23 +00:00

## Steps

- [ ] Gate without CI and filled conventions: reword setup steps 2 and 7 for the no-CI path and the conventions; pressure scenario on the Python fixture. Blocked by: nothing. Stories 1, 3, 4. Done when the with-change run leaves a passing gate and filled conventions while the baseline does not, results recorded beside the scenario in `concepts/bc-setup-project/tests/`. Out of scope: CI toolchain.
- [ ] CI toolchain from existing CI or markers: reword the CI part of setup and the scaffold TODO comment; pressure scenario on the Node fixture. Blocked by: Gate without CI and filled conventions. Stories 2, 4. Done when the with-change run's workflow installs Node and dependencies before `scripts/gate` while the baseline does not; CONCEPT status, `index.md`, `.bc-agent/log.md` updated; lint has 0 ERROR and the gate passes. Out of scope: running CI remotely.

## Outcome

