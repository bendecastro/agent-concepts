# One bc-file-findings skill files a review's findings after the owner picks

Why: `bc-find-bugs`, `bc-improve-codebase-architecture` and `bc-council-audit-security` each restate how findings become work items, and only `bc-find-bugs` has the tested parts (use an answer already in the message; plan every chosen item). `bc-self-improve`, `bc-prototype` and `bc-council-challenge-plan` would use it too.
Done when: `bc-file-findings` holds the rules (wait for the pick; chosen → numbered planned item with Kind/Source; rejected → dropped with Outcome; rest → ideas; number only from the main checkout; index check), the three callers load it, and the find-bugs filing scenario passes against it.
Stage: now
Blocked by: 055-project-files-in-scaffold
Kind: architecture
Source: modularity scan 2026-11-27 (run ~/.local/state/bc-swarm/2026-11-27-agents-modularity/memo.md), owner pick 1 (candidate C)
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Steps

- [x] Create the skill from `bc-find-bugs` §5, point the three callers and the three would-be callers at it, add `loads` edges. Done when lint passes and `bc-plan-to-pipeline/tests/pressure-plan-every-item-results-2026-11-24.md`'s scenario holds when run against the new skill.

## Outcome

_To be filled when finished or dropped._
