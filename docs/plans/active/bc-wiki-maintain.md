# `bc-wiki-maintain` — project-vault maintenance

Date: 2026-08-22
Status: active
Verification: scaffold pointer and computed architecture-runway check implemented; concept pressure test, qmd registration, and the CV pilot remain open.

## Problem

Project-local agent vaults depend on agents remembering to maintain the state that tells the
next agent what exists. That mechanism fails in three visible ways.

- The CV vault's `index.md` lists the scaffold pages, but its six `findings/` pages and ADRs
  0002 and 0003 are absent. A compliant cold start can therefore miss the project's actual
  work.
- The generated architecture-runway page asks agents to update a review date and a PRD
  checklist. In the live vault that state is still `TODO`; the nudge has never fired.
- Durable synthesis accumulates in `log.md` because appending is easy. Promotion into a
  finding, decision, or open question requires placement and contradiction judgment, so it
  is skipped. The log contains useful examples, including a linter blind spot and an
  unresolved public/private mirror decision.

The general failure is recorded state. A trigger that requires an agent to update its own
counter is another page that can become stale. `bc-wiki-maintain` makes health signals and
promotion automatic while keeping the write surface narrow and reversible.

## Resolved design

The following decisions were settled before implementation.

### 1. Scope is the project vault

The first target is the `.bc-agent` project vault. The global personal wiki, the Music entity
corpus, and source-tree documentation have different ownership and evidence rules. The
maintenance skill may accept other vault roots later, but its first pilot is project context.

### 2. The target failures are write and read starvation

The vault already receives append-only session capture in `log.md`, but promoted pages and
catalog entries fall behind. Agents also lose access to relevant pages when the catalog or
search registry is stale. The design fixes both sides rather than adding another generic
context file.

### 3. Capture stays separate from synthesis

Capture already works through `log.md`; this plan does not add a second scratch protocol. A
later maintenance run reads new log material, promotes durable facts into the smallest
relevant page, and leaves the log as evidence. Cheap capture and judgment-heavy synthesis
have separate jobs and separate failure handling.

### 4. The index remains curated

`index.md` contains editorial groupings and context guidance, so generation would erase useful
annotations. The maintenance checker reports pages missing from the index and leaves the
curation decision visible to the agent or human. It does not rewrite the catalog to make the
warning disappear.

### 5. Git supplies dates; pages get no new frontmatter

A required `updated:` property would duplicate `git log -1 --format=%cs -- <path>` and create
another field agents could forget to change. Directory placement already supplies the broad
page kind. The first version adds no vault-wide frontmatter migration.

### 6. The compile pass promotes and reconciles

The pass reads log entries since the previous committed state, places durable material into
findings, decisions, references, or open questions, and checks nearby pages for conflicting
claims. It must preserve the append-only log. A contradiction is recorded for resolution; the
automatic pass never chooses a winner.

### 7. The canonical home is a new central concept

`bc-wiki-maintain` owns the instructions and the root-argument maintenance script in the
agent-concepts workspace. Vaults point at the canonical body through their skill map. They do
not receive copied scripts, so `.bc-agent/`, `.agent/`, and legacy `agent/wiki/` instances do
not grow independent implementations.

### 8. Detection and promotion run automatically

Health detection is computed from the filesystem, Git history, links, index membership, and
qmd registration. Promotion is a headless agent run. No hand-maintained counter is part of the
trigger. The architecture-runway scaffold now uses a Git-derived planning-surface signal; it
can over-count when commit history does not identify a review, but it cannot silently expire
because an agent forgot a checklist entry.

### 9. The read path includes qmd coverage

The maintenance check reports vaults that are absent from the qmd registry. Homeflix's public
and production `.agent` vaults are active but missing from the current registry. CV remains
excluded because it contains personal data; that exclusion is a privacy decision, not a
search defect. The registry and its ownership rules are updated separately from the vault
scaffold.

### 10. Rollout starts with CV, then image-maze

CV is local-only and has the exact index drift this plan addresses, so it is a safe pilot for
an automatic writer. Image-maze follows because it contains a real contradiction: a Turnstile
research page says the acceptance bar was lowered while the active task and index say it was
not. The rollout does not rename `.agent` to `.bc-agent` or fold legacy variants into a
migration.

### 11. The runner is a systemd user timer

The pilot uses one headless Luna max run scoped to CV. A systemd user timer supplies service
status and journal logs when the run fails; the unit and wrapper are written as canonical
artifacts but are not installed by the scaffold change. Each vault gets an isolated run so a
bad state in one vault does not stop maintenance elsewhere when the rollout expands.

## Automatic-promotion safety

Automatic writes are acceptable only with all three constraints below.

1. **Additive-only changes.** The pass may create a new page or append a clearly bounded
   section. It may not delete, rewrite, or reflow existing prose. This follows the scaffold's
   existing additive/idempotent behavior.
2. **A dedicated Git commit.** Promotion runs only from a clean working tree and lands as one
   maintenance commit, such as `wiki: promote log entries 2026-08-04..2026-08-22`. The diff is
   reviewable with `git show` and undoable with `git revert`; the runner never edits a dirty
   tree in place.
3. **Contradictions are flagged, never resolved.** The pass writes both claims and their page
   or log citations into `open-questions/`, then stops that decision. It must not silently
   choose between competing statements.

## What came from Perplexity Brain

Brain's useful mechanism is a Git-backed Markdown wiki compiled offline by a background
"Dream" agent and navigated on demand. This plan adopts the separation between cheap session
capture and deliberate synthesis, deterministic checks before promotion, contradiction
handling as a first-class result, and Git history as the audit and rollback mechanism. The
existing `log.md` supplies the capture layer, so the project vault does not need Brain's
separate session store.

## What this plan rejects

- **Generated indexes.** They would remove the human's curated grouping and annotations. A
  checker that reports missing entries preserves that information and makes drift visible.
- **Required `updated` frontmatter.** Git already records the date without another mutable
  field.
- **A Perplexity-scale staged semantic graph sync.** A staged tree and semantic verification
  are useful for concurrent large-scale compilation. The first local pilot has one writer and
  a small vault; additive commits, deterministic checks, and Git rollback provide the needed
  boundary without introducing a second graph transaction system.
- **Index prefill in every prompt.** Brain measured a usage benefit in its own harness, but the
  local evidence is stale indexes and missing qmd collections. The first read-path fix is an
  accurate curated index plus registry coverage; prompt-size tax can be revisited after that
  is measured locally.
- **Silent conflict resolution.** Brain describes source chasing, but this project requires a
  scheduled writer to leave contested claims for human resolution. A wrong automatic winner is
  worse than an open question.

## Verification and follow-up

The concept needs a pressure scenario before deployment. The scenario must attack additive-only
writes, dirty-tree refusal, dedicated-commit behavior, and the contradiction rule. The first
pilot should inspect the generated commit and its `git show` output, then run the checker over
CV and confirm that a second run is a no-op. Image-maze is the next validation surface after
that evidence exists.

## Sources

- [Perplexity, "Brain: Agentic Memory as a Knowledge Wiki"](https://www.perplexity.ai/hub/blog/brain-agentic-memory-as-a-knowledge-wiki) — Git-backed Markdown memory, offline compilation, staged writes, citations, and on-demand navigation.
- The user's existing personal wiki lint and consolidation scripts — prior art for broken-link, orphan, index-drift, and semantic-maintenance checks.
- [`bc-init-agent`](../../../concepts/bc-init-agent/CONCEPT.md) — additive project-vault scaffold, archetypes, and canonical skill-map pattern.
- [`qmd`](../../../concepts/qmd/CONCEPT.md) — global search/index overlay and collection registration model.
