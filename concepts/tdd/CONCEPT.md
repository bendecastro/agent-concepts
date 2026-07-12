# Concept: tdd

Model-invoked discipline for test-driven development: a red-green-refactor loop that builds features or fixes bugs one vertical slice at a time, testing behavior through public interfaces. The correctness feedback loop that lets an agent run human-in-the-loop or unattended without drifting silently.

## Design decisions

- **Behavior-through-interface is the core rule.** Tests verify what the system does via public APIs, not how it does it internally. The named anti-test is the implementation-detail test (mocks internal collaborators, asserts call counts, breaks on refactor without behavior change). Detail in `body/tests.md`.
- **Vertical, not horizontal.** "Write all tests, then all code" is the explicit anti-pattern — bulk tests assert imagined behavior and the shape of things. One test → one implementation → repeat, each cycle informed by the last. Shared framing with `to-issues` tracer bullets.
- **Mock only at system boundaries.** `body/mocking.md` draws the line: external APIs/DB/time/FS yes; your own collaborators no — via dependency injection and SDK-style interfaces.
- **Never refactor while RED.** Refactoring is safe only with a green test as the safety net; `body/refactoring.md` lists candidates.
- **Composes `codebase-design`.** Planning step reaches for the deep-module vocabulary and testability checks rather than restating them.
- **Progressive disclosure.** Lean `SKILL.md`; `tests.md` / `mocking.md` / `refactoring.md` loaded only when that depth is needed. (Upstream's `refactoring.md` was recovered as a summary; reconstructed faithfully — see provenance.)

## Provenance

- `raw/ingested/pocock-skills-upstream/captured-skills.md` — verbatim `tdd/SKILL.md`, `tests.md`, `mocking.md`; `refactoring.md` recovered as a summary and reconstructed. https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd
- `raw/ingested/AI Engineer Workshop 2026.md` — workshop's TDD execution step (agent writes failing test, then code, then commits).
- `raw/ingested/obra-superpowers/skills/test-driven-development/` — strict red/green/refactor wording, “watched it fail” iron law, rationalization table, and testing anti-patterns; absorbed as reinforcement rather than a duplicate concept.
- `raw/ingested/obra-superpowers/skills/writing-skills/` — applies the same TDD loop to process documentation; informs workspace test-gate practice.

## Tests

`tests/pressure-tdd.md` — scripted attacks on the discipline (write-all-tests-first; mock-an-internal; assert-on-call-count; refactor-while-red). Expected: vertical loop holds, mocking stays at boundaries, no refactor while RED. Scenario authored; full pressure run pending.

## Deploy targets

- Claude Code: `~/.claude/skills/tdd` → relative symlink to `body/`. Discipline skill — deploy after the pressure run holds (or flag as deployed-pending-test in index).
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../harnesses.md`.
