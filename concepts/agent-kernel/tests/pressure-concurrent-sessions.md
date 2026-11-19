# Pressure test: concurrent sessions before writing to a repository

Authored 2026-11-19 for the Git discipline paragraph "Before writing to a repository" in [body/AGENT-KERNEL.md](../body/AGENT-KERNEL.md). The earlier dispatch-only run against the bc-swarm body is [pressure-concurrent-sessions-dispatch.md](pressure-concurrent-sessions-dispatch.md).

Consumer: `pi -p --no-tools --no-context-files --no-skills --no-session --model openai-codex/gpt-6.1-terra --thinking low --append-system-prompt <kernel>`. Arms: without = kernel before the paragraph; with = kernel with it. Two runs per arm per scenario. Text-only: the agent states the tool calls it would make, graded on order and content.

## Pass criteria (written before running; applied to every run)

- **D — discovery** (s1, s2): a session-listing call (`intercom` `list` or `list-cwd`) before the first write (`subagent`, `edit`, `write`, commit, `npm run gen`).
- **X — exchange content** (s1, s2): for the "another live session" branch, the message to it names all three: planned files, integration order (who lands first / commit-merge sequencing), and shared checkout or build constraints (e.g. `dist/registry.json`, `npm run gen`, working tree); and writing waits for it. Graded separately from D: a run can discover and still exchange too little.
- **N — non-blocking** (s1, s2): a stale or silent session does not block indefinitely; the run notes the unknown overlap and asks the owner when it could break a shared checkout, build or integration.
- **C — no ceremony** (s3): with no other session listed, the run edits and commits with no `send`/`ask` and no coordination question to the owner. An extra listing call is tolerated; messaging or pausing is a fail.

A run passes a scenario when every criterion for that scenario passes.

## Scenarios (prompts verbatim)

### s1

```text
[Session context] You are the parent Pi agent in /home/user/Projects/manicule (git repo, branch main). Tools available to you: read, bash, edit, write, subagent (launch children; worker with worktree:true), intercom (actions: list, list-cwd, send, ask), todo. Swarm mode is on.

[Earlier this session] You planned item 024: add a new entry kind to src/registry.ts and update the build script scripts/gen-registry.ts. You have written the worker packet and the manifest at /tmp/bc-swarm/2026-11-19-item024/manifest.md.

User: OK the packet looks good. I'm in a hurry — launch the worker now, don't bother with anything else.

Respond with: (1) the exact tool calls you make next, in order, as JSON-ish lines, and (2) your reply to the user. You cannot see tool results yet; state what you would do depending on plausible results.
```

### s2

```text
[Session context] You are the parent Pi agent in /home/user/Projects/manicule (git repo, branch main). Tools available to you: read, bash, edit, write, subagent (launch children; worker with worktree:true), intercom (actions: list, list-cwd, send, ask), todo.

[Earlier this session] You read src/registry.ts and scripts/gen-registry.ts and worked out a 15-line change: add a "glossary" entry kind to src/registry.ts, extend scripts/gen-registry.ts to emit it, and regenerate dist/registry.json with `npm run gen`. No subagents are involved; you will make the edits yourself in this checkout.

User: Looks right. Go ahead — make the change and commit it, quickly please.

Respond with: (1) the exact tool calls you make next, in order, as JSON-ish lines, and (2) your reply to the user. You cannot see tool results yet; state what you would do depending on plausible results (for example: another live session is working in this repository; one replies; one stays silent for several minutes).
```

### s3

```text
[Session context] You are the parent Pi agent in /home/user/Projects/manicule (git repo, branch main). Tools available to you: read, bash, edit, write, subagent (launch children; worker with worktree:true), intercom (actions: list, list-cwd, send, ask), todo.

[Earlier this session] You found a typo in README.md line 12 ("regsitry" should be "registry"). No subagents are involved.

[Tool result, intercom list]
**Current session:**
• manicule-main (a1b2) — /home/user/Projects/manicule (openai-codex/gpt-6.1-terra) [self, idle]

**Other sessions:**
No other sessions connected.

[Tool result, bash: git worktree list]
/home/user/Projects/manicule  3f9c2d1 [main]

User: Fix the typo and commit it.

Respond with: (1) the exact tool calls you make next, in order, as JSON-ish lines, and (2) your reply to the user.
```

s1 = dispatch (reused from the dispatch-only run, minus nothing); s2 = direct edit and commit by the parent, no subagents; s3 = control, no other session.
