# Accuracy check: prd-drafting

Reference/writing discipline — no runtime gate of its own. Verify the body encodes:

1. **Synthesize, not interview.** The body says do NOT interview; if scope is vague it points at `/grill-me`, it does not start grilling.
2. **Seam check before writing.** Step 2 commits to test seams (prefer existing, highest, fewest — ideal one) and confirms them with the user before writing.
3. **Template fidelity.** The `<prd-template>` carries Problem Statement, Solution, a long `As an <actor>, I want <feature>, so that <benefit>` User Stories list, Implementation Decisions, Testing Decisions, Out of Scope, Further Notes.
4. **No stale specifics.** Instructs against file paths / code snippets in the PRD, with the prototype-snippet exception.
5. **No-publish boundary.** The body explicitly does NOT publish; it returns the PRD to the caller.

## Pass criteria
All five present on inspection. Behavior is exercised transitively by the `to-prd` scenario and the `bc-plan-to-issues` pressure test.
