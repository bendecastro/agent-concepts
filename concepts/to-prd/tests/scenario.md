# Scenario: to-prd

Run a subagent with `body/SKILL.md` loaded, after a short fictional conversation that already discussed a feature, in a throwaway git repo. Grade by the produced PRD text and the (dry-run or stubbed) `gh` invocation.

## Checks

1. **No interview.** The agent synthesizes from the conversation; it does NOT start asking grilling-style questions. (If it judges scope too vague, it should say "run `/grill-me` first", not interview.)
2. **Seam check before writing.** The agent proposes test seams (prefers existing, highest, fewest) and confirms them with the user before writing the PRD.
3. **Template fidelity.** PRD contains Problem Statement, Solution, a long User Stories list in `As an <actor>, I want <feature>, so that <benefit>` form, Implementation Decisions, Testing Decisions, Out of Scope, Further Notes.
4. **No stale specifics.** No file paths or code snippets in the PRD (except a flagged prototype-derived decision snippet, if any).
5. **Publish.** Ends with `gh issue create --title ... --label ready-for-agent --body-file ...` (or asks which label if `ready-for-agent` is absent).

## Pass criteria
All five hold on inspection of the PRD and the publish command.
