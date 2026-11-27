# The generated .bc-agent/AGENTS.md owns role lookup and the work-item numbering rule

Why: 12 skills each explain how to resolve a project file through the "Where things go" table, and the "number work items only in the main checkout; in a worktree add an ideas line" rule exists in 5 wordings. Owner choice: the bc-agent scaffold holds it, not a new skill.
Done when: `bc-setup-project`'s generated `.bc-agent/AGENTS.md` states the role-lookup rule, the no-table defaults and the numbering rule once; callers say only "resolve <role> from the Where things go table" with no restated rule; the migration steps tell earlier projects how to add the block.
Stage: now
Blocked by: 050-ship-setup-migrations
Kind: architecture
Source: modularity scan 2026-11-27 (run ~/.local/state/bc-swarm/2026-11-27-agents-modularity/memo.md), owner pick 1 (candidate B; owner: use the bc-agent scaffold)
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Requirements

- Callers: `rg -l "Where things go" concepts/*/body` (12 today). Each caller's own fallback paths that differ (plan: `docs/changes/`, triage: `.bc-agent/out-of-scope/`) stay in the caller unless the scaffold's table already names them.
- A skill running in a project without the table still needs a safe default: keep one line per caller ("if there is no table, use <default>").
- Regenerate this repository's own `.bc-agent/AGENTS.md` from the scaffold or update it by hand to match; scaffold tests cover the new block.

## Steps

- [ ] Add the block to the scaffold, trim the callers, add the migration step. Done when a new scaffold carries the block (test), the five numbering wordings are gone (`rg`), lint passes, and `bc-plan-to-pipeline`'s numbering pressure scenario still holds.

## Outcome

_To be filled when finished or dropped._
