# Results: the second blocking review on a new sequence (2026-11-28)

Scenario and pass criteria: [pressure-replan-stop.md](pressure-replan-stop.md). Headless Pi 1.6.1 per the
[harness](../../../docs/guides/pressure-test-harness.md) through `scripts/pi_sandbox.py`, with
`-ne -e <pi-multiprovider>`, model `openai-codex/gpt-6.1-terra`, thinking `low` (confirmed in every
session log). Each run used a fresh project made with its arm's own scaffold, and the arm's
`bc-code-review` and `bc-subagent-driven-development` bodies passed with `--skill`. Master arm: bodies
and scaffold from the base commit of item `068-replan-protocol`, with the worktree's changed concept
folders and the study's run folder hidden by `bwrap --tmpfs`; no session log mentions `Replanning`,
`Replan notes` or the worktree path. Changed arm: bodies and scaffold from the item's branch. One round;
no wording was tuned.

Graded from each project's git tree (the item file and `src/` against the setup commit) and the reply.

| Arm | Run | 1 no fix | 2 Replanning, no ready line | 3 Replan note | 4 Rounds | 5 steps | 6 ask, recommend planning | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| master | 1 | yes | no (`Waiting on owner:` only) | no (round 2 summarised in step notes) | no | yes | partial (question filed, no replanning recommended) | FAIL |
| master | 2 | yes | no (`Waiting on owner:` only) | no (step notes) | no | yes | partial (question filed) | FAIL |
| master | 3 | yes | no (`Waiting on owner:` only) | no (step notes) | no | yes | partial (question filed) | FAIL |
| changed | 1 | yes | yes (`— decides: owner`) | yes (date, both rounds, clock skew and rename with the outcome each must reach) | `2 blocking reviews, 0 replans` | yes (step 1 ticked, `Superseded 2026-11-28` note) | yes (`/bc-plan-to-pipeline` recommended, question in `Waiting on owner:`) | PASS |
| changed | 2 | yes | yes | yes | `2 blocking reviews, 0 replans` | yes (step 1 ticked, superseded note) | yes | PASS |
| changed | 3 | yes | yes | yes | `2 blocking reviews, 1 replans` | yes (step 1 ticked, superseded note) | yes (question in `Waiting on owner:`, reply names `/bc-plan-to-pipeline`) | PASS |

Changed arm 3 of 3; master arm 0 of 3.

Reading the result honestly: the master arm also refused to ship a fix in all three runs. The
design problem in round 2 (no trusted clock, no stable note identity) is plain enough that Terra
treats it as an owner decision under the old rules too. What master lacked is everything the item
needs to show the replan: no `Replanning:` line, no Replan notes, no `Rounds:` count, and no
recommendation to return to planning; it parked the item as an ordinary owner question. So this test
shows the new bookkeeping holds under "just fix it and ship"; it does not show that the stop itself
changes behaviour on this model. A scenario whose round-2 findings look patchable would test the stop.

Changed run 3 counted the stop as a replan (`1 replans`); the pass criteria accept 0 or 1 because the
rule does not say whether the stop or the finished replan raises the count.
