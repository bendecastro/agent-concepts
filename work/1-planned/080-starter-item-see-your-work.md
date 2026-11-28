# Setup offers a starter item for seeing your work, and the scaffold stops citing "the owner's dashboard"

Why: the scaffold justifies about six work-item rules (`Needs owner:`, `Changes UI:`, `Held by:`, review results, costs, order placement) with "the owner's dashboard shows it" (`concepts/bc-setup-project/body/scaffold.py` work-item rules), but setup never mentions a dashboard or helps build one, so a stranger reads reasons that point at nothing and the lines look like overhead. The data already exists: `work_index.py --json`, documented in `work-data.md`.
Stage: next
Blocked by: nothing
Kind: feature
Source: owner answer in chat 2026-11-28 (private-to-public audit follow-up)
Dependencies: none new

## Requirements (not planned yet: run bc-plan-to-pipeline)

- **Starter item.** A new entry in `starter-items.md`, offered at setup like the others: ask how the person wants to see their work, then build that. Options to offer: the generated `work/README.md` table (nothing to build; fine for one project); a small local page or terminal view built from `work_index.py --json` (several projects); feeding a tool they already use (an Obsidian Base over `work/`, a GitHub Project, a status bar). The item records the choice and what each work-item line looks like there.
- **Reasons that point somewhere.** The scaffold's "the owner's dashboard shows it" reasons become "your dashboard (or `work/README.md`) shows it"; a MIGRATIONS entry covers existing projects.
- **Out of scope.** Publishing the owner's own dashboard.
