---
name: bc-swarm
description: Aggressively delegate investigation, analysis, and review to parallel subagents under a durability contract, so a lost tool result or a dead terminal never destroys the work. Use when the user says bc-swarm, swarm, go wide, fan out, or asks for heavy/aggressive subagent use.
---

# bc-swarm

Go wide. While this skill is active, delegating is the default and **keeping** work is what needs a reason.

It composes `dispatching-parallel-agents`, which owns how to split work, what goes in a packet, and the parent's integration duties. Read that for *how to split*. This skill covers *how hard to push* and *how not to lose the results*.

## The inversion

Normally you delegate when a split is obvious. Here it flips: assume every unit of work goes to a child, and justify what you keep.

The parent keeps exactly three things:

- **Decisions** — judgment calls, tradeoffs, anything the user would want to weigh.
- **Integration and verification** — reconciling children, spotting contradictions, running the combined check.
- **Work genuinely cheaper to do than to describe** — one grep, a single file read, a command whose output you need before you can even write the packet.

That third one is the honest escape hatch, and it is also the one that rots. Why: "it's faster if I just do it" is true for almost any single item and false for the whole task — it is how an aggressive posture decays into an ordinary one, one reasonable-sounding exception at a time. It is a **per-track** test, never a verdict on the whole job; applied to everything at once it is not a test, it is the rationalization.

**The tooth: name the tracks out loud at the decision point, and say where each one goes.** List the independent tracks you found. For every dispatched track, name the role and the model plus thinking level that will actually run it, in this session's routing names — not a vendor id. Shape: `notes → scout, Luna max`. Do not also label tracks as child or parent — the role already says it is dispatched. Why: the list is how the user sees the fleet; a track without a model is a guess they cannot correct, and parent/child is noise once the role is named. The list is a promise about the launch: if the harness lets you set model and thinking per child, set them to match. Do not announce a routing choice and then launch the role's bundled default. Announce, then launch in the same turn. If fewer than two tracks exist, or any track stays with you, say why in one line (`hotfix → cheaper than a packet`). Those kept tracks are not subagents.

This binds **whichever way you decide, including when you decide to dispatch nothing.** Why: keeping the work is the decision that silently ends the swarm, so it is the one that most needs saying out loud. A rule that only fires on the dispatch path cannot catch the case where you quietly chose not to dispatch — and "just read them yourself, it's faster than writing the packets" is precisely that case, arriving as a reasonable request.

## Durability contract

The parent's context is not a storage medium. A lost tool result, a compaction, or a dead terminal destroys it with no warning and no trace. The host is itself a failure domain: when a multiplexer pane or terminal window dies, every foreground child dies with it and leaves nothing behind. Assume the session can vanish between any two tool calls.

Four rules. They are cheap. The failure they prevent is not.

**1. Manifest before dispatch.** Before launching anything, write a scratch file listing each dispatched track: key → artifact path → role → model + thinking → one-line task. Then **state the run directory path in chat.** Why: a path that exists only in your context dies with your context, and rule 4 cannot fire without it. Telling the user makes the user your backup index. Model and thinking belong here too so the durable copy matches the chat list. Use the same routing names the user just read; the resolved registry id belongs on the dispatch call, not as a substitute in the manifest.

**2. Multi-child fan-out runs async.** Two or more children means async. This is a gate, not a preference. Why: foreground children are bound to the parent's lifetime and the returned tool result is their only delivery channel, so a single crash takes N children and N results atomically. Async runs are retained and stay inspectable after the parent is gone. "It's simpler blocking" is precisely the trade that produced this rule.

**3. Every child writes to its artifact, and checkpoints as it goes.** The artifact is the deliverable; the returned text is a summary of it. Children append findings as they establish them rather than composing one final write. Why: a child killed at minute four of five leaves nothing recoverable if it was holding everything for the end.

**4. Recover before relaunch.** When a result is missing or a run failed, check in this order — the manifest, then the artifact paths on disk, then the harness's retained runs — and only then re-dispatch, and only the tracks actually missing. Why: re-running a whole fan-out because one result didn't come back pays the full cost again to rediscover work that is usually already on disk.

Artifacts are scratch, not knowledge. Anything worth keeping gets explicitly promoted into the repo, a concept, or a note; the run directory is disposable by design.

## The thin-parent guard

Aggressive delegation buys speed by making the parent's context deliberately thin — which silently removes your ability to catch a child that is confidently wrong. You did not read the file, so you cannot feel the error.

**Children return claims with evidence anchors: a file path plus the quoted line carrying the claim.** Put this in the packet — it does not happen by default, and it is the half of the guard this skill owns.

Why anchors rather than trusting or re-reading: re-reading everything defeats the delegation, trusting everything scales confabulation with fan-out, and an anchor makes a spot-check cheap and constant per claim.

**The other half — not repeating an unverified claim as fact — is an always-on verification rule, not a swarm rule.** It lives in the base instructions (`agent-kernel`, under Verification) because it has to fire when nothing about the task looks like a fan-out: someone hands you a report, you are only asked to summarize, and the source was never yours to begin with. Tested 2026-08-18: stating it here did not make it fire; stating it in always-on context did. Do not re-add a copy of it to this skill — a duplicate that cannot fire only launders the obligation.

## What every child packet adds

`dispatching-parallel-agents` defines the packet (scope, goal, constraints, evidence, output contract). Under `bc-swarm`, add three lines:

```
- Write your findings to <artifact path>. Append them as you establish them; do not hold
  everything for a single write at the end.
- Anchor every claim: file path plus the quoted line that supports it.
- The returned summary is a summary of that file, never the only copy of your findings.
```

## Boundary

`bc-swarm` is for **investigation, analysis, and review** — reconnaissance, reading docs, cross-referencing, independent critique. Fan-out is cheap here because children only read.

For implementation fan-out, stop and use `subagent-driven-development` or `bc-drain-issues`. They already own worker packets, spec and standards review, worktree isolation, and rework loops. Why: a thinner parallel-implementation path competing with those will lose in ways nobody notices until something is merged.

Harness-specific mechanics, including the concrete dispatch syntax and observed failure modes, live in [pi.md](pi.md).
