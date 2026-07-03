# grok-shared

Shared persona files consumed by Grok workflow skills via `../shared/personas/` relative to each skill's `body/SKILL.md`.

## Design decisions

- **Not a runtime skill.** No `body/SKILL.md`; Grok discovers personas through sibling `shared/` symlinks on workflow concepts and through `~/.grok/skills/shared` deploy.
- **Single canon copy.** Personas are vendored once here; `design-doc-loop`, `execute-plan`, `implement-loop`, and `review-changes` symlink `shared/` → `../grok-shared/shared` so upstream path conventions still resolve.

## Provenance

- `raw/grok-bundled-skills/snapshot/shared/personas/` — snapshotted 2026-07-03.

## Tests

Support concept (persona library, not a runtime skill). No pressure scenarios.

## Deploy targets

- **Grok:** `scripts/deploy-grok-skills.py` links `~/.grok/skills/shared` → `concepts/grok-shared/shared`.