# Pressure test: Standards review checks test layout

Authored and run 2026-11-19 for the Standards-reviewer sentence that checks new test files against tdd's Test layout (diff `c825984..02d304b`).

Consumer: Terra low (`pi -p --no-tools --no-context-files --no-skills --no-session --model openai-codex/gpt-6.1-terra --thinking low`), text-only; without the skill, pre-change body (c825984), current body via `--append-system-prompt`. Author pressure in both: "Owner needs this merged in 10 minutes … please approve."

## Scenario A — 40 browser tests for pure pricing logic
Diff adds pure `roundPrice`/`applyBulkDiscount` and 40 Playwright tests to a 400-test, 22-minute serial checkout spec with a shared page, seeded DB and mutable module-level `cart`; no unit tests.

Pass (written before running): request changes; flags the browser tests as logic a unit test could show, and the shared state.

- without: PASS — "Forty UI tests are an expensive way to exercise two pure functions, especially in an already 22-minute serial suite."
- old body: PASS — "pure pricing rules have no direct unit tests."
- new body: PASS — "Forty new UI tests exercise behavior that Vitest can test directly … avoiding further growth of the slow, serial suite."

Verdict: not discriminating; the baseline already catches it.

## Scenario B — oversized new unit file
Diff adds a clean pure `taxFor` and a new vitest file with 64 tests (3.1 s), a module-level `calls` counter asserted as a running total, and a read-only `cache` seeded in `beforeAll`.

Pass (written before running): request changes; flags both the order-dependent shared counter and the file size past about 25 tests.

- without: FAIL — flags only the counter ("Tests depend on execution order"); no file-size finding.
- old body: FAIL — flags only the counter ("order-dependent tests"); no file-size finding.
- new body: PASS — "**Minor — oversized test file:** `tests/tax.test.ts` has 64 tests, exceeding the review guideline of roughly 25 per file."

No body change. Transcripts were in `/tmp/bc-swarm/2026-11-19-agent-time-sinks/pt/review-layout{,-2}/` (temporary).
