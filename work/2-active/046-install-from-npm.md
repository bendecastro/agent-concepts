# Strangers install from npm and get every release through `pi update`

Why: The README's `pi install git:…@v0.3.0` pins the package, and Pi skips pinned packages on `pi update`, so everyone stays on the version they first installed even after new releases.
Done when: The release workflow publishes each tagged release to npm as `agent-concepts`; the README's Pi install is `pi install npm:agent-concepts` with no version (pinning shown as an option); `pi update` on a fresh install moves to a newer release.
Stage: now
Blocked by: nothing
Kind: release
Source: owner decision A1 on release reach, 2026-11-27
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Requirements

- No stored token (owner choice 2026-11-27): the release workflow publishes through npm trusted publishing (GitHub Actions OIDC, `id-token: write`, an npm CLI new enough for trusted publishing, `--provenance`). The first publish is manual from the owner's machine after `npm login` (the integrating session runs `npm publish --access public` for the release); the owner then connects the trusted publisher on npmjs.com (repository and `release.yml`). `docs/guides/releasing.md` documents both. The name `agent-concepts` was free on 2026-11-27.
- `package.json` drops `"private": true`, adds a `files` list so only the skills, roles, kernel extension and licence ship, and stays the single version home.
- `.github/workflows/release.yml` publishes with provenance after `release_check.py` passes, and skips publishing cleanly (with a notice) when the version is already on npm, so the manual first publish does not fail the tag's workflow; `release_check.py` or the fresh-install test proves the packed tarball installs in Pi with the skills, roles and kernel.
- `release_check.py` accepts a README Pi install that names no tag (npm, unpinned) while still checking the pin example; README Install, `docs/guides/releasing.md`, `docs/guides/harnesses.md` and decision 0002 updated (npm is the unpinned default; git tags remain for pinning).

## Steps

- [ ] Publish tagged releases to npm and point the README at it. Done when a release run publishes and a fresh Pi home installs `npm:agent-concepts` and lists the skills. Out of scope: other harnesses' marketplaces.

## Outcome

_To be filled when finished or dropped._
