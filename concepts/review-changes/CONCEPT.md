# review-changes

User-invoked Grok orchestrator: run a read-only reviewer subagent against **local** uncommitted changes (default), a **branch** diff vs merge-base, or a **GitHub PR** (posts a PENDING review for UI submit).

## Design decisions

- **Upstream-maintained body.** Bundled at `~/.grok/bundled/skills/review/` — distinct from obra [[code-review]] (request/receive discipline) and from [[strict-code-review]] (harsh maintainability audit prompts).
- **Three modes with deterministic arg parsing.** `--local`, `--branch`, `--pr`, plus auto-detect for URLs/`#123`/branch names.
- **PR mode posts PENDING only.** Orchestrator never sets review `event`; user submits via GitHub Files tab. Inline comments filtered to diff-visible lines.
- **Artifacts in /tmp.** Local/branch modes deliver `review_file` + `summary_file`; PR mode cleans up on success.

## Provenance

- `raw/grok-bundled-skills/snapshot/review/SKILL.md`
- `raw/grok-bundled-skills/snapshot/shared/personas/reviewer.md`

## Tests

Orchestrator with file/PR side effects. Pressure scenarios not yet authored.

## Deploy targets

- **Grok:** `~/.grok/bundled/skills/review/` (bundled).
- **Other harnesses:** manual bootstrap.