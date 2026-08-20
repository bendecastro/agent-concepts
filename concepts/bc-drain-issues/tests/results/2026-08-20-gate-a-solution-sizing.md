# Gate A — 2026-08-20 — PASS 25/25 (solution sizing)

Second Gate A run of the day, after wiring `minimal-solution-ladder` into the worker
dispatch and bounding the Standards axis's structural findings with `codebase-design`
vocabulary. The earlier 23/23 run for the discriminating-evidence rule is
[results/2026-08-20-gate-a.md](2026-08-20-gate-a.md).

- Runner: `run-pressure.py`, no arguments.
- Result: **PASS 25/25**, sandbox `/tmp/bc-drain-v2-gate-a-zj0ma5lz`. `summary.json`
  reports `checks: 25`, `all_checks_pass: true`, `no_real_mutation: true`.
- `summary.json`'s pass key was renamed `all_23_pass` → `all_checks_pass` and a `checks`
  count added, so the field stops needing an edit every time a check is appended.

## What changed in canon

- `body/SKILL.md` — the driver now passes `minimal-solution-ladder` on every
  implementation packet, alongside `tdd` / `diagnosing-bugs` / `bc-autoresearch-loop`
  where applicable. Before this, the Pi drain roles excluded the broad skill catalog and
  the dispatch list named only those three, so the ladder never reached a drain worker.
- `body/execute-issue.md` — build loop opens with the sizing paragraph: climb before
  writing, rung 2 needs a qmd/tree prior-art search because a fresh worktree has no
  familiarity, a forwarding wrapper is a failed rung, the acceptance matrix counts as
  explicitly requested, shape defers to `codebase-design`, and the ladder's terse output
  convention does not replace `READY_FOR_REVIEW`.
- `body/review-contract.md` — structural findings use module/interface/depth/seam/adapter,
  must pass the deletion test before being raised, and grade Minor unless they break
  stated behavior, leave it untestable through any interface, or duplicate the repository.

## Fireability

Each new rule was deleted in turn and the run re-executed:

| Mutation | Observed failure |
|---|---|
| Drop the ladder from the SKILL dispatch line | `driver does not pass the ladder to implementation workers` |
| Reword the worker's rung-2 fresh-worktree clause | `worker contract missing solution-sizing rule: no accumulated familiarity` |
| Delete the structural-findings paragraph | `review contract missing structural-finding rule: Structural findings use codebase-design vocabulary` |

Restoring all three passes 25/25. Neither check is inert.

## Scope note

Check 6's existing assertion tracked the old dispatch wording (`pass only the applicable
worker discipline explicitly`) and was updated to the new phrasing. Its subject —
explicit discipline selection despite disabled skill inheritance — is unchanged.

Gate B: NOT RUN, unchanged. This change adds a discipline to the build phase and a bound
to the review phase; its token effect is unmeasured, and v3's Gate B was already
outstanding.
