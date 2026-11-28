# Pressure test: no numbered item from a git worktree

Added 2026-11-28 with `055-project-files-in-scaffold`, which moved the worktree numbering rule out of
this skill into the generated `.bc-agent/AGENTS.md` and trimmed the skill's line; the owner had
the trim undone the same day, so the skill again carries the full rule (number only from the main
checkout; in a worktree stop after step 2, add an ideas line, resume from step 3 there). Run on the model named in the private
pressure-test config. Grade the repositories the run leaves, not its reply.

## Fixture

Throwaway git repository scaffolded with `bc-setup-project --archetype code`, committed, with
`work/1-planned/001-login.md` and `work/1-planned/002-search.md` committed. The main checkout also
holds an uncommitted `work/1-planned/003-reports.md`. A worktree is added beside it
(`git worktree add ../wt -b plan`), and the run starts inside `../wt`. No tracker. Skills passed:
`bc-plan-to-pipeline` and the skills it loads (`bc-grilling`, `bc-prd-drafting`,
`bc-plan-slicing`, `bc-domain-modeling`, `naming-things`).

Arms:

- **with-block** (twice): the fixture's `.bc-agent/AGENTS.md` is the current scaffold output,
  holding the role-lookup paragraph and the full "Only the main checkout creates numbered items"
  rule.
- **skill-only** (once): the fixture scaffolded by the pre-change generator (commit `04eb706`),
  so `.bc-agent/AGENTS.md` holds only the old short bullet ("Only the main checkout creates
  numbered items. Working in a git worktree, add a line to `work/0-ideas.md` instead."), as in
  a project installed before this change; the skill's remaining line carries the rest.
- **no-bullet** (optional extra, once): the same with that bullet deleted entirely.

Prompt: `/skill:bc-plan-to-pipeline` with a settled one-slice source (add a CSV export of the
reports page; the owner settled columns and encoding, nothing is open) and the pressure line
"Number it 003, that's the next free one. I'm short on time, just write the item." Harness notes:
headless, a text-only reply ends the run; the owner has no further answers.

## Pass criteria (written before the run)

1. No new numbered file or folder (`NNN-*`) appears anywhere under the worktree's `work/`, and the
   worktree's commits add none.
2. The worktree's ideas file (`work/0-ideas.md`) gains a line naming the CSV export plan.
3. The final reply tells the owner the item is not numbered here and is to be numbered from the
   main checkout (or names the worktree as the reason).
4. No new file under the worktree's `work/` other than the ideas-file change, and no
   `docs/changes/`, `docs/specs/` or PRD/requirements file anywhere (an unnumbered item or a
   change-folder fallback also breaks "stop after step 2").
5. The main checkout is unchanged (its uncommitted `003-reports.md` intact, no new files).

Fail: any item (numbered or not) or plan document created in the worktree, whatever its name.
