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

Not deployed yet. Destructive/publishing-adjacent workflow; deploy after pressure test.
