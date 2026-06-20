---
name: to-issues
description: Break a plan, spec, or PRD into independently-grabbable GitHub issues using tracer-bullet vertical slices.
disable-model-invocation: true
---

# To Issues

Break a plan into independently-grabbable issues using **vertical slices (tracer bullets)**.

**Issue tracker: GitHub**, via the `gh` CLI. Slices that are ready for an agent to grab are published with the `ready-for-agent` label.

## Process

### 1. Gather context
Work from whatever is already in the conversation. If the user passes an issue reference (number, URL, or path), fetch it (`gh issue view <n> --comments`) and read the full body and comments.

### 2. Explore the codebase (optional)
If you haven't already, explore the code. Issue titles and descriptions should use the project's `CONTEXT.md` glossary vocabulary, and respect ADRs in the area you're touching. Look for **prefactoring** opportunities: "Make the change easy, then make the easy change."

### 3. Draft vertical slices
Break the plan into tracer-bullet issues. Each issue is a thin vertical slice that cuts through **all** integration layers end-to-end — NOT a horizontal slice of one layer.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests).
- A completed slice is demoable or verifiable on its own.
- Any prefactoring is its own first slice.
</vertical-slice-rules>

### 4. Quiz the user
Present the breakdown as a numbered list. For each slice show: **Title**, **Blocked by** (which slices must finish first), **User stories covered**. Ask: Does the granularity feel right (too coarse / too fine)? Are the dependency relationships correct? Should any slices merge or split? Iterate until the user approves.

### 5. Publish to GitHub
For each approved slice, publish a GitHub issue with the body template below, **in dependency order** (blockers first) so you can reference real issue numbers in "Blocked by":
```
gh issue create --title "<slice title>" --label ready-for-agent --body-file <path>
```
Publish with `ready-for-agent` unless instructed otherwise. **Do NOT close or modify any parent issue.**

<issue-template>
## Parent
A reference to the parent issue (e.g. `#42`), if the source was an existing issue — otherwise omit.

## What to build
A concise description of this vertical slice — the end-to-end behavior, not layer-by-layer implementation. Avoid file paths or code snippets (they go stale). Prototype-snippet exception as in `to-prd`.

## Acceptance criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by
- `#NN` (the blocking issue), or "None — can start immediately".
</issue-template>
