# Ship the rules that only live in the owner's setup

Why: Behaviours strangers need live only in the owner's own instructions: carry-on puts unfinished active work first only in the owner's file, away-mode questions point at the owner's dashboard, and drain fixes for performance regressions do not load `bc-performance-guardrails`.
Done when: The generated work rules carry the active-first carry-on order and fall back to `Waiting on owner:` lines for questions; the drain loads `bc-performance-guardrails` for regression fixes; requirements in [requirements.md](requirements.md).
Stage: now
Blocked by: nothing
Kind: feature
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state
Planned: bc-plan-to-pipeline 2026-11-26
Ready for agent: yes
Held by: pi 01a218e4 since 2026-11-26 22:54 +00:00

## Steps

- [x] Carry-on order and question fallback: generated work rules in `scaffold.py` and the reworded "where the owner sees questions" references; scaffold test asserting the carry-on text (watched failing first); two pressure scenarios. Blocked by: nothing. Stories 2, 3. Done when the test and both with-change scenarios pass while the baselines do not. Out of scope: kernel install, guardrails.
  - Review: approved by tier-1 2026-11-26 (round 2)
  - Gate: pass ./scripts/gate at 34c6f8e 2026-11-26
  - Landed in `34c6f8e`.
- [ ] Regression fixes load guardrails: `bc-pipeline-to-done` packet and review contract; RELATIONSHIPS edge `loads` to `bc-performance-guardrails` regenerated; pressure scenario. Blocked by: nothing. Story 4. Done when the with-change run adds a check and the baseline does not. Out of scope: other worker packets. CONCEPT status, `index.md`, `.bc-agent/log.md` updated; lint has 0 ERROR and the gate passes.

## Outcome

