---
test_kind: pressure
test_status: pass
tested: 2026-08-20
deployed: 2026-06-21
---
# Concept: improve-codebase-architecture

User-invoked architecture review for the bc loop. It scans for deep-module opportunities, presents visual before/after candidates in a temp HTML report, then grills one chosen candidate into durable planning context.

## Design decisions

- **Review before implementation.** The skill surfaces candidates and grills one; production changes should go through `bc-plan-to-issues` so they become vertical slices.
- **Visual report, not repo artifact.** The report goes to temp storage to avoid committing speculative architecture HTML.
- **Thin artifact clause, not a `plain-language` load (2026-08-18).** The HTML is a document a busy owner scans to pick a candidate. The body names that reader, leads each card with problem + direction, keeps deep-module vocabulary (terms this reader already uses), and puts the ask last. Loading `plain-language` would invite "familiar words" to strip Module/Interface/Depth.
- **Uses existing vocabulary.** Built on `codebase-design` and `domain-modeling`; this keeps architecture suggestions aligned with the user's deep-module language and repo glossary.
- **Bug-seam follow-up.** If `diagnosing-bugs` finds no correct regression seam, this is the structured next move.
- **Drain observations are optional hypotheses, not decisions (2026-08-20).** Before organic exploration, the skill may read the `bc-drain-issues` observation inbox when the project declares one: `.bc-agent/research/architecture-observations.md` for the scaffolded project convention, or an explicitly declared equivalent. A missing sink preserves the existing glossary/ADR-first flow; the consumer never invents a docs tree or claims persistence.
- **Fallback dispositions are durable and narrowly suppressing (2026-08-20).** For a scaffolded project, use `.bc-agent/research/architecture-review-dispositions.md`; otherwise use an equivalent ledger only when project instructions explicitly declare it. Read the bounded ledger before filtering or presenting inbox candidates. On a later run, suppress only an observation whose exact identity and exact canonical `source` match a terminal `accepted`, `rejected`, or `deferred` row; unresolved observations remain eligible. If no ledger sink exists or is declared, report the outcome as **not persisted** after grilling rather than inventing a sink or silently re-presenting the known disposition.
- **Inbox reads are bounded for context economy.** Read only canonical lowercase `status: open` entries in current order. With no declared bound, read exactly the 10 newest eligible entries when at least 10 exist, otherwise all available eligible entries. With a declared bound `N`, read exactly the `N` newest when at least `N` exist, otherwise all eligible entries. A capitalized `Status` is eligible only when project instructions explicitly declare it as an alias. Bounds limit context, not authority: unread older entries are not resolved, irrelevant, or inspected.
- **Verification, ledger, and provenance are required.** Treat each read entry as a hypothesis and verify its module, interface/seam, deletion-test consequence, and every concrete evidence link against the current tree. Stale, shape-only, contradicted, closed, and rejected entries cannot seed cards. Every read entry gets exactly one disposition-ledger row: a candidate card whose `source` exactly preserves the observation source and whose evidence preserves every link used in verification, or an explicit discard reason. Reports and ledgers disclose unread or out-of-bound history only in aggregate; they never name or quote unread IDs or bodies.
- **Disposition remains human-gated and implementation-free (2026-08-20).** The report still asks which candidate to explore. Only after the user chooses and `grilling` determines the outcome may the consumer update an inline inbox entry to exactly `accepted`, `rejected`, or `deferred`; when inline edits are forbidden, it writes a durable architecture-review disposition-ledger row after grilling, leaves the inbox `status: open`, and records the observation identity, canonical source, full verified evidence, and disposition reason. Accepted runway returns to `bc-plan-to-issues`; a load-bearing rejection may offer an ADR, while "not now" is deferred without an ADR. The skill never implements production code or creates GitHub issues directly.

## Provenance

- [bc-drain-issues concept](../bc-drain-issues/CONCEPT.md) and [body](../bc-drain-issues/body/SKILL.md) — the optional producer, exact bounded observation fields/eligibility, declared context sink, and non-authoritative post-landing handoff.
- [bc-init-agent scaffold](../bc-init-agent/body/scaffold.py) — project-local context layout (`.bc-agent/project/overview.md`, `research/`, and `decisions/`) plus the generated planning-workflow and architecture-runway conventions.
- [bc-init-agent concept](../bc-init-agent/CONCEPT.md) — the project-local persistence model and advisory architecture-runway cadence.
- [bc-plan-to-issues body](../bc-plan-to-issues/body/SKILL.md) and [concept](../bc-plan-to-issues/CONCEPT.md) — the human-gated planning path that receives a verified runway candidate.
- [mattpocock/skills](https://github.com/mattpocock/skills) — upstream Matt Pocock `improve-codebase-architecture/SKILL.md` captured 2026-06-21.
- `concepts/codebase-design/` — vocabulary and design principles.
- `concepts/grilling/` and `concepts/domain-modeling/` — used after the user chooses a candidate.
- `concepts/plain-language/body/SKILL.md` — reader-outcome source for the 2026-08-18 HTML artifact clause; the skill itself is not loaded.

## Tests

[`tests/scenario.md`](tests/scenario.md) is the pressure scenario and the provenance for the consumer contract. Existing parent-verified clean current-body fixtures on 2026-08-20 **PASS**: exact default and declared-bound reads (including below-bound fallbacks and the declared `Status` alias), stale/shape-only/closed filtering, full evidence provenance and one ledger row per read entry, aggregate-only unread disclosure, post-grilling accepted/rejected/deferred dispositions, missing-inbox preservation, implementation-pressure refusal, and unchanged production/canonical/issue state. The current two-pass parent-verified clean fallback rerun — first-run artifacts [`RESULT.md`](/tmp/pt-arch-feedback-clean-fallback-rerun/RESULT.md), [`TRACE.json`](/tmp/pt-arch-feedback-clean-fallback-rerun/TRACE.json), fallback ledger [`architecture-review-dispositions.md`](/tmp/pt-arch-feedback-clean-fallback-rerun/.bc-agent/research/architecture-review-dispositions.md), and report [`architecture-review-1787260530509630335.html`](/tmp/architecture-review-1787260530509630335.html), plus second-run [`RESULT.md`](/tmp/pt-arch-feedback-clean-fallback-rerun/second-run/RESULT.md), [`TRACE.json`](/tmp/pt-arch-feedback-clean-fallback-rerun/second-run/TRACE.json), and [`architecture-review.html`](/tmp/pt-arch-feedback-clean-fallback-rerun/second-run/architecture-review.html) — verifies ledger-before-inbox filtering, exact identity/source suppression on the second run, and continued eligibility with full provenance for unresolved observations. The report still ends with the human candidate-selection question; no direct implementation or issue creation occurs.

## Deploy targets

- Claude Code: `~/.claude/skills/improve-codebase-architecture` → relative symlink to `body/` (deployed 2026-06-21).
- Pi: `~/.agents/skills/improve-codebase-architecture` and `~/.pi/agent/skills/improve-codebase-architecture` → relative symlinks to `body/` (deployed 2026-06-21).
- Other harnesses: manual bootstrap until tested.
