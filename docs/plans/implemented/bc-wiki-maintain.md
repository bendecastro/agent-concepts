# `bc-wiki-maintain` — project-vault maintenance

Date: 2026-08-22
Status: implemented
Verification: deployed 2026-08-23; pressure 4/4 (2026-08-22) and 5/5 after the Gate 2 split (2026-08-25); 25 stdlib regression tests; `bc-wiki-lint.service` passes 8/8 vaults; completed 2026-08-25

This is a design record, not current truth. It states the problem as it stood on 2026-08-22 and
the decisions taken then. Where a decision was later superseded, the change is marked inline.
The authority for current behavior is
[`concepts/bc-wiki-maintain/`](../../../concepts/bc-wiki-maintain/CONCEPT.md).

## Problem (as of 2026-08-22)

Project-local agent vaults depend on agents remembering to maintain the state that tells the
next agent what exists. That mechanism failed in three visible ways.

- The CV vault's `index.md` listed the scaffold pages, but its six `findings/` pages and ADRs
  0002 and 0003 were absent. A compliant cold start could therefore miss the project's actual
  work. **Closed:** the 2026-08-23 pilot filed them; they are now at `CV/.bc-agent/index.md:18-30`.
- The generated architecture-runway page asks agents to update a review date and a PRD
  checklist. In the live vault that state was still `TODO`; the nudge had never fired.
  **Closed 2026-08-25:** the counter now records an accurate zero (no review has run, no
  artifact exists) instead of a placeholder that could not be told apart from an unfilled form.
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
curation decision visible to the agent or human.

**Superseded in part.** "It does not rewrite the catalog" was too strong. Gate 1 now lets the
pass append an index link for a page it files, because a promotion that creates a page and then
reports it as missing from the index leaves work half-done. Generation and reordering are still
forbidden; the constraint is additive-only, not read-only.

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

The maintenance check reports vaults that are absent from the qmd registry. CV remains
excluded because it contains personal data; that exclusion is a privacy decision, not a
search defect. The registry and its ownership rules are updated separately from the vault
scaffold.

**Extended 2026-08-25.** One boolean could not express the real states, so the check reports
four: `registered`, `unregistered`, `intentional exclusion`, and `unindexed` — the last meaning
present in the canonical `qmd-collections.yml` but absent from this machine's `~/.config/qmd/index.yml`.
Drift between canon and machine is a different problem from a vault nobody has decided about, and
collapsing them hid the first. Both Homeflix vaults were `unindexed`; they now read `registered`
on both sides.

That check then found a worse fault it was not built for. The `agents` collection pointed at
`~/Sync/CONFIG/agents`, a path that has never existed on this machine — wrong since the entry was
first committed, not a regression. It still held 491 indexed documents, so searches returned
content from a directory that is gone rather than returning nothing. It now points at the real
workspace and indexes 232 files. `bc-qmd-setup` cannot repair this class by itself: it deliberately
skips a collection already registered under a different path, so a corrected canonical path never
reaches the machine until someone removes the stale entry.

### 10. Rollout starts with CV, then image-maze

CV is local-only and has the exact index drift this plan addresses, so it is a safe pilot for
an automatic writer. Image-maze follows because it contains a real contradiction: a Turnstile
research page says the acceptance bar was lowered while the active task and index say it was
not. The rollout does not rename `.agent` to `.bc-agent` or fold legacy variants into a
migration.

**Landed wider.** The lint timer now covers eight vaults: Music, Scripts, image-maze, CV, the
codebase-design and sql learning vaults, and Homeflix public and production. The `.agent` and
`.bc-agent` names still coexist, as planned.

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

   **Who commits changed on 2026-08-25.** The commit still exists, but the agent no longer
   makes it under the runner: it writes the pages and stops, and the wrapper stages, verifies
   classification coverage, and commits. An agent creates the commit itself only when a human
   explicitly asks in that conversation. The reason is that the wrapper can enforce the range
   subject and the classification gate mechanically, and an agent that commits mid-run defeats
   both. This rewrite is what desynchronised the pressure scenario from the skill — see
   *Where it landed*.
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

## Where it landed

**Deployed 2026-08-23**, after a 4/4 pressure pass on 2026-08-22. Detection runs daily as
`bc-wiki-lint.service` over eight vaults; promotion runs through `run-promotion.sh`.

**The test material drifted from the skill, and that is the lesson worth keeping.** The Gate 2
rewrite above landed at 01:39 on 2026-08-25 and touched `CONCEPT.md`, `SKILL.md`, `docs/status.md`,
and `log.md` — but not `tests/pressure-promotion.md`, last edited at 00:27. For a day the scenario
graded "creates exactly one new commit" while the skill said the agent must not create it. A
compliant agent would have failed the test and a violating one would have passed. `CONCEPT.md`
also claimed all three post-08-22 changes had reached the scenario file, which was true for two of
them. A test that is not updated in the same pass as the behavior it grades inverts, and it does so
silently — nothing was failing.

**Pressure re-run 2026-08-25: 5/5.** Scenario 3 was split into 3a (runner default, agent must not
commit) and 3b (explicit manual request) so both Gate 2 branches are graded. Five fresh consumers,
one per scenario, each in an isolated fixture repository with a private copy of the skill body and
no path into this workspace, so none could read the expected behavior. Graded from the repositories:
byte-prefix comparison against the committed blob, `git log`, `git diff --cached`, and the contents
of every page written. `log.md` was byte-identical in all five. The dirty-tree refusal was checked
directly against the runner rather than through an agent.

Two limits on that evidence: the consumers were one model at max thinking, where gate loopholes are
least likely to open, and they ran standalone rather than through `run-promotion.sh`, so 3a shows
the agent leaves the commit alone but not that the wrapper then makes it — that half rests on
`test_runner_creates_exact_range_commit`. The `[[wikilinks]]` fixture variant is still unrun, which
matters more than it did: the codebase-design vault uses wikilinks and produced all eight link
faults found on 2026-08-25.

**The daily timer was failing and is not any more.** Two of eight vaults failed the detector: Music
with one broken link, codebase-design with five broken and three ambiguous. All were real faults,
not detector noise. `[[image-maze]]` and `[[expression]]` named pages that were never written, and
bare `[[plan]]` collided with `templates/plan.md`. They now point at the pages that actually document
those things. The service reports `failures=0` across all eight vaults.

**Follow-up still open.** No architecture review has run in CV, so the runway counter reads a true
zero. The `sql` learning vault is deliberately excluded from qmd while it remains scaffold — it has
no `log.md` and no recorded sessions, so nearly all its text is unedited template boilerplate.
Re-running the pressure set against a wikilink vault, and a low-thinking consumer, are the two
checks that would most strengthen the evidence.

## Sources

- [Perplexity, "Brain: Agentic Memory as a Knowledge Wiki"](https://www.perplexity.ai/hub/blog/brain-agentic-memory-as-a-knowledge-wiki) — Git-backed Markdown memory, offline compilation, staged writes, citations, and on-demand navigation.
- The user's existing personal wiki lint and consolidation scripts — prior art for broken-link, orphan, index-drift, and semantic-maintenance checks.
- [`bc-init-agent`](../../../concepts/bc-init-agent/CONCEPT.md) — additive project-vault scaffold, archetypes, and canonical skill-map pattern.
- [`qmd`](../../../concepts/qmd/CONCEPT.md) — global search/index overlay and collection registration model.
