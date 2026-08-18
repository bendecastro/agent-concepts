---
name: codebase-docs
description: >
  Keep source-tree documentation truthful: one home per fact, current state
  not change history, tutorial vs reference, and update the owning README or
  existing docs page in the same change as the behavior it describes. Use when
  writing, moving, reviewing, or auditing README, docs/, architecture pages, or
  JSDoc, or when a review says the docs do not match the code. Not for
  .bc-agent/ wikis, agent-facing skills/gates, or human-facing prose quality.
---

# Codebase Docs

Source-tree docs are a map of **current** behavior for the next maintainer
or agent. They fail when the same fact lives in two places, when a page
narrates the PR that wrote it, or when the code moves and the owning page
does not.

This skill owns **placement** and **truthful maintainer writing**. It does
not own reader-outcome prose (`plain-language`), agent-instruction authoring
(`prompting-agents`), or whether a decision earns an ADR (`domain-modeling`).

## When this applies

Use it on **source-tree** maintainer docs: README, an existing `docs/` tree,
architecture pages, package READMEs, and JSDoc that states a contract.

**Do not apply it to `.bc-agent/`.** Do not edit, move, or delete vault
files to satisfy one-home. The vault has its own placement; a second
copy there is not this skill's problem to erase.
**Do not apply it to skill bodies, kernels, gates, or this workspace's
concept files** unless the user asked to edit those — that is
`prompting-agents`.
**Do not use it to restyle a help page or announcement.** Placement still
applies if the file is source-tree docs; wording for human readers is
`plain-language`.

On a mixed change, apply this skill only to the source-tree doc surface.
`code-review` loads this skill when a Standards pass sees source-tree docs
in the diff. `bc-init-agent` points new code wikis at it and keeps it off
the vault.

## One home per fact

Each fact has one home: the page whose job it is. Elsewhere, link there.

| Job | Home | Does not belong there |
|---|---|---|
| Standing orders an agent needs every session | Root `AGENTS.md` — one to three lines, then a link to the home | Stories, procedures, restated contracts |
| Current behavior a caller or maintainer looks up | README, or the existing owning `docs/` / architecture page | Why we chose it, PR history, a second copy of the same contract |
| Cross-module map (only if the page already exists) | `docs/architecture.md` or equivalent | Type catalogs, per-package detail, rationale |
| Costly, puzzling, trade-off decision | An ADR, and only when `domain-modeling`'s three-part bar holds | Everyday implementation notes |
| How-to with verify steps | An existing cookbook / contributor page | Design rationale |

A document's subject and tree position fix its detail: describe this
subject; name children by purpose; link to the owner for lower-level
detail. Why: a README that also retells architecture and the last three
PRs becomes a second, worse source of truth.

**Do not create a `docs/` tree** because this skill fired, because the
README feels crowded, or because the user said "just make `docs/foo.md`"
or "I'm short on time." That is a request to document a fact, not a
request for a docs tree. Update the existing owner (usually README).
Create `docs/` only when it already exists, or when the user asks for a
*tree* — architecture, contributor guides, more than one page — not a
single file that duplicates the README. Why: "just make docs/cli.md"
is the shortcut that grows a second wiki.

If no page owns the fact, say so. Do not invent a folder to house it.

## Tutorial vs reference

Classify every in-scope page as a **tutorial** (ordered path to an
observable outcome) or a **reference** (lookup of current behavior, no
teaching sequence). Split them when both forms are substantial. Why:
a reference that also onboards, or a tutorial that also catalogs, hides
the fact the next reader came for.

## Write the current state

Name the live mechanism. Do not write "previously," "now," "no longer,"
"this PR," "this commit," or "rejected in review" in durable source-tree
docs. Put the change story in the commit, the PR, or an ADR.

A reader at HEAD, with no session or PR, must be able to resolve every
reference and verify every claim. If they cannot, restate the surviving
fact from the repository's vantage and delete the transcript.

Do not hand-edit a file that says it is generated. Edit the owner, then
regenerate if you know the command; otherwise leave it and say so.

## Same-change sync

When you change behavior that a README or existing docs page **already
describes**, update that page in the same change. Why: "the code is the
docs" is how the next session ships against a lie.

This is a human placement rule, not a verifier. Do not add type-paste
gates, word-count budgets, or i18n pairing. Do not create a page just
so the rule has a target.

If the owning page is unclear, pick the existing page that already
claims that surface (usually the nearest README) or report that none
does.

## Never

These fail by rationalization — the moment they are inconvenient is
when they matter.

- **Never create `docs/`** because someone asked for a single file or
  was short on time. Why: that is how a second wiki starts. A real
  docs-tree request names more than one page or a new home README
  cannot own.
- **Never edit, move, or delete `.bc-agent/`** under this skill. Why:
  one-home is not a license to empty the vault.
- **Never skip the owning-page update** because the diff is "obvious"
  or you are short on time. Why: that is how docs and code diverge.
- **Never dump rationale into a README** to avoid the ADR bar. Why:
  `domain-modeling` keeps ADRs rare so the load-bearing ones stay
  visible; a README is not the overflow tank.
- **Never treat this skill as a note-every-change gate.** Why: that
  default was considered from DeepSeek's Agent Notes and rejected.

## Output

- Writing/moving: the page that owns the fact, updated to current
  state, with links instead of copies. If you did not update a page,
  say which existing owner was checked and why it needed no change.
- Review: short findings tagged `home` / `current` / `form` /
  `same-change`. Do not rewrite a tree you were asked only to review.
