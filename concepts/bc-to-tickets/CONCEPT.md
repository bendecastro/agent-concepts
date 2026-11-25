---
test_kind: pressure
test_status: partial # slicing-quiz removal 2026-11-24 untested
tested: 2026-07-16
deployed: yes
---
# Concept: bc-to-tickets

User-invoked orchestrator that breaks a plan/spec/PRD into independently-grabbable **GitHub issues** using tracer-bullet vertical slices, publishing the agent-finalized slices with the `ready-for-agent` label.

## Design decisions

- **Thin wrapper over `bc-plan-slicing` (refactor 2026-06-20).** The slicing behavior — vertical tracer-bullet slices, prefactor-first, the finalization step, the template, no-touch-parent — was extracted into the model-invoked `bc-plan-slicing` discipline so `bc-plan-to-pipeline` can reuse it without orchestrator-calls-orchestrator. `bc-to-tickets` is now: run `/bc-plan-slicing` → publish in dependency order. The former `/to-issues` compatibility alias was removed 2026-09-27. Behavior preserved, relocated.
- **GitHub tracker baked in** (user's decision), same rationale as `bc-to-spec`: `gh` + `ready-for-agent`, no `setup-matt-pocock-skills` indirection. Publishing happens in dependency order so real issue numbers can fill "Blocked by".
- **Finalization lives in the discipline.** `bc-plan-slicing` finalizes the breakdown (granularity + dependency graph) without a human approval stop since 2026-11-24 (owner decision); this orchestrator only publishes the final slices.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) `captured-skills.md` — original `to-issues` body and template (the slicing half now lives in `bc-plan-slicing`).
- Matt Pocock upstream `skills/engineering/to-tickets/SKILL.md` at `391a2701dd948f94f56a39f753f8eea9a859c87` — current public name and wide-refactor guidance. https://github.com/mattpocock/skills/blob/391a2701dd948f94f56a39f753f8eea9a859c87/skills/engineering/to-tickets/SKILL.md
- AI Engineer Workshop 2026 (Matt Pocock) — workshop's `/prd-to-issues` step and the tracer-bullet framing.
- `concepts/bc-plan-slicing/` — the extracted slicing discipline this orchestrator wraps.

## Tests

`tests/scenario.md` — verifies vertical (not horizontal) slicing, the quiz-before-publish step, dependency-ordered publication with real `#NN` references, and the no-touch-parent guard. Process orchestrator; pressure-tested 2026-07-16 **PASS** (Grok).

## Deploy targets

- Canonical deploy: `bc-to-tickets`; the former `to-issues` compatibility alias was removed 2026-09-27.
- Claude Code: `~/.claude/skills/bc-to-tickets` → relative symlink to `body/`.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../docs/guides/harnesses.md`.
