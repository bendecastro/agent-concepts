---
name: bc-swarm
description: Aggressively delegate investigation, analysis, and review to parallel subagents under a durability contract, so a lost tool result or a dead terminal never destroys the work. Use when the user says bc-swarm, swarm, go wide, fan out, or asks for heavy/aggressive subagent use.
---

# bc-swarm

Go wide. While this skill is active, delegating is the default and **keeping** work is what needs a reason.

It composes `dispatching-parallel-agents`, which owns how to split work, what goes in a packet, and the parent's integration duties. Read that for *how to split*. This skill covers *how hard to push* and *how not to lose the results*.

## Recovery gate — before routing

If a prompt names an interrupted, failed, empty, missing, or reaped prior run, treat it as recovery even when it says redo, relaunch, or start again. Stop before the Tooth or any replacement track, manifest, or dispatch decision and execute rule 4 for that prior run. Never stash, delete, move, or overwrite prior-run evidence merely to make a replacement launchable. Do not name or launch a replacement until recovery proves that track has no usable artifact, valid handoff patch, recorded Git object, or preserved worktree/ref.

## The inversion

Normally you delegate when a split is obvious. Here it flips: assume every unit of work goes to a child, and justify what you keep.

The parent keeps exactly three things:

- **Decisions** — judgment calls, tradeoffs, anything the user would want to weigh.
- **Integration and verification** — reconciling children, spotting contradictions, running the combined check.
- **Work genuinely cheaper to do than to describe** — one grep, a single file read, a command whose output you need before you can even write the packet.

That third one is the honest escape hatch, and it is also the one that rots. Why: "it's faster if I just do it" is true for almost any single item and false for the whole task — it is how an aggressive posture decays into an ordinary one, one reasonable-sounding exception at a time. It is a **per-track** test, never a verdict on the whole job; applied to everything at once it is not a test, it is the rationalization.

**The tooth: name the tracks out loud at the decision point, and say where each one goes.** List the independent tracks you found. For every dispatched track, name the role and the effective model plus thinking route, in this session's routing names — not a vendor id. Shape: `notes → scout, Luna max`. Do not also label tracks as child or parent — the role already says it is dispatched. Why: the list is how the user sees the fleet; a track without an effective route is a guess they cannot correct, and parent/child is noise once the role is named. The list records the route that will actually run, not a fixed set of fields that every harness must copy into every child object. If the harness exposes per-child model or thinking controls, use them to preserve that route through its own mechanics; read [pi.md](pi.md) for Pi-specific dispatch rules. Keep the effective route in chat and the manifest. Announce, then launch in the same turn. If fewer than two tracks exist, or any track stays with you, say why in one line (`hotfix → cheaper than a packet`). Those kept tracks are not subagents.

This binds **whichever way you decide, including when you decide to dispatch nothing.** Why: keeping the work is the decision that silently ends the swarm, so it is the one that most needs saying out loud. A rule that only fires on the dispatch path cannot catch the case where you quietly chose not to dispatch — and "just read them yourself, it's faster than writing the packets" is precisely that case, arriving as a reasonable request.

## Durability contract

The parent's context is not a storage medium. A lost tool result, a compaction, or a dead terminal destroys it with no warning and no trace. The host is itself a failure domain: when a multiplexer pane or terminal window dies, every foreground child dies with it and leaves nothing behind. Assume the session can vanish between any two tool calls.

Four rules. They are cheap. The failure they prevent is not.

**1. Manifest before dispatch.** Before launching anything, write a scratch file listing each dispatched track: key → artifact path → role → effective route (model + thinking) → one-line task. Then **state the run directory path in chat.** Why: a path that exists only in your context dies with your context, and rule 4 cannot fire without it. Telling the user makes the user your backup index. Record the same routing name the user just read so the durable copy matches. Preserve that route through whatever launch controls the harness provides; keep harness-specific field rules in its reference.

**2. Multi-child fan-out runs async.** Two or more children means async. This is a gate, not a preference. Why: foreground children are bound to the parent's lifetime and the returned tool result is their only delivery channel, so a single crash takes N children and N results atomically. Async runs are retained and stay inspectable after the parent is gone. "It's simpler blocking" is precisely the trade that produced this rule.

**3. Every child writes to its artifact, and checkpoints as it goes.** The artifact is the durable record of the deliverable; the returned text is a summary of it. For recon, the deliverable is the file. For a worktree worker, the deliverable is its commit plus the harness patch. Immediately after each commit, the worker appends these two start-of-line records to the artifact:

```text
Commit: <full 40-hex SHA> <subject>
Branch: <exact branch>
```

If no commit was made, it records `Commit: none` and `Branch: none`. The worker records the full SHA and exact branch on their own lines as soon as they exist; the returned summary alone does not count. Children append findings as they establish them rather than composing one final write. Why: a child killed at minute four of five leaves nothing recoverable if it was holding everything for the end, and a clean harness teardown can otherwise reap the branch containing the real deliverable.

**4. Recover before relaunch.** When a result is missing or a run failed, check in this order:

1. the manifest;
2. the artifact paths on disk;
3. the harness's retained runs, for output, artifact paths, and handoff paths only — a retained run cannot reopen a worktree that cleanup already removed;
4. for a worktree worker, the exact child entry in the runtime handoff JSON and its patch. A patch is usable only when it belongs to that exact child and branch (matching the expected `Branch:` record), is nonempty, says `changed: true`, has no capture error, and carries the expected `baseCommit` that resolves as a commit. Inspect it and require `git apply --check` before any mutation. Empty, error, mismatched, or wrong-base patches are not recovery;
5. the artifact's **last own-line `Commit:`/`Branch:` pair only** as an untrusted candidate; earlier pairs are evidence, not candidates. For a claimed commit, require the `Commit:` value to be a full 40-character lowercase-hex SHA and verify with Git that it resolves to a commit (`git cat-file -t` and `git rev-parse --verify`). Require the pair's `Branch:` value to equal the exact expected branch from the handoff. If that branch ref still exists, resolve it and require its tip to equal the candidate tip; its absence after successful cleanup is allowed. Require the handoff's expected `baseCommit` to resolve as a commit, inspect exactly one linear `baseCommit..tip` chain, and validate the resulting tree/diff before integration. Never integrate from prose, an abbreviated or non-resolving SHA, branch text alone, or tip alone. A `none`/`none` pair is only the no-commit case. If these checks succeed, recover the full linear `baseCommit..tip` range, not only the tip: if tip is already an ancestor of parent `HEAD`, it is integrated; if parent `HEAD` equals `baseCommit`, use a fast-forward-only merge; if parent advanced from that same base, inspect and cherry-pick the ordered range. Stop on non-linear or ambiguous history or conflict rather than guessing, then verify the resulting diff/tree;
6. a preserved worktree or ref, but only when cleanup refused and the harness says it was preserved;
7. `git fsck --no-reflogs --lost-found` only with that validated full SHA, and only to exact-match it — never browse or select dangling objects.

After applying a valid patch, verify the resulting diff/tree before any commit or report. An artifact for a worktree worker is usable only when its own-line `Commit:`/`Branch:` records are valid (`none`/`none` is valid when no commit was made). Re-dispatch only after this order, and only a track with no usable artifact, valid handoff patch, recorded commit object, or preserved worktree/ref. No patch plus no SHA does not license relaunch while a preserved worktree/ref exists. Why: the current harness normally captures a patch and then removes a cleanly handed-off worktree and branch, while preserved leftovers are exceptions; re-running a whole fan-out because one result did not come back pays the full cost again to rediscover work that is usually already on disk or in Git.

**Parent integration on receipt.** On the first turn a completed worktree result is in front of the parent — a completion wake, status poll, or user report — apply its validated handoff patch or integrate its validated full commit range before any other dispatch. This is completion-wake behavior, never a reason to block or wait on the launch turn; rule 2 remains intact.

Artifacts are scratch, not knowledge. Anything worth keeping gets explicitly promoted into the repo, a concept, or a note; the run directory is disposable by design. For worktree workers, the Git commit and harness patch are the durable handoff records used before that promotion.

## The thin-parent guard

Aggressive delegation buys speed by making the parent's context deliberately thin — which silently removes your ability to catch a child that is confidently wrong. You did not read the file, so you cannot feel the error.

**Children return claims with evidence anchors: a file path plus the quoted line carrying the claim.** Put this in the packet — it does not happen by default, and it is the half of the guard this skill owns.

Why anchors rather than trusting or re-reading: re-reading everything defeats the delegation, trusting everything scales confabulation with fan-out, and an anchor makes a spot-check cheap and constant per claim.

**The other half — not repeating an unverified claim as fact — is an always-on verification rule, not a swarm rule.** It lives in the base instructions (`agent-kernel`, under Verification) because it has to fire when nothing about the task looks like a fan-out: someone hands you a report, you are only asked to summarize, and the source was never yours to begin with. Tested 2026-08-18: stating it here did not make it fire; stating it in always-on context did. Do not re-add a copy of it to this skill — a duplicate that cannot fire only launders the obligation.

## What every child packet adds

`dispatching-parallel-agents` defines the packet (scope, goal, constraints, evidence, output contract). Under `bc-swarm`, add these bullets:

```
- Write your findings to <artifact path>. Append them as you establish them; do not hold
  everything for a single write at the end.
- Anchor every claim: file path plus the quoted line that supports it.
- The returned summary is a summary of that file, never the only copy of your findings.
- If you are a worktree worker: immediately after each commit, append to the artifact
  `Commit: <full 40-hex SHA> <subject>` and `Branch: <exact branch>` on their own,
  start-of-line records. If you made no commit, write `Commit: none` and `Branch: none`.
  The returned summary is not the only copy of those records.
```

The worktree requirement is scoped to worker packets; recon packets keep the first three bullets only.

## Boundary

`bc-swarm` is for **investigation, analysis, and review** — reconnaissance, reading docs, cross-referencing, independent critique. Fan-out is cheap here because children only read.

For implementation fan-out, stop and use `subagent-driven-development` or `bc-drain-issues`. They already own worker packets, spec and standards review, worktree isolation, and rework loops. Why: a thinner parallel-implementation path competing with those will lose in ways nobody notices until something is merged.

Harness-specific mechanics, including the concrete dispatch syntax and observed failure modes, live in [pi.md](pi.md).
