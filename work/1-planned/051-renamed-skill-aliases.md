# A renamed skill keeps working under its old name for installed users

Why: Renaming `bc-ui-design` to `bc-design` removed the old name for npm, plugin and `npx skills` users (only local deploys keep an alias), and no policy says how renames or removals are announced.
Done when: A written policy keeps an old skill name working for at least one minor release on every install method that can carry it, `bc-ui-design` follows it, and the CHANGELOG format has a Renamed/Removed section.
Stage: now
Blocked by: nothing
Kind: release
Source: blind-spot council, owner decisions 2026-11-27 (4a: finding D)
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Requirements

- Decide per install method how an alias ships (for example a tiny stub skill whose body says "renamed: load bc-design" in the package's `files`); record the method in `docs/guides/releasing.md` or a decision, with the removal version.
- Lint or `release_check.py` flags a skill name present in the previous tag but missing now with no alias or CHANGELOG Removed entry.

## Steps

- [ ] Write the rename policy, ship a `bc-ui-design` alias in the package, and add the check. Done when a fresh npm-pack install answers `/skill:bc-ui-design` by pointing to bc-design, and the check fails on a fixture rename with no alias. Out of scope: local deploy aliases (already work).

## Outcome

_To be filled when finished or dropped._
