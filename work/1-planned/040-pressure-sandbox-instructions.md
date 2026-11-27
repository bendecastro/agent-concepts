# Pressure-test sandboxes load the right instruction files

Why: In the 2026-11-26 drain, 3 of 10 items needed a review round because a test session read the wrong instruction files: the owner's private instructions decided 029's baseline, the owner's `APPEND_SYSTEM.md` reached both arms of 030's carry-on run, and 033's `-nc` hid the project's own `AGENTS.md` (reflection report in the owner's archive, 2026-11-27).
Done when: One sandbox helper empties the harness's global instruction files, keeps the project's own files, and is used by both the pressure-test guide and `scripts/stranger_end_to_end.sh`; before each run a check extracts the session's system prompt and fails on a private-denylist term or on a project `AGENTS.md` that exists but did not load.
Stage: next
Blocked by: nothing
Kind: tests
Source: bc-self-improve reflection on the 2026-11-26 drain; replaces the `work/0-ideas.md` line about harness masks

## Steps

- [ ] Shared sandbox helper and system-prompt check: extract the masking from `scripts/stranger_end_to_end.sh` and the system-prompt extractor from the 033 audit into one helper; use it in the stranger test; document it in `docs/guides/pressure-test-harness.md`. Done when a test shows the check failing on a sandbox that leaks a global instruction file and on one run with `-nc`, and passing on the helper's default.
- [ ] Re-check the 2026-11-26 pressure runs of 026, 027, 028 and 029 for comparisons the owner's rules could have decided; record each verdict in its results file. Done when each results file states whether its comparison stands.

## Outcome
