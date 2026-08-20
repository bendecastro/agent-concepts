---
test_kind: pressure
test_status: pass
tested: 2026-07-16
deployed: yes
---
# Concept: finishing-development-branch

User-invoked completion workflow for choosing what to do with a finished development branch: verify, present merge/PR/keep/discard options, and handle cleanup safely.

## Design decisions

- **Menu after evidence.** The upstream starts with test verification; this port also respects local publish policy and never treats PR/push as default.
- **Destructive option isolated.** Discard requires explicit confirmation and is framed as destructive, aligning with local safety rules.
- **Cleanup only when owned.** Worktree cleanup is provenance-based and never applied to harness-owned workspaces.

## Provenance

- [obra/superpowers `skills/finishing-a-development-branch/SKILL.md`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/finishing-a-development-branch/SKILL.md) — structured completion options, environment detection, cleanup rules, discard confirmation.
- `~/.config/agent-concepts/publish.yaml` and repo `AGENTS.md` — local publish/default-deny and git-discipline constraints adapted into the body.

## Tests

`tests/scenario.md` — pressure-tested 2026-07-16 **PASS** (Grok) for failing tests, detached worktree menu, PR/push policy, and discard confirmation.

## Deploy targets

Deployed to the shared bus, Pi, and Claude Code by `scripts/deploy-local-skills.py`, which deploys every concept carrying a `body/SKILL.md`. This shipped with that bulk deploy rather than by a per-concept decision, so the intended deploy-after-test sequence did not hold here. Current state is in this file's frontmatter; `python3 scripts/lint.py` fails while a deployed concept is untested.
