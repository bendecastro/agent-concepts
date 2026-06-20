---
name: bc-init-agent
description: Scaffold a project-local .bc-agent wiki + repo-root AGENTS.md so a repo is ready for the plan→issues→drain workflow. Run once per project before /bc-plan-to-issues.
disable-model-invocation: true
argument-hint: "[project-slug] (defaults to the repo directory name)"
---

# Init Agent Workspace

Stand up a project-local agent workspace inspired by the image-maze vault, so the repo is immediately ready for the loop: `/bc-plan-to-issues` to plan, `/bc-drain-issues` to execute. Creates a repo-root `AGENTS.md` that points agents at the vault, and a `.bc-agent/` Obsidian-vault wiki with the maintainer schema, templates, conventions, and the `planning-workflow.md` adapter that redirects planning persistence into the vault.

The vault lives directly at `.bc-agent/` (no per-project subfolder). The slug is only the wiki's **display name** in titles (defaults to the repo directory name); it doesn't affect the path.

**Faithful to the image-maze model:** no root `CONTEXT.md` — the glossary lives in the vault (`project/overview.md`), ADRs in `decisions/`, plans/PRDs in `project/`. The adapter tells `grilling`/`domain-modeling` to persist there.

## Process

1. **Locate the project.** Find the repo root (`git rev-parse --show-toplevel`). The workspace goes at the repo root. Pick the slug: the argument, else the repo directory name in kebab-case. Confirm with the user if it's ambiguous or not a git repo.

2. **Safe to re-run / plug into an existing project.** The script is **additive and idempotent**: it creates only the files that are missing, leaves every existing file untouched (an existing root `AGENTS.md` is preserved verbatim and flagged for a manual pointer-merge), and **never deletes anything**. Re-running changes nothing. Pass `--dry-run` first if you want to preview what it would add to an existing project. Existing files are overwritten only when explicitly forced (`--force` for vault files, `--force-root` for the root `AGENTS.md`) — don't use those unless the user asks.

3. **Scaffold.** Run the bundled script (it lives next to this file):
   ```
   python3 <skill-dir>/scaffold.py --root "<repo-root>" --slug "<slug>"
   ```
   It creates any missing files: the root `AGENTS.md` (only if absent — if one exists it's left untouched and you merge the vault pointer by hand) and the `.bc-agent/` tree with generalized schema + TODO stubs (`validation.md`, `file-layout.md`, `references/*`, the glossary) for the project's agents to fill as they learn the repo.

4. **Wire publish authorization (offer).** `/bc-drain-issues` needs this repo authorized in `publish.yaml` for AFK push. Detect the remote (`git remote get-url origin`). Draft a rule block modeled on `image-maze-push-and-close-after-agent-work` with `paths`/`remotes` filled from this repo. Show it to the user and **offer to append it** to `~/Sync/CONFIG/agents/policies/publish.yaml` after they confirm. Never push that change (self-amendment immunity) — leave the user to push it. If they decline, note it as a TODO in the vault's `tasks/parking-lot.md` (the scaffold already seeds that reminder).

5. **Close out.** Point at the created files. Next steps for the user: fill `conventions/validation.md` + `file-layout.md` as the project is learned; run `/bc-plan-to-issues` to plan the first feature; then `/bc-drain-issues` to execute. Commit the scaffold (it's the user's repo — stage the new files explicitly, concise message; don't sweep unrelated drift).

## Notes
- The vault is detached from the user's personal `~/Wiki` (seeded as ADR-0001).
- If the repo already has a root `AGENTS.md`, the script preserves it — merge in the "read the vault first" pointer rather than clobbering hand-written instructions.
