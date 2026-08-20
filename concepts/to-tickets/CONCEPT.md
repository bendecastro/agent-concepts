---
test_kind: pressure
test_status: pass
tested: 2026-07-16
deployed: yes
---
# Concept: to-tickets

User-invoked orchestrator that breaks a plan/spec/PRD into independently-grabbable **GitHub tickets** (GitHub issues) using tracer-bullet vertical slices, quizzing the user on granularity and dependencies before publishing with the `ready-for-agent` label.

## Design decisions

- **Thin wrapper over `issue-slicing` (refactor 2026-06-20).** The slicing behavior — vertical tracer-bullet slices, prefactor-first, the quiz-before-finalize gate, the template, no-touch-parent — was extracted into the model-invoked `issue-slicing` discipline so `bc-plan-to-issues` can reuse it without orchestrator-calls-orchestrator. `to-tickets` is now: run `/issue-slicing` → publish in dependency order. `/to-issues` remains a deployment alias for compatibility. Behavior preserved, relocated.
- **GitHub tracker baked in** (user's decision), same rationale as `to-prd`: `gh` + `ready-for-agent`, no `setup-matt-pocock-skills` indirection. Publishing happens in dependency order so real issue numbers can fill "Blocked by".
- **Quiz before publish lives in the discipline.** The user approves the breakdown (granularity + dependency graph) inside `issue-slicing` before any issues are created; this orchestrator only publishes already-approved slices.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) `captured-skills.md` — original `to-issues` body and template (the slicing half now lives in `issue-slicing`).
- Matt Pocock upstream `skills/engineering/to-tickets/SKILL.md` at `391a2701dd948f94f56a39f753f8eea9a859c87` — current public name and wide-refactor guidance. https://github.com/mattpocock/skills/blob/391a2701dd948f94f56a39f753f8eea9a859c87/skills/engineering/to-tickets/SKILL.md
- [AI Engineer Workshop 2026.md](https://www.aihero.dev/ai-engineer-workshop-2026~dwnll) — workshop's `/prd-to-issues` step and the tracer-bullet framing.
- `concepts/issue-slicing/` — the extracted slicing discipline this orchestrator wraps.

## Tests

`tests/scenario.md` — verifies vertical (not horizontal) slicing, the quiz-before-publish step, dependency-ordered publication with real `#NN` references, and the no-touch-parent guard. Process orchestrator; pressure-tested 2026-07-16 **PASS** (Grok).

## Deploy targets

- Canonical deploy: `to-tickets`; compatibility alias: `to-issues` → `to-tickets`.
- Claude Code: `~/.claude/skills/to-tickets` → relative symlink to `body/`.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../docs/harnesses.md`.
