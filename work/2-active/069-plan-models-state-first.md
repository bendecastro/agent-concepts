# Planning stateful work writes and reviews a state table before any build step

Why: most long review loops in the replan study came from interactions nobody modelled before building: several writers, delivery order between machines, versions in rollout, identity (another project's sync items went through six blocking reviews, then a replan with a model built first), and state transitions (`067-planning-map-mode` passed its pressure test 3 of 3, then blocked twice in review). A passing pressure test does not cover these; reviewers found them one at a time.
Done when: On the pressure-test model, planning a change that touches state shared across writers or machines writes a `### State model` table (states × events × orderings, each with its required outcome) and a first review-the-model step that blocks every build step, 3 of 3, with master failing at least once; a stateless change gets no table, 3 of 3.
Stage: next
Blocked by: 068-replan-protocol
Kind: feature
Source: owner request 2026-11-28 (replan experience study)
Planned: bc-plan-to-pipeline 2026-11-28
Ready for agent: yes
Dependencies: none new

## Requirements

Owner decision (2026-11-28): a reviewed table, with an executable model only when the project's own rules ask for one.

- **When.** During planning, after the grill: does the change touch state shared across writers, time, versions, machines or identity (sync, migration, concurrency, caching, a state machine, a multi-step workflow with persisted status)? If not, nothing changes.
- **Table.** If so, the requirements get a `### State model` section: rows are states (including partial and legacy ones), columns are events and their orderings across writers or machines, and each cell names the required outcome. Unknown cells are named, not left blank; an unknown the session cannot settle follows the usual open-question rules.
- **Review first.** The first step is "Review the state model": an independent reviewer looks for missing states, events, orderings and version pairings; Done when it approves. Every build step is blocked by it. `Ready for agent: yes` may still be written: the drain runs the review step.
- **Executable model.** Only when the project's rules ask for one (for example for sync items) does the step also build an executable check of the table.
- **Replans feed the table.** When `068-replan-protocol`'s Replan note names unmodelled sequences and the item has a state model, those rows go into the table in the same edit.
- **Test.** Two scenarios (a cross-machine sync feature; a stateless text change), master vs changed, 3 runs each, Terra low via `scripts/pi_sandbox.py`.

## Steps

- [ ] **State-model check in the planning skill (held until the pressure test passes).** `bc-plan-to-pipeline` (and `bc-prd-drafting` if the table belongs in its template), the review-first step, the replan link; CONCEPT.md provenance; `relationships.json` edges if any. Done when every Requirement has one home and lint passes. Out of scope: an executable-model tool, a new review role.
- [ ] **Pressure test, then land.** Blocked by: State-model check in the planning skill. The Test requirement. Done when the results file shows changed 3 of 3 on both scenarios and master failing the stateful one at least once, graded from artifacts. Out of scope: testing the drain running the review step.
