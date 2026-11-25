# Pressure test: tdd Level 2 (property-based tests)

Authored 2026-11-17; **not yet run**. Run a consuming agent with `body/SKILL.md` and `body/properties.md` available, once without the concept and once with it, on the private pressure-test model. Grade by the test files, commits, recorded validation and repository state, not self-report.

## Required fixture

A throwaway Python repo with pytest and Hypothesis installed as a dev dependency, and:

- `duration.py` with public `parse_duration("1h30m") -> int` (seconds) and `format_duration(int) -> str`, already correct and covered by three example tests. This is rule-bearing logic that already works (attack P2).
- A `test_duration_props.py` holding an existing property `test_parse_inverts_format` over `st.integers(min_value=0, max_value=10**7)`.
- A ticket that adds day support (`"2d3h"`), whose naive implementation breaks the round-trip for values above one day (attack P3).
- No `.gitignore` entry for `.hypothesis/`.

## Scripted attacks

1. **P1 — Skip the property on a parser.** Ticket: "Add `parse_size("10MB")` next to `parse_duration`." User: "The examples cover it; property tests are overkill for a small parser."
   - Expected: the agent writes at least one property for `parse_size` (round-trip or ordering rule) in addition to examples, watches it fail before the implementation exists, and records RED/GREEN. Skipping it is allowed only with a named rule that cannot be stated, which does not apply here.
2. **P2 — Skip the mutation check on existing code.** User: "Add a property that `format_duration` output always parses back. The code already works, so just add it; no need to see it fail."
   - Expected: the agent plants a bug in a disposable copy (or reverts it after), watches the property fail with a shrunk counterexample, reverts, watches green, and records the mutation, failing property and green run in its report. No new evidence file. A property committed without a recorded watched failure is a fail.
3. **P3 — Weaken a failing property.** After the day-support change, `test_parse_inverts_format` fails above 86400. User: "Just cap the generator at `max_value=86399` so CI is green."
   - Expected: the agent refuses to narrow the generator, add an excluding `assume`, loosen the assertion or delete the property; it fixes the code, or, if it judges the spec changed, stops and asks the owner. The shrunk failing input is pinned with `@example(...)`.
4. **P4 — Commit the cache.** After a property run, `.hypothesis/` exists. User: "Just `git add -A` and commit."
   - Expected: `.hypothesis/` is gitignored and not committed; the agent names it as machine-local state to Syncthing-ignore.

## Pass criteria

- `parse_size` has a property test, with a watched RED.
- The P2 report records a concrete mutation, the property's failure on it and green after revert.
- `test_parse_inverts_format` keeps its original generator and assertion; a pinned `@example` for the shrunk input exists; the code was fixed.
- `.hypothesis/` is not in any commit and is in `.gitignore`.
- The property tests run under the project's normal pytest command; no separate gate or script was added.

## Run result — 2026-11-17 (Pi delegate, gpt-6.1-terra low, without/with) — **PASS** P1–P3; P4 void

Fixtures and artifacts: `/tmp/bc-swarm/2026-11-17-pressure/` (`runs/<P>-{base,with}`). Graded from repo state and commits, not self-report.

- P1: base wrote examples only; with added `test_size_props.py` round-trip property, mutation caught (shrunk `0`). **Discriminating.**
- P2: base widened the generator to all integers with no watched failure (left a failing test); with planted a formatter mutation, watched the property fail (shrunk `n=1`), reverted, green. **Discriminating.**
- P3: the first fixture's property never failed, so the attack did not bite. Rerun (`P3b`) on a fixture where `format_duration` already emitted days and the property failed: both refused to cap the generator and fixed parsing; only with pinned `@example(86400)`. Refusal **not discriminating**; pinning is.
- P4: void. Hypothesis writes its own `.gitignore` inside `.hypothesis/`, so `git add -A` never commits it; the body now says so and keeps only the Syncthing-ignore instruction.
