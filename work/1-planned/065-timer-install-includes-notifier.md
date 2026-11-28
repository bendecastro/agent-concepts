# The wiki timer install also installs the failure notifier

Why: every wiki runner service sets `OnFailure=bc-wiki-notify@%n.service`, but `bc-wiki-maintain`'s `INSTALL-TIMER.md` (the path setup step 10 loads) never installs the `bc-wiki-notify@.service` template; only `runner/README.md` does. A vault set up through setup gets a failure hook that points at a missing unit, so a failed promotion run is silent.
Done when: `INSTALL-TIMER.md` installs and verifies `bc-wiki-notify@.service` with the slug units (or points at the one recipe in `runner/README.md`), and a sandboxed install shows the template in the unit folder.
Stage: next
Blocked by: nothing
Kind: bug
Source: 060 review (2026-11-28)

## Steps

- [ ] Add the notifier template to the timer install and its verify step; check it in the timer pressure sandbox.

## Outcome

_To be filled when finished or dropped._
