# Release once a stranger installs from the README with no friction

Why: Strangers install tagged releases, and `v0.3.0` predates every fix from the 2026-11-26/27 stranger tests.
Done when: The stranger end-to-end test passes installing exactly as the README says (no copied roles), the new dependency rule's pressure test holds, and a new release is tagged and pushed per `docs/guides/releasing.md`.
Stage: now
Blocked by: 042-one-command-pi-install, 043-plain-pipeline-messages, 045-starter-items-for-new-projects
Kind: release
Source: owner decision 6a (release without asking again), 2026-11-27
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Steps

- [x] Pressure-test the planned-dependencies rule on the pressure-test model (old/new arms). Done when results are recorded and `test_status` set. Out of scope: other concepts.
- [x] Pressure-test `bc-setup-project`'s new-project starter-items arm (`concepts/bc-setup-project/tests/pressure-starter-items.md`) on the pressure-test model. Done when results are recorded and `test_status` set. Out of scope: other arms.
- [x] Pressure-test `bc-security-audit`'s typed-command full-audit rule on the pressure-test model (see `docs/research/2026-11-27-release-audit.md`). Done when results are recorded and `test_status` set.
- [x] Fix the build stall the 2026-11-27 stranger rerun found (owner choices 1a 2a): a user who names an item sets the order for that run (`bc-pipeline-to-done`), and a bare yes to a question with a recommended option means that option (`agent-kernel`). Done when both rules hold in pressure tests on the pressure-test model (old/new arms). Out of scope: other pipeline rules.
- [ ] Rerun the stranger test with the README install and record results next to the 039 rerun. Done when setup, plan and build pass with no copied roles. Out of scope: other harnesses.
- [ ] Release per `docs/guides/releasing.md`. Done when the tag's `release` workflow is green.

## Outcome

_To be filled when finished or dropped._
