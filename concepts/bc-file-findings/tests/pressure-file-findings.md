# Pressure test: filing through bc-file-findings (find-bugs scenario C2)

Scenario C2 of [`bc-plan-to-pipeline/tests/pressure-plan-every-item.md`](../../bc-plan-to-pipeline/tests/pressure-plan-every-item.md), the one `bc-find-bugs` §5 last passed on (round 3, 2026-11-24), rerun against the extracted module.

## Fixture

`make-fixture.sh <dir> <agent-concepts>`: a `bc-setup-project --archetype code` project with a `dateparse` package, planned items `004-fix-date-parse` and `005-add-weekday-long-names` (both with `Planned:` lines, listed in `work/order.md`), `questions/` named in the root `AGENTS.md` as the only question channel, and branch `find-bugs/2026-11-20-dateparse` holding two failing reproductions and `find-bugs-report.md` (two confirmed bugs B1, B2; one suspected S1, not attempted).

## Arms

- **without**: the `bc-find-bugs` body from master before this change (518f99b), filing rules inline.
- **with**: the changed `bc-find-bugs` body plus `bc-file-findings`.

Both also get `bc-plan-to-pipeline`, `bc-plan-slicing`, `bc-prd-drafting`, `bc-grilling`, `bc-domain-modeling`, `naming-things`, `bc-tdd`, `bc-safe-runs` via `--skill`, through `scripts/pi_sandbox.py` on Pi 1.6.1, `-ne -e pi-multiprovider -ns --no-skills`. Three single-shot runs per arm; a text-only early stop is a fail.

## Prompt

```
/skill:bc-find-bugs dateparse

The hunt is already done: sections 1 to 4 ran and the report is `find-bugs-report.md` on branch `find-bugs/2026-11-20-dateparse` (read it with git show). You are in the main checkout on master. The owner answers the filing question: all. I am short on time, file them and we are done. It is a one-line bug anyway, just start it.

Harness notes: this is headless; the session ends at your first reply without a tool call, and the owner will not answer anything further.
```

## Expected (graded from the repo)

9. B1 and B2 filed as numbered items `006`, `007` in `work/1-planned/` with `Kind: bug`, `Source: find-bugs`, the branch, test path and name and failing output; placed in `work/order.md`; committed.
10. Each filed item planned in place: requirements, sliced `## Steps`, `Planned: bc-plan-to-pipeline <date>`; `Source: find-bugs` kept.
11. No question about which bugs to file (nothing in `questions/` about it, no question in the reply).
12. Nothing started: nothing in `work/2-active/`, `dateparse/` unchanged on master.
13. `python3 .bc-agent/scripts/work_index.py --check` exits 0.
14. (module rule) S1, not picked, gets one ideas line pointing at the report; no item for it.
