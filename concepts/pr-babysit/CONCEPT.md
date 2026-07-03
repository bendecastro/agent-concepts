# pr-babysit

User-invoked Grok PR babysitter: watch GitHub PRs (standalone, Graphite stacks, or `gh stack` chains), detect CI/review/conflict issues, fix autonomously in worktree-isolated subagents, cap fixes per cycle, compose with `/loop` for polling.

## Design decisions

- **Upstream-maintained body.** Bundled at `~/.grok/bundled/skills/pr-babysit/`; heavy `gh` GraphQL/API usage and Grok scheduler integration.
- **Never merges PRs.** Fixes and substantive replies only; merging stays human.
- **Session-scoped state.** `~/.grok/plugin-data/pr-babysit/watched-prs-<INSTANCE_ID>.json` — not shared across Grok sessions.
- **Plain-git stacks lack babysit handoff.** execute-plan's plain-git mode explicitly does not chain here (stack walking depends on `gt`).

## Provenance

- `raw/grok-bundled-skills/snapshot/pr-babysit/SKILL.md`

## Tests

Discipline-enforcing orchestrator (fix cap, no platitude replies, every thread evaluated). Pressure scenarios not yet authored.

## Deploy targets

- **Grok:** `~/.grok/bundled/skills/pr-babysit/` (bundled).
- **Other harnesses:** manual bootstrap; requires `gh` auth and likely substantial tool mapping.