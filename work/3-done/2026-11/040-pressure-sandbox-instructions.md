# Pressure-test sandboxes load the right instruction files

Why: In the 2026-11-26 drain, 3 of 10 items needed a review round because a test session read the wrong instruction files: the owner's private instructions decided 029's baseline, the owner's `APPEND_SYSTEM.md` reached both arms of 030's carry-on run, and 033's `-nc` hid the project's own `AGENTS.md` (reflection report in the owner's archive, 2026-11-27).
Done when: One sandbox helper empties the harness's global instruction files, keeps the project's own files, and is used by both the pressure-test guide and `scripts/stranger_end_to_end.sh`; before each run a check extracts the session's system prompt and fails on a private-denylist term or on a project `AGENTS.md` that exists but did not load.
Stage: next
Blocked by: nothing
Kind: tests
Source: bc-self-improve reflection on the 2026-11-26 drain; replaces the `work/0-ideas.md` line about harness masks
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Requirements

- One helper under `scripts/` (shell or Python, matching what `scripts/stranger_end_to_end.sh` already does) that runs a Pi command with the harness's global instruction files (`~/.pi/agent/AGENTS.md`, `APPEND_SYSTEM.md`, and any other always-loaded global file Pi 1.6.1 reads) replaced by empty files, deployed skill folders and private overlays hidden, and the project's own `AGENTS.md`/`.bc-agent/AGENTS.md` left in place. No `-nc` by default.
- A pre-run check, part of the helper: start the session, take its system prompt (from the RPC stream or session JSONL; the stranger script already extracts it from RPC), and fail when it contains a term from the private denylist (`~/.config/agent-concepts/personal-terms.txt`, skipped with a note when absent) or when the working directory holds a project `AGENTS.md` whose text is missing from the prompt.
- `scripts/stranger_end_to_end.sh` and `docs/guides/pressure-test-harness.md` both use it; the guide's command loses `-nc` and explains why (the 033 finding).
- Tests in `scripts/tests/` that fake only the Pi process boundary.

## Steps

- [x] Shared sandbox helper and system-prompt check: build the helper, switch the stranger script and the pressure-test guide to it, add tests. Done when a test shows the check failing on a sandbox that leaks a global instruction file and on a run with `-nc` in a project that has an `AGENTS.md`, and passing on the helper's default; and one real Pi start (no model turn needed if the prompt is available before one) passes the check. Out of scope: rerunning the stranger test (039-stranger-rerun); other harnesses than Pi; changing any skill body.
- [x] Re-check the 2026-11-26 pressure runs of 026-setup-starter-items, 027-pipeline-default-branch, 028-missing-private-tool-fallbacks and 029-setup-green-gate-and-ci for comparisons the owner's private instructions could have decided: read each run's recorded command and, where kept, its session system prompt. Record a one-line verdict (stands / does not stand, with the reason) in each results file, and correct the concept's `test_status` only where a comparison does not stand. Blocked by: Shared sandbox helper and system-prompt check. Done when each results file states whether its comparison stands. Out of scope: rerunning those pressure tests (file an item if one does not stand).

## Outcome

Done 2026-11-27 (integrated; full gate passed on tree fafe65fe, 644 passed, 4 skipped). `scripts/pi_sandbox.py` masks the seven global instruction files Pi 1.6.1 reads from its agent folder (`AGENTS.override.md`, `AGENTS.md`, `AGENTS.MD`, `CLAUDE.md`, `CLAUDE.MD`, `SYSTEM.md`, `APPEND_SYSTEM.md`; only the ones that exist, resolved through symlinks because bwrap refuses to mount on one and would create absent files on the host), the deployed skill folders, the private overlays and any `.agents/skills` above the working folder. Before running, it starts the same command in RPC mode without a session, takes the `system` message Pi records before its first model request, aborts, and fails on a private-denylist term (home and working-folder prefixes replaced first, since skill and docs paths are not instructions) or on a project `AGENTS.md` whose text is missing. The pressure-test guide uses it with `-ne` and no `-nc`; the stranger script runs every session through it (`STRANGER_PI`) and checks with it that the fresh home has nothing to mask.

Finding: with the old guide flags the check fails on the owner's machine because the owner's Pi extensions add private text to the tools and rules sections; the guide now turns extensions off and names needed ones with `-e` (approved by the supervisor).

Checks (real Pi 1.6.1 starts on the pressure-test model, counted as checks): helper default with `-ne` passed; `-nc` failed on the missing project `AGENTS.md`; without `-ne` failed on an extension's private term; one full `-p` run through the helper read 0 bytes from the masked global files. Tests: `scripts/tests/test_pi_sandbox.py` (5) and `test_stranger_rpc_driver.py` (4), 9 passed.

Re-check of the 2026-11-26 runs (counted as results files, 8 in total): 7 stand, 1 does not. Does not stand: `bc-setup-project`'s no-CI gate comparison (the old arm followed the owner's private test-runner rules instead of running the gate); its `test_status` note is corrected and a rerun is in `work/0-ideas.md`. Stands with a caveat: the missing-publish-policy owner-away pass (the owner's away rule was in both arms). The owner's `APPEND_SYSTEM.md` preferences reached 6 of the 8 results' runs; the missing-machine-tools and existing-CI runs masked it.
