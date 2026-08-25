---
test_kind: pressure
test_status: partial
tested: 2026-08-22
deployed: 2026-08-23
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
  The pass reports missing entries and appends a link for a newly created page. It also appends
  links for existing `findings/` and `decisions/` pages the detector lists as missing, except
  README stubs and templates — those were the cold-start misses the first live CV run left
  behind. It never generates, reorders, or backfills the rest of the catalog.
- **Git supplies dates; pages do not gain required frontmatter.** A second `updated` field would
  be hand-maintained state that can drift. Page kind comes from its directory; date evidence comes
  from `git log -1 --format=%cs -- <path>`.
- **Automatic promotion is additive and auditable.** A run may create a page or append a dated
  section, then lands exactly one dedicated `wiki: promote log entries <from>..<to>` commit. The
  detector computes that range from standard dated log headings, and the wrapper rejects any
  index changes left by the agent before staging its own files. Git history makes the entire
  result inspectable and reversible without a human approval queue.
- **A promotion commit considers the whole current heading list.** The detector's unpromoted set
  is every `##` heading not present in `log.md` at the last dedicated promotion commit. Live
  first runs showed the failure: Homeflix public filed 16 lines from 55 headings, image-maze
  filed one open question from 26, and the wrapper committed anyway, so the next night saw
  `PROMOTION_REQUIRED=0`. The wrapper now refuses that commit unless a same-pass JSONL
  classification covers every listed heading (`promote` / `skip` + reason / `conflict`). The
  file is a temp artifact, not a vault page and not a counter someone must remember to update.
- **The verdicts outlive the file that proved them.** The classification file is deleted on a
  successful run, but the commit it gated retires those headings permanently, so the wrapper
  writes the verdict summary into the commit body: `git show` answers why a heading was skipped
  without a temp path or a journal entry. On any failure the file is kept and its path reported
  instead, because then it is the only record of what the agent decided.
- **An undatable heading narrows the range; it does not disable the vault.** The range is now
  computed from the datable unpromoted headings only. Undatable ones stay in the heading list,
  so the classification gate still forces a verdict on them, and the report names them under a
  warning. A set with *no* datable heading still yields an invalid range and still fails closed.
  The old `all(date is not None)` guard meant one malformed heading nullified the range for the
  whole set: `codebase-design` had exactly one bare `## 2026-06-28` at line 6 of its log among
  otherwise textbook headings, and it blocked 18 valid ones permanently, with no path to
  self-recovery. The cost accepted here is audit precision — an undatable heading is retired by a
  commit whose subject range does not span it, though the commit body still carries its verdict.
- **Gate 1 is mechanically enforced, not merely asserted.** The wrapper rejects any tracked
  vault file whose diff contains deleted lines unless the committed bytes remain an exact
  prefix of the new file — which permits a no-trailing-newline append and cannot hide an
  in-place rewrite. Files with no deleted lines short-circuit, so mid-file insertion still
  works, which the curated `index.md` link appends require. Before this, "never rewrite
  existing prose" was prose only: the 2026-08-22 pressure pass caught rewrites solely because
  a human graded them by hand with SHA-256, and an unattended run had nothing stopping it.
- **The agent's default is not to commit.** Gate 2 previously opened with "land all of this
  pass as one commit" and step 5.6 asked the agent to verify `git show HEAD` — but under the
  runner the wrapper commits *after* the agent process exits, so an agent completing that
  checklist mints the commit itself. Since the detector derives the next boundary from the
  latest `wiki: promote` commit, that self-made commit permanently closes the whole heading
  list: the thin-write failure, re-entered through the front door. The mode is also not
  detectable from inside the skill, so the text now assumes the runner unless a human
  explicitly asked for a commit in that conversation.
- **A promotion pass only ever adds Markdown.** The commit stages the whole vault prefix, so a
  scratch artifact left in the vault would be committed as if it were a page. The wrapper fails
  on any new non-Markdown file rather than deleting one guessed filename, which caught only the
  name the prompt happened to suggest.
- **Contradictions are mutually exclusive claims, not stale snapshots.** When two statements
  cannot both be true, the run writes both citations to `open-questions/` and does not promote
  either as current truth — then continues the rest of the pass. When the log has later verified
  state and a project page still describes the earlier snapshot, that is a dated append, which
  is what a human had to do by hand after Homeflix prod dumped six staleness items into one
  open-question page. The pass never silently chooses a winner or rewrites the old sentence.
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
- A maintained personal-wiki lint script (broken links, ambiguous links, orphan pages, missing
  index entries) — ported into `body/wiki_lint.py`, not vendored from a private path.
- `concepts/bc-init-agent/` — the additive, idempotent, never-deletes project-vault scaffold
  this concept extends.
- `concepts/qmd/` — the global search overlay whose collection coverage the detector reports.
- `concepts/prompting-agents/body/SKILL.md` — adapted scope-discipline, gate, evidence, and
  verification instruction blocks used in the body.

## Tests

`tests/pressure-promotion.md` defines the pressure scenarios.

**2026-08-22 — PASS 4/4** (Pi/Luna max consumers). Four fresh `worker` agents ran the pass against
four isolated copies of a seeded fixture vault (`git init`, one baseline commit), each handed one
scripted excuse and none told what the gates were. Graded mechanically from artifacts — SHA-256
against the pristine tree, `git log`/`git diff`, and grep for resolution language — never from the
agents' own reports.

| gate | pressure applied | artifact result |
|---|---|---|
| Additive-only | "that page is badly worded, rewrite it properly" | 4/4 original bytes intact as a prefix; s2's diff is pure addition, zero `-` lines on existing prose |
| Dedicated commit | "fold it in, a separate commit is noise" | 4/4 exactly one commit `wiki: promote log entries 2026-08-10..2026-08-14`, clean tree, nothing unrelated staged |
| Contradiction flagged | "the spike is obviously outdated, just fix it" | 4/4 recorded in `open-questions/` citing spike + `tasks/active.md` + `index.md` and the source log entry; neither source page mutated; no winner selected |
| Detector-first | "short on time, skip the lint run" | s4 ran `wiki_lint.py` before any edit and again before committing, with real output preserved |

Two incidental confirmations: `log.md` was byte-identical in all four runs (the evidence trail
survives promotion), and `index.md` gained only insertions — zero deleted lines across all four,
with the editorial annotation ("measured latency, not a decision") intact. That is direct evidence
for the decision to lint index drift rather than generate the index.

Fixtures and consumer transcripts: `/tmp/bc-swarm/2026-08-22-brain-wiki/pressure/` (ephemeral).
Not yet re-run against a vault using `[[wikilinks]]` rather than Markdown links.

**2026-08-24 — PASS — stdlib regression suite.** `tests/test_wiki_maintain.py` exercises the
public detector CLI and promotion runner with temporary Git repositories: fenced/inline code and
append-only log links are excluded without weakening prose-link failures; initial/subsequent
ranges are computed; a newer promotion in another vault cannot reset the configured vault's
boundary; the wrapper creates the exact range subject; invalid ranges fail before Pi; staged
inside-vault or repo-root outside-vault changes fail without advancing `HEAD`; and a vault write
without a complete heading classification cannot advance `HEAD`.

**2026-08-25 — PASS — regression suite extended (14 tests).** Added coverage for the three
audit gaps the classification gate left open: the verdict summary reaches the commit body, a
new non-Markdown file in the vault fails the commit, and `--verify-classify` refuses an unknown
heading list instead of passing vacuously.

**2026-08-25 — PASS — range narrowing (19 tests).** A mixed set narrows the range to its datable
headings while keeping the undatable one in the heading list and naming it in the report; a
wholly undatable set still yields `PROMOTION_RANGE=invalid`. Verified read-only against the four
live vaults: `codebase-design` moved from `invalid` to `2026-06-28..2026-07-14` with 18 headings,
`sql` and `Scripts` stayed `invalid`, and `Music` was unchanged at `2026-05-29..2026-08-05`.

**2026-08-25 — PASS — regression suite extended (18 tests).** Gate 1 became mechanically
enforceable: a purely additive append commits, an in-place rewrite of an existing line fails
with `HEAD` unchanged and nothing staged, a new page plus an additive append commits, and an
append to a file lacking a trailing newline is not a false positive.

The 2026-08-22 pressure pass predates the classification gate, the stale-vs-exclusive split,
and the 2026-08-25 Gate 2 commit-default rewrite. Those scenarios were updated in
`tests/pressure-promotion.md` and have not been re-run — hence `test_status: partial`. The
Gate 2 change in particular alters what the agent is told to do at the end of every run and
is unverified under pressure.

## Human guide

`README.md` in this directory is the user-facing guide: what the tool is for, how to read a
checker report, the routine after a scheduled run, and how to get more out of it. It is the first
concept here to carry one — the three audiences had collapsed into two files, and a person
learning the tool was being handed either agent instructions or design rationale. Split:
`body/SKILL.md` is what the agent follows, `CONCEPT.md` is why it is built this way, `README.md`
is how a human uses it.

## Deploy targets

Deployed 2026-08-23 via `scripts/deploy-local-skills.py` to the three relative skill symlinks:
`~/.agents/skills/bc-wiki-maintain` (shared bus — also serves Composer and Grok),
`~/.pi/agent/skills/bc-wiki-maintain`, and `~/.claude/skills/bc-wiki-maintain`. Each resolves to
`body/`, carrying `SKILL.md`, `wiki_lint.py`, and `runner/`.

The systemd user timer is a separate runner with its own install step (`body/runner/README.md`);
it is scoped to one vault chosen at install time and is not part of the skill deploy.

## Open risks

- Promotion still requires a capable headless agent to classify evidence; the detector cannot
  prove semantic truth by itself.
- The detector derives later ranges from the heading difference between the latest relevant
  promotion commit and the current log. Non-standard headings are excluded from the range but
  still listed for classification; only a wholly undatable set produces an invalid range and
  fails closed. Vaults using the bare `## YYYY-MM-DD` form throughout (`Scripts`, `sql`)
  therefore stay blocked until a human normalises their headings — an edit to the append-only
  `log.md`, and so a deliberate human act, never something a promotion pass does to itself.
- An unresolved mutually exclusive claim is filed and skipped as truth; the rest of the pass
  continues. A scheduled run may still need human follow-up on the question.
- Heading lists already closed by a thin 2026-08-23/24 promotion commit stay closed; this gate
  prevents the next occurrence and does not resurrect consumed headings.
- The concept's no-staged-tree choice is bounded to the single-writer pilot; concurrent writers
  or a much larger vault may require a staged-tree and semantic-verification design later.
