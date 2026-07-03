# check-work

User-invoked Grok self-verification orchestrator: verifier subagent reviews diffs, runs builds/tests, loops fixes until pass. Grok slash command: `/check-work` (aliases `/check`, `/verify`).

## Design decisions

- **Vendored body** in `body/SKILL.md`. CONFIG → Grok via `deploy-grok-skills.py`.
- **Complements agent-kernel verification** with a concrete subagent loop.

## Provenance

- `raw/grok-user-skills/snapshot/check-work/SKILL.md`

## Tests

Discipline-enforcing. Pressure scenarios not yet authored.

## Deploy targets

- **Grok:** `~/.grok/skills/check-work` → concept `body/`.