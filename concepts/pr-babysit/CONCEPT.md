# pr-babysit

User-invoked Grok PR babysitter: watch GitHub PRs, detect CI/review/conflict issues, fix in worktree-isolated subagents; supports Graphite, `gh stack`, and plain git. Grok slash command: `/pr-babysit`.

## Design decisions

- **Vendored body** in `body/SKILL.md`. CONFIG → Grok via `deploy-grok-skills.py`.
- **Never merges PRs** — fixes and substantive replies only.
- **Session state** at `~/.grok/plugin-data/pr-babysit/` (runtime, not in canon).

## Provenance

- `raw/grok-bundled-skills/snapshot/pr-babysit/SKILL.md`

## Tests

Discipline-enforcing orchestrator. Pressure scenarios not yet authored.

## Deploy targets

- **Grok:** `~/.grok/skills/pr-babysit` → concept `body/`.