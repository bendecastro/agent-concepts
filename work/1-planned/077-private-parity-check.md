# Each minor release re-checks what is private only, and the stranger test covers a review loop

Why: the owner's sessions always load the private layer, so the owner cannot see a stranger's experience; the review stop rule and the items filed with this one were private for weeks unnoticed. The stranger end-to-end test covers setup, planning and build, but never a review loop or a wait. Evidence: the run folder `2026-11-28-private-to-public` (rules, pi-ext and concepts reports).
Stage: next
Blocked by: 068-replan-protocol
Kind: tests
Source: private-to-public audit 2026-11-28 (owner rec)
Dependencies: none new

## Requirements (not planned yet: run bc-plan-to-pipeline)

- `docs/guides/releasing.md`: before each minor release, rerun the private-versus-public comparison (owner's private rules, extensions, roles, overlays and helper tools against the public bodies) and file each gap; the comparison's recipe lives in the guide, the owner's paths in a private overlay.
- The stranger test gains one scenario where a review blocks twice on new sequences, graded on the replan behaviour from `068-replan-protocol`.
