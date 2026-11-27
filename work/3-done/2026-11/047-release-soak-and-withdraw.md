# Releases reach strangers only after a soak, and a bad one can be pulled back

Why: Agents release without asking, the npm install is unpinned and the Pi package loads the kernel into every session, so a bad agent-written release reaches every stranger at once; the only written remedy is "release the next patch".
Done when: A tagged release lands on npm's `next` dist-tag, moves to `latest` only after the stranger end-to-end test passes on that version, and `docs/guides/releasing.md` has a bad-release procedure (deprecate, move `latest` back, release note, CHANGELOG entry) that has been dry-run.
Stage: now
Blocked by: nothing
Kind: release
Source: blind-spot council, owner decisions 2026-11-27 (1a: soak on next, agents keep releasing without asking)
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Requirements

- `release.yml`'s `publish-npm` job publishes with `--tag next`; `latest` moves only by the promotion step.
- Promotion runs after `STRANGER_SOURCE=pack scripts/stranger_end_to_end.sh` (or an npm-installed variant of it) passes for that version. The npm trusted publisher allows both `npm publish` and `npm dist-tag` (owner choice 2026-11-27, staged publishing declined), so promotion runs from `release.yml` under OIDC with no stored token; if npm still refuses, stop and ask the owner; do not add a token.
- "Bad release" section in `docs/guides/releasing.md`: `npm deprecate agent-concepts@X "<reason; use Y>"`, move `latest` back to the last good version, a GitHub release note, and a CHANGELOG "Withdrawn" line; decision 0002 and AGENTS.md's Release operation name the soak.
- README: say that `pi install npm:agent-concepts` follows `latest`, and how to try `next`.

## Steps

- [x] Publish to `next`, promote to `latest` after the stranger test, and document a bad-release procedure. Done when a test version goes to `next` and is promoted (or the owner has chosen the promotion authorization), and the bad-release steps are run once against a throwaway prerelease or reviewed line by line against npm docs. Out of scope: Claude Code and Codex plugin channels.

## Outcome

Done 2026-11-27 (gate green on tree c6a74ca40e394b35a7fa6d47467b6ba76f5c8fbc: 657 passed, 4 skipped, 2m05s). `release.yml` publishes tags to `next`; a `workflow_dispatch` `set-latest` job (promote: only the version on `next`; rollback: any published version) moves `latest` over OIDC with npm CLI >= 11.21.0, the minimum npm's trusted-publishers page names for dist-tags (11.5.1 is enough only for publish). `stranger_end_to_end.sh` gained `STRANGER_SOURCE=npm STRANGER_VERSION=X.Y.Z` to test the published version. `docs/guides/releasing.md` has the soak (steps 11-13) and "Withdraw a bad release"; decision 0002, AGENTS.md's Release operation, README and harnesses.md name the soak.

Done-when met by its alternatives: the owner chose the promotion authorization (trusted publisher with Allow npm dist-tag), and the bad-release steps were reviewed line by line against docs.npmjs.com (trusted-publishers, dist-tag, deprecate, unpublish policy; research notes in the run folder) rather than run against a throwaway prerelease, which would leave a permanent version on npm. `set-latest`'s shell logic was tested with a stub npm (promote, wrong version, rollback, already latest, unknown version, bad format). The first real promotion is the first live run of `set-latest`.

Found on the way: Pi 1.6.1's plain `pi update` updates only Pi (`--self` is the default), so the README's update advice now says `pi update --extensions`; Pi treats `npm:agent-concepts@next` as unpinned and updates it to the newest `next`, and never downgrades, so moving `latest` back does not roll anyone back (written into the withdraw section). `npm deprecate` cannot run under OIDC, so it stays a maintainer step.
