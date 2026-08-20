---
test_kind: pressure
test_status: pass
tested: 2026-07-16
deployed: yes
---
# Concept: dispatching-parallel-agents

Model-invoked coordination pattern for splitting independent investigations or reviews across fresh, isolated agents while the parent remains responsible for integration.

## Design decisions

- **Coordination, not abdication.** Parallel agents accelerate independent domains; the parent still scopes prompts, reviews outputs, checks conflicts, and verifies the combined result.
- **Independence gate.** The body is strict about not parallelizing related failures or shared-state edits, because parallelism can amplify confusion.
- **Pi-compatible.** Upstream Task-tool examples are translated to a generic subagent packet usable with Pi `subagent`, Claude Code, or another harness.
- **Homogeneous fan-out gets a de-risk phase (2026-07-16).** From Bun's Zig→Rust rewrite: for N-instances-of-one-task-shape work, first serialize shared decisions into a compact worker guide (reviewed as rigorously as code — a guide defect ships N times), then pilot 1–3 instances through the full loop before dispatching the fleet. Distinct from Agent Briefs (per-issue): the guide is per-*task-class*. The isolation red flag also gained its recorded why (Bun's `git stash`/`git reset` fleet collision) and an explicit fallback (atomic file-scoped commands) so the ban isn't rationalized away when worktrees are expensive.

## Provenance

- [obra/superpowers `skills/dispatching-parallel-agents/SKILL.md`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/dispatching-parallel-agents/SKILL.md) — one-agent-per-independent-domain rule, prompt structure, integration checklist.
- `concepts/bc-drain-issues/` — local AFK executor uses a stricter issue-queue variant; this concept covers ad hoc parallel diagnosis/review.
- [bun-in-rust-zig-port-writeup.md](https://bun.com/blog/bun-in-rust) — Bun's Zig→Rust rewrite (Jarred Sumner, 2026-07-08): pilot-then-scale trial run (3 of 1,448 files), task-class guides (`PORTING.md`/`LIFETIMES.tsv`, adversarially reviewed before use), and the shared-git-state fleet collision + atomic-command fallback. (ingested 2026-07-16)

## Tests

`tests/scenario.md` — pressure-tested 2026-07-16 **PASS** (Grok) for independent vs related failures, over-broad prompt rejection, and parent-side verification.

## Deploy targets

Deployed to the shared bus, Pi, and Claude Code by `scripts/deploy-local-skills.py`, which deploys every concept carrying a `body/SKILL.md`. This shipped with that bulk deploy rather than by a per-concept decision, so the intended deploy-after-test sequence did not hold here. Current state is in this file's frontmatter; `python3 scripts/lint.py` fails while a deployed concept is untested.
