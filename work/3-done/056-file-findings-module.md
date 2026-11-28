# One bc-file-findings skill files a review's findings after the owner picks

Why: `bc-find-bugs`, `bc-improve-codebase-architecture` and `bc-council-audit-security` each restate how findings become work items, and only `bc-find-bugs` has the tested parts (use an answer already in the message; plan every chosen item). `bc-self-improve`, `bc-prototype` and `bc-council-challenge-plan` would use it too.
Done when: `bc-file-findings` holds the rules (wait for the pick; chosen → numbered planned item with Kind/Source; rejected → dropped with Outcome; rest → ideas; number only from the main checkout; index check), the three callers load it, and the find-bugs filing scenario passes against it.
Stage: now
Blocked by: 055-project-files-in-scaffold
Kind: architecture
Source: modularity scan 2026-11-27 (run ~/.local/state/bc-swarm/2026-11-27-agents-modularity/memo.md), owner pick 1 (candidate C)
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes
Dependencies: none new

## Steps

- [x] Create the skill from `bc-find-bugs` §5, point the three callers and the three would-be callers at it, add `loads` edges. Done when lint passes and `bc-plan-to-pipeline/tests/pressure-plan-every-item-results-2026-11-24.md`'s scenario holds when run against the new skill.

## Outcome

New `bc-file-findings` skill (deployed) holds the filing rules; `bc-find-bugs`, `bc-improve-codebase-architecture` and `bc-council-audit-security` load it, and `bc-self-improve`, `bc-prototype` and `bc-council-challenge-plan` load it when their output becomes project work. The security audit narrows it: only picked findings are filed, the rest stay in the git-ignored run folder (owner decision from `020-council-later-chains`). Find-bugs filing scenario on Haiku low (Codex out of quota): with the skill 3/3 after one tune, without 3/3, so it shows parity, not improvement. Security audit filing section rerun 2/2 on Haiku. Open: architecture planning scenario C1 not rerun against the skill (noted in its CONCEPT). Review blocked once; fixes verified.
