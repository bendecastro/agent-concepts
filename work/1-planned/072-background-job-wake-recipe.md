# A portable way to resume when a background job finishes

Why: `bc-durable-subagents` requires a completion wake for the background full gate, but only the owner's private wake helper arranges one for a shell job; native subagent wakes do not cover it. A stranger's agent polls or waits for the user. Evidence: the run folder `2026-11-28-private-to-public` (rules, pi-ext and concepts reports).
Stage: next
Blocked by: nothing
Kind: feature
Source: private-to-public audit 2026-11-28 (owner rec)
Dependencies: none new

## Requirements (not planned yet: run bc-plan-to-pipeline)

- Detect whether the harness can wake the session on a job's completion; give a portable recipe where it can (for example running the job as a subagent task, or a marker file plus the harness's own wake), and a stated manual-resume fallback where it cannot.
- The wake message names the next action and re-checks authority, as the private one does.
