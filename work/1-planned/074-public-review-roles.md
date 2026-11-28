# The review loop's roles and their limits are public

Why: the owner's review loops use private roles: `re-reviewer` (the first re-review covers the whole change plus fixes), `post-review-patcher` (fixes only cited findings, asks before redesign), `fix-verifier` (fix-only checks, only after a full re-review), plus `routine-worker` and `locator`. Public ships only the three pipeline roles and a narrower re-review, so a stranger's review loops behave differently from the owner's. Evidence: the run folder `2026-11-28-private-to-public` (rules, pi-ext and concepts reports).
Stage: next
Blocked by: 068-replan-protocol
Kind: feature
Source: private-to-public audit 2026-11-28 (owner rec)
Dependencies: none new

## Requirements (not planned yet: run bc-plan-to-pipeline)

- Decide, with evidence, whether the first re-review covers the whole change (private) or the changed hunks (public pipeline); the two conflict on purpose today.
- Port the patcher's escalation boundary and the fix-verifier's later-rounds-only limit as contracts in `bc-code-review` or the pipeline rework contract, and ship role profiles if the package should provide them.
- Blocked by `068-replan-protocol` because both edit the review-loop home.
