# Stranger end-to-end test of v0.5.0 from npm `next`, 2026-11-28

**Result: inconclusive. Both allowed attempts were refused by the model provider (HTTP 429 `rate_limit_error`) on every call, so no phase ran and nothing was graded. `latest` stays at 0.4.1; v0.5.0 is not promoted.**

Recipe: [stranger-end-to-end.md](../../scripts/stranger-end-to-end.md), run as releasing step 11 ([releasing.md](../guides/releasing.md)):
`STRANGER_SOURCE=npm STRANGER_VERSION=0.5.0 EVIDENCE=<private dir> MODEL=anthropic/claude-haiku-5-5 THINKING=low scripts/stranger_end_to_end.sh`.

- Consumer model: `anthropic/claude-haiku-5-5` at thinking `low`, replacing Terra (`openai-codex/gpt-6.1-terra`) because the Codex quota is used up (owner decision, 2026-11-28).
- Package: `npm:agent-concepts@0.5.0` as published (dist-tags at the time: `latest` 0.4.1, `next` 0.5.0), plus `pi-subagents` 0.90.0 on Pi 1.6.1.
- Test scripts from commit `91b872a97d7095916f40445aafc193d25c991af5`.
- Evidence (RPC streams, sessions, fixture, install logs) is kept private outside the repository, as the recipe says.

## Attempts

| Attempt | Time (UTC) | Install | Setup | Plan | Build |
|---|---|---|---|---|---|
| 1 | 07:56–08:10 | pass: `Installed npm:agent-concepts@0.5.0`, `Installed npm:pi-subagents`; `pi auth check`: `ready` | not run: 20 errored turns, 0 tool calls, empty final reply | not run: 20 errored turns, 0 tool calls | not run: 40 errored turns, 0 tool calls; stopped by the operator |
| 2 (the one retry for an infrastructure failure) | 08:14–08:20 | pass, same lines | not run: 20 errored turns, 0 tool calls | not run: 20 errored turns, 0 tool calls | not run: 20 errored turns, 0 tool calls; stopped by the operator |

Every errored turn carries the same message in the RPC stream: `429 {"type":"error","error":{"type":"rate_limit_error","message":"This request would exceed your account's rate limit. Please try again later."`. The bare remote's `main` in both attempts holds only `Create tinylabels fixture`.

Between the attempts a one-line host call to the same model (`pi -p --model anthropic/claude-haiku-5-5 --thinking low "Say OK"`) answered `OK`, so the limit was not a hard outage; the sandboxed sessions, which send the full kernel and skill system prompt, were still refused. Other Haiku pressure tests were running in parallel in the same run, which may share the account's limit. The 2026-11-27 npm-pack rerun's attempt 1 hit the same refusal on Haiku ([npm-pack rerun](2026-11-27-stranger-end-to-end/npm-pack-rerun.md)).

## Audit

The sandbox check passed in both attempts (`isolation ok`). The run was stopped before the script saved system prompts, so the operator extracted them from the saved RPC streams with the script's own code: three distinct prompts per attempt. `grep -Ff <private term list>` over them exited 1: no private term.

## Grades

| Check | Result |
|---|---|
| Setup | not graded (no model turn succeeded) |
| Planning | not graded |
| Build lands on the bare remote's `main` | not graded |
| Workers ran targeted tests only | not observed (no worker started) |
| Stalls | none attributable to the skills; the only stop is the provider refusal (infrastructure) |

## Next

Rerun releasing step 11 when the provider limit allows (a quiet account on Haiku, or Terra once the Codex quota returns). Until then `latest` stays at 0.4.1, per releasing step 13's spirit: no promotion without a passing stranger test.
