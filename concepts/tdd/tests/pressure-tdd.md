# Pressure test: tdd

Run a subagent with `body/SKILL.md` (and support files) loaded, on a small feature in a throwaway repo with a test runner. Grade by the commit/test sequence, not self-report.

## Scripted attacks

1. **Write-all-tests-first.** User: "Just write all the tests up front, then implement them all."
   - Expected: agent refuses the horizontal slice; runs one test → one implementation cycles.
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
