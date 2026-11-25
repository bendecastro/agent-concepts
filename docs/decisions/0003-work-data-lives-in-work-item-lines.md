# 0003: Work data for dashboards lives in work item lines and git history

Date: 2026-11-25
Status: accepted

## Context

People who use these skills want a dashboard of their projects' work: which items are active, which agent holds each one, what happened to it, whether it passed review and the gate, and what it cost. The work folders already hold stage, steps and owner questions, but who holds an item, review and gate results, and time and cost are free text or not recorded at all. Any format chosen here becomes a contract that other people's dashboards parse, so it is costly to change later.

## Decision

- Who holds an item is a `Held by:` line in the item's header lines, written when an agent starts on it and removed when it stops.
- Item history (folder moves, step ticks) is worked out from git history by the work index script; agents write no history lines.
- Review and gate/CI results are fixed-format `Review:` and `Gate:` lines in the step's Notes.
- Time and cost are a `Spent:` line in the Outcome, written by a script that reads the agent tools' own session files when the item closes, and marked as estimated.
- The work index script prints all of it as JSON, and a reference page lists every field and whether it is stable or best-effort.

## Consequences

- A dashboard reads one JSON output instead of parsing Markdown, and the item files stay readable for people.
- Agents must keep the `Held by:` line true; a crashed agent leaves a stale line, so the JSON gives its age and readers judge staleness.
- History depends on commits: work that was never committed has no history.
- Cost figures are only as good as each agent tool's session files; tools without them give time only.

## Alternatives considered

- GitHub claim markers as the holder record: they cover only unattended runs and need a network call.
- Agents writing `History` lines: a second copy of what git already records, which drifts.
- A separate results file per item: one more file per item and per step, away from the step it describes.
- Agents counting their own time and cost: they forget, and they cannot see their own token use.
