# Scenario: to-spec

Run a subagent with `body/SKILL.md` loaded, after a short fictional conversation that already discussed a feature, in a throwaway git repo. Grade by the produced PRD text and the (dry-run or stubbed) `gh` invocation. The PRD-writing behavior itself is owned by `prd-drafting` (see its accuracy check); this scenario checks the orchestrator delegates to it and publishes correctly.

## Checks

1. **Delegates drafting.** Runs `/prd-drafting` to produce the PRD rather than inventing its own process — synthesizes (no interview), and the PRD follows the standard template (Problem / Solution / User Stories / Implementation / Testing / Out of Scope / Further Notes).
2. **No interview.** The agent does NOT start grilling-style questioning. If it judges scope too vague, it says "run `/grill-me` first".
3. **Publish.** Ends with `gh issue create --title ... --body-file ...` for an unlabeled PRD parent issue; it does not apply `ready-for-agent`.

## Pass criteria
All three hold on inspection of the PRD and the publish command.

## Historical run — 2026-06-21 (then named `to-prd`; Claude Code subagent, Haiku low-thinking per cost rule) — **PASS**

Sandbox `/tmp/pt-toprd`; `gh` stubbed; settled CSV-export context supplied as prior conversation.
1. Delegated to `prd-drafting` and produced a template-conformant PRD (Problem / Solution / User Stories / Implementation / Testing / Out of Scope / Further Notes). ✓
2. No interview/grilling — synthesized from the settled context. ✓
3. Ended with `gh issue create --title ... --label ready-for-agent --body-file ...`. ✓ (Historical run before the 2026-06-26 parent-PRD label correction; rerun pending.)
