# Seed starter work items when setting up an existing codebase

Why: on an existing codebase `bc-setup-project` creates `docs/design/README.md` and `docs/guardrails/README.md` with empty lists and only names follow-up skills in its close-out, so nothing records the app's existing design, nothing adds the stack checks that `bc-performance-guardrails` § Setup checks says belong "at project setup", and `work/` starts empty on the owner's dashboard.
Done when: setting up an existing code, ops or hybrid project proposes, in the init plan, only the starter items its recon shows apply (design inventory only with a UI or CLI surface, guardrails setup checks, architecture review for a codebase big enough to need one, issue triage only when issues exist); the owner can untick any; the accepted ones land in `work/1-planned/` and `work/order.md`, and the change has held under a pressure test.
Stage: next
Blocked by: nothing
Kind: feature
Source: owner conversation about post-setup onboarding, 2026-11-26

## Steps

- [x] Settled by the owner (2026-11-26): setup seeds items and does not run the audits itself; items are proposed in the init plan and the owner unticks what they do not want; only items that apply are proposed (no UI, no design item).
- [ ] Define the applicability signal for each starter item from recon (UI or CLI surface, codebase size, open GitHub issues) and what each item's `Done when:` says.
- [ ] Guardrails item: measure first and ratchet at today's value; improvements become follow-up items (`bc-optimize-code`), not part of setup.
- [ ] Update `bc-setup-project` (init-plan step and close-out), add the `hands_off` edges to `bc-performance-guardrails`, `bc-ui-design`, `bc-improve-codebase-architecture` and `bc-triage` in `concepts/relationships.json`, and regenerate the views.
- [ ] Make `bc-performance-guardrails` § Setup checks and `bc-ui-design` agree with the new hand-off.
- [ ] Pressure test: an existing repo without a UI gets no design item; one with a UI gets it; the agent does not run the audits during setup when told to hurry.
- [ ] Lint and gate green; update `index.md` and `.bc-agent/log.md`.

## Outcome

