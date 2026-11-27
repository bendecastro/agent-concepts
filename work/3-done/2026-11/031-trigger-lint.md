# Lint: a skill that runs at a named moment needs a trigger

Why: Skills say they run "at project setup", "on first need" or "periodically" while no skill that owns that moment hands off to them; the setup-starter-items gap was found only by the owner thinking of it.
Done when: `scripts/lint.py` reports each moment phrase in a deployed body that has no matching edge in `concepts/relationships.json` from the skill owning that moment, with an allow comment for deliberate exceptions; current hits are fixed or allowed.
Stage: now
Blocked by: nothing
Kind: build
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state
Planned: bc-plan-to-pipeline 2026-11-26
Ready for agent: yes

## Requirements

- A small table in `scripts/lint.py` maps moment phrases to the skill that owns the moment ("at project setup" → `bc-setup-project`, "when planning" → `bc-plan-to-pipeline`, "during a drain" → `bc-pipeline-to-done`, and so on); the check looks for a `hands_off` or `loads` edge from that owner to the skill whose body has the phrase.
- An exception is a `trigger-allow: <reason>` comment on the line.
- Severity: WARN for one release, then ERROR (the change log entry says when).
- Test seam: lint tests in `scripts/tests/` on fixture concept folders, watched failing first.
- Out of scope: phrases with no owning skill (reported as unknown moments for a human).

## Steps

- [x] Implement the check with fixture tests, fix or allow the current hits, update `.bc-agent/log.md`. Blocked by: nothing. Done when the tests pass after failing first and `python3 scripts/lint.py` shows no unallowed trigger warning. Out of scope: turning the warning into an error.
  - Review: approved by tier-1 2026-11-27
  - Gate: pass ./scripts/gate at 4b05ddf 2026-11-27
  - Landed in `4b05ddf`.

## Outcome

Landed in `4b05ddf`: `scripts/lint.py` maps six moment phrases to their owning skills and warns when a deployed body uses one without a `hands_off` or `loads` edge from the owner; a `trigger-allow:` comment exempts a line. WARN now, ERROR from the second tagged `CHANGELOG.md` version. 13 new fixture and property tests, watched failing first. The three current hits (brainstorming, setup and writing-plans phrases naming planning) were not real handoffs and carry allow comments. Phrases with no owning skill get no warning; found: `bc-setup-project` "on first need" and `bc-teach` "Periodically". Full gate 626 passed, 4 skipped.

Spent: 23m active, 6.5M tokens, $4.20 (estimated; pi 5 sessions, claude-code 0 sessions, codex 0 sessions; other tools not counted)

