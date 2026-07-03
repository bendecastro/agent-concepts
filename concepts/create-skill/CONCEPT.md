# create-skill

User-invoked Grok meta-skill: interactively scaffold `SKILL.md` into project `.grok/skills/` or user `~/.grok/skills/`. Grok slash command: `/create-skill`.

## Design decisions

- **Vendored body** in `body/SKILL.md`. CONFIG → Grok via `deploy-grok-skills.py`.
- **Grok-only** — other harnesses use their own skill-authoring flows.

## Provenance

- `raw/grok-user-skills/snapshot/create-skill/SKILL.md`

## Tests

Reference/meta skill — conversational accuracy check only.

## Deploy targets

- **Grok:** `~/.grok/skills/create-skill` → concept `body/`.