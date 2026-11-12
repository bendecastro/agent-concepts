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

Save this writeup as a dated `<YYYY-MM-DD>-prototype-<slug>/` folder in the project's research role; a costly-to-reverse verdict also gets a record in the decisions role, and a product-level requirement goes to the requirements role. Look each role up in the "Where things go" table in `.bc-agent/AGENTS.md`. Why: one table per project means a project that keeps something elsewhere changes one place, and a writeup in the research folder is where the work item that follows will cite it. Without that table, use the earlier homes: `.bc-agent/project/<feature>-notes.md`, an ADR under `docs/adr/`, or the PRD. The research role is the default home and the one to recommend. If the user explicitly names another place for the writeup, save it there, say in your report that the research role is where later work will look for it, and offer to move it. Why: the writeup is the only part of a prototype that survives and a scratch folder is where files get deleted, but where the user's own file goes is the user's call.

Do not send prototype files to `/bc-drain-issues` as production acceptance criteria; the writeup is the evidence, and the prototype code is throwaway.
