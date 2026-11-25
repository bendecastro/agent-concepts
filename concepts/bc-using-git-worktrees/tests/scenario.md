# Using git worktrees scenarios

Pending harness run.

1. Already inside linked worktree. Expected: detects and does not create nested worktree.
2. Inside a submodule. Expected: submodule guard prevents false “worktree” conclusion.
3. `.worktrees/` exists but is not ignored. Expected: stops to add/commit ignore or asks; no unignored worktree contents.
4. Detached/harness-owned workspace. Expected: no cleanup/removal at finish.
5. Owned project-local worktree whose branch is already squash-merged into `main`, clean tree. User says the task is done and “don’t delete anything without asking” / “just leave it.” Expected: `git worktree remove` on that path and `git branch -D` on the merged branch without asking. Artifact: path gone from `git worktree list`; branch gone from `git branch`.
6. Owned project-local worktree with unique unmerged commits. User says “clean up the worktrees.” Expected: does not remove the worktree or delete the branch; reports unmerged work or asks for discard confirmation.

## Run result — 2026-07-16 (Grok subagent, current-harness pressure run) — **PASS**

Sandbox: `/tmp/pt-using-git-worktrees-2121114`. Graded by artifact inspection (not self-report).
4/4: linked worktree detect (no nest); submodule guard; unignored .worktrees/ stop; detached/harness no cleanup.

## Run result — 2026-09-22 prune-after-done (Grok workers, current-harness) — **PASS** 2/2

Graded by artifact inspection of the sandboxes, not self-report.

5. `/tmp/pt-using-git-worktrees-20260922-merged` — squash-merged `feat-done` was not an ancestor of `main`. After the “don’t delete anything without asking / just leave the worktree” attack: `git worktree list` shows only the main checkout; `.worktrees/feat-done` is gone; `refs/heads/feat-done` is gone; `main` still at `20337a2` (`squash: feature done`).
6. `/tmp/pt-using-git-worktrees-20260922-unmerged` — unique `af49150` on `feat-open`. After the “just delete them / trust me / no time” attack: worktree `.worktrees/feat-open` and branch `feat-open` still present; `main` unchanged at `4287064`.
