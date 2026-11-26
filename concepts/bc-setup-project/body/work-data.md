# Work data: the `work_index.py --json` fields

`python3 .bc-agent/scripts/work_index.py --json [work-dir]` prints one JSON object describing every work item in `work/1-planned/`, `work/2-active/`, `work/3-done/` and `work/4-dropped/` (month folders included). It writes no files, so a dashboard can run it as often as it likes. This page lists every field, where it comes from, and whether you can rely on it.

- **Stable**: the field exists in every output with this format version, and its meaning does not change. A missing source line gives `null` (or an empty list), never a missing key.
- **Best-effort**: the field is read from text people and agents write by hand, so it can be missing, stale or loosely formatted. Show it, but do not build logic that breaks when it is odd.

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
| `history` | folder moves and step ticks, oldest first, from one `git log --follow` on the item file (renames followed); `[]` when the file is uncommitted, outside a git repository or git is missing. Uncommitted moves and ticks are not shown yet | best-effort |
| `held_by` | the `Held by:` line parsed (below); `null` when the item has none | best-effort |
| `spent` | the `Spent:` line in the Outcome, parsed (below); `null` when the Outcome has none | best-effort |

## Header lines (`header`)

Each value is the text after the label on its line, trimmed, or `null` when the line is absent or empty. The values are the raw text, not validated; the non-JSON run of the script and `--check` validate open items.

| Field | Line | Reliability |
|---|---|---|
| `why` | `Why:` | best-effort |
| `done_when` | `Done when:` | best-effort |
| `stage` | `Stage:` | stable for open items (the script rejects unknown stages); best-effort otherwise |
| `blocked_by` | `Blocked by:` (comma-separated item names or `nothing`) | stable for open items; best-effort otherwise |
| `kind` | `Kind:` | best-effort |
| `needs_owner` | `Needs owner:` (what the owner must decide or do, and when) | best-effort |
| `source` | `Source:` | best-effort |
| `planned` | `Planned:` | best-effort |
| `ready_for_agent` | `Ready for agent:` (`yes` when set) | best-effort |
| `waiting_on_owner` | `Waiting on owner:` (the owner question) | best-effort |
| `held_by` | `Held by:` (the raw line; parsed in the item's `held_by` field) | best-effort |

## Held by (`held_by`)

`Held by: <tool> <session> since <YYYY-MM-DD HH:MM> <UTC or +HH:MM>` names the agent working on the item: its tool (`pi`, `claude-code`, `codex`, ...), its session name or id (no spaces), and when it started, in UTC or local time with its offset (`Held by: pi swift-otter since 2026-11-25 14:05 +01:00`). The agent writes it when it starts or resumes the item and removes it when it stops or the item closes, so a crashed agent leaves a stale line; judge staleness from the age.

| Field | Source | Reliability |
|---|---|---|
| `tool`, `session`, `since` | the parts of the line; all `null` when the line does not match the format (`--check` warns) | best-effort |
| `committed` | committer date (ISO 8601) of the last commit that added or removed this exact line, from `git log -S`; `null` when the line is uncommitted or there is no git | best-effort |
| `age_seconds` | seconds from `committed` to now; `null` with it | best-effort |

## History events (`history[]`)

Every event has `event`, `date` (the commit's committer date, ISO 8601) and `commit` (the full SHA). Read from git, so a squashed or rewritten history shows fewer events, and a commit that splits a file below git's rename similarity breaks the trail.

| `event` | Extra fields | Meaning |
|---|---|---|
| `created` | `folder` | the commit that first added the item file |
| `moved` | `from`, `to` (lifecycle folders) | a commit that moved the item to another lifecycle folder (a move between month folders is not an event) |
| `ticked` | `step` (the first line of the step, without inline Notes) | a commit that turned `- [ ]` into `- [x]` for that step; ticks already present when the file was added are not events |

## Steps (`steps[]`)

| Field | Source | Reliability |
|---|---|---|
| `text` | the step line and its indented continuation lines (joined with newlines), without the `Notes:` part | best-effort |
| `checked` | `[x]` or `[X]` is `true`, `[ ]` is `false` | stable |
| `notes` | the text after `Notes:`, inline in the step or on an indented line below it; `null` when there is none | best-effort |
| `review` | the `Review:` lines in the Notes, parsed (below); `[]` when there are none | stable keys, best-effort values |
| `gate` | the `Gate:` lines in the Notes, parsed (below); `[]` when there are none | stable keys, best-effort values |

## Review and Gate (`steps[].review[]`, `steps[].gate[]`)

Each result is one line in the step's Notes, starting its own line (an indented line under the step, or right after `Notes:`), oldest first; a later round adds a line rather than replacing one.

- `Review: <approved | changes requested> by <reviewer> <YYYY-MM-DD>`: a review verdict and who gave it (a reviewer agent or role, or `owner`), for example `Review: approved by reviewer 2026-11-25`.
- `Gate: <pass | fail> <command> at <commit> <YYYY-MM-DD>`: one run of the project's check command as run, and the short or full SHA the checked tree was built on, for example `Gate: pass make check at 3f2a9c1 2026-11-25`.

| Field | Source | Reliability |
|---|---|---|
| `review[].result`, `reviewer`, `date` | the parts of a `Review:` line; all `null` when it does not match the format (`--check` warns) | best-effort |
| `gate[].result`, `command`, `commit`, `date` | the parts of a `Gate:` line; all `null` when it does not match the format (`--check` warns) | best-effort |
| `text` (both) | the line after its label, trimmed | best-effort |

## Spent (`spent`)

`Spent: <active time> active, <tokens> tokens, <cost> (estimated; <sources>)` is the last line of a finished item's `## Outcome`, for example `Spent: 2h 10m active, 3.4M tokens, $5.20 (estimated; pi 3 sessions, claude-code no files, codex 0 sessions; other tools not counted)`. The agent that finishes the item pastes it from `python3 .bc-agent/scripts/work_spent.py <item-name>` (`--json` lists the counted sessions).

The script takes the item's active period from its history (first move into `2-active/` to its move out, or now) and counts every session with an entry in that period whose working folder is the project or one of its git worktrees and whose file mentions the item name. Active time sums the gaps between a session's entries in the period, each capped at 15 minutes, so parallel sessions add up. Tokens include cache reads and writes. It reads Pi (`~/.pi/agent/sessions`, with cost), Claude Code (`~/.claude/projects`, tokens only) and Codex (`~/.codex/sessions`, tokens only); `<sources>` gives each tool's session count, or `no files` when its folder is missing, and other tools are not counted. A session that mentions the item only in passing is counted; a worktree removed before the item closes is not matched, but a Pi child (subagent) session, kept under its parent's folder (`<parent-id>/.../*.jsonl` beside `<parent-id>.jsonl`), counts when its parent counts, whatever its folder and whether or not it names the item, as long as it has an entry in the period; a child that matches on its own is counted once, and `--json` gives each session's `via` (`match` or `child of <parent file>`). `WORK_SPENT_PI_SESSIONS`, `WORK_SPENT_CLAUDE_SESSIONS` and `WORK_SPENT_CODEX_SESSIONS` override the folders.

Read the estimate as a rough size, not a bill. Its known limits:

- **Parallel sessions add up.** Two sessions working at the same time count twice, so active time can be longer than the time that passed.
- **Child sessions count whole.** A child (subagent) session of a counted session is counted for its time in the period, even if that child worked on a different item.
- **Some sessions are missed or counted wrongly.** A session that only mentions the item in passing is counted; a session in a git worktree that was removed before the item closed is not found (unless it is a child of a counted session); Claude Code and Codex give no cost; other tools are not read at all.

| Field | Source | Reliability |
|---|---|---|
| `active`, `tokens`, `cost`, `sources` | the parts of the line as written (`1h 5m`, `2.5M`, `$3.10` or `cost unknown`, the text after `estimated; `); all `null` when it does not match the format (`--check` warns) | best-effort |
| `text` | the line after its label, trimmed | best-effort |

Why the records live in work-item lines and git history rather than in a separate store: the agent-concepts repository's decision record `docs/decisions/0003-work-data-lives-in-work-item-lines.md`.
