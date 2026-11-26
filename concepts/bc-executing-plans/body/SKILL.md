---
name: bc-executing-plans
description: Use when the user provides or selects a written implementation plan and wants the current session to execute it task-by-task.
---

# Executing Plans

Execute written plans deliberately: review the plan, verify preconditions, complete each task, and stop instead of guessing when the plan is wrong.

In preflight and verification: run pytest through the guarded test runner the project's or machine's instructions name (never with a custom `--basetemp`); make scratch folders with `mktemp -d`, never under `/tmp`; before a full suite, worktree isolation or fan-out, run the machine's storage health check if one exists and stop on critical or unknown health. Run targeted checks per task and one shared landing run of the full suite. The `agent-kernel` concept's Storage safety (temp files, scratch folders) and Verification sections hold their rules, when loaded. Why: task-by-task execution must not duplicate full suites.

## Preflight

1. Read the plan fully.
2. Inspect current git branch/status.
3. If on `main`/`master` and the work is more than a trivial edit, ask before implementing in place or use an approved isolated workspace.
4. Review the plan critically. Raise blockers, contradictions, missing files, or unsafe steps before coding.
5. Create a task list from the plan’s tasks.

## Execution loop

For each task:

1. Mark the task in progress.
2. Follow the plan steps in order.
3. If behavior changes, keep the red-green-refactor order unless the plan explicitly justifies another verified path.
4. Run the specified verification and read the output.
5. Commit only the files authored for that task when the repo’s instructions require commits.
6. Mark complete only after evidence supports it.

## Stop and ask when

- A plan instruction is unclear enough that two implementations would be plausible.
- A required dependency, file, credential, fixture, or service is unavailable.
- Verification fails repeatedly after a bounded diagnosis loop.
- The plan requires a broad architectural decision not already resolved.
- You discover the plan would overwrite, delete, publish, or mix unrelated user changes.

Do not force through blockers. A targeted question is better than confident wrong work.

## Completion

After all tasks are complete and verified, use the project’s completion workflow. If `bc-finishing-development-branch` is available and the user wants branch integration/PR options, use it. Otherwise report changed files, commits, verification, and remaining risks.

## Red flags

- Skipping critical review because the plan “looks detailed.”
- Treating a failed verification as a minor detail.
- Continuing to the next task with an uncommitted broken state.
- Asking “should I continue?” after every successful task when the user already asked you to execute the plan.
