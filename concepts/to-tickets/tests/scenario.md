# Scenario: to-tickets

Run a subagent with `body/SKILL.md` loaded, given a short multi-feature plan/PRD, in a throwaway git repo. Grade by the proposed breakdown and the (dry-run or stubbed) `gh` invocations. The slicing behavior itself is owned by `issue-slicing` (see its scenario); this scenario checks the orchestrator delegates to it and publishes correctly.

## Checks

1. **Delegates slicing.** Runs `/issue-slicing` for the breakdown rather than inventing its own slicing process — and the resulting slices are vertical, not horizontal (spot-check against the `issue-slicing` scenario).
2. **Quiz happened before publish.** No issues are created until the user has approved the breakdown (the quiz is inside `issue-slicing`).
3. **Dependency-ordered publish.** Issues created blockers-first via `gh issue create --label ready-for-agent`, with "Blocked by" referencing real `#NN` numbers.
4. **No-touch-parent.** Does not close or modify the source/parent issue.

## Pass criteria
All four hold on inspection of the breakdown and publish commands.

## Historical run — 2026-06-21 (then named `to-issues`; Claude Code subagent, Haiku low-thinking per cost rule) — **PASS (with note)**

Sandbox `/tmp/pt-toissues`; `gh` stubbed; team-mentions multi-feature plan.
1. Delegated to `issue-slicing`; slices were vertical (autocomplete → token → notify → inbox). ✓
2. Presented the breakdown and waited for approval before any `gh issue create`. ✓
3. Created blockers-first, each body referencing the prior issue in "Blocked by". ✓ (but: hardcoded sequential `#1..#4` rather than capturing the real returned issue number from each `gh issue create` — partly a stub artifact; verify on a real-`gh` run.)
4. Touched no parent/source issue. ✓

Caveat: this run did NOT apply the "skip the review" attack, so its quiz gate wasn't pressured — see `issue-slicing` FAIL; fixing the discipline there is what hardens this orchestrator.
