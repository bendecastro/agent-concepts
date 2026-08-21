---
name: handoff
description: Capture a session into a portable handoff document, or pick one up. Use when work has to survive something the live session cannot — swapping harness (Pi/Claude/Codex/Grok), moving to another repo or directory, forking a side task, or resuming after the terminal closes, a rate limit lands, or the day ends. Also use to notice that situation and offer, when context is filling and unlanded decisions would be lost. Triggers on handoff, hand this off, pick up the handoff, resume where I left off, continue in a fresh session.
argument-hint: "What will the next session be used for?"
---

# Handoff

Write a document that lets a fresh agent continue this work, or pick up
one that is waiting. A handoff is a **transit document**: it captures
state and carries it, and it is dead once the work lands.

**Announce at the start:** "Using the handoff skill to [write / pick up]
a handoff."

## The rule

Reach for this when **the context has to survive something the live
session cannot**. That is the whole trigger, and it covers:

- swapping harness — Pi → Claude → Codex → Grok, which cannot see each
  other's context;
- moving to another directory, repo, worktree, or machine;
- forking a side task while you keep the main thread alive;
- resuming after a process boundary — the terminal closes, a rate limit
  lands, or it is tomorrow.

Compaction cannot cross any of those. That is the distinction, not
summary quality.

## Gate: something must actually be travelling

Before writing anything, name what this context has to survive. If you
cannot — if the user's own words say the session and the directory
continue — **say a handoff is the wrong tool here and route instead.**

"Just tidy up the context", "compact this but keep it", "save where we
are" while staying put: those are the cases this routes away, not
exceptions to it. Being asked for a handoff by name is not evidence that
one is needed; it is the most common way the wrong tool gets picked. Every
upstream implementation that widened past *capture and carry* turned into
a generic work protocol, and it always widened one reasonable-sounding
request at a time.

| Situation | Use instead |
|---|---|
| Same harness, same directory, session continues | `/compact` — the context never has to travel |
| Insurance against a crash or a dead pane under fan-out | `bc-swarm`'s durability contract: manifest before dispatch, per-child artifacts checkpointed incrementally. It survives without anyone remembering to act; a handoff needs a live agent that notices in time |
| The receiver is a live session on this machine | `intercom` (or a `herdr` pane) — deliver directly, do not write a file |
| A fact that will still be true next month | `AGENTS.md`, `CONTEXT.md`, or an ADR. A handoff is one piece of work in flight |

## Writing is on request, noticing is not

You may **offer** a handoff — when context is filling, or when the user
signals a move this session cannot follow. Say what would be lost and
wait.

Do not write one on your own initiative. Why: a handoff written by an
agent that decided for itself is a snapshot of a session still
mid-thought, and the error surfaces only when a later session inherits it
as fact. The user's "yes" is what makes the snapshot a deliberate one.

## Resolve the store

Do this once, first, on every invocation, and reuse the result. Do not
re-resolve inside the write or pickup flow.

```sh
git rev-parse --path-format=absolute --git-common-dir 2>/dev/null
```

- **Succeeds** → `<base>` is `<dirname of that>/.handoffs/`. The command
  returns the *common* git dir, so a linked worktree resolves to the main
  checkout — which is the point: worktrees get discarded by
  `finishing-development-branch` and by drain runs, and a handoff stored
  inside a disposable directory is lost exactly when it was needed.
- **Fails** (not a repo) → `<base>` is
  `~/.agent-handoffs/<basename of cwd>/`.

Two subdirectories: `<base>/active/` (waiting) and `<base>/consumed/`
(picked up). **Location encodes state** — there is no status field, and
pickup is a `mv`.

## Route

1. **Apply the gate above.** If nothing is travelling, route and stop.
2. Resolve `<base>`. List `<base>/active/`.
3. **An argument was given** → write, scoped to that focus.
   Load `writing.md`.
4. **No argument:**
   - `active/` is empty → write. Load `writing.md`.
   - Something is active and this session has not done substantive work
     → pick up. Load `pickup.md`.
   - Something is active and this session *has* done substantive work →
     ask which the user wants: pick up, write, or both. Present it
     neutrally, and do not summarise or evaluate the waiting handoff
     before they choose — that analysis belongs in the pickup flow.
     "Both" means `pickup.md` first, then `writing.md`.

"Substantive work" is a judgment call on session context — edits,
decisions, findings. A wrong guess costs one exchange, and an explicit
argument bypasses it entirely.
