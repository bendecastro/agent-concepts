---
test_kind: pressure
test_status: partial # no-approval-stop change passed 2026-11-24 (Terra low); wide-refactor and unsafe-split checks not exercised
tested: 2026-11-24
deployed: yes
---
# Concept: plan-slicing

Model-invoked discipline that breaks a plan/spec/PRD into independently-grabbable **vertical tracer-bullet slices**, dependency-ordered, and finalized by the agent without stopping for human approval. Holds the reusable *slicing* behavior; it does NOT publish and does NOT touch any parent issue. The user-invoked `to-tickets` wraps it with GitHub publication, and `bc-plan-to-pipeline` publishes its output as part of the planning run.

## Design decisions

- **Renamed from `issue-slicing` (2026-11-24, owner decision).** It slices into work items as well as tracker issues, the same reason `bc-plan-to-issues` became `bc-plan-to-pipeline`. The old name stays as a deploy alias (`DEPLOY_ALIASES`).
- **Extracted from the then-named `to-issues` (refactor 2026-06-20; renamed `to-tickets` 2026-07-11).** Same motivation as `prd-drafting`: split reusable slicing behavior out of the user-invoked publication orchestrator so `bc-plan-to-pipeline` can inline a model-invoked discipline instead of calling another user-invoked orchestrator (composition boundary; see `prompting-agents`).
- **The issue template lives here, not in the orchestrator** — one home, no drift between `to-tickets` and `bc-plan-to-pipeline`.
- **Vertical slices, not horizontal.** Each slice cuts end-to-end through every layer and is independently demoable — the tracer bullet. Horizontal slices are the named anti-pattern, shared with `tdd`.
- **Prefactor first.** "Make the change easy, then make the easy change" — prefactoring is its own first slice.
- **Wide refactors expand–contract.** A mechanical change whose blast radius prevents independently green vertical slices expands the new form beside the old, migrates callers in bounded green batches, then contracts only after every batch lands.
- **Fresh-context sizing.** Ordinary slices fit one fresh agent context; split before a handoff becomes necessary.
- **Drain-lifecycle sizing is qualitative, not a token-threshold readiness gate.** Audit + build + independent review + likely rework—not implementation alone—inform whether a slice fits the executor's lifecycle. When scope, compatibility surface, external semantics, migration risk, or likely rework make end-to-end verification and safe rework implausible, split at independently verifiable behavior boundaries; if the user rejects a necessary split, do not label the unsplit work agent-ready. Explain the judgment in the reported breakdown. Do not invent token estimates or treat former 200k/300k executor limits as current requirements; when one slice cannot be verified and reworked safely, the agent splits it rather than handing it back as agent-ready.
- **No approval stop (owner decision 2026-11-24).** The agent checks granularity and dependencies itself, finalizes, and shows the final breakdown as a report rather than a question. Replaces the former quiz-before-finalize gate, which explicitly refused "I trust you" as approval: the owner now trusts model slicing and the stop blocked the pipeline from running on its own. A user who asks in the request to review the slices first still gets a draft and a wait. In `bc-plan-to-pipeline` the grill is now the only human gate before the AFK executor.
- **Hands back, never publishes.** Returns final slices in dependency order for the caller to publish with real `#NN` references; never creates/closes/modifies a parent issue.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) `captured-skills.md` — original `to-issues` body and template; this discipline is the slicing half of that skill, split out.
- Matt Pocock upstream `skills/engineering/to-tickets/SKILL.md` at `391a2701dd948f94f56a39f753f8eea9a859c87` — fresh-context sizing and wide-refactor expand–contract exception. https://github.com/mattpocock/skills/blob/391a2701dd948f94f56a39f753f8eea9a859c87/skills/engineering/to-tickets/SKILL.md
- AI Engineer Workshop 2026 (Matt Pocock) — workshop's `/prd-to-issues` step and the tracer-bullet framing.
- `concepts/prompting-agents/body/SKILL.md` — composition boundary that motivates the split.
- `concepts/bc-drain-issues/body/SKILL.md` — executor lifecycle, review/rework bounds, and recovery contract; its former 200k/300k token gates were removed from current policy on 2026-09-26.

## Tests

`tests/scenario.md` — verifies vertical (not horizontal) slicing, fresh-context and qualitative drain-lifecycle sizing, the expand–contract exception, finalizing without an approval stop (draft-and-wait only on explicit request), the no-publish / no-touch-parent boundary, and dependency-ordered handback. The 2026-08-17 direct pressure pass exercised the former token-threshold policy; current qualitative-sizing expectations were updated 2026-09-26 and were partly exercised on 2026-11-24, when the removal of the approval quiz passed on Terra low (finalizes without asking; still waits when asked to review first; baseline sliced horizontally). Prior pressure also ran transitively via `to-tickets` (then named `to-issues`) and `bc-plan-to-pipeline`.

## Deploy targets

- Claude Code: `~/.claude/skills/plan-slicing` → relative symlink to `body/`.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../docs/harnesses.md`.
