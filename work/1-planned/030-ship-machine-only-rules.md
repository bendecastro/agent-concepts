# Ship the rules that only live in the owner's setup

Why: Several behaviours strangers need live only in the owner's own instructions: the agent kernel is a manual copy step (so "workers never run the full suite" is easy to miss), carry-on puts unfinished active work first only in the owner's file, away-mode questions go to the owner's dashboard with no portable place, and drain fixes for performance regressions do not load `bc-performance-guardrails`.
Done when: Setup checks whether the agent kernel is loaded and offers to install it; the generated work rules carry the active-first carry-on order and a portable place for owner questions; the drain loads `bc-performance-guardrails` for regression fixes.
Stage: later
Blocked by: nothing
Kind: feature
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state

## Steps

- [ ] Setup: detect the kernel in the harness's always-on instructions and offer the install step.
- [ ] Generated work rules: active-first carry-on and a live-holder check.
- [ ] A portable owner-question location in the scaffold, with private dashboards as an optional adapter.
- [ ] Drain: regression packets load `bc-performance-guardrails` and must add the check.
- [ ] Pressure tests for the reworded discipline parts; lint and gate green.

## Outcome

