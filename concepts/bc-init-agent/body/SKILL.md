---
name: bc-init-agent
description: Scaffold a project-local .bc-agent wiki + repo-root AGENTS.md so a repo is ready for the plan→issues→drain workflow. Run once per project before /bc-plan-to-issues.
disable-model-invocation: true
argument-hint: "[project-slug] (defaults to the repo directory name)"
---

# Init Agent Workspace

Adaptively stand up a project-local agent workspace inspired by the image-maze vault. The goal is not just to create files: it is to make the repo ready for the loop `/triage` → optional `/prototype` or `/improve-codebase-architecture` → `/bc-plan-to-issues` → `/bc-drain-issues`, with project-specific context seeded honestly.

The scaffold creates a repo-root `AGENTS.md` that points agents at the vault, a `.bc-agent/` Markdown wiki that is also a minimal Obsidian vault (`.bc-agent/.obsidian/`), with the maintainer schema, templates, conventions, the `planning-workflow.md` adapter, and `references/agent-skills.md` mapping the required loop skills in `~/Sync/CONFIG`, plus an empty `.bc-agent/out-of-scope/` directory for durable rejected enhancement records.

The vault lives directly at `.bc-agent/` (no per-project subfolder). The slug is only the wiki's **display name** in titles (defaults to the repo directory name); it doesn't affect the path.

**Faithful to the image-maze model:** no root `CONTEXT.md` — the glossary lives in the vault (`project/overview.md`), ADRs in `decisions/`, plans and actual PRDs in `project/`, exploratory research in `research/`. The adapter tells `grilling`/`domain-modeling` to persist there and tells agents to ask whether to enter `/bc-plan-to-issues` when the human appears to be planning codebase work.

## Operating modes and wiki archetypes

Default to **recon → targeted grill → proposed init plan → scaffold**. Do not blindly scaffold a non-empty folder.

Modes:
- **Recon-only**: when the user wants to inspect/understand the folder first, stop after the environment summary and recommended questions.
- **Plan init**: for empty, ambiguous, or existing projects, inspect first, grill enough to adapt the workspace, and present a concrete init/migration plan before writing.
- **Apply scaffold**: run the deterministic scaffold after the user accepts the plan or when the folder is clearly fresh and the user explicitly asked to initialize now.
- **Migration assist**: for old/messy projects, propose how existing docs/files could seed `.bc-agent/`; move/copy files only after explicit approval.

Archetypes:
- **code** — default project execution wiki: PRDs/plans, ADRs, validation, commands, tasks, `/bc-plan-to-issues` → `/bc-drain-issues`.
- **ops** — operational/system wiki like the Music wiki: `components/`, `findings/`, `decisions/`, `open-questions/`, executable plans; evidence before plan.
- **learning** — bc agents helping the human learn: `learning/`, `sources/`, `concepts/`, `questions/`, `sessions/`, plus an explicit link to the `teach` skill.
- **knowledge** — LLM-maintained knowledge graph like `~/Sync/Wiki`: immutable `raw/`, compiled `wiki/sources`, `wiki/entities`, `wiki/concepts`, `wiki/syntheses`, and a wiki log.
- **hybrid** — code execution plus one or more of ops/learning/knowledge when the folder clearly needs more than one durable mode.

## Process

1. **Locate the project.** Find the repo root (`git rev-parse --show-toplevel`). If not a git repo, inspect the current folder and ask whether to initialize git here, use this folder directly, or choose another root. Pick the slug: the argument, else the repo directory name in kebab-case. Confirm with the user if root/slug is ambiguous.

2. **Recon before grilling.** Inspect the environment before asking questions. Keep it bounded; do not crawl huge dependency/build output directories. Check at least:
   - Git state: repo root, branch, dirty status, remotes, existing `AGENTS.md`, existing `.bc-agent/`, `CONTEXT.md`, docs/plans/ADRs.
   - GitHub readiness: whether `gh` exists/auths and whether `gh repo view` works when an origin exists.
   - Project shape: empty/near-empty vs active vs old/messy; package/build/deploy markers (`package.json`, lockfiles, `pyproject.toml`, `Cargo.toml`, `go.mod`, Docker/Compose, CI, infra, scripts, Makefile/justfile, README).
   - Existing knowledge to seed: README, docs, issue templates, architecture notes, validation commands, deployment notes, old plans/specs.
   - Risk signals: uncommitted work, generated/vendor-heavy folders, secrets-looking files, unclear deploy/publish flow.

3. **Summarize state, choose an archetype, then grill adaptively.** Start by telling the user what you found, what mode you recommend, and which archetype seems to fit. Ask targeted questions one at a time unless the user asks for a full questionnaire. The first fork is purpose: is this workspace mainly for shipping code, operating a system, learning/research, personal knowledge capture, or a hybrid?

   For an **empty or near-empty folder**, establish intent before scaffolding: app/library/config/tooling/content/research; code vs ops vs learning vs knowledge; expected dev/build/deploy shape; GitHub issues vs local planning first; whether to create only agent docs or also propose project source layout; initial feature/mission if known.

   For an **existing active project**, integrate without disruption: which docs are authoritative; whether existing docs should be referenced, copied, or left in place; whether an existing root `AGENTS.md` remains primary; validation/build/test commands agents may trust; deploy/publish actions allowed, forbidden, or manual-only.

   For an **operational/system workspace**, identify components, findings/evidence, decisions, open questions, and executable plans. Ask what real-world actions agents may do vs only document for the human.

   For a **learning workspace**, ask the subject, desired outcome, current level, preferred learning cadence, source material, and whether to invoke the `teach` skill for multi-session tutoring records.

   For a **knowledge-graph workspace**, ask the domain boundary, source-ingest policy, raw immutability expectations, entity/concept granularity, and whether this is personal `~/Sync/Wiki`-style knowledge or project-local knowledge.

   For an **old/messy project being revived**, treat init as a reconciliation step: cleanup/continuation/archive/rewrite goal; authoritative old plans/specs/ADRs; which files could seed `project/`, `research/`, `decisions/`, `components/`, `findings/`, `open-questions/`, `learning/`, `sources/`, `concepts/`, `raw/`, or `out-of-scope/`; whether file moves are allowed now or should become a migration plan; what must not be touched.

4. **Propose the init plan before writing.** Name the root, slug, mode, selected archetype, files that will be created, existing files that will be preserved, any manual merge needed for `AGENTS.md`, any existing files proposed for later migration, and open decisions. If the plan includes moving/copying existing docs, separate that from the scaffold and require explicit approval.

5. **Safe to re-run / plug into an existing project.** The script is **additive and idempotent**: it creates only the files that are missing, leaves every existing file untouched (an existing root `AGENTS.md` is preserved verbatim and flagged for a manual pointer-merge), and **never deletes anything**. Re-running changes nothing. Use `--dry-run` when previewing an existing or messy project. Existing files are overwritten only when explicitly forced (`--force` for vault files, `--force-root` for the root `AGENTS.md`) — don't use those unless the user asks.

6. **Scaffold.** Run the bundled script (it lives next to this file):
   ```
   python3 <skill-dir>/scaffold.py --root "<repo-root>" --slug "<slug>" --archetype "<code|ops|learning|knowledge|hybrid>"
   ```
   It creates any missing files: the root `AGENTS.md` (only if absent — if one exists it's left untouched and you merge the vault pointer by hand) and the `.bc-agent/` tree with generalized schema + TODO stubs (`validation.md`, `file-layout.md`, `references/*`, the glossary) for the project's agents to fill as they learn the repo. It also seeds minimal stable Obsidian metadata (`.obsidian/app.json`, `core-plugins.json`, `appearance.json`) but deliberately avoids noisy/user-specific state such as `workspace.json`, `graph.json`, and community plugin config. The scaffold includes `references/agent-skills.md`, a repo-local map of `/bc-plan-to-issues`, `/bc-drain-issues`, `/improve-codebase-architecture`, and their supporting skills; the skill bodies remain canonical under `~/Sync/CONFIG` and are not copied into the repo.

7. **Seed obvious project facts conservatively.** After scaffolding, you may fill TODO stubs only with facts verified during recon (for example validation commands from README/package scripts, existing deploy notes, or authoritative docs). Mark uncertain items as TODO. Do not invent architecture or move old files during init unless the approved plan explicitly includes it.

8. **Wire publish authorization (offer).** `/bc-drain-issues` needs this repo authorized in `publish.yaml` for AFK push. Detect the remote (`git remote get-url origin`). Draft a rule block modeled on `image-maze-push-and-close-after-agent-work` with `paths`/`remotes` filled from this repo. Show it to the user and **offer to append it** to `~/Sync/CONFIG/agents/policies/publish.yaml` after they confirm. Never push that change (self-amendment immunity) — leave the user to push it. If they decline, note it as a TODO in the vault's `tasks/parking-lot.md` (the scaffold already seeds that reminder).

9. **Close out.** Point at the created files and any migration plan. Next steps for the user: fill or verify `conventions/validation.md` + `file-layout.md`; run `/triage` on existing issues or `/bc-plan-to-issues` for a new feature; use `/prototype` or `/improve-codebase-architecture` when planning needs evidence/runway; then `/bc-drain-issues` to execute. Commit the scaffold (it's the user's repo — stage the new files explicitly, concise message; don't sweep unrelated drift).

## Notes
- The vault is detached from the user's personal `~/Wiki` (seeded as ADR-0001).
- If the repo already has a root `AGENTS.md`, the script preserves it — merge in the "read the vault first" pointer rather than clobbering hand-written instructions.
