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

- [x] Write the rename policy, ship a `bc-ui-design` alias in the package, and add the check. Done when a fresh npm-pack install answers `/skill:bc-ui-design` by pointing to bc-design, and the check fails on a fixture rename with no alias. Out of scope: local deploy aliases (already work).

## Outcome

Added a compatibility stub across package, plugins and npx skill installs, with a documented removal policy (bc-ui-design no earlier than v0.6.0). Release checks compare public names against the previous tag and require a Removed entry for any missing name. Fresh packed Pi install listed the alias and loaded its target instruction; npx-all could not run locally because the skills CLI is unavailable.

Review rounds: the first review's four findings were fixed (strict `- `name`: reason` Removed entries, alias-only pack lifecycle, alias target/shadowing tests, packed-Pi `/skill:bc-ui-design` expansion probe). The second review's follow-ups were fixed by the parent (owner choice a, 2026-11-28): Removed entries inside HTML comments or fenced code no longer count, aliases obey the `bc-` prefix rule, and the kernel test tolerates the alias's retirement; each new test failed first. Known gap, accepted: the packed-Pi probe calls Pi's private `_expandSkillCommand` directly rather than submitting a prompt, so it would stay green if Pi stopped calling that resolver during normal submission while keeping the function; a missing resolver, changed output or undiscovered alias still fails it.
