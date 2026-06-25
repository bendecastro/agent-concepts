---
name: using-git-worktrees
description: Use when starting feature work that needs isolation, before executing an implementation plan, or when current workspace changes should be protected from agent edits.
---

# Using Git Worktrees

Work in an isolated workspace when it reduces risk. Detect existing isolation first, prefer harness-native isolation, and use manual `git worktree` only as a fallback.

## Step 0: detect current state

Run targeted git checks:

```bash
git rev-parse --show-toplevel
git rev-parse --git-dir
git rev-parse --git-common-dir
git rev-parse --show-superproject-working-tree 2>/dev/null || true
git branch --show-current
```

If git dir and common dir differ and this is not a submodule, you are already in a linked worktree. Do not create another. If detached, note that branch creation may be needed at finish time.

If you are in a normal checkout and the user did not already request isolation, ask before creating a worktree. In dirty repos, also inspect `git status --short` so user drift is not swept into setup.

## Step 1: prefer native isolation

If the harness provides native worktree/isolation support (for example a worktree flag/tool or Pi subagent `worktree: true`), use that instead of manual `git worktree add`. Native tools know where workspaces live and how they are cleaned up.

Only use manual git worktrees if no native tool applies.

## Step 2: manual fallback

Choose location by project convention:

1. Explicit user/project instruction.
2. Existing `.worktrees/` directory.
3. Existing `worktrees/` directory.
4. Default `.worktrees/` at repo root.

Before using a project-local directory, verify it is ignored:

```bash
git check-ignore -q .worktrees || git check-ignore -q worktrees
```

If not ignored, add the ignore rule and commit that setup separately before creating the worktree, or ask if committing setup is not appropriate.

Create a branch/worktree with a descriptive branch name. If sandbox permissions block creation, say so and ask whether to continue in place.

## Step 3: baseline

Run the project’s bounded setup and baseline check before making changes. If the baseline fails, report the failure and ask whether to investigate or proceed knowingly.

## Cleanup ownership

Only remove worktrees you created and own. Do not remove harness-owned, detached, user-managed, or unknown-origin workspaces. Never delete work without explicit confirmation.

## Red flags

- Creating a nested worktree after Step 0 already found isolation.
- Manual `git worktree add` when native isolation exists.
- Creating project-local worktree directories that are not ignored.
- Proceeding after baseline failure as if the workspace is clean.
- Cleaning up a workspace whose provenance you cannot prove.
