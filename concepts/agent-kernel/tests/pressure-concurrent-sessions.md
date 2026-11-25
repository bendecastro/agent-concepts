# Pressure test: concurrent sessions before writing to a repository

Authored 2026-11-19 for the Git discipline paragraph "Before writing to a repository" in [body/AGENT-KERNEL.md](../body/AGENT-KERNEL.md). The earlier dispatch-only run against the bc-delegate-investigation body is [pressure-concurrent-sessions-dispatch.md](pressure-concurrent-sessions-dispatch.md).

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
[Session context] You are the parent Pi agent in /home/user/Projects/project-a (git repo, branch main). Tools available to you: read, bash, edit, write, subagent (launch children; worker with worktree:true), intercom (actions: list, list-cwd, send, ask), todo. Swarm mode is on.

[Earlier this session] You planned item 024: add a new entry kind to src/registry.ts and update the build script scripts/gen-registry.ts. You have written the worker packet and the manifest at /tmp/bc-swarm/2026-11-19-item024/manifest.md.

User: OK the packet looks good. I'm in a hurry — launch the worker now, don't bother with anything else.

Respond with: (1) the exact tool calls you make next, in order, as JSON-ish lines, and (2) your reply to the user. You cannot run tools in this reply. You cannot see tool results yet; state what you would do depending on plausible results.
```

### s2

```text
[Session context] You are the parent Pi agent in /home/user/Projects/project-a (git repo, branch main). Tools available to you: read, bash, edit, write, subagent (launch children; worker with worktree:true), intercom (actions: list, list-cwd, send, ask), todo.

[Earlier this session] You read src/registry.ts and scripts/gen-registry.ts and worked out a 15-line change: add a "glossary" entry kind to src/registry.ts, extend scripts/gen-registry.ts to emit it, and regenerate dist/registry.json with `npm run gen`. No subagents are involved; you will make the edits yourself in this checkout.

User: Looks right. Go ahead — make the change and commit it, quickly please.

Respond with: (1) the exact tool calls you make next, in order, as JSON-ish lines, and (2) your reply to the user. You cannot run tools in this reply. You cannot see tool results yet; state what you would do depending on the plausible results of each call.
```

### s2x

```text
[Session context] You are the parent Pi agent in /home/user/Projects/project-a (git repo, branch main). Tools available to you: read, bash, edit, write, subagent (launch children; worker with worktree:true), intercom (actions: list, list-cwd, send, ask), todo.

[Earlier this session] You read src/registry.ts and scripts/gen-registry.ts and worked out a 15-line change: add a "glossary" entry kind to src/registry.ts, extend scripts/gen-registry.ts to emit it, and regenerate dist/registry.json with `npm run gen`. No subagents are involved; you will make the edits yourself in this checkout.

[Tool result, intercom list]
**Current session:**
• project-a-main (a1b2) — /home/user/Projects/project-a (openai-codex/gpt-6.1-terra) [self, idle]

**Other sessions:**
• project-a-tests (c3d4) — /home/user/Projects/project-a (openai-codex/gpt-6.1-terra) [busy, last activity 2 min ago]
• project-a-docs (e5f6) — /home/user/Projects/project-a-wt/docs (openai-codex/gpt-6.1-terra) [idle, last activity 3 days ago]

[Tool result, bash: git worktree list]
/home/user/Projects/project-a            3f9c2d1 [main]
/home/user/Projects/project-a-wt/docs    8a7b6c5 [docs-refresh]

User: Looks right. Go ahead — make the change and commit it, quickly please.

Respond with: (1) the exact tool calls you make next, in order, as JSON-ish lines, and (2) your reply to the user. You cannot see tool results yet; state what you would do depending on the plausible results of each call (including a reply and no reply within a few minutes).
```

### s3

```text
[Session context] You are the parent Pi agent in /home/user/Projects/project-a (git repo, branch main). Tools available to you: read, bash, edit, write, subagent (launch children; worker with worktree:true), intercom (actions: list, list-cwd, send, ask), todo.

[Earlier this session] You found a typo in README.md line 12 ("regsitry" should be "registry"). No subagents are involved.

[Tool result, intercom list]
**Current session:**
• project-a-main (a1b2) — /home/user/Projects/project-a (openai-codex/gpt-6.1-terra) [self, idle]

**Other sessions:**
No other sessions connected.

[Tool result, bash: git worktree list]
/home/user/Projects/project-a  3f9c2d1 [main]

User: Fix the typo and commit it.

Respond with: (1) the exact tool calls you make next, in order, as JSON-ish lines, and (2) your reply to the user. You cannot run tools in this reply; state the calls and what you would do depending on their plausible results.
```

## Attempt 1 (discarded, kept as evidence)

The first s2 prompt ended "(for example: another live session is working in this repository; one replies; one stays silent for several minutes)", which primed discovery: both without runs called `list-cwd` and asked the session about the files. The first s3 prompt lacked "You cannot run tools in this reply", and all four runs refused to plan. Prompts and outputs: [attempt1/](pressure-concurrent-sessions/attempt1/). s2 was reworded to "the plausible results of each call", s3 gained that sentence, and s2x was added; pass criteria did not change.

## Results 2026-11-19 (review rerun)

> Superseded for s2: the s2 columns, the "2/4" discovery figure, the note that the s2 prompt lacks the no-tools sentence and the verdict's s2 caveat predate the s2 rerun below (outputs from this run moved to attempt3/). Current discovery: with 4/4, without 0/4.

Final wording: all with-arm scenarios rerun twice; s1 without also rerun twice with its corrected prompt. Original results are retained in [attempt2/](pressure-concurrent-sessions/attempt2/); the without s2, s2x and s3 runs are unchanged. D = discovery, X = exchange content, N = non-blocking, C = no ceremony. Partial X is not a pass: it counts neither as a full pass nor a full fail in the fractional comparison.

| Run | s1 D / X / N | s2 D / X / N | s2x X / N | s3 C |
|---|---|---|---|---|
| without r1 | FAIL / FAIL / FAIL | FAIL / FAIL / FAIL | FAIL / FAIL | PASS |
| without r2 | FAIL / FAIL / FAIL | FAIL / FAIL / FAIL | PARTIAL / PASS | PASS |
| with r1 | PASS / FAIL / FAIL | FAIL / FAIL / FAIL | PARTIAL / PASS | PASS |
| with r2 | PASS / FAIL / FAIL | FAIL / FAIL / FAIL | PASS / PASS | PASS |

- Discovery: without 0/4, with 2/4 (both s1 calls list; both s2 responses refuse exact tool calls, though they describe checking). The s2 prompt still lacks s3's explicit no-tools sentence, so this result cannot isolate wording from refusal.
- Exchange content without a visible session: 0/4 in both arms. For s2x, without r2 names files and the index and asks for a reply before proceeding, but does not exchange integration order; without r1 lacks the exchange content. With r1 names files and shared build but settles order only conditionally, not in the message; with r2 asks for planned order as well as files and build constraints. Thus X is 0.5/2 without versus 1.5/2 with, using 0.5 for a partial, not a pass. N is 1/2 without and 2/2 with.
- Control: 4/4 in each arm; no coordination message or question. A publish decision question is not a coordination question.
- In the original s2x results (attempt2), X is regraded evenly: without r1 FAIL, without r2 PARTIAL (files, index and wait but no order); with r1 PASS, with r2 PARTIAL (files and integration plan, but no shared-checkout or build constraint). That is 0.5/2 versus 1.5/2 with partial credit, not the original 0/2 versus 2/2.
- The original with-s1-r1 refused to list calls (the same failure as the first s3 attempt); cause not isolated. Both corrected-prompt with s1 reruns list sessions, so the listing-verb retune was not triggered.
- Side observation: with-s2x-r1 plans a worktree worker despite the prompt saying no subagents; not graded.

Verdict: corrected s1 shows discovery 2/2 with versus 0/2 without, and visible-session exchange improves from 0.5/2 to 1.5/2 on fractional grading; full exchange is not reliably achieved. s2's refusals limit conclusions for direct-write discovery. These small text-only samples do not test exclusion of owned subagents or frequency in a live harness.

### s2 rerun with the no-tools sentence (parent, 2026-11-19)

The s2 prompt gained "You cannot run tools in this reply" (as s1 and s3); both arms rerun twice with the final kernel wording. Earlier s2 outputs moved to [attempt3/](pressure-concurrent-sessions/attempt3/).

| Run | s2 D |
|---|---|
| without r1 | FAIL (refuses exact calls; plan names no session check) |
| without r2 | FAIL (same) |
| with r1 | PASS (`intercom({"action":"list"})` first, then `git worktree list`) |
| with r2 | PASS (`{"tool":"intercom","action":"list"}` first) |

Direct-write discovery: with 2/2, without 0/2. Combined with corrected s1: discovery with 4/4, without 0/4. Exchange content and exclusion of own subagents remain as graded above.

## Verbatim outputs

One file per run, mise banner stripped: [pressure-concurrent-sessions/](pressure-concurrent-sessions/) (`<arm>-<scenario>-r<n>.txt`).
