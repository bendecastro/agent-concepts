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

- [x] Rerun: one run on the pressure-test model with at most one infrastructure retry; capture child prompts too. Done when the results folder exists and every stall has an item or a fix.

## Outcome

Done 2026-11-27. One run, no retry, installed `87782c9`: setup, planning, build, two reviews and landing on the bare remote's `main` all passed with no stall; workers ran targeted tests only. Finding R1 (`bc-tdd` told every project to Syncthing-ignore its property-test cache) is fixed in the same change; R3 (host path visible in the sandbox's process list) is an idea line. Results: `docs/research/2026-11-27-stranger-end-to-end/README.md` § Rerun after the fixes.
