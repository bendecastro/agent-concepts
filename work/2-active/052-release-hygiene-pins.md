# Release checks prove privacy and the publish job has fixed inputs

Why: The personal-terms lint returns silently when the private list is missing, so a release cut on a machine without it proves nothing about privacy; and the job holding `id-token: write` installs `npm@>=11.5.1` and uses actions by moving tag.
Done when: The release check fails when the personal-terms list is missing (with an explicit opt-out for CI and strangers), and the `publish-npm` job pins npm to an exact version and its actions by commit SHA.
Stage: now
Blocked by: nothing
Kind: security
Source: blind-spot council, owner decisions 2026-11-27 (4a: finding G)
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Steps

- [x] Make a missing personal-terms list an error in the release path (not in plain lint for strangers), and pin the publish job's npm and actions. Done when `release_check.py` fails with the list absent and passes with it, and `release.yml`'s publish job has no version range or moving action tag. Out of scope: pinning every workflow's actions.

## Outcome

Release checks require the private list and fail on scan issues unless explicitly opted out; CI opts out. The npm publishing job pins its actions and npm, and promotion uses the same exact npm version. Targeted regression tests cover the release scan and publishing inputs.

The release check scans the staged snapshot read from git, not the working copy: symlinks are scanned as their stored text, submodule links are skipped, and a tracked file that differs from the staged snapshot is an error, so the scan covers what the release commit takes. Two reviews blocked; the owner chose on 2026-11-28 to bind the scan to the snapshot and finish without a third full review.

Accepted gap (owner, 2026-11-28): the publish-pin test reads `uses:` lines and `npm install` text, so a quoted `"uses":` key or the `npm i` alias would slip past it. Catching those means parsing the workflow's YAML; it guards our own workflow against deliberate evasion of our own check, so it is left for a later item if it ever matters.
