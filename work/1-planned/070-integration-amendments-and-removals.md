# Integration records amended decisions, and removals check the tests that name them

Why: in another project's integration a planned detail was disproved by the merged tree (a shortcut row that made a list scroll) and reverted mid-integration; the amendment was logged by hand and nearly lost. The same step failed the full suite twice because old tests still used a removed editor and a renamed label: workers run only their targeted tests, so the 50-minute full run was the first to see it.
Done when: On the pressure-test model, an integrator who reverts a planned detail edits the step with an `Amended` note and records the amendment in the same commit, and a worker whose packet removes or renames a user-visible name searches the tests for the old name and runs the matches, each 3 of 3 with master failing at least once.
Stage: next
Blocked by: 068-replan-protocol
Kind: feature
Source: owner request 2026-11-28 (replan experience study)
Planned: bc-plan-to-pipeline 2026-11-28
Ready for agent: yes
Dependencies: none new

## Requirements

- **Amendments.** When integration changes a planned or recorded decision, the integrator adds an indented `Amended <date>: <what changed> because <evidence>` note under the step and, when the decision was recorded elsewhere (a decision record, the log), records the amendment there in the same commit. No new item state.
- **Removal fallout.** A build packet or brief that removes or renames a user-visible name (UI label, component, command, flag, key) tells the worker to search the test folders for each old name and run the matching tests before reporting done. One home for the rule (expected: `bc-pipeline-to-done`'s builder brief, with a pointer from `bc-dispatching-parallel-agents` if packets are written there); settle with lint's repeated-text check.
- **Test.** Two scenarios (integrator reverts a planned detail; worker renames a label used in an old test), master vs changed, 3 runs each, Terra low via `scripts/pi_sandbox.py`.

## Steps

- [ ] **Amendment and removal rules in the skills (held until the pressure test passes).** Done when both Requirements have one home, pointers and `relationships.json` edges are in place, and lint passes. Out of scope: running the full suite in workers (still the integrator's job), changes to the Replanning line.
- [ ] **Pressure test, then land.** Blocked by: Amendment and removal rules in the skills. The Test requirement. Done when the results file shows changed 3 of 3 on both scenarios and master failing each at least once, graded from artifacts. Out of scope: re-testing `068-replan-protocol`'s rules.
