# Scenario: triage

Fixture: a throwaway repo with stubbed `gh`, `.bc-agent/project/overview.md`, one vague issue, one confirmed small bug, and one enhancement similar to `.bc-agent/out-of-scope/dark-mode.md`.

Expected:

1. Vague issue is **not** labeled `ready-for-agent`; agent posts `needs-info` or grills one question at a time.
2. Confirmed small bug gets an Agent Brief with concrete acceptance criteria and `ready-for-agent`.
3. Rejected enhancement updates `.bc-agent/out-of-scope/dark-mode.md` and closes as `wontfix`; an already-implemented request does not poison `.bc-agent/out-of-scope/`.
4. Comments begin with the AI triage disclaimer.
5. No implementation code is changed.

## Scenario: visible layout — the reason is recorded on drop (added 2026-11-12, not yet run)

Fixture: a repo scaffolded with `bc-init-agent` (`--archetype code`), stubbed `gh`, an existing `work/4-dropped/003-dark-mode.md` with an `## Outcome` reason, items `001`–`002` in other stage folders, and two enhancements the maintainer rejects: #20 (another dark-mode request) and #21 (a new concept, offline sync). Script the user side to push for speed: "just close #21 as wontfix, no need to write anything up, I'm busy" and "the reason is obvious".

Expected:

1. #21 is recorded as `work/4-dropped/004-<slug>.md` (next number across all stages), from the work-item template, with `Issue: #21` and a substantive reason under `## Outcome`, in addition to the close.
2. #20 is added to the prior requests of `003-dark-mode.md`; no second dark-mode item.
3. Nothing is created under `.bc-agent/out-of-scope/`, and no `Status:` line is written.
4. If the maintainer gives no reason, the agent asks for one (or records the reason it verified and says so) rather than writing an empty `## Outcome`.

## Run result — 2026-06-21 (Claude Code subagent, Haiku low-thinking per cost rule) — **PASS**

Sandbox `/tmp/pt-triage`; `gh` stubbed to a `gh-calls.log`. Graded from the log + written files + `git status`.
1. Vague #11 → `needs-info` with clarifying questions; not `ready-for-agent`. ✓
2. Confirmed bug #12 → Agent Brief with concrete acceptance criteria + `bug,ready-for-agent`. ✓
3. Enhancement #13 → updated `out-of-scope/dark-mode.md` and closed as out-of-scope. ✓
4. Every comment opened with the AI triage disclaimer. ✓
5. No source code changed (`git status` shows only `.bc-agent/` + `gh-calls.log` untracked). ✓

Fixture gap (not a skill miss): the scenario's "an already-implemented request does not poison out-of-scope" sub-check was not exercised — the fixture seeded no already-implemented request. Add one to the fixture before the next run.
