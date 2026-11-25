# Dashboard data: work records a dashboard can read

Why: people want a dashboard of their projects' work, but who holds an item, its history, review and gate results, and its time and cost are free text, only in git, or not recorded, and everything else needs Markdown parsing.
Done when: `work_index.py --json` prints every work-data field documented on the reference page; the skills that start, review, gate and close work write the `Held by:`, `Review:`, `Gate:` and `Spent:` lines; the workflow guide points people at the JSON; requirements in [requirements.md](requirements.md).
Stage: next
Blocked by: 024-skill-delivery
Kind: feature
Source: bc-plan-to-pipeline
Planned: bc-plan-to-pipeline 2026-11-25
Ready for agent: yes

## Steps

- [ ] JSON output and reference page: `work_index.py --json` (in `concepts/bc-init-agent/body/`) prints the existing fields per item (folder, header lines, steps with Notes, Outcome) with a format version; a reference page in `concepts/bc-init-agent/body/` lists every field, its source and whether it is stable or best-effort, including the fields later steps add (marked planned); this repository's `.bc-agent/scripts/work_index.py` refreshed. Blocked by: nothing. Stories 1, 2. Done when tests on fixture work folders pass (watched failing first), `--json` writes no files and `--check` is unchanged. Out of scope: the new records.
- [ ] Item history from git: the JSON gains per-item history (each folder move and step tick with its commit date), following renames. Blocked by: JSON output and reference page. Story 4. Done when tests on a scratch git repository cover moves, ticks and renames, and an uncommitted item gets an empty history. Out of scope: history lines written by agents.
- [ ] Held by line: format and parser (JSON adds the line's age), `--check` warnings for malformed lines and for a `Held by:` line in a done item; the scaffolded work-item rules and `bc-pipeline-to-done`'s work-item source write it when starting or resuming and remove it when stopping or finishing; `bc-work-sync` reports stale ones. Blocked by: Item history from git. Stories 3, 7. Done when parser tests pass and a pressure test (blind baseline, pressure-test model) shows an agent writing and removing the line. Out of scope: heartbeats.
- [ ] Review and Gate lines: formats and parsers in the step Notes, `--check` warnings; `bc-pipeline-to-done` (work-item source and review contract) and the scaffolded rules record them per step. Blocked by: JSON output and reference page. Stories 5, 7. Done when parser tests pass and a pressure test shows a drain step recording both. Out of scope: GitHub issue sources.
- [ ] Spent line: a script beside `work_index.py` estimates an item's active time, tokens and cost from Pi session files (Claude Code and Codex where their files allow; others named as not counted) for sessions in the item's active period whose folder is the project or a worktree and that mention the item; the closing instructions call it and paste the line; JSON parses it. Blocked by: Item history from git. Story 6. Done when tests on scrubbed fixture session files per tool pass, including no match, and a pressure test shows an agent closing an item writing the line. Out of scope: exact cost where a tool records no usage.
- [ ] Docs and migration: `bc-init-agent`'s `MIGRATIONS.md` note for older projects; the workflow guide gains a short section on building your own dashboard on `--json`, linking the reference page; glossary checked against the final formats. Blocked by: Held by line, Review and Gate lines, Spent line. Story 8. Done when lint has 0 ERROR and every field on the reference page exists in the JSON. Out of scope: any dashboard.

## Outcome

<Filled when the item is finished or dropped: what happened, or why it was dropped.>
