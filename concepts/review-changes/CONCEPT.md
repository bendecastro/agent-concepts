# review-changes

User-invoked Grok orchestrator: read-only reviewer subagent for **local** changes, a **branch** diff, or a **GitHub PR** (posts PENDING review). Grok slash command: `/review`.

## Design decisions

- **Vendored body** in `body/SKILL.md`. CONFIG → Grok via `deploy-grok-skills.py`.
- **Distinct from obra [[code-review]]** and [[strict-code-review]].
- **Shared personas** via symlink to [[grok-shared]].

## Provenance

- `raw/grok-bundled-skills/snapshot/review/SKILL.md`

## Tests

Orchestrator with file/PR side effects. Pressure scenarios not yet authored.

## Deploy targets

- **Grok:** `~/.grok/skills/review` → concept `body/`.