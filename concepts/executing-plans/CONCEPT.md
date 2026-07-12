# Concept: executing-plans

Model-invoked inline executor for a written implementation plan when the user wants the current session to carry out plan tasks with verification checkpoints.

## Design decisions

- **Critical review first.** A plan is not blindly executed; the agent checks for blockers, ambiguity, and unsafe branch state before changing code.
- **Inline fallback.** Existing `bc-drain-issues` is the AFK/GitHub queue executor and `subagent-driven-development` handles fresh-agent task execution; this concept is for direct execution in the current session.
- **Stop on real blockers.** The upstream stop rules are preserved because guessing during plan execution compounds errors.

## Provenance

- `raw/ingested/obra-superpowers/skills/executing-plans/SKILL.md` — load/review/execute/finish sequence and stop rules.
- `concepts/writing-plans/` — sibling concept that creates the plans this executes.
- `concepts/finishing-development-branch/` — completion workflow referenced at the end.

## Tests

`tests/scenario.md` — pending pressure run for ambiguous plan steps, failing verification, main-branch safety, and completion handoff.

## Deploy targets

Not deployed yet. Discipline-enforcing concept; deploy after pressure test.
