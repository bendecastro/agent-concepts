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

At the beginning of Explore, locate the project's architecture-observation inbox:

- For a project scaffolded by `bc-init-agent`, use `.bc-agent/research/architecture-observations.md`.
- Otherwise use an equivalent path only when project instructions explicitly declare it. If no sink exists or is declared, preserve the existing flow; do not invent a docs tree or claim that observations will be persisted.

Before organic exploration, read only entries eligible under the producer's canonical lowercase `status: open` marker from that inbox alongside the project glossary and ADRs. A capitalized `Status` is eligible only when project instructions explicitly declare it as a syntax alias for the canonical lowercase field. Preserve the inbox's current order (newest first). If project instructions declare an eligible-entry read bound `N`, read exactly the `N` newest eligible entries when at least `N` exist, otherwise read all eligible entries. With no declared bound, read exactly the 10 newest canonical lowercase `status: open` entries when at least 10 exist, otherwise read all available canonical lowercase `status: open` entries. Do not scan older history beyond that set. These bounds are for context economy, not correctness authority: unread older entries are not thereby resolved or irrelevant. Treat every entry actually read as a hypothesis, not a decision, and verify every one against the current code/tree: its named **module**, **interface**/**seam**, deletion-test consequence, and every concrete evidence link declared in the observation and used in verification. Do not present stale, closed/rejected, shape-only, or contradicted entries as candidates. For every read entry, either include it in a candidate card whose `source` exactly carries the entry's source value (the observation identity) and whose evidence carries every concrete evidence link declared in the observation and used in verification, or explicitly discard it with a reason. A missing or unverified link invalidates a candidate card: discard it with an explicit reason rather than silently omitting the link. Shape-only, stale, closed/rejected, and contradicted entries must be discarded and cannot seed cards. Never copy an old recommendation into a decision.

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

Require the temporary architecture report—or the declared durable review artifact when it is the report surface—to show a disposition ledger for every entry actually read: each entry must have either a candidate card with full provenance or an explicit discard reason. Unread entries must not be presented or called resolved.

End with a top recommendation and ask: **"Which of these would you like to explore?"** That ask is the last thing on the page. Do not implement yet.

## 3. Grill the chosen candidate

When the user picks one, if it was seeded by an inbox observation, leave that observation unchanged while reading and presenting it. The producer's canonical field is lowercase `status`; a capitalized `Status` is only a project-declared syntax alias for that field. Reading and report generation must not write the inbox status or a fallback artifact. Run `grilling` one question at a time to resolve constraints, dependencies, the deepened module shape, what sits behind the seam, and what tests survive; run `domain-modeling` inline for terminology/ADRs that crystallize. Determine the user's outcome first. Only after the outcome is determined may the consumer either update the selected observation's canonical lowercase `status` to exactly `accepted`, `rejected`, or `deferred` when inline edits are permitted, or write the durable architecture-review artifact when inline edits are forbidden. In the latter path, leave the inbox's lowercase `status` as `open`; write the artifact only after outcome determination, and require it to carry the observation identity, exact disposition, canonical `source` value, every concrete evidence link declared in the observation and used in verification, and the verification/disposition reason.

If the user rejects a candidate for a load-bearing reason, offer to record an ADR so future architecture reviews don't re-suggest it. Skip ADRs for temporary "not now" reasons.

## Integration with bc skills

- Before `/bc-plan-to-issues`: use this when the next feature needs an architectural runway before slicing.
- After `diagnosing-bugs`: use this when a bug fix reveals no correct regression-test seam.
- Output should become a plan/ADR/issue set via `/bc-plan-to-issues`; this skill itself does not create GitHub issues or edit production code.
