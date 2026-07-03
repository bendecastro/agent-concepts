# execute-plan

User-invoked Grok orchestrator: parse a design doc's **PR Plan** DAG, implement PRs in parallel worktree-isolated subagents with mandatory review-fix loops, then assemble a Graphite or plain-git branch stack.

## Design decisions

- **Vendored body** in `body/SKILL.md` + `body/scripts/validate-plan.py`. CONFIG → Grok via `deploy-grok-skills.py`.
- **Downstream of design-doc-loop.** Expects `## PR Plan` from `/design`; composes with `/pr-babysit` after Graphite stack submit.
- **Shared memory with implement-loop.** Uses `implement-loop/body/scripts/memory.py` at runtime (path announced in skill); memory file under `~/.grok/implement-memory/`.
- **Shared personas** via symlink to [[grok-shared]].

## Provenance

- `raw/grok-bundled-skills/snapshot/execute-plan/SKILL.md`
- `raw/grok-bundled-skills/snapshot/execute-plan/scripts/validate-plan.py`

## Tests

Discipline-enforcing orchestrator. Pressure scenarios not yet authored.

## Deploy targets

- **Grok:** `~/.grok/skills/execute-plan` → concept `body/`.