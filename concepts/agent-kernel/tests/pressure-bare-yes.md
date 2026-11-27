# Pressure test: a bare yes means the recommended option

Rule under test (`body/AGENT-KERNEL.md`, questions to the user): a bare yes / ok / go ahead / "rec" to a question with a recommended option means that option, for every question in a batch. Source: the stranger rerun's build stall, where the driver rejected "Yes, that's fine. Go ahead." twice (`docs/research/2026-11-27-stranger-end-to-end/evidence/npm-pack-rerun-build-stall.md`).

Consumer `openai-codex/gpt-6.1-terra` low via `scripts/pi_sandbox.py` with `-ne -ns --no-skills`, kernel through `--append-system-prompt`, `mktemp -d` scratch. Old arm = the kernel at the commit before this change; its captured prompt holds no new wording (checked with `grep` on `--prompt-out`).

Pass (written before running): the run proceeds with the recommended option(s) without asking the question again.

## Scenario B1 — batch question in a plain project ([run-bare-yes.sh](run-bare-yes.sh))

The prompt replays an earlier turn asking two lettered questions (Markdown vs HTML report, recommended Markdown; chart no vs yes, recommended no), then "Yes, that is fine. Go ahead." Graded on files under `out/`.

| Arm | Pass |
| --- | --- |
| old kernel | 3/3 (`out/summary.md`, no chart) |
| new kernel | 3/3 (`out/summary.md`, no chart) |

No difference: without a competing rule, the model already reads the yes as the recommendation.

## Scenario B2 — the stall itself (`concepts/bc-pipeline-to-done/tests/run-named-item.sh`, `FOLLOWUP=1`)

Both arms load the **old** pipeline body (with "never jump an item the order puts ahead of it") so only the kernel differs. The prompt replays the driver's earlier question (1. build `003-trim-whitespace` now and move it first, recommended; 2. build `001-guardrails-setup-checks` first) and the user's "Yes, that's fine. Go ahead." Graded on `plan.md`.

| Arm | Runs | Pass |
| --- | --- | --- |
| old kernel | 5 | 3/5 — two runs asked again ("Reply like `1`"), no `plan.md` |
| new kernel | 5 | 5/5 — every `plan.md` claims `003-trim-whitespace` and moves it first |

The first new-kernel batch silently ran without the kernel (a relative `KERNEL` path resolved after `cd`); the runner now resolves it first, and those runs are discarded.
