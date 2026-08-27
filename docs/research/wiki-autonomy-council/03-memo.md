# Decision memo — seamless automatic wiki maintenance and cheap traversal

Supervisor: parent Pi session. Written by the supervisor, not delegated.
Date: 2026-08-26. Council: 3 advisors, 2 passes (1 cross-exam failed on quota).

## Question and scope

How to make agent-wiki maintenance run seamlessly and automatically, with the
most linked knowledge available to agents and the fewest tokens spent traversing
it. Scope, non-goals, and roster: [00-brief.md](00-brief.md).

## The finding that reframes the question

The write path is not the bottleneck. The read path is, and it barely exists.

Measured on the live vaults ([vault-reality](#evidence)):

- Zero broken links and zero ambiguous links in all nine vaults. The link
  checking works.
- 7 to 21 orphan pages per vault; up to 42% of pages unreachable from `index.md`.
- Reaching an answer in image-maze costs 4,543 tokens for `index.md` alone, or
  11,657 for index plus the three pages a typical question needs.
- `qmd query` — the designated search overlay — took **67.1 seconds**
  (57.3s expansion + 7.2s embedding). It cannot be an inline read path.
- Meanwhile `map.md`, the scaffolded "context picker" present in all nine vaults,
  writes its targets as inline code spans. `without_code()` blanks them before
  `links()` runs, so it contributes **zero** graph edges and lint has never
  validated one of its entries (verified directly; see
  [02-supervisor-findings.md](02-supervisor-findings.md) V1).

All three advisors independently reached the same resolution of the
linked-vs-cheap tension, and it is the core recommendation:

> **Change the access verb from read to filter.** Navigation should be a
> generated artifact the agent greps, not a page it loads. Then disk size scales
> with knowledge while context cost stays flat.

## Recommendation

### 1. Build a generated catalog and make filtering the first move

Add a `--write-catalog` mode to `wiki_lint.py` that emits one row per eligible
page: path, kind (from its directory), Git date, inbound count, byte size,
a deterministic summary sentence, and keywords from its `##` headings. Every one
of those fields already exists in the detector.

The agent's first move becomes a filter returning 5-20 rows (~150-500 tokens)
instead of a 4,543-token index load. Fallback order on a miss: `qmd search`
(BM25, no models), then the catalog's highest-inbound rows as a compact hub list.
**Never `qmd query`.**

This satisfies "computed triggers, never recorded triggers" by extending it to
computed *artifacts*: no hand-maintained field, invalidated by content
fingerprint or mtime. That is precisely how it avoids becoming the next `map.md`.

### 2. Fix the prescribed first move and repair `map.md`

The catalog is useless if the instructions still point elsewhere.
`scaffold.py:163` sends agents to `index.md` first, and `run-promotion.sh:122`
tells the writer to read `AGENTS.md`, `index.md`, and `log.md` — image-maze's log
alone is 49,767 tokens. Change both.

Separately, make the scaffold emit `map.md` targets as real Markdown links so
they enter the graph, and have lint validate map targets. `map.md` stays a
curated task-bundle layer; it is not the link graph and never was.

### 3. Nightly, list-driven promotion over all nine vaults

Not a dispatcher. The nightly no-ops are a **coverage** bug: the four vaults with
promotion timers hold 1 unpromoted heading between them, while the five without
hold 68. One unit looping the existing vault list takes coverage from 4/9 to 9/9.
Sol proposed a 10-minute event-driven dispatcher in Pass 1 and withdrew it in
cross-exam on this evidence.

The loop must skip-and-report per vault, never abort the batch — otherwise sql
and Scripts failing on `PROMOTION_RANGE=invalid` silently stops the other seven.

### 4. Unblock sql and Scripts at the root cause, not the parser

Both are stuck because their log headings are bare `## YYYY-MM-DD`. Two advisors
initially proposed widening the parser regex; **both retreated under
cross-examination**, and I accept the retreat.

The root cause is upstream: `scaffold.py:307` emits `## __DATE__` while
`wiki_lint.py:19` requires `## [YYYY-MM-DD]`. The scaffold has been minting
headings its own detector cannot read. Fix:

1. Scaffold emits `## [__DATE__]`.
2. Lint exits nonzero on `PROMOTION_RANGE=invalid` (today it exits 0, so the
   block is inaudible — `wiki_lint.py:527`).
3. One explicit human, non-promotion edit normalises the 13 existing headings.

This preserves `CONCEPT.md:221-226`'s deliberate human act while ensuring the
condition can never be created again.

### 5. Page contract: a summary line, still no frontmatter dates

Line 1 title, line 3 one sentence. No `updated:` or `status:` field — freshness
stays `git_date`. Warn above ~12KB; never auto-split, because a split is a
rewrite.

The strongest evidence for this is not from an advisor. The user's personal wiki
at `~/Sync/Wiki` *does* carry `updated:` frontmatter, and its daily consolidation
pass had to repair five pages whose `updated:` was objectively wrong against
`git log`. `CONCEPT.md`'s recorded rationale — "a second `updated` field would be
hand-maintained state that can drift" — is observably drifting next door and
consuming daily LLM effort to correct.

### 6. Sequencing, and the one number

1. Catalog writer plus the first-move change. **Measure: median tokens from vault
   entry to opening the correct page, over a fixed ~20-question benchmark.
   Baseline 4,543 (image-maze index). Target ≤800.**
2. List-driven promotion 9/9. Measure: total unpromoted headings across all
   vaults, 68 → <10.
3. Scaffold heading fix plus loud lint. Measure: zero `PROMOTION_RANGE=invalid`.
4. `map.md` link repair and summary lines, new pages only.

## Accepted and rejected advisor feedback

**Accepted:**

- Filter-don't-read as the core resolution (unanimous).
- Reachability means presence in the generated catalog; orphan count drops from
  goal to advisory smell (unanimous).
- Nightly 9/9 coverage over an event-driven dispatcher (Sol conceded to Grok and
  Opus on measured evidence).
- Withdrawal of silent parser widening in favour of the scaffold root-cause fix
  (Grok withdrew; Sol moved it to owner-decision).
- No bulk automatic prose linking (unanimous on policy).
- `map.md` is graph-invisible and needs repair (Opus found it; Grok and Sol
  verified it independently in cross-exam; I verified it myself).

**Rejected:**

- SQLite FTS plus a `wiki_route.py` query wrapper as the first move. It adds a
  third index beside Git and qmd, and requires a binary where a shell filter
  suffices. Largest eligible graph is 151 pages. Revisit only if a measured probe
  shows plain filtering and `qmd search` both miss.
- The 10-minute polling dispatcher, on the coverage evidence above and because
  "log.md quiet for 10 minutes" is a poor session proxy — capture is a cheap
  mid-task act, so a quiet log does not mean the session ended.

**Corrected — an advisor claim I checked and found wrong:**

Grok and Opus both asserted that Gate 1's byte-prefix check mechanically
prevents inserting a link into an existing page. **That is false.**
`run-promotion.sh:226` is `[[ "$deleted" == '0' ]] && continue` — a file with zero
deleted lines short-circuits the check entirely, so mid-file insertion passes.
`CONCEPT.md` says so explicitly, because the curated `index.md` link appends
depend on it. Sol caught this and I verified it at the source.

This matters: the prohibition on automatic linking is a **policy** choice, not a
mechanical guarantee. Anyone who later relies on "the gate won't let it happen"
will be wrong. If bulk auto-linking is to be prevented, something must actually
enforce it.

## Owner decisions

1. **Where the catalog lives — the one genuinely unresolved dispute.** The
   advisors *diverged* here rather than converging. Grok moved to
   `$XDG_CACHE_HOME` (untracked, disposable, no Syncthing exposure); Sol moved to
   a tracked in-vault `catalog.md` (clone-portable, links validated by existing
   lint); Opus proposed gitignored in-vault.

   Verified hazard: `maintenance_report()` excludes only `_meta/` files prefixed
   `lint-`, `health-check-`, or `semantic-consolidation-`, and `_meta` is not in
   `SKIP_DIR_NAMES`. A Syncthing conflict copy (`_meta/catalog.sync-conflict-*.md`)
   would therefore enter the page walk and be counted as a page. This applies to
   **any** in-vault Markdown catalog, tracked or not.

   *My recommendation:* do not decide this yet. Start with the disposable cache —
   it is the cheapest, touches no gate, and is trivially reversible — then run the
   step-1 benchmark. Only promote it to a tracked artifact if the read path
   demonstrably works. Sequencing dissolves the dispute: you do not need to choose
   a location before you know the approach earns one.

2. **Silent failure is unaddressed by every proposal, including mine.** The
   personal wiki's stranded PID lock "silently skipped every scheduled run for
   seven weeks," visible as the 2026-06-30 → 2026-08-19 gap. Today, 2026-08-26,
   its consolidation timed out after 24 minutes; the wrapper caught it and wrote
   `status: needs-review`. The catch is the model to copy; the seven weeks are the
   failure mode to design against. A "seamless and automatic" system needs an
   answer to *how the user learns it stopped working*. Nothing in the current
   runner or any advisor proposal has one.

3. **Whether to port rather than invent.** `~/Sync/Wiki` already achieves the
   target state — 379 pages, 0 broken links, 0 orphans, 0 missing index entries —
   under daily unattended LLM maintenance that commits. Its
   `wiki_semantic_consolidation.py` is 5,983 bytes. Before building new machinery,
   decide whether that pass should be adapted for project vaults.

4. Whether `dng` (unregistered in qmd, absent from the lint list, last commit
   2026-06-08) is in scope.

5. Whether Music's first unattended promotion run (37 headings) is allowed to run
   unattended, or gets one manual pass first.

## Confidence

**Medium-high on the diagnosis, medium on the prescription.**

The diagnosis is verified against source and the live machine, much of it by me
rather than by advisor report: the `map.md` code-span defect, the Gate 1
short-circuit, the `maintenance_report` prefix gap, the timer-coverage
distribution, and the 67-second qmd measurement.

The prescription's core bet — that filtering a generated keyword table reliably
reaches the right page — is **unmeasured**. All three advisors flagged the same
gap and each proposed a falsification test. That convergence on what is unproven
is the most useful thing the council produced, and it is why step 1 ships with a
benchmark rather than a promise.

## What would change the decision

- The step-1 benchmark showing filtering misses the right page more than ~30% of
  the time. Then filter-don't-read fails, and the answer is a small generated
  index that is read, or a cheap local embedding step.
- `qmd search` (BM25, not `query`) measuring genuinely fast and accurate on these
  corpora. Then the catalog shrinks to a fallback for the three unregistered
  vaults, and the fix is mostly a one-line first-move change.
- Evidence that mtime is unreliable under Syncthing here. Then the cache cannot
  self-invalidate and must be tracked, which forces owner decision 1 immediately.

## Run record

| item | value |
|---|---|
| Roster | `council-grok` (xai/grok-4.6 high), `council-sol` (openai-codex/gpt-5.6-sol high), `council-opus` (claude-bridge/claude-opus-5 high) |
| Context mode | all three `fresh` (profile `defaultContext: fresh`), requested explicitly |
| Passes | 2 (independent reports, then one curated cross-exam) |
| Evidence tracks | `researcher` (sources), `scout` (vault reality) — run 56a73023 |
| Pass 1 | run 55d098ca — grok c1790dd1, sol 7fab90ff, opus 79cb8d10 — 3/3 complete |
| Pass 2 | run a54a44c0 — grok dee6b54b, sol 01a59ed6 — 2/3 complete |
| Fallback | `cross-opus` failed twice: first a mutation-capability check on the `output:` path, then a hard Opus quota (resets 20:10). No artifact was produced; recovery confirmed nothing salvageable. Opus's Pass 1 report stands **uncross-examined**. |

### Disclosures

- **Asymmetric evidence.** The `~/Sync/Wiki` finding arrived after Grok and Sol
  were dispatched for Pass 2. Only Opus's retry packet contained it, and that run
  never completed. So no advisor has responded to the most consequential evidence
  in this memo; sections citing it are supervisor analysis, unreviewed by the
  council.
- **A relayed figure was imprecise.** My Pass 2 packet repeated "Music's map omits
  34 of 69 pages" from Opus. Sol checked it: the map names 11 unique files, so it
  omits 58 of 69; the 34 was a different subtraction. The underlying point stands,
  the number I relayed did not.
- **A scout undercount.** `vault-reality.md` reports 5 installed timers; there are
  7. The two it missed belong to the personal wiki, not to `bc-wiki-maintain`.
- **Grok corrected its own citation** mid-run: the human-normalisation rule is
  `CONCEPT.md:221-226`, not `:96-97`.

### Evidence

Full artifacts (ephemeral, `/tmp/bc-swarm/2026-08-26-wiki-autonomy/`):
`sources.md`, `vault-reality.md`, `pass1/{grok,sol,opus}.json`,
`pass2/aggregate.json`, `manifest.md`.

Durable in this folder: [00-brief.md](00-brief.md),
[01-claim-matrix.md](01-claim-matrix.md),
[02-supervisor-findings.md](02-supervisor-findings.md).
