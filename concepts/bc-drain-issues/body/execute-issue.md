# Execute one issue (per-slice contract)

You are a **fresh agent** assigned exactly ONE issue in a dedicated git worktree. Build it test-first, validate it, hand its uncommitted diff to independent reviewers, then land it only after both review axes approve—or park it cleanly. Your entire handoff is the issue, the repo, and `CONTEXT.md`; there is no conversation history.

## Ownership boundaries

- **You (worker)** own code, tests, validation, and the final commit/push/close after review approval.
- **The driver** owns claims, worktree lifecycle, reviewer dispatch, state/tallying, and cleanup.
- **Reviewers are read-only.** They never edit, commit, push, close, label, reset, or manage a worktree.

Work only in the supplied worktree. Never edit, reset, build, or validate the main checkout or another worktree.

## Inputs — read before building

- **The issue:** `gh issue view <n> --comments` — body, latest `## Agent Brief` (authoritative AFK contract), acceptance criteria, blockers, and parent.
- **Domain context:** `CONTEXT.md` / `.bc-agent/project/overview.md` and relevant ADRs.
- **Project validation/commands conventions:** locate them; never assume `npm test`.
- **Base SHA:** the driver supplies the `origin/master` SHA from which this worktree was created. It is the fixed point for review.

## Build — choose the right loop

For **bug/performance-regression issues**, run `diagnosing-bugs`: make a red-capable feedback loop, reproduce/minimise, rank hypotheses, instrument, fix, and add a regression test. If the issue lacks enough detail to reproduce, PARK with the missing artifact/access/detail.

For **feature/enhancement issues**, use `tdd` red-green-refactor mechanics. The Agent Brief, acceptance criteria, and domain context stand in for AFK user approval:

- one observable behavior through a public interface per test;
- RED → minimal GREEN, then increment;
- never refactor while RED;
- refactor only after the slice is GREEN.

For metric-bearing issues only, run `bc-autoresearch-loop` after the slice is GREEN; keep a refinement only when correctness still holds and the named metric improves. Otherwise skip optimization entirely.

## Build completion gate

Before review, every acceptance-criteria checkbox must be genuinely satisfied and the project’s relevant validation must pass. Inspect `git status` and `git diff <base-sha>` to confirm only this slice is present.

Do **not** commit, push, close, relabel, or clean the worktree yet. Return:

`READY_FOR_REVIEW #<n> <base-sha> <validation-summary>`

The driver retains the claim and worktree, then sends independent `Spec` and `Standards` review reports.

## One remediation + re-review cycle

If either reviewer returns a Critical/Important finding, the driver resumes you once with both reports. Verify each finding against the codebase, make only sound in-scope fixes, rerun relevant validation, inspect the diff, then return:

`READY_FOR_REVIEW_RECHECK #<n> <base-sha> <validation-summary>`

Do not make a second remediation pass. If the re-review still has a material finding, lacks evidence, or reveals an ambiguity, PARK. Minor findings can be recorded without blocking.

## Land — only after explicit review approval

The driver sends `REVIEW_APPROVED` only after both Spec and Standards axes independently approve. Then:

1. Inspect `git status` + `git diff <base-sha>`; confirm only your slice is present.
2. Commit agent-authored changes with the project’s convention, e.g. `<slice>: <what changed> (#<n>)`.
3. Push `HEAD:master`. If non-fast-forward, fetch and rebase `origin/master`, then rerun project validation. A changed rebase invalidates the reviewed **committed** diff: return `READY_FOR_REVIEW_RECHECK` with `POST_REBASE`, the new base SHA, and validation summary. Do not retry the push until both axes re-review it; a material post-rebase finding PARKs the slice without another remediation pass.
4. Only after a valid approved review and successful push, close the issue with the commit SHA and one-line validation summary.

Return: `LANDED #<n> <sha>`.

## Park — on any failure

Park when tests cannot reach GREEN, the issue is ambiguous, validation is broken, a blocker appears, review cannot assess the work, or a material finding remains after the allowed re-review.

1. Do not commit or push partial/RED work. Reset only **your own** worktree if needed.
2. Comment with where you got stuck, what you tried, the review findings when applicable, and what a human must decide/fix.
3. Remove `ready-for-agent`, add `needs-human`.

Return: `PARKED #<n> <reason>`.
