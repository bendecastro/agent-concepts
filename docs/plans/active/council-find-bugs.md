# Council bug hunt — `council-chain`, `find-bugs`, `bc-council-find-bugs`

Date: 2026-11-24
Status: active
Decided in a grilling session with the owner (every answer was the recommended option).

## Goal

A bug hunt the owner can run with or without the advisor council, whose confirmed findings come
with a failing test, so a fix starts from proof rather than from a vote.

## Decisions

1. **Shape.** A standalone parent skill `find-bugs` plus a thin chain `bc-council-find-bugs`,
   the same split as `improve-codebase-architecture` and `bc-council-improve-codebase`. Why: the
   parent stays usable and testable without paying for the council; the chain holds only the
   council steps.
2. **Scope.** One hunt covers an area the owner names (folder, module or feature), or the whole
   repo when it is small; optionally limited to changes since a ref. Why: deep reading of a bounded
   area finds real bugs; a whole large repo spreads every reader thin.
3. **Two tiers.** *Confirmed*: a failing test or reproduction the hunt ran and watched fail for the
   stated reason. *Suspected*: ranked by evidence quoted from the code, each with why it is not
   confirmed. Advisor agreement only orders the suspected tier. Why: agreement is not evidence that
   a bug is real.
4. **Reproductions.** Advisors stay read-only and propose a reproduction per candidate (input,
   steps, expected vs actual). After cross-examination one worker in its own worktree writes and
   runs them; tests that fail for the stated reason are kept on a branch, and each filed bug item
   names its test. Without the council, the parent's single agent does the same.
5. **Filing.** The owner picks from the report with every confirmed bug pre-selected: `all` files
   each as a `Kind: bug` work item linked to its test (placed by the top-kind rule). Suspected bugs
   the owner picks become investigation items. The rest go to the ideas file; a rejected bug is
   recorded with the owner's reason, as in the architecture chain.
6. **Shared council steps.** Extract now into a new public concept `council-chain` that every
   `bc-council-*` skill loads: roster (from an optional private overlay), the shared map, pass 1,
   merge, pass 2, advisor fallbacks, sandbox-copy cleanup. `bc-council-improve-codebase` is cut down
   to load it; the private roster overlay moves to `council-chain`. `council-mode` stays close to
   its upstream source. Why: the second copy is the moment to extract.
7. **What it hunts.** Wrong behaviour of every kind: logic and edge cases, error handling, state
   and data loss, concurrency, contracts between modules. A security hole seen in passing is
   filed as `Kind: security` with a pointer to `security-audit`; slowness is out of scope.
8. **Focuses.** In the chain each advisor gets a focus dealt round-robin from that fixed list
   (inputs and edge cases, error and failure paths, state and data lifecycle, concurrency and
   ordering, contracts between modules) and still reports bugs outside it. Pass 2: each advisor
   attacks the others' candidates. Why: unstanced advisors converge on the obvious.
9. **Reproduction form.** The project's own test framework when it has one; otherwise a small
   runnable script on the same branch that prints the wrong result and exits non-zero. A candidate
   that cannot be reproduced either way within the time limit stays suspected, with the reason.
10. **Tests.** A practice project with one or two planted bugs per focus plus decoys (code that
    looks wrong but is correct). The parent runs on the pressure-test model and must confirm planted
    bugs with failing tests and confirm no decoy. The chain runs with the pressure-test model
    standing in for every advisor (focus dealing, two tiers, `all` filing, cleanup). The first real
    run with the real council is the live test.
11. **Limits.** At most 8 candidates per advisor in pass 1; the 12 strongest after
    cross-examination are reproduced, 10 minutes each; the rest stay suspected, marked
    "not attempted". Each limit can be raised per run (for example `--max-repro 20`).

## Build order

1. `council-chain` extracted; `bc-council-improve-codebase` loads it; a pressure check shows the
   architecture chain behaves as before. (Parallel with 2.)
2. `find-bugs` and the practice project; parent pressure test.
3. `bc-council-find-bugs` on top of both; chain pressure test with stand-in advisors.

## Execution record

- 2026-11-24: steps 1 and 2 dispatched to two workers.
