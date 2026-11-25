---
name: bc-plan-slicing
description: Break a plan, spec, or PRD into independently-grabbable vertical tracer-bullet slices — dependency-ordered and finalized by the agent without waiting for human approval. Use when splitting resolved work into agent-ready tickets.
---

# Slicing into tickets

Break a plan into independently-grabbable units using **vertical slices (tracer bullets)**. This is the reusable **slicing discipline** — it does NOT publish anywhere and does NOT touch any parent ticket. The caller publishes the final slices: `/bc-to-tickets` creates GitHub issues; `/bc-plan-to-pipeline` publishes them as part of the planning run.

## Process

### 1. Gather context
Work from whatever is already in the conversation. If the caller passes a ticket reference (number, URL, or path), fetch it (`gh issue view <n> --comments`) and read the full body and comments.

### 2. Explore the codebase (optional)
If you haven't already, explore the code. Slice titles and descriptions should use the project's `glossary.md` glossary vocabulary, and respect ADRs in the area you're touching. Look for **prefactoring** opportunities: "Make the change easy, then make the easy change."

### 3. Draft vertical slices
Break the plan into tracer-bullet slices. Each slice is a thin vertical slice that cuts through **all** integration layers end-to-end — NOT a horizontal slice of one layer.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests).
- A completed slice is demoable or verifiable on its own.
- An ordinary slice fits one fresh agent context window; split it before it needs a handoff.
- Size for the executor's whole ticket lifecycle, not implementation alone: consider audit + build + independent review + likely rework and explain fit in qualitative scope/risk terms. When risk or interaction breadth makes an end-to-end slice implausible to verify and rework safely, split at independently verifiable behavior boundaries; never hand back work you judge unsafe to verify and rework as one slice as agent-ready. This is a sizing judgment, not a numeric drain-readiness gate: child-token totals and former token thresholds do not determine whether work is drain-ready. Do not invent per-slice token estimates; classify fit qualitatively from scope, compatibility surface, external semantics, migration risk, and likely rework.
- Any prefactoring is its own first slice.
</vertical-slice-rules>

### 4. Check the breakdown yourself, then finalize
Do not stop to ask the user to approve the slices; the owner trusts the agent's slicing, so no human gate sits here. Review the draft yourself before finalizing: Is the granularity right (too coarse / too fine)? Are the dependency relationships correct? Should any slices merge or split? Revise until the answers hold, then finalize and continue.

Show the final breakdown in your reply so the user can see what was decided — for each slice: **Title**, **Blocked by** (which slices must finish first), **User stories covered**, and **Lifecycle fit** (a brief qualitative scope/risk reason; never an invented token estimate). This is a report, not a question: do not wait for an answer.

Exception: when the user asked in this request to review the slices before they are finalized, present them as a numbered **draft** and wait for approval.

### 5. Hand back the final slices
**Wide-refactor exception.** When one mechanical change has a codebase-wide blast radius and no vertical slice can stay green, use expand–contract instead: first add the new form beside the old; then migrate callers in green batches sized by blast radius; finally remove the old form only after every batch lands. Each migration batch is blocked by the expand step, and the contract step is blocked by all batches. Do not disguise a wide refactor as a fake vertical slice.

Return the final breakdown in **dependency order** (blockers first), each slice in the template below, so the caller can publish them and fill real "Blocked by" references. Do not publish; do not create, close, or modify any parent ticket.

<ticket-template>
## Parent
A reference to the parent ticket (e.g. `#42`), if the source was an existing ticket — otherwise omit.

## What to build
A concise description of this vertical slice — the end-to-end behavior, not layer-by-layer implementation. Avoid file paths or code snippets (they go stale). Prototype-snippet exception as in `bc-prd-drafting`.

## Acceptance criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by
- `#NN` (the blocking ticket/slice), or "None — can start immediately".
</ticket-template>

For glossary discovery in legacy projects, follow `bc-domain-modeling`’s legacy glossary rule.
