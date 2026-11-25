# Tidy local clutter and make the gate green

Why: untracked local folders leak into lint, a duplicate deploy script lingers, and four existing check failures keep the new gate red.
Done when: `scripts/gate` passes on a clean checkout and in CI, and no local-only folder can show up as untracked.
Stage: now
Blocked by: nothing
Kind: build
Source: bc-init-agent
Planned: grilled with the owner 2026-11-25 (decisions in the bc-init-agent grill; summary below)

## Steps

- [ ] Add `.handoffs/`, `.hypothesis/` and `.gemini/` to `.gitignore`; keep `.agents/` tracked (project skills live there).
- [ ] Make `scripts/lint.py` skip git-ignored files (the three current lint errors come from an ignored handoff note).
- [ ] Remove `scripts/deploy-pi-skills.py` (byte-identical to `deploy-local-skills.py`) unless something still calls it by that name; update references.
- [ ] Fix the `test_vault_archetypes_output_is_byte_identical_to_base` cases (learning, knowledge) in `concepts/bc-init-agent/tests/test_visible_layout.py`: `.bc-agent/references/agent-skills.md` differs from the base output.
- [ ] Fix portability-check failure "no planned symlink points into the author's tree" (the `bc-agent-reflect` alias link).
- [ ] Fix portability-check failure "lint reports no errors on a fresh checkout" (`bc-autoresearch-loop: deployed:2026-06-21 but no deploy symlink exists`).
- [ ] `scripts/gate` green locally; CI run green after push.

## Outcome


