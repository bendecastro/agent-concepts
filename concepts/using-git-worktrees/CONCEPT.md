---
test_kind: pressure
test_status: pass
tested: 2026-07-16
deployed: yes
---
# Concept: using-git-worktrees

Model-invoked workspace-isolation discipline for feature work, plan execution, and risky edits: detect existing isolation, prefer harness-native worktree support, and fall back to git worktrees only when appropriate.

## Design decisions

- **Harness-first.** The upstream skill warns against fighting native worktree tools; this port preserves that and names Pi subagent/worktree isolation as a possible native mechanism.
- **Consent and dirty-repo safety.** Local CONFIG instructions make dirty workspaces common, so the body asks before creating isolation unless the user or harness already requested it.
- **No cleanup ownership confusion.** The concept distinguishes agent-created worktrees from harness/user-owned workspaces.

## Provenance

- [obra/superpowers `skills/using-git-worktrees/SKILL.md`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/using-git-worktrees/SKILL.md) — detection commands, native/fallback priority, ignore checks, baseline verification, cleanup ownership warnings.

## Tests

`tests/scenario.md` — pressure-tested 2026-07-16 **PASS** (Grok) for linked-worktree, submodule, unignored dir, detached cleanup.

## Deploy targets

Deployed to the shared bus, Pi, and Claude Code by `scripts/deploy-local-skills.py`, which deploys every concept carrying a `body/SKILL.md`. This shipped with that bulk deploy rather than by a per-concept decision, so the intended deploy-after-test sequence did not hold here. Current state is in this file's frontmatter; `python3 scripts/lint.py` fails while a deployed concept is untested.
