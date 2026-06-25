---
name: brainstorming
description: Use when a feature, behavior change, UI, architecture, or product idea is not yet designed and needs collaborative exploration before implementation planning.
---

# Brainstorming

Turn a rough idea into an approved design. Do not implement while core purpose, scope, constraints, or success criteria are still being discovered.

## When to use

Use for new product ideas, features with unresolved behavior, UI/architecture choices, or broad changes where implementation could go in multiple valid directions.

Do not use to block clearly specified small edits, bug fixes with a tight repro, or tasks where the user explicitly gave the design and asked for implementation.

## Process

1. Explore current project context: docs, relevant files, recent decisions.
2. If the request contains multiple independent subsystems, stop and decompose before detailed questioning.
3. Ask clarifying questions one at a time. Prefer multiple choice when useful.
4. Propose 2–3 approaches with tradeoffs and a recommendation.
5. Present the design in appropriately sized sections: architecture, components, data flow/state, edge cases/errors, testing.
6. Get user approval or revisions.
7. Save the approved design/spec if the project expects durable planning docs.
8. Self-review the spec/design for placeholders, contradictions, ambiguity, and over-broad scope.
9. Hand off to implementation planning (`writing-plans`, `prd-drafting`, `issue-slicing`, or project-specific pipeline). Do not start coding unless the user approved both design and execution.

## Design quality checks

- Every component has one clear responsibility and interface.
- The design follows existing project patterns unless deliberately changing them.
- Refactoring is targeted to the current goal, not drive-by cleanup.
- YAGNI: remove speculative features and “professional” extras not needed for success.
- Tests/verification are considered before planning implementation.

## Red flags

- “This is simple, I can just build it.” Simple unchecked assumptions still waste time.
- Asking five questions at once. Use one-at-a-time to keep decisions crisp.
- Presenting only one approach when the design space is still open.
- Writing code, scaffolding, or editing files before design approval.
- Producing a spec with `TBD`, contradictory sections, or ambiguous requirements.
