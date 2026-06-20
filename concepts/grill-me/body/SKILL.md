---
name: grill-me
description: Get relentlessly interviewed about a plan or design until every decision is resolved, capturing the shared vocabulary and hard decisions in durable project docs as you go.
disable-model-invocation: true
argument-hint: "What are we planning?"
---

# Grill Me (stateful)

Run a relentless grilling session — and **persist what it produces**, so the next session starts from shared understanding instead of re-litigating it. This is the always-stateful grill: every run should leave `CONTEXT.md` and any ADRs better than it found them.

1. **Grill.** Run the `/grilling` loop: interview the user one question at a time, recommended-answer-first, down every branch of the decision tree. Read the codebase to answer questions you can answer yourself rather than asking.

2. **Persist inline — don't batch.** As decisions and terminology crystallize *during* the interview, run `/domain-modeling`:
   - Sharpen vague or conflicting terms into one canonical name, and record them in `CONTEXT.md` (a pure glossary at the repo root — no implementation detail).
   - When a decision is costly to reverse, would surprise a future reader, and reflects a real trade-off, write an ADR under `docs/adr/` (numbered `NNNN-dash-case-title.md`).

3. **Close out.** Restate the resolved scope, and point at the exact files you wrote or updated.

**Guard:** if the current directory isn't a project where `CONTEXT.md`/ADRs belong (empty scratch dir, unrelated files), confirm with the user before creating docs, or grill without persisting. If the user explicitly wants a throwaway no-files session, honor that; otherwise persist by default.
