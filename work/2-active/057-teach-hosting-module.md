# One home for how teach state maps onto a hosted .bc-agent vault

Why: `bc-teach` (about 1,650 words) defines the hosted path map and marker, `bc-wiki-maintain` § Teach adapter boundary copies it, and `bc-setup-project/body/scaffold.py` generates it; a change in one silently breaks the others.
Done when: The marker, the two path maps and the never-create rules live in one file (`bc-teach-hosting` or a shared file in `bc-teach/body/` that the others link via a `loads` edge), wiki-maintain and setup derive from it, and a test fails when scaffold output and the map disagree.
Stage: later
Blocked by: nothing
Kind: architecture
Source: modularity scan 2026-11-27 (run ~/.local/state/bc-swarm/2026-11-27-agents-modularity/memo.md), owner pick 1 (candidate D)
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes
Dependencies: none new

## Steps

- [x] Move the map to one home and point the two other skills at it. Done when lint passes, a scaffold test compares generated map to the home file, and bc-teach's hosted-vault pressure scenario still holds.

## Outcome

_To be filled when finished or dropped._
