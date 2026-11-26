# Setup leaves a passing gate and a working CI job

Why: On an existing repository without CI, setup has no rule for filling `./scripts/gate`, so it stays red and blocks landing; the generated `.github/workflows/gate.yml` leaves a toolchain TODO, so a locally green gate fails in CI; `conventions/validation.md` and `file-layout.md` stay stubs.
Done when: Setting up an existing repository fills the gate from verified local test/build commands when there is no CI, configures the CI job's toolchain from the project's markers or existing CI, fills validation and file-layout from the survey, and reports anything unresolved as an owner action instead of leaving a silent TODO.
Stage: next
Blocked by: nothing
Kind: build
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state

## Steps

- [ ] Rule in `bc-setup-project` for repos without CI: derive the minimum gate from documented local commands, run it, record the result.
- [ ] Toolchain setup for the generated CI job from lockfiles/markers or the existing CI; report unknowns.
- [ ] Fill validation and file-layout conventions from verified survey facts.
- [ ] Pressure test on a fixture repo with tests but no CI; lint and gate green.

## Outcome

