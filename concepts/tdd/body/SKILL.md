---
name: tdd
description: Test-driven development with a red-green-refactor loop. Use when the user wants to build a feature or fix a bug test-first, mentions "red-green-refactor", or wants integration tests.
---

# Test-Driven Development

## Philosophy

**Core principle:** tests verify behavior through *public interfaces*, not implementation details. The code inside can change entirely; the tests shouldn't.

**Good tests** are integration-style: they exercise real code paths through public APIs and describe *what* the system does, not *how*. "User can checkout with valid cart" tells you a capability exists. These survive refactors. See [tests.md](tests.md).

**Bad tests** are coupled to implementation: they mock internal collaborators, test private methods, or verify through external means (querying the DB directly instead of using the interface). The warning sign: a test breaks when you refactor but behavior hasn't changed. See [mocking.md](mocking.md) for where mocking is and isn't appropriate.

## Anti-pattern: horizontal slices

**DO NOT write all tests first, then all implementation.** Treating RED as "write all tests" and GREEN as "write all code" produces crap tests: written in bulk they test *imagined* behavior, drift toward asserting the *shape* of things rather than user-facing behavior, and go insensitive to real changes. You outrun your headlights.

```
WRONG (horizontal):   RED: test1..test5   then   GREEN: impl1..impl5
RIGHT (vertical):     RED→GREEN: test1→impl1, test2→impl2, ...
```

Each test responds to what you learned from the previous cycle.

**Principled exit (time-pressed).** The incremental cadence is the default, not a cage. If the user explicitly says they're short on time and want all your recommendations implemented at once, honor it — write the planned tests as a batch and implement together. The exit trades only *cadence*, never *test quality*: the invariants still hold — behavior through public interfaces, mock only at boundaries, no implementation-coupled assertions (call counts, private state) — and you name once what batching gives up: the per-cycle feedback that keeps tests from asserting *imagined* behavior. What's not allowed is silently dropping the discipline because pushing back feels slow, or treating "it's faster" as the exit — the exit is an explicit time-pressed instruction, and it never licenses bad tests.

## Workflow

### 1. Planning
When exploring, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the domain language, and respect ADRs in the area you're touching. Before writing any code:
- [ ] Confirm with the user what interface changes are needed.
- [ ] Confirm which behaviors to test, prioritized — **you can't test everything**; focus on critical paths and complex logic, not every edge case.
- [ ] Identify deep-module opportunities (small interface, deep implementation) — run `/codebase-design` for the vocabulary and testability checks.
- [ ] List the behaviors to test (not implementation steps).
- [ ] Get user approval on the plan.

Ask: "What should the public interface look like? Which behaviors matter most to test?"

### 2. Tracer bullet
Write ONE test that confirms ONE thing. **RED:** test fails. **GREEN:** minimal code to pass. This proves the path works end-to-end.

### 3. Incremental loop
For each remaining behavior: **RED** (next test fails) → **GREEN** (minimal code to pass). One test at a time; only enough code to pass the current test; don't anticipate future tests; keep tests on observable behavior.

### 4. Refactor
After all tests pass, look for [refactor candidates](refactoring.md). **Never refactor while RED** — get to GREEN first, then refactor with the tests as your safety net.

## Checklist per cycle
```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive an internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```
