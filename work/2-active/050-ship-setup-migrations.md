# Projects set up earlier can find the upgrade steps in the installed package

Why: The migration guide previously sat outside `body/`, so npm, plugin and `npx skills` installs did not ship it despite references to it; and generated projects carry no scaffold version to say which steps apply.
Done when: The migration steps ship inside `body/`, every reference points to the shipped path, and setup stamps a scaffold version into generated projects that the migration page uses.
Stage: now
Blocked by: nothing
Kind: bug
Source: blind-spot council, owner decisions 2026-11-27 (4a: finding C)
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Steps

- [x] Move MIGRATIONS.md into `body/`, update references (scaffold.py, CHANGELOG link for the next release, CONCEPT.md, relationships if any), and stamp a scaffold version in generated projects. Done when `npm pack --dry-run` lists the file, a test proves a new scaffold carries the version, and lint passes. Out of scope: rewriting existing migration steps.

## Outcome

The earlier partial commit fec697b shipped the guide and updated references. This commit adds the first-scaffold version marker, release annotations and regression tests; review and integration remain with the parent.
