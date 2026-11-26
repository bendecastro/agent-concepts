# Fallbacks when a machine-only tool is missing

Why: Deployed skills name tools only the owner's machine has (the publish check found through a private overlay, a guarded pytest runner, a storage health check, Pi worker roles), so on a stranger's machine the pipeline aborts at preflight or the instruction has no defined action.
Done when: Every deployed reference to a machine-provided tool states what to do when it is absent; the pipeline ships its own publish checker and asks once per run when no policy exists; the README lists what the pipeline needs; requirements in [requirements.md](requirements.md).
Stage: now
Blocked by: nothing
Kind: bug
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state
Planned: bc-plan-to-pipeline 2026-11-26
Ready for agent: yes

## Steps

- [x] Bundled publish checker: move the checker into `bc-pipeline-to-done`'s body with `scripts/publish-check.py` as a thin entry point; existing checker tests pass against it. Blocked by: nothing. Stories 1, 2. Done when the checker tests pass, the fresh-install test shows the checker present in a plugin install, and lint has 0 ERROR. Out of scope: preflight wording.
  - Review: approved by tier-1 2026-11-26
  - Gate: pass ./scripts/gate at 6dc06f8 2026-11-26
  - Landed in `6dc06f8`.
- [x] Preflight asks once without a policy: reword preflight (checker choice, per-run question when present, local-only when away, manifest record); pressure scenario both ways, results beside it in `concepts/bc-pipeline-to-done/tests/`. Blocked by: Bundled publish checker. Stories 1, 2. Done when the with-change runs ask once and record the answer (present) and commit without pushing (away), the baseline does not, and CONCEPT status, `index.md` and `.bc-agent/log.md` are updated. Out of scope: other tools' fallbacks.
  - Review: approved by tier-1 2026-11-26 (round 2)
  - Gate: pass ./scripts/gate at bc525c0 2026-11-26
  - Landed in `bc525c0`.
- [x] Fallback for every machine-tool reference and README prerequisites: inventory, classify and reword each hit in deployed bodies; README lists pipeline prerequisites and optional tools. Blocked by: nothing. Stories 3, 4. Done when every inventoried hit states a fallback or stop (inventory recorded in this item's folder), lint has 0 ERROR and the gate passes. Out of scope: shipping the tools themselves.
  - Review: approved by tier-1 2026-11-26 (round 2)
  - Gate: pass ./scripts/gate at 502ed1a 2026-11-26
  - Landed in `502ed1a`.

## Outcome

Strangers no longer hit tools that exist only on the owner's machine. The publish checker ships inside `bc-pipeline-to-done`; with no publish policy, preflight asks once per run whether it may push to the target branch (a yes also sets single-driver mode: one item at a time, no remote claim refs), and an owner-away run commits locally only. Every deployed-body reference to a machine-only tool (inventory: `inventory.md`, 43 rows) now states a fallback or a stop: plain pytest with `tmp_path` and the temp-file rules, a skipped-and-reported absent storage check, a stop before claims when Pi subagents or the pipeline roles are missing. README lists the pipeline's install prerequisites and the optional tools. Pressure tests were dry runs on Terra low, one run per arm: missing-policy treatment asked once and planned only the target push; missing-tools treatment 5/5 against 2/5 for the old body. No live pipeline run has exercised the no-policy path yet.

Spent: 2h 37m active, 33.9M tokens, $17.32 (estimated; pi 19 sessions, claude-code 0 sessions, codex 0 sessions; other tools not counted)
