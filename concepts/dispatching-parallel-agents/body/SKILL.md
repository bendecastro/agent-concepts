---
name: dispatching-parallel-agents
description: Use when there are two or more independent investigations, reviews, failures, or implementation-adjacent tasks that can proceed without shared state or sequential dependencies.
---

# Dispatching Parallel Agents

Dispatch one fresh agent per independent problem domain. Parallelism is useful only when the domains do not depend on each other and agents will not edit or rely on the same mutable state.

## Use when

- Multiple test files or subsystems fail for apparently different reasons.
- Several independent reviews/research tasks are needed.
- Each task can be understood with a focused context packet.
- Agents can work without conflicting file edits or shared external state.

Do **not** use when failures are likely related, the whole system must be understood together, or the agents would touch overlapping files/resources.

## Pattern

1. Group work by independent domain.
2. Write one focused task per domain.
3. Provide self-contained context: files, errors, constraints, and expected output.
4. Run agents concurrently only if the harness supports safe isolation.
5. Read every result, inspect diffs if any, check conflicts, then run the combined verification yourself.

## Prompt packet

Each agent gets:

- Specific scope: one file, subsystem, issue, or question.
- Goal: what success means.
- Constraints: files not to touch, no broad refactors, no production changes if diagnostic-only.
- Evidence to inspect: error messages, paths, commands, relevant snippets.
- Output contract: root cause, changed files, tests run, residual risks.

Bad: “Fix all tests.”
Good: “Diagnose the three failures in `tests/abort.test.ts`; determine timing bug vs assertion drift; do not change unrelated tests; return root cause, patch summary, and verification command/output.”

## Homogeneous fan-out (many agents, one task shape)

When the split is N instances of the same task — port every file, fix every crate’s errors, update every call site — a packet defect multiplies by N. Two steps come before scaling:

1. **Serialize the shared decisions first.** Compile the pattern mappings, conventions, and edge-case policies into one compact guide that every worker receives, instead of letting each worker re-derive them divergently. Review the guide as rigorously as code — fresh reviewers, assume it has defects — because a mistake in it ships N times.
2. **Pilot, then scale.** Run 1–3 instances through the full loop (implement, review, integrate) and fix the packet and guide from what they reveal before dispatching the fleet. Prompt defects are cheapest to catch here; at fleet scale they become a cleanup workflow of their own.

## Parent responsibilities

Parallel agents do not make the combined result true. The parent must:

- Compare outputs for contradictions.
- Check whether two agents edited the same files or made incompatible assumptions.
- Re-run the relevant full verification after integration.
- Escalate if an agent reports uncertainty rather than papering it over.

## Red flags

- “These might share a cause, but parallelism is faster.” Investigate together first.
- “The agents said done.” Verify diffs and commands yourself.
- “One agent can handle the broad problem.” Then do not split.
- “They may edit the same files.” Use sequencing or worktrees instead. Shared mutable state fails within minutes at scale, not eventually — in Bun’s Rust-rewrite fleet, parallel agents ran `git stash`/`git reset` over each other’s work almost immediately. If full isolation is genuinely impractical (e.g. worktree disk cost), the fallback is restricting every worker to atomic, file-scoped, non-destructive commands — commit one file at a time; never `stash`, `reset`, or slow repo-wide scans — not hoping the agents coordinate.
