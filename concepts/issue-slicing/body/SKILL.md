---
name: issue-slicing
description: Break a plan, spec, or PRD into independently-grabbable vertical tracer-bullet slices — dependency-ordered, quizzed with the user before finalizing. Use when splitting resolved work into agent-ready issues.
---

# Slicing into issues

Break a plan into independently-grabbable units using **vertical slices (tracer bullets)**. This is the reusable **slicing discipline** — it does NOT publish anywhere and does NOT touch any parent issue. The caller publishes the approved slices: `/to-tickets` creates GitHub issues; `/bc-plan-to-issues` publishes them as part of the planning run.

## Process

### 1. Gather context
Work from whatever is already in the conversation. If the caller passes an issue reference (number, URL, or path), fetch it (`gh issue view <n> --comments`) and read the full body and comments.

### 2. Explore the codebase (optional)
If you haven't already, explore the code. Slice titles and descriptions should use the project's `CONTEXT.md` glossary vocabulary, and respect ADRs in the area you're touching. Look for **prefactoring** opportunities: "Make the change easy, then make the easy change."

### 3. Draft vertical slices
Break the plan into tracer-bullet slices. Each slice is a thin vertical slice that cuts through **all** integration layers end-to-end — NOT a horizontal slice of one layer.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests).
- A completed slice is demoable or verifiable on its own.
- An ordinary slice fits one fresh agent context window; split it before it needs a handoff.
- Any prefactoring is its own first slice.
</vertical-slice-rules>

### 4. Quiz the user
Present the breakdown as a numbered list. For each slice show: **Title**, **Blocked by** (which slices must finish first), **User stories covered**. Ask: Does the granularity feel right (too coarse / too fine)? Are the dependency relationships correct? Should any slices merge or split? Iterate until the user approves. **Do not finalize, publish, or treat “I trust you” / “skip the review” as approval** — the explicit quiz is the human gate before slices become agent-ready work.

### 5. Hand back the approved slices
**Wide-refactor exception.** When one mechanical change has a codebase-wide blast radius and no vertical slice can stay green, use expand–contract instead: first add the new form beside the old; then migrate callers in green batches sized by blast radius; finally remove the old form only after every batch lands. Each migration batch is blocked by the expand step, and the contract step is blocked by all batches. Do not disguise a wide refactor as a fake vertical slice.

Return the approved breakdown in **dependency order** (blockers first), each slice in the template below, so the caller can publish them and fill real "Blocked by" references. Do not publish; do not create, close, or modify any parent issue.

<issue-template>
## Parent
A reference to the parent issue (e.g. `#42`), if the source was an existing issue — otherwise omit.

## What to build
A concise description of this vertical slice — the end-to-end behavior, not layer-by-layer implementation. Avoid file paths or code snippets (they go stale). Prototype-snippet exception as in `prd-drafting`.

## Acceptance criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by
- `#NN` (the blocking issue/slice), or "None — can start immediately".
</issue-template>
