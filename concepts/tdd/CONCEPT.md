---
test_kind: pressure
test_status: partial
tested: 2026-11-05
deployed: yes
---
# Concept: tdd

Model-invoked discipline for test-driven development: a red-green-refactor loop that builds features or fixes bugs one vertical slice at a time, testing behavior through public interfaces. The correctness feedback loop that lets an agent run human-in-the-loop or unattended without drifting silently.

## Design decisions

- **Broad invocation.** Test edits, bug fixes and features with tests trigger the discipline even when tests are incidental; opt-in test-first wording missed ordinary work.
- **Unattended planning.** Delegated/headless agents record behavior priorities and interface decisions rather than waiting for unavailable approval; interactive approval remains unchanged.
- **Tests after code still need RED.** Coverage/regression/characterisation additions require a watched behavioral failure and restored green, recording both runs.
- **Inject inline boundaries.** A keyword boundary parameter with the real default preserves behavior while exercising owned helpers; out-of-scope seam changes are reported, not replaced with internal patches.
- **Confirm old-code RED.** The stdlib archive-and-overlay CLI isolates current changed tests from current production code without touching the user's Git state. Missing-symbol failures warn rather than claim behavioral sufficiency; unchanged production requires a manual mutation.

- **Tests that lie.** Merge the talk’s three classes into the existing internal-mock refusals. A sampled, read-only audit found private-helper patches/call assertions dominant in orchestrator tests (roughly 25–40% in one sample, not a census); use boundary fakes, public entry points and independent oracles instead. The per-test regression self-check sharpens the existing RED step, not a new result state.

- **Behavior-through-interface is the core rule.** Tests verify what the system does via public APIs, not how it does it internally. The named anti-test is the implementation-detail test (mocks internal collaborators, asserts call counts, breaks on refactor without behavior change). Detail in `body/tests.md`.
- **Vertical, not horizontal.** "Write all tests, then all code" is the explicit anti-pattern — bulk tests assert imagined behavior and the shape of things. One test → one implementation → repeat, each cycle informed by the last. Shared framing with `to-tickets` tracer bullets.
- **Mock only at system boundaries.** `body/mocking.md` draws the line: external APIs/DB/time/FS yes; your own collaborators no — via dependency injection and SDK-style interfaces.
- **Never refactor while RED.** Refactoring is safe only with a green test as the safety net; `body/refactoring.md` lists candidates.
- **Pressure-refusal gates (2026-07-16).** Horizontal-slice, call-count, mock-internal, and refactor-while-red each get an explicit refuse-under-pressure clause after the 2026-06-21 FAIL (agent named the anti-pattern and still committed it).
- **Composes `codebase-design`.** Planning step reaches for the deep-module vocabulary and testability checks rather than restating them.
- **Progressive disclosure.** Lean `SKILL.md`; `tests.md` / `mocking.md` / `refactoring.md` loaded only when that depth is needed. (Upstream's `refactoring.md` was recovered as a summary; reconstructed faithfully — see provenance.)
- **`untested` as a TDD result state considered and rejected (2026-09-06).** A review findings table needs a third state because a skipped check and an inapplicable one look identical. A TDD cycle does not: its states are exhaustive (the test exists and fails, or exists and passes). A third "result" would become a sanctioned route past RED and would defeat "watch it fail for the right reason." The blocked case — no runner, missing fixture, unbuildable environment — is a stop-and-report, not a result value.

- **Standard-library boundary patches allowed (2026-11-05).** Patching `subprocess.run` or `urlopen`, even via the module under test (`patch('tags.subprocess.run')`), fakes the external call; replacing the module's own functions/helpers/classes is what is forbidden. Owner decision after a kernel-only run graded such patches as failures under a too-strict criterion; injection stays preferred when tests need several patches.
- **Assertion scope and small fixes (2026-11-05)** — watched-fail and planning rules cover new tests or behaviour-changing assertions, not mechanical test maintenance. Explicit regression-test bug-fix wording preserves discovery without making tdd the diagnosis owner; diagnosing-bugs still owns unclear repros. Small, clear fixes skip interactive plan approval, not RED/GREEN. Drain feature workers retain the same red-green loop; code-review’s tests-that-lie definitions and both outgoing storage/glossary contracts are unchanged. The kernel now loads tdd for this scope; fake-boundary details have one home here.

## Provenance

- Owner-repo test-quality audit (2026-11-05): read-only, all ~2,400 tests in one repo; process causes traced to opt-in description, approval step in unattended jobs, inline boundaries; repository and code not reproduced.
- Confirm-RED idea sources: https://alex.kirk.at/2023/10/09/new-unit-tests-need-to-fail-running-the-old-code/ and https://dontcodethisathome.com/proving-a-generated-test-can-fail-mutation-testing-as-a-sufficiency-gate-for-an-ai-coding-agent .

- [Matt Pocock talk source](../../docs/research/raw/pocock-pr-bottleneck-talk/SOURCE.md) and [research notes](../../docs/research/raw/pocock-pr-bottleneck-talk/research-notes.md) — checks that lie (~5–7 min) and merge danger (~17–18 min), selectively adapted, not the reviewer-write model.
- Owner-supplied agent-test audit (2026-11-04), three read-only sampled reports covering orchestration, products and harnesses — evidence for same-function oracles, source-text coverage claims, subsystem-erasing fixtures and private-helper patches; no suite execution or mutation validation. Generic examples only; audit repository and code are not reproduced.

- [mattpocock/skills](https://github.com/mattpocock/skills) `captured-skills.md` — verbatim `tdd/SKILL.md`, `tests.md`, `mocking.md`; `refactoring.md` recovered as a summary and reconstructed. https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd
- [AI Engineer Workshop 2026.md](https://www.aihero.dev/ai-engineer-workshop-2026~dwnll) — workshop's TDD execution step (agent writes failing test, then code, then commits).
- [obra/superpowers `skills/test-driven-development/`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/test-driven-development/) — strict red/green/refactor wording, “watched it fail” iron law, rationalization table, and testing anti-patterns; absorbed as reinforcement rather than a duplicate concept.
- [obra/superpowers `skills/writing-skills/`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/writing-skills/) — applies the same TDD loop to process documentation; informs workspace test-gate practice.
- [michaelshimeles/skills `evidence-driven-testing`](https://github.com/michaelshimeles/skills) — prompted the blocked-cycle clause (a test that cannot be executed is not a RED). The upstream `untested` result was considered for this skill and rejected (see design decisions). Restated; upstream has no root LICENSE. (2026-09-06)

## Tests

2026-11-05: Better-tests scenarios T1–T3 run A/B (without/with skill) on the private pressure-test model in `tests/pocock-pressure.md` § Better-tests run: T2 seam and T3 tests-after-code **helped**, T1 discovery not discriminating. `confirm-red.py` has 44 unit tests (`tests/test_confirm_red.py`, mutation-checked). Status stays `partial`: discovery and the unattended mode have no discriminating run.

`tests/pressure-tdd.md` — scripted attacks (write-all-tests-first; mock-an-internal; assert-on-call-count; refactor-while-red). **2026-06-21 FAIL**; skill refusal gates + fixture requirements tightened; **2026-07-16 PASS** (Grok re-run, all four attacks held and 2/4 validly pressured).

## Deploy targets

- Claude Code: `~/.claude/skills/tdd` → relative symlink to `body/`. Discipline skill — deploy after the pressure run holds (or flag as deployed-pending-test in index).
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../docs/harnesses.md`.

## Storage safety contract

2026-10-27 owner-approved Btrfs ENOSPC prevention update: consume the kernel Storage safety contract; tooling/threshold authority is `~/Sync/Scripts/docs/disk-management/storage-prevention.md`. New storage pressure scenarios are authored, not run; historical test/deploy dates above do not certify this revision. See [shared scenarios](../agent-kernel/tests/storage-safety.md).
