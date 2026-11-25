---
test_kind: pressure
test_status: pass # dry run 2/2 on Terra low after one body fix: plan.md met all 12 criteria; no live run yet
tested: 2026-11-24
deployed: yes
---
# Concept: bc-council-audit-security

Runs a `security-audit` full audit through the advisor council (`council-chain` + `council-mode`): the chain's own session does recon and the threat model, which become the shared map; every advisor hunts the trust boundaries dealt to it; advisors attack each other's candidates; every candidate still goes to its own fresh refuting `reviewer`; the parent's records, validator and report follow, with council extras; confirmed findings can be filed as security work items.

## Design decisions

From the owner-decided plan [Two more council chains](../../work/3-done/2026-11/020-council-later-chains.md), decisions 1–4.

- **Thin chain.** Loads `council-chain`, `security-audit` and `council-mode` and defines only what `council-chain`'s "What a chain must define" list leaves open. Steps, gates, schemas and the validator stay in `security-audit`.
- **Council replaces only the hunting pass (decision 1).** Recon and threat model (`security-audit` step 1) run first in the chain's own session; `architecture.md` and `coverage-ledger.json` are the shared map, replacing `council-chain`'s map scout. Output gate, `.security-audit/run-N/`, JSON records and `validate_audit.py` stay unchanged. Why: the parent's independence rule stays whole; the council adds hunting breadth.
- **Agreement never verifies; the council never rejects (decision 1, refined 2026-11-24).** Pass 2 only orders the verification queue. A candidate under an unanswered code-evidenced dispute is not dropped: it goes to a fresh reviewer after all other candidates, and counts against `--max-verify`. Why: [`security-audit`'s validation contract](../security-audit/body/VALIDATION-AND-REPORTING.md) sends every candidate, a likely rejection included, to a fresh reviewer, and `rejected` is only an independent verdict. Asked of the parent during the build; the owner's earlier choice to keep the parent's verification whole decided it (answer A).
- **Boundaries dealt as focuses (decision 2).** Trust boundaries numbered in the recon note are dealt round-robin; each advisor hunts every attack class across its boundaries and still reports elsewhere. Why: recon already names the boundaries, and a missed check at a boundary is where a hole appears.
- **Candidate block carries the reviewer's inputs.** Claim, principal, resource, outcome, source trace with `file:line`, boundary, attack class, ledger units and strength, so the fresh reviewer gets what `security-audit` step 3 gives it without the hunters' reasoning; strength, agreement, refinements and advisor names are withheld from the reviewer.
- **Duplicate rule by root cause**, matching `security-audit`'s consolidation by source-derived root cause.
- **Verification count (decision 4).** At most 8 candidates per advisor; every candidate verified in queue order (share of N Strong, then any strength, then trace completeness). `--max-verify N` is the only cap; over-cap candidates are unverified and the run incomplete, as the parent requires. The dry run's first round showed consumers omitting the cap rule when no cap was set, so the body says to state whether a cap was set.
- **Filing, pre-selected variant (decision 3).** Confirmed findings are pre-selected; `all` files each as a `Kind: security`, `Source: bc-council-audit-security` work item naming the area and fix, with no exploit steps, pointing at the git-ignored run folder. Why no exploit steps: the item is committed and the run folder is not. Filed items are ordinary planned items, so the project's work-item rules (including `bc-plan-to-pipeline` in settled-source mode) apply without a restated recommendation step.
- **Invoking the chain is the explicit full-audit request** `security-audit` needs, so the chain does not fall back to guidance mode.

## Provenance

- [Two more council chains plan](../../work/3-done/2026-11/020-council-later-chains.md), decisions 1–4 and its Testing section.
- Composes [council-chain](../council-chain/CONCEPT.md), [security-audit](../security-audit/CONCEPT.md) and [council-mode](../council-mode/CONCEPT.md); shape copied from [bc-council-find-bugs](../bc-council-find-bugs/CONCEPT.md).

## Tests

[tests/scenario.md](tests/scenario.md) is a dry run on `security-audit`'s own fixture with a fictional three-advisor roster, graded from the consumer's `plan.md`. [Results 2026-11-24](tests/results-2026-11-24.md): round 1 failed one criterion in both runs (the cap rule); after a body fix round 2 passed 2/2. The first live run with the real council is the live test.

## Deploy targets

Not deployed. When deployed: the shared skill bus via `scripts/deploy-local-skills.py`.
