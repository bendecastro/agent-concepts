# Keep only rules for everyone in the agent kernel

Why: The kernel is what a stranger copies into every session, but it also holds the owner's own tastes and tools (for example the emoji recap format, the `/bc-self-improve` offer, owner-only checks), so offering it at setup would push the owner's preferences onto everyone.
Done when: Every kernel rule is either kept as sensible for anyone (with its why) or moved to the owner's private preferences, with each move the owner approved recorded; the kernel's pressure-tested rules still hold; decision in `docs/decisions/0005-kernel-holds-rules-for-everyone.md`.
Stage: next
Blocked by: nothing
Kind: docs
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state
Planned: bc-plan-to-pipeline 2026-11-26
Needs owner: approve the keep/move list for each kernel rule before anything moves

## Requirements

- The audit classifies each kernel rule: **everyone** (stays, generic wording), **personal** (moves to the owner's private preferences, outside this repository), or **split** (a generic rule stays; the owner's specifics move to the private overlay).
- Moving a rule never weakens the owner's own setup: their always-on instructions keep loading it from the private home in the same change.
- Kernel copies the lint tracks (`kernel-copies.json`) are updated for the new text.
- Out of scope: rewording rules that stay; adding new rules.

## Steps

- [ ] Audit list: one line per kernel rule with class and reason, written into this item's Steps Notes and shown to the owner. Blocked by: nothing. Done when the owner has approved or changed each line. Out of scope: moving anything.
- [ ] Apply the approved moves: edit `concepts/agent-kernel/body/AGENT-KERNEL.md`, carry personal rules into the owner's private preferences, update the kernel copies and CONCEPT provenance. Blocked by: Audit list. Done when no approved-personal rule remains in the kernel, the owner's own instructions still contain each moved rule, kernel-copy lint warnings are resolved, and the pressure-tested kernel rules are unchanged in wording. Out of scope: re-running kernel pressure tests for unchanged rules.

## Outcome

