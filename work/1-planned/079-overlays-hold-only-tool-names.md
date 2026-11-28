# Private overlays hold only tool names

Why: overlays are meant to name only the owner's tools. The `bc-pipeline-to-done` overlay states behaviour and overrides a public default, and the `bc-tdd` overlay states prohibitions and timing rules, so the owner's agents follow rules strangers never see. Evidence: the run folder `2026-11-28-private-to-public` (rules, pi-ext and concepts reports).
Stage: next
Blocked by: nothing
Kind: feature
Source: private-to-public audit 2026-11-28 (owner rec)
Dependencies: none new

## Requirements (not planned yet: run bc-plan-to-pipeline)

- Each rule in an overlay either moves into the public body (generic form), into the owner's preferences (personal), or is dropped; overlays keep tool names and invocation forms only.
- Consider a lint warning for imperative rule language in overlays when the private folder exists.
