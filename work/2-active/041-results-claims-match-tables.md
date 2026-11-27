# Test status lines match their results tables

Why: In the 2026-11-26 drain, 4 of 10 items had a summary that claimed more than its results table showed: 027 called a comparison run blind, 029 step 1 counted three checks in one run as "3/3", 029 step 2's status contradicted its FAIL grade, 030's "2/3" disagreed with its results file (reflection report in the owner's archive, 2026-11-27).
Done when: The drain's worker packet says to write a concept's `test_status` and log line last, copying counts from the results table and saying whether they count runs or checks; the review standards check that every count in `test_status` appears in the cited results file; both held under a pressure scenario.
Stage: next
Blocked by: nothing
Kind: concept
Source: bc-self-improve reflection on the 2026-11-26 drain
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Requirements

- Worker side: the instructions `bc-pipeline-to-done` gives a build worker (its worker packet) say to write a concept's `test_status` and `.bc-agent/log.md` line last, copying each count from the results table and saying whether it counts runs or checks ("2 of 3 runs", "5 of 5 checks in one run").
- Reviewer side: the Standards review in `bc-code-review` checks that every count and claim in a changed `test_status` or log line appears in the results file it cites, and reports a mismatch as a finding.
- Each clause is one or two sentences with its why; account for `RELATIONSHIPS.md` edges of both concepts.

## Steps

- [ ] Worker-packet clause in `bc-pipeline-to-done` and a reviewer check in `bc-code-review`, with a pressure scenario whose results file and draft status disagree (for example a table with one run of three checks and a draft saying "3/3 runs"). Run on the pressure-test model, without and with each change, dry run where the skill launches subagents. Done when the without-change arm ships the overclaim and the with-change arm does not, or the reviewer catches it; scenario and results in each concept's `tests/`. Out of scope: auditing past status lines (the reflection already listed them); lint checks for counts.

## Outcome
