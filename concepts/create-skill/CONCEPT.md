# create-skill

User-invoked Grok meta-skill: interactively scaffold a new Agent Skill (`SKILL.md` + optional scripts) into project `.grok/skills/` or user `~/.grok/skills/`.

## Design decisions

- **Upstream-maintained body (user-scope).** Grok-specific paths and frontmatter conventions; reference concept only.
- **Grok-only utility.** Other harnesses have their own skill-authoring flows (Claude `skill-writer`, agents workspace ingest/implement operations).
- **Documents project vs user scope.** Project skills live in `<repo>/.grok/skills/` for teammate sharing; user skills in `~/.grok/skills/`.

## Provenance

- `raw/grok-user-skills/snapshot/create-skill/SKILL.md`

## Tests

Reference/meta skill — conversational accuracy check only.

## Deploy targets

- **Grok:** `~/.grok/skills/create-skill/`.