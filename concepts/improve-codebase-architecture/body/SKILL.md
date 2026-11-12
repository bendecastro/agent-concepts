---
name: improve-codebase-architecture
description: Scan a codebase for deep-module opportunities, present a visual temp-file report, then grill through one chosen refactor candidate for the bc planning loop.
disable-model-invocation: true
argument-hint: "[area/folder/problem]"
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deeper, more testable, more agent-navigable modules. This is a planning/review tool, not an implementation sprint.

Use `codebase-design` vocabulary exactly: **module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**. Use domain names from the project's glossary; respect its decision records.

## Find the project's paths

This skill names roles — glossary, decisions, research, ideas, work-planned, work-dropped — not paths. Resolve each role from the "Where things go" table in the project's `.bc-agent/AGENTS.md`. Why: each project has one table, so a project that keeps something elsewhere changes one place and every skill follows. When the project has no such table, use the earlier defaults: glossary `glossary.md` (or `.bc-agent/project/overview.md` in a `bc-init-agent` vault), decisions `docs/adr/` (or `.bc-agent/decisions/` in a vault), and the observation inbox and disposition ledger described under [Projects without the table](#projects-without-the-table). Those projects have no ideas, work-planned or work-dropped role, so step 4 does not apply to them.

## 1. Explore

Read the glossary and the decision records first, so candidates use the project's names and do not re-suggest a recorded rejection.

**With the table.** Observations other agents made between reviews are lines in the ideas file. Read the lines that name a module, seam or architecture friction, and the most recent `*-architecture-review/` folder in the research role, if any. Treat each observation as a hypothesis: verify its module, seam and evidence against the current tree before it can seed a candidate, and say in the report which observations you discarded and why. Why: an observation was true when written; the code may have moved since.

If the project has the table but still holds an old observation inbox (`.bc-agent/research/architecture-observations.md`) or disposition ledger (`.bc-agent/research/architecture-review-dispositions.md`): read both, add one ideas-file line for every inbox entry with `status: open` that has no terminal (`accepted`, `rejected`, `deferred`) row for the same identity and `source` in the ledger and whose `source` does not already appear in the ideas file, then add one dated note at the end of the old inbox saying its open entries were carried to the ideas file on that date. Leave both old files where they are, and tell the owner they exist and were carried over. Why the `source` check and the note: both files stay, so without them every later review would carry the same entries again; the inbox is append-only history, so a dated note is the allowed way to mark it. Why: the table retires these files, but deleting them would lose history the owner has not reviewed; carrying the open entries keeps them visible in the one place that now shows pending ideas.

**Without the table**, follow [Projects without the table](#projects-without-the-table) before organic exploration.

Then explore organically for the friction signals in `codebase-design` § Friction signals, confirming each with its deletion test: would deleting the suspected module concentrate complexity or merely move it? Concentration is a deepening signal.

## 2. Present candidates as a visual report

Write a self-contained HTML report:

- **With the table**, save it as `report.html` in a new folder `<YYYY-MM-DD>-architecture-review/` under the research role, and commit it with a subject containing `architecture review` (for example `docs: architecture review of the report pipeline`). Why: the review is durable evidence that later work items point at, and the project's architecture-runway convention finds the last review by that commit subject.
- **Without the table**, write it to a temp directory, never the repo: resolve `$TMPDIR`, then `/tmp`, then `%TEMP%` on Windows, and name it `architecture-review-<timestamp>.html`.
- Open it (`xdg-open`, `open`, or `start`) when possible and report the path.

The report is for a busy owner choosing a candidate, not an architecture paper. Lead each card with the problem and the recommended direction; keep **module / interface / depth / seam** — those are this reader's words. One topic per card. Do not load `plain-language`.

Each candidate card includes:

- **Files/modules involved**.
- **Problem** — why current structure causes friction.
- **Solution** — deepening direction in this project's vocabulary, not a full interface spec yet.
- **Benefits** — locality/leverage/testability.
- **Before/after diagram** — Mermaid for graph-shaped relationships, hand CSS/SVG where clearer.
- **Recommendation strength** — Strong / Worth exploring / Speculative.
- **Provenance** — for a card seeded by an observation, quote the observation (the ideas-file line, or without the table the inbox entry's exact `source` value) and every concrete evidence link it declares and you verified. A missing or unverified link invalidates the card: discard it with an explicit reason rather than silently omitting the link.

End with a top recommendation and ask: **"Which of these would you like to explore?"** That ask is the last thing on the page. Do not implement yet.

## 3. Grill the chosen candidate

When the owner picks one, run `grilling` one question at a time to resolve constraints, dependencies, the deepened module shape, what sits behind the seam, and what tests survive; run `domain-modeling` inline for terminology and decision records that crystallize.

If the owner rejects a candidate for a load-bearing reason, offer to record a decision record in the decisions role so future architecture reviews don't re-suggest it. Skip it for temporary "not now" reasons.

## 4. Record every finding (projects with the table)

Wait until the owner has seen the report and said which findings they want. Why: a review proposes; only the owner decides what becomes work, and a planned item created on the agent's own judgment reads as a decision nobody made. Then give every finding in the report exactly one home:

- **Chosen** → a numbered work item in the work-planned folder, made from the project's work-item template, citing the report folder. Grilling outcomes go into the item.
- **Rejected** → a numbered work item in the work-dropped folder whose `## Outcome` states the owner's reason. Why: a recorded "no, because" stops the next review re-proposing it; a rejection without its reason is lost at the next review.
- **Everything else** (not chosen, not rejected, including discarded observations still worth watching) → one line in the ideas file pointing at the report folder.

Delete each ideas line that seeded a chosen or rejected finding, in the same commit as its item; replace a line that seeded an "everything else" finding instead of adding a second line. Why: the ideas file lists only what is undecided, and a decided line left there would seed the next review again.

Number items as the project's `.bc-agent/AGENTS.md` work-item rules say, and create numbered items only from the main checkout. In a git worktree, add an ideas-file line for each chosen or rejected finding instead, stating the owner's choice and reason, so the main checkout can number it later. Why: two worktrees cannot see each other's numbers and would pick the same one.

Observations you make outside a review, in any later task, are also single lines in the ideas file, naming the module, the seam and the evidence. Why: the next review reads them there, and the ideas file is the one place that shows what is undecided.

## Projects without the table

These projects keep the older observation inbox and disposition ledger, written by `bc-drain-issues`.

At the beginning of Explore, locate the project's architecture-observation inbox and, when inline inbox edits are forbidden, its durable fallback disposition ledger:

- For a project scaffolded by `bc-init-agent`, use `.bc-agent/research/architecture-observations.md` for the inbox and `.bc-agent/research/architecture-review-dispositions.md` for the ledger.
- Otherwise use equivalent paths only when project instructions explicitly declare each path. An inbox declaration does not implicitly declare a fallback ledger. If no inbox sink exists or is declared, preserve the existing flow; do not invent a docs tree or claim that observations will be persisted. If inline edits are forbidden and no ledger sink exists or is declared, report the disposition as **not persisted** after grilling; if a later run encounters that known disposition, state the non-persistence instead of silently re-presenting it as a candidate.

Before organic exploration or presenting inbox candidates, read the bounded fallback disposition-ledger entries first when a ledger sink exists or is declared. Match a ledger row only when both the exact observation identity and exact canonical `source` value match, and only `accepted`, `rejected`, or `deferred` are terminal dispositions. Suppress that exact terminal match before inbox candidate presentation and before current-tree verification or report disposition-ledger processing. A suppressed terminal match intentionally receives no current-run verification, candidate card, or report disposition-ledger row; it is already resolved by the matching ledger entry. Read the ledger metadata needed to filter the bounded inbox set without disclosing unread IDs or bodies. Do not suppress an observation merely because it was read; an open entry with no matching terminal ledger row remains eligible on a later run.

Then, before organic exploration, read only entries eligible under the producer's canonical lowercase `status: open` marker from that inbox alongside the project glossary and ADRs. A capitalized `Status` is eligible only when project instructions explicitly declare it as a syntax alias for the canonical lowercase field. Preserve the inbox's current order (newest first). If project instructions declare an eligible-entry read bound `N`, read exactly the `N` newest eligible entries when at least `N` exist, otherwise read all eligible entries. With no declared bound, read exactly the 10 newest canonical lowercase `status: open` entries when at least 10 exist, otherwise read all available canonical lowercase `status: open` entries. Do not scan older history beyond that set. These bounds are for context economy, not correctness authority: unread older entries are not thereby resolved or irrelevant. Treat each non-suppressed eligible inbox entry actually processed as a hypothesis, not a decision, and verify its named **module**, **interface**/**seam**, deletion-test consequence, and every concrete evidence link declared in the observation and used in verification against the current code/tree. Do not present stale, closed/rejected, shape-only, or contradicted entries as candidates. For each non-suppressed eligible inbox entry actually processed, emit exactly one candidate/discard row: either a candidate card whose `source` exactly carries the entry's source value (the observation identity) and whose evidence carries every concrete evidence link declared in the observation and used in verification, or an explicit discard reason. A missing or unverified link invalidates a candidate card: discard it with an explicit reason rather than silently omitting the link. Shape-only, stale, closed/rejected, and contradicted entries must be discarded and cannot seed cards. Never copy an old recommendation into a decision.

Require the temporary architecture report—or the declared durable review artifact when it is the report surface—to show exactly one candidate/discard row for every non-suppressed eligible inbox entry actually processed: each row must have either a candidate card with full provenance or an explicit discard reason. Suppressed terminal matches intentionally have no current-run verification, candidate card, or report disposition-ledger row; the matching fallback ledger entry already resolves them. Unread entries must not be presented or called resolved.

Do not name, list, quote, or otherwise reveal unread entry IDs or bodies in the temporary report, report disposition ledger, fallback disposition ledger, trace, or durable review artifact. The only permitted reference is an aggregate statement that older or out-of-bound history was not inspected.

When the owner picks a candidate seeded by an inbox observation, leave that observation unchanged while reading and presenting it. The producer's canonical field is lowercase `status`; a capitalized `Status` is only a project-declared syntax alias for that field. Reading and report generation must not write the inbox status or the fallback disposition ledger. Grill it as in step 3 and determine the owner's outcome first. Only after the outcome is determined may the consumer update the selected observation's canonical lowercase `status` to exactly `accepted`, `rejected`, or `deferred` when inline edits are permitted. When inline edits are forbidden, append a row to `.bc-agent/research/architecture-review-dispositions.md` for a scaffolded project, or to the explicitly declared equivalent ledger, after the outcome; leave the inbox's lowercase `status` as `open`. That durable row must carry the exact observation identity, exact canonical `source` value, exact terminal disposition, every concrete evidence link declared in the observation and used in verification, and the verification/disposition reason. On a later run, consult the bounded ledger before inbox candidate filtering and suppress only that exact identity/source pair; do not add it as a candidate or report ledger row. If no fallback ledger sink exists or is declared, report **not persisted** after the outcome; if a later run encounters that known disposition, state the non-persistence instead of silently re-presenting it as a candidate. An observation is never suppressed merely because it was read.

## Integration with bc skills

- Before `/bc-plan-to-issues`: use this when the next feature needs an architectural runway before slicing.
- After `diagnosing-bugs`: use this when a bug fix reveals no correct regression-test seam.
- A chosen finding becomes a planned work item (or, without the table, a plan/decision record/issue set via `/bc-plan-to-issues`); this skill itself does not create GitHub issues or edit production code.

Inline how-it-works visuals outside this report → `show-me`; this report keeps its own format.

For glossary discovery in legacy projects, follow `domain-modeling`’s legacy glossary rule.
