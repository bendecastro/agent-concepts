# Releasing

How a maintainer cuts a release of the public skills. People outside this repository install
tagged releases, never `master` ([decision 0002](../decisions/0002-tagged-releases-for-strangers.md)),
so a release is a deliberate step. Tags are `vMAJOR.MINOR.PATCH`.

## Before you tag

1. Pick the commit to release, normally the tip of `master`. Check that its `gate` workflow
   run is green, including both `fresh-install` jobs (Ubuntu and macOS).
2. Check that the pressure tests of every discipline skill changed since the last release
   held. Run `git diff --stat <last tag>..HEAD -- concepts/` to see what changed, then look
   each changed concept up in [status.md](../status.md): its `tested` date must be after the
   change, and it must not be under "Needs testing". Re-run any that are missing; see the Test
   operation in `AGENTS.md`.
3. Set the version. Its one home is `version` in `package.json`. Edit it, then run
   `python3 scripts/lint.py --write-plugin-manifests` so the Claude Code and Codex plugin
   manifests and the Claude Code marketplace carry the same version.
4. Add the release to `CHANGELOG.md`: move the `Unreleased` items under a new
   `## [MAJOR.MINOR.PATCH] - YYYY-MM-DD` heading, written for people who install the skills,
   and update the comparison links at the bottom.
5. Run `python3 scripts/release_check.py vMAJOR.MINOR.PATCH`. It exits nonzero when any
   description's version differs from the tag or `CHANGELOG.md` has no entry for it. Run
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
   (`python3 scripts/fresh_install_test.py --ref vMAJOR.MINOR.PATCH`).
10. If it fails, do not move the tag. Fix the problem on `master` and release the next patch
    version; someone may already have installed the broken tag.

## What the fresh-install test runs for a tag

The test runs each command in the [Install section of the README](../../README.md#install) in
an empty home folder, with the pinned agent versions in `.github/workflows/release.yml`. For
`npx skills` it runs the all-skills command and one pack command from
[install-packs.md](install-packs.md).

The test runs the update commands against the same tag. Moving an install from one tag to a
newer one has not been tested yet; until it is, the safe way is to uninstall and install again
with the new tag.
