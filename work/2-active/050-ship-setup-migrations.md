# Projects set up earlier can find the upgrade steps in the installed package

Why: `concepts/bc-setup-project/MIGRATIONS.md` sits outside `body/`, so npm, plugin and `npx skills` installs do not ship it, yet the CHANGELOG and `scaffold.py` point strangers to it; and generated projects carry no scaffold version to say which steps apply.
Done when: The migration steps ship inside `body/`, every reference points to the shipped path, and setup stamps a scaffold version into generated projects that the migration page uses.
Stage: now
Blocked by: nothing
Kind: bug
Source: blind-spot council, owner decisions 2026-11-27 (4a: finding C)
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Steps

- [ ] Move MIGRATIONS.md into `body/`, update references (scaffold.py, CHANGELOG link for the next release, CONCEPT.md, relationships if any), and stamp a scaffold version in generated projects. Done when `npm pack --dry-run` lists the file, a test proves a new scaffold carries the version, and lint passes. Out of scope: rewriting existing migration steps.

## Outcome

_To be filled when finished or dropped._
