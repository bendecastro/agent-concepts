---
name: bc-durable-subagents
description: Durability contract for any run that launches subagents, so a lost tool result, a compaction or a dead terminal never destroys the work - run folder and manifest before dispatch, async fan-out, per-child artifacts with Commit/Branch records, evidence anchors, and recovery before relaunch. Use before launching subagents, and whenever a prior subagent run was interrupted, failed, came back empty or was reaped.
---

# bc-durable-subagents

If `~/.config/agent-concepts/overlays/bc-durable-subagents.md` exists, read it: it supplies tool names for the generic steps below that this machine's agent instructions do not already name. It never changes behaviour, and the project's own instructions take precedence.

Any skill that launches subagents loads this one. It covers how not to lose the results; how hard to delegate and how to split the work belong to the launching skill. The rules are harness-neutral; Pi mechanics (run directory, dispatch syntax, observed failure modes, recovery commands) are in [pi.md](pi.md).

Load `bc-safe-runs`. Else: guarded test runner (fallback `pytest`; no custom `--basetemp`), `mktemp -d` outside `/tmp`, targeted tests; configured storage check before full suites, worktrees, fan-out: stop if critical or unknown, or if the check cannot run.

Put the `bc-safe-runs` packet line in every worker or reviewer task. Before removing a worktree or deleting its branch, prove its commits are in `HEAD` (ancestor or patch-equivalent) and record that proof. Why: children do not inherit the kernel, and retained worktrees consume storage.

## Recovery rule — before anything else

If a prompt names an interrupted, failed, empty, missing, or reaped prior run, treat it as recovery even when it says redo, relaunch, or start again. Stop before naming tracks or making any replacement track, manifest, or dispatch decision, and execute rule 4 of the durability contract for that prior run. Never stash, delete, move, or overwrite prior-run evidence merely to make a replacement launchable. Do not name or launch a replacement until recovery proves that track has no usable artifact, valid handoff patch, recorded Git object, or preserved worktree/ref.

## Durability contract

The parent's context is not a storage medium. A lost tool result, a compaction, or a dead terminal destroys it with no warning and no trace. The host is itself a failure domain: when a multiplexer pane or terminal window dies, every foreground child dies with it and leaves nothing behind. Assume the session can vanish between any two tool calls.

Four rules. They are cheap. The failure they prevent is not.

**1. Manifest before dispatch.** Before launching anything, write a scratch file listing each dispatched track: key → artifact path → role → effective route (model + thinking) → one-line task. Then **state the run directory path in chat.** Why: a path that exists only in your context dies with your context, and rule 4 cannot fire without it. Telling the user makes the user your backup index. Record the same routing name the user just read so the durable copy matches. Preserve that route through whatever launch controls the harness provides; keep harness-specific field rules in its reference.

**Manifest events, todo obligations.** The run manifest records events — dispatched, launched, landed, recovered — as durable history; the session `todo` tool tracks open obligations that outlive the turn (owner waits, deferred items, out-of-sight runs, partial work), with a trigger for deferred checks. They are complementary: do not copy the manifest into todos or use todos as the manifest; later verification or integration of a dispatched run is a todo obligation (which may auto-create from the run), while its launch/landing is a manifest line. Why: a deferred item left only in the manifest was never re-checked after compaction; the todo snapshot is re-injected every turn, the manifest is not.

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
5. the artifact's **last own-line `Commit:`/`Branch:` pair only** as an untrusted candidate; earlier pairs are evidence, not candidates. For a claimed commit, require the `Commit:` value to be a full 40-character lowercase-hex SHA and verify with Git that it resolves to a commit (`git cat-file -t` and `git rev-parse --verify`). Require the pair's `Branch:` value to equal the exact expected branch from the handoff. If that branch ref still exists, resolve it and require its tip to equal the candidate tip; its absence after successful cleanup is allowed. Require the handoff's expected `baseCommit` to resolve as a commit, inspect exactly one linear `baseCommit..tip` chain, and validate the resulting tree/diff before integration. Never integrate from prose, an abbreviated or non-resolving SHA, branch text alone, or tip alone. A `none`/`none` pair is only the no-commit case. If these checks succeed, recover the full linear `baseCommit..tip` range, not only the tip: if tip is already an ancestor of parent `HEAD`, it is integrated; if parent `HEAD` equals `baseCommit`, use a fast-forward-only merge; if parent advanced from that same base, inspect and cherry-pick the ordered range. Stop on non-linear or ambiguous history or conflict rather than guessing, then verify the resulting diff/tree and record the ancestry/patch-equivalence proof in the manifest before cleanup;
6. a preserved worktree or ref, but only when cleanup refused and the harness says it was preserved;
7. `git fsck --no-reflogs --lost-found` only with that validated full SHA, and only to exact-match it — never browse or select dangling objects.

After applying a valid patch, verify the resulting diff/tree before any commit or report. An artifact for a worktree worker is usable only when its own-line `Commit:`/`Branch:` records are valid (`none`/`none` is valid when no commit was made). Re-dispatch only after this order, and only a track with no usable artifact, valid handoff patch, recorded commit object, or preserved worktree/ref. No patch plus no SHA does not license relaunch while a preserved worktree/ref exists. Why: the current harness normally captures a patch and then removes a cleanly handed-off worktree and branch, while preserved leftovers are exceptions; re-running a whole fan-out because one result did not come back pays the full cost again to rediscover work that is usually already on disk or in Git.

**Parent integration on receipt.** On the first turn a completed worktree result is in front of the parent — a completion wake, status poll, or user report — apply its validated handoff patch or integrate its validated full commit range before any other dispatch. This is completion-wake behavior, never a reason to block or wait on the launch turn; rule 2 remains intact.

**Full gate on the integrated tree.** After integrating, start the project's full gate (through the project's or machine's offload/heavy-run wrapper if its instructions name one; otherwise run the gate directly) in the background with a completion wake, and dispatch the independent reviewer on the same tree in parallel; record the tree SHA (`git rev-parse HEAD^{tree}`) and the gate result. The reviewer reports the gate as pending; the parent combines the gate result with the review verdict before landing. Never wait with sleep or poll loops. Why: the gate and the review are independent, so running them in sequence doubles the wait.

Artifacts are scratch, not knowledge. Anything worth keeping gets explicitly promoted into the repo, a concept, or a note; the run directory is disposable by design. For worktree workers, the Git commit and harness patch are the durable handoff records used before that promotion.

## Evidence anchors

Aggressive delegation buys speed by making the parent's context deliberately thin — which silently removes your ability to catch a child that is confidently wrong. You did not read the file, so you cannot feel the error.

**Children return claims with evidence anchors: a file path plus the quoted line carrying the claim.** Put this in the packet — it does not happen by default, and it is the half of the guard this skill owns.

Why anchors rather than trusting or re-reading: re-reading everything defeats the delegation, trusting everything scales confabulation with fan-out, and an anchor makes a spot-check cheap and constant per claim.

**The other half — not repeating an unverified claim as fact — is an always-on verification rule, not a swarm rule.** It lives in the base instructions (`agent-kernel`, under Verification) because it has to fire when nothing about the task looks like a fan-out: someone hands you a report, you are only asked to summarize, and the source was never yours to begin with. Tested 2026-08-18: stating it here did not make it fire; stating it in always-on context did. Do not re-add a copy of it to this skill — a duplicate that cannot fire only launders the obligation.

## What every child packet adds

`bc-dispatching-parallel-agents` defines the packet (scope, goal, constraints, evidence, output contract). Every child packet adds these bullets:

```
- Write your findings to <artifact path>. Append them as you establish them; do not hold
  everything for a single write at the end.
- Anchor every claim: file path plus the quoted line that supports it.
- The returned summary is a summary of that file, never the only copy of your findings.
- If you are a worktree worker: immediately after each commit, append to the artifact
  `Commit: <full 40-hex SHA> <subject>` and `Branch: <exact branch>` on their own,
  start-of-line records. If you made no commit, write `Commit: none` and `Branch: none`.
  The returned summary is not the only copy of those records.
- For implementation/testing: follow kernel Storage safety; run pytest through
  the configured guarded runner or, if absent, plain `pytest` with `tmp_path`
  for test fixtures and cleanup even on failure. Never use custom `--basetemp`. Run only these targeted checks: <test files or IDs, typecheck, lint>.
  No browser/e2e tests and no full gate; the parent runs it on the integrated tree.
  Why: fresh workers must not multiply full suites or unmanaged test roots.
```

Name the guarded runner from the project's or machine's instructions and docs, if configured. Fill the targeted checks with named test files or IDs; never paste the project's full gate into a packet, even when its validation page lists the gate. Why: a pasted gate is a full run per worker. The worktree requirement is scoped to worker packets; recon packets keep the first three bullets only.
