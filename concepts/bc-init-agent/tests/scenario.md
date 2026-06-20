# Scenario: bc-init-agent

Mostly a deterministic check of `body/scaffold.py` plus a process check of the skill's judgment steps. Run the script against throwaway dirs; run the skill body against a subagent in a throwaway git repo for the interview/offer steps.

## Script checks (deterministic)

1. **Tree shape.** `scaffold.py --root <tmp> --slug demo-proj` writes the repo-root `AGENTS.md`, the full `.bc-agent/` vault (AGENTS/index/home/map/log, `project/overview.md`, `references/*`, `conventions/*` including `planning-workflow.md`, `decisions/adr-0001-*`, `tasks/*`, `templates/*`), and `.bc-agent/research/README.md` + `.bc-agent/scratch/.gitkeep`. The vault is at `.bc-agent/` directly — no `<slug>` subfolder.
2. **Substitution.** No literal `__SLUG__` / `__DATE__` remain in any written file; the slug and date appear correctly.
3. **Idempotent re-run (never destructive).** Re-running against a fully-scaffolded root creates/overwrites/deletes nothing — every file is reported "untouched" and the on-disk checksums are identical to before the re-run.
4. **Additive plug-in.** In a root that already has a hand-written `AGENTS.md` and some pre-existing `.bc-agent/` pages, the script creates only the missing files and leaves the existing ones **byte-for-byte unchanged** (the existing root `AGENTS.md` is preserved and flagged for a manual pointer-merge). Nothing is deleted.
5. **No overwrite without force; dry-run writes nothing.** Default never overwrites an existing file; `--dry-run` reports intended writes but creates 0 files; `--force`/`--force-root` are the only paths that replace existing content (and still delete nothing).
6. **Slug validation.** A slug with spaces or uppercase is rejected (exit 1).

## Skill process checks

7. **Locate + confirm.** Uses the git repo root and a kebab-case slug; confirms when ambiguous or non-git.
8. **publish.yaml offer-then-confirm.** Drafts a repo-specific allow rule and OFFERS to append it to `policies/publish.yaml`; does NOT write it without confirmation and never pushes it. On decline, leaves the parking-lot TODO.
9. **Close-out.** Points at created files and the next steps (`/bc-plan-to-issues` → `/bc-drain-issues`); commits the scaffold staging only the new files.

## Pass criteria
Script checks 1–6 pass on inspection of the generated tree; process checks 7–9 hold in the subagent transcript.
