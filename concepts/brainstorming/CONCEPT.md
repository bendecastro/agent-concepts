# Concept: brainstorming

User-invoked collaborative design step for turning a rough idea into an approved, scoped design before implementation planning.

## Design decisions

- **Softer than upstream default.** Upstream says use before every creative/code change; this port narrows invocation to genuinely unresolved design or behavior changes, because local agent-kernel favors acting directly on clear tasks.
- **One-question discipline.** Keeps upstream one-question-at-a-time interview and alternatives-with-recommendation pattern.
- **Design feeds planning.** This concept stops at an approved design/spec and hands off to `writing-plans`, `prd-drafting`, or `bc-plan-to-issues`; it does not implement.
- **Visual companion omitted.** Upstream browser companion scripts are filed as provenance but not ported until there is a local tool path worth maintaining.

## Provenance

- `raw/obra-superpowers/skills/brainstorming/SKILL.md` — design gate, context exploration, alternatives, spec review, handoff.
- `raw/obra-superpowers/skills/brainstorming/visual-companion.md` and `scripts/` — upstream visual companion, not ported.
- `concepts/grilling/`, `concepts/prototype/`, `concepts/bc-plan-to-issues/` — local adjacent planning skills.

## Tests

`tests/scenario.md` — pending pressure run for premature implementation, over-broad project decomposition, one-question discipline, and handoff.

## Deploy targets

Not deployed yet. Discipline-enforcing planning concept; deploy after pressure test.
