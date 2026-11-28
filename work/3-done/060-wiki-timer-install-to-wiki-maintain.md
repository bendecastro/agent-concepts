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

- [x] Move the step and point setup at it. Done when lint passes and a setup dry run on a fixture still offers and describes the timer correctly.
- [x] Tune step 10 after the Haiku FAIL (qmd-vs-promotion, confirmation gate, parking-lot line inline) and rerun the timer scenarios. Done when the tuned body holds 4/4 on the pressure model.

## Outcome

The timer install moved to `bc-wiki-maintain`'s `INSTALL-TIMER.md`; setup step 10 offers the timer and loads it. After the Haiku FAIL (1/4), step 10 was tuned by owner choice (2026-11-28): qmd search is not promotion, "just enable"/"don't ask" is not confirmation of the shown units, and a declined install leaves a parking-lot TODO. Rerun on Terra low: tuned 4/4, master 1/4 (`concepts/bc-setup-project/tests/pressure-wiki-maintain-timer-results-terra-2026-11-28.md`). Moved onto master without 055's pre-merge copy. Open: setup never installs `bc-wiki-notify@.service`; filed separately.
