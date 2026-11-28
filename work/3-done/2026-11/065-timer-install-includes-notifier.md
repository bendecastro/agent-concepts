# The wiki timer install also installs the failure notifier

Why: every wiki runner service sets `OnFailure=bc-wiki-notify@%n.service`, but `bc-wiki-maintain`'s `INSTALL-TIMER.md` (the path setup step 10 loads) never installs the `bc-wiki-notify@.service` template; only `runner/README.md` does. A vault set up through setup gets a failure hook that points at a missing unit, so a failed promotion run is silent.
Done when: `INSTALL-TIMER.md` installs and verifies `bc-wiki-notify@.service` with the slug units (or points at the one recipe in `runner/README.md`), and a sandboxed install shows the template in the unit folder.
Stage: next
Blocked by: nothing
Kind: bug
Source: 060 review (2026-11-28)
Planned: bc-plan-to-pipeline 2026-11-28
Ready for agent: yes
Dependencies: none new

## Requirements

- Owner decision (2026-11-28, 1a): `INSTALL-TIMER.md` holds the full install, timer units and the `bc-wiki-notify@.service` template together, with its verify step covering the template; `runner/README.md` points to `INSTALL-TIMER.md` instead of keeping its own recipe (one home).
- Check: the timer pressure sandbox install shows the template in the unit folder and `systemd-analyze verify` (or the existing verify step) accepts the units.

## Steps

- [x] Move the notifier template install and its verify into `INSTALL-TIMER.md`; make `runner/README.md` point there.
- [x] Run the timer install in the pressure sandbox and record that the template is present.

## Outcome

Done 2026-11-28. `INSTALL-TIMER.md` now installs and verifies the `bc-wiki-notify@.service` template in its per-vault block, and `runner/README.md` links there instead of keeping its own notifier recipe. A scripted sandbox install (scratch HOME, systemctl shim) showed the byte-identical template beside the slug service and timer, and `systemd-analyze verify` accepted all three; the real unit folder was untouched. Two new tests in `test_wiki_maintain.py` (red first). Not done: `runner/README.md` still has its own commands for the lint-all and all-vault installs and unsuffixed unit names in its check/disable examples; the agent-confirm path was not exercised.
