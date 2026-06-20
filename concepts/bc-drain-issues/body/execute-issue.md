# Execute one issue (per-slice contract)

You are a **fresh agent** assigned exactly ONE issue. Build it test-first, validate it, and land it — or park it cleanly. Your entire handoff is the issue, the repo, and `CONTEXT.md`; there is **no conversation history**. Nobody is watching (AFK), so you **cannot ask questions** — the issue's acceptance criteria are your spec.

## Inputs — read before building
- **The issue:** `gh issue view <n> --comments` — body (what to build), acceptance criteria, "Blocked by", "Parent".
- **`CONTEXT.md`** (domain vocabulary) and any ADRs in the area you're touching — match their names.
- **The project's own validation + commands conventions.** Find them (e.g. `conventions/validation.md`, `references/commands.md`, README, package scripts). Do **NOT** assume a generic `npm test` — use what this project actually defines.

## Build — TDD, AFK-adapted
Run the `/tdd` red-green-refactor mechanics, with one adaptation: `/tdd` normally asks the user to approve the interface and test plan — AFK has no user, so the issue's **acceptance criteria + `CONTEXT.md` stand in for that approval**. Treat the acceptance criteria as the agreed spec.
- **Tracer bullet:** one test for one behavior. **RED** → minimal **GREEN**.
- **Incremental loop** over the remaining behaviors, one test at a time. Tests assert observable behavior through public interfaces, never implementation detail. **Never refactor while RED.**
- **Refactor** only once everything is GREEN, with the tests as the safety net.

## Completion gate — ALL must hold to land
- Every acceptance-criteria checkbox is genuinely satisfied.
- The project's own validation passes (the commands you found above — tests + lint/typecheck/build as the project defines them).

If you cannot reach this gate within honest effort → **PARK**. Never push partial or RED work.

## Optional: bounded improvement — only when there's a metric
Run this **only if** the issue targets a measurable improvement (speed, size, memory, cost) or its acceptance criteria name a metric. Otherwise **skip entirely** and land the slice as-is — do not optimize blind.

If it applies, now that the slice is GREEN run `/bc-autoresearch-loop` for a bounded, gated refinement: name one objective metric, baseline it, make ONE bounded change, and keep it **only if** the project's tests still pass **and** the metric beats the threshold — otherwise revert. Never trade behavior for the metric, and never "improve" by dropping required output. Record any kept win (metric, baseline → current, delta, win kind) in the land commit message and the issue close-comment.

## Land — only when the gate holds
1. **Inspect:** `git status` + `git diff`. Confirm ONLY your slice's changes are present — never sweep unrelated working-tree changes into the commit.
2. **Commit** (agent-authored changes only) with a message naming the issue, e.g. `<slice>: <what changed> (#<n>)`.
3. **Push `master`.**
4. **Close the issue** with a comment containing the commit sha + a one-line validation summary (what you ran, that it passed). This satisfies the `publish.yaml` rule's close-with-comment + acceptance-criteria + validation conditions.

Return: `LANDED #<n> <sha>`.

## Park — on any failure
Triggers: tests won't reach GREEN within honest effort, the issue is underspecified/ambiguous, project validation is broken, or a hidden blocker surfaces.
1. Do **NOT** push or commit partial/RED work — reset the working tree if needed so nothing half-built lingers.
2. **Comment** on the issue: exactly where you got stuck, what you tried, and what a human needs to decide or fix.
3. **Relabel:** remove `ready-for-agent`, add `needs-human`.

Return: `PARKED #<n> <reason>`.
