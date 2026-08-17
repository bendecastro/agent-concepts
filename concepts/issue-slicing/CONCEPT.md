# Concept: issue-slicing

Model-invoked discipline that breaks a plan/spec/PRD into independently-grabbable **vertical tracer-bullet slices**, dependency-ordered, quizzing the user on granularity and dependencies before finalizing. Holds the reusable *slicing* behavior; it does NOT publish and does NOT touch any parent issue. The user-invoked `to-tickets` wraps it with GitHub publication, and `bc-plan-to-issues` publishes its output as part of the planning run.

## Design decisions

- **Extracted from `to-issues` (refactor 2026-06-20).** Same motivation as `prd-drafting`: split the reusable slicing behavior out of the user-invoked `to-issues` so `bc-plan-to-issues` can inline a model-invoked discipline instead of calling another user-invoked orchestrator (composition boundary; see `prompting-agents`).
- **The issue template lives here, not in the orchestrator** — one home, no drift between `to-issues` and `bc-plan-to-issues`.
- **Vertical slices, not horizontal.** Each slice cuts end-to-end through every layer and is independently demoable — the tracer bullet. Horizontal slices are the named anti-pattern, shared with `tdd`.
- **Prefactor first.** "Make the change easy, then make the easy change" — prefactoring is its own first slice.
- **Wide refactors expand–contract.** A mechanical change whose blast radius prevents independently green vertical slices expands the new form beside the old, migrates callers in bounded green batches, then contracts only after every batch lands.
- **Fresh-context sizing.** Ordinary slices fit one fresh agent context; split before a handoff becomes necessary.
- **Drain-lifecycle budget sizing.** Audit + build + independent review + likely rework—not implementation alone—must plausibly stay below `bc-drain-issues`' current 200k aggregate child-token soft cap. This is an agent-readiness gate: uncertainty requires splits at independently verifiable behavior boundaries even under pressure to keep one issue or target 300k; if rejected, the unsplit work is not drain-ready. The slicing quiz exposes a qualitative budget-fit judgment and risk reason for every slice; agents do not invent token estimates, and the 300k recovery boundary is never a sizing target. This keeps planning aligned with the executor's real economy controls.
- **Quiz before finalize — the human gate.** The user approves the breakdown (granularity + dependency graph) before slices become agent-ready work. In `bc-plan-to-issues` this quiz *is* the last human checkpoint before the AFK executor runs, so the discipline must not finalize without it.
- **Hands back, never publishes.** Returns approved slices in dependency order for the caller to publish with real `#NN` references; never creates/closes/modifies a parent issue.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) `captured-skills.md` — original `to-issues` body and template; this discipline is the slicing half of that skill, split out.
- Matt Pocock upstream `skills/engineering/to-tickets/SKILL.md` at `391a2701dd948f94f56a39f753f8eea9a859c87` — fresh-context sizing and wide-refactor expand–contract exception. https://github.com/mattpocock/skills/blob/391a2701dd948f94f56a39f753f8eea9a859c87/skills/engineering/to-tickets/SKILL.md
- [AI Engineer Workshop 2026.md](https://www.aihero.dev/ai-engineer-workshop-2026~dwnll) — workshop's `/prd-to-issues` step and the tracer-bullet framing.
- `concepts/prompting-agents/body/SKILL.md` — composition boundary that motivates the split.
- `concepts/bc-drain-issues/body/SKILL.md` — executor lifecycle and provisional 200k soft / 300k hard aggregate child-token boundaries.

## Tests

`tests/scenario.md` — verifies vertical (not horizontal) slicing, fresh-context and drain-lifecycle budget sizing, the expand–contract exception, the quiz-before-finalize gate, the no-publish / no-touch-parent boundary, and dependency-ordered handback. Pressure-tested directly and transitively via `to-issues` and `bc-plan-to-issues`; latest direct run passed 2026-08-17.

## Deploy targets

- Claude Code: `~/.claude/skills/issue-slicing` → relative symlink to `body/`.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../harnesses.md`.
