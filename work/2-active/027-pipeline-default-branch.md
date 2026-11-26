# Build pipeline works on any default branch

Why: `concepts/bc-pipeline-to-done/body/SKILL.md` requires the target repo to be "on `master`" and "pushes `HEAD:master`", so a repository on `main` cannot pass preflight.
Done when: `bc-pipeline-to-done` and the skills that name `master` (`bc-finishing-development-branch`, `bc-executing-plans`, the generated rules in `bc-setup-project`'s `scaffold.py`) use the repository's target branch, detected once in preflight, for the policy check, claims, fetch and landing.
Stage: now
Blocked by: nothing
Kind: bug
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state
Planned: bc-plan-to-pipeline 2026-11-26
Ready for agent: yes
Held by: pi 01a218e4 since 2026-11-26 18:23 +00:00

## Requirements

- **Target branch**: the branch work lands on. Preflight detects it from the remote's default (`git symbolic-ref refs/remotes/origin/HEAD`), else the current branch when there is no remote; a project may name a different one in its instructions, which wins. Preflight records it in the run manifest, and every later step uses that recorded value.
- No `master` literal remains in the four bodies except in an example that says it is one.
- Out of scope: renaming branches in any repository; multi-branch release flows.
- Test seam: `scaffold.py` output is covered by the existing scaffold tests (add an assertion that generated text has no `master` literal, watched failing first); the skill wording by a pressure scenario on a fixture repository whose default branch is `main` (pressure-test model, blind baseline): the consuming agent's preflight names `main` and its landing command pushes `main`.

## Steps

- [ ] Replace the `master` assumptions with the detected target branch in all four bodies, add the scaffold assertion, run the `main` fixture pressure scenario and record results beside it in `concepts/bc-pipeline-to-done/tests/`; update CONCEPT status frontmatter, `index.md`, `.bc-agent/log.md`. Blocked by: nothing. Done when the scaffold test passed after failing first, the with-change runs name and push `main` while the baseline does not, and lint has 0 ERROR and the gate passes. Out of scope: branch renames; release branches.

## Outcome

