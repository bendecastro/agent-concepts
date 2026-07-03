# design-doc-loop

User-invoked Grok orchestrator: writer/reviewer subagent loop until a design document reaches zero open review issues, with mandatory **PR Plan** and **Key Decisions** sections. Grok slash command: `/design`.

## Design decisions

- **Vendored body.** Canon lives in `body/SKILL.md`; ingested from xAI's bundled skill snapshot. Edit here, deploy to Grok via `scripts/deploy-grok-skills.py` — CONFIG is source, Grok is consumer.
- **Grok-first tooling.** Assumes `spawn_subagent`, persona prompt injection, and temp artifact paths; porting to other harnesses needs tool mapping.
- **Shared personas.** `shared/` symlinks to [[grok-shared]] so `../shared/personas/` resolves from `body/SKILL.md`.

## Provenance

- `raw/grok-bundled-skills/snapshot/design/SKILL.md`
- `raw/grok-bundled-skills/snapshot/shared/personas/design-doc-writer.md`
- `raw/grok-bundled-skills/snapshot/shared/personas/design-doc-reviewer.md`

## Tests

Discipline-enforcing orchestrator (no iteration cap, stalemate escalation). Pressure scenarios not yet authored.

## Deploy targets

- **Grok:** `~/.grok/skills/design` → concept `body/` (via `deploy-grok-skills.py`).