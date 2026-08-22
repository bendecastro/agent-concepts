---
test_kind: pressure
test_status: not-run
tested: never
deployed: no
---
# Concept: bc-wiki-maintain

Explicit maintenance pass for a project-local Markdown agent wiki. It runs a deterministic
health detector first, promotes durable evidence from the vault's append-only `log.md` into the
smallest appropriate page, updates the curated index, and records contradictions as unresolved
open questions. A systemd user timer may invoke the same pass headlessly, but automation never
weakens its three write-safety gates. The `bc-` prefix is the user's personal namespace.

## Design decisions

- **Separate capture from synthesis.** Agents already capture discoveries in `log.md` because
  appending is cheap and placement-free. This concept performs the later judgment-heavy promotion
  instead of asking the task agent to notice, classify, and rewrite the wiki at the end of work.
  The log remains intact as the evidence trail.
- **Computed triggers, never recorded triggers.** Git history and the filesystem determine the
  last dedicated promotion boundary, current pages, and detector state. No hand-maintained marker
  or counter is introduced. The existing architecture-runway tracker has remained `TODO / TODO /
  TODO` since 2026-07-31 and never fired; a new recorded trigger would repeat that failure mode.
- **Central detector with a vault-root argument.** The bundled `body/wiki_lint.py` is the project
  adaptation of the user's small stdlib-only personal-wiki linter. It must accept a root rather
  than hardcode `.bc-agent`, because live vaults also use `.agent/` and `agent/wiki/` variants.
- **Curated index, not generated index.** `index.md` carries editorial groupings and annotations.
  The pass reports missing entries and appends only the link for a newly created page; it never
  replaces the index with a generated catalog.
- **Git supplies dates; pages do not gain required frontmatter.** A second `updated` field would
  be hand-maintained state that can drift. Page kind comes from its directory; date evidence comes
  from `git log -1 --format=%cs -- <path>`.
- **Automatic promotion is additive and auditable.** A run may create a page or append a dated
  section, then lands exactly one dedicated `wiki: promote log entries <from>..<to>` commit. Git
  history makes the entire result inspectable and reversible without a human approval queue.
- **Contradictions are first-class unresolved work.** When pages disagree, the run creates or
  appends an `open-questions/` record containing both citations and stops the conflicting
  promotion. It never silently chooses the newer, more detailed, or more plausible claim. This
  protects scheduled runs from turning ambiguity into false canonical truth.
- **No broad cleanup during promotion.** The pass does not reflow prose, delete stale pages,
  normalize headings, or modify qmd registry policy. Those are separate, explicitly scoped
  operations. The pilot is one writer against a small vault; staged whole-graph semantic
  verification from Perplexity Brain is intentionally deferred until concurrency or scale makes
  that machinery worthwhile.

## Provenance

- Perplexity Brain distillation captured in the run artifact `brain.md` — separate capture from
  synthesis, deterministic verification, contradiction handling, and Git-backed audit:
  https://www.perplexity.ai/hub/blog/brain-agentic-memory-as-a-knowledge-wiki
- Perplexity, “Brain: Agentic Memory as a Knowledge Wiki,” 19 Aug 2026:
  https://www.perplexity.ai/hub/blog/brain-agentic-memory-as-a-knowledge-wiki
- `~/Sync/Wiki/scripts/wiki_lint.py` — the ported prior art for broken links, ambiguous links,
  orphan pages, and missing index entries.
- `concepts/bc-init-agent/` — the additive, idempotent, never-deletes project-vault scaffold
  this concept extends.
- `concepts/qmd/` — the global search overlay whose collection coverage the detector reports.
- `concepts/prompting-agents/body/SKILL.md` — adapted scope-discipline, gate, evidence, and
  verification instruction blocks used in the body.

## Tests

`tests/pressure-promotion.md` defines the pressure scenarios. The pressure run has **not** been
executed in this implementation work, so the frontmatter remains `test_status: not-run`,
`tested: never`, and `deployed: no`. Do not deploy this concept until a fresh consuming agent
holds all three gates under the scripted excuses and the result is graded from its artifacts.

## Deploy targets

Not deployed. After the pressure test passes, the intended targets are the normal relative skill
symlinks (`~/.agents/skills/bc-wiki-maintain`, `~/.pi/agent/skills/bc-wiki-maintain`, and
`~/.claude/skills/bc-wiki-maintain`) through the workspace deploy script. The systemd user timer
is a separate runner and must be installed only after the pilot is explicitly authorized.

## Open risks

- Promotion still requires a capable headless agent to classify evidence; the detector cannot
  prove semantic truth by itself.
- An unresolved contradiction deliberately stops its conflicting promotion, so a scheduled run
  may need human follow-up rather than silently making progress.
- The concept's no-staged-tree choice is bounded to the single-writer pilot; concurrent writers
  or a much larger vault may require a staged-tree and semantic-verification design later.
