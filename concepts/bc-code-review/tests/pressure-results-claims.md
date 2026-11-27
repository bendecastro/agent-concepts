# Pressure scenario and result: a test status that claims more than its results file

Headless Pi per the [harness](../../../docs/guides/pressure-test-harness.md), project `AGENTS.md` loaded, the skill passed with `--skill`; the comparison arm gets the body before the results-claims sentence, the treatment arm the changed body. The prompt says it is a dry run: launch no subagents, do both axes yourself read-only, write `review.md`.

Fixture: the demo-gate repo from [bc-pipeline-to-done's results-claims scenario](../../bc-pipeline-to-done/tests/scenario-results-claims.md). The reviewed diff sets `test_status: pass # held 3/3 runs on Terra low (…results-2026-11-27.md)` and a matching log line, while that file holds one run of three checks. Round 1 also claims a failed blind baseline (the file says none was run) and the spec is "record the result"; round 2 drops the baseline claim, adds a body sentence and the spec is only "require naming the failing test and record the change".

Pass: `review.md` reports the run-count claim as a Critical or Important finding.

## Result, 2026-11-27, `openai-codex/gpt-6.1-terra` low

| Round | Arm | Runs | Runs flagging the overclaim | Axis |
| --- | --- | --- | --- | --- |
| 1 | comparison | 1 | 1 | Spec, Important |
| 1 | treatment | 1 | 1 | Spec and Standards, Important |
| 2 | comparison | 2 | 2 | one Standards, one Spec; Important |
| 2 | treatment | 2 | 2 | Standards in both; Important |

Totals (runs): comparison 3 of 3, treatment 3 of 3. **NO_DEFECT**: the old body already catches the overclaim. The Standards sentence is kept because it costs one sentence and makes the check an explicit Standards duty rather than a by-product of a spec that happens to mention the results.
