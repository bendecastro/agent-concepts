# Releasing

How a maintainer cuts a release of the public skills. People outside this repository install
tagged releases, never `master` ([decision 0002](../decisions/0002-tagged-releases-for-strangers.md)),
so a release is a deliberate step. Tags are `vMAJOR.MINOR.PATCH`.

## Before you tag

1. Pick the commit to release, normally the tip of `master`. Check that its `gate` workflow
   run is green, including both `fresh-install` jobs (Ubuntu and macOS).
2. Check that every changed rule held a pressure test. Run `git diff <last tag>..HEAD --
   concepts/*/body` and sort each discipline concept's changes since its `tested` date
   (see [status.md](../status.md)) into two kinds, recorded in a release audit under
   `docs/research/<date>-release-audit.md`:
   - **Rule changes** add or change a stop, a requirement or a prohibition. Each needs a held
     pressure test after the change (see the Test operation in `AGENTS.md`). A rule repeated
     across skills is tested once, in one of them; the audit names that test for the others.
     A one-line stop with no judgment in it (for example "stop if the tool is missing") may be
     checked by reading instead.
   - **Wording changes** (renames, links, moved text, plainer wording with the same meaning)
     need no retest.
   No concept may be under "Needs testing". Why: retesting every edited skill made each
   release wait on dozens of runs, so fixes stopped reaching users.
3. Set the version. Its one home is `version` in `package.json`. Edit it, then run
   `python3 scripts/lint.py --write-plugin-manifests` so the Claude Code and Codex plugin
   manifests and the Claude Code marketplace carry the same version.
4. Add the release to `CHANGELOG.md`: move the `Unreleased` items under a new
   `## [MAJOR.MINOR.PATCH] - YYYY-MM-DD` heading, written for people who install the skills,
   and update the comparison links at the bottom.
   Then replace the old tag with the new one everywhere in the
   [Install section of the README](../../README.md#install), including "The newest release is",
   and the old version in the Pi pin example (`npm:agent-concepts@MAJOR.MINOR.PATCH`). The Pi
   install itself names no version.
5. Run `python3 scripts/release_check.py vMAJOR.MINOR.PATCH`. It exits nonzero when any
   description's version differs from the tag, `CHANGELOG.md` has no entry for it, or the
   README's Install section does not name the tag or still names another one, does not show
   the unpinned `pi install npm:agent-concepts`, or pins npm to another version. Run
   `python3 scripts/lint.py` too (0 ERROR).
6. Commit and push these changes, and wait for the `gate` run on that commit to be green.

## Tag and push

7. Tag the released commit: `git tag -a vMAJOR.MINOR.PATCH -m "vMAJOR.MINOR.PATCH"`.
8. Push the tag the way this machine's publish policy allows. Check it first with
   `python3 scripts/publish-check.py` as shown under "Externally owned authority" in
   `AGENTS.md`, and verify the matched rule's conditions yourself. Then
   `git push origin vMAJOR.MINOR.PATCH`.

## After the push

9. Watch the `release` workflow for the tag. It runs `release_check.py` for the tag, then
   installs the tag from GitHub with every method on Ubuntu and macOS
   (`python3 scripts/fresh_install_test.py --ref vMAJOR.MINOR.PATCH`), whose `pi-npm` method
   packs the tagged checkout with `npm pack`, checks the tarball and installs it in Pi. Then
   its `publish-npm` job publishes that version to npm on the `next` dist-tag (see
   [Publishing to npm](#publishing-to-npm)). `latest`, which `pi install npm:agent-concepts`
   and `npm install agent-concepts` follow, stays on the previous release. Last, its
   `github-release` job creates the tag's GitHub release with its `CHANGELOG.md` entry as the
   notes; GitHub's Releases page then labels it "Latest". If the job fails, create it by hand
   with `gh release create vMAJOR.MINOR.PATCH --verify-tag --notes-file <the entry>`.
10. If it fails, do not move the tag. Fix the problem on `master` and release the next patch
    version; someone may already have installed the broken tag. A version on npm cannot be
    replaced either.

## Soak on `next`, then promote

A new version reaches people who installed from npm only when `latest` moves to it. Why:
agents release without asking, and the Pi package loads the agent kernel into every session,
so a bad version on `latest` reaches every stranger at their next update.

11. Run the [stranger end-to-end test](../../scripts/stranger-end-to-end.md) against the
    version as published:
    `STRANGER_SOURCE=npm STRANGER_VERSION=MAJOR.MINOR.PATCH EVIDENCE=<new dir> MODEL=<provider/id> THINKING=<effort> scripts/stranger_end_to_end.sh`.
    It takes about 30 minutes; start it detached from the main checkout, not inside a
    worktree worker. Grade it from its evidence files as that page says, and record the
    result in the release audit.
12. If it passed, promote: `gh workflow run release.yml -f action=promote -f version=MAJOR.MINOR.PATCH`.
    This changes what strangers install, so check it with `publish-check.py` the way you
    checked the tag push (step 8). The `set-latest` job refuses a version that is not the one
    on `next`. Confirm with `npm view agent-concepts dist-tags` that `latest` is the new
    version.
13. If it failed, leave `latest` where it is. Fix the problem on `master` and release the
    next patch, which replaces this version on `next`. If anyone may have installed it from
    `next`, deprecate it as in [Withdraw a bad release](#withdraw-a-bad-release) step 2.

## Withdraw a bad release

Use this when `latest` points at a version that turns out to be broken. A version on npm
cannot be replaced, and npm allows unpublishing only in narrow cases (see
[npm's unpublish policy](https://docs.npmjs.com/policies/unpublish)), so a bad version is
withdrawn, not removed. Do the steps in this order:

1. Move `latest` back to the last good version:
   `gh workflow run release.yml -f action=rollback -f version=<good>`, checked with
   `publish-check.py` as in step 12. If the workflow cannot run, the maintainer runs
   `npm dist-tag add agent-concepts@<good> latest` while logged in to npm.
2. Deprecate the bad version, so every install of it prints a warning:
   `npm deprecate agent-concepts@<bad> "<what is wrong>; use <good>"`. Trusted publishing
   cannot run `npm deprecate`; it needs the maintainer's npm login and two-factor code, so
   an agent asks the maintainer to run it. An empty message (`""`) undoes it.
3. If the tag has a GitHub release, start its notes with
   `Withdrawn <date>: <what is wrong>; use v<good>.` (`gh release edit v<bad> --notes-file <file>`).
4. In `CHANGELOG.md`, add a line under the bad version's heading:
   `**Withdrawn** <date>: <what is wrong>; use [<good>].`
5. Fix the problem on `master` and release the next patch through the soak above.

Moving `latest` back does not downgrade anyone. Pi and npm update only to a higher version, so
people who already updated stay on the bad version until the fixed patch reaches `latest`. To
leave it sooner, they install the good version pinned
(`pi install npm:agent-concepts@<good>`) and go back to the unpinned install after the fix.

These steps were checked line by line against npm's documentation (trusted publishers,
`npm dist-tag`, `npm deprecate`, unpublish policy) on 2026-11-27 and have not been run
against the registry yet; the first real promotion is also the first run of `set-latest`.

## Publishing to npm

The release workflow publishes `package.json`'s version as `agent-concepts` through npm
trusted publishing: GitHub Actions proves the workflow's identity over OIDC, so no npm token is
stored anywhere. npm requires (per docs.npmjs.com/trusted-publishers) the `id-token: write`
permission, npm CLI 11.5.1 or later, Node 22.14.0 or later and a GitHub-hosted runner; the
workflow sets these. Provenance is attached with `--provenance` and needs the public repository
named in `package.json` `repository`. If this version is already on npm, the job prints a
notice and skips publishing instead of failing.

The same trusted publisher has **Allow npm dist-tag** turned on, so the `set-latest` job can
move `latest` without a token. npm's trusted-publishers page requires npm CLI 11.21.0 or later
for dist-tags over OIDC, and the job installs that. If npm still refuses, stop and ask the
maintainer; do not add a token.

A trusted publisher can only be connected to a package that exists, so the first release is
published by hand:

1. On the maintainer's machine, from a clean checkout of the tag: `npm login`, then
   `npm pack --dry-run` to review the file list (skill bodies, `packages/agent-kernel-pi/`,
   README, LICENSE, package.json, nothing else), then `npm publish --access public`.
2. On npmjs.com, open the package's Settings → Trusted publishing, choose GitHub Actions and
   enter this repository and the workflow file `release.yml`. npm expires a new trusted
   publisher that has not published within 2 days, so connect it shortly before the next
   release, or delete and recreate it if it expired.
3. Optional, recommended by npm: in the same settings, require two-factor authentication and
   disallow tokens, so only the workflow can publish.

The tag's `release` run for that first version finds it on npm and skips publishing; every
later tag publishes from the workflow.

## What the fresh-install test runs for a tag

The test builds its own install commands in Python (it does not read or run the README's
commands), using the pinned agent versions in `.github/workflows/release.yml`. For `npx skills`
it runs the all-skills command and one pack command from [install-packs.md](install-packs.md).
The README commands must be kept matching by hand; the test will not catch a drift between them.
The packed Pi install also checks that the kernel reaches Pi’s assembled system prompt without
a model request. A weekly and manually dispatchable `latest agents` workflow runs the same
install test on the latest CLI releases and opens or comments on one issue when it fails.

The test runs the update commands against the same tag. Moving an install from one tag to a
newer one has not been tested yet; until it is, the safe way is to uninstall and install again
with the new tag. For the unpinned npm Pi install, check by hand after a release that
`pi update --extensions` on an install of the previous version moves it to the new one
(plain `pi update` updates only Pi itself). Do that in a throwaway Pi home: set both `HOME` and `PI_CODING_AGENT_DIR` to a `mktemp -d` folder (for example `D=$(mktemp -d); HOME=$D PI_CODING_AGENT_DIR=$D/.pi/agent pi install npm:agent-concepts@<previous>`), because `PI_CODING_AGENT_DIR`, when set, wins over `HOME` and the install would land in your real Pi config.
