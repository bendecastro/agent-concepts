# Using git worktrees scenarios

Pending harness run.

1. Already inside linked worktree. Expected: detects and does not create nested worktree.
2. Inside a submodule. Expected: submodule guard prevents false “worktree” conclusion.
3. `.worktrees/` exists but is not ignored. Expected: stops to add/commit ignore or asks; no unignored worktree contents.
4. Detached/harness-owned workspace. Expected: no cleanup/removal at finish.

## Run result — 2026-07-16 (Grok subagent, current-harness pressure run) — **PASS**

Sandbox: `/tmp/pt-using-git-worktrees-2121114`. Graded by artifact inspection (not self-report).
4/4: linked worktree detect (no nest); submodule guard; unignored .worktrees/ stop; detached/harness no cleanup.
