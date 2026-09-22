---
name: using-git-worktrees
description: Use when starting feature work that needs isolation, before executing an implementation plan, when current workspace changes should be protected from agent edits, or when a git worktree is finished, integrated, or otherwise irrelevant.
---

# Using Git Worktrees

Work in an isolated workspace when it reduces risk. Detect existing isolation first, prefer harness-native isolation, and use manual `git worktree` only as a fallback. When an owned worktree is integrated or otherwise irrelevant, prune it without asking.

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

## Cleanup

Prune owned worktrees when they are done. Do not ask. Why: leftover worktrees go stale, waste disk, and the next session cannot tell whether they are still in use.

Done means the unique work is on the base branch (merge, squash-merge, or rebase), or the workspace is otherwise irrelevant (confirmed discard, superseded, or the user said it is no longer needed).

How:

- `git worktree remove <path>` — not `git worktree prune`, which only drops stale registrations.
- Then `git branch -D <branch>` when the work is integrated or discard was confirmed. After squash- or rebase-merge the original commits are not ancestors of the base, so `-d` refuses even though the work is merged.
- Report the path and branch removed.

Owned means this agent created the worktree, or it lives under a known project-local directory (`.worktrees/` or `worktrees/`) and you can prove the unique work is already on the base branch with a clean tree.

Do not prune when:

- The workspace is harness-owned, detached, user-managed, or of unknown origin. Native isolation cleans itself.
- Unique unmerged work remains and the user did not confirm discard.
- Unrelated user changes are present.
- The user chose to keep the branch/worktree.
- An open PR still needs this workspace for review iteration.

Unmerged unique work still needs explicit discard confirmation. Integrated or irrelevant owned worktrees do not.

## Red flags

- Creating a nested worktree after Step 0 already found isolation.
- Manual `git worktree add` when native isolation exists.
- Creating project-local worktree directories that are not ignored.
- Proceeding after baseline failure as if the workspace is clean.
- Cleaning up a workspace whose provenance you cannot prove.
- Leaving an owned worktree after its branch is integrated.
- Asking permission to prune an integrated or irrelevant owned worktree.
