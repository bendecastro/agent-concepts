# Gate A — 2026-08-20 — PASS 27/27 (solution sizing, docs, resume)

Second Gate A run of the day, after wiring `minimal-solution-ladder` into the worker
dispatch and bounding the Standards axis's structural findings with `codebase-design`
vocabulary. The earlier 23/23 run for the discriminating-evidence rule is
[results/2026-08-20-gate-a.md](2026-08-20-gate-a.md).

- Runner: `run-pressure.py`, no arguments.
- Result: **PASS 27/27**, sandbox `/tmp/bc-drain-v2-gate-a-g56w9pkg`. `summary.json`
  reports `checks: 27`, `all_checks_pass: true`, `no_real_mutation: true`.
- Checks 24–25 (solution sizing, structural findings) landed first at 25/25 in sandbox
  `/tmp/bc-drain-v2-gate-a-zj0ma5lz`; checks 26–27 were added in the same day's follow-up
  and the whole gate re-run.
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
  A second rule loads `codebase-docs` when the diff touches a README, an existing `docs/`
  page, an architecture page, or contract-stating JSDoc, bounded so that absent
  documentation is never a finding and the review never becomes a rewrite request.
- `body/execute-issue.md` — the worker updates an owning documentation page in the same
  diff as the behavior it describes, and does not invent a `docs/` tree or narrate the
  issue in a page.
- `body/SKILL.md` — new `## Resuming an interrupted run` section. Remote
  `bc-drain-claims/*` refs are the authoritative index of what a dead run owned, because
  they are the one record that does not live in the context that vanished. Four
  dispositions: adopt a worktree holding an uncommitted diff (re-running the gate and both
  axes, since no standing approval survives a run whose reviewer records are gone),
  restore a valid bundle, release an untouched claim, and report-and-skip anything else
  without releasing a claim or deleting a worktree. Adapted from `bc-swarm`'s
  recover-before-relaunch rule, which the drain did not inherit — `bc-swarm` is read-shaped
  and hands implementation fan-out to this loop.

## Fireability

Each new rule was deleted in turn and the run re-executed:

| Mutation | Observed failure |
|---|---|
| Drop the ladder from the SKILL dispatch line | `driver does not pass the ladder to implementation workers` |
| Reword the worker's rung-2 fresh-worktree clause | `worker contract missing solution-sizing rule: no accumulated familiarity` |
| Delete the structural-findings paragraph | `review contract missing structural-finding rule: Structural findings use codebase-design vocabulary` |
| Reword the worker's `codebase-docs` placement clause | `worker contract missing docs rule: follow the repo-available codebase-docs for placement` |
| Delete the reviewer's source-tree-docs paragraph | `review contract missing docs rule: Source-tree documentation is checked against the diff, not written by it` |
| Delete the resume section | `SKILL missing resume rule: ## Resuming an interrupted run` |
| Soften the unaccountable-claim fail-safe to "Release the claim" | `SKILL missing resume rule: Never release a claim you cannot account for` |

Restoring all of them passes 27/27. No new check is inert.

## Scope note

Check 6's existing assertion tracked the old dispatch wording (`pass only the applicable
worker discipline explicitly`) and was updated to the new phrasing. Its subject —
explicit discipline selection despite disabled skill inheritance — is unchanged.

Gate B: NOT RUN, unchanged. This change adds a discipline to the build phase and a bound
to the review phase; its token effect is unmeasured, and v3's Gate B was already
outstanding.
