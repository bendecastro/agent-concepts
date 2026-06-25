# Execute one issue (per-slice contract)

You are a **fresh agent** assigned exactly ONE issue. Build it test-first, validate it, and land it — or park it cleanly. Your entire handoff is the issue, the repo, and `CONTEXT.md`; there is **no conversation history**. Nobody is watching (AFK), so you **cannot ask questions** — the issue's acceptance criteria are your spec.

## Where you work — your worktree, nothing else
You have been given a dedicated git **worktree path**. That is your working directory for everything: reading the code you'll change, editing, building, and validating all happen there. It is a full checkout branched from the latest `master` tip. **Never** edit, reset, build, or run validation in the main repo checkout or any other worktree — concurrent slices live in sibling worktrees and touching them corrupts other agents' in-flight work. Run every `git` command from inside your worktree (`cd` there first, or use `git -C <worktree>`); `git status`/`git diff` are then naturally scoped to just your slice. The driver creates and destroys this worktree — you do not manage its lifecycle.

## Inputs — read before building
- **The issue:** `gh issue view <n> --comments` — body, latest `## Agent Brief` if present (authoritative AFK contract), acceptance criteria, "Blocked by", "Parent".
- **`CONTEXT.md` / `.bc-agent/project/overview.md`** (domain vocabulary) and any ADRs in the area you're touching — match their names.
- **The project's own validation + commands conventions.** Find them (e.g. `conventions/validation.md`, `references/commands.md`, README, package scripts). Do **NOT** assume a generic `npm test` — use what this project actually defines.

## Build — choose the right loop

For **bug/performance-regression issues**, run the `diagnosing-bugs` debug discipline first: build a tight red-capable feedback loop for the reported symptom, reproduce/minimise, rank hypotheses, instrument, then fix with a regression test. This is not optional triage; it is the required loop for bug-like work. AFK adaptation: if the Agent Brief/issue lacks enough detail to build a red-capable loop, PARK with the exact missing artifact/access/detail.

For **feature/enhancement issues**, run the `tdd` red-green-refactor mechanics, with one adaptation: `tdd` normally asks the user to approve the interface and test plan — AFK has no user, so the issue's **Agent Brief + acceptance criteria + domain context** stand in for that approval. Treat the acceptance criteria as the agreed spec.
- **Tracer bullet:** one test for one behavior. **RED** → minimal **GREEN**.
- **Incremental loop** over the remaining behaviors, one test at a time. Tests assert observable behavior through public interfaces, never implementation detail. **Never refactor while RED.**
- **Refactor** only once everything is GREEN, with the tests as the safety net.

If a bug fix reveals there is no correct regression-test seam, finish/park the bug honestly and note a follow-up recommendation for `/improve-codebase-architecture`; do not smuggle an architecture refactor into the bug slice unless it is required by the acceptance criteria.

## Completion gate — ALL must hold to land
- Every acceptance-criteria checkbox is genuinely satisfied.
- The project's own validation passes (the commands you found above — tests + lint/typecheck/build as the project defines them).

If you cannot reach this gate within honest effort → **PARK**. Never push partial or RED work.

## Optional: bounded improvement — only when there's a metric
Run this **only if** the issue targets a measurable improvement (speed, size, memory, cost) or its acceptance criteria name a metric. Otherwise **skip entirely** and land the slice as-is — do not optimize blind.

If it applies, now that the slice is GREEN run `bc-autoresearch-loop` for a bounded, gated refinement: name one objective metric, baseline it, make ONE bounded change, and keep it **only if** the project's tests still pass **and** the metric beats the threshold — otherwise revert. Never trade behavior for the metric, and never "improve" by dropping required output. Record any kept win (metric, baseline → current, delta, win kind) in the land commit message and the issue close-comment.

## Land — only when the gate holds
1. **Inspect:** `git status` + `git diff` in your worktree. Confirm ONLY your slice's changes are present. (Because the worktree branched from `origin/master` in isolation, the only changes should be yours — if anything else appears, stop and PARK; do not commit it.)
2. **Commit** (agent-authored changes only) with a message naming the issue, e.g. `<slice>: <what changed> (#<n>)`. Follow the project's commit-message conventions (trailers, etc.).
3. **Push to `master`:** `git push origin HEAD:master`. If it's rejected as non-fast-forward (another slice landed while you worked), `git fetch origin master && git rebase origin/master`, then **re-run the project validation** — a textually clean rebase can still break behavior — and push again. Repeat until it lands; if a rebase produces a conflict you cannot resolve safely, PARK.
4. **Close the issue** with a comment containing the commit sha + a one-line validation summary (what you ran, that it passed). This satisfies the `publish.yaml` rule's close-with-comment + acceptance-criteria + validation conditions.

Return: `LANDED #<n> <sha>`.

## Park — on any failure
Triggers: tests won't reach GREEN within honest effort, the issue is underspecified/ambiguous, project validation is broken, or a hidden blocker surfaces.
1. Do **NOT** push or commit partial/RED work — reset **your own worktree** if needed (`git reset --hard` from inside it) so nothing half-built lingers. Never touch the main checkout or another worktree.
2. **Comment** on the issue: exactly where you got stuck, what you tried, and what a human needs to decide or fix.
3. **Relabel:** remove `ready-for-agent`, add `needs-human`.

Return: `PARKED #<n> <reason>`.
