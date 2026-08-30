# Agent vault write/read contract — make the scaffold and the maintainer agree

Date: 2026-08-29, updated 2026-08-30
Status: implemented
Verification: W1–W7 done; W5 promotion pressure **PASS 5/5** after one Gate 3 tune and contradiction rerun (2026-08-30)

## Progress (2026-08-30)

W1–W7 are implemented. W5's first post-change pressure run was **4/5**; the Gate 3 tune plus
contradiction rerun brought the combined grade to **PASS 5/5**. This plan is complete.

| Item | State | Evidence |
|---|---|---|
| W1 scaffold mints the read path | **done** | `43072a4`, hardened by `0423ada`; pressure gate passes 3/3 ([results](../../../concepts/bc-init-agent/tests/pressure-read-path-results-2026-08-29.md)) |
| W2.1 scaffold emits `## [__DATE__]` | **done** | `43072a4`; generated vault lints to a valid range |
| W2.2 normalize five existing logs | **done** | one commit in each of Scripts, sql, codebase-design, CV, image-maze; heading counts unchanged, diffs heading-only |
| W2.3 lint fails closed on `invalid` | **done** | `56cc7bd`; all eight live vaults still exit 0, a pre-normalization backlog now exits 1 |
| W3 search corpus boundary | **done** | owner chose **tracked-only** on 2026-08-29; boundary is recorded in `bc-wiki-maintain` and both canonical instruction copies; untracked-page regression passes |
| W4 non-lexical ranker signal | **done — null result** | 2026-08-30 round-two report: direct BM25 3/20 misses, 174.88 median; page-kind candidate 2/20, 179.88 median; overlapping Wilson intervals make the one-miss delta noisy, so production remains lexical |
| W5 promotion runner prompt | **done — PASS 5/5** | `6794ee3` plus Gate 3 tune `71aa735`; first post-change run 4/5; contradiction rerun cited the originating `log.md` heading/date; combined grade in [results](../../../concepts/bc-wiki-maintain/tests/pressure-promotion-results-2026-08-30.md) |
| W6 catch up eight vaults | **done** | one commit per repo; all eight vault files carry the empty-result and hub-page rules, no root file is index-first |
| W7 reconcile predecessor | **done** | `6f20b27`; the `$AGENT_CONCEPTS` blocker was re-measured, found still live, then fixed |

One finding outside the original scope, left open deliberately: five of six pressure agents
committed to a fixture repo without being asked, while correctly following the generated
"append durable discoveries to `log.md`" instruction. Whether a read-only question should
trigger a wiki write is an update-discipline decision, not a defect.
Verification: W1/W2/W3/W4/W5 implementation, W6 catch-up, and W7 reconciliation are recorded
above and below. W3's tracked-only boundary is covered by focused reader and generator tests;
W4's reproducible 20-question page-kind experiment is in
[`retrieval-results-round2.md`](../../../concepts/bc-wiki-maintain/tests/retrieval-results-round2.md)
and produced a null result. W5's runner prompt is present and the post-`6794ee3` promotion
pressure is **PASS 5/5** after one targeted tune and contradiction rerun. The original 2026-08-29 findings
below remain as baseline rationale and are labeled where their current state changed.

Successor to [`agent-vault-read-path.md`](../active/agent-vault-read-path.md), which resolved the retrieval
question and left the write side untouched. That plan proved ranked search beats every
alternative it measured: 171 median output tokens at a 0.15 miss rate, against 4,543 for an
`index.md` load (`agent-vault-read-path.md:346-348`). This plan addresses the other half of the
same goal — **a lot of knowledge the agent can traverse cheaply and effectively** — where the
knowledge is written by one concept and maintained by another that does not accept its output.

## Problem

At filing on 2026-08-29, `bc-init-agent` and `bc-wiki-maintain` were designed at different times
and shared no contract. W1/W2/W5/W6 now close the scaffold, heading, runner, and existing-vault
parts of that mismatch; W3 records the remaining tracked-only visibility boundary and W4 records
the measured ranking result. The original consequences below remain as the diagnosis that drove
the work, with their post-implementation state called out explicitly.

**Baseline diagnosis (fixed by W1): new vaults were born on the retired read path.** At filing,
`scaffold.py:40-42` emitted "Before making
non-trivial changes, read: 1. `.bc-agent/index.md`", and `scaffold.py:163` also emitted "Read
`index.md` → this file → `map.md` → `tasks/active.md`". The maintainer says the opposite:
"First move: search the vault, do not read the index"
([`SKILL.md:75`](../../../concepts/bc-wiki-maintain/body/SKILL.md)). The 2026-08-28 rollout
edited eight existing vaults by hand; it did not touch the generator that mints the ninth. Every
future vault regresses, and the rollout has to be repeated manually forever.

**Baseline diagnosis (fixed by W2): the promoter failed closed when no heading in a vault's backlog was datable.** At filing, init emitted
`## __DATE__`, rendered to `## 2026-06-26` (`scaffold.py:307`). The detector matches only
`^## \[(\d{4}-\d{2}-\d{2})\]` (`wiki_lint.py:19`). A backlog with no datable heading yields
`PROMOTION_RANGE=invalid`, and
[`run-promotion.sh:82-84`](../../../concepts/bc-wiki-maintain/body/runner/run-promotion.sh)
aborted. Lint still exited 0, so nothing surfaced it. W2 now emits detector-compatible headings,
normalizes the five affected live logs, and fails closed for an all-undatable backlog.

A mixed backlog is **not** a failure and must not be treated as one: an undatable heading narrows
the range while staying in the emitted heading list, so the classification gate still forces a
verdict on it ([`CONCEPT.md:74-77`](../../../concepts/bc-wiki-maintain/CONCEPT.md), locked by
`tests/test_wiki_maintain.py:107-119`). That behavior is deliberate and this plan does not touch
it.

**Newly created pages are invisible to the next search by deliberate choice.** The retrieval corpus
is `git ls-files` (`wiki_search.py:65-76`), read from the working tree (`:121`). Edits to tracked
pages are therefore findable immediately; a page created this turn is not findable until it is
registered with Git via `git add`. W3 records that write/read boundary and requires an agent not
to interpret an empty result as absence when an untracked page may contain the answer.

## What the 2026-08-29 sweep found (baseline)

`wiki_lint.py` against each live vault, plus `grep -c "^## \["` on each `log.md`. W1/W2/W6
corrected the generated and live surfaces after this inventory. An independent
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

Before W6, the read-path rollout was also uneven. All eight vault `AGENTS.md` files name
`wiki_search.py`, but
four (Scripts, codebase-design, sql, CV) carry the one-line form with no empty-result or hub-page
rules. And **before W6, all eight root `AGENTS.md` files routed a cold agent to `index.md` first** —
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

**Result (2026-08-30 — done).** The owner chose tracked-only with the boundary in the write/read
discipline: a newly created Markdown page is invisible until `git add` registers it with Git,
and an empty result is not proof of absence when that page may be untracked. The canonical block
in `bc-wiki-maintain/body/SKILL.md` and its generator copy in `bc-init-agent/body/scaffold.py`
state the rule. `test_wiki_search.py` proves exclusion before `git add` and visibility afterward;
`bc-init-agent/tests/test_read_contract.py` proves the two canonical copies stay synchronized.

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

**Result (2026-08-30 — done, null).** The extended 20-question corpus marks eight compiled-page
cases with exact six-or-more-token page/log overlap. The incumbent direct BM25 reader measured
3/20 misses (0.15), median 174.88 tokens; the sole page-kind candidate measured 2/20 misses
(0.10), median 179.88 tokens. Both candidate bars passed, but the Wilson intervals overlap and
the one-miss delta is therefore noisy at n=20. No production weighting was retained; the
production reader remains lexical. The reproducible per-question measurements and overlap
excerpts are in `retrieval-results-round2.md`, with deterministic coverage in
`tests/test_retrieval_benchmark_round2.py`.

### W5 — inherit the unfinished remainder of the predecessor's W2

The predecessor's W2 acceptance required removing the wholesale index read from the promotion
runner. That implementation landed in `6794ee3`: `run-promotion.sh:122-123` now names the vault
`AGENTS.md`, search-first retrieval, and relevant log entries instead of reading `index.md` and
`log.md` wholesale. The first post-change consuming-agent pressure run was **4/5**: additive-only,
runner-default, explicit-manual, and detector-first held from artifacts. Contradiction cited both
conflicting pages and carried the date, but did not explicitly cite the originating `log.md`
heading/date. Gate 3 was tuned to require that citation; the contradiction-only rerun passed.
Combined grade **PASS 5/5** is in
[`tests/pressure-promotion-results-2026-08-30.md`](../../../concepts/bc-wiki-maintain/tests/pressure-promotion-results-2026-08-30.md).

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
