# implement-loop

User-invoked Grok orchestrator: **implement → review → fix** loop with effort-scaled parallel reviewers (1–6), specialization selection (general/tests/security/plan-alignment), workspace memory briefing, and no iteration cap until zero open issues.

## Design decisions

- **Upstream-maintained body.** Bundled at `~/.grok/bundled/skills/implement/`; includes `scripts/memory.py` for cross-run pattern memory (shared with execute-plan).
- **Distinct from obra subagent-driven-development.** obra's skill executes a pre-written plan with spec/code review gates; this skill is a standalone feature builder with multi-reviewer scaling and memory — closer to a Grok-native "ship this feature" loop.
- **`disable-model-invocation: true` upstream.** User must invoke `/implement`; not auto-loaded as model-invoked discipline.
- **Anti-hallucination tool-call discipline.** Body explicitly requires `spawn_subagent` calls before any "launching" narration — worth preserving if porting.

## Provenance

- `raw/grok-bundled-skills/snapshot/implement/SKILL.md`
- `raw/grok-bundled-skills/snapshot/implement/scripts/memory.py`
- `raw/grok-bundled-skills/snapshot/shared/personas/implementer.md`
- `raw/grok-bundled-skills/snapshot/shared/personas/reviewer.md`
- `raw/grok-bundled-skills/snapshot/shared/personas/security-auditor.md`

## Tests

Discipline-enforcing orchestrator. Pressure scenarios not yet authored.

## Deploy targets

- **Grok:** `~/.grok/bundled/skills/implement/` (bundled).
- **Other harnesses:** manual bootstrap; memory helper requires Python 3 + git workspace context.