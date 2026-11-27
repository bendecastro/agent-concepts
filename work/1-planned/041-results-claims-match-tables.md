# Test status lines match their results tables

Why: In the 2026-11-26 drain, 4 of 10 items had a summary that claimed more than its results table showed: 027 called a comparison run blind, 029 step 1 counted three checks in one run as "3/3", 029 step 2's status contradicted its FAIL grade, 030's "2/3" disagreed with its results file (reflection report in the owner's archive, 2026-11-27).
Done when: The drain's worker packet says to write a concept's `test_status` and log line last, copying counts from the results table and saying whether they count runs or checks; the review standards check that every count in `test_status` appears in the cited results file; both held under a pressure scenario.
Stage: next
Blocked by: nothing
Kind: concept
Source: bc-self-improve reflection on the 2026-11-26 drain

## Steps

- [ ] Worker-packet clause in `bc-pipeline-to-done` and a reviewer check in `bc-code-review`, with a pressure scenario whose results file and draft status disagree. Done when the scenario's without-change arm ships the overclaim and the with-change arm does not, or the reviewer catches it.

## Outcome
