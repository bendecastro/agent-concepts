# Scenario: to-issues

Run a subagent with `body/SKILL.md` loaded, given a short multi-feature plan/PRD, in a throwaway git repo. Grade by the proposed breakdown and the (dry-run or stubbed) `gh` invocations.

## Checks

1. **Vertical slices.** Each proposed issue cuts end-to-end through the layers and is independently demoable/verifiable — NOT "do all the schema", "do all the API". Attack: push for a layer-by-layer breakdown; expected refusal in favor of vertical slices.
2. **Prefactor first.** Any prefactoring is called out as its own first slice.
3. **Quiz before publish.** Presents a numbered breakdown (Title / Blocked by / User stories) and asks about granularity + dependencies; iterates to approval before creating anything.
4. **Dependency-ordered publish.** Issues created blockers-first via `gh issue create --label ready-for-agent`, with "Blocked by" referencing real `#NN` numbers.
5. **No-touch-parent.** Does not close or modify the source/parent issue.

## Pass criteria
All five hold on inspection of the breakdown and publish commands.
