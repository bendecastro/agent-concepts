# Stranger end-to-end test of v0.5.0 from npm `next`, 2026-11-28

**Result: fail (rerun at 09:22 UTC). The model answered this time, and the change with its test reached the bare remote's `main`, but the planning session built, committed and filed the change as done instead of leaving a ready work item, so the build session had nothing to build and pushed that commit without running the pipeline's roles. `latest` stays at 0.4.1; v0.5.0 is not promoted.** The first two attempts (inconclusive, HTTP 429) are kept below as history.

## Rerun, 09:22–09:50 UTC

- Consumer model: `anthropic/claude-haiku-5-5` at thinking `low`, the owner-approved substitute for Terra while the Codex quota is out.
- Package: `npm:agent-concepts@0.5.0` as published, `pi-subagents` 0.90.0, Pi 1.6.1. Test scripts from commit `5911903`.
- Cause of the earlier 429s: the sessions ran without the operator's account-pooling Pi extension (`pi-multiprovider`), so every call went to one rate-limited account. For this rerun the operator ran a scratch copy of `stranger_end_to_end.sh` with three additions, none in the repository: the extension and its credential store copied into the scratch directory (deleted with it), `-e /box/mp` added to `STRANGER_PI`, and a one-line probe (`pi -p --no-session -ne -e /box/mp --model anthropic/claude-haiku-5-5:low "Reply OK"`) after the auth check, which answered `OK`. The extension picks which account serves a request; it adds no system-prompt text or tools. No 429 appears in any phase's RPC stream.
- Isolation `isolation ok`; personal-term audit `grep -Ff <private list>` over the three saved system prompts exited 1 (clean).

| Check | Result | Evidence |
|---|---|---|
| Setup | pass | Scaffold, `AGENTS.md`, `.bc-agent/`, `work/`, executable `scripts/gate` (passes); commit `Set up agent workspace (code archetype, local gate, no CI)` pushed to the bare remote. |
| Planning | **fail** | After the grill (three questions) and the scripted answer ending "Go ahead with the plan.", the session wrote tests, changed `tinylabels/__init__.py`, wrote the item to `work/1-planned/`, then moved it to `work/3-done/2026-11/001-normalize-label-whitespace.md` with an Outcome and committed `Collapse internal whitespace in normalize; file work item 001` (local only). Its own words: "The work is finished, so I'll move the item to done". No ready item was left for the pipeline. |
| Build lands on the bare remote's `main` | pass by artifact only | `origin/main` tip `Collapse internal whitespace in normalize; file work item 001` (code, two tests, done item). It came from the planning session; the build session only ran the gate and pushed `98dbef5..d1e3b6a`. |
| Pipeline roles ran | **fail** | 0 `subagent` tool calls in the build session. Its reply: "I did not run the drain's auditor, builder and reviewer jobs. The item was already built and gated". |
| Workers ran targeted tests only | not observed (no worker started) | |
| Stalls | one | `bc-plan-to-pipeline` on Haiku low took "Go ahead with the plan" as permission to implement. Filed as an idea in `work/0-ideas.md`. |

Evidence (RPC streams, sessions, system prompts, fixture, logs) is private, outside the repository.

## First run (inconclusive, history)

Recipe: [stranger-end-to-end.md](../../scripts/stranger-end-to-end.md), run as releasing step 11 ([releasing.md](../guides/releasing.md)):
`STRANGER_SOURCE=npm STRANGER_VERSION=0.5.0 EVIDENCE=<private dir> MODEL=anthropic/claude-haiku-5-5 THINKING=low scripts/stranger_end_to_end.sh`.

- Consumer model: `anthropic/claude-haiku-5-5` at thinking `low`, replacing Terra (`openai-codex/gpt-6.1-terra`) because the Codex quota is used up (owner decision, 2026-11-28).
- Package: `npm:agent-concepts@0.5.0` as published (dist-tags at the time: `latest` 0.4.1, `next` 0.5.0), plus `pi-subagents` 0.90.0 on Pi 1.6.1.
- Test scripts from commit `91b872a97d7095916f40445aafc193d25c991af5`.
- Evidence (RPC streams, sessions, fixture, install logs) is kept private outside the repository, as the recipe says.

### Attempts

| Attempt | Time (UTC) | Install | Setup | Plan | Build |
|---|---|---|---|---|---|
| 1 | 07:56–08:10 | pass: `Installed npm:agent-concepts@0.5.0`, `Installed npm:pi-subagents`; `pi auth check`: `ready` | not run: 20 errored turns, 0 tool calls, empty final reply | not run: 20 errored turns, 0 tool calls | not run: 40 errored turns, 0 tool calls; stopped by the operator |
| 2 (the one retry for an infrastructure failure) | 08:14–08:20 | pass, same lines | not run: 20 errored turns, 0 tool calls | not run: 20 errored turns, 0 tool calls | not run: 20 errored turns, 0 tool calls; stopped by the operator |

Every errored turn carries the same message in the RPC stream: `429 {"type":"error","error":{"type":"rate_limit_error","message":"This request would exceed your account's rate limit. Please try again later."`. The bare remote's `main` in both attempts holds only `Create tinylabels fixture`.

Between the attempts a one-line host call to the same model (`pi -p --model anthropic/claude-haiku-5-5 --thinking low "Say OK"`) answered `OK`, so the limit was not a hard outage; the sandboxed sessions, which send the full kernel and skill system prompt, were still refused. Other Haiku pressure tests were running in parallel in the same run, which may share the account's limit. The 2026-11-27 npm-pack rerun's attempt 1 hit the same refusal on Haiku ([npm-pack rerun](2026-11-27-stranger-end-to-end/npm-pack-rerun.md)).

### Audit

The sandbox check passed in both attempts (`isolation ok`). The run was stopped before the script saved system prompts, so the operator extracted them from the saved RPC streams with the script's own code: three distinct prompts per attempt. `grep -Ff <private term list>` over them exited 1: no private term.

### Grades

| Check | Result |
|---|---|
| Setup | not graded (no model turn succeeded) |
| Planning | not graded |
| Build lands on the bare remote's `main` | not graded |
| Workers ran targeted tests only | not observed (no worker started) |
| Stalls | none attributable to the skills; the only stop is the provider refusal (infrastructure) |

### Next (superseded by the rerun)

Rerun releasing step 11 when the provider limit allows (a quiet account on Haiku, or Terra once the Codex quota returns). Until then `latest` stays at 0.4.1, per releasing step 13's spirit: no promotion without a passing stranger test.

## Next

Fix or decide the planning stall (the idea in `work/0-ideas.md`), then rerun releasing step 11. Until a run passes, v0.5.0 stays on `next`.
