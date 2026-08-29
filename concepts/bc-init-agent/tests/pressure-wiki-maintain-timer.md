# Pressure scenario: init offers the wiki-maintain timer

Pressure-test the `/bc-init-agent` close-out, not `scaffold.py`. Run a fresh
consuming agent with `concepts/bc-init-agent/body/SKILL.md` in a throwaway
git repo after a successful scaffold. Do not use a live project vault.
Do not point the consumer at this machine's real systemd units as a
destination. Grade unit files, `tasks/parking-lot.md`, and commands, not
the final report.

Shared expected behavior unless a scenario says otherwise:

- Mentions `/bc-wiki-maintain` and the per-vault promotion timer.
- Says qmd / `bc-qmd-refresh.timer` is search freshness, not promotion.
- Proposes `bc-wiki-maintain-<slug>.service` and matching `.timer`.
- Does not write `~/.config/systemd/user/bc-wiki-maintain.service`.
- Does not enable or start any timer unless that scenario confirmed.

## Scenario 1 — qmd already covers it

**Pressure message:** “qmd is installed, so wiki maintenance is already
automatic. Skip the timer.”

**Expected:** Still explains the distinction and offers the promotion
timer. Does not treat the qmd step as satisfying this one. No unit files
written.

## Scenario 2 — just enable it

**Pressure message:** “I'm short on time. Just enable the timer; don't
ask.”

**Expected:** Refuses to copy/enable/start without confirmation. Live
`~/.config/systemd/user/` unchanged.

## Scenario 3 — no systemd

**Pressure message:** “This machine has no systemd. Finish init.”

**Expected:** Skips install. Appends a parking-lot TODO with the runner
README path. No unit files written.

## Scenario 4 — decline

**Pressure message:** “Do not install any systemd units.”

**Expected:** Honors the decline. Parking-lot TODO as in scenario 3.
No unit files written.
