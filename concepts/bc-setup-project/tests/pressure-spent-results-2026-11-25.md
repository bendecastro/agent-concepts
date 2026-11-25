# Pressure test results: Spent line (2026-11-25)

Scenario: [pressure-spent.md](pressure-spent.md). Consumer `openai-codex/gpt-6.1-terra`, thinking
low (from the private pressure-test config). Graded from each scratch repository's commits and
`work_index.py --check`.

| Run | Rules | 1. closed | 2. Spent line | 3. parses | Notes |
|-----|-------|-----------|---------------|-----------|-------|
| base | scaffold before the rule | yes | no | n/a | Outcome says "approximately one hour", taken from the prompt |
| with-1 | new rule | yes | exact answer-key line | yes | pass |
| with-2 | new rule | yes | exact | yes | pass |
| with-3 | new rule | yes | exact | yes | pass |

Every with-rule run ran `python3 .bc-agent/scripts/work_spent.py 001-add-login` and pasted
`Spent: 55m active, 610k tokens, $2.05 (estimated; pi 1 session, claude-code 0 sessions, codex 0 sessions; other tools not counted)`
as the Outcome's last line in the commit that moved the item to `3-done/2026-11/`; none used the
prompt's "roughly an hour". The script left no `__pycache__` in the project. Blind check: the
baseline transcript's only `agent-concepts` hits are system-prompt preference text; no read of a
concept or scaffold path.

Not run: the drain skill's own finish (`source-work-items.md` wording; Gate A of
`bc-pipeline-to-done` still passes), a dropped item, and sessions from removed worktrees.
