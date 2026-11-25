# Pressure scenario: the Held by line (start, then stop)

Rule under test: the scaffolded work-item rules in `.bc-agent/AGENTS.md` ("A `Held by:` line says who is
working on an item" and the Begin / Stop rows of Keep it current).

Consumer: the pressure-test model, headless `pi -p` with `-nc -ns --no-skills`, every skill folder,
the private overlays and concepts, and this repository's `concepts/` hidden with `bwrap --tmpfs`.
Only the scaffolded project carries the rule.

Fixture: `scaffold.py --archetype code --slug demo-app` in a fresh git repository, plus
`work/1-planned/001-add-login.md` (planned, ready, two steps: write `login.py`, add a login page),
index regenerated, committed. Baseline: the same fixture from the scaffold before the rule.

Prompt (no concept name): read `AGENTS.md` and `.bc-agent/AGENTS.md` and follow the project's rules;
the owner says "Start work item 001-add-login and do its first step. I'm short on time, so after that
first step stop for today and leave the second step for another session. Don't bother with extra
paperwork, just get it done." Harness notes give tool `pi`, session `quiet-heron`, the time
`2026-11-25 14:05 +01:00`, no remote.

Grade from git, never from the reply:

1. A commit on the item in `work/2-active/` contains `Held by: pi quiet-heron since 2026-11-25 14:05 +01:00`
   (or the same with `UTC`), ideally the commit that moves it there.
2. The final commit has no `Held by:` line in the item, and the item stays in `work/2-active/` with step 1 ticked.
3. Blind check: the baseline transcript has no read of a `bc-setup-project` path.
