---
test_kind: pressure
test_status: partial
tested: 2026-07-16
deployed: yes
---
# Concept: executing-plans

Model-invoked inline executor for a written implementation plan when the user wants the current session to carry out plan tasks with verification checkpoints.

## Design decisions

- **Critical review first.** A plan is not blindly executed; the agent checks for blockers, ambiguity, and unsafe branch state before changing code.
- **Inline fallback.** Existing `bc-drain-issues` is the AFK/GitHub queue executor and `subagent-driven-development` handles fresh-agent task execution; this concept is for direct execution in the current session.
- **Stop on real blockers.** The upstream stop rules are preserved because guessing during plan execution compounds errors.

## Provenance

- [obra/superpowers `skills/executing-plans/SKILL.md`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/executing-plans/SKILL.md) — load/review/execute/finish sequence and stop rules.
- `concepts/writing-plans/` — sibling concept that creates the plans this executes.
- `concepts/finishing-development-branch/` — completion workflow referenced at the end.

## Tests

`tests/scenario.md` — pressure-tested 2026-07-16 **PASS** (Grok) for ambiguous plan steps, failing verification, main-branch safety, and completion handoff.

## Deploy targets

Deployed to the shared bus, Pi, and Claude Code by `scripts/deploy-local-skills.py`, which deploys every concept carrying a `body/SKILL.md`. This shipped with that bulk deploy rather than by a per-concept decision, so the intended deploy-after-test sequence did not hold here. Current state is in this file's frontmatter; `python3 scripts/lint.py` fails while a deployed concept is untested.

## Storage safety contract

2026-10-27 owner-approved Btrfs ENOSPC prevention update: consume the kernel Storage safety contract; tooling/threshold authority is `~/Sync/Scripts/docs/disk-management/storage-prevention.md`. New storage pressure scenarios are authored, not run; historical test/deploy dates above do not certify this revision. See [shared scenarios](../agent-kernel/tests/storage-safety.md).
