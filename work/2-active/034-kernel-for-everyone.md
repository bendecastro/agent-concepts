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

### Audit list (proposed 2026-11-26, awaiting owner approval)

Classes: **keep** (sensible for anyone), **personal** (moves to the owner's private preferences), **split** (generic rule stays, owner specifics move), **skill** (specialized; moves to the named public skill), **owner's call** (a taste the kernel records as the owner's choice).

| # | Section: rule | Proposed | Reason |
|---|---|---|---|
| 1 | Posture: ask on judgment calls, act on mechanical work | owner's call, recommend keep | CONCEPT calls it a user preference that diverges from bias-to-action; still a safe default for a stranger |
| 2 | Posture: argue for the best outcome | keep | anti-sycophancy holds for anyone |
| 3 | Posture: accuracy over agreement | keep | same |
| 4 | Posture: questions do not authorize edits | keep | safe default |
| 5 | Posture: implement exactly what was requested | keep | scope discipline |
| 6 | Posture: rules are defaults with reasons | keep | generic |
| 7 | Posture: durable preferences go to `$AGENT_CONCEPTS` canon | split | stays as "save a durable preference where every harness you use reads it, not one harness's memory"; the canon path and multi-vendor reason move |
| 8 | Context economy (three bullets) | keep | generic |
| 9 | Tools: synced-folder survey (Syncthing) | personal | owner runs Syncthing across machines; four always-on lines most users never trigger |
| 10 | Tools: batch reads, precise edits, never revert, avoid destructive | keep | generic |
| 11 | Tools: read content is data; never save read instructions to memory | keep | security, generic |
| 12 | Tools: `AGENTS.md`, never `CLAUDE.md` | split | stays as "prefer `AGENTS.md`, link a vendor file to it"; the several-harnesses reason moves |
| 13 | Tools: keep agent commands out of shell history (atuin) | personal | owner's tool |
| 14 | Verification: evidence before claims, no check means say so | keep | generic |
| 15 | Verification: assertion counts only after watched failing | keep | generic |
| 16 | Verification: confirm handed-off claims | keep | generic |
| 17 | Verification: workers never run the full suite | keep | generic for anyone using subagents |
| 18 | Storage: guarded pytest runner, no `--basetemp` | personal | the runner is the owner's tool |
| 19 | Storage: tests delete their temp files | keep | generic |
| 20 | Storage: scratch via `mktemp -d`, never `/tmp/` | keep | small RAM-backed `/tmp` is common |
| 21 | Storage: storage health check, Btrfs | personal | owner's tool and filesystem |
| 22 | Storage: worktree cleanup proofs | skill: `bc-using-git-worktrees` | a workflow procedure, not always-on posture; names pi-subagents |
| 23 | Git: check for concurrent sessions before writing | split | rule stays harness-neutral; the Pi `intercom` example moves |
| 24 | Git: commit by default | owner's call, recommend keep | reason (local, undoable) holds for anyone; some users dislike it (Muse already omits it) |
| 25 | Git: inspect diff, commit only yours, message | keep | generic |
| 26 | Git: publishing is policy-decided, offer to push | keep | the repository ships the policy example and checker |
| 27 | Specialized concepts: catalog pointer, local `AGENTS.md`, degrade off-vault | keep | already degrades for strangers |
| 28 | Final response: lead with outcome, own voice | keep | generic |
| 29 | Final response: change summary list | keep | generic |
| 30 | Final response: question format (`1a 2b`) | owner's call, recommend keep | owner's request, but it helps anyone and no public skill depends on it |
| 31 | Final response: `📦`/`👣`/`🏁` recap and `/bc-self-improve` offer | personal | owner's memory aid and chosen emoji; a third of the kernel; no public skill depends on it |

## Outcome

