# Scenario: bc-init-agent

Mostly a deterministic check of `body/scaffold.py` plus a process check of the skill's judgment steps. Run the script against throwaway dirs; run the skill body against a subagent in a throwaway git repo for the interview/offer steps.

## Script checks (deterministic)

1. **Tree shape.** `scaffold.py --root <tmp> --slug demo-proj` writes the repo-root `AGENTS.md`, the full `.bc-agent/` vault (AGENTS/index/home/map/log, `project/overview.md`, `references/*`, `conventions/*` including `planning-workflow.md`, `decisions/adr-0001-*`, `tasks/*`, `templates/*`), and `.bc-agent/research/README.md` + `.bc-agent/scratch/.gitkeep`. The vault is at `.bc-agent/` directly — no `<slug>` subfolder.
2. **Substitution.** No literal `__SLUG__` / `__DATE__` remain in any written file; the slug and date appear correctly.
3. **Clobber guard.** Re-running against the same root exits 2 and writes nothing.
4. **Root AGENTS.md preserved.** With a pre-existing `<root>/AGENTS.md`, the script does NOT overwrite it (prints a merge note); the vault is still written.
5. **Slug validation.** A slug with spaces or uppercase is rejected (exit 1).

## Skill process checks

6. **Locate + confirm.** Uses the git repo root and a kebab-case slug; confirms when ambiguous or non-git.
7. **publish.yaml offer-then-confirm.** Drafts a repo-specific allow rule and OFFERS to append it to `policies/publish.yaml`; does NOT write it without confirmation and never pushes it. On decline, leaves the parking-lot TODO.
8. **Close-out.** Points at created files and the next steps (`/bc-grill-to-issues` → `/bc-drain-issues`); commits the scaffold staging only the new files.

## Pass criteria
Script checks 1–5 pass on inspection of the generated tree; process checks 6–8 hold in the subagent transcript.
