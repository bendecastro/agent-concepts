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

Read project glossary and ADRs first. Then explore organically for friction:

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

End with a top recommendation and ask: **"Which of these would you like to explore?"** That ask is the last thing on the page. Do not implement yet.

## 3. Grill the chosen candidate

When the user picks one, run `grilling` one question at a time to resolve constraints, dependencies, the deepened module shape, what sits behind the seam, and what tests survive. Run `domain-modeling` inline for terminology/ADRs that crystallize.

If the user rejects a candidate for a load-bearing reason, offer to record an ADR so future architecture reviews don't re-suggest it. Skip ADRs for temporary "not now" reasons.

## Integration with bc skills

- Before `/bc-plan-to-issues`: use this when the next feature needs an architectural runway before slicing.
- After `diagnosing-bugs`: use this when a bug fix reveals no correct regression-test seam.
- Output should become a plan/ADR/issue set via `/bc-plan-to-issues`; this skill itself does not create GitHub issues or edit production code.
