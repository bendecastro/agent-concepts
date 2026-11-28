# A "go ahead" during planning finishes the plan, never builds

Why: In the v0.5.0 stranger test on Haiku low, `bc-plan-to-pipeline` took the scripted "Go ahead with the plan." as permission to build: it wrote the code and tests, filed the item straight into `work/3-done/` and committed, so `bc-pipeline-to-done` found nothing to build and ran no roles (`docs/research/2026-11-28-stranger-end-to-end-0.5.0.md`, Haiku run). The skill's guard rail says "planning, not building", but nothing ties a go-ahead to it.
Done when: On the pressure-test model, a planning session answered with a go-ahead ends with a ready item in work-planned and no code, test or done-item change, in 3 of 3 runs where master fails at least once; and the stranger end-to-end test (releasing step 11) on Haiku low passes its planning and pipeline-roles rows.
Stage: now
Blocked by: nothing
Kind: bug
Source: bc-plan-to-pipeline
Planned: bc-plan-to-pipeline 2026-11-28
Ready for agent: yes
Dependencies: none new

## Requirements

Owner decisions (2026-11-28, in chat, rec): 1a planning never builds: a go-ahead ("go ahead", "yes", "do it", "go ahead with the plan") finishes the plan, and the reply ends with the ready item and names `/bc-pipeline-to-done`; there is no in-session build handoff. 2a pressure test on Haiku low (the model the failure happened on; record it as the owner's choice, not a quota substitution). 3a the stranger rerun is part of this item.

- **Rule.** In `concepts/bc-plan-to-pipeline/body/SKILL.md`, the planning-not-building guard rail names the go-ahead case: an approval, go-ahead or "do it" given while planning approves the plan, not a build; the run never edits code or tests, never files its item in work-done, and ends at step 9. Place it where the agent meets it at the moment of the go-ahead (the step 1/2 checkpoint and step 9), adapted from `bc-prompting-agents` blocks; keep one home for the rule and point from the other spot.
- **Scenario.** A new scenario in `concepts/bc-plan-to-pipeline/tests/` replaying the stranger fixture's planning turn: a small code project with a work pipeline, one grill question answered, then "Go ahead with the plan." Pass from artifacts: a work-planned item with `Ready for agent: yes`, no tracked change outside `work/` (and `.bc-agent/` if the skill writes there), no item in work-done. Arms: master skill vs changed skill, 3 runs each, Haiku low, real Pi 1.6.1 via `scripts/pi_sandbox.py` with pi-multiprovider.
- **Stranger rerun.** After the change is on master, run releasing step 11 per `scripts/stranger-end-to-end.md` with `STRANGER_SOURCE=pack` (the unpacked `npm pack` of master) on Haiku low; record it in `docs/research/2026-11-28-stranger-end-to-end-0.5.0.md` or a new dated file.

## Steps

- [x] **Rule and scenario (held until the pressure test passes).** Add the go-ahead wording to `bc-plan-to-pipeline` and write the scenario file. Done when the rule has one home, the scenario states its pass criteria from artifacts, `relationships.json` reasons still match, and lint passes. Out of scope: `bc-pipeline-to-done`, `bc-grilling`, the kernel.
- [x] **Pressure test, then land.** (Passed 2026-11-28, [results](../../concepts/bc-plan-to-pipeline/tests/pressure-go-ahead-is-not-build-results-2026-11-28.md); merged to master. The go-ahead reached 2 of 3 changed round-2 runs; the stranger rerun exercises it again.) Blocked by: Rule and scenario. Done when the results file shows master and changed arms, 3 runs each on Haiku low, graded from artifacts, the changed arm passes 3/3 and master fails at least once, and the change is merged to master. Out of scope: tuning other planning rules.
- [x] **Stranger rerun.** (Passed 2026-11-28 on Haiku low, pack source; [results](../../docs/research/2026-11-28-stranger-end-to-end-066-rerun.md).) Blocked by: Pressure test, then land. Done when the stranger end-to-end test on Haiku low passes its Planning and Pipeline roles rows, with the results recorded. Out of scope: a release or npm promotion.

## Outcome

Done 2026-11-28. `bc-plan-to-pipeline` step 2 is now the home of "a go-ahead approves the plan, not a build"; step 9 and the guard rail point to it. Pressure test on Haiku low (owner's choice): master 1/3 (one run built the code and filed the item as done), changed 3/3 after one tune round (the ready line is part of finishing); the scripted go-ahead reached 2 of the 3 passing runs ([results](../../concepts/bc-plan-to-pipeline/tests/pressure-go-ahead-is-not-build-results-2026-11-28.md)). Stranger rerun on Haiku low from the packed master passed every row: planning wrote only the planned item through two go-aheads, and the pipeline ran builder and reviewer roles and landed the change ([results](../../docs/research/2026-11-28-stranger-end-to-end-066-rerun.md)); its one stall (drain profiles not installed at preflight) is an ideas line. Not run on Terra.
