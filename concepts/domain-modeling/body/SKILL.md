---
name: domain-modeling
description: Actively build and sharpen a project's domain model — challenge terms against the glossary, stress-test with edge cases, and update CONTEXT.md and ADRs inline. Use when terminology is vague or a hard design decision needs recording.
---

# Domain Modeling

Actively build and refine the project's domain model. This runs *during* design and grilling — it is not passive note-taking after the fact. A shared language is the payoff: consistent terms make variables, functions, and files self-consistent, make the codebase easier for an agent to navigate, and cut the tokens everyone spends decoding jargon.

## Challenge the language
When the user — or the code — uses a vague or conflicting term, surface the discrepancy *immediately* and propose one precise canonical name. If the glossary already defines a term one way and the user means another, stop and reconcile it rather than letting both meanings run.

## Stress-test with scenarios
Don't accept abstract relationships at face value. Invent concrete edge cases to probe concept boundaries until the meaning is forced to be precise.

## Cross-reference reality
When stated domain logic contradicts how the code actually behaves, flag the contradiction and resolve it — don't paper over it.

## Capture decisions immediately — don't batch
- **`CONTEXT.md`** (repo root) is a **pure glossary**: canonical terms and their meanings, stripped of implementation detail, file paths, or specs. Update it the moment a term crystallizes, not at the end.
- **Multi-context systems:** put a `CONTEXT-MAP.md` at the root pointing to a `CONTEXT.md` inside each bounded context (e.g. `src/ordering/CONTEXT.md`).

## ADRs — a deliberately high bar
Write an Architecture Decision Record under `docs/adr/` only when **all three** hold:
1. the decision is costly to reverse,
2. it would puzzle a future reader without the rationale, and
3. real trade-offs shaped it.

Otherwise skip the ADR and keep moving — not every decision earns one, and a directory full of trivial ADRs is noise that hides the load-bearing ones.
