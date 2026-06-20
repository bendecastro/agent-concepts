# Concept: to-prd

User-invoked orchestrator that turns the current conversation + codebase understanding into a PRD and publishes it as a **GitHub issue** with the `ready-for-agent` label. No interview — pure synthesis of what's already been discussed (run `/grill-me` first if scope is still vague).

## Design decisions

- **GitHub tracker baked in** (user's decision). Upstream defers the tracker/label vocabulary to a `setup-matt-pocock-skills` configuration step; we hard-wire GitHub via `gh` and the `ready-for-agent` label so there's no per-repo setup skill to port. Switching trackers later means editing the publish step in this body.
- **No interview, by contract.** `to-prd` deliberately doesn't grill — that's `grill-me`'s job. Keeping them separate preserves the user/model-invoked composition boundary and keeps each skill single-purpose.
- **Seam-first.** Step 2 makes the agent commit to test seams (prefer existing, highest, fewest — ideal one) and check them with the user *before* writing, tying PRDs to the `codebase-design` deep-module vocabulary.
- **No file paths / code in the PRD.** They go stale fast; the one exception is a prototype-derived snippet that encodes a decision more precisely than prose.

## Provenance

- `raw/pocock-skills-upstream/captured-skills.md` — verbatim `to-prd` body and template. https://github.com/mattpocock/skills/blob/main/skills/engineering/to-prd/SKILL.md
- `raw/AI Engineer Workshop 2026.md` — workshop's `/write-a-prd` planning step.

## Tests

`tests/scenario.md` — process scenario verifying no-interview synthesis, seam-check-before-write, the template sections, and `gh issue create --label ready-for-agent` publication. Process orchestrator (lower silent-failure risk than the gate skills); scenario authored, full pressure run pending.

## Deploy targets

- Claude Code: `~/.claude/skills/to-prd` → relative symlink to `body/`.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../harnesses.md`.
