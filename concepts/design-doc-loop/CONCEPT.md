# design-doc-loop

User-invoked Grok orchestrator: writer/reviewer subagent loop until a design document reaches zero open review issues, with mandatory **PR Plan** and **Key Decisions** sections.

## Design decisions

- **Upstream-maintained body (no vendored copy).** Like [[omarchy]] and [[notebooklm]], the SKILL.md lives in xAI's bundled directory and updates with Grok. Vendoring would fork a fast-moving orchestrator tied to Grok tool names.
- **Grok-first, document for porting.** Canonical deploy is Grok's bundled skill discovery. Other harnesses should read the snapshot in `raw/grok-bundled-skills/` and map `spawn_subagent` + persona injection to their subagent APIs.
- **Personas are part of the contract.** `design-doc-writer` and `design-doc-reviewer` persona files ship beside the skill under `shared/personas/`; orchestrator prepends them to prompts (no `persona` spawn parameter).

## Provenance

- `raw/grok-bundled-skills/snapshot/design/SKILL.md`
- `raw/grok-bundled-skills/snapshot/shared/personas/design-doc-writer.md`
- `raw/grok-bundled-skills/snapshot/shared/personas/design-doc-reviewer.md`

## Tests

Discipline-enforcing orchestrator (no iteration cap, stalemate escalation). Pressure scenarios not yet authored — Grok harness required for meaningful run.

## Deploy targets

- **Grok:** `~/.grok/bundled/skills/design/` (bundled; auto-discovered).
- **Other harnesses:** manual bootstrap — read bundled SKILL.md + personas for the session.