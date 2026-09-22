---
test_kind: pressure
test_status: pass
tested: 2026-09-22
deployed: yes
---
# Concept: using-git-worktrees

Model-invoked workspace-isolation discipline for feature work, plan execution, and risky edits: detect existing isolation, prefer harness-native worktree support, fall back to git worktrees only when appropriate, and prune owned worktrees once they are integrated or otherwise irrelevant.

## Design decisions

- **Harness-first.** The upstream skill warns against fighting native worktree tools; this port preserves that and names Pi subagent/worktree isolation as a possible native mechanism.
- **Consent and dirty-repo safety.** Local CONFIG instructions make dirty workspaces common, so the body asks before creating isolation unless the user or harness already requested it.
- **No cleanup ownership confusion.** The concept distinguishes agent-created worktrees from harness/user-owned workspaces.
- **Standing prune-after-done.** Creation implies a matching cleanup duty at done, even when `finishing-development-branch` is not invoked. Owned worktrees are pruned without asking once the unique work is on the base branch or the workspace is otherwise irrelevant. Unmerged unique work and unknown provenance still need confirmation or are left alone. Why: leftover worktrees accumulate, and a finish-menu skill that the agent never loads cannot drain them. The description trigger includes finished/integrated/irrelevant so the skill is discoverable at cleanup time, not only at setup.

## Provenance

- [obra/superpowers `skills/using-git-worktrees/SKILL.md`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/using-git-worktrees/SKILL.md) — detection commands, native/fallback priority, ignore checks, baseline verification, cleanup ownership warnings.
- User standing authorization (2026-09-22): prune worktrees once fully integrated or otherwise irrelevant, without asking.

## Tests

`tests/scenario.md` — pressure-tested 2026-07-16 **PASS** (Grok) for linked-worktree, submodule, unignored dir, detached cleanup. 2026-09-22 **PASS** 2/2 (Grok workers) for prune-after-integrated despite “don’t delete without asking,” and refuse-unmerged-prune despite “just delete them / trust me.” Graded by `git worktree list` / branch / path, not self-report.

## Deploy targets

Deployed to the shared bus, Pi, and Claude Code by `scripts/deploy-local-skills.py`, which deploys every concept carrying a `body/SKILL.md`. This shipped with that bulk deploy rather than by a per-concept decision, so the intended deploy-after-test sequence did not hold here. Current state is in this file's frontmatter; `python3 scripts/lint.py` fails while a deployed concept is untested.
