# Work data: the `work_index.py --json` fields

`python3 .bc-agent/scripts/work_index.py --json [work-dir]` prints one JSON object describing every work item in `work/1-planned/`, `work/2-active/`, `work/3-done/` and `work/4-dropped/` (month folders included). It writes no files, so a dashboard can run it as often as it likes. This page lists every field, where it comes from, and whether you can rely on it.

- **Stable**: the field exists in every output with this format version, and its meaning does not change. A missing source line gives `null` (or an empty list), never a missing key.
- **Best-effort**: the field is read from text people and agents write by hand, so it can be missing, stale or loosely formatted. Show it, but do not build logic that breaks when it is odd.
- **Planned**: a later step of the dashboard-data work adds it; it is not in the output yet.

`format_version` changes only on a breaking change (a field removed, renamed or given a new meaning). New fields are added without a version change, so ignore keys you do not know.

## Top level

| Field | Source | Reliability |
|---|---|---|
| `format_version` | the script (currently `1`) | stable |
| `stages` | the `Stages:` line in `.bc-agent/AGENTS.md` (default `now, next, later, unscheduled`) | stable |
| `items` | one entry per item file or folder, ordered planned, active, done, dropped, then by folder and name | stable |

## Per item

| Field | Source | Reliability |
|---|---|---|
| `number` | the first three digits of the item name (`025`) | stable |
| `slug` | the item name after the number (`dashboard-data`) | stable |
| `name` | the full item name (`025-dashboard-data`) | stable |
| `folder` | the lifecycle folder: `planned`, `active`, `done` or `dropped` | stable |
| `path` | the item file relative to `work/` (`2-active/025-dashboard-data/plan.md`) | stable |
| `title` | the first `# ` heading | best-effort |
| `header` | the header lines below (an object) | stable keys, best-effort values |
| `steps` | the `- [ ]` / `- [x]` lines under `## Steps` (a list) | stable keys, best-effort values |
| `outcome` | the text under `## Outcome`, trimmed; `null` when the section is missing or empty (may still be the template placeholder) | best-effort |
| `history` | folder moves and step ticks with their commit dates, from `git log` following renames | planned |
| `spent` | the `Spent:` line in the Outcome, parsed | planned |

## Header lines (`header`)

Each value is the text after the label on its line, trimmed, or `null` when the line is absent or empty. The values are the raw text, not validated; the non-JSON run of the script and `--check` validate open items.

| Field | Line | Reliability |
|---|---|---|
| `why` | `Why:` | best-effort |
| `done_when` | `Done when:` | best-effort |
| `stage` | `Stage:` | stable for open items (the script rejects unknown stages); best-effort otherwise |
| `blocked_by` | `Blocked by:` (comma-separated item names or `nothing`) | stable for open items; best-effort otherwise |
| `kind` | `Kind:` | best-effort |
| `source` | `Source:` | best-effort |
| `planned` | `Planned:` | best-effort |
| `ready_for_agent` | `Ready for agent:` (`yes` when set) | best-effort |
| `waiting_on_owner` | `Waiting on owner:` (the owner question) | best-effort |
| `held_by` | `Held by: <tool> <session> since <YYYY-MM-DD HH:MM>`, plus the line's age | planned |

## Steps (`steps[]`)

| Field | Source | Reliability |
|---|---|---|
| `text` | the step line and its indented continuation lines (joined with newlines), without the `Notes:` part | best-effort |
| `checked` | `[x]` or `[X]` is `true`, `[ ]` is `false` | stable |
| `notes` | the text after `Notes:`, inline in the step or on an indented line below it; `null` when there is none | best-effort |
| `review` | `Review: <approved \| changes requested> by <reviewer> <YYYY-MM-DD>` lines in the Notes | planned |
| `gate` | `Gate: <pass \| fail> <command> at <commit> <YYYY-MM-DD>` lines in the Notes | planned |

Why the records live in work-item lines and git history rather than in a separate store: the agent-concepts repository's decision record `docs/decisions/0003-work-data-lives-in-work-item-lines.md`.
