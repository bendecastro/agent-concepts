# Build pipeline works on any default branch

Why: `concepts/bc-pipeline-to-done/body/SKILL.md` requires the target repo to be "on `master`" and "pushes `HEAD:master`", so a repository on `main` cannot pass preflight.
Done when: `bc-pipeline-to-done` detects the repository's default branch in preflight and uses it for the policy check, claims, fetch and landing; no `master` literal remains in its body except as an example.
Stage: next
Blocked by: nothing
Kind: bug
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state

## Steps

- [ ] Find every `master` assumption in `bc-pipeline-to-done` and the skills it hands to (claims, landing, publish check).
- [ ] Detect the default branch (remote HEAD, else current branch with owner confirmation) and use it everywhere.
- [ ] Pressure or fixture check on a `main` repository; lint and gate green.

## Outcome

