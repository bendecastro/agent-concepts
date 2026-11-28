---
name: bc-safe-runs
description: Storage-safe test runs, scratch folders and worktree removal. Use before running tests, making scratch folders, running a full suite, creating a worktree, launching workers or reviewers, or removing a worktree or branch; its packet line goes into every worker or reviewer task.
---

# Safe runs

Rules for running code without filling the disk or losing work. They derive from the `agent-kernel` concept's Storage safety and Verification sections, which state the same rules when the kernel is loaded. If `~/.config/agent-concepts/overlays/bc-safe-runs.md` exists, read it: it names this machine's guarded test runner and storage health check. The project's own instructions take precedence over it.

## Test runs

- Run pytest through the guarded test runner the project's or machine's instructions name, with the selected interpreter for uv/venv projects. If none is configured, run plain `pytest` in the project's environment. Never supply a custom `--basetemp`, including through `PYTEST_ADDOPTS` or project addopts. Why: the guarded runner owns temporary storage and its retention; a custom `--basetemp` bypasses it.
- Tests and test helpers you write or change delete every temporary file and folder they create (temp dirs, browser profiles, fixtures in the OS temp dir), including on failure; use pytest's `tmp_path` for test fixtures. After the run, compare the project's temp-dir footprint before and after (count or size of its prefix) and fix any leak. Why: in one project tests left about 14,000 folders (2.5 GB) in a 7.7 GB RAM-backed `/tmp`, filling it and crashing two agent runs mid-task.
- Run targeted tests while working. Workers and reviewers never run the full suite or full gate, even when a project page says to: the session that integrates runs it once per integrated tree (and once per base where a workflow needs a baseline) and records the command, result and exact tree identity; everyone else reuses that record, and reviewers repro findings with targeted tests. Why: each full run costs minutes, and parallel agents multiply the cost without adding evidence.

## Scratch folders

Make scratch folders (prototypes, throwaway projects, build output, logs; not durable run folders) with `mktemp -d` and no path argument, which uses `$TMPDIR`, or in a git-ignored folder inside your worktree. Never type `/tmp/` into a command, a `CARGO_TARGET_DIR` or a worker's task unless the user named that exact path. Delete the scratch folder before you finish. Why: `/tmp` may be a small RAM-backed disk that also holds agent runner state; one Rust build there took 5.7 GB of 7.7 GB and three agent runs died without a log line.

## Storage health check

Before a full suite, creating a worktree, a parallel review or launching two or more workers, run the storage health check the machine's instructions name. Stop and report on critical or unknown health, or if the configured check cannot run. If no check is configured, skip it and say so in one line of the report. On Btrfs judge free space with that check (or `btrfs filesystem usage`), not `df`. Why: free bytes can hide metadata exhaustion, and parallel work multiplies disk use.

## Packet line

Children do not load this skill on their own. Copy this line into every worker or reviewer task:

> Run pytest through the guarded test runner the project's or machine's instructions name (otherwise plain `pytest`), with the selected interpreter for uv/venv projects; use `tmp_path` for fixtures and clean up even on failure; never a custom `--basetemp`; make scratch folders with `mktemp -d`, never under `/tmp`, and delete them before finishing; run targeted tests only, never the full suite or gate.

## Removing a worktree or branch

Before removing a worktree or deleting its branch, prove its commits are in `HEAD`: its tip is an ancestor of `HEAD` (`git merge-base --is-ancestor <tip> HEAD`), or every commit is patch-equivalent in `HEAD`: `git cherry HEAD <tip>` succeeds and prints only `-` lines (empty output alone is not proof without ancestry). Record the tip, the landed `HEAD` and the proof (in the run manifest when there is one) before cleanup. Keep anything dirty, unmerged or unclear. Remove with `git worktree remove`, never `--force`. The full recipe, including resolved conflict picks and branch deletion, is in the `bc-using-git-worktrees` skill, section Cleanup. Why: deletion without proof loses work, and integration without cleanup leaks disk.
