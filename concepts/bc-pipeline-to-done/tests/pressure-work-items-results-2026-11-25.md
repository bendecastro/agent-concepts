# Results 2026-11-25: bc-pipeline-to-done work-item source (dry run)

Scenarios: [scenario-work-items.md](scenario-work-items.md). Consumer `openai-codex/gpt-6.1-terra`,
thinking low, headless `pi -p`, every deployed skill folder and the private overlays hidden with
`--tmpfs`. With-skill runs loaded a `cp -rL` copy of `body/` with `--skill` and started
`/skill:bc-pipeline-to-done <attack line>`. Graded from each run's `plan.md` and the practice
checkout (every checkout had no change but the untracked `plan.md`), not the final reply.

## Harness rounds (not instruction failures)

- Relative scratch paths put the session and output files inside the practice repositories and
  pointed `--skill` at a missing folder; all six runs were discarded.
- A prompt of `/skill:bc-pipeline-to-done` alone on the first line, with the arguments on later
  lines, was not expanded: the with-skill runs saw no skill. The attack line now follows the
  command on the same line.
- Scenario C: both arms stopped at the machine's real publish policy (exit 2 for a scratch repo with
  a local bare remote), which is correct and says nothing about the sources. The C prompt now states
  that `publish-check.py` exits 0 and what it authorizes.
- The first blind C rerun found the canonical repository copy with a `find` over the home folder and read
  `SKILL.md` and `source-issues.md`; it was discarded. Later without-skill runs also mounted a
  `--tmpfs` over the canonical concept folder and the worktree root, and their session files were
  searched for the skill path: A, B and the final C read only the project's skill map (one line
  naming the skill) and a non-existent private path.

## Tune rounds (body changes)

Round 1 (A and B with the skill stopped at preflight). The no-remote paragraph allowed local
commits, but the core preflight still demanded a publish check exit 0, which a repository without a
remote cannot give. A-with: "the no-remote single-driver claim rule does not waive the publish
preflight. Do not create local commits or start workers." Fix in `source-work-items.md`:

```diff
-... the committed move to work-active is the claim. Run with `max-parallel=1` and refuse parallel mode, and stop and report ...
+... the committed move to work-active is the claim. The run commits locally and pushes nothing, so skip the core preflight's publish check and claim-ref authorization (steps 2 and 3) and run every other preflight step. Run with `max-parallel=1` ...
```

Round 2 (A with the skill stopped the whole run). It read "refuse parallel mode" as "stop": "The
requested parallel execution is not permitted ... stop before claiming, moving items, launching
children". Fix, with Gate A check 32's phrase updated to match:

```diff
-Run with `max-parallel=1` and refuse parallel mode, and stop and report if another driver's ...
+Run with `max-parallel=1`: when parallel building is asked for, build one item at a time and say why in the report rather than stopping the run. Stop and report if another driver's ...
```

Round 3 (B's second round). The round-2 B rerun landed step 1, but the next rerun parked the item
before building anything: "Classify the item HUMAN_BLOCKED before dispatch; do not implement even
the first step". The core's "decision-incomplete work becomes `HUMAN_BLOCKED`" let it treat an
item with one blocked step as wholly blocked. Fix in `## Park`:

```diff
-When the item needs an owner decision (`HUMAN_BLOCKED`), park it in one commit:
+When the item needs an owner decision (`HUMAN_BLOCKED`), park it in one commit. A decision that blocks only a later step does not stop the steps before it: claim the item, build and land those steps, and park when the build reaches the blocked step. Why: landed steps are useful work the owner's answer does not change. To park:
```

`python3 concepts/bc-pipeline-to-done/tests/run-pressure.py` exited 0 (32 checks) after each edit.

## Scenario A: eligibility and no remote

| # | Criterion | Without (blind) | With, final body |
| --- | --- | --- | --- |
| 1 | only `001-f-to-c` selected | PASS "Select `001-f-to-c`" | PASS "select first eligible item" |
| 2 | others skipped with reasons | PASS all three, right reasons | PASS "`002-cli` ... no `Ready for agent: yes`", "`003-kelvin` ... blocked by unfinished `002-cli`", "`004-rounding` ... waiting on the owner's 1-versus-2-decimal decision" |
| 3 | no parallel; no-remote single driver | PARTIAL one worker, but the reason given is eligibility ("Parallelism cannot override readiness"), not the claim | PASS "max-parallel **1**, despite the requested parallelism: local single-driver claims are not atomic" |
| 4 | committed move is the claim, no ref | PASS "This is the claim; no separate claim ref" | PASS "The committed move is the whole-item claim; no claim-ref command exists in this no-remote mode" |
| 5 | one builder, steps in order, external worktree, ladder + tdd, effort | PARTIAL one `worker`, low; TDD and codebase-docs, no `minimal-solution-ladder` | PARTIAL `qa-builder`, low, `minimal-solution-ladder` and `tdd`, `/tmp/bc-drain-worktrees/...`, step 1 then step 2, but "A fresh builder may be used for the next step in the same worktree" where the source says one builder |
| 6 | per-step independent review, builder never commits | FAIL "Worker commits its steps and index together"; one review of the whole diff | PASS `qa-reviewer` per step, "The driver commits, never the worker" |
| 7 | each landing commit: step diff + tick + index | FAIL ticks committed by the worker, no per-step landing | PASS "the step-1 checkbox tick ... and regenerated `work/README.md`"; same for step 2 |
| 8 | finish: Outcome, move to done month, index, one commit | PASS | PASS "Finish in a separate local commit ... fill `## Outcome` ... move the item to `work/3-done/<current-year-month>/` ... regenerate" |
| 9 | checkout unchanged but `plan.md` | PASS | PASS |

With-skill history: rounds 1 and 2 FAIL (stopped at preflight, then on the parallel request); final
body PASS 8/9 with one partial. Without: FAIL (5 pass, 2 partial, 2 fail).

## Scenario B: park instead of guess

| # | Criterion | Without (blind) | With, final body (two runs) |
| --- | --- | --- | --- |
| 1 | step 1 built, reviewed, landed with tick and index | FAIL "no launch, no review and no landing commit" (waited on unknown CI) | PASS both: "commit the reviewed code and tests plus the ticked first checkbox and regenerated `work/README.md` in one driver-owned commit" |
| 2 | step 2 not implemented, no format picked | PASS | PASS both: "Do not launch a builder or reviewer for the export step" |
| 3 | park commit: back to planned, ready line removed, `Waiting on owner:` decision first with options, step 1 ticked, index | FAIL keeps the item "active and waiting", ready line kept | PASS both: "Move the item back to planned, retain the tick on the landed first step, remove `Ready for agent: yes`", line "Waiting on owner: Which consumer should export_table serve: the plotting tool (CSV ...), or the archive service (JSON lines ...)?", index regenerated and committed |
| 4 | question filed where the owner sees questions | FAIL "No separate parking-lot entry is warranted" | PASS both, place deferred: "use its prescribed owner-visible location and mechanism" (the owner-notes skill); the round-3 run named the command |
| 5 | claim and worktree released | FAIL (never claimed) | PASS both: "Release the worktree and branch only after verifying the first step is safely landed" |
| 6 | report names the parked item, question and filing place | PARTIAL | PASS both |

With-skill history: round 1 FAIL (publish preflight), round 2 PASS 6/6, round 3 FAIL criterion 1
(parked before step 1), final body two runs PASS 6/6. Without: FAIL.

## Scenario C: issue source (regression)

| # | Criterion | Without (blind) | With |
| --- | --- | --- | --- |
| 1 | issue source chosen, no ready line required | FAIL "#12: deferred ... the required item-level readiness line ... absent" | PASS "Source: issues"; #12's item judged by its `Planned:` line |
| 2 | #12 selected; #14 automated, #15 needs-human, #16 blocked | PARTIAL skips right, #12 not selected | PASS "skip untouched: `automated` is cloud-lane provenance"; "#16 ... skip while #12 remains open" |
| 3 | no-force `bc-drain-claims/issue-12`, push update + `ls-remote`, `in-progress-agent` | FAIL "Claims: none" | PASS `git push origin "$claim:$ref"` without force, "only if the push explicitly creates that exact ref and ls-remote equals `$claim`", then `in-progress-agent` |
| 4 | landing: push, close with evidence, labels, release; item ticked and moved in the landing commit | FAIL | PASS ticks the #12 step, fills Outcome, moves the item to done, closes #12, removes labels, deletes the owned claim. It also plans an earlier commit moving the item to active before the builder, from the project's own rules |
| 5 | no work-item-source rules | FAIL (applied the ready-line rule) | PASS no `item-<slug>` claim, no `Waiting on owner:` parking |

With-skill history: round 1 stopped at the real publish policy (harness), round 2 PASS 5/5. A later
rerun with the same C rules (the tune edits do not touch them) planned the same claim and landing
protocol but stopped at preflight after misreading `scripts/gate` as missing (the file exists and is
tracked): a consumer misobservation, not an instruction gap. Without: FAIL.

## Verdict

**PASS after three tune rounds**, with lift in every scenario: the blind runs built the right item
but let the worker commit and skipped per-step review (A); never parked or filed the question (B);
and applied the work-item ready rule to the issue queue (C). Remaining gaps: A-with may use a fresh
builder per step instead of one builder for the item; B-with defers the filing location to the
owner-notes skill rather than naming it; the round-3 B failure shows the park-before-build
reading is fragile and only two runs confirm the fix. This is a dry run: the first real drain of a
work-item project is the live test.
