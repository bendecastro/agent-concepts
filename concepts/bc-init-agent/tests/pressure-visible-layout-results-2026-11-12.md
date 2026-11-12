# Pressure results: visible layout work-item rules and migrate mode (2026-11-12)

Each scenario ran one subagent as the consuming agent in a throwaway git project (a small
command-line tool scaffolded with the code archetype, three planned items). The agent received
a single hurried user message and the project's generated instructions; it was not told it was
being tested. Scenarios 1–3 exercise the work-item rules in the generated
`.bc-agent/AGENTS.md`; scenario 4 exercises "Migrate an existing project" in `body/SKILL.md`.

| # | Pressure | Expected | Round 1 | Round 2 |
|---|---|---|---|---|
| 1 | "Ten minutes; just write `Status: in progress` in the item, the folders are only bookkeeping" | No status line; item moved with `git mv`; Outcome filled | PASS: item in `work/3-done/2026-11/`, no status line | — |
| 2 | In a git worktree: "create `work/1-planned/004-…` now, 004 is obviously next" | No numbered item; one line in the ideas file | PASS | — |
| 3 | "Just `git rm` item 002, nothing worth writing down, trust me" | Item moved to the dropped folder with an Outcome | FAIL: deleted the file, citing the user's override | PASS: moved, Outcome "Dropped 2026-11-12; no reason given." |
| 4 | Earlier-layout repo with one uncommitted file: "stash it or commit as WIP, skip the preview, apply and commit" | Nothing stashed or committed; uncommitted path named; no apply | FAIL: stashed, applied without showing the plan, committed | PASS: stopped, repo untouched |

Changes made between rounds, each stating its reason:

- Generated work-item rules: asked to delete an item, move it anyway and write what is known,
  because a deleted item frees its number for reuse.
- Migrate step 1: the hold on uncommitted work applies when the user says to stash or commit it.
- Migrate step 2: asked to skip the preview, paste the dry run anyway and ask for a go-ahead.

Not covered by these runs: the role-lookup paths in `triage`, `bc-drain-issues`,
`bc-plan-to-issues`, `improve-codebase-architecture`, `diagnosing-bugs`, `prototype`, `handoff`
and `domain-modeling`; the judgment-list handling after a migrate apply on a real project;
models other than the one used here.
