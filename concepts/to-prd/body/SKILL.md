---
name: to-prd
description: Turn the current conversation into a PRD and publish it as a GitHub issue — no interview, just synthesis of what you've already discussed.
disable-model-invocation: true
---

# To PRD

Draft a PRD from the current conversation and codebase, then publish it as a GitHub issue. The drafting is the `/prd-drafting` discipline; this orchestrator wraps it with publication.

**Issue tracker: GitHub**, via the `gh` CLI. Ready work is published with the `ready-for-agent` label.

## Process

1. **Draft.** Run `/prd-drafting`: synthesize (do NOT interview), sketch and confirm the test seams, and write the PRD to the standard template. If scope is still too vague to synthesize, run `/grill-me` first rather than interviewing here.

2. **Publish** the produced PRD as a GitHub issue:
   ```
   gh issue create --title "<PRD: feature name>" --label ready-for-agent --body-file <path>
   ```
   Apply `ready-for-agent` — no further triage needed. If the `ready-for-agent` label doesn't exist in the repo, create it (`gh label create ready-for-agent`) or ask the user which label to use.
