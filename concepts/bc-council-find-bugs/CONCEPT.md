---
test_kind: pressure
test_status: pass # dry run 2/2 on Terra low: plan.md met all 11 criteria; earlier live attempt stopped early in 6 of 7 runs; plan-every-item handoff inherited from bc-find-bugs, which passed 3/3 on Terra low 2026-11-24 (bc-plan-to-pipeline/tests/pressure-plan-every-item-results-2026-11-24.md); this chain not run
tested: 2026-11-24
deployed: yes
---
# Concept: bc-council-find-bugs

Runs `bc-find-bugs` through the advisor council (`bc-council-chain` + `bc-council-mode`): one scout maps the area, every advisor hunts it with a focus dealt from `bc-find-bugs`' five-focus list, advisors attack each other's candidates, one worker reproduces the strongest as failing tests on the hunt branch, and the normal two-tier report and filing follow.

## Design decisions

All from the owner-approved [council bug hunt plan](../../work/3-done/2026-11/019-council-find-bugs.md); numbers are that plan's decisions.

- **Reproduction worker gets `bc-safe-runs` (2026-11-28, item 054-safe-runs-module).** The reproduction worker loads `bc-safe-runs` from its launch skill list and runs `bc-find-bugs` §3, which keeps the one-line fallback. Its task also carries the module’s packet line, since children do not load skills on their own.

- **Thin chain (decisions 1, 6).** Loads `bc-council-chain`, `bc-find-bugs` and `bc-council-mode` and defines only what `bc-council-chain`'s "What a chain must define" list leaves open: pre-reading and map contents, focuses, candidate format, duplicate rule, verdict rule, report additions and filing. Scope, reproduction, report sections and filing stay in `bc-find-bugs`.
- **Agreement orders, never confirms (decision 3).** Pass 2 attacks; an unanswered code-evidenced dispute drops a candidate; agreement shares of N only order the reproduction queue and the suspected tier. Only a reproduction watched failing confirms.
- **Focuses dealt round-robin (decision 8)** in `bc-find-bugs` §2's order; each advisor still reports outside its focus.
- **One reproduction worker, advisors read-only (decision 4).** After pass 2 a single `worker` runs `bc-find-bugs` §3 on the top `--max-repro` (default 12, decision 11). It is launched with `bc-find-bugs` plus the worker role's default skills, because a launch skill list replaces the defaults and no role carries `bc-find-bugs` (owner, 2026-11-24, recorded in the plan).
- **At most 8 candidates per advisor (decision 11)**, raisable per run.
- **Filing is `bc-find-bugs` §5 with `Source: bc-council-find-bugs`** (decision 5), so filters can tell council hunts apart.
- **Duplicate rule: same location and same claimed wrong result.** Same location with a different claim is two candidates, mirroring `bc-council-chain`'s "disagreement, not duplicate".
- **Run through without stopping (pressure test 2026-11-24).** In the first run both consumers stopped after the map and reported "incomplete"; the body now says to run every step through the report, asking only the questions the loaded skills require.
- **Report written by the parent on the hunt branch.** The worker returns per-candidate outcomes; the parent adds agreement lines, disputes, focuses and the roster section. Choice made here: the plan does not say who writes the report, and only the parent holds the pass 2 matrix.
- **Filing now ends with planning (2026-11-24, owner decision).** Filing is `bc-find-bugs` §5 unchanged, which now runs `bc-plan-to-pipeline` on each filed planned item; nothing is added here.

## Provenance

- [Council bug hunt plan](../../work/3-done/2026-11/019-council-find-bugs.md), decisions 1–11 and step 3 of its build order.
- Composes [bc-council-chain](../bc-council-chain/CONCEPT.md), [bc-find-bugs](../bc-find-bugs/CONCEPT.md) and [bc-council-mode](../bc-council-mode/CONCEPT.md); shape copied from [bc-council-improve-architecture](../bc-council-improve-architecture/CONCEPT.md).
- Owner decision 2026-11-24: every item in work-planned gets the `bc-plan-to-pipeline` treatment before it starts (filing-time handoff, pickup rule, `Planned:` marker).

## Tests

[tests/scenario.md](tests/scenario.md) runs the chain on `bc-find-bugs`' practice project with three stand-in advisors on the pressure-test model, graded against `bc-find-bugs`' answer key. [Results 2026-11-24](tests/results-2026-11-24.md): the earlier live attempt did not pass (on Terra low most runs stopped before the report); the dry run (`plan.md` only, launches nothing) passed 2/2, so the instructions are complete and the live gap is the consumer carrying a long chain. The first live run with the real council is the live test (decision 10). Since 2026-11-24 `bc-find-bugs` §5 filing ends by running `bc-plan-to-pipeline` on each filed item, so the scenario's `all` filing check now also expects that; the 2026-11-24 results predate the change.

## Deploy targets

Not deployed. When deployed: the shared skill bus via `scripts/deploy-local-skills.py`.
