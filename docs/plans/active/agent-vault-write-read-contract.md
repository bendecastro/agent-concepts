# Agent vault write/read contract — make the scaffold and the maintainer agree

Date: 2026-08-29
Status: active
Verification: no work item implemented. The findings below come from running
[`wiki_lint.py`](../../../concepts/bc-wiki-maintain/body/wiki_lint.py) against all eight live
vaults on 2026-08-29, reading the current
[`scaffold.py`](../../../concepts/bc-init-agent/body/scaffold.py), and an independent review that
corrected five claims in the first draft — the citation audit is in that review, and its
corrections are folded in below.

Successor to [`agent-vault-read-path.md`](agent-vault-read-path.md), which resolved the retrieval
question and left the write side untouched. That plan proved ranked search beats every
alternative it measured: 171 median output tokens at a 0.15 miss rate, against 4,543 for an
`index.md` load (`agent-vault-read-path.md:346-348`). This plan addresses the other half of the
same goal — **a lot of knowledge the agent can traverse cheaply and effectively** — where the
knowledge is written by one concept and maintained by another that does not accept its output.

## Problem

`bc-init-agent` and `bc-wiki-maintain` were designed at different times and share no contract.
Init writes a shape the maintainer cannot consume, and the maintainer expects a shape init does
not produce. Three consequences, each verified against the code rather than inferred:

**New vaults are born on the retired read path.** `scaffold.py:40-42` still emits "Before making
non-trivial changes, read: 1. `.bc-agent/index.md`", and `scaffold.py:163` still emits "Read
`index.md` → this file → `map.md` → `tasks/active.md`". The maintainer says the opposite:
"First move: search the vault, do not read the index"
([`SKILL.md:75`](../../../concepts/bc-wiki-maintain/body/SKILL.md)). The 2026-08-28 rollout
edited eight existing vaults by hand; it did not touch the generator that mints the ninth. Every
future vault regresses, and the rollout has to be repeated manually forever.

**The promoter fails closed when no heading in a vault's backlog is datable.** Init emits
`## __DATE__`, rendered to `## 2026-06-26` (`scaffold.py:307`). The detector matches only
`^## \[(\d{4}-\d{2}-\d{2})\]` (`wiki_lint.py:19`). A backlog with no datable heading yields
`PROMOTION_RANGE=invalid`, and
[`run-promotion.sh:82-84`](../../../concepts/bc-wiki-maintain/body/runner/run-promotion.sh)
aborts. Lint still exits 0, so nothing surfaces it.

A mixed backlog is **not** a failure and must not be treated as one: an undatable heading narrows
the range while staying in the emitted heading list, so the classification gate still forces a
verdict on it ([`CONCEPT.md:74-77`](../../../concepts/bc-wiki-maintain/CONCEPT.md), locked by
`tests/test_wiki_maintain.py:107-119`). That behavior is deliberate and this plan does not touch
it.

**Newly created pages are invisible to the next search.** The retrieval corpus is `git ls-files`
(`wiki_search.py:65-76`), read from the working tree (`:121`). Edits to tracked pages are
therefore findable immediately; a page created this turn is not findable until it is tracked,
which collides with the same-turn update discipline.

## What the 2026-08-29 sweep found

`wiki_lint.py` against each live vault, plus `grep -c "^## \["` on each `log.md`. An independent
reviewer re-grepped the heading counts and confirmed all eight; the Git-derived columns were not
independently re-run.

| Vault | `PROMOTION_RANGE` | Unpromoted | Undatable | Bracketed | Pages |
|---|---|---|---|---|---|
| `Music/.bc-agent` | `2026-05-29..2026-08-05` | 37 | 0 | 37/37 | — |
| `Scripts/.bc-agent` | **`invalid`** | 12 | 12 | 0/12 | 54 |
| `Work/PUBLIC/Homeflix/.agent` | `none` | 0 | 0 | 55/55 | — |
| `Work/homeflix-prod/.agent` | `2026-08-24..2026-08-24` | 65 | 0 | 65/65 | — |
| `codebase-design/.bc-agent` | `2026-06-28..2026-07-14` | 18 | 1 | 17/18 | — |
| `sql/.bc-agent` | **`invalid`** | 1 | 1 | 0/1 | — |
| `Work/CV/.bc-agent` | `none` | 0 | 0 | 0/10 | — |
| `.../image-maze/.bc-agent` | `none` | 0 | 0 | 0/26 | 155 |

Three states:

- **Blocked now (2):** Scripts and sql sit at `invalid` — no datable heading in the backlog at
  all. Scheduled promotion cannot run. Scripts has twelve entries stranded since June.
- **Latent (2):** CV and image-maze have 10 and 26 unbracketed headings but empty backlogs, because
  a promotion commit on 2026-08-25 cleared them. Their next log entry moves them to `invalid`.
- **Working as designed (1):** codebase-design's single undatable heading narrows its range and
  still reaches the classification gate. No action needed beyond normalization.

Only Music, homeflix-prod, and Homeflix are structurally safe, and only because their logs were
written in the bracketed style the workspace root uses.

The read-path rollout is also uneven. All eight vault `AGENTS.md` files name `wiki_search.py`, but
four (Scripts, codebase-design, sql, CV) carry the one-line form with no empty-result or hub-page
rules. And **all eight root `AGENTS.md` files still route a cold agent to `index.md` first** —
`Music/AGENTS.md:9`, `Scripts/AGENTS.md:5`, `Homeflix/AGENTS.md:11`, `homeflix-prod/AGENTS.md:12`,
and `:7` in each of CV, sql, codebase-design, and image-maze. A fresh agent pays the old cost
before it reaches the vault file that replaced it.

## Scope

In scope: the generator (`bc-init-agent`), the detector and reader (`bc-wiki-maintain`), the
promotion runner prompt, and one-time normalization of the eight live vaults.

Out of scope: the vault taxonomy, page-size or corpus caps, semantic deduplication, and what the
promoter judges. See non-goals.

## Resolved decisions

- **The scaffold is the fix site, not the vaults.** Hand-editing eight vaults was the right
  emergency move on 2026-08-28 and is the wrong permanent one. Behavior that must be true in
  every vault is generated, or it drifts. W6 handles the one-time catch-up for vaults that
  already exist, because W1 alone cannot reach them.
- **Bracketed headings win over relaxing the detector.** `## [YYYY-MM-DD]` is the convention this
  workspace's own `log.md` uses (`AGENTS.md:67-71`). Widening the regex was proposed by two
  advisors during the council and withdrawn by both under cross-examination
  (`agent-vault-read-path.md:511-516`); do not revive it. Note that this workspace's own
  `scripts/lint.py` exempts `log.md` from its path checks, so the linter is not the enforcer
  here — the detector is.
- **A backlog that cannot produce any range is a failure, not a warning.** `invalid` currently
  exits 0, and the point of the scheduled runner is that nobody is watching. A *mixed* backlog
  stays a warning; changing that would contradict `CONCEPT.md:74-77`.
- **W4 does not change ranking without measurement.** The predecessor's central lesson is that the
  design everyone agreed on lost to the one that was measured.

## Work items

### W1 — the scaffold mints the current read path

Inherited from `agent-vault-read-path.md` W5, which never landed, and widened to that item's full
acceptance list.

The root and vault files get **different** content, and conflating them is a live hazard. The
canonical block is delimited by the `BEGIN`/`END canonical vault read path` markers at
[`SKILL.md:76-106`](../../../concepts/bc-wiki-maintain/body/SKILL.md), under the "Pasteable vault
instruction block" heading at `:67`. It sets `VAULT_ROOT="$PWD"` and must be run from the
directory holding the vault `AGENTS.md`. Pasted into the **root** `AGENTS.md` it would resolve
`$PWD` to the repo root; the corpus filter keeps every tracked file under that path
(`wiki_search.py:86-92`), so it would search the whole repository instead of the vault.

- Vault `AGENTS.md` (`scaffold.py:163`): the canonical block, including the empty-result and
  hub-page rules the four thin vaults are missing.
- Root `AGENTS.md` (`scaffold.py:40-42`): point at the vault's `AGENTS.md` as the first read, not
  at `index.md`.
- ADR-0001 consequence (`scaffold.py:593`) and `tasks/active.md` (`scaffold.py:602`): stop naming
  `index.md` as where an agent starts.
- `INDEX`, `HOME`, and `MAP` templates (`scaffold.py:218` still says `## Start here`): stop
  advertising themselves as the retrieval entry point. They survive as human-facing orientation.
- `upgrade_notes()` (`scaffold.py:880-906`) gains a read-path check. **Dependency:** that function
  returns `[]` unless the archetype is `code` or `hybrid` (`scaffold.py:882-883`), so learning
  vaults such as sql and codebase-design never see any upgrade note. Either lift the gate for
  this check or state that learning vaults are covered only by W6.
- `concepts/bc-init-agent/CONCEPT.md` records the change and its dependency on `bc-wiki-maintain`.

**Acceptance.**
- Scaffold a vault into a temp Git repo. Its vault `AGENTS.md` contains the canonical block
  verbatim; its root `AGENTS.md` names the vault `AGENTS.md` as the first read; ADR-0001 and
  `tasks/active.md` name search as the first move. `grep -rn "index\.md" ` over the generated tree
  returns only orientation references, none instructing an agent to read it to locate a fact.
- Running the scaffold against a pre-change `code` vault prints an upgrade note naming the read
  path; the learning-archetype behavior matches whichever branch of the dependency above was
  chosen.
- `bc-init-agent`'s existing script checks still pass, extended with one case asserting the
  generated first move.
- **Test gate:** W1 changes generated discipline text, which is the half of `bc-init-agent` that
  was never pressure-tested (`CONCEPT.md:42-44` — checks 1–7 PASS, 8–12 BLOCKED, status
  `partial`). One pressure scenario against the generated instructions is required before this
  counts as deployed.

### W2 — the log heading contract holds end to end

Three changes. They are **not** equally coupled, and the first draft of this plan was wrong to
say so:

1. **Scaffold emits `## [__DATE__]`** (`scaffold.py:307` and `:632`). Safe alone; improves every
   new vault.
2. **Normalize the existing logs.** Wrap the date token in Scripts, sql, codebase-design, CV, and
   image-maze, each committed in its own repo. Safe alone; unblocks Scripts and sql. Note that
   CV and image-maze headings carry suffixes (`## 2026-07-31 — Pipeline built`); the detector
   accepts `## [YYYY-MM-DD]` followed by whitespace, so wrap the date and keep the suffix — do not
   flatten to date-only lines.
3. **`wiki_lint.py` exits nonzero when promotion is required and the range is `invalid`** (today
   `:522-526` returns 1 only for broken or ambiguous links). **This is the one change that is
   harmful alone:** `run-lint.sh:54-56` currently treats log backlog as non-fatal, so shipping
   this before normalization turns the scheduled lint timer red on Scripts and sql. Land it after
   step 2.

A mixed backlog must keep exiting 0. Failing on any undatable heading would break
codebase-design and contradict `CONCEPT.md:74-77`.

**Acceptance.**
- After normalization, `wiki_lint.py` reports no `PROMOTION_RANGE=invalid` in any of the eight
  vaults, and Scripts' twelve entries appear in a valid range.
- A scratch vault whose unpromoted headings are **all** undatable exits nonzero; a scratch vault
  with a mixed backlog still exits 0 and still lists the undatable heading.
- `tests/test_wiki_maintain.py` gains a case for each of those two states.

### W3 — decide the search corpus boundary

`wiki_search.py` searches tracked, non-ignored Markdown from the working tree. Edits to tracked
pages are visible immediately; a newly created page is not, which collides with the same-turn
update discipline.

This is an owner decision, not a defect. Options:

- **Keep tracked-only.** Cheapest; retrieval reflects tracked state. The write discipline must
  then say plainly that a new page is not findable until it is added.
- **Union tracked with on-disk vault Markdown.** Finds new pages; also surfaces untracked scratch
  and anything the ignore rules deliberately exclude.

**Acceptance.** The owner is asked and the answer is recorded here and in
[`bc-wiki-maintain/CONCEPT.md`](../../../concepts/bc-wiki-maintain/CONCEPT.md). Then either
`wiki_search.py` implements it, or the read-path block states the boundary explicitly so an agent
does not read an empty result as absence. A fresh agent cannot close this item without that
answer; asking is the first step, not an optional one.

### W4 — measure whether the ranker needs a non-lexical signal

BM25 scores term counts and length only (`wiki_search.py:132-164`). Consequences: `log.md`
competes with the page its content was promoted into; superseded prose the promoter deliberately
preserves (`SKILL.md:227-243`) ranks equal to current prose; hub pages surface often enough that
the instructions tell agents to re-query around them (`SKILL.md:46-51`).

Do not change the scorer first. Extend
[`run_retrieval_benchmark_round2.py`](../../../concepts/bc-wiki-maintain/tests/run_retrieval_benchmark_round2.py)
and its `retrieval-queries-round2.tsv` with questions whose gold page is a compiled page whose
text also appears in `log.md`, then measure the current reader against **one** candidate signal —
page-kind weight or Git recency, not both.

**Acceptance.** A results file in the shape of
[`retrieval-results-round2.md`](../../../concepts/bc-wiki-maintain/tests/retrieval-results-round2.md).
Keep a signal only if the miss rate improves against the 0.15 baseline without the median
exceeding the 800-token bar (`agent-vault-read-path.md:346,398`). Note the predecessor's own
constraint: n=20 cannot rank retrievers by accuracy (`:357-359`), so a small miss-rate delta is
not evidence. A null result is a valid outcome and closes the item.

### W5 — inherit the unfinished remainder of the predecessor's W2

The predecessor's W2 acceptance required removing the wholesale index read from the promotion
runner. It is still there: `run-promotion.sh:122-123` instructs the agent to "Read the vault's
AGENTS.md, index.md, log.md". That contradicts the read path in the same concept's own skill.

**Acceptance.** The runner prompt names search-first retrieval instead of a wholesale `index.md`
read, and the promotion pressure scenario
([`tests/pressure-promotion.md`](../../../concepts/bc-wiki-maintain/tests/pressure-promotion.md))
still passes.

### W6 — catch up the eight existing vaults

W1 fixes generation only. Init preserves existing files and requires manual merge
(`bc-init-agent/body/SKILL.md:60-70`), and the upgrade note is archetype-gated, so no existing
vault is reached by W1. One pass, each vault committed in its own repo:

- All eight root `AGENTS.md` files point at the vault `AGENTS.md`, not `index.md`.
- The four thin vault files (Scripts, codebase-design, sql, CV) gain the empty-result and
  hub-page rules. Music keeps its plans-first route after the search step, per the exception at
  `SKILL.md:70-73`.

**Acceptance.** `grep -l wiki_search.py` matches all eight vault files and each contains the
empty-result and hub-page rules; no root `AGENTS.md` names `index.md` as the first read.

### W7 — reconcile the predecessor plan

`agent-vault-read-path.md` misstates its own state: `:254-257` records interactive
`$AGENT_CONCEPTS` as broken, which is fixed — `~/.zshenv:3` and
`~/.config/environment.d/agent-concepts.conf:4` both resolve correctly, and only processes started
before that fix carry the stale value.

**Do not move it to `implemented/` yet.** Its W3 (notify on scheduled-run failure, `:302-333`) is
still open and is not inherited here: no `OnFailure=` exists in either unit file. Its deferred
`map.md` link repair (`:517-519`) is likewise neither inherited nor dropped.

**Acceptance.** The predecessor's `$AGENT_CONCEPTS` paragraph is corrected; W2 and W5 are marked
with what actually landed and what this plan inherited; its W3 and the `map.md` deferral are
either kept open there or explicitly dropped with a reason. No active plan claims a fixed blocker
is live.

## Non-goals

- **Page-size, section, or corpus caps.** Growth is unbounded on both sides and the reader loads
  every eligible page per query. At 54 pages (Scripts) this is free; at 155 (image-maze) it is
  still cheap. Revisit when a vault crosses a few hundred pages.
- **Semantic deduplication or a current-state metadata schema.** The maintainer explicitly refuses
  invented frontmatter (`SKILL.md:176-178`); overturning that needs its own plan and evidence.
- **A semantic fallback for local reads.** `qmd query` took 67 seconds in the council measurement
  and is correctly excluded from the inline path.
- **List-driven promotion across all eight vaults.** Inherited deferral; still deferred.
- **Notification on scheduled-run failure.** Stays with the predecessor's W3.

## Open risks

- **W2 and W6 touch repositories outside this workspace.** Eight foreign histories, one commit
  each. The edits are mechanical but not local.
- **Normalization rewrites an append-only evidence trail.** The runner's additivity gate rejects
  non-prefix rewrites (`run-promotion.sh:216-245`), so normalization must be a human-authorized
  commit made outside the runner, never through it.
- **W1 reaches no existing vault.** That is why W6 exists; if W6 slips, the diagnosis in this plan
  is unused inventory.
- **`bc-init-agent`'s test status is `partial`** and W1 changes exactly the untested half. The
  test gate in W1's acceptance is not optional.
- **Init can scaffold a vault into a non-Git folder** (`scaffold.py:925-932` guards only
  `root.is_dir()`) where the default reader cannot run (`wiki_search.py:54-62`). Not scheduled
  here; worth a guard if it ever occurs.

## What would change this plan

- If W4 measures a real gain from a non-lexical signal, the reader stops being purely lexical and
  W3's corpus decision becomes more consequential.
- If a vault crosses a few hundred pages, the growth non-goals reopen as a measured question.
- If the owner decides the scaffold's page taxonomy should change — the open decision the
  predecessor deferred at `:441-465` — W1 should land inside that change rather than before it.
