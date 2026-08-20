---
name: improve-codebase-architecture
description: Scan a codebase for deep-module opportunities, present a visual temp-file report, then grill through one chosen refactor candidate for the bc planning loop.
disable-model-invocation: true
argument-hint: "[area/folder/problem]"
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deeper, more testable, more agent-navigable modules. This is a planning/review tool, not an implementation sprint.

Use `codebase-design` vocabulary exactly: **module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**. Use domain names from `.bc-agent/project/overview.md` or `CONTEXT.md`; respect ADRs.

## 1. Explore

At the beginning of Explore, locate the project's architecture-observation inbox and, when inline inbox edits are forbidden, its durable fallback disposition ledger:

- For a project scaffolded by `bc-init-agent`, use `.bc-agent/research/architecture-observations.md` for the inbox and `.bc-agent/research/architecture-review-dispositions.md` for the ledger.
- Otherwise use equivalent paths only when project instructions explicitly declare each path. An inbox declaration does not implicitly declare a fallback ledger. If no inbox sink exists or is declared, preserve the existing flow; do not invent a docs tree or claim that observations will be persisted. If inline edits are forbidden and no ledger sink exists or is declared, report the disposition as **not persisted** after grilling; if a later run encounters that known disposition, state the non-persistence instead of silently re-presenting it as a candidate.

Before organic exploration or presenting inbox candidates, read the bounded fallback disposition-ledger entries first when a ledger sink exists or is declared. Match a ledger row only when both the exact observation identity and exact canonical `source` value match, and only `accepted`, `rejected`, or `deferred` are terminal dispositions. Suppress that exact terminal match before inbox candidate presentation and before current-tree verification or report disposition-ledger processing. A suppressed terminal match intentionally receives no current-run verification, candidate card, or report disposition-ledger row; it is already resolved by the matching ledger entry. Read the ledger metadata needed to filter the bounded inbox set without disclosing unread IDs or bodies. Do not suppress an observation merely because it was read; an open entry with no matching terminal ledger row remains eligible on a later run.

Then, before organic exploration, read only entries eligible under the producer's canonical lowercase `status: open` marker from that inbox alongside the project glossary and ADRs. A capitalized `Status` is eligible only when project instructions explicitly declare it as a syntax alias for the canonical lowercase field. Preserve the inbox's current order (newest first). If project instructions declare an eligible-entry read bound `N`, read exactly the `N` newest eligible entries when at least `N` exist, otherwise read all eligible entries. With no declared bound, read exactly the 10 newest canonical lowercase `status: open` entries when at least 10 exist, otherwise read all available canonical lowercase `status: open` entries. Do not scan older history beyond that set. These bounds are for context economy, not correctness authority: unread older entries are not thereby resolved or irrelevant. Treat each non-suppressed eligible inbox entry actually processed as a hypothesis, not a decision, and verify its named **module**, **interface**/**seam**, deletion-test consequence, and every concrete evidence link declared in the observation and used in verification against the current code/tree. Do not present stale, closed/rejected, shape-only, or contradicted entries as candidates. For each non-suppressed eligible inbox entry actually processed, emit exactly one candidate/discard row: either a candidate card whose `source` exactly carries the entry's source value (the observation identity) and whose evidence carries every concrete evidence link declared in the observation and used in verification, or an explicit discard reason. A missing or unverified link invalidates a candidate card: discard it with an explicit reason rather than silently omitting the link. Shape-only, stale, closed/rejected, and contradicted entries must be discarded and cannot seed cards. Never copy an old recommendation into a decision.

Then explore organically for friction:

- Understanding one concept requires bouncing across many files.
- A module's interface is almost as complex as its implementation.
- Helpers were extracted for testability but real bugs hide in how they are called (low locality).
- Tight coupling leaks across seams.
- Behavior is hard to test through a public interface.

Apply the deletion test: would deleting the suspected module concentrate complexity or merely move it? Concentration is a deepening signal.

## 2. Present candidates as a visual report

Write a self-contained HTML report to a temp directory, never the repo:

- Resolve temp dir from `$TMPDIR`, then `/tmp`, then `%TEMP%` on Windows.
- Name it `architecture-review-<timestamp>.html`.
- Open it (`xdg-open`, `open`, or `start`) when possible and report the path.

The report is for a busy owner choosing a candidate, not an architecture paper. Lead each card with the problem and the recommended direction; keep **module / interface / depth / seam** — those are this reader's words. One topic per card. Do not load `plain-language`.

Each candidate card includes:

- **Files/modules involved**.
- **Problem** — why current structure causes friction.
- **Solution** — deepening direction in this project's vocabulary, not a full interface spec yet.
- **Benefits** — locality/leverage/testability.
- **Before/after diagram** — Mermaid for graph-shaped relationships, hand CSS/SVG where clearer.
- **Recommendation strength** — Strong / Worth exploring / Speculative.
- **Provenance** — for a card seeded by an observation, carry the exact observation `source` value (the source identity) as `source` and every concrete evidence link declared in the observation and used in verification. A missing or unverified link invalidates the card: discard it with an explicit reason rather than silently omitting the link.

Require the temporary architecture report—or the declared durable review artifact when it is the report surface—to show exactly one candidate/discard row for every non-suppressed eligible inbox entry actually processed: each row must have either a candidate card with full provenance or an explicit discard reason. Suppressed terminal matches intentionally have no current-run verification, candidate card, or report disposition-ledger row; the matching fallback ledger entry already resolves them. Unread entries must not be presented or called resolved.

Do not name, list, quote, or otherwise reveal unread entry IDs or bodies in the temporary report, report disposition ledger, fallback disposition ledger, trace, or durable review artifact. The only permitted reference is an aggregate statement that older or out-of-bound history was not inspected.

End with a top recommendation and ask: **"Which of these would you like to explore?"** That ask is the last thing on the page. Do not implement yet.

## 3. Grill the chosen candidate

When the user picks one, if it was seeded by an inbox observation, leave that observation unchanged while reading and presenting it. The producer's canonical field is lowercase `status`; a capitalized `Status` is only a project-declared syntax alias for that field. Reading and report generation must not write the inbox status or the fallback disposition ledger. Run `grilling` one question at a time to resolve constraints, dependencies, the deepened module shape, what sits behind the seam, and what tests survive; run `domain-modeling` inline for terminology/ADRs that crystallize. Determine the user's outcome first. Only after the outcome is determined may the consumer update the selected observation's canonical lowercase `status` to exactly `accepted`, `rejected`, or `deferred` when inline edits are permitted. When inline edits are forbidden, append a row to `.bc-agent/research/architecture-review-dispositions.md` for a scaffolded project, or to the explicitly declared equivalent ledger, after the outcome; leave the inbox's lowercase `status` as `open`. That durable row must carry the exact observation identity, exact canonical `source` value, exact terminal disposition, every concrete evidence link declared in the observation and used in verification, and the verification/disposition reason. On a later run, consult the bounded ledger before inbox candidate filtering and suppress only that exact identity/source pair; do not add it as a candidate or report ledger row. If no fallback ledger sink exists or is declared, report **not persisted** after the outcome; if a later run encounters that known disposition, state the non-persistence instead of silently re-presenting it as a candidate. An observation is never suppressed merely because it was read.

If the user rejects a candidate for a load-bearing reason, offer to record an ADR so future architecture reviews don't re-suggest it. Skip ADRs for temporary "not now" reasons.

## Integration with bc skills

- Before `/bc-plan-to-issues`: use this when the next feature needs an architectural runway before slicing.
- After `diagnosing-bugs`: use this when a bug fix reveals no correct regression-test seam.
- Output should become a plan/ADR/issue set via `/bc-plan-to-issues`; this skill itself does not create GitHub issues or edit production code.
