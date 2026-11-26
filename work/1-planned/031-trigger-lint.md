# Lint: a skill that runs at a named moment needs a trigger

Why: Skills say they run "at project setup", "on first need" or "periodically" while no skill that owns that moment hands off to them; the setup-starter-items gap was found only by the owner thinking of it.
Done when: `scripts/lint.py` flags each moment phrase in a deployed body that has no matching `hands_off` or `loads` edge from the skill owning that moment in `concepts/relationships.json`, with an allow comment for deliberate exceptions; existing hits are fixed or allowed.
Stage: later
Blocked by: nothing
Kind: build
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state

## Steps

- [ ] Define the moment phrases and which skill owns each moment.
- [ ] Implement the check with a failing test first.
- [ ] Fix or allow the current hits.

## Outcome

