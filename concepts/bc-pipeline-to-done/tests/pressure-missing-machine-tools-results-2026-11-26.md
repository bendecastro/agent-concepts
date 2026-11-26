# Missing machine tools: dry-run results

[Scenario](scenario-missing-machine-tools.md), 2026-11-26. One completed headless Terra low dry run per arm (n=1 each), with four simulated cases in each plan. Comparison used the body at `7cd82c3`; treatment used the revised body. The first startup attempt in each arm rejected a CLI flag before any consumer session; the one retry per arm omitted that flag and completed. Extensions and MCP were disabled; the only enabled tools were read and write. Deployed skills, private overlays, all three concept roots and the other arm were hidden.

| Criterion | Body at `7cd82c3` | Revised body |
| --- | --- | --- |
| A. Pi has no subagent tool | Fail: planned an early stop but gave no installation or restart guidance. | Pass: planned an early stop and named `pi-subagents` and restarting Pi. |
| B. Reviewer job has no role | Fail: planned an early stop without a pointer to configure a role from the examples. | Pass: named the missing reviewer job and the example profiles; did not substitute the driver. |
| C. No optional storage or runner tools | Fail: skipped the absent check but then stopped because pytest had no guarded runner. | Pass: planned to skip and report the absent check, use distinct jobs and pass plain `pytest`, `tmp_path`, cleanup on failure and no custom `--basetemp` in the builder packet. |
| D. Configured check cannot run | Pass: planned to stop before work or baseline because health was unknown. | Pass: planned to stop and report the configured check's failure, without treating it as absence. |
| Only the plan was written | Pass. | Pass. |

Graded from the plans and session traces: 2/5 comparison, 5/5 treatment. The comparison read only its own copied contract files; the treatment made no read calls. Both wrote only `plan.md`. Claims, checks, launches, reviews and landing were planned, not executed. No live pipeline run or configured guarded-runner execution was tested.
