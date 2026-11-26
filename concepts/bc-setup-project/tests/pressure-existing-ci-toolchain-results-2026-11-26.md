# Existing-CI toolchain: pressure results, 2026-11-26

[Scenario](pressure-existing-ci-toolchain.md). Real execution, one completed run per arm on `openai-codex/gpt-6.1-terra`, low, not a dry run. Both arms started from the scaffold at `5e6aa44`. Each first launch failed before any model turn because `--no-swarm` was unavailable with extensions disabled; the one permitted startup retry omitted that switch and kept extensions disabled. Both retries exited zero. Session logs confirm the assigned bodies were injected and show no reads of other skill copies.

| Observable | Initial revised body (one run) | Old body (one run) |
| --- | --- | --- |
| Node setup and dependency installation before `scripts/gate` | Graded FAIL at the time: workflow has checkout, Node 22 setup and `scripts/gate`, with `npm ci` inside the gate. Regraded PASS under the corrected criterion: CI is fully provisioned. | Same output and placement; regraded PASS. |
| Workflow delegates checks and preserves prior CI | PASS: no inline `npm test`; original workflow, package and test unchanged. The gate contains `npm ci` followed by `npm test`. | PASS: same. |
| Local gate, separate from workflow grade | PASS: one test. No GitHub Actions run. | PASS: one test. No GitHub Actions run. |

The tested wording did not distinguish the arms. The original criterion demanded `npm ci` in the workflow; installing dependencies as the gate's first step also provisions CI on a clean runner, so the scenario now accepts either. A follow-up on a no-CI uv fixture also found no defect in the old wording ([results](pressure-no-ci-uv-toolchain-results-2026-11-26.md)), so the wording change was dropped and only the scaffold TODO comment was kept, covered by the generated-workflow regression assertion.
