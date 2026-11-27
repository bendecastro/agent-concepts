# Strangers install from npm and get every release through `pi update`

Why: The README's `pi install git:…@v0.3.0` pins the package, and Pi skips pinned packages on `pi update`, so everyone stays on the version they first installed even after new releases.
Done when: The release workflow publishes each tagged release to npm as `agent-concepts`; the README's Pi install is `pi install npm:agent-concepts` with no version (pinning shown as an option); `pi update` on a fresh install moves to a newer release.
Stage: now
Blocked by: 042-one-command-pi-install
Kind: release
Source: owner decision A1 on release reach, 2026-11-27
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: no

## Requirements

- Owner action first: an npm account and a granular publish token saved as the GitHub secret `NPM_TOKEN` (or npm trusted publishing once the package exists). The name `agent-concepts` was free on 2026-11-27.
- `package.json` drops `"private": true`, adds a `files` list so only the skills, roles, kernel extension and licence ship, and stays the single version home.
- `.github/workflows/release.yml` publishes with provenance after `release_check.py` passes; `release_check.py` or the fresh-install test proves the packed tarball installs in Pi with the skills, roles and kernel.
- README Install, `docs/guides/releasing.md`, `docs/guides/harnesses.md` and decision 0002 updated (npm is the unpinned default; git tags remain for pinning).

## Steps

- [ ] Publish tagged releases to npm and point the README at it. Done when a release run publishes and a fresh Pi home installs `npm:agent-concepts` and lists the skills. Out of scope: other harnesses' marketplaces.

## Outcome

_To be filled when finished or dropped._
