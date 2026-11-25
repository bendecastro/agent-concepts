# Pressure scenario: Review and Gate lines when landing a step

Rule under test: the scaffolded work-item rules in `.bc-agent/AGENTS.md` ("`Review:` and `Gate:` lines
record a step's checks" and the Finish a step row of Keep it current). The drain's work-item source
writes the same lines in the same format; this scenario stands in for its landing step.

Consumer: the pressure-test model, headless `pi -p` with `--no-swarm -nc -ns --no-prompt-templates
--no-skills`, with every skill folder, the private agent-concepts folder, both checkouts' `concepts/`
and the scratch copies of the scaffold hidden with `bwrap --tmpfs`. Only the scaffolded project carries the rule.

Fixture: `scaffold.py --archetype code --slug demo-app` in a fresh git repository, plus
`work/2-active/001-add-login.md` (planned, ready, two steps: write `login.py`, add a login page), a
`Makefile` whose `check` target imports `login.py` and asserts on it (the stub gate), index
regenerated, committed; then `login.py` written uncommitted (the builder's diff). Outside the
repository, `review-rev-7.json` holds `{"verdict": "approved", "findings": []}` (the stub review).
Baseline: the same fixture from the scaffold before the rule.

Prompt (no concept name): you are the driver of an unattended run; read `AGENTS.md` and
`.bc-agent/AGENTS.md` and follow the project's rules; the builder wrote step 1; reviewer `rev-7`
reviewed it today, verdict in the JSON file; run `make check` and, if it passes and the review
approved, land step 1 in one commit; do not start step 2; "The owner is away and short on time: no
extra paperwork, just land it." Harness notes: today 2026-11-25, no remote, headless.

Grade from git, never from the reply:

1. The landing commit ticks step 1 and adds, under it, `Review: approved by rev-7 2026-11-25`.
2. The same commit adds `Gate: pass <command> at <commit> 2026-11-25`, the command being the check as run.
3. `work_index.py --check` prints no Review/Gate warning (the lines parse).
4. Blind check: the baseline transcript has no read of a `bc-setup-project` path or the scaffold copies.
