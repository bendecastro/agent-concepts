# Concept: writing-plans

User-invoked implementation-plan authoring skill for turning an approved spec or resolved requirements into agent-executable, test-first tasks.

## Design decisions

- **Plain plan, not PRD/issue publishing.** Existing `prd-drafting` and `issue-slicing` cover the GitHub pipeline; this concept covers standalone local implementation plans.
- **Agent-ready detail.** The body preserves upstream insistence on exact paths, commands, expected outputs, and code snippets because plans are often executed by fresh agents with no context.
- **No placeholder plans.** Placeholder bans are retained as a gate: a vague plan is worse than no handoff.

## Provenance

- `raw/ingested/obra-superpowers/skills/writing-plans/SKILL.md` — plan structure, task granularity, no-placeholder rule, self-review checklist.
- `raw/ingested/obra-superpowers/skills/writing-plans/plan-document-reviewer-prompt.md` — reviewer mindset referenced but not copied into body.
- `concepts/issue-slicing/` and `concepts/prd-drafting/` — local GitHub-oriented sibling concepts.

## Tests

`tests/scenario.md` — pending pressure run for vague requirements, multi-subsystem specs, placeholder temptation, and execution handoff.

## Deploy targets

Not deployed yet. Discipline-enforcing concept; deploy after pressure test.
