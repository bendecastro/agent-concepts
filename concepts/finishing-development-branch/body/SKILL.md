---
name: finishing-development-branch
description: Use when implementation is complete and the user needs options for merging, creating a PR, keeping a branch, or discarding branch work.
---

# Finishing Development Branch

Finish work by verifying first, then presenting clear options. Do not publish, merge, or discard by implication.

## 1. Verify before offering completion

Run the relevant project checks fresh and read the output. If checks fail, stop and report failures; do not offer merge/PR options until the user chooses to proceed despite them.

Also inspect:

```bash
git status --short
git branch --show-current
git rev-parse --git-dir
git rev-parse --git-common-dir
git log --oneline --decorate -5
```

Separate agent-authored changes from unrelated user drift before any commit/merge/push.

## 2. Detect workspace and branch state

- Normal repo on a named branch: standard options.
- Linked worktree on a named branch: standard options, but cleanup only if this agent created/owns it.
- Detached or harness-owned workspace: no local merge option unless a branch is created intentionally.

Determine likely base branch (`main`, `master`, or project instruction), but ask if uncertain.

## 3. Present options

Named branch:

1. Merge back to `<base>` locally.
2. Push/create PR, only if user explicitly chooses and publish policy allows or user authorizes.
3. Keep branch/worktree as-is.
4. Discard this work.

Detached/harness-owned workspace:

1. Create/push a branch and PR, only with explicit authorization.
2. Keep as-is.
3. Discard this work.

Do not add a hidden default. Ask the user to pick.

## 4. Execute safely

- Merge locally: update base, merge, run verification on merged result before cleanup.
- PR/push: check publish policy or ask; preserve worktree for review iteration.
- Keep: report branch/path and stop.
- Discard: require typed confirmation after listing branch, commits, and path. Never discard unrelated user changes.

## Cleanup rules

Only remove a worktree if all are true:

- It was created for this task or is under a known project-local worktree directory.
- The chosen option is merge-local or confirmed discard.
- Merge/discard completed successfully.
- No unrelated user changes are present.

Never force-push. Never delete unmerged work without explicit confirmation.
