# Gate A — 2026-10-04 — PASS 31/31 (automated lane isolation)

## Commands and results

All Python commands used `PYTHONDONTWRITEBYTECODE=1`.

- `python3 concepts/bc-drain-issues/tests/run-pressure.py`: baseline **PASS 30/30**, sandbox `/tmp/bc-drain-v2-gate-a-bg70lo3g`.
- Same command with check 31 added before the source change: **FAIL** `automated isolation contract failed: SKILL.md::fresh_automated_skipped` (expected RED).
- Same command after implementation: **PASS 31/31**, final sandbox `/tmp/bc-drain-v2-gate-a-_nf982br`. `artifacts/summary.json` reports `checks: 31`, `all_checks_pass: true`, `no_real_mutation: true`, and `gate_b: NOT RUN`.
- `python3 -m unittest discover -s concepts/bc-init-agent/tests -p 'test_*.py'`: **PASS 15/15**.
- `python3 -m unittest discover -s scripts/tests -p 'test_*.py'`: **PASS 38/38** (relationship tooling).
- `python3 -m unittest discover -s concepts/bc-wiki-maintain/tests -p 'test_*.py'`: **PASS 56/56**.
- `python3 scripts/lint.py --write-status`: regenerated the board; no content change (partial status/date unchanged).
- `python3 scripts/lint.py`: **PASS**, with existing partial-test/worktree-external deploy-symlink warnings.
- `git diff --check`: **PASS**.

## New evidence

`artifacts/31/automated-isolation.json` records these source-named checks against `body/SKILL.md`:

- `SKILL.md::fresh_automated_skipped`
- `SKILL.md::deferred_rework_automated_skipped`
- `SKILL.md::restart_active_automated_reported_without_mutation`
- `SKILL.md::non_automated_owner_execution_unchanged`

Six in-memory source mutations fail their named checks: fresh exclusion removed; rework provenance guard removed; claim protection removed; bundle preservation removed; owner untouched-release removed; provenance moved after marker inspection. No canonical file is mutated by these tripwires.

The new check inspects instruction text and ordering, **not a consuming-model command ledger**. There is no parallel queue implementation whose simulated success could stand in for the skill. Existing checks 12–16/27/29 cover deterministic local recovery/landing; check 30 still exercises structural released markers, exact CAS leases, absent-ref creation, ownership proof and safe deletion against a disposable local bare remote. The complete runner remains green.

## Relationship impact and pending gate

`bc-init-agent/body/scaffold.py` already delegates **Claim before work** to `/bc-drain-issues`' authorized claim protocol; no-force absent-ref creation and leased marker reuse are unchanged. The TDD worker load and optional planner handoff are unchanged. No graph edge was added/changed and no generated relationship view was hand-edited.

All four new consuming-model pressure scenarios in `pressure-drain.md` remain **PENDING before deployment**, including the active automated/no-local-state release excuse. Gate B and prior model-pressure gaps remain outstanding; this run does not change `test_status: partial`. No models, network, production claim/label/issue writes, deploy, or push ran. Pre-existing in-flight local bundles were not accessed or migrated/deleted.
