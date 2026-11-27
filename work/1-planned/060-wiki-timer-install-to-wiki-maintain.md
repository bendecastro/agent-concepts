# The wiki timer install lives in bc-wiki-maintain, and setup loads it

Why: `bc-setup-project` step 10 (about 350 words) describes installing the wiki-maintain systemd timer, while the runner and its README live in `bc-wiki-maintain`; the procedure has two homes.
Done when: The install procedure lives in `bc-wiki-maintain` (next to `runner/`), `bc-setup-project` step 10 is one line that loads it, and a `loads` edge records it.
Stage: later
Blocked by: nothing
Kind: architecture
Source: modularity scan 2026-11-27 (run ~/.local/state/bc-swarm/2026-11-27-agents-modularity/memo.md), owner pick 1 (finding G)
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Steps

- [ ] Move the step and point setup at it. Done when lint passes and a setup dry run on a fixture still offers and describes the timer correctly.

## Outcome

_To be filled when finished or dropped._
