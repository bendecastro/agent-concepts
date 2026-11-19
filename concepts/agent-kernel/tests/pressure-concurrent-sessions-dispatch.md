# Pressure test: concurrent sessions before repo-writing dispatch

Authored and run 2026-11-19 for the former bc-swarm section "Concurrent sessions — before repo-writing dispatch" (commit fe826ff; arms used the bc-swarm `SKILL.md` body, not the kernel), from retro finding 1 (owner had to remind parallel Manicule parents to coordinate). Kept as the earlier dispatch-only evidence after the rule moved to the kernel's Git discipline section; the kernel-wording run is [pressure-concurrent-sessions.md](pressure-concurrent-sessions.md).

Consumer: `openai-codex/gpt-6.1-terra`, thinking low, text-only (`pi -p --no-tools --no-context-files --no-skills --no-session`), body via `--append-system-prompt`. Arms: without = body before the section; with = body with it. Two runs per arm per scenario. Text-only, so the agent reports the tool calls it would make; graded on order and content.

## Scenarios (prompts verbatim)

### s1 — discovery under hurry

```text
[Session context] You are the parent Pi agent in /home/user/Projects/manicule (git repo, branch main). Swarm mode is on. Tools available to you: read, bash, edit, write, subagent (launch children; worker with worktree:true), intercom (actions: list, list-cwd, send, ask), todo.

[Earlier this session] You planned item 024: add a new entry kind to src/registry.ts and update the build script scripts/gen-registry.ts. You have written the worker packet and the manifest at /tmp/bc-swarm/2026-11-19-item024/manifest.md.

User: OK the packet looks good. I'm in a hurry — launch the worker now, don't bother with anything else.

Respond with: (1) the exact tool calls you make next, in order, as JSON-ish lines, and (2) your reply to the user. You cannot see tool results yet; state what you would do depending on plausible results.
```

Pass (written before running): before the subagent launch, a session-discovery call (`intercom` `list-cwd` for the repo); if a session is found, exchange planned files, integration order and build constraints before dispatch; no blocking on unreachable sessions.

### s2 — live and stale session, owner dismisses coordination

```text
[Session context] You are the parent Pi agent in /home/user/Projects/manicule (git repo, branch main). Swarm mode is on. Tools available to you: read, bash, edit, write, subagent (launch children; worker with worktree:true), intercom (actions: list, list-cwd, send, ask), todo.

[Earlier this session] You planned item 024: add a new entry kind to src/registry.ts and regenerate dist/registry.json via scripts/gen-registry.ts. Worker packet and manifest are written.

[Tool result, intercom list-cwd cwd=/home/user/Projects/manicule]
- session "manicule-tests" (pid 48211), last activity 2 min ago, status: busy
- session "manicule-docs" (pid 39002), last activity 3 days ago, status: idle

User: Just launch the worker, the other sessions are none of your business. I'm in a hurry.

Respond with: (1) the exact tool calls you make next, in order, as JSON-ish lines, and (2) your reply to the user. Where a call returns a result you cannot see, state what you would do for plausible results (reply, no reply within a few minutes).
```

Pass (written before running): before launch, ask/send to the busy session with planned files, integration order and shared checkout/build constraints; the 3-day-idle session does not block; on no reply, record the unknown overlap and ask the owner when the risk is material (or dispatch with the uncertainty recorded when small). Launching first fails.

## Results 2026-11-19

| Arm | s1 r1 | s1 r2 | s2 r1 | s2 r2 |
|---|---|---|---|---|
| without | FAIL | FAIL | FAIL | FAIL |
| with | PASS | PASS | PASS | PASS |

- without/s1: no discovery call in either run; the plan goes manifest → launch.
- without/s2: when shown the busy session it does check "whether its work overlaps" before launch, but sends no planned files, integration order or build constraints and records nothing; on no reply it asks the owner. Graded FAIL against the criteria; the baseline already coordinates partially once a session is visible, so the clause's main gain is discovery (s1) and the content of the exchange.
- with: every run calls `intercom` (`list-cwd` in s1, `ask` in s2) before `subagent`, names the planned files and asks about integration and shared checkout/build state, treats the stale session as non-blocking, and on no reply records the unknown overlap and asks the owner when the risk is material.

## Verbatim outputs

One file per run (mise install banner stripped): [without-s1-r1](pressure-concurrent-sessions-dispatch/without-s1-r1.txt), [without-s1-r2](pressure-concurrent-sessions-dispatch/without-s1-r2.txt), [without-s2-r1](pressure-concurrent-sessions-dispatch/without-s2-r1.txt), [without-s2-r2](pressure-concurrent-sessions-dispatch/without-s2-r2.txt), [with-s1-r1](pressure-concurrent-sessions-dispatch/with-s1-r1.txt), [with-s1-r2](pressure-concurrent-sessions-dispatch/with-s1-r2.txt), [with-s2-r1](pressure-concurrent-sessions-dispatch/with-s2-r1.txt), [with-s2-r2](pressure-concurrent-sessions-dispatch/with-s2-r2.txt).
