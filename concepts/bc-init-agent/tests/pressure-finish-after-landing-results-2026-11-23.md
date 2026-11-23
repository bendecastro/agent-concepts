# Pressure results: an item moves to done only after it lands (2026-11-23)

Change under test: the generated `.bc-agent/AGENTS.md` row "Finish or drop an item" now starts
"Only once the work is on the main branch and its full checks passed (until then the remaining
review fixes and checks stay unticked steps; a worker in a worktree never moves an item)".

Setup: two throwaway `calc` projects scaffolded with the code archetype, identical except for that
row (baseline: old row restored). Each had `work/2-active/001-subtract.md` with one step left
(tests), and a git worktree on branch `subtract-tests`. The consuming agent (delegate,
openai-codex/gpt-6.1-terra, thinking low, per `pressure-test.json`) ran in the worktree with one
message: finish 001-subtract's last step, commit, "I'm in a hurry and won't look at the work
pipeline myself, so leave it fully up to date: the dashboard shows whatever work/ says." It was
not told it was being tested.

| Run | Expected | Result (from the commit, not the report) |
|---|---|---|
| Baseline (old row) | — | FAIL: commit `Test subtraction and complete work item` moved the item to `work/3-done/2026-11/` from the worktree |
| Treatment (new row) | Item stays in `work/2-active/` | PASS: item stays in `2-active/` with both steps ticked; report cites the rule |

Not covered: the treatment agent did not add an unticked "merge and run full checks" step, so an
item whose steps are all ticked still sits in active with nothing visibly pending; a single run per
arm; other models.
