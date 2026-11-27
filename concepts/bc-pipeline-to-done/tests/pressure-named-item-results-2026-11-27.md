# Pressure test: the user names an item that the order puts behind others

Rule under test (`body/source-work-items.md` § Eligibility): when the user's request names an item, that naming is the order decision for the run; record it in the claim commit. Source: the stranger rerun's build stall (`docs/research/2026-11-27-stranger-end-to-end/evidence/npm-pack-rerun-build-stall.md`).

Runner: [run-named-item.sh](run-named-item.sh) (fixture: `001-guardrails-setup-checks` and `002-architecture-review` ready and first in `work/order.md`, `003-trim-whitespace` ready and third; no remote; prompt "Build 003-trim-whitespace, the item I just planned" plus dry-run harness notes). Consumer `openai-codex/gpt-6.1-terra` low via `scripts/pi_sandbox.py` with `-ne -ns --no-skills`, the body copied into a `mktemp -d` scratch folder. No extension was needed (dry run with a fictional roster), so no `-e`. Old arm = the body at the commit before this change; it never sees the new wording, and no transcript read a concept path.

Pass (written before running): `plan.md` names `003-trim-whitespace` as the claim and the run asks no order question.

## Results 2026-11-27

| Arm | Runs | Pass | What happened |
| --- | --- | --- | --- |
| old body | 3 | 0/3 | All three stopped: "the pipeline rules prohibit skipping them", asked whether to reorder; no `plan.md`. |
| new body | 3 | 3/3 | All wrote `plan.md` claiming `item-003-trim-whitespace`; each claim commit moves the item to the top of `work/order.md` (two also regenerate `work/README.md`). |

First run of every arm stopped at preflight (no `subagent` tool, unmatched roster); the harness notes were changed to state that preflight passes, and all six runs above are from the corrected runner.
