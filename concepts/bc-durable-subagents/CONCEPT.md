---
test_kind: pressure
test_status: pass # 2026-11-28 post-split recovery, manifest and packet scenarios: with PASS 4/4, without FAIL 4/4 (Terra low)
tested: 2026-11-28
deployed: 2026-11-28
---
# Concept: bc-durable-subagents

The durability contract for any run that launches subagents: a run folder and
manifest written before dispatch and announced in chat, async execution for
two or more children, per-child artifacts appended as the child works
(worktree workers add own-line `Commit:`/`Branch:` records), evidence anchors
on child claims, the packet bullets that carry those duties to children, and
recovery before relaunch (manifest, artifacts, retained runs, the exact
handoff patch, the last Git-verified commit record, preserved state, then
re-dispatch only what is truly missing). Pi mechanics live in `body/pi.md`;
the entry file is harness-neutral.

Job B of the 2026-11-28 split of `bc-delegate-investigation` (work item
053-split-swarm-and-durable-subagents); job A, the delegate-by-default posture,
is `bc-swarm`, which loads this skill in one line. Step 2 of that item makes
the other launching skills load it too.

## Design decisions

- **Split out of the swarm posture (2026-11-28, owner decision in bc-self-improve 2026-11-27).** The rules had three drifting copies (the swarm skill, the Pi swarm-mode prompt, `bc-pipeline-to-done`), and skills that launch children without going wide (councils, subagent-driven development) had none; the 2026-11-27 council ran without a run folder until the parent made one by hand. One home that every launcher loads replaces the copies. This reverses the old "one concept, not two" decision recorded in `bc-swarm`'s CONCEPT, whose condition ("the day something else needs it") has arrived.
- **Moved verbatim.** The Durability contract, Recovery rule, Evidence anchors and packet bullets are the text that held in the earlier pressure runs, moved without rewording except for references to the routing decision (now "naming tracks") and the owning skill's name. The full design history of each rule (async as a gate, checkpointing from the 2026-08-18 pane loss, Commit/Branch identity from the 2026-08-25 reaped worktree, last-pair selection from 2026-09-02, recovery before routing) stays in [bc-swarm's CONCEPT](../bc-swarm/CONCEPT.md) where it was written.
- **Storage packet line and full gate live here.** The `bc-safe-runs` load, its packet line, the targeted-checks packet bullet and the background full gate on the integrated tree go with the packets and integration duty every launcher shares, so a council or a single worker gets them without the swarm posture. Test levels packet rules stay with `bc-swarm` (they are not durability).
- **Private overlay follows the rules it names.** The overlay supplies the full-gate wrapper, so its path is now `~/.config/agent-concepts/overlays/bc-durable-subagents.md`. Moving the owner's file is step 3 of item 053 (outside the repository).

## Provenance

- [bc-swarm CONCEPT](../bc-swarm/CONCEPT.md) (formerly `bc-delegate-investigation`): every rule's origin, incidents and earlier pressure runs.
- Work item `053-split-swarm-and-durable-subagents` (requirements for the split).
- Pi mechanics in `body/pi.md`: observed `pi-subagents` behaviour on this machine, recorded in its failure-mode notes.

## Tests

Moved here with their rules (history stays valid; they were run against the pre-split body):
[todo/manifest](tests/pressure-todo-manifest.md), [inline storage](tests/pressure-inline-storage-2026-11-25.md),
[targeted packets](tests/pressure-targeted-packets.md), [private overlay](tests/pressure-private-overlay.md).
The post-split rerun of the recovery, manifest and packet scenarios is in
[tests/pressure-split-2026-11-28.md](tests/pressure-split-2026-11-28.md).

## Deploy targets

Deployed 2026-11-28 via `scripts/deploy-local-skills.py` from the main checkout after integration: shared bus `~/.agents/skills/bc-durable-subagents`, Pi `~/.pi/agent/skills/bc-durable-subagents` and Claude Code `~/.claude/skills/bc-durable-subagents`, each a relative symlink to `body/`; also shipped in the npm package through `concepts/public-skills.json`. Other harnesses: manual bootstrap; see `../../docs/guides/harnesses.md`.
