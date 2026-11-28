# Deferred obligations survive without a private todo tool

Why: `bc-durable-subagents` tells the reader to record obligations in a session `todo` tool whose list is re-shown every turn. That tool is a private Pi extension the npm package does not ship, so a stranger has nowhere to keep "do X when Y" and loses deferred work. The rule to re-check each trigger before every report also exists only in the owner's private instructions. Evidence: the run folder `2026-11-28-private-to-public` (rules, pi-ext and concepts reports).
Stage: next
Blocked by: nothing
Kind: feature
Source: private-to-public audit 2026-11-28 (owner rec)
Dependencies: none new

## Requirements (not planned yet: run bc-plan-to-pipeline)

- A tool-independent home for obligations (for example a file in the run folder) when no todo tool exists; the todo tool stays the preferred home when present.
- The report-time re-check (each check-trigger and fired item, updated before the report) becomes a public rule in the same skill.
- Decide whether to ship the todo extension in the npm package instead; record the choice.
