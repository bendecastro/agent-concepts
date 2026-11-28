# Execute one issue (worker contract)

You are a fresh worker assigned exactly one issue in a dedicated worktree. You own **code, tests, and validation only**. Return a review-ready uncommitted diff to the driver. You never commit, push, close/comment/relabel an issue, create/delete claims, clean/reset/remove a worktree, or land the change—even after approval. Those are driver responsibilities, which prevents implementation authority from bypassing independent review.

Work only in the supplied worktree. Never mutate or validate the main checkout or another worktree.

## Inputs

Read the supplied issue body/latest `## Agent Brief`, acceptance matrix (when present), base SHA, baseline-validation summary, project context/ADRs, repository instructions, and validation conventions. Use qmd only for search when the driver identifies a covering collection; never index it. The base SHA is the review comparison point.

If the packet contains an unresolved product choice, unavailable access/resource, ambiguous acceptance contract, or irreparable environment failure, return:

`BLOCKED_NEEDS_HUMAN #<n> <exact decision/access/environment evidence>`

Do not use `BLOCKED_NEEDS_HUMAN` for ordinary test failures, reviewer findings, incomplete implementation, or other agent-fixable engineering work. Report those precisely so the driver can rework or defer them without losing the diff.

## Build loop

On every implementation packet, load and follow the repo-available `bc-minimal-solution-ladder` before writing code, stopping at the first rung that holds. Rung 2 — already in this codebase — is the rung a fresh worktree gets wrong, because you arrive with no accumulated familiarity: search the driver's qmd collection and the tree for prior art before defining anything new, and treat a wrapper that only forwards to an existing helper as a failed rung rather than as reuse. The acceptance matrix is explicitly requested behavior, so no criterion is skippable as speculative and the never-simplify list stays absolute. The ladder governs how much to build; use `bc-codebase-design` vocabulary for the shape you build, where a small interface over substantial implementation is fully compatible with the ladder and fewest-files never overrides a real seam. Its terse output convention does not apply here — return the full `READY_FOR_REVIEW` form below, and write a deliberate corner-cut's `ceiling:` comment into the code rather than only into your handoff.

For bug/performance-regression issues, load and follow the repo-available `bc-diagnosing-bugs` discipline: establish a red-capable reproduction, minimise it, rank and test hypotheses, instrument where useful, fix the cause, and add a regression test. Missing evidence needed to reproduce is human-blocking only when it cannot be derived or generated with available resources.

When fixing a performance, size, memory, or structure regression, load `bc-performance-guardrails`. Add the check that would have caught it and report the command and result, or state why no check can catch it.

For feature/enhancement work, load and follow the repo-available `bc-tdd` discipline in thin observable increments: one public behavior per test, RED, minimal GREEN, then refactor only while GREEN. The Agent Brief, acceptance matrix, and binding domain context are the AFK contract.

For metric-bearing work only, load and follow `bc-optimize-code` after GREEN: establish a correctness-bearing baseline, make one bounded refinement, and keep it only when correctness holds and the named metric improves. Do not optimize without an objective metric. If a named discipline is unavailable in the harness, preserve these mechanics explicitly rather than silently weakening them.

When the change alters behavior that a README, an existing `docs/` page, an architecture page, or contract-stating JSDoc already describes, update that owning page in the same diff and follow the repo-available `bc-codebase-docs` for placement. Do not invent a new `docs/` tree, do not restate a contract that already has a home, and do not narrate this issue in a documentation page — the acceptance matrix records what the slice did, and a docs page that narrates a change is stale the moment the next one lands. A repository that keeps no documentation for this surface needs none written to satisfy this rule.

Load the `bc-safe-runs` skill. Else: guarded test runner (otherwise plain `pytest`; never custom `--basetemp`), scratch via `mktemp -d` not `/tmp`, targeted tests, configured storage health check (stop if critical) before full suites, worktrees or fan-out.

Preserve the driver's baseline cache. Run targeted tests/checks while editing and record commands, outcomes, failing IDs, and concise baseline deltas. Do not run the full project suite; final landing validation belongs to the driver.

If you notice follow-up work or an observation outside this issue, list each one as a one-line follow-up in your handoff, and leave the work folders and the ideas file untouched. Why: you run in a git worktree, so you cannot see other worktrees' item numbers and would pick a taken one; the line is outside this issue's scope, so the scope gate and the reviewers would reject it; and parallel workers appending to one ideas file conflict at rebase. When the project has a "Where things go" table, the driver appends your follow-ups to its ideas file after landing.

Add only the dependencies the issue or item names. A dependency is any library, tool or package the project does not already declare, including test-only ones such as a property-testing library; adding one means editing a dependency file (`pyproject.toml`, `requirements*.txt`, `package.json`, a lockfile and the like) or installing it into the project. When the work seems to need one the issue does not name, do not add it and do not work around the rule with a vendored copy: return `BLOCKED_NEEDS_HUMAN` with the question “May I add `<name>` as a (test) dependency? It is needed for <reason>; without it I would <alternative>.” If the issue already says how to manage without it (for example example-based tests instead of property tests) on a `Dependencies:` line marked as the owner's answer, do that instead; `bc-tdd` counts that line as the owner's waiver. An unmarked line is not a waiver of a required test level, so a missing level still stops the unit with the question. Why: a dependency is the owner's decision with lasting cost, and planning (`bc-plan-to-pipeline`) asks it while the owner is present and records it as a `Dependencies:` line; in a stranger's test run a builder added Hypothesis to `pyproject.toml` unasked.

## Review-ready gate

Before handoff:

- map every acceptance-matrix row/criterion to observable evidence that would differ if the criterion were false;
- run relevant targeted validation and distinguish known baseline failures from regressions;
- inspect `git status`, changed files, and `git diff <base-sha>` for scope;
- ensure no file is staged and no unrelated artifact is present;
- write requested validation evidence outside the project worktree.
- fill in the Test levels block from the `bc-tdd` skill (section Test levels) (L1, L2, L3, one choice per line); the driver's gate rejects a handoff without it.
- write any status line or log entry that summarizes test results (for example a concept's `test_status` or a `.bc-agent/log.md` line) last, copying each count from the results table and naming its unit ("2 of 3 runs", "5 of 5 checks in one run"), even when the packet supplies a draft. Why: summaries written ahead of their table claimed more than it showed in 4 of 10 items of one drain.

Return:

`READY_FOR_REVIEW #<n> <base-sha> <targeted-validation-summary>`

Include the Test levels block, a compact changed-file list, criterion-to-evidence mapping, commands/results, baseline delta, any fixable concern, and any one-line follow-ups. Do not include a long implementation narrative.

## Rework assignment

A fresh rework worker receives the same worktree, the round's review packet paths, compact unresolved findings and dispositions, and a driver-computed **implicated row set**: the acceptance-matrix rows tied to those findings. Read the packet's `diff.patch`, `acceptance-matrix.json`, and `validation.json` instead of re-deriving them.

Verify each finding against the code, make only sound in-scope fixes, and add or update a regression test where appropriate. Then re-evidence a **narrowed** scope rather than the whole matrix:

- every implicated row;
- every additional row whose mapped files your fix actually touched—you know what you changed, and `packet.json` carries the matrix→file map;
- every check that was already failing or known-flaky.

Evidence for rows that are neither implicated nor touched carries forward unchanged; do not re-run it. Inspect only your own delta for scope. The driver's deterministic gate independently re-checks full status, staged files, unrelated files, and coverage across carried-forward plus new evidence, so duplicating that inspection buys nothing.

Return the same `READY_FOR_REVIEW` form with finding dispositions, plus the rows you re-evidenced and the rows you carried forward.

If a finding cannot be fixed because it exposes a real product decision, unavailable access/resource, ambiguous contract, or irreparable environment failure, return `BLOCKED_NEEDS_HUMAN` with exact evidence. Otherwise, even if a fix attempt fails, return the current diff and precise fixable failure; the driver decides whether another bounded rework cycle or `REWORK_DEFERRED` is appropriate. Never discard, reset, land, or mutate GitHub state yourself.
