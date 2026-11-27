# Pi stranger end-to-end test

**Status: live run not executed.** The [recipe](../../../scripts/stranger-end-to-end.md) and [fixture generator](../../../scripts/stranger_fixture.py) are ready for a driver-run attempt. This report records a deterministic sandbox preflight, not a dry run or a model test. One initial preflight and one corrected preflight ran; zero model requests, zero comparison/treatment arms and zero pipeline jobs ran.

The corrected preflight started Pi 1.6.1 in a mount namespace with a new HOME. It verified readable empty instruction files, absence of host homes and private concept configuration, and no `bc-*` helpers on PATH. Pi reported the selected `openai-codex/gpt-6.1-terra` model and locally ready credentials, without making a model request; low thinking was selected for the future run, not used. The public release was not installed in this preflight.

| Artifact or behavior | Grade | Evidence |
| --- | --- | --- |
| Generated starting repository | Pass | [Corrected preflight](evidence/sandbox-preflight.txt) shows a clean `main`, a local `origin`, and the starter commit on bare `main`. The fixture unit test verifies the exact initial tracked files (no CI), the tracking branch and the two baseline tests. |
| Setup writes project files and produces a runnable local gate | Not run | No setup session. |
| Planning writes an agent-ready item | Not run | No planning session. |
| A feature commit lands on bare `origin/main` | Not run | The only observed bare-remote commit is the fixture seed, not a feature commit. |
| Whether a worker ran the full suite | Not observed | No pipeline workers or transcripts. |

## Stalls and stops

| Point | Evidence | Disposition |
| --- | --- | --- |
| First preflight: mask and auth command | Pi printed `EACCES: permission denied, open '/box/home/.pi/agent/APPEND_SYSTEM.md'` and `Unknown option: --no-refresh`. | Fixed in the recipe: read-only regular masks sourced from `/dev/null`, and `pi auth check` with its subcommand options after `check`. The corrected preflight passed. |
| Before the README install and live phases | The worker run did not authorize a release installation via GitHub or spawning the pipeline's required child roles. | Driver runs the live recipe in the isolated test environment. This is a run constraint, not an observed product stall; no skill defect is inferred. |

No consumer process was started, so no session directory or system prompt existed to audit or copy. Only the corrected preflight excerpt is included here; temporary homes and fixture repositories were deleted after preflight evidence was saved.
