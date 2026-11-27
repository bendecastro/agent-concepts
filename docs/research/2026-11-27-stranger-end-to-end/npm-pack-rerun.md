# Stranger rerun with the npm package (044), 2026-11-27

**Result: attempt 4 passes every phase (install, setup, plan, build) on openai-codex/gpt-6.1-terra low. Attempt 2's build stall is fixed; the 044 rerun step is done.**

Every attempt installed the committed HEAD with `STRANGER_SOURCE=pack scripts/stranger_end_to_end.sh`: `npm pack`, unpack, `pi install <unpacked dir>` (what `pi install npm:agent-concepts` delivers), then `pi install npm:pi-subagents` 0.90.0 on Pi 1.6.1. Nothing was copied into the sandbox's agent directory; skills, kernel and roles came from the package only.

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

## Attempt 4, 21:15–21:48: openai-codex/gpt-6.1-terra low, pass

Installed revision `68864ef` (driver fix on top of `d308141`). Graded by the orchestrator from the evidence files.

| Phase | Evidence (from files) | Grade |
|---|---|---|
| Install | `Installed /box/src/package`, `Installed npm:pi-subagents`; no copied roles | pass |
| Setup | origin `main` has `Set up local agent workspace`; final reply "Pushed `cbfddd1` to the local remote" | pass |
| Plan | three questions answered, the third the dependency choice; the item's line reads `Dependencies: may add Hypothesis as a test-only dependency (owner's answer, 2026-11-27)`; pushed as `Plan internal whitespace normalization` | pass |
| Build | one scripted answer (the opening request) and no further question; origin `main` gained `Start whitespace normalization work`, `Normalize internal label whitespace`, `Finish whitespace normalization work`; `normalize` is `" ".join(label.split()).lower()`; the item is in `work/3-done/2026-11/`; the final reply reports a 6-test gate and two approving reviews; checkout clean and in sync | pass |

The named item was built although the starter items came first in the order (N3 fixed), and no "yes" had to be re-asked (N4 not reached).

## Friction a stranger hits

| # | Where | What happened | Status |
|---|---|---|---|
| N1 | Attempt 1, every phase | On a provider 429 every phase ends with an empty reply; the error is only in the RPC stream. | Pi behavior; recorded only. |
| N2 | Install | The tarball is `agent-concepts-0.3.0.tgz`: `package.json` still says 0.3.0. | Release step must raise the version. |
| N3 | Build (blocker) | Setup's new starter items (`001-guardrails-setup-checks`, `002-architecture-review`, both `Ready for agent: yes`) sit ahead of the user's freshly planned item, so the pipeline refuses to build the item the user named without a numbered reorder answer, even though the user already said which item to build. | Fixed: a named item sets the order for its run (`source-work-items.md`); attempt 4 passed. |
| N4 | Build | A "yes" to a numbered choice is rejected rather than taken as the recommended option; a stranger answering conversationally loops. | Fixed: the kernel reads a bare yes as the recommended option. |
| N5 | Build | The build session ran 40 minutes (21 subagent calls) before stalling. | Recorded. |
