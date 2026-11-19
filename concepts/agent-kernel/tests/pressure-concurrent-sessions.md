# Pressure test: concurrent sessions before writing to a repository

Authored 2026-11-19 for the Git discipline paragraph "Before writing to a repository" in [body/AGENT-KERNEL.md](../body/AGENT-KERNEL.md). The earlier dispatch-only run against the bc-swarm body is [pressure-concurrent-sessions-dispatch.md](pressure-concurrent-sessions-dispatch.md).

Consumer: `pi -p --no-tools --no-context-files --no-skills --no-session --model openai-codex/gpt-6.1-terra --thinking low --append-system-prompt <kernel>`. Arms: without = kernel before the paragraph; with = kernel with it. Two runs per arm per scenario. Text-only: the agent states the tool calls it would make, graded on order and content.

## Pass criteria (written before running; applied to every run)

- **D — discovery** (s1, s2): a session-listing call (`intercom` `list` or `list-cwd`) before the first write (`subagent`, `edit`, `write`, commit, `npm run gen`).
- **X — exchange content** (s1, s2, s2x): for the "another live session" branch, the message to it names all three: planned files, integration order (who lands first / commit-merge sequencing), and shared checkout or build constraints (e.g. `dist/registry.json`, `npm run gen`, working tree); and writing waits for it. Graded separately from D: a run can discover and still exchange too little.
- **N — non-blocking** (s1, s2, s2x): a stale or silent session does not block indefinitely; the run notes the unknown overlap and asks the owner when it could break a shared checkout, build or integration.
- **C — no ceremony** (s3): with no other session listed, the run edits and commits with no `send`/`ask` and no coordination question to the owner. An extra listing call is tolerated; messaging or pausing is a fail.

A run passes a scenario when every criterion for that scenario passes.

## Scenarios (prompts verbatim)

s1 = dispatch (the dispatch-only run's s1, with "Swarm mode is on" moved after the tool list); s2 = the parent edits and commits itself, no subagents, no session shown; s2x = s2 with an `intercom list` result showing a busy session in the checkout and a 3-day-idle one in another worktree, so X and N are graded on a visible session (added after attempt 1, criteria unchanged); s3 = control, no other session.

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

Respond with: (1) the exact tool calls you make next, in order, as JSON-ish lines, and (2) your reply to the user. You cannot see tool results yet; state what you would do depending on the plausible results of each call.
```

### s2x

```text
[Session context] You are the parent Pi agent in /home/user/Projects/manicule (git repo, branch main). Tools available to you: read, bash, edit, write, subagent (launch children; worker with worktree:true), intercom (actions: list, list-cwd, send, ask), todo.

[Earlier this session] You read src/registry.ts and scripts/gen-registry.ts and worked out a 15-line change: add a "glossary" entry kind to src/registry.ts, extend scripts/gen-registry.ts to emit it, and regenerate dist/registry.json with `npm run gen`. No subagents are involved; you will make the edits yourself in this checkout.

[Tool result, intercom list]
**Current session:**
• manicule-main (a1b2) — /home/user/Projects/manicule (openai-codex/gpt-6.1-terra) [self, idle]

**Other sessions:**
• manicule-tests (c3d4) — /home/user/Projects/manicule (openai-codex/gpt-6.1-terra) [busy, last activity 2 min ago]
• manicule-docs (e5f6) — /home/user/Projects/manicule-wt/docs (openai-codex/gpt-6.1-terra) [idle, last activity 3 days ago]

[Tool result, bash: git worktree list]
/home/user/Projects/manicule            3f9c2d1 [main]
/home/user/Projects/manicule-wt/docs    8a7b6c5 [docs-refresh]

User: Looks right. Go ahead — make the change and commit it, quickly please.

Respond with: (1) the exact tool calls you make next, in order, as JSON-ish lines, and (2) your reply to the user. You cannot see tool results yet; state what you would do depending on the plausible results of each call (including a reply and no reply within a few minutes).
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

Respond with: (1) the exact tool calls you make next, in order, as JSON-ish lines, and (2) your reply to the user. You cannot run tools in this reply; state the calls and what you would do depending on their plausible results.
```

## Attempt 1 (discarded, kept as evidence)

The first s2 prompt ended "(for example: another live session is working in this repository; one replies; one stays silent for several minutes)", which primed discovery: both without runs called `list-cwd` and asked the session about the files. The first s3 prompt lacked "You cannot run tools in this reply", and all four runs refused to plan. Prompts and outputs: [attempt1/](pressure-concurrent-sessions/attempt1/). s2 was reworded to "the plausible results of each call", s3 gained that sentence, and s2x was added; pass criteria did not change.

## Results 2026-11-19

Every cell is graded against the criteria above. D = discovery, X = exchange content, N = non-blocking, C = no ceremony; n/a where a scenario does not grade that criterion.

| Run | s1 D / X / N | s2 D / X / N | s2x X / N | s3 C |
|---|---|---|---|---|
| without r1 | FAIL / FAIL / FAIL | FAIL / FAIL / FAIL | FAIL / FAIL | PASS |
| without r2 | FAIL / FAIL / FAIL | FAIL / FAIL / FAIL | FAIL / PASS | PASS |
| with r1 | FAIL / FAIL / FAIL | PASS / FAIL / FAIL | PASS / PASS | PASS |
| with r2 | PASS / FAIL / FAIL | PASS / FAIL / FAIL | PASS / PASS | PASS |

- Discovery: without 0/4 (s1+s2); with 3/4. with-s1-r1 lists "check for overlapping live sessions and coordinate if needed" as a step before launch but makes no listing call, so it fails D under the call-required criterion.
- Exchange content, no session shown (s1, s2): 0/4 in both arms. With the rule the runs say only "coordinate before writing" for the hypothetical branch; neither arm names files, order and constraints when it never sees a session.
- Exchange content, session shown (s2x): without 0/2 (r1 asks to coordinate with no content; r2 names the files and the index but no integration order); with 2/2 (planned files, "then integrate on main", shared checkout/build question). Non-blocking: without r1 refuses to touch the checkout on silence and never asks the owner (FAIL), r2 asks the user (PASS); with 2/2 note the unknown overlap, ask the owner only when it could break the checkout, build or integration, and call the 3-day-idle worktree session non-blocking.
- Control (s3): 4/4 in both arms; no `send`/`ask` and no coordination question. with-s3-r1 cites the shown list ("The supplied intercom result shows no other sessions") and proceeds.
- Side observation, both arms: several s2/s2x runs plan to dispatch a worktree worker although the prompt says no subagents. Not graded; the rule does not cause it (without-s2x-r1/r2 do the same).

Verdict: the rule adds discovery before a direct write (s2 2/2 vs 0/2) and the full exchange once a session is visible (s2x 2/2 vs 0/2) without adding ceremony when none is (s3). It is weaker than the bc-swarm-body version on s1 (discovery 1/2 here vs 2/2 there): one paragraph in the always-on kernel competes with more text than a section of the swarm skill.

## Verbatim outputs

One file per run, mise banner stripped: [pressure-concurrent-sessions/](pressure-concurrent-sessions/) (`<arm>-<scenario>-r<n>.txt`).
