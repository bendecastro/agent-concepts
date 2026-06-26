---
name: to-prd
description: Turn the current conversation into a PRD and publish it as a GitHub issue — no interview, just synthesis of what you've already discussed.
disable-model-invocation: true
---

# To PRD

Draft a PRD from the current conversation and codebase, then publish it as a GitHub issue. The drafting is the `/prd-drafting` discipline; this orchestrator wraps it with publication.

**Issue tracker: GitHub**, via the `gh` CLI. A PRD parent issue is a planning/coordination artifact, not drainable work; `ready-for-agent` is reserved for implementation slices created by `/to-issues` or `/bc-plan-to-issues`.

## Process

1. **Draft.** Run `/prd-drafting`: synthesize (do NOT interview), sketch and confirm the test seams, and write the PRD to the standard template. If scope is still too vague to synthesize, run `/grill-me` first rather than interviewing here.

2. **Publish** the produced PRD as a GitHub parent issue:
   ```
   gh issue create --title "<PRD: feature name>" --body-file <path>
   ```
   Do **not** apply `ready-for-agent` to the PRD parent. Run `/to-issues` or `/bc-plan-to-issues` to create drainable `ready-for-agent` implementation slices.
