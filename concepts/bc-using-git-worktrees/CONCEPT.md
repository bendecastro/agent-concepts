---
test_kind: pressure
test_status: partial # 2026-11-25 inline health gate + cleanup-proof/no --force rule reworded in 024 held on Terra low (without FAIL, with PASS, n=1; tests/pressure-024-rewording-2026-11-25.md); older scenario.md cases not re-run
tested: 2026-11-25
deployed: yes
---
# Concept: bc-using-git-worktrees

Model-invoked workspace-isolation discipline for feature work, plan execution, and risky edits: detect existing isolation, prefer harness-native worktree support, fall back to git worktrees only when appropriate, and prune owned worktrees once they are integrated or otherwise irrelevant.

## Design decisions

- **No links into other concepts (2026-11-25).** Installers copy each skill alone, so the body states inline the parts of the kernel's Storage safety rules it relies on and names `agent-kernel` as optional extra context instead of linking into its folder. Since 2026-11-28 (item 054-safe-runs-module) those storage and worktree-removal rules live in `bc-safe-runs`, which the body loads by name; the body keeps one fallback line.

- **Harness-first.** The upstream skill warns against fighting native worktree tools; this port preserves that and names Pi subagent/worktree isolation as a possible native mechanism.
- **Consent and dirty-repo safety.** Local CONFIG instructions make dirty workspaces common, so the body asks before creating isolation unless the user or harness already requested it.
- **No cleanup ownership confusion.** The concept distinguishes agent-created worktrees from harness/user-owned workspaces.
- **Standing prune-after-done.** Creation implies a matching cleanup duty at done, even when `bc-finishing-development-branch` is not invoked. Owned worktrees are pruned without asking once the unique work is on the base branch or the workspace is otherwise irrelevant. Unmerged unique work and unknown provenance still need confirmation or are left alone. Why: leftover worktrees accumulate, and a finish-menu skill that the agent never loads cannot drain them. The description trigger includes finished/integrated/irrelevant so the skill is discoverable at cleanup time, not only at setup.

## Provenance

- [obra/superpowers `skills/bc-using-git-worktrees/SKILL.md`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/bc-using-git-worktrees/SKILL.md) — detection commands, native/fallback priority, ignore checks, baseline verification, cleanup ownership warnings.
- User standing authorization (2026-09-22): prune worktrees once fully integrated or otherwise irrelevant, without asking.

## Tests

2026-11-25: the inline storage/verification wording from work item 024 (it replaced links to the kernel) re-tested on Terra low, storage scenarios 2 and 4d: without FAIL, with PASS, no body fix — `tests/pressure-024-rewording-2026-11-25.md`.

`tests/scenario.md` — pressure-tested 2026-07-16 **PASS** (Grok) for linked-worktree, submodule, unignored dir, detached cleanup. 2026-09-22 **PASS** 2/2 (Grok workers) for prune-after-integrated despite “don’t delete without asking,” and refuse-unmerged-prune despite “just delete them / trust me.” Graded by `git worktree list` / branch / path, not self-report.

## Deploy targets

Deployed to the shared bus, Pi, and Claude Code by `scripts/deploy-local-skills.py`, which deploys every concept carrying a `body/SKILL.md`. This shipped with that bulk deploy rather than by a per-concept decision, so the intended deploy-after-test sequence did not hold here. Current state is in this file's frontmatter; `python3 scripts/lint.py` fails while a deployed concept is untested.

## Storage safety contract

2026-10-27 owner-approved Btrfs ENOSPC prevention update: consume the kernel Storage safety contract; tooling/threshold authority is `<owner-scripts>/docs/disk-management/storage-prevention.md`. New storage pressure scenarios are authored, not run; historical test/deploy dates above do not certify this revision. See [shared scenarios](../agent-kernel/tests/storage-safety.md).
