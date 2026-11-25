# Tidy local clutter and make the gate green

Why: untracked local folders leak into lint, a duplicate deploy script lingers, and four existing check failures keep the new gate red.
Done when: `scripts/gate` passes on a clean checkout and in CI, and no local-only folder can show up as untracked.
Stage: now
Blocked by: nothing
Kind: build
Source: bc-init-agent
Planned: grilled with the owner 2026-11-25 (decisions in the bc-init-agent grill; summary below)

## Steps

- [x] Add `.handoffs/`, `.hypothesis/` and `.gemini/` to `.gitignore`; keep `.agents/` tracked (project skills live there).
- [x] Make `scripts/lint.py` skip git-ignored files (the three current lint errors come from an ignored handoff note).
  Note: link and inline-path checks ask `git check-ignore`; outside a git checkout every file is still scanned. Test: `scripts/tests/test_lint_ignored_files.py`.
- [x] Remove the duplicate `deploy-pi-skills.py` script (byte-identical to `scripts/deploy-local-skills.py`) unless something still calls it by that name; update references.
  Note: nothing in the repository (outside log history) or in the local Pi, Claude or config folders called it, and no symlink pointed at it, so it is removed.
- [x] Fix the `test_vault_archetypes_output_is_byte_identical_to_base` cases (learning, knowledge) in `concepts/bc-init-agent/tests/test_visible_layout.py`: `.bc-agent/references/agent-skills.md` differs from the base output.
  Note: the test's expectation was stale, not the scaffold. The base output is rebuilt from an older `scaffold.py` with renames rewritten; the deliberate `issue-slicing` to `plan-slicing` rename (2026-11-24) was never added to that rewrite. The test now applies it too.
- [x] Fix portability-check failure "no planned symlink points into the author's tree" (the `bc-agent-reflect` alias link).
  Note: the check was wrong. It searched the whole planned line, including the link path under the scratch HOME, and the scratch folder sits inside the author's home when TMPDIR does. The alias was only first alphabetically; every line matched. It now checks only the link target.
- [x] Fix portability-check failure "lint reports no errors on a fresh checkout" (`bc-autoresearch-loop: deployed:2026-06-21 but no deploy symlink exists`).
  Note: the lint check was wrong, not the data. Every deployed concept fails in a fresh HOME (only the first was shown), because `deployed:` records the owner's deployment. Lint now compares it with symlinks only when the home has deployed at least one concept.
- [x] `scripts/gate` green locally; CI run green after push.
  Note: CI first failed on three PromotionAll tests (a test stub's indented shebang ran under dash) and on uutils `timeout`; fixed, and the workflow now clones full history so no test skips.

## Outcome

Done. Gate green locally (468 passed, tree 73371676) and in GitHub CI (468 passed, 0 skipped). `run-promotion-all.sh` now requires GNU `timeout`; a portable process-group kill is an idea in `work/0-ideas.md`.


