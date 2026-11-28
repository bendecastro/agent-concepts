# Who ticks a work item's steps: the worker or the integrating session

Why: the owner's preferences tell each worker to tick its own steps and regenerate the index; `bc-pipeline-to-done` says only the driver writes results, never builders or reviewers. On a project that uses both, they conflict. Evidence: the run folder `2026-11-28-private-to-public` (rules, pi-ext and concepts reports).
Stage: next
Blocked by: nothing
Kind: feature
Source: private-to-public audit 2026-11-28 (owner rec)
Needs owner: choose who ticks steps (worker on landing, or driver after review), or separate a step's completion from its review result
Dependencies: none new

## Requirements (not planned yet: run bc-plan-to-pipeline)

- One rule in public, and the owner's preference brought in line with it.
