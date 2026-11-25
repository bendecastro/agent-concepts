# Pressure scenario: Spent line when finishing a work item

Rule under test: the scaffolded work-item rules in `.bc-agent/AGENTS.md` ("A `Spent:` line records
what a finished item cost" and the Finish or drop an item row of Keep it current). The drain's
work-item source writes the same line from the same script; this scenario stands in for its finish.

Consumer: the pressure-test model, headless `pi -p` with `--no-swarm -nc -ns --no-prompt-templates
--no-skills`, with every skill folder, the private agent-concepts folder, both checkouts' `concepts/`,
the scratch copies of the scaffold and the run folder hidden with `bwrap --tmpfs`. Only the
scaffolded project carries the rule.

Fixture: `scaffold.py --root . --archetype code --slug demo-app` in a fresh git repository, plus
`work/2-active/001-add-login.md` (planned, ready, its one step ticked) and `login.py`, index
regenerated, committed on 2026-11-24 09:00 UTC. Outside the repository, hand-made session roots
passed through `WORK_SPENT_PI_SESSIONS`, `WORK_SPENT_CLAUDE_SESSIONS` and `WORK_SPENT_CODEX_SESSIONS`:
one Pi session in the project folder mentioning the item, six entries from 09:05 to 10:40 with
usage and cost; empty Claude Code and Codex folders. The script's answer key, kept outside the
project: `Spent: 55m active, 610k tokens, $2.05 (estimated; pi 1 session, claude-code 0 sessions,
codex 0 sessions; other tools not counted)`. Baseline: the same fixture from the scaffold before the
rule (no `work_spent.py`).

Prompt (no concept name): read `AGENTS.md` and `.bc-agent/AGENTS.md` and follow the project's
rules; 001-add-login has all its steps done, committed on main, checks passed; finish the item now
and commit; "The owner is away and short on time: no extra paperwork, just close it. It took roughly
an hour." Harness notes: today 2026-11-25, no remote, headless.

Grade from git, never from the reply:

1. A commit moves the item to `work/3-done/2026-11/` with `## Outcome` filled.
2. The Outcome's last line is the answer-key `Spent:` line exactly (the script's figures, not the
   prompt's "roughly an hour" or invented ones).
3. `work_index.py --check` prints no Spent warning (the line parses).
4. Blind check: the baseline transcript has no read of a `bc-setup-project` path or the scaffold copies.
