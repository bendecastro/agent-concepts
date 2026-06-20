---
name: prd-drafting
description: Draft a PRD from the current conversation and codebase — synthesize (don't interview), sketch the test seams, and write it to the standard template. Use when turning an already-resolved plan into a structured PRD document.
---

# Drafting a PRD

Produce a PRD from what's already been discussed plus the codebase. This is the reusable **writing discipline** — it does NOT publish anywhere. The caller decides where the PRD lands: `/to-prd` publishes it as a GitHub issue; `/bc-plan-to-issues` carries it straight into slicing; a human might paste it into a wiki.

**Do NOT interview the user** — synthesize what you already know. (If the scope is still vague, that's a sign to run `/grill-me` first, not to start interviewing here.)

## Process

1. **Explore the repo** to understand current state (if you haven't already). Use the project's `CONTEXT.md` glossary vocabulary throughout the PRD, and respect any ADRs in the area you're touching.

2. **Sketch the seams** at which you'll test the feature. Prefer existing seams to new ones; use the highest seam possible; the fewer seams the better — the ideal is one. If new seams are needed, propose them at the highest point you can. Check with the user that these seams match their expectations before writing the PRD. (Run `/codebase-design` if you need the deep-module / seam vocabulary.)

3. **Write the PRD** using the template below. Return it to the caller — do not publish it yourself.

<prd-template>
## Problem Statement
The problem the user faces, from the user's perspective.

## Solution
The solution, from the user's perspective.

## User Stories
A LONG, numbered list. Each: `As an <actor>, I want <feature>, so that <benefit>`. Be extensive — cover all aspects of the feature.

## Implementation Decisions
Modules built/modified and their interfaces; technical clarifications; architectural decisions; schema changes; API contracts; specific interactions. Do NOT include specific file paths or code snippets (they go stale fast). Exception: a prototype-derived snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape) — inline just the decision-rich part and note it came from a prototype.

## Testing Decisions
What makes a good test (test external behavior, not implementation detail); which modules will be tested; prior art for the tests in the codebase.

## Out of Scope
What's explicitly out of scope for this PRD.

## Further Notes
Anything else worth recording.
</prd-template>
