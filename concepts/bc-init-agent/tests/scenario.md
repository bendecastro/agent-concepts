# Scenario: bc-init-agent

Mostly a deterministic check of `body/scaffold.py` plus a process check of the skill's judgment steps. Run the script against throwaway dirs; run the skill body against a subagent in a throwaway git repo for the interview/offer steps.

## Script checks (deterministic)

1. **Tree shape.** `scaffold.py --root <tmp> --slug demo-proj` writes the repo-root `AGENTS.md`, the full `.bc-agent/` vault (AGENTS/index/home/map/log, `project/overview.md`, `references/*` including `agent-skills.md`, `conventions/*` including `planning-workflow.md`, `decisions/adr-0001-*`, `tasks/*`, `templates/*`), and `.bc-agent/research/README.md` + `.bc-agent/scratch/.gitkeep`. The vault is at `.bc-agent/` directly — no `<slug>` subfolder.
2. **Substitution.** No literal `__SLUG__` / `__DATE__` remain in any written file; the slug and date appear correctly.
3. **Idempotent re-run (never destructive).** Re-running against a fully-scaffolded root creates/overwrites/deletes nothing — every file is reported "untouched" and the on-disk checksums are identical to before the re-run.
4. **Additive plug-in.** In a root that already has a hand-written `AGENTS.md` and some pre-existing `.bc-agent/` pages, the script creates only the missing files and leaves the existing ones **byte-for-byte unchanged** (the existing root `AGENTS.md` is preserved and flagged for a manual pointer-merge). Nothing is deleted.
5. **No overwrite without force; dry-run writes nothing.** Default never overwrites an existing file; `--dry-run` reports intended writes but creates 0 files; `--force`/`--force-root` are the only paths that replace existing content (and still delete nothing).
6. **Slug validation.** A slug with spaces or uppercase is rejected (exit 1).

## Skill process checks

7. **Locate + recon before grilling.** Uses the git repo root and a kebab-case slug; confirms when ambiguous or non-git. Before asking substantive questions, inspects git state/remotes, `gh` readiness when applicable, existing agent/docs/plans files, project/build/deploy markers, and risk signals.
8. **Adaptive grill.** Summarizes the detected state and recommends a mode. Empty folders get project-intent/dev-shape questions; active projects get integration/validation/deploy-policy questions; old or messy projects get reconciliation/migration questions. It does not blindly scaffold a non-empty folder.
9. **Proposed init plan before writing.** Names the root, slug, files to create, files to preserve, manual root-`AGENTS.md` merge needs, conservative seed edits, and any separate migration plan. Existing file moves/copies require explicit approval.
10. **publish.yaml offer-then-confirm.** Drafts a repo-specific allow rule and OFFERS to append it to `policies/publish.yaml`; does NOT write it without confirmation and never pushes it. On decline, leaves the parking-lot TODO.
11. **Close-out.** Points at created files, `references/agent-skills.md`, any migration plan, and the next steps (`/bc-plan-to-issues` → `/bc-drain-issues`); commits the scaffold staging only the new files.

## Pass criteria
Script checks 1–6 pass on inspection of the generated tree; process checks 7–11 hold in the subagent transcript.

## Run result — 2026-06-21 — **PASS**

Script checks 1–6 run directly (no subagent):
1. Tree shape: root `AGENTS.md` + full `.bc-agent/` vault (AGENTS/index/home/map/log, `project/overview.md`, `references/*` incl. `agent-skills.md`, `conventions/*` incl. `planning-workflow.md`, `decisions/adr-0001-*`, `tasks/*`, `templates/*`, `research/README.md`, `scratch/.gitkeep`, `out-of-scope/.gitkeep`) at `.bc-agent/` with no slug nesting. ✓
2. Substitution: no residual `__SLUG__`/`__DATE__`; slug + date present. ✓
3. Idempotent re-run: byte-identical checksums, reported "untouched", nothing created/deleted. ✓
4. Additive plug-in: into a root with hand-written `AGENTS.md` + pre-existing vault page, existing files left byte-identical, only missing created, root `AGENTS.md` flagged for manual pointer-merge, nothing deleted. ✓
5. No-overwrite/dry-run: `--dry-run` wrote 0 files; default left existing untouched. ✓
6. Slug validation: spaces and uppercase both exit 1. ✓

Process checks 7–9 via Haiku subagent (low-thinking, hard-sandboxed to `/tmp/pt-bcinit2`):
7. Located root via `git rev-parse --show-toplevel`, kebab-case slug, no ambiguity. ✓
8. Drafted a repo-specific `publish.yaml` allow-rule and OFFERED to append it; did not write it (verified: real `agents/policies/publish.yaml` untouched). ✓
9. Close-out pointed at created files + named next steps (`/triage` → `/bc-plan-to-issues` → `/bc-drain-issues`); committed staging only the new scaffold files (`git add AGENTS.md .bc-agent/`), clean tree after. ✓

## New checks to run after adaptive-onboarding update

Run additional process scenarios before treating the new behavior as proven:

- **Empty folder:** non-git or newly initialized empty directory; pass = recon identifies emptiness and asks project-intent/dev-shape questions before scaffolding.
- **Existing active project:** repo with README, package/build files, existing docs, and dirty status; pass = summarizes environment, asks integration/validation/deploy questions, and does not scaffold until plan approval.
- **Old/messy project:** repo with scattered old plans/docs; pass = proposes a separate migration/reconciliation plan and does not move/copy files during init without explicit approval.
