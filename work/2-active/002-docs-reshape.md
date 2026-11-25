# Reshape docs/ and move plans into work/

Why: `docs/` mixes guides, a generated page, config templates, plans and undated research at one level.
Done when: `docs/` holds a README, `guides/`, `examples/`, dated research folders, `decisions/` and `design/`; `docs/plans/` is gone; lint finds no broken link.
Stage: next
Blocked by: 001-tidy-local-clutter
Kind: docs
Source: bc-init-agent
Planned: grilled with the owner 2026-11-25 (decisions in the bc-init-agent grill; summary below)

## Steps

- [x] Turn each of the 3 active plans in `docs/plans/active/` into a work item after checking what is still open (`agent-vault-read-path` may only need closing). Became `007-agent-vault-read-path` (two live-vault rollout steps still open; the 655-line plan moved to `docs/research/2026-08-27-agent-vault-read-path/`) and `008-bc-drain-issues-v3-review-economy` (only the real Gate B A/B is open; plan body kept in the item). `bc-drain-issues-gate-b-deterministic-trace` had every task done, so it was filed as done (`021`).
- [x] Move the 12 implemented plans unchanged into `work/3-done/<year>-<month>/` as numbered items, dated from git history; remove `docs/plans/`. Numbered 009–020 by the month each reached `implemented/` (2026-08 or 2026-11); the `Status:` line was dropped because work items must not carry one. `docs/plans/README.md` removed; `docs/README.md` points to `work/` instead.
- [x] Put the owner's research into `docs/research/<YYYY-MM-DD>-<topic>/` folders dated from first commit; `cross-provider-code-review.md` becomes its folder's README; `docs/research/raw/` stays where it is. Dated with `git log --diff-filter=A` (iso-24495-1 from its earliest name, 2026-08-17).
- [x] Move `bootstrap.md`, `harnesses.md`, `pipeline.md`, `pressure-test-harness.md` to `docs/guides/`; rewrite every link (about 38 files). `scripts/lint.py` no longer checks plan lifecycle folders and now checks inline `docs/guides/` and `docs/examples/` paths. `log.md` and captured evidence keep their historical paths.
- [x] Move the four `*.example.*` templates to `docs/examples/` (`policies/publish.example.yaml` stays); update lint and scripts that name them.
- [x] Write `docs/README.md` naming what each page and folder is for.
- [x] Lint and gate green. Lint 0 ERROR / 196 WARN before and after (identical list). Gate passed on tree dd51b28bc833594b3de51ff6336512a0b1b39618 (468 tests, portability PASS).

## Outcome


