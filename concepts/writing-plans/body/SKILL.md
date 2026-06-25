---
name: writing-plans
description: Use when an approved spec or resolved requirements need to become a detailed implementation plan before code is changed.
---

# Writing Plans

Write plans for a capable engineer or fresh agent with little project context. The plan must be concrete enough to execute task-by-task without guessing.

## Scope gate

Before planning, check whether the spec contains multiple independent subsystems. If so, split into separate plans or ask the user which subsystem to plan first. One plan should produce one working, testable slice.

## Plan location

Use the project’s stated plan location. If none exists, suggest `docs/plans/YYYY-MM-DD-<feature>.md` (or preserve an existing local convention).

## Required header

```markdown
# <Feature> Implementation Plan

**Goal:** <one sentence>
**Architecture:** <2–3 sentences about the approach and boundaries>
**Tech stack:** <relevant project tools/libraries>
**Execution note:** Work task-by-task. Use TDD where behavior changes. Verify and commit each task independently.

---
```

## Before tasks: file map

Map planned files before decomposing tasks:

- Create: exact paths and responsibilities.
- Modify: exact paths, relevant functions/sections if known.
- Tests: exact test files/commands.
- Docs/config/migrations if applicable.

Prefer well-bounded files with clear interfaces. Follow existing project patterns; include targeted cleanup only when it directly serves this feature.

## Task shape

Each task should be small enough to implement, verify, and commit independently. Use checkbox steps.

For code changes, include:

- Failing test to write.
- Command to run and expected failure.
- Minimal implementation shape or exact code when known.
- Command to verify green.
- Commit command with explicit paths.

Never write placeholders: `TBD`, `TODO`, “add appropriate error handling”, “write tests for this”, “similar to above”, or references to functions/types not defined by earlier tasks.

## Self-review before handoff

Check:

1. Every spec requirement maps to a task.
2. No placeholder or vague instruction remains.
3. Function/type/path names are consistent across tasks.
4. The task order respects dependencies.
5. Each task has a meaningful verification command.

Fix issues inline before presenting the plan.

## Handoff

After saving the plan, offer execution modes rather than assuming one:

1. Fresh-agent/task execution, with review between tasks.
2. Inline execution in this session.
3. Stop after planning.

Do not start implementation until the user chooses or previously authorized execution.
