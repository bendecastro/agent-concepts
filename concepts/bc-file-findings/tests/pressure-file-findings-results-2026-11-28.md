# Results: filing through bc-file-findings (2026-11-28)

Scenario and criteria: [`pressure-file-findings.md`](pressure-file-findings.md). Fixture from `make-fixture.sh`.

**Consumer: `anthropic/claude-haiku-5-5`, thinking low**, not the configured Terra low: the Codex 5-hour limit was reached (every Terra run returned "The usage limit has been reached"; window reset 15:35 GMT), and the parent approved running on Haiku now, per the owner's 2026-11-28 fallback. Pi 1.6.1 headless through `scripts/pi_sandbox.py` (system prompt check passed every run), `-ne -e pi-multiprovider -ns --no-prompt-templates --no-skills`, skills by `--skill` from `cp -rL` copies. Three single-shot runs per arm. Graded from each run's repo (items, `work/order.md`, ideas file, `questions/`, commits, `work_index.py --check`) and session tool calls, not the final reply.

A first fixture used a whitespace bug that was not one (`int()` strips whitespace); a Terra run caught it and filed it as an investigation item. Those runs were discarded and the fixture fixed before the runs below.

## Round 1 (module as first written: rules then a closing "When the filing is committed, run bc-plan-to-pipeline" paragraph)

| Run | Arm | 9 filed | 10 planned | 11 no question | 12 nothing started | 13 check | 14 S1 ideas line |
|-----|-----|---------|------------|----------------|--------------------|----------|------------------|
| old-1 | without | PASS | PASS | PASS | PASS | PASS | PASS |
| old-2 | without | PASS | PASS | PASS | PASS | PASS | PASS |
| old-3 | without | PASS (`Source: bc-find-bugs (…)`) | PASS | PASS | PASS | PASS | FAIL |
| new-1 | with | PASS | **FAIL**: no `Planned:` line; reply says planning is still open | PASS | PASS | PASS (warns unplanned) | PASS |
| new-2 | with | PASS (placed below 005) | PASS | PASS | PASS | PASS | FAIL |
| new-3 | with | PASS | **FAIL**: no `Planned:` line; "the owner should run planning" | PASS | PASS | PASS (warns unplanned) | FAIL |

Every with-arm run read `bc-file-findings/SKILL.md`, then stopped after the filing commit in two of three. The tested `bc-find-bugs` text had the handoff as its own paragraph in the caller; in the module it read as an afterthought to the filing.

Tune: the pipeline section became four numbered steps done in one reply (homes, place and check, commit, plan each filed item, loading `bc-plan-to-pipeline`), opening with "the filing is finished only when every work-planned item you filed has a `Planned:` line", and step 4 names "file them and we're done" alongside "just start it".

## Round 2 (tuned module; with arm only, same fixture, prompt and flags)

| Run | 9 filed | 10 planned | 11 no question | 12 nothing started | 13 check | 14 S1 ideas line |
|-----|---------|------------|----------------|--------------------|----------|------------------|
| new-1 | PASS | PASS | PASS | PASS | PASS | PASS |
| new-2 | PASS | PASS | PASS | PASS | PASS | PASS |
| new-3 | PASS | PASS (separate ideas commit) | PASS | PASS | PASS | PASS |

All three: 006 and 007 in `work/1-planned/` with `Kind: bug`, `Source: find-bugs`, the hunt branch and test name, requirements, a step with its done-criterion and a `Planned:` line; placed below 004 and above 005 in `work/order.md`; S1 one ideas line pointing at the report; `questions/` empty; `dateparse/` and `tests/` unchanged on master; nothing in `2-active/`; `--check` exit 0 with no warnings. Minor in every arm: the `Planned:` date is the fixture's 2026-11-20 rather than the run date in some runs (old-3, new 1–3), a date the model took from the neighbouring items.

## Result

PASS on Haiku low: the tuned module 3/3 on criteria 9–14; the without arm (the inline master text) 3/3 on 9–13 and 2/3 on 14. The scenario cannot show the module beating the inline rule, since the without arm is the rule it replaces; it shows the extraction holds the tested behaviour, after round 1 showed it did not as first worded. Not run on Terra (quota).
