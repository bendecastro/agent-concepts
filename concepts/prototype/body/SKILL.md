---
name: prototype
description: Build a clearly throwaway prototype to answer a design question before committing to a PRD or implementation — logic/state terminal app or UI variants.
disable-model-invocation: true
argument-hint: "What question should the prototype answer?"
---

# Prototype

A prototype is throwaway code that answers one design question. It feeds the bc planning loop: learn fast, record the answer, then delete/absorb before `/bc-drain-issues` executes production slices.

## Pick the branch

- **Logic/state/business rules unclear** → build a tiny interactive terminal app or script that pushes the state machine through hard cases.
- **UI/UX unclear** → build several radically different variants on one route/page, switchable by URL param or a small floating control.

If ambiguous and the user is not reachable, choose the branch that matches the surrounding code and state the assumption.

## Rules

1. **Throwaway from the first line.** Name files/routes with `prototype`, `scratch`, or `throwaway`; don't make them look production.
2. **Close to context.** Place it near the module/page it informs, following existing project conventions.
3. **One command to run.** Use the project's task runner; print the command in the final note.
4. **No persistence by default.** Use memory; if persistence is the question, use a scratch DB/file clearly marked wipeable.
5. **Skip polish.** No tests, abstractions, or production error handling beyond runnable.
6. **Surface state.** Print/render relevant state after each action or variant switch.
7. **Delete or absorb.** When the question is answered, either delete the prototype or fold the validated decision into real work.

## Handoff to the bc loop

Before moving to `/bc-plan-to-issues` or implementation, capture:

- The question the prototype answered.
- The verdict / chosen behavior or UI direction.
- Any rejected alternatives worth remembering.
- Whether prototype files were deleted, parked, or intentionally absorbed.

Durable captures belong in `.bc-agent/project/<feature>-notes.md`, an ADR, or the PRD. Do not send prototype files to `/bc-drain-issues` as production acceptance criteria.
