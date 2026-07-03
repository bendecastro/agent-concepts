# strict-code-review

User-invoked **harsh maintainability audit** skill: push reviewers toward "code judo" simplification, anti-spaghetti branching rules, 1k-line file guardrails, and a high approval bar — separate from obra [[code-review]] (request/receive discipline) and [[review-changes]] (Grok review orchestrator).

## Design decisions

- **Vendored body.** Unlike bundled Grok workflow skills, this user-scope skill (`~/.grok/skills/code-review/`) may be locally tuned; canon lives here so edits survive Grok reinstalls and sync across machines via CONFIG.
- **`disable-model-invocation: true`.** Explicit user invocation only — appropriate for an unusually strict audit that should not fire on routine tasks.
- **No subagent orchestration.** Single reviewer prompt + standards; harness runs the review inline or dispatches one reviewer subagent per harness convention.
- **Dual Grok symlinks.** Both `~/.grok/skills/code-review` and `~/.grok/skills/strict-code-review` point at this body; frontmatter `name: code-review` keeps `/code-review` as the slash command.

## Provenance

- `raw/grok-user-skills/snapshot/code-review/SKILL.md` — snapshotted 2026-07-03.

## Tests

Discipline-enforcing (approval bar, structural findings prioritized). Pressure scenario: rubber-stamp "it works" implementation — not yet authored.

## Deploy targets

- **Grok:** `scripts/deploy-grok-skills.py` (2026-07-03) — `code-review` + `strict-code-review` → concept `body/`.
- **Claude Code / Pi:** `deploy-local-skills.py` when cross-harness strict audits are wanted.