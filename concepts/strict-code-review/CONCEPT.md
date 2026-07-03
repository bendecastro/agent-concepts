# strict-code-review

User-invoked **harsh maintainability audit** skill: push reviewers toward "code judo" simplification, anti-spaghetti branching rules, 1k-line file guardrails, and a high approval bar — separate from obra [[code-review]] (request/receive discipline) and [[review-changes]] (Grok review orchestrator).

## Design decisions

- **Vendored body.** Unlike bundled Grok workflow skills, this user-scope skill (`~/.grok/skills/code-review/`) may be locally tuned; canon lives here so edits survive Grok reinstalls and sync across machines via CONFIG.
- **`disable-model-invocation: true`.** Explicit user invocation only — appropriate for an unusually strict audit that should not fire on routine tasks.
- **No subagent orchestration.** Single reviewer prompt + standards; harness runs the review inline or dispatches one reviewer subagent per harness convention.
- **Deploy to Grok via symlink** (optional): `~/.grok/skills/strict-code-review` → concept body, or keep the upstream skill name `code-review` if the user prefers that slash command — document both in harnesses.

## Provenance

- `raw/grok-user-skills/snapshot/code-review/SKILL.md` — snapshotted 2026-07-03.

## Tests

Discipline-enforcing (approval bar, structural findings prioritized). Pressure scenario: rubber-stamp "it works" implementation — not yet authored.

## Deploy targets

- **Grok:** live at `~/.grok/skills/code-review/` today; optional symlink rename to `strict-code-review` if we want name alignment.
- **Claude Code / Pi:** symlink `concepts/strict-code-review/body` when user wants cross-harness strict audits.