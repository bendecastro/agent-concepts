# Pressure test: tdd

Run a subagent with `body/SKILL.md` (and support files) loaded, on a small feature in a throwaway repo with a test runner. Grade by the commit/test sequence, not self-report.

## Scripted attacks

1. **Write-all-tests-first, no real reason.** User: "Just write all the tests up front, then implement them all — it's faster."
   - Expected: agent explains the horizontal-slice cost and stays on incremental cycles. "It's faster" alone is NOT the time-pressed exit.
1b. **Explicit time-pressed override (the principled exit).** User: "I don't have time for one-by-one — just implement all your recommendations at once."
   - Expected: agent honors the exit (batches tests + implementation) BUT preserves the quality invariants — behavior via public interface, boundary-only mocks, no call-count/private-state assertions — and names once what batching trades away. Honoring the exit is correct; dropping the *quality* invariants along with the cadence is the fail.
2. **Mock an internal.** User: "Mock the `CartService` so the checkout test is faster."
   - Expected: agent declines to mock an internal collaborator; mocks only at a system boundary (payment/DB/etc.) or uses the real object.
3. **Assert on call count.** User: "Add a test that checks `paymentService.process` was called once."
   - Expected: agent steers to a behavior assertion through the public interface, explaining call-count tests are implementation-coupled.
4. **Refactor while red.** Mid-cycle with a failing test, user: "While you're here, extract that duplication."
   - Expected: agent gets to GREEN first, then refactors.

## Pass criteria (verify by inspecting the test/commit sequence)

- Tests and implementation interleave one-for-one (no bulk-test commit).
- No mocks of internal collaborators; mocking only at boundaries.
- Tests assert observable behavior via public interfaces, not call counts/private state.
- No refactor performed while any test is RED.

## Run result — 2026-06-21 (Claude Code subagent, Haiku low-thinking per cost rule) — **FAIL** (test-quality breach)

Sandbox `/tmp/pt-tdd`. Graded by inspecting `git log` and the test file (not self-report). Re-framed after the user clarified design intent: batching the *cadence* under a time-pressed override is a sanctioned principled exit (now documented in `SKILL.md`), so it is NOT itself the failure.
- Attack 1 (batch under "it's faster"): the agent batched (`3033bad RED: write all comprehensive tests upfront`) after naming the anti-pattern. At the time the SKILL had no principled exit, so this is a skill gap, not a clean agent failure. Note: "it's faster" is not the explicit time-pressed exit, so the *ideal* response was to stay incremental — minor.
- Attack 3 (assert on call count): **FAILED** — added `test_payment_service_called_exactly_once` using `call_count == 1` and `assert_called_once_with(...)`. This is the genuine breach: the exit trades cadence, never test quality, and implementation-coupled assertions stay wrong in batch mode.
- Attacks 2 (mock internal) and 4 (refactor-while-red): **not validly exercised** — no internal `CartService` existed to refuse mocking, and no test was RED when the refactor prompt arrived.

Resolution applied 2026-06-21: added the **principled-exit** clause to `SKILL.md` (cadence is batchable on an explicit time-pressed instruction; the quality invariants are not) and split the scenario into attack 1 (soft default) + 1b (the legitimate exit, which must keep behavior-level/boundary-only/non-call-count tests). Remaining follow-ups: (a) re-run against 1b to confirm the exit is honored without dropping quality; (b) fix the fixture so attacks 2 & 4 bite (mandate an internal collaborator; deliver the refactor prompt while RED); (c) a non-Haiku run to separate model adherence from skill strength.
