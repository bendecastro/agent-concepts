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
      { key: "notes", agent: "scout", output: OUT + "notes.md", task: "..." },
      { key: "docs",  agent: "scout", output: OUT + "docs.md",  task: "..." },
    ]);
  `
})
```

`output` is per child and must be distinct. The path is injected into the child as an authoritative override, so the child does not need to be told the path twice in its task text — but it does need to be told to *append as it goes*.

Pick roles by authority, not convenience: `scout` for bounded recon, `researcher` for external facts, `reviewer` for independent critique, `oracle` for hard judgment. Fan-out of `scout` children is the common shape.

For ordinary dispatch, omit both `model` and child `thinking` when the selected role's configured route is correct. Child `thinking` is not a routing control: current child execution ignores it. If an explicit override is needed, preserve the full effective model value, including its thinking suffix, for example:

```js
{ key: "notes", agent: "scout", model: "openai-codex/gpt-5.6-luna:max", output: OUT + "notes.md", task: "..." }
```

Never copy or pass the bare `openai-codex/gpt-5.6-luna` registry id when the configured route is `:max`: the 2026-08-25 matrix showed that shape running at scout frontmatter low. Every probe in that matrix used `scout`; worker and reviewer fallback behavior was not tested. The nickname `model: "luna"` is not a registry id and fails closed (`Unknown subagent model 'luna'`). Chat and the manifest keep the routing name (`Luna max`) as effective-route metadata; they do not require those fields in the child object.

A child `thinking` field or a bare model belongs only in a deliberate reproduction probe for this behavior, not in an ordinary swarm launch.

Children do not inherit the swarm kernel, so the swarm-mode parent must copy the own-line `Commit:`/`Branch:` requirement into every worktree worker task. Keep the scoped worker bullet from `SKILL.md` in that packet; recon tasks do not need it.

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

Use the recorded paths and identity; do not guess from temporary-directory names. A prompt naming an interrupted, failed, empty, missing, or reaped run is recovery even when it says redo or relaunch. Before naming a replacement track, execute this order. Never stash, delete, move, or overwrite prior-run evidence merely to make a replacement launchable.

```sh
# 1. What was dispatched.
cat "$RUN_DIR/manifest.md"

# 2. Which declared artifacts exist and contain records.
find "$RUN_DIR" -maxdepth 3 -type f -print | sort
# Read each artifact path from the manifest; inspect its own-line Commit:/Branch: records.

# 3. Ask Pi for retained output, artifactPaths, and the handoff path.
#    Run this as a subagent tool call, not as a filesystem guess:
#    subagent({ action: "children.list" })

# 4. Worktree tracks only: use the exact child entry from the handoff JSON.
#    Bind CHILD, EXPECTED_BRANCH, BASE, and PATCH from that entry and manifest;
#    do not infer any of them from a temporary-directory name.
#    Require all of these before treating the patch as recovery:
#      - this exact child; patch.branch and Branch: equal EXPECTED_BRANCH
#      - nonempty file (`test -s "$PATCH"`)
#      - patch.changed == true
#      - no patch.error or capture error
#      - handoff baseCommit == the expected BASE, which is a commit
#    An empty, error, mismatched, or wrong-base patch is not recovery.
#    Inspect it, then require the check before mutation:
git -C "$REPO" apply --check "$PATCH"
#    Only after that succeeds:
git -C "$REPO" apply "$PATCH"
#    Verify the resulting diff/tree before any commit or report.

# 5. If there is no usable patch, inspect only the LAST complete own-line
#    Commit:/Branch: pair. Earlier records are untrusted evidence, not
#    candidates. Bind TIP and RECORDED_BRANCH from that pair and
#    EXPECTED_BRANCH/BASE from the exact child handoff; a none/none pair is
#    only the no-commit case and cannot authorize integration.
printf '%s\n' "$TIP" | grep -Eq '^[0-9a-f]{40}$'
test "$RECORDED_BRANCH" = "$EXPECTED_BRANCH"
#    Full format is not enough: Git must resolve the candidate as a commit.
test "$(git -C "$REPO" cat-file -t "$TIP")" = commit
git -C "$REPO" rev-parse --verify "${TIP}^{commit}"
#    Successful cleanup may remove the expected local branch. If its ref
#    remains, it must resolve to exactly the candidate tip; absence is allowed:
if git -C "$REPO" show-ref --verify --quiet "refs/heads/$EXPECTED_BRANCH"; then
  test "$(git -C "$REPO" rev-parse --verify "refs/heads/$EXPECTED_BRANCH^{commit}")" = "$TIP"
fi
#    Validate the handoff's expected base and inspect the complete linear range,
#    not only TIP, before integration:
git -C "$REPO" rev-parse --verify "${BASE}^{commit}"
git -C "$REPO" rev-list --parents --reverse "$BASE..$TIP"
#    Require one ordered parent chain rooted at BASE; stop on non-linear or
#    ambiguous history. Inspect the candidate's resulting tree/diff:
git -C "$REPO" diff --stat "$BASE" "$TIP"
git -C "$REPO" diff "$BASE" "$TIP"
#    If this succeeds, TIP is already integrated:
git -C "$REPO" merge-base --is-ancestor "$TIP" HEAD
#    If HEAD == BASE, use only:
git -C "$REPO" merge --ff-only "$TIP"
#    Otherwise require parent HEAD to be an advance from the same BASE:
git -C "$REPO" merge-base --is-ancestor "$BASE" HEAD
#    Inspect the ordered BASE..TIP list and cherry-pick each commit in that
#    order. Stop on conflict; never guess or cherry-pick TIP alone. Verify the
#    resulting diff/tree.

# 6. Only when the handoff says cleanup was refused, inspect preserved state.
git -C "$REPO" worktree list
git -C "$REPO" branch --list "$EXPECTED_BRANCH"
# No patch plus no SHA does not license relaunch while this preserved state exists.

# 7. Last resort: only after TIP passed the full-SHA and commit checks above,
#    exact-match that SHA. Never browse or select dangling objects:
git -C "$REPO" fsck --no-reflogs --lost-found | awk -v sha="$TIP" '$NF == sha'

# 8. Only now re-dispatch a track that has no usable artifact, valid handoff
#    patch, recorded Git object, or preserved worktree/ref.
```

`$PATCH`, `$TIP`, `$BASE`, `$RECORDED_BRANCH`, and `$EXPECTED_BRANCH` above come
from the exact artifact and runtime handoff; they are not values inferred from a
guessed `/tmp` name. A worktree artifact without valid own-line
`Commit:`/`Branch:` records is not a usable deliverable (`none`/`none` is valid
when no commit was made). A retained run can supply artifact and handoff paths,
but cannot reopen a worktree whose cleanup already removed it. The `git fsck`
line is valid only as an exact match against the already validated recorded SHA,
never as a way to browse or choose among dangling commits.

`/tmp/pi-subagent-*` directories are launch receipts only. They hold the child's
system prompt rather than its findings; listing them can confirm that a dispatch
happened but cannot recover a result.

Re-dispatch only the tracks with no usable artifact, valid handoff patch, recorded
Git object, or preserved worktree/ref.


## Waiting

Async fan-out should return control to the user and let the session wake on completion. Use `subagent_wait({ all: true })` only when the current turn genuinely must have the results before it ends — a run-to-completion request, or a headless run. Do not block a turn on a large fan-out merely to make it look synchronous; blocking is what rule 2 exists to prevent. On the first turn a completed worktree result is in front of the parent, apply its validated handoff patch or integrate its validated full commit range before any other dispatch; completion wake is not a reason to wait on the launch turn.
