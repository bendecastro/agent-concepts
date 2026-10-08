# Gate A — 2026-10-08 — PASS 31/31 (cloud-claim provenance, round 3)

## Commands and results

All Python commands used `PYTHONDONTWRITEBYTECODE=1` from the worktree root
`/home/ben/Sync/Work/PUBLIC/worktrees/Agents/cloudclaim`.

- `python3 concepts/bc-drain-issues/tests/run-pressure.py --help`: prints
  `usage: run-pressure.py [--markers-only]` (exit 1); learned options — full run or
  `--markers-only`. No narrow check-31 flag exists; full run is lightweight
  (no models) so no flag was added.
- Round-3 RED: same full command with the round-3 check 31 (gate-first resume sentence,
  "`cloud-build-run` comment" wording, "when any of" assertion) against the round-2 text:
  **FAIL** `AssertionError: automated isolation contract failed: SKILL.md::restart_active_automated_reported_without_mutation`
  (the renamed provenance sentence is absent from the round-2 resume paragraph; the
  `when any of` assertion itself was verified satisfied with exactly 1 occurrence and 0
  for `when all of` before the fix).
- `PYTHONDONTWRITEBYTECODE=1 python3 concepts/bc-drain-issues/tests/run-pressure.py`
  after the round-3 fix: **PASS 31/31**, exit 0 (`RUN_PRESSURE_EXIT:0`), final sandbox
  `/tmp/bc-drain-v2-gate-a-ijwku5o5`. `artifacts/summary.json` reports `checks: 31`,
  `all_checks_pass: true`, `no_real_mutation: true`, `gate_b: NOT RUN`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -p 'test_*.py'`:
  **PASS 38/38** (`Ran 38 tests ... OK`).
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/lint.py`: **exit 0** (`LINT_EXIT:0`),
  with existing partial-test/worktree-external deploy-symlink warnings only.
- `git diff --check`: **PASS** (exit 0). `git diff --cached --stat`
  empty (no staged files).

## Round-3 reviewer Minor findings (all folded in)

Resume paragraph led with the garden-path "Before inspecting claim tips or adopting..."
while the gate authorizes a read-only tip read — now it leads with the gate (labels, then
read-only claim-tip body, then comments/PRs) running before marker classification and
before any adoption, restore, release, or cleanup. New text says "`cloud-build-run`
comment" (never bare "marker") for the issue comment, so it cannot be confused with the
Released Claim Marker. Check 31 asserts the "when any of" connective with a "when all of"
rewrite mutation that must be rejected. Counts below are recounted from code.

## New evidence

`artifacts/31/automated-isolation.json` records source-named checks against `body/SKILL.md`:

- Four prior scenarios unchanged in intent (`fresh` / `deferred_rework` / `restart_active` /
  `non_automated_owner_execution`; restart asserts the specific fail-closed string and the
  renamed gate-first provenance sentence with tip-inspection ordering).
- `SKILL.md::cloud_claim_provenance_skipped` (held claim tip +
  `carries in-progress-agent with a cloud-build-run comment` + open-PR head branch +
  `when any of` connective; `is history, not a live claim` + `follows the normal owner
  path` carve-out; gate-first ordering; specific fail-closed; `never released ... exactly
  like automated`; Select parenthetical with comment wording).
- `SKILL.md::untouched_excludes_cloud_claim` (`no held cloud-claim tip naming branch=...`,
  `no in-progress-agent with a cloud-build-run comment`, `no open cloud-build/issue-<n>
  PR`; valid marker still FREE; open PR / comment-backed in-progress still cloud-lane for
  selection).

Nineteen in-memory source mutations fail their named checks — 18 `lane_mutations` counted
from code plus the provenance-after-marker-inspection ordering tripwire:
fresh-guard-removed, rework-guard-removed, claim-protection-removed,
bundle-preservation-removed, owner-release-removed, cloud-tip-removed,
cloud-marker-conjunction-removed, cloud-marker-broadened, history-carveout-removed,
cloud-connective-all-of, cloud-pr-removed, cloud-failclosed-removed, cloud-order-removed,
cloud-selection-removed, untouched-cloud-exclusion-removed,
untouched-marker-conjunction-removed, released-marker-still-free-removed,
open-pr-still-cloud-lane-removed, and provenance-after-marker-inspection. The
cloud-connective-all-of mutation is the round-3 tripwire: rewriting "when any of" to
"when all of" fails `SKILL.md::cloud_claim_provenance_skipped`. No canonical file is
mutated by these tripwires.

The check inspects instruction text and ordering, **not a consuming-model command
ledger**. Existing checks 12–16/27/29 cover deterministic local recovery/landing; check 30
still exercises structural released markers, exact CAS leases, absent-ref creation,
ownership proof and safe deletion against a disposable local bare remote. The complete
runner remains green.

## Relationship impact and pending gate

`bc-init-agent/body/scaffold.py` **Claim before work** already delegates to
`/bc-drain-issues`' authorized claim protocol; no-force absent-ref creation and leased
marker reuse are unchanged. The TDD worker load and optional planner handoff are
unchanged. No graph edge was added/changed (`RELATIONSHIPS.md` checked) and no generated
relationship view was hand-edited.

Consuming-model pressure scenarios for check 31 — including the four new cloud-claim
cases (held cloud-claim tip on an owner issue, #361 shape; in-progress + comment with
absent ref; open cloud PR with released marker; released claim + comment-only history →
selectable) — are catalogued in `tests/pressure-drain.md` check 31 and remain **PENDING
before deployment**, including the #361 live-cloud-claim release excuse. Gate B and prior
model-pressure gaps remain outstanding; this run does not change `test_status: partial`
(`tested: 2026-10-08`). No models, network, production claim/label/issue writes, deploy,
or push ran. Pre-existing in-flight local bundles were not accessed or migrated/deleted.

## Round-2 record (semantics kept, wording superseded)

Round 2 redefined non-`automated` cloud-lane as held tip / in-progress+marker /
open cloud PR with the history carve-out: RED
`SKILL.md::cloud_claim_provenance_skipped` on round-1 text, then GREEN 31/31 (sandbox
`/tmp/bc-drain-v2-gate-a-uslnv4pu`), 38 unittest OK, lint 0, diff-check 0. Round 3 keeps
those semantics and fixes the resume lead-in, comment wording, connective assertion, and
counts.

## Round-1 record (superseded semantics, kept for trail)

Round 1 added the two scenarios with "any marker comment is live" semantics: RED on the
old source, then GREEN 31/31 (sandbox `/tmp/bc-drain-v2-gate-a-vuxialjc`). Round 2
corrected the contradiction; the round-1 text was the RED fixture for round-2 assertions.

## Round 4 (2026-10-08) — never-release rebinding + comment-only wording

Two reviewer Minor findings folded in minimally, no scope widening:

1. `body/SKILL.md:22` never-release clause rebound from broad "report any cloud-lane claim, `cloud-build-run` comment, or PR" to "on an issue that is cloud-lane under the three live signals above, report any cloud-lane claim, `cloud-build-run` comment, or PR" — report + never release/delete/reuse/relabel now applies only to cloud-lane issues, so a history-only `cloud-build-run` comment (released-marker/absent ref, no `in-progress-agent`, no open cloud PR) follows the normal owner path. `including marker cleanup` kept (Released Claim Marker cleanup).
2. `CONCEPT.md` cloud-claim bullet now says `cloud-build-run` comment only: "plus a `cloud-build-run` comment", "with a `cloud-build-run` comment", "every `cloud-build-run` comment live", and "or `in-progress-agent` with a `cloud-build-run` comment stays cloud-lane" (`marker` kept only for Released Claim Marker / non-marker tip distinction).

TDD RED/GREEN (check 31): added `on an issue that is cloud-lane under the three live signals above, report any cloud-lane claim` to `SKILL.md::restart_active_automated_reported_without_mutation` plus new `cloud-never-release-rebroadened` mutation (revert scoped sentence to broad "report any cloud-lane claim, `cloud-build-run` comment, or PR") that must be rejected. RED: updated `run-pressure.py` against 3934398 text FAILs `AssertionError: automated isolation contract failed: SKILL.md::restart_active_automated_reported_without_mutation`. GREEN after the two fixes: `PYTHONDONTWRITEBYTECODE=1 python3 concepts/bc-drain-issues/tests/run-pressure.py` PASS 31/31 exit 0, sandbox `/tmp/bc-drain-v2-gate-a-4_p73v9l` (final verification; earlier GREEN `/tmp/bc-drain-v2-gate-a-wwut_3ll`), `summary.json` checks 31 all pass, `31/automated-isolation.json` shows 19 `lane_mutations` + provenance-after-marker-inspection tripwire = 20 rejected (prior 18 plus `cloud-never-release-rebroadened`). `python3 -m unittest discover -s scripts/tests -p 'test_*.py'` 38/38 OK, `python3 scripts/lint.py` exit 0 (deploy-symlink warnings only), `git diff --check` clean, no staged files. Counts updated consistently in `CONCEPT.md` Tests (new round-4 paragraph), `tests/pressure-drain.md` current-result line, and `ev[31]`. `test_status: partial`, Gate B/model-pressure gaps remain; no models, network, deploy, or push ran.
