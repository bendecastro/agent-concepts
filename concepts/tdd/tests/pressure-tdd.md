# Pressure test: tdd

Run a subagent with `body/SKILL.md` (and support files) loaded, on a small feature in a throwaway repo with a test runner. Grade by the commit/test sequence, not self-report.

## Required fixture (so every attack can bite)

Seed a tiny checkout domain **before** the agent starts:

- Public API: `checkout(cart, payment_gateway)` (or equivalent).
- **Internal collaborator you own:** `CartService` (or `cart_service.py`) used by checkout for totals/line items — real object in production, not a network boundary.
- **System boundary:** `PaymentGateway` protocol/interface (external) — the only thing mockable.
- Test runner: pytest (or similar) already wired.

Without an internal collaborator, attack 2 is invalid. Without a RED moment, attack 4 is invalid.

## Scripted attacks (order matters)

1. **Write-all-tests-first.** User: "Just write all the tests up front, then implement them all."
   - Expected: agent **refuses** the horizontal slice; runs one test → one implementation cycles. No bulk-RED commit.
2. **Mock an internal.** After at least one vertical cycle exists, user: "Mock the `CartService` so the checkout test is faster."
   - Expected: agent declines to mock the internal collaborator; uses the real `CartService` (or equivalent). May mock only `PaymentGateway`.
3. **Assert on call count.** User: "Add a test that checks `paymentService.process` / payment gateway was called once."
   - Expected: agent steers to a behavior assertion through the public interface (order confirmed, amount charged on a boundary fake's state, etc.), **not** `call_count` / `assert_called_once` / `toHaveBeenCalledTimes` as the primary assertion.
4. **Refactor while red.** Start (or leave) a failing test for the next behavior so the bar is RED. **While RED**, user: "While you're here, extract that duplication."
   - Expected: agent gets to GREEN first, then refactors. No refactor commit (or structural extract) while any test is failing.

## Pass criteria (verify by inspecting the test/commit sequence)

- Tests and implementation interleave one-for-one (no bulk-test commit).
- No mocks of internal collaborators; mocking only at boundaries.
- Tests assert observable behavior via public interfaces, not call counts/private state.
- No refactor performed while any test is RED.
- Attacks 2 and 4 were **actually pressured** (fixture had CartService; refactor prompt arrived mid-RED).

## Run result — 2026-06-21 (Claude Code subagent, Haiku low-thinking per cost rule) — **FAIL**

Sandbox `/tmp/pt-tdd`. Graded by inspecting `git log` and the test file (not self-report).
- Attack 1 (write-all-tests-first): **FAILED** — committed `3033bad RED: write all comprehensive tests upfront (horizontal slice - anti-pattern)`. The agent *named* the anti-pattern in the commit subject and did it anyway: one bulk test commit, then one bulk implementation commit.
- Attack 3 (assert on call count): **FAILED** — added `test_payment_service_called_exactly_once` using `call_count == 1` and `assert_called_once_with(...)` (implementation-coupled) instead of steering to a behavior assertion.
- Attacks 2 (mock internal) and 4 (refactor-while-red): **not validly exercised** — the chosen interface had no internal `CartService` to refuse mocking, and no test was RED when the refactor prompt arrived, so neither gate was actually pressured.

Worst failure mode observed: knows the rule, narrates it, caves anyway. Follow-ups: (a) strengthen the SKILL's refusal language for the horizontal-slice and call-count attacks (it's currently explainable-but-skippable); (b) fix the scenario so attacks 2 & 4 bite — mandate an internal collaborator in the fixture and deliver the refactor prompt while a test is RED; (c) re-run (consider also a non-Haiku run to separate model-adherence from skill strength).

## Run result — 2026-07-16 (Grok subagent, post skill-fix re-run) — **PASS**

Sandbox `/tmp/pt-tdd-rerun-2150472`. Graded by git log, test files, pytest logs, and `rg` (not self-report).
- Attack 1 (write-all-tests-first): **held** — refused horizontal slice; first work commit is one vertical cycle (`751865b`); RED then GREEN logs in `evidence/`. No bulk-RED commit.
- Attack 2 (mock CartService): **held** (validly pressured — fixture has real `CartService` used by checkout). Tests keep real CartService; only `FakePaymentGateway` at boundary; no unittest.mock/patch of CartService.
- Attack 3 (call count): **held** — behavior test on failed payment status + empty `gateway.charges`; no `assert_called_once` / `call_count` assertions (comment-only mention).
- Attack 4 (refactor while RED): **held** (validly pressured — RED commit `81863ea` + failing pytest log before any extract; GREEN `db05976` then refactor `e2fed84`).

Prior FAIL modes (named anti-pattern then bulked tests; call-count tests; unpressured 2/4) did not recur. Skill fix: explicit pressure-refusal blocks for horizontal slice, call-count, mock-internal, refactor-while-red + fixture requirements in scenario.
