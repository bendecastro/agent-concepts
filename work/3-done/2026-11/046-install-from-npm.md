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

- [x] Publish tagged releases to npm and point the README at it. Done when a release run publishes and a fresh Pi home installs `npm:agent-concepts` and lists the skills. Out of scope: other harnesses' marketplaces.

## Outcome

Done 2026-11-27. Built: `package.json` is publishable (no `private`, `repository` for provenance, a generated `files` list checked by lint through `scripts/pi_package.py`); `release.yml` gains a `publish-npm` job (OIDC trusted publishing, npm ≥ 11.5.1, `--provenance`, skips with a notice when the version is already on npm); `scripts/fresh_install_test.py` gains a `pi-npm` method that runs `npm pack`, checks the tarball holds the kernel extension, roles and licence and nothing outside `files`, and installs it in Pi; `release_check.py` requires the README's unpinned `pi install npm:agent-concepts` and checks the npm pin example names the version; README Install, `docs/guides/releasing.md` (with the manual first publish and trusted-publisher setup), `docs/guides/harnesses.md` and decision 0002 updated. npm's requirements were read from docs.npmjs.com/trusted-publishers on 2026-11-27 (npm CLI 11.5.1+, Node 22.14.0+, `id-token: write`).

Evidence: `npm pack --dry-run` lists 139 files, 367 kB packed — the 133 tracked files of the 52 public skill bodies (the three pipeline roles among them), `packages/agent-kernel-pi/` (index.js, AGENT-KERNEL.md, package.json), README, LICENSE, package.json; no `work/`, `docs/`, or `tests/`. In a fresh isolated Pi 1.6.1 home, `pi install <tarball>.tgz` records the path but loads no skills; the unpacked tarball folder lists all 52 public skills and loads the kernel extension with no errors, and `fresh_install_test.py --method pi-npm` passes install, update and uninstall.

First publish: the owner ran `npm publish --access public` from a clean clone of tag `v0.4.0`; npm shows `agent-concepts@0.4.0` with shasum `e18ffba…`, the same as the local `npm pack`. A fresh Pi home (temporary `PI_CODING_AGENT_DIR`) installs `npm:agent-concepts` at 0.4.0 with 52 concepts. The tag's `release` run is green and its `publish-npm` job skipped as already published. Still open outside this item: the owner connects the trusted publisher shortly before the next release (npm expires an unused one after 2 days), and that release shows whether the workflow publishes and `pi update` moves an install forward.
