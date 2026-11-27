# Stranger rerun with the npm package (044), 2026-11-27

**Result: setup and planning pass; the build FAILED (it stalled on a question and never built). The 044 step stays open.**

Both attempts installed the committed HEAD with `STRANGER_SOURCE=pack scripts/stranger_end_to_end.sh`: `npm pack`, unpack, `pi install <unpacked dir>` (what `pi install npm:agent-concepts` delivers), then `pi install npm:pi-subagents` 0.90.0 on Pi 1.6.1. Nothing was copied into the sandbox's agent directory; skills, kernel and roles came from the package only.

## Attempt 1, 16:51–17:14: anthropic/claude-haiku-5-5 low, not graded

Consumer: anthropic/claude-haiku-5-5 low (owner choice 2026-11-27 for this release). Install `5137d11` passed, but every model call was refused with HTTP 429 `rate_limit_error` (16 errored turns in setup, 32 in the build), so no phase ran. The limit persisted afterwards, so the orchestrator switched the model.

## Attempt 2, 19:06–19:52: openai-codex/gpt-6.1-terra low

Model: openai-codex/gpt-6.1-terra low (orchestrator choice after Haiku stayed rate-limited). Installed revision `29ae424`.

| Phase | Evidence (from files) | Grade |
|---|---|---|
| Install | `Installed /box/src/package`, `Installed npm:pi-subagents`; no copied roles | pass |
| Setup | `AGENTS.md`, `.bc-agent/`, `work/`, `scripts/gate` exist; `scripts/gate` exits 0 on the fixture copy; origin `main` has `Set up project agent workspace` | pass |
| Plan | `work/1-planned/003-normalize-internal-whitespace.md`: `Ready for agent: yes`, requirements, one step; pushed as `Plan internal whitespace normalization` | pass |
| Build | origin `main` tip is still the plan commit; no code or test change anywhere. Final reply: "I can't tell which item "yes" refers to. Reply **1** for whitespace or **2** for guardrails." | **FAIL** |

Build transcript, condensed ([excerpt](evidence/npm-pack-rerun-build-stall.md)):

1. Driver asks permission to push to `origin` `main` (fine).
2. The stranger answers: "Build the whitespace item I just planned. Yes, push to the local origin … main only."
3. Driver: "**001-guardrails-setup-checks** is ahead of it in the pipeline. The drain's work-item rules say not to skip an eligible item. Which should run first? 1. Whitespace (recommended) … 2. Guardrails". 
4. Neutral "Yes, that's fine. Go ahead." twice; the driver re-asks, then refuses to guess. Script answer budget (3) exhausted.

## Attempt 3, 20:27–21:12: openai-codex/gpt-6.1-terra low, test-driver fault

Installed revision `d308141` (after the named-item and bare-yes fixes). Setup passed. Planning asked three questions instead of two: the third was the new dependency question ("Reply `1` or `2`."), which has no question mark, so the scripted stranger took it as the end of the phase and never answered; no plan was written or pushed. The build then correctly reported that no whitespace item exists and asked for it. Not graded as a skill failure: the driver now also answers a "Reply `…`" choice (`scripts/stranger_rpc_driver.py`, with a test), and the rerun is attempt 4.

## Friction a stranger hits

| # | Where | What happened | Status |
|---|---|---|---|
| N1 | Attempt 1, every phase | On a provider 429 every phase ends with an empty reply; the error is only in the RPC stream. | Pi behavior; recorded only. |
| N2 | Install | The tarball is `agent-concepts-0.3.0.tgz`: `package.json` still says 0.3.0. | Release step must raise the version. |
| N3 | Build (blocker) | Setup's new starter items (`001-guardrails-setup-checks`, `002-architecture-review`, both `Ready for agent: yes`) sit ahead of the user's freshly planned item, so the pipeline refuses to build the item the user named without a numbered reorder answer, even though the user already said which item to build. | Open: needs a fix in `bc-pipeline-to-done` (an explicit user naming of an item should count as the reorder decision) and/or in the starter items' readiness from 045. Needs a work item. |
| N4 | Build | A "yes" to a numbered choice is rejected rather than taken as the recommended option; a stranger answering conversationally loops. | Same work item as N3. |
| N5 | Build | The build session ran 40 minutes (21 subagent calls) before stalling. | Recorded. |
