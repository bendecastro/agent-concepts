---
name: bc-subagent-driven-development
description: Use when executing a written implementation plan in the current session with fresh agents for individual tasks and review checkpoints.
---

# Subagent-Driven Development

A controller executes a plan by giving each task to a fresh implementer agent, then running spec-compliance and code-quality review before moving on.

Load `bc-safe-runs`. Else: guarded test runner (fallback `pytest`; no custom `--basetemp`), `mktemp -d` outside `/tmp`, targeted tests; configured storage check before full suites, worktrees, fan-out: stop if critical or unknown, or if the check cannot run.

Load `bc-durable-subagents` before the first launch. Else: before launching, write a run folder and `manifest.md` (key → artifact path → role → model + thinking → task), state its path in chat, and have each child append to its own artifact.

At completion, prove each worker's commits are in `HEAD` (ancestor or patch-equivalent) and record that proof before removing worktrees or branches. Put the `bc-safe-runs` packet line in every worker or reviewer task. Workers run targeted tests only and reuse the shared full-suite evidence. Why: fresh agents cannot infer shared storage ownership.

## Use when

- A written plan exists with reasonably independent tasks.
- The harness supports subagents or equivalent fresh-context workers.
- The controller should stay in this session and own integration.

Do not use for tightly coupled tasks that require constant shared context; execute inline or rewrite the plan.

## Controller preflight

1. Read the whole plan once.
2. Extract every task with its full text and dependency context.
3. Inspect git status/branch and establish isolation if needed.
4. Create a task list for controller tracking.

Never make the implementer read the whole plan to find its task. Paste the exact task and curated context into the packet.

## Per-task loop

1. Dispatch implementer with full task text, context, working directory, constraints, and status contract.
2. If implementer returns `NEEDS_CONTEXT`, provide missing context and re-dispatch.
3. If `BLOCKED`, change something: more context, better model, smaller task, or escalate to the user. Do not retry blindly.
4. If `DONE_WITH_CONCERNS`, read concerns before review.
5. Run spec-compliance review: did the change implement exactly the task, no less and no extra?
6. Fix/re-review until spec compliant.
7. Run code-quality review: bugs, tests, maintainability, architecture, edge cases.
8. Fix/re-review until quality issues are resolved or explicitly deferred.
9. Parent verifies and marks task complete.

Do not dispatch multiple implementers in parallel unless tasks are proven independent and isolated; use `bc-dispatching-parallel-agents` for that case.

## Implementer packet essentials

- Task name and full plan text for this task.
- Scene-setting: what came before and what this enables.
- Files/commands expected by the plan.
- Constraints: do not broaden scope, ask when unclear, commit if repo rules require.
- Report format: `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`; include files changed, tests run, evidence, concerns.

## Completion

After all tasks pass review, run a final whole-diff review or relevant verification, then use the project’s branch-completion workflow if merge/PR/cleanup is needed.

## Red flags

- Skipping spec review because code quality review “looks good.”
- Letting implementer self-review replace independent review.
- Proceeding with open Important/Critical review issues.
- Ignoring a blocked subagent or forcing the same failed prompt again.
- Trusting subagent success reports without checking diff and verification.
