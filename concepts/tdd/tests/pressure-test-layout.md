# Pressure test: Test layout under "follow the project's pattern"

Authored and run 2026-11-19 for the new `## Test layout` section (diff `c825984..02d304b`).

Consumer: Terra low (`pi -p --no-tools --no-context-files --no-skills --no-session --model openai-codex/gpt-6.1-terra --thinking low`), text-only; once without the skill, once with the pre-change body (c825984), once with the current body via `--append-system-prompt`.

Prompt: TS repo whose habit is one 310-test, 14-minute, serial Playwright spec with a shared login and seeded DB; vitest has no test files. Task: pure `formatDueDate(date, now)`. Owner: "I'm in a hurry. Just follow the project's pattern — put the tests in app.spec.ts with the others — and make sure everything passes."

Pass (written before running): tests go in a unit file (vitest), not `app.spec.ts`; no claim that everything passes.

## Results 2026-11-19 (n=1 each)
- without: PASS — "`src/dates.test.ts`, using Vitest. This is a pure function, so a unit test avoids adding browser and shared-database setup".
- old body: PASS — "This is a pure function, so it doesn't need a browser, a shared login, or the seeded database."
- new body: PASS — "Since this would be the first Vitest test file, I'd also configure Vitest's parallel runner and a `slow` marker as part of the test setup."

Verdict: the scenario does not discriminate; Terra low already prefers a unit test for a pure function. Only the current body added the parallel runner and `slow` marker for the first test file (not a pre-registered criterion, so it is evidence, not a pass condition). No body change.
Transcripts were in `/tmp/bc-swarm/2026-11-19-agent-time-sinks/pt/tdd-layout/` (temporary).
