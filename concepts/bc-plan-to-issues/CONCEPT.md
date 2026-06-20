# Concept: bc-plan-to-issues

User-invoked planning orchestrator that runs the whole interactive planning front of the loop in one command: `grilling` → `domain-modeling` (inline) → `prd-drafting` → publish PRD parent issue → `issue-slicing` (with the approval quiz) → publish dependency-ordered `ready-for-agent` slice issues. Hands off to `bc-drain-issues` for autonomous execution. The `bc-` prefix is the user's personal namespace.

## Design decisions

- **Exists to remove sequencing burden** (user's request). The four planning behaviors already existed as separate skills; the user didn't want to remember the order (`grill-me` → `to-prd` → `to-issues`). This collapses the front into one invocation.
- **Composes model-invoked disciplines only — option (c) refactor.** Rather than calling the user-invoked `grill-me`/`to-prd`/`to-issues` (which would break the no-orchestrator-calls-orchestrator boundary it shares with `grilling`/`grill-me`), it inlines `grilling`, `domain-modeling`, `prd-drafting`, `issue-slicing`. The drafting/slicing disciplines were extracted from `to-prd`/`to-issues` specifically to make this clean (see those concepts). No behavior is duplicated.
- **Owns publication itself.** The disciplines don't publish; this orchestrator runs the two `gh issue create` steps (parent PRD issue, then slices in dependency order). Keeps publishing in one place for the pipeline run.
- **Publishes a PRD parent issue.** Resolved open question from the plan: yes, publish the PRD as a parent issue (matching standalone `to-prd`) and reference it as `## Parent` from each slice, for parent/child traceability.
- **Two human gates, then AFK.** The grill (step 1) and the slicing quiz (step 5) are interactive; everything after is autonomous. The body states this explicitly so unresolved scope is closed before `/bc-drain-issues` runs, where a vague issue becomes a parked issue.
- **Recommends the handoff.** Close-out points at `/bc-drain-issues` so planning ends pointing at execution (the loop's two halves).

## Provenance

- `plans/bc-grill-to-ship-loop.md` — the grilled-out build plan this concept implements (decisions locked 2026-06-20).
- `raw/AI Engineer Workshop 2026.md` — the workshop's plan→execute lifecycle (grill → PRD → tracer-bullet issues) this fuses into one command.
- `concepts/grill-me/`, `concepts/to-prd/`, `concepts/to-issues/` — the single-step orchestrators it supersedes for the combined flow (kept standalone for individual use).
- `concepts/prompting-agents/body/SKILL.md` — composition boundary and gate phrasing.

## Tests

`tests/pressure-plan-to-issues.md` — verifies the pipeline runs in order, the grilling one-question gate holds, docs are captured inline (not batched), the slicing quiz is not skipped, it composes disciplines (does not invoke `grill-me`/`to-prd`/`to-issues`), and slices publish blockers-first with real `#NN` and a `## Parent` ref. Discipline-enforcing → must hold before deploy. **Run 2026-06-21 in Pi: FAIL** — batching attack broke one-question-at-a-time, slicing approval was not held as a real gate, and issue body references stayed as placeholders.

## Deploy targets

- Claude Code: `~/.claude/skills/bc-plan-to-issues` → relative symlink to `body/` (deployed 2026-06-21 by explicit user request despite the failing Pi pressure run; use with caution until fixed/re-tested).
- Pi: `~/.agents/skills/bc-plan-to-issues` and `~/.pi/agent/skills/bc-plan-to-issues` → relative symlinks to `body/` (deployed 2026-06-21 by explicit user request despite the failing Pi pressure run; use with caution until fixed/re-tested).
- Other harnesses: manual bootstrap until a real deploy is tested; record in `../../harnesses.md`.
