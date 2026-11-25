# Requirements: dashboard data

## Problem Statement

People who run these skills across several projects want a dashboard of their work: what is active, which agent is on it, what happened to it, whether it passed review and the gate, and what it cost. The work folders hold the stage, the steps and owner questions, but a dashboard has to parse Markdown to read them. Who holds an item, review and gate results are free text, item history is only in git, and time and cost are recorded nowhere.

## Solution

The work index script gains a JSON output carrying every work-data field, documented on one reference page that says which fields are stable and which are best-effort. Three new fixed-format records fill the gaps: a `Held by:` line in the item header, `Review:` and `Gate:` lines in step Notes, and a `Spent:` line in the Outcome written by a script that reads the agent tools' session files. Item history is worked out from git, with nothing new for agents to write. The skills that start, review, gate and close work write these records. The workflow guide tells people they can build their own dashboard on the JSON. Decision: [0003](../../../docs/decisions/0003-work-data-lives-in-work-item-lines.md).

## User Stories

1. As someone building a dashboard, I want one JSON output per project, so that I do not parse Markdown.
2. As someone building a dashboard, I want a reference page listing every field, where it comes from and whether it is stable, so that I know what I can rely on.
3. As a project owner, I want to see which agent is working on each active item and since when, so that I can tell live work from abandoned work.
4. As a project owner, I want each item's history (when it was planned, started, each step ticked, finished), so that I can see how work moved without reading git.
5. As a project owner, I want each step's review and gate results in a fixed format, so that a dashboard can show which steps passed.
6. As a project owner, I want each finished item's estimated time, tokens and cost, so that I can see what work costs.
7. As an agent, I want the skills to tell me exactly when to write and remove each record, so that the records stay true without extra judgment.
8. As someone with an older project, I want a migration note, so that I can adopt the records without re-scaffolding.

## Implementation Decisions

- The canonical script is `concepts/bc-setup-project/body/work_index.py`; projects get it as `.bc-agent/scripts/work_index.py` through `bc-setup-project`, and this repository's own copy is refreshed from it.
- JSON output: `work_index.py --json` prints one object with a format version, the project's stages, and one entry per item: number, slug, folder (stage of the pipeline), path, title, header lines (Why, Done when, Stage, Blocked by, Kind, Source, Planned, Ready for agent, Waiting on owner, Held by), steps (text, ticked, Notes, parsed Review and Gate lines), Outcome, parsed Spent line, and history. It writes no files. The format version changes only on a breaking change.
- History: from `git log` of the item's path(s), following renames: the commit date of each folder move and of each step tick. Uncommitted changes have no history entry.
- `Held by:` format: `Held by: <tool> <session name or id> since <YYYY-MM-DD HH:MM>` (local time with offset or UTC, stated on the reference page). Written in the same commit that moves an item to work-active or resumes it; removed when the agent stops or the item moves to done. JSON adds the line's age from its last commit; staleness is the reader's judgment.
- `Review:` format: `Review: <approved | changes requested> by <reviewer role or name> <YYYY-MM-DD>`. `Gate:` format: `Gate: <pass | fail> <command> at <commit> <YYYY-MM-DD>`. Both go in the step's Notes; a step may carry several (one per round).
- `Spent:` format: `Spent: <active time> active, <tokens> tokens, <cost> (estimated; <sources>)`. A script (shipped beside `work_index.py`) finds the sessions of the item's active period (from history) whose working folder is the project or one of its worktrees and that mention the item's slug, and sums them. Pi first; Claude Code and Codex where their session files allow; a tool without usable files is named as not counted. It prints the line; the closing instructions call it and paste the line.
- `work_index.py --check` warns (no exit change) on malformed `Held by:`, `Review:`, `Gate:` and `Spent:` lines, and on a `Held by:` line in a done item.
- Skills that write the records: the work-item rules scaffolded by `bc-setup-project` (start, stop, close), `bc-pipeline-to-done`'s work-item source (claim, review, gate, landing), `bc-work-sync` (repairs and reports stale or malformed records). Each change keeps the generic wording and overlay rule of these skills.

## Testing Decisions

- Unit tests for the JSON output and each parser on fixture work folders, including malformed lines and older projects without the new lines; the format test fails first.
- History tests on a scratch git repository built by the test (folder moves, step ticks, renames), cleaned up by the test runner's temp storage.
- `Spent:` script tests on fixture session files for each tool (small, scrubbed), including no matching session and a tool without files.
- Pressure tests (the test gate) for the reworded discipline parts: an agent starting and stopping an item writes and removes `Held by:`; a drain step records `Review:` and `Gate:` lines; closing an item writes `Spent:`.

## Out of Scope

- Any dashboard, including the owner's own; it becomes its own work item in its own project.
- Answering owner questions from a dashboard.
- GitHub issue-based work (only work items).
- Exact cost for tools whose session files carry no usage data.
- A live agent-presence feed or heartbeat.

## Further Notes

Evidence for the current state of the work data and the owner's dashboard: two scout reports from the 2026-11-25 skill-delivery run (pipeline data and dashboard sources), summarised in this item's planning conversation. Owner choices 2026-11-25: full version plus time and cost; `Held by:` line; history from git; fixed-format lines in step Notes; `Spent:` line from session files; the owner's dashboard is a separate item.
