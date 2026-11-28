# Warn that a launch skill replaces a role's default skills on Pi

Why: on Pi, passing `skill` when launching a subagent replaces the role's default skills instead of adding to them. Only the owner's private routing skill says so (one public council skill knows it for itself), so a stranger who customises a launch silently drops safety skills. Evidence: the run folder `2026-11-28-private-to-public` (rules, pi-ext and concepts reports).
Stage: next
Blocked by: nothing
Kind: docs
Source: private-to-public audit 2026-11-28 (owner rec)
Dependencies: none new

## Requirements (not planned yet: run bc-plan-to-pipeline)

- One home for the warning in `bc-durable-subagents`'s Pi adapter; the council skill points to it.
