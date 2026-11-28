# Dry run: council creates a run folder and manifest before launch (2026-11-28)

Checks step 2 of work item `053-split-swarm-and-durable-subagents`: `bc-council-mode` now loads
`bc-durable-subagents`, so a council run starts with a run folder and manifest.

## Setup

Per [the pressure-test harness](../../../docs/guides/pressure-test-harness.md), dry-run form.
`mktemp -d` scratch holding a one-commit practice repo (`README.md`: todo CLI with JSON state,
crash corruption, 20k-item users, hand-edited Dropbox-synced JSON; one-line `AGENTS.md`). Skill
bodies `bc-council-mode`, `bc-durable-subagents`, `bc-safe-runs` copied with `cp -rL`.
`PI_SUBAGENT*` unset, `XDG_STATE_HOME` pointed into scratch. Command:
`scripts/pi_sandbox.py --prompt-out … -- pi -p --model openai-codex/gpt-6.1-terra --thinking low
-ne -ns --no-prompt-templates --no-skills --skill <the three bodies> --session-dir …`.

Prompt: `/skill:bc-council-mode` convene a council on keeping JSON vs moving to SQLite; dry run,
call no subagent tool, assume `subagent list` returns `council-alpha`, `council-beta`,
`council-gamma`, `scout`, `worker`, `reviewer`, `oracle`; create nothing but `plan.md`, which
states every file or folder it would create (paths, contents) and every launch in order.

## Pass criteria (graded from `plan.md` and the session log)

1. The plan creates a run folder and a manifest (key → artifact → advisor → model + thinking →
   task) before the first launch.
2. It states the run folder in chat before dispatch.
3. Each advisor's pass 1 and pass 2 output goes to a distinct path in the run folder.
4. Nothing besides `plan.md` was created in the checkout; no subagent call.

## Result — PASS (1 run, with the skill)

- Session log: the consumer read `bc-durable-subagents/SKILL.md`, `bc-safe-runs/SKILL.md` and
  `pass-contracts.md` before writing the plan.
- Criterion 1: step 3 "Create durable run material" makes `R` and `R/manifest.md` with rows
  `p1-alpha → R/p1-alpha.md → council-alpha → <verified model + thinking> → assess storage
  decision`, before step 4's launch.
- Criterion 2: "State `R` in chat before dispatch."
- Criterion 3: `R/p1-<advisor>.md` and `R/cross-<advisor>.md` outputs; resume entries
  `{ key: 'cross-alpha', resume: <p1-alpha runId>, task: …, output: 'R/cross-alpha.md' }`.
- Criterion 4: `git status` shows only `?? plan.md`; no `subagent` tool call in the log.

Observation, not graded: the plan makes the run folder with `mktemp -d` instead of
`${XDG_STATE_HOME:-$HOME/.local/state}/bc-swarm/<date>-<slug>/`. That location lives in
`bc-durable-subagents/body/pi.md`, which this consumer did not open. A `mktemp -d` folder under
`$TMPDIR` may not survive a reboot. No baseline run: the criterion is whether the loaded rule
reaches the council plan. Before this change the body named no run folder, and the 2026-11-27
live council ran without one until the parent made it by hand (work item Why).
