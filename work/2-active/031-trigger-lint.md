# Lint: a skill that runs at a named moment needs a trigger

Why: Skills say they run "at project setup", "on first need" or "periodically" while no skill that owns that moment hands off to them; the setup-starter-items gap was found only by the owner thinking of it.
Done when: `scripts/lint.py` reports each moment phrase in a deployed body that has no matching edge in `concepts/relationships.json` from the skill owning that moment, with an allow comment for deliberate exceptions; current hits are fixed or allowed.
Stage: now
Blocked by: nothing
Kind: build
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state
Planned: bc-plan-to-pipeline 2026-11-26
Ready for agent: yes
Held by: pi 01a218e4 since 2026-11-27 02:39 +00:00

## Requirements

- A small table in `scripts/lint.py` maps moment phrases to the skill that owns the moment ("at project setup" → `bc-setup-project`, "when planning" → `bc-plan-to-pipeline`, "during a drain" → `bc-pipeline-to-done`, and so on); the check looks for a `hands_off` or `loads` edge from that owner to the skill whose body has the phrase.
- An exception is a `trigger-allow: <reason>` comment on the line.
- Severity: WARN for one release, then ERROR (the change log entry says when).
- Test seam: lint tests in `scripts/tests/` on fixture concept folders, watched failing first.
- Out of scope: phrases with no owning skill (reported as unknown moments for a human).

## Steps

- [ ] Implement the check with fixture tests, fix or allow the current hits, update `.bc-agent/log.md`. Blocked by: nothing. Done when the tests pass after failing first and `python3 scripts/lint.py` shows no unallowed trigger warning. Out of scope: turning the warning into an error.

## Outcome

