# implement-loop

User-invoked Grok orchestrator: **implement → review → fix** with effort-scaled parallel reviewers (1–6), specialization selection, workspace memory (`body/scripts/memory.py`), and no iteration cap until zero open issues. Grok slash command: `/implement`.

## Design decisions

- **Vendored body** in `body/SKILL.md`, `body/scripts/memory.py`, `body/tests/test_memory.py`. CONFIG → Grok via `deploy-grok-skills.py`.
- **Distinct from obra subagent-driven-development** — standalone feature builder with multi-reviewer scaling, not a pre-written plan executor.
- **`disable-model-invocation: true`** — user-invoked only.
- **Shared personas** via symlink to [[grok-shared]].

## Provenance

- `raw/grok-bundled-skills/snapshot/implement/SKILL.md`
- `raw/grok-bundled-skills/snapshot/implement/scripts/memory.py`

## Tests

Discipline-enforcing orchestrator. Pressure scenarios not yet authored.

## Deploy targets

- **Grok:** `~/.grok/skills/implement` → concept `body/`.