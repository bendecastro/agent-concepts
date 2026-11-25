# Reshape docs/ and move plans into work/

Why: `docs/` mixes guides, a generated page, config templates, plans and undated research at one level.
Done when: `docs/` holds a README, `guides/`, `examples/`, dated research folders, `decisions/` and `design/`; `docs/plans/` is gone; lint finds no broken link.
Stage: next
Blocked by: 001-tidy-local-clutter
Kind: docs
Source: bc-init-agent
Planned: grilled with the owner 2026-11-25 (decisions in the bc-init-agent grill; summary below)

## Steps

- [ ] Turn each of the 3 active plans in `docs/plans/active/` into a work item after checking what is still open (`agent-vault-read-path` may only need closing).
- [ ] Move the 12 implemented plans unchanged into `work/3-done/<year>-<month>/` as numbered items, dated from git history; remove `docs/plans/`.
- [ ] Put the owner's research into `docs/research/<YYYY-MM-DD>-<topic>/` folders dated from first commit; `cross-provider-code-review.md` becomes its folder's README; `docs/research/raw/` stays where it is.
- [ ] Move `bootstrap.md`, `harnesses.md`, `pipeline.md`, `pressure-test-harness.md` to `docs/guides/`; rewrite every link (about 38 files).
- [ ] Move the four `*.example.*` templates to `docs/examples/` (`policies/publish.example.yaml` stays); update lint and scripts that name them.
- [ ] Write `docs/README.md` naming what each page and folder is for.
- [ ] Lint and gate green.

## Outcome


