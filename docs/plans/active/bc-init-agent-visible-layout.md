# bc-init-agent visible layout — work folders the owner can browse

Date: 2026-11-12
Status: active
Verification: none yet. Design agreed with the owner in a 22-question interview on 2026-11-12;
no code has changed.

## Problem

`bc-init-agent` scaffolds everything inside a hidden `.bc-agent/` vault: glossary in
`project/overview.md`, ADRs in `decisions/`, plans and PRDs mixed in `project/`, status in
`tasks/active.md`, `tasks/completed.md` and `tasks/parking-lot.md`.

Recon of the owner's projects on 2026-11-12 found that this no longer matches how projects are
built:

- The two newest real projects moved knowledge into the open on their own. One has no vault at
  all (root `glossary.md`, `decisions/`, `research/`, `docs/plans/`). The other kept the vault
  for agent mechanics only and put the rest in `docs/` plus a root `glossary.md`.
- Hand-kept status files go stale or unused. `completed.md` holds only its scaffold entry in
  three older projects; `parking-lot.md` still holds seed text in two; one project's
  `active.md` names a next action that is already done. `scratch/` and `out-of-scope/` only
  ever held `.gitkeep`.
- Plans sit in one flat folder and carry their state as a line inside the file, or as
  checkboxes. The owner cannot tell what is planned, in progress or done by browsing folders.
- The one place where state is readable at a glance is a job queue whose folders are named
  for states (`ready/`, `running/`, `done/`).

The owner's goal: open a project and see, from the directory tree alone, what was planned, what
is being worked on, what is done, and what was dropped.

## Resolved decisions

Numbers are the interview questions. Each was put to the owner with alternatives.

### Layout (code, ops and hybrid archetypes)

```
AGENTS.md
glossary.md
ARCHITECTURE.md          only when the project needs one
work/
  0-ideas.md             undecided ideas and agents' observations, one line each
  1-planned/             decided, not started
  2-active/              being worked on
  3-done/<year>-<month>/ finished, with an Outcome
  4-dropped/             abandoned or rejected, with the reason
docs/
  decisions/             one file per decision
  research/              dated folders, including architecture reviews
  PRD.md                 only when the project has a product-level spec
.bc-agent/
  AGENTS.md              session protocol plus the "where things go" table
  map.md  log.md
  conventions/  references/  templates/
.agents/skills/local-<name>/   project skills, created on first need
```

1. **Knowledge is visible; `.bc-agent/` holds agent mechanics only** (Q1).
2. **Lifecycle folders: a work item's folder is its status** (Q2), changed with `git mv`. The
   owner added a fourth state for work that was planned and then deliberately not done.
3. **`work/` at the repo root with numbered stages** (Q5), so every listing shows lifecycle
   order.
4. **Ideas are one list file, `work/0-ideas.md`** (Q6). Files in folders are committed work;
   the list is not. "Parking lot" is retired as a term in this layout.
5. **Root `glossary.md`; decisions and research under `docs/`** (Q7). Plans have no folder of
   their own: a plan is the work item.
6. **No placeholders** (Q8). Feature requirements live in the work item. `docs/PRD.md` and
   `ARCHITECTURE.md` have fixed homes named in the layout table and are created on first need;
   the skill asks whether the project has a product-level spec.
7. **Removed from the scaffold** (Q9): `tasks/`, `project/`, `decisions/`, `research/`,
   `scratch/`, `index.md`, `home.md`, Obsidian settings. `log.md`, `map.md`, `conventions/`,
   `references/`, `templates/` stay.
8. **Rejected requests and dropped work share `work/4-dropped/`** (Q10). `out-of-scope/` is
   retired; `triage` writes there.
9. **`3-done/` uses month subfolders from the first item** (Q20). A rule applied always needs
   no threshold detection. Lint fails on an item directly in `3-done/`. `4-dropped/` is flat.

### Work items

10. **The item is the feature or plan; slices live inside it** (Q4). A small item is one file.
    A large one is a folder holding `plan.md`, requirements and slice files, and the whole
    folder moves.
11. **Name: sequence number plus slug**, `012-search-ranking` (Q11). The owner chose numbers
    over dates for the short citable id.
12. **Only the main checkout creates items** (Q12). Next number is the highest across all
    stages plus one. Workers in worktrees add a line to `0-ideas.md`. Lint fails on duplicates.
    Why: nothing hands out numbers centrally, so parallel worktrees would collide.
13. **No priority mechanism** (Q13). Moving an item to `2-active/` is the choice.
14. **Template** (Q14): title, `Why:`, `Done when:`, optional `Issue:`, `## Steps`,
    `## Outcome`. No `Status:` line, so a file cannot disagree with its folder.
15. **Folders are the source of truth; GitHub issues are optional and point back** (Q3). The
    file records the issue number; closing the issue is part of moving the file.
16. Resolved by the agent and shown to the owner without objection: several items may be active
    at once; the agent doing the work moves the item in the same commit as the work.

### Skill behaviour and scope

17. **Learning and knowledge archetypes keep the current vault for now** (Q15). `teach` reads
    exact vault paths and tests pin that mapping; changing it is a separate plan.
18. **Default location is suggested, with a warning inside a synced folder** (Q16). The
    suggestion is read from the owner's preferences file, not hard-coded, because the owner
    plans to standardise project locations after this plan.
19. **Project skills and agents use the standard discovered folders** (Q21): `.agents/skills/`
    with a `local-` prefix and a README recording which entries are copies of shared concepts
    and how to refresh them. Named in the layout table, created on first need. Open check:
    which project folder `pi-subagents` discovers agent definitions in.

### Other concepts

20. **One "where things go" table per project; skills refer to roles** (Q18). The scaffold
    writes the table in `.bc-agent/AGENTS.md` (work items, ideas, decisions, research,
    glossary, requirements, project skills, project agents). Skills say "the project's
    decisions folder" and look it up; scripts read the same table. A project with a justified
    exception edits one table.
21. **Architecture reviews** (Q19): the report is saved as
    `docs/research/<date>-architecture-review/`; a chosen finding becomes an item in
    `1-planned/`, a rejected one goes to `4-dropped/` with the reason, the rest become lines in
    `0-ideas.md`. Agents' observations between reviews go to `0-ideas.md`. The separate
    observation inbox and disposition ledger are retired.

### Existing projects

22. **Five vault projects are migrated in one pass** after the concepts land (Q17): planned
    moves are shown per repository first, done with `git mv` in one commit, and a repository
    with uncommitted work waits for the owner.
23. **One project without a vault gets the new layout in a separate focused session** with its
    own interview (Q22); its domain folders and root `decisions/` and `research/` stay, recorded
    as exceptions in its table. A second vault-less project that follows ordinary open-source
    conventions is left alone.

## Affected concepts

Literal-path consumers found by search on 2026-11-12; indirect consumers may exist.
`RELATIONSHIPS.md` edges must be accounted for in each change.

| Concept | Change |
|---|---|
| `bc-init-agent` | new tree, layout table, work-item template, location suggestion, migration |
| `bc-wiki-maintain` | lint reads the table; drops `index.md` and `tasks/active.md` assumptions for the new layout; gains work-folder checks |
| `triage` | rejection records go to the dropped folder via the table |
| `bc-drain-issues` | observations go to the ideas file; work status by moving items |
| `bc-plan-to-issues` | slices live inside the work item; issue number recorded in it |
| `improve-codebase-architecture` | inbox and ledger rules replaced by the work folders; report saved to research |
| `diagnosing-bugs`, `prototype`, `handoff` | path references become role lookups |
| `teach` | unchanged; its adapter still targets the old vault |

## Work packages

- **W1 — scaffold.** `scaffold.py` and `SKILL.md` produce the new tree for code, ops and hybrid;
  write the layout table and the work-item template; update `tests/` (scenario, map links, read
  contract) and keep the teach-adapter tests passing unchanged.
- **W2 — lint.** Work-folder checks: duplicate numbers, items directly in `3-done/`, a
  `Status:` line in an item, a dropped or done item without an Outcome. Table parsing shared
  with W3.
- **W3 — dependent concepts.** Role lookups in the concepts listed above; rewrite the
  architecture inbox rules; regenerate relationships.
- **W4 — migration.** A dry-run-first migrate mode that maps old vault paths to the new layout
  with `git mv`, and `MIGRATIONS.md` notes.
- **W5 — test and deploy.** Pressure scenarios for the discipline parts (move the item rather
  than edit a status; workers do not create numbered items; reason recorded on drop), then
  deploy.
- **W6 — migrate the five projects**, one commit each, moves shown to the owner first.

W1 fixes the table format that W2 and W3 read, so it lands first. W2 and W3 touch different
concepts and can follow in parallel.

## Out of scope

- Learning and knowledge archetypes.
- Standardising where the owner's projects live on disk; follows this plan.
- Investigating stray `skills/system/run-workflow/` folders found in two projects; reported
  during W6 before anything is touched.

## Evidence

Recon reports for this plan were produced by four read-only scouts on 2026-11-12 and are not
stored in this repository; the counts above were taken from them and spot-checked against the
projects.
