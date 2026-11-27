# Rerun the stranger test through building and landing

Why: The first stranger run (`docs/research/2026-11-27-stranger-end-to-end/README.md`) stopped before the pipeline launched any child, and its planning and build sessions ran without the project instructions setup wrote (`-nc`, now removed from the driver), so building, review, landing on the bare remote and whether workers run only targeted tests are still untested for a stranger.
Done when: One run of `scripts/stranger_end_to_end.sh` reaches the build phase's landing step or records the new stall; results are filed next to the first run with each stall fixed or turned into an item.
Stage: later
Blocked by: 038-starter-items-pass-index-check
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes
Kind: tests
Source: 033-stranger-end-to-end-test

## Steps

- [ ] Rerun: one run on the pressure-test model with at most one infrastructure retry; capture child prompts too. Done when the results folder exists and every stall has an item or a fix.

## Outcome

