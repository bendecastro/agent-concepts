# Scenario: to-issues

Run a subagent with `body/SKILL.md` loaded, given a short multi-feature plan/PRD, in a throwaway git repo. Grade by the proposed breakdown and the (dry-run or stubbed) `gh` invocations. The slicing behavior itself is owned by `issue-slicing` (see its scenario); this scenario checks the orchestrator delegates to it and publishes correctly.

## Checks

1. **Delegates slicing.** Runs `/issue-slicing` for the breakdown rather than inventing its own slicing process — and the resulting slices are vertical, not horizontal (spot-check against the `issue-slicing` scenario).
2. **Quiz happened before publish.** No issues are created until the user has approved the breakdown (the quiz is inside `issue-slicing`).
3. **Dependency-ordered publish.** Issues created blockers-first via `gh issue create --label ready-for-agent`, with "Blocked by" referencing real `#NN` numbers.
4. **No-touch-parent.** Does not close or modify the source/parent issue.

## Pass criteria
All four hold on inspection of the breakdown and publish commands.
