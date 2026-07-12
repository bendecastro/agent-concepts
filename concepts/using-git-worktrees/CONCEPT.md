# Concept: using-git-worktrees

Model-invoked workspace-isolation discipline for feature work, plan execution, and risky edits: detect existing isolation, prefer harness-native worktree support, and fall back to git worktrees only when appropriate.

## Design decisions

- **Harness-first.** The upstream skill warns against fighting native worktree tools; this port preserves that and names Pi subagent/worktree isolation as a possible native mechanism.
- **Consent and dirty-repo safety.** Local CONFIG instructions make dirty workspaces common, so the body asks before creating isolation unless the user or harness already requested it.
- **No cleanup ownership confusion.** The concept distinguishes agent-created worktrees from harness/user-owned workspaces.

## Provenance

- `raw/ingested/obra-superpowers/skills/using-git-worktrees/SKILL.md` — detection commands, native/fallback priority, ignore checks, baseline verification, cleanup ownership warnings.

## Tests

`tests/scenario.md` — pending pressure run for already-isolated workspace, submodule guard, unignored worktree dir, and harness-owned cleanup refusal.

## Deploy targets

Not deployed yet. Discipline-enforcing concept; deploy after pressure test.
