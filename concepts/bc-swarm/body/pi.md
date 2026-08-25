# Pi mechanics for bc-swarm

Concrete syntax for the `subagent` tool from the `pi-subagents` extension. The contract in `SKILL.md` is harness-neutral; this file is not. In a harness without these primitives, keep the four rules and use whatever the harness offers for durable output and retained runs.

## Run directory

```
${TMPDIR:-/tmp}/bc-swarm/<YYYY-MM-DD>-<slug>/
```

`mkdir -p` it **before** dispatch. A child cannot write to a directory that does not exist, and it discovers this at the end of its run, which is the worst possible moment. The manifest goes at `manifest.md` in that root.

## Fan-out

```js
subagent({
  async: true,
  workflowScript: `
    const OUT = "/tmp/bc-swarm/2026-08-18-dsh-recon/";
    return await runs.all([
      { key: "notes", agent: "scout", thinking: "max", output: OUT + "notes.md", task: "..." },
      { key: "docs",  agent: "scout", thinking: "max", output: OUT + "docs.md",  task: "..." },
    ]);
  `
})
```

`output` is per child and must be distinct. The path is injected into the child as an authoritative override, so the child does not need to be told the path twice in its task text — but it does need to be told to *append as it goes*.

Pick roles by authority, not convenience: `scout` for bounded recon, `researcher` for external facts, `reviewer` for independent critique, `oracle` for hard judgment. Fan-out of `scout` children is the common shape.

Pass `thinking` on each child to match the announced line. Pass `model` only as a registry id you have resolved (`subagent({ action: "models" })` or this session's routing table). Chat and the manifest keep the routing name (`Luna max`); `model: "luna"` is not a registry id and fails closed (`Unknown subagent model 'luna'`). Role frontmatter can disagree with this session's routing — bundled `scout` thinking is `low`.

## Failure modes observed on this machine

**Children silently share one default output path.** Omitting `output` makes every child resolve to the same configured default (`<cwd>/context.md`), and the workflow aborts with `Workflow children 'notes' and 'docs' resolve output to the same path`. Always set `output` explicitly per child. This one fails cheaply — under 100ms — but it aborts the entire fan-out before any child runs.

**A blocking fan-out loses everything at once.** 2026-08-18: five `scout` children launched with `async:false`. The Herdr pane hosting the session died and had to be reopened; the parent and all five foreground children went with it. `coredumpctl` showed no dump and `systemd-oomd` logged no kill — no segfault, no memory exhaustion, the host container simply vanished. Afterwards `children.list` retained nothing, no artifact had been written, and the tool result returned `[no tool result recorded]`. Total recoverable output: zero, from five children. This is the evidence behind rule 2.

## Worktree lifecycle (pi-subagents 0.56.0)

A successful managed-worktree handoff captures the child diff as a patch and records
it in the runtime handoff JSON, then removes the temporary worktree and its
`pi-parallel-*` branch. Preserved worktrees or branches are exceptions: cleanup
refused because the child was dirty/divergent, capture was missing, or a retained
child still needs its managed CWD. Do not infer retention from a successful
handoff, and do not treat a cleaned worktree as resumable.

## Recovery, in order

Use the recorded paths and SHA; do not guess from temporary-directory names.

```sh
# 1. What was dispatched.
cat "$RUN_DIR/manifest.md"

# 2. Which declared artifacts exist and contain records.
find "$RUN_DIR" -maxdepth 3 -type f -print | sort
# Read each artifact path from the manifest; inspect its own-line Commit:/Branch: records.

# 3. Ask Pi for retained output, artifactPaths, and the handoff path.
#    Run this as a subagent tool call, not as a filesystem guess:
#    subagent({ action: "children.list" })

# 4. Worktree tracks only: inspect the handoff JSON and patch paths exposed by
#    artifactPaths or the handoff manifest. Apply a usable patch first:
git -C "$REPO" apply --check "$PATCH"
git -C "$REPO" apply "$PATCH"

# 5. If there is no usable patch, resolve the artifact's recorded full SHA.
git -C "$REPO" cat-file -t "$SHA"
git -C "$REPO" rev-parse --verify "$SHA^{commit}"
# If the object exists, integrate it without relaunching:
git -C "$REPO" cherry-pick "$SHA"

# 6. Only when the handoff says cleanup was refused, inspect preserved state.
git -C "$REPO" worktree list
git -C "$REPO" branch --list "$BRANCH"

# 7. Last resort: match the SHA already recorded in the artifact. Never run
#    fsck to browse dangling objects or choose a commit without that SHA.
git -C "$REPO" fsck --no-reflogs --lost-found | grep -F -- "$SHA"

# 8. Re-dispatch only the track with no usable patch, recorded object, or
#    preserved worktree/ref. No patch plus no recorded SHA means re-dispatch
#    only that track.
```

`$PATCH`, `$SHA`, and `$BRANCH` above come from the artifact and runtime handoff;
they are not values inferred from a guessed `/tmp` name. A retained run can supply
artifact and handoff paths, but cannot reopen a worktree whose cleanup already
removed it. If the patch applies, verify the resulting tree before committing; if
only the recorded commit survives, cherry-pick it after `cat-file`/`rev-parse`
verification. The `git fsck` line is valid only as a last-resort match against that
recorded SHA.

`/tmp/pi-subagent-*` directories are launch receipts only. They hold the child's
system prompt rather than its findings; listing them can confirm that a dispatch
happened but cannot recover a result.

Re-dispatch only the tracks with no usable artifact, handoff patch, recorded Git
object, or preserved worktree/ref.


## Waiting

Async fan-out should return control to the user and let the session wake on completion. Use `subagent_wait({ all: true })` only when the current turn genuinely must have the results before it ends — a run-to-completion request, or a headless run. Do not block a turn on a large fan-out merely to make it look synchronous; blocking is what rule 2 exists to prevent. On the first turn a completed worktree result is in front of the parent, apply its handoff patch or cherry-pick its recorded commit before any other dispatch; completion wake is not a reason to wait on the launch turn.
