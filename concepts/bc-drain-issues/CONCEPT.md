# Concept: bc-drain-issues

User-invoked AFK executor that drains a repo's `ready-for-agent` GitHub issue queue: a preflight-gated launcher runs a driver loop that, per unblocked issue, dispatches a fresh subagent to build the slice test-first and land it trunk-based (commit → push `master` → close with a validation comment), parking cleanly on failure. The autonomous execution half of the loop; runs after `bc-plan-to-issues`. The `bc-` prefix is the user's personal namespace.

## Design decisions

- **Fresh subagent per issue.** The handoff is durable artifacts only (issue body + `CONTEXT.md` + repo). Forces self-contained issues and prevents context rot over a long queue. The alternative (one long-running agent) degrades and hides whether issues are really independent. Driver dispatches per iteration; it is not a single in-context loop and not a wall-clock cron (wrong shape for draining a queue).
- **Trunk-based, not PR-per-slice.** Each slice commits → pushes `master` → closes its issue. PR-per-slice was rejected for AFK: dependency-ordered slices need prior work visible to the next, and with nobody to merge, stacked PRs leave slice N+1 branched off a base that never saw slice N. Trunk-based propagates dependencies for free and is exactly what `publish.yaml` already authorizes (image-maze rule: `git_push` + `github_issue_close` on `master`).
- **Hard parallel safety uses a remote Git claim branch, not labels/kanban.** Research against Matt Pocock's current public skills found a triage state machine (`ready-for-agent`, `ready-for-human`, etc.) and agent briefs, but no atomic claim/lock mechanism; workshop footage shows a simple `afk.sh` loop reading local `issues/*.md`. Labels, assignees, comments, and kanban/project columns are visible hints, not compare-and-swap locks. A no-force push to `bc-drain-claims/issue-<n>` on the shared origin is the durable cross-harness primitive: exactly one runner can create the claim ref; losers skip the issue.
- **Preflight is the only human gate.** AFK can't answer mid-run, so every human-decision check happens once, before the loop: branch=`master`, `publish-check.py` authorization, claim-branch authorization for parallel mode, label hygiene, caps. A `publish-check` exit 2 **blocks** the AFK push (abort, or opt-in commit-only-local) — the loop never edits `publish.yaml` to grant its own push (self-amendment immunity).
- **Park-and-continue + circuit-breaker.** A slice that can't complete cleanly is parked (comment + `needs-human` relabel, nothing partial/RED pushed) and the loop moves on, so one bad slice doesn't waste the run. A run of N consecutive parks (default 3) trips the circuit-breaker and stops the whole loop — that pattern signals a systemic break. Plus a `max-iters` runaway backstop.
- **Completion gate reads the project's own validation.** The per-issue agent finds the project's validation/commands conventions rather than hardcoding a test command, so the gate matches how the project actually builds. This is what satisfies the rule's `after_relevant_validation`.
- **TDD / diagnosis AFK adaptation.** Feature slices use `/tdd`: with no user, the issue's Agent Brief + acceptance criteria + domain context stand in for approval. Bug/performance issues use `diagnosing-bugs`: first build a red-capable feedback loop; if the issue lacks enough repro detail, PARK rather than guessing. Stated explicitly in `execute-issue.md`.
- **Optional bounded improvement (`bc-autoresearch-loop`), conditional.** After a slice is GREEN, the per-issue agent runs `/bc-autoresearch-loop` for a metric-gated refinement **only when** the issue targets a measurable improvement; with no objective metric it skips entirely (don't optimize blind). Gated tightly because an AFK agent doing open-ended optimization is a regression risk — the discipline keeps a change only if correctness still holds and the metric provably improves, else reverts. Composition stays clean: the executor inlines the model-invoked `bc-autoresearch-loop`, not a user-invoked orchestrator.
- **Two-file body.** `SKILL.md` = launcher + driver loop (preflight, select, dispatch, circuit-breaker, report); `execute-issue.md` = the per-issue subagent contract (TDD → gate → land/park). Split because they run in different agents.

## Provenance

- `plans/bc-grill-to-ship-loop.md` — the grilled-out build plan this implements (decisions locked 2026-06-20).
- `raw/AI Engineer Workshop 2026.md` — the workshop's execution half: an agent (Ralph) running human-in-the-loop then AFK with TDD, selecting issues, writing tests, implementing, committing.
- Matt Pocock upstream `skills/engineering/triage/SKILL.md`, `AGENT-BRIEF.md`, and `setup-matt-pocock-skills/SKILL.md` (checked 2026-06-21) — public workflow defines triage labels/state and agent briefs, but no atomic claim/lock; this concept adds the missing parallel-safe claim layer.
- `policies/publish.yaml` — the `image-maze-push-and-close-after-agent-work` rule whose push + close-with-comment + acceptance-criteria + validation conditions the land step is built to satisfy; `scripts/publish-check.py` for the preflight.
- `concepts/tdd/` — the red-green-refactor discipline the per-issue agent inlines for features (AFK-adapted).
- `concepts/diagnosing-bugs/` — the diagnosis discipline the per-issue agent inlines for bug/performance issues.
- `concepts/bc-autoresearch-loop/` — the optional, conditional metric-gated improvement discipline the per-issue agent inlines post-GREEN.
- `concepts/prompting-agents/body/SKILL.md` — composition (executor inlines the model-invoked `tdd`, not a user-invoked orchestrator) and gate phrasing.

## Tests

`tests/pressure-drain.md` — pressure scenarios: parks instead of pushing RED; preflight **blocks** launch on a repo `publish.yaml` doesn't authorize; preflight blocks parallel mode unless claim branches are authorized; concurrent runners contending for the same issue result in one successful claim and one skip; circuit-breaker trips after N consecutive parks; never closes an issue with unmet acceptance criteria; never grabs an issue with an open blocker; commit contains only the slice's changes. Discipline-enforcing → must hold before deploy. Test the driver loop and the per-issue contract against stubbed `gh`/git so no real pushes occur. **Run 2026-06-21 in Pi: PASS** against stubbed `gh`/push artifacts before the claim-branch addition; concurrency pressure rerun pending.

## Deploy targets

- Claude Code: `~/.claude/skills/bc-drain-issues` → relative symlink to `body/` (carries `execute-issue.md` alongside; deployed 2026-06-21).
- Pi: `~/.agents/skills/bc-drain-issues` and `~/.pi/agent/skills/bc-drain-issues` → relative symlinks to `body/` (deployed 2026-06-21).
- Other harnesses: manual bootstrap until a real deploy is tested; record in `../../harnesses.md`.
