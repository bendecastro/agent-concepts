# Find which local pi-subagents patches change behaviour strangers rely on

Why: the owner's Pi reapplies local patches to `pi-subagents` (the private `bc-subagents-carry-patches` extension), and strangers install the stock package. Nobody has checked which patches change behaviour the public skills assume, so the owner's subagent experience may differ from a stranger's. Evidence: the run folder `2026-11-28-private-to-public` (rules, pi-ext and concepts reports).
Stage: next
Blocked by: nothing
Kind: tests
Source: private-to-public audit 2026-11-28 (owner rec)
Dependencies: none new

## Requirements (not planned yet: run bc-plan-to-pipeline)

- List every carried patch with what it changes, and for each: cosmetic, owner-only, or a behaviour a public skill relies on.
- For each behaviour a public skill relies on: upstream it, ship it, or change the skill to work on stock pi-subagents; file each as an item.
- Check the stock version with the stranger sandbox, not the owner's install.
