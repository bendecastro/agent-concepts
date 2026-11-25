# Agent vault read path: finish the live-vault rollout

Why: the cheap read path across `bc-setup-project` and `bc-wiki-maintain` is built and its benchmark is settled, but two rollout steps still only exist in this repository and have not reached the live vaults.
Done when: the batch promotion timer runs every listed vault in place of the per-vault promotion timers and unpromoted headings fall below 10; every live vault's `map.md` uses real Markdown links for in-vault targets.
Stage: done
Blocked by: nothing
Kind: feature
Source: docs/plans/active (migrated in 002-docs-reshape)

## Steps

Already done (see the plan record): W1 dropped after the W4 benchmark, W2/W5 closed by the write/read-contract successor (`015-agent-vault-write-read-contract`), W3 failure notification, ranked search as the first move in all eight vaults, the scaffold heading fix with loud lint, and the scaffold side of the `map.md` link repair.

- [ ] Enable the list-driven promotion timer (`bc-wiki-maintain-all.timer`) and disable the per-vault promotion timers it replaces in the same change, so no two agents promote one vault concurrently. On 2026-11-25 the batch timer was not installed and per-vault promotion timers were still active on the owner's main machine.
- [ ] Measure total unpromoted headings after the first batch runs (target: 68 → under 10).
- [ ] Migrate the `map.md` of each of the eight live vaults to real Markdown links for in-vault targets (rows pointing outside the vault stay inline code), and record the orphan counts before and after.
- [ ] Close the plan's open "does the scaffold's shape change too?" question in the plan record: W4 retired the summary convention and `kind` frontmatter as retrieval arguments and argued for leaving the taxonomy alone, so record "no shape change" unless the owner wants it for human readers.

## Design

The full plan is kept as research: [docs/research/2026-08-27-agent-vault-read-path/](../../docs/research/2026-08-27-agent-vault-read-path/README.md). It holds the problem measurements, resolved decisions, each W-item with its original specification, the W4 benchmark result (rank, not filter; no generated artifact), non-goals, the deferred list, open risks, and what would change the plan. Read its "Deferred" section items 2 and 4 before either rollout step: promotion reads its own vault list, a per-vault `timeout --kill-after` is required, and a timed-out vault fails closed until a human clears its dirty tree.

## Outcome

Closed 2026-11-25, reduced in scope by the owner. A relevance check found the rollout no longer fits: five of the eight listed projects now use the visible layout, where agents write findings straight into `work/` and `docs/` and promotion does not apply. Only three classic vaults remain (two learning vaults untouched since August, and one production vault with nothing to promote), holding 19 unpromoted headings, several of them empty scaffold headings.

- Promotion timers: the owner chose to remove both remaining per-vault promotion timers rather than install the batch timer. One served a visible-layout project, so it could never run; the other found nothing to promote and started no agent. Classic vaults can still be promoted by hand with `bc-wiki-maintain`. The daily lint timer stays.
- Measuring unpromoted headings and migrating `map.md` to Markdown links: dropped. Little value with three mostly dormant classic vaults, and visible-layout maps point outside the vault, so a blanket conversion would be wrong.
- Scaffold shape question: no further shape change is warranted for retrieval. The W4 benchmark showed ranked search does not need it; the visible layout for code, ops and hybrid projects is a separate later change (`bc-setup-project`), not a retrieval change.

