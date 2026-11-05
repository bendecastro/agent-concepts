---
name: tdd
description: Use when writing new tests or behaviour-changing assertions, including a bug fix that adds a regression test or tests added as a side part of a feature; also for test-first, red-green-refactor, or new integration-test requests. Excludes reading, running or mechanically updating tests.
---

# Test-Driven Development

Use targeted RED/GREEN checks through guarded pytest under [kernel Storage safety](../../agent-kernel/body/AGENT-KERNEL.md#storage-safety); health-check before a full suite, not each cycle. Why: fast feedback does not require repeated full suites.

These rules apply to new tests and behaviour-changing assertions, including regression tests added during bug fixes or feature work. Reading, running or mechanical test edits (such as import renames) do not require a watched fail or a new plan. For bugs without a tight repro, `diagnosing-bugs` owns diagnosis; this concept owns the regression-test RED/GREEN cycle once the behaviour is identified.

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

## Tests that lie

A green test is useful only if a plausible behavioral regression can turn it red. Reject these substitutes for behavioral coverage:

- **Tautological:** `assert MAX_RETRIES == 3`, or `assert normalize(x) == normalize(x)` — the expected value repeats implementation rather than supplying an independent oracle.
- **Structure-sensitive:** `assert "send_receipt(" in source`, source/docs/config text scans, private names, line numbers or string positions instead of executing behavior. Privacy scans and other repository invariants are legitimate **lints**, not behavioral coverage; label them accordingly. Text assertions on a public text-transformer's output can test real behavior.
- **Cannot-fail:** an error-path test whose HTTP fake always succeeds; an autouse fixture that replaces the subsystem it claims to test; `assert result is not None` when a specific outcome matters, or no assertion/check at all. A fixture that rejects live network access is useful hygiene, not permission to erase the behavior under test.
- **Implementation-coupled:** monkeypatching the module's own private helpers (`service._retry = fake`) or asserting internal call counts. See the refusal rules below; a green wiring test does not cover the replaced collaborator.

**Self-check for every new test or behaviour-changing assertion:** name the plausible regression that turns it red, and confirm the existing RED run actually failed for that reason.

**Positive shape:** fake at the system boundary, drive the public entry point, use an independent oracle. For example, let a fake HTTP transport raise a timeout, call public `submit_order(...)` with real retry logic, and assert the specified failure result and no recorded charge—not an expected result computed by `submit_order` itself.

If asked to pin a constant, grep source, or stub away the claimed failure, decline that substitute and test the observable contract instead. Why: those tests can stay green while the behavior breaks.

## Anti-pattern: implementation-coupled assertions

Do **not** add tests whose primary assertion is:

- `assert_called_once` / `toHaveBeenCalledTimes` / `call_count`
- mock call order (`toHaveBeenCalledBefore`, …)
- private method invocation
- internal collaborator method names

Those couple the suite to *how* the system is wired. When asked for a call-count test ("check `paymentService.process` was called once"), **refuse and steer**: assert the *observable outcome* through the public interface (e.g. order confirmed, charge amount recorded at the boundary fake, receipt returned). Explain briefly why call-count tests break on valid refactors. See [tests.md](tests.md).

## Anti-pattern: mock internals

Mock only at **system boundaries** (payment network, DB, clock, mailer). **Never** mock your own modules/classes/collaborators (e.g. `CartService` inside checkout) "to make the test faster." Use the real collaborator, or redesign the seam. See [mocking.md](mocking.md).

In Python, refuse `monkeypatch.setattr(orders, '_charge', fake)` when `orders` is the module under test. Inject the external boundary instead, keeping the real `_charge` logic:

```python
# Production: _charge uses the supplied payment-network boundary.
def submit_order(order, *, payment_client=real_payment_client):
    return _charge(order, payment_client=payment_client)

# Test: a boundary fake declines; real order/charge handling still runs.
result = orders.submit_order(order, payment_client=DecliningPaymentClient())
assert result.status == "declined"
```

**Patching a standard-library boundary is allowed:** `monkeypatch.setattr(subprocess, 'run', fake)` or `patch('tags.subprocess.run')` replaces the external call, not your code, even when reached through the module under test. What is forbidden is replacing the module's own functions, helpers or classes (`tags._parse`, `sync._revision`).

**Seam rule:** prefer an injected boundary when tests would otherwise need several patches, or when the only way to fake the boundary is to patch the module's own names: add a keyword boundary parameter with the real default (behavior unchanged), e.g. `runner=subprocess.run`. If that design change is out of scope, report it rather than writing the coupled test.

**Pressure refusal (mock internal).** User: "Mock the `CartService` so the test is faster." → decline; keep the real object (or a boundary fake only if CartService *is* the external system, which it isn't when you own it).

## Anti-pattern: refactor while RED

**Never refactor while any test is RED.** Get to GREEN first; only then extract/cleanup with the suite as the net. See [refactoring.md](refactoring.md).

**Pressure refusal (refactor while red).** Mid-cycle, with a failing test, user: "While you're here, extract that duplication." → acknowledge, finish GREEN for the current test, *then* refactor. Do not interleave structural cleanup with a red bar.

## Workflow

### 1. Planning
When exploring, read `glossary.md` (if it exists) so test names and interface vocabulary match the domain language, and respect ADRs in the area you're touching. For work in scope, before writing code:
- [ ] Confirm with the user what interface changes are needed.
- [ ] Confirm which behaviors to test, prioritized — **you can't test everything**; focus on critical paths and complex logic, not every edge case.
- [ ] Identify deep-module opportunities (small interface, deep implementation) — run `/codebase-design` for the vocabulary and testability checks.
- [ ] List the behaviors to test (not implementation steps).
- [ ] Get user approval on the plan.

Ask: "What should the public interface look like? Which behaviors matter most to test?"

**Small bug fixes:** when the requested behaviour and unchanged interface are clear, state the regression to test and proceed without interactive plan approval; still watch RED before the fix and GREEN after it. Ask if behaviour or interface needs a decision.

**Unattended mode:** when no user can answer (delegated child or headless job), do not stop for confirmation/approval. Record the behavior list and interface decision in your output or commit message, then proceed; keep the other planning checks.

### 2. Tracer bullet
Write ONE test that confirms ONE thing. **RED:** test fails (watch it fail for the right reason). **GREEN:** minimal code to pass. This proves the path works end-to-end. [confirm-red.py](scripts/confirm-red.py) can run current changed tests against old code in a disposable tree: `python3 "$AGENT_CONCEPTS/concepts/tdd/body/scripts/confirm-red.py" --base HEAD -- <test command...>` (use guarded pytest where applicable; see `--help` for environment limits). Inspect the failure reason, not just its exit status.

If the test cannot be executed at all — no runner, missing fixture, unbuildable environment — you do not have a RED. Stop and report the blocker. Never proceed to GREEN against a test you have not watched fail. Why: GREEN without a watched fail is a green bar you invented.

**Tests written after the code:** coverage, regression and characterisation tests for existing code still need a watched fail. Revert the fix or make a minimal mutation that breaks the named covered behavior, watch the test go red for that reason, restore, then watch green. Record both runs. Use a disposable copy for mutations; do not disturb unrelated working-tree changes. A missing-symbol/collection failure alone does not prove behavior is covered.

### 3. Incremental loop
For each remaining behavior: **RED** (next test fails) → **GREEN** (minimal code to pass). One test at a time; only enough code to pass the current test; don't anticipate future tests; keep tests on observable behavior.

### 4. Refactor
After the current cycle is green, look for [refactor candidates](refactoring.md). **Never refactor while RED.**

## Checklist per cycle
```
[ ] Test describes behavior, not implementation; source/config scans are labelled lints
[ ] Plausible regression named; RED failed for that reason (confirm-red.py or behavioral mutation); both RED/GREEN runs recorded
[ ] Independent oracle; fixtures preserve the claimed failure mode
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
| "Just pin MAX_RETRIES / grep the call" | Exercise retry behavior through the public entry point; label legitimate repository scans as lints. |
| "Stub success so the error test passes" | Make the boundary fake produce the error; keep real error handling and assert its outcome. |
| "Faster to write all tests first" | One vertical cycle; refuse the batch. |
| "I named the anti-pattern, so it's fine" | Naming it is not refusing it. Don't commit the horizontal slice. |
| "Call-count proves the payment path ran" | Assert the observable result (status, receipt, boundary fake state). |
| "Mocking CartService is just faster CI" | Keep the real collaborator; mock only external boundaries. |
| "Quick extract while this test is red" | GREEN first, then extract. |
| "Can't run it; treating that as red enough" | Stop and report the blocker. A test you have not watched fail is not a RED. |

For glossary discovery in legacy projects, follow `domain-modeling`’s legacy glossary rule.
