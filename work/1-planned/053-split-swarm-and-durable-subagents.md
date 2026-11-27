# Split bc-delegate-investigation into bc-swarm and bc-durable-subagents, and give every launching skill the durability rules

Why: `bc-delegate-investigation` does two jobs under a name that fits neither the way the owner calls it ("swarm", "go wide") nor how swarm mode uses it. Its durability rules (run folder, manifest, artifacts, Commit/Branch records, recovery before relaunch) have three drifting copies: the skill, the Pi swarm-mode prompt, and `bc-pipeline-to-done`. Other skills that launch children have none, so the 2026-11-27 council ran with no run folder until the parent made one by hand.
Done when: `bc-durable-subagents` holds the durability contract and today's `pi.md`; `bc-swarm` holds the delegate-by-default posture and loads it; every skill that launches children loads `bc-durable-subagents` instead of restating it; the Pi swarm-mode prompt points to it instead of carrying a copy; the old name still resolves through the rename policy; and the affected pressure scenarios pass on the new skills.
Stage: later
Blocked by: 051-renamed-skill-aliases, 054-safe-runs-module
Kind: architecture
Source: bc-self-improve 2026-11-27, owner picked split + rename and "add job B to the other skills that could use it"
Planned: bc-plan-to-pipeline 2026-11-27

## Requirements

- Job B (`bc-durable-subagents`): the Durability contract and Recovery rule sections of today's SKILL.md, the Evidence anchors and packet bullets that serve durability (Commit/Branch records, append-as-you-go), and all of `body/pi.md`. Harness-neutral entry file; Pi mechanics stay a linked file.
- Job A (`bc-swarm`): the inversion, the routing decision, keep cases, fan-out width, the read-only boundary; one line loading `bc-durable-subagents`. Description keeps the triggers swarm, go wide, fan out.
- Callers that load job B with a `loads` edge in `concepts/relationships.json` (check each actually launches children before adding): `bc-council-mode` (and through it `bc-council-chain`, `bc-council-find-bugs`, `bc-council-improve-architecture`, `bc-council-challenge-plan`), `bc-subagent-driven-development`, `bc-dispatching-parallel-agents`, `bc-pipeline-to-done` (keep its drain-specific run state; replace only the overlapping generic rules), and `bc-handoff`'s pointer. Account for every edge in each RELATIONSHIPS.md.
- Outside the repo (parent or owner, not a worker): `~/.pi/agent/extensions/swarm-mode/kernel.md` replaces its durability copy with "load `bc-durable-subagents`" and fixes the stale words listed in `work/0-ideas.md` (then delete that ideas line); the private overlay and `pi-subagent-routing` follow the rename. Keep the extension prompt constant within a session (extensions AGENTS.md cache rule).
- Rename through 051's policy: `bc-delegate-investigation` stays an alias for at least one minor release; CHANGELOG Renamed entry.

## Steps

- [ ] Create `bc-durable-subagents` and `bc-swarm` from the current body, with the alias. Done when lint passes, the alias loads `bc-swarm`, and the recovery, manifest and packet pressure scenarios from `concepts/bc-delegate-investigation/tests/` pass against the new skills on the pressure-test model.
- [ ] Make every launching skill load `bc-durable-subagents`. Done when each caller has its `loads` edge and one line in its body, the council skill creates a run folder and manifest in a dry-run plan, and lint passes.
- [ ] Point the swarm-mode prompt and private files at the new skills. Done when the swarm prompt holds no durability copy and a fresh Pi session in swarm mode reads `bc-durable-subagents` before its first launch.

## Outcome

_To be filled when finished or dropped._
