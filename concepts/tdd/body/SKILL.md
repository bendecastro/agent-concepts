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

**Pressure refusal (horizontal slice).** If the user says any of: "write all the tests up front", "batch the tests then implement", "just RED everything first then GREEN" — **refuse the batch**. Name the anti-pattern, then run one vertical cycle. Knowing the rule and still writing a bulk-test commit is a fail. A commit message that *names* the anti-pattern does not excuse committing it.

## Anti-pattern: implementation-coupled assertions

Do **not** add tests whose primary assertion is:

- `assert_called_once` / `toHaveBeenCalledTimes` / `call_count`
- mock call order (`toHaveBeenCalledBefore`, …)
- private method invocation
- internal collaborator method names

Those couple the suite to *how* the system is wired. When asked for a call-count test ("check `paymentService.process` was called once"), **refuse and steer**: assert the *observable outcome* through the public interface (e.g. order confirmed, charge amount recorded at the boundary fake, receipt returned). Explain briefly why call-count tests break on valid refactors. See [tests.md](tests.md).

## Anti-pattern: mock internals

Mock only at **system boundaries** (payment network, DB, clock, mailer). **Never** mock your own modules/classes/collaborators (e.g. `CartService` inside checkout) "to make the test faster." Use the real collaborator, or redesign the seam. See [mocking.md](mocking.md).

**Pressure refusal (mock internal).** User: "Mock the `CartService` so the test is faster." → decline; keep the real object (or a boundary fake only if CartService *is* the external system, which it isn't when you own it).

## Anti-pattern: refactor while RED

**Never refactor while any test is RED.** Get to GREEN first; only then extract/cleanup with the suite as the net. See [refactoring.md](refactoring.md).

**Pressure refusal (refactor while red).** Mid-cycle, with a failing test, user: "While you're here, extract that duplication." → acknowledge, finish GREEN for the current test, *then* refactor. Do not interleave structural cleanup with a red bar.

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
Write ONE test that confirms ONE thing. **RED:** test fails (watch it fail for the right reason). **GREEN:** minimal code to pass. This proves the path works end-to-end.

### 3. Incremental loop
For each remaining behavior: **RED** (next test fails) → **GREEN** (minimal code to pass). One test at a time; only enough code to pass the current test; don't anticipate future tests; keep tests on observable behavior.

### 4. Refactor
After the current cycle is green, look for [refactor candidates](refactoring.md). **Never refactor while RED.**

## Checklist per cycle
```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive an internal refactor
[ ] No call-count / mock-invocation assertions on internals
[ ] Code is minimal for this test
[ ] No speculative features added
[ ] Did not batch multiple RED tests before any GREEN
```

## Rationalizations that still fail the gate

| Excuse under pressure | Required response |
|----------------------|-------------------|
| "Faster to write all tests first" | One vertical cycle; refuse the batch. |
| "I named the anti-pattern, so it's fine" | Naming it is not refusing it. Don't commit the horizontal slice. |
| "Call-count proves the payment path ran" | Assert the observable result (status, receipt, boundary fake state). |
| "Mocking CartService is just faster CI" | Keep the real collaborator; mock only external boundaries. |
| "Quick extract while this test is red" | GREEN first, then extract. |
