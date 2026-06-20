# Plan: the grill→ship loop (`bc-grill-to-issues` → `bc-drain-issues`)

Date: 2026-06-20
Status: Proposed — grilled and resolved; not yet built.

Build plan for the missing **plan→execute loop** that ties the workshop pipeline
together: a single interactive planning command that produces a `ready-for-agent`
issue queue, and an autonomous (AFK) executor that drains that queue to shipped.

This doc is the durable output of a grilling session. It exists so the build can
start without re-litigating any of the decisions below.

## Why this exists

The workspace already has the four pieces as separate composable skills
(`grill-me`, `to-prd`, `to-issues`, `tdd`, ingested from the Pocock workshop). What
is missing is (a) one command that runs the planning sequence so the user doesn't
have to remember the order, and (b) the "Ralph"-style execution loop that the
workshop describes but we never built. The image-maze `.agent` repo is a consumer
of the planning skills via a repo-local adapter and stops at `to-issues`; nothing
chains planning into execution.

## Locked decisions (from grilling, 2026-06-20)

1. **Shape** — plan-once *interactively*, then *AFK* execution loop over the queue.
   The human gate sits exactly at the planning/execution seam: AFK can't grill, so
   grilling stays in front and only execution detaches.
2. **Autonomy** — execution is fully AFK once the queue exists.
3. **Driver mechanism** — **fresh agent per issue**, spawned per iteration (Agent
   tool) from a thin driver loop. Not a single long-running in-context loop; not a
   wall-clock cron. Fresh-per-issue forces durable handoff and prevents context rot.
4. **Composition boundary** — honored. The executor inlines the *model-invoked*
   discipline (`/tdd`), never the user-invoked orchestrators. For the planner we
   take **option (c): refactor to disciplines** — extract `to-prd`/`to-issues`
   reusable behavior into model-invoked disciplines so both the standalone skills
   and the new orchestrator inline them (no duplication, no boundary break).
5. **Git output — trunk-based.** Each slice: commit (agent-authored only) → push
   `master` → close the issue with a commit + validation-summary comment.
   - **PR-per-slice was rejected for AFK**: dependency-ordered slices need prior
     work visible to the next slice; with nobody to merge, stacked PRs leave slice
     N+1 branched off a base that never saw slice N. Trunk-based propagates
     dependencies for free, and it's exactly what `publish.yaml` already authorizes.
6. **Publish authorization** — `policies/publish.yaml` already authorizes image-maze
   via rule `image-maze-push-and-close-after-agent-work` (`git_push` +
   `github_issue_close` on `master`, gated on agent-authored + relevant validation +
   acceptance criteria satisfied; requires a commit/validation comment on close).
   - The executor's **launch preflight** runs `scripts/publish-check.py
     --repo --remote --branch master`. Exit 0 → push authorized. Exit 2 → **AFK push
     blocked**: abort and tell the user to pre-authorize the target repo (copy the
     image-maze rule block, paths/remotes swapped) or run a local-only variant. The
     loop **never edits `publish.yaml`** to grant its own push (self-amendment
     immunity).
7. **Failure posture — park-and-continue + circuit-breaker.** On a slice that can't
   complete cleanly (tests won't reach GREEN within effort bound, underspecified
   issue, validation failure, hidden blocker): abandon it **without pushing anything
   partial/RED**, comment on the issue explaining where it stuck, swap
   `ready-for-agent` → `needs-human`, move to the next independently-grabbable issue.
   Circuit-breaker: if N consecutive slices park (default 3) or only blocked/parked
   issues remain, stop the whole loop (systemic failure signal). End with a report.
8. **Per-iteration contract** (the runtime spec):
   - **Select** — oldest open `ready-for-agent` issue whose every "Blocked by #NN" is
     closed; skip `needs-human` and anything still blocked.
   - **Execute** — fresh subagent; TDD that one slice against its acceptance criteria
     using the project's `CONTEXT.md` vocabulary.
   - **Completion gate** (satisfies the rule's `after_relevant_validation`) — all
     acceptance-criteria checkboxes met **and** the project's own validation passes.
     The agent **reads the project's validation/commands conventions** (image-maze:
     `conventions/validation.md` + `references/commands.md`) rather than hardcoding
     a generic `npm test`.
   - **Land** — commit (agent-authored only, with git status/diff inspection per the
     rule's constraints) → push `master` → close issue with the required comment.
   - **Terminate** — when no open `ready-for-agent` issue has all blockers satisfied
     (queue drained or only blocked/parked remain). Plus circuit-breaker, plus a hard
     `max-iters` runaway backstop.
9. **TDD AFK adaptation** — `/tdd` as written has interactive checkpoints ("get user
   approval on the plan"). AFK has no user, so the **issue's acceptance criteria +
   `CONTEXT.md` stand in for user confirmation**. The executor inlines tdd's
   red-green-refactor *mechanics* but treats acceptance criteria as the approved
   spec. Make this substitution explicit in `execute-issue.md`.
10. **Naming** — `bc-grill-to-issues` (planner), `bc-drain-issues` (executor). The
    `bc-` prefix is the user's personal namespace. `bc-grill-to-issues`'s close-out
    **recommends running `/bc-drain-issues`** next — planning ends pointing at
    execution.

## Deliverables

### A. Refactor — extract two model-invoked disciplines (build first)
- **`prd-drafting`** (model-invoked) — synthesize conversation + codebase + test
  seams into a PRD body (the reusable *writing* behavior, minus publishing).
- **`issue-slicing`** (model-invoked) — break a plan into vertical tracer-bullet
  slices, dependency-ordered, including the granularity/deps quiz.
- Rewire **`to-prd`** → "run `/prd-drafting` → publish to GitHub" and **`to-issues`**
  → "run `/issue-slicing` → publish to GitHub". Behavior preserved, relocated. This
  mirrors how `grilling`/`domain-modeling` already back `grill-me`.
- Re-run/author `to-prd`/`to-issues` pressure tests to confirm behavior preserved.

### B. `bc-grill-to-issues` (user-invoked planning orchestrator)
One command, the interactive front:
`grilling` → `domain-modeling` (inline, as `grill-me` does) → `prd-drafting` →
publish PRD parent issue → `issue-slicing` (incl. the approval quiz — this is the
**human gate**) → publish slice issues blockers-first with real `#NN` refs, all
`ready-for-agent`. Composes only model-invoked disciplines. Close-out recommends
`/bc-drain-issues`.
- Open sub-decision to settle at build time: whether to publish a PRD *parent* issue
  in addition to the slice issues (standalone `to-prd` does). Lean: yes, for
  parent/child traceability.

### C. `bc-drain-issues` (user-invoked AFK executor)
- **`body/SKILL.md`** — launcher + driver loop. Preflight (publish-check, branch
  `master`, label hygiene for `ready-for-agent`/`needs-human`, `max-iters` +
  circuit-breaker params), select-next-eligible loop, spawn fresh subagent per issue,
  record landed/parked, circuit-breaker, terminate, end-of-run report (landed vs
  parked vs blocked).
- **`body/execute-issue.md`** — the per-issue agent contract: read issue +
  `CONTEXT.md` + project validation/commands conventions → `/tdd` red-green-refactor
  (with the AFK adaptation in decision 9) → completion gate → land (commit/push/close
  with comment) or **park** (comment, relabel `needs-human`, no partial/RED push).

### D. Docs
- **Pipeline doc** in the workspace tying `bc-grill-to-issues → bc-drain-issues` (and
  the disciplines beneath them).
- **Extend image-maze `planning-workflow.md`** with the execution phase (trunk-based
  push/close, `needs-human` parking) so that wiki documents the full loop, not just
  planning.

## Test gates (both new concepts enforce discipline → must hold before deploy)
- **`bc-drain-issues`**: parks instead of pushing RED; preflight **blocks** launch on
  a repo `publish.yaml` doesn't authorize; circuit-breaker trips after N consecutive
  parks; never closes an issue with unmet acceptance criteria; never grabs an issue
  with an open blocker.
- **`bc-grill-to-issues`**: one-question grilling gate holds (transitive); quiz
  before publishing slices; composes disciplines (does not call user-invoked skills);
  publishes blockers-first with real issue numbers.
- **Refactor**: `to-prd`/`to-issues` behavior preserved after relocation.

## Build order (checkbox steps)
- [ ] 1. Refactor → `prd-drafting` + `issue-slicing`; rewire `to-prd`/`to-issues`; re-test.
- [ ] 2. `bc-grill-to-issues` + test.
- [ ] 3. `bc-drain-issues` (`SKILL.md` + `execute-issue.md`) + pressure tests.
- [ ] 4. Pipeline doc + image-maze adapter extension.
- [ ] 5. Deploy (Claude Code symlinks after gates; Pi via `scripts/deploy-local-skills.py`)
      + bookkeeping (`CONCEPT.md` ×N, `index.md`, `harnesses.md`, `log.md`) + lint + commit.

## Bookkeeping note
Concept-name uniqueness: `bc-grill-to-issues`, `bc-drain-issues`, `prd-drafting`,
`issue-slicing` — all new, dash-case, unique. When authoring the instruction bodies,
adapt blocks from `concepts/prompting-agents/body/SKILL.md` rather than inventing
phrasing (per AGENTS.md Implement/Update).
