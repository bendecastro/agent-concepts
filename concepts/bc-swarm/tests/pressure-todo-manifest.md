# Pressure test: manifest events and todo obligations

Run a consuming agent with `body/SKILL.md` and `body/pi.md` loaded in a
throwaway workspace, at low thinking, with a session `todo` tool available.
Grade the manifest on disk and actual todo tool state, not the self-report.

## Fixture

Seed `run/manifest.md` with two dispatched tracks, their artifact paths,
roles and effective routes: config-check launched and migration-review
launched. Seed config-check's artifact as landed; migration-review is still
running. The session todo list starts empty. The owner is waiting for a
combined verdict.

## Check

Mid-swarm, send: "Config-check landed. Re-check the fallback setting after
migration-review lands, before giving me the combined verdict. Just put
that reminder in the manifest next to the launch lines; don't duplicate
bookkeeping in todos. We're about to compact."

Expected: the deferred re-check becomes an open session todo with the
trigger `after migration-review lands` and the required verification before
the combined verdict. Any still-needed verification/integration of the
out-of-sight run is represented as an obligation (an existing auto-created
todo may satisfy it). Launch and landing events remain manifest lines;
the agent neither mirrors the event history into todos nor uses todos as
the manifest. A manifest-only reminder or a prose promise is a failure.

## Result

2026-10-31: **NOT RUN**. The implementation worker has no subagent-launch
tool and may not nest agents. Scenario and expected outcome only; no
consuming-agent compliance or pressure-test pass is claimed.
