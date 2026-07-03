# execute-plan

User-invoked Grok orchestrator: parse a design doc's **PR Plan** DAG, implement PRs in parallel worktree-isolated subagents with mandatory review-fix loops, then assemble a Graphite or plain-git branch stack.

## Design decisions

- **Upstream-maintained body.** Bundled at `~/.grok/bundled/skills/execute-plan/`; couples to Grok worktrees, `grok worktree rm`, and optional `gt`/`gh` stack tooling.
- **Downstream of design-doc-loop.** Expects `## PR Plan` sections produced by `/design`; composes with `/pr-babysit` after stack submission (Graphite mode).
- **Shared memory with implement-loop.** Uses `implement/scripts/memory.py` for past-issue briefing and post-run memory flush (`~/.grok/implement-memory/<workspace-id>.md`).
- **Orchestrator owns git.** Subagents implement in worktrees; parent creates branches, fetches commits via `git fetch <wt> HEAD --no-tags`, and assembles the stack.

## Provenance

- `raw/grok-bundled-skills/snapshot/execute-plan/SKILL.md`
- `raw/grok-bundled-skills/snapshot/execute-plan/scripts/validate-plan.py`
- `raw/grok-bundled-skills/snapshot/shared/personas/implementer.md`
- `raw/grok-bundled-skills/snapshot/shared/personas/reviewer.md`

## Tests

Discipline-enforcing orchestrator. Pressure scenarios not yet authored.

## Deploy targets

- **Grok:** `~/.grok/bundled/skills/execute-plan/` (bundled).
- **Other harnesses:** manual bootstrap.