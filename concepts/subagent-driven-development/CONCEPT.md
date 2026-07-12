# Concept: subagent-driven-development

User-invoked plan execution pattern where a controller dispatches fresh implementer/reviewer agents per task, maintains context, and integrates only after spec and quality review.

## Design decisions

- **Controller-owned context.** The body keeps the upstream rule that subagents receive curated task text, not the whole parent session.
- **Sequential implementation, review loop.** Implementers are not parallelized by default because plan tasks often touch shared state; review may be delegated but integration remains parent-owned.
- **Harness-neutral templates.** Upstream prompt files are summarized into packet contracts instead of copied verbatim so Pi/Claude/Codex can each use their native subagent mechanism.

## Provenance

- `raw/ingested/obra-superpowers/skills/subagent-driven-development/SKILL.md` — fresh subagent per task, status handling, spec-review then quality-review loop.
- `raw/ingested/obra-superpowers/skills/subagent-driven-development/implementer-prompt.md` — implementer packet and status contract.
- `raw/ingested/obra-superpowers/skills/subagent-driven-development/spec-reviewer-prompt.md` and `code-quality-reviewer-prompt.md` — two-stage review model.
- `concepts/dispatching-parallel-agents/` — related but for independent parallel domains, not sequential plan tasks.

## Tests

`tests/scenario.md` — pending pressure run for skipped review, parallel implementer temptation, broad plan-file handoff, and blocked-subagent handling.

## Deploy targets

Not deployed yet. Discipline-enforcing orchestration concept; deploy after pressure test.
