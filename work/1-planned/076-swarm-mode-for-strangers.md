# Should strangers get a delegate-by-default mode

Why: the owner works in a private swarm mode that delegates implementation to workers in worktrees by default. Public `bc-swarm` only does reconnaissance and review, on purpose, so a stranger never gets the way the owner works. Whether that should change is an unsettled design question. Evidence: the run folder `2026-11-28-private-to-public` (rules, pi-ext and concepts reports).
Stage: later
Blocked by: nothing
Kind: map
Source: private-to-public audit 2026-11-28 (owner rec)
Dependencies: none new

## Requirements (not planned yet: run bc-plan-to-pipeline as a map)

- Destination: a decision on whether, and how, strangers can opt into delegate-by-default implementation, without bypassing review gates.
- Open questions: cost to strangers' quotas; which harnesses can host it; what of the private swarm text is already public (`bc-swarm`, `bc-durable-subagents`).
