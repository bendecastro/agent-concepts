---
name: bc-swarm
description: Aggressively delegate investigation, analysis, and review to parallel subagents; delegating is the default and keeping work needs a reason. Use when the user says bc-swarm, swarm, go wide, fan out, or asks for heavy/aggressive subagent use.
---

# bc-swarm

Go wide. While this skill is active, delegating is the default and **keeping** work is what needs a reason.

Load `bc-durable-subagents` and follow it for every launch and every recovery: run folder, manifest, async fan-out, artifacts, packet bullets, recovery before relaunch. Its recovery rule runs before the routing decision below.

It composes `bc-dispatching-parallel-agents`, which owns how to split work, what goes in a packet, and the parent's integration duties. Read that for *how to split*. This skill covers *how hard to push*.

## The inversion

Normally you delegate when a split is obvious. Here it flips: assume every unit of work goes to a child, and justify what you keep.

The parent keeps exactly three things:

- **Decisions** — judgment calls, tradeoffs, anything the user would want to weigh.
- **Integration and verification** — reconciling children, spotting contradictions, running the combined check.
- **Work genuinely cheaper to do than to describe** — one grep, a single file read, a command whose output you need before you can even write the packet.

That third one is the honest escape hatch, and it is also the one that rots. Why: "it's faster if I just do it" is true for almost any single item and false for the whole task — it is how an aggressive posture decays into an ordinary one, one reasonable-sounding exception at a time. It is a **per-track** test, never a verdict on the whole job; applied to everything at once it is not a test, it is the rationalization.

**The routing decision: name the tracks at the decision point, and decide where each one goes.** List the independent tracks you found; show the dispatched ones in chat. For every dispatched track, name the role and the effective model plus thinking route, in this session's routing names — not a vendor id. Shape: `notes → scout, Luna max`. Do not also label tracks as child or parent — the role already says it is dispatched. Why: the list is how the user sees the fleet; a track without an effective route is a guess they cannot correct, and parent/child is noise once the role is named. The list records the route that will actually run, not a fixed set of fields that every harness must copy into every child object. If the harness exposes per-child model or thinking controls, use them to preserve that route through its own mechanics; read the `pi.md` file of `bc-durable-subagents` for Pi-specific dispatch rules. Keep the effective route in chat and the manifest. Announce, then launch in the same turn. If fewer than two tracks exist, or any track stays with you, settle why per track in your reasoning (`hotfix → cheaper than a packet`) and do not write it in the reply. Those kept tracks are not subagents. Why: the user does not want a keep/no-dispatch justification heading every reply (2026-10-26); the reason still has to exist and fit the three keep cases above.

This binds **whichever way you decide, including when you decide to dispatch nothing.** Why: keeping the work is the decision that silently ends the swarm, so it is the one that most needs an explicit reason, even one kept out of the reply. A rule that only fires on the dispatch path cannot catch the case where you quietly chose not to dispatch — and "just read them yourself, it's faster than writing the packets" is precisely that case, arriving as a reasonable request.

## Fan-out width

One child for a bounded fact or single-file read, two to four for comparisons and multi-surface recon, and more only for genuinely broad investigation. The default settles whether to delegate, never how wide. Why: multi-agent runs cost roughly 15x a single session, and an uncapped default drifts toward five children for a two-file question.

## What bc-swarm packets add

Every packet carries the bullets from `bc-durable-subagents`. For code changes, add:

**Test levels travel with the code** (load the `bc-tdd` skill, section Test levels):

- A worker packet never waives, narrows or forbids a tdd test level or its property library ("examples are enough", "no new dependency") unless it quotes the owner's approval. A parent that thinks a level is wrong for the task asks the owner. Why: a packet that overrides a level is a skip nobody approved, and the worker follows the packet.
- A review packet includes the worker's Test levels block, or the commits' `Test-levels:` trailers, and asks the reviewer to audit it against the diff. Why: a reviewer given only diff and spec never sees the levels, so nobody audits them.
- The parent's own commits of code changes carry the block too.

## Boundary

`bc-swarm` is for **investigation, analysis, and review** — reconnaissance, reading docs, cross-referencing, independent critique. Fan-out is cheap here because children only read.

For implementation fan-out, stop and use `bc-subagent-driven-development` or `bc-pipeline-to-done`. They already own worker packets, spec and standards review, worktree isolation, and rework loops. Why: a thinner parallel-implementation path competing with those will lose in ways nobody notices until something is merged.

Harness-specific mechanics, including the concrete dispatch syntax and observed failure modes, live in the `pi.md` file of `bc-durable-subagents`.
