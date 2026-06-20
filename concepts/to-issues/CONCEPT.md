# Concept: to-issues

User-invoked orchestrator that breaks a plan/spec/PRD into independently-grabbable **GitHub issues** using tracer-bullet vertical slices, quizzing the user on granularity and dependencies before publishing with the `ready-for-agent` label.

## Design decisions

- **Thin wrapper over `issue-slicing` (refactor 2026-06-20).** The slicing behavior — vertical tracer-bullet slices, prefactor-first, the quiz-before-finalize gate, the template, no-touch-parent — was extracted into the model-invoked `issue-slicing` discipline so `bc-grill-to-issues` can reuse it without orchestrator-calls-orchestrator. `to-issues` is now: run `/issue-slicing` → publish in dependency order. Behavior preserved, relocated.
- **GitHub tracker baked in** (user's decision), same rationale as `to-prd`: `gh` + `ready-for-agent`, no `setup-matt-pocock-skills` indirection. Publishing happens in dependency order so real issue numbers can fill "Blocked by".
- **Quiz before publish lives in the discipline.** The user approves the breakdown (granularity + dependency graph) inside `issue-slicing` before any issues are created; this orchestrator only publishes already-approved slices.

## Provenance

- `raw/pocock-skills-upstream/captured-skills.md` — verbatim `to-issues` body and template (the slicing half now lives in `issue-slicing`). https://github.com/mattpocock/skills/blob/main/skills/engineering/to-issues/SKILL.md
- `raw/AI Engineer Workshop 2026.md` — workshop's `/prd-to-issues` step and the tracer-bullet framing.
- `concepts/issue-slicing/` — the extracted slicing discipline this orchestrator wraps.

## Tests

`tests/scenario.md` — verifies vertical (not horizontal) slicing, the quiz-before-publish step, dependency-ordered publication with real `#NN` references, and the no-touch-parent guard. Process orchestrator; scenario authored, full pressure run pending.

## Deploy targets

- Claude Code: `~/.claude/skills/to-issues` → relative symlink to `body/`.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../harnesses.md`.
