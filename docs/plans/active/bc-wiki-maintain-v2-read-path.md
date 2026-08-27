# `bc-wiki-maintain` v2 — the read path

Date: 2026-08-27
Status: active
Verification: nothing implemented yet; W4 is the go/no-go harness (baseline 4,543 tokens, bars: median ≤800 and miss rate ≤0.30)

Derived from the council memo at
[`docs/research/wiki-autonomy-council/03-memo.md`](../../research/wiki-autonomy-council/03-memo.md).
That memo diagnoses; this plan is the approved slice of its prescription, with the owner
decisions resolved and the memo's source claims re-verified against current code.

## Problem

`bc-wiki-maintain` invests in the write path — promotion, gates, link validation — and that
part works. The council's measurement is that the read path is the bottleneck and barely
exists.

Measured 2026-08-26 across the nine vaults that then qualified (that set includes `dng`, which
[decision 4](#resolved-decisions) later put out of scope; every *forward-looking* count in this
plan is over the 8 lint-list vaults):

- Zero broken links and zero ambiguous links in every vault. Validation works.
- 7 to 21 orphan pages per vault; up to 42% of pages unreachable from `index.md`.
- Reaching an answer in image-maze costs **4,543 tokens for `index.md` alone**, or 11,657 for
  index plus the three pages a typical question needs.
- `qmd query`, the designated search overlay, took **67.1 seconds** (57.3s expansion + 7.2s
  embedding). It cannot sit in an inline read path.
- `map.md`, the scaffolded "context picker" present in every vault, writes its targets as
  inline code spans. `without_code()` blanks them before `links()` runs, so it contributes
  **zero** graph edges and lint has never validated one of its entries.

The tension is between wanting the most linked knowledge available and wanting the fewest
tokens spent reaching it. All three advisors resolved it the same way, and that resolution is
this plan's core bet:

> **Change the access verb from read to filter.** Navigation becomes a generated artifact the
> agent greps, not a page it loads. Disk size then scales with knowledge while context cost
> stays flat.

That bet is **unmeasured**. Every advisor flagged the same gap. This is why W4 is a harness
rather than a promise, and why the rest of the memo is deferred behind it.

## Scope

**This plan is step 1 of the memo's four-step sequence, and only step 1.** Steps 2 through 4
are deferred until W4 clears its bars. See [Deferred](#deferred).

One addition to the memo's step 1: failure notification (W3) is in scope, because a
"seamless and automatic" system whose failures are invisible is the failure mode the personal
wiki already demonstrated for seven weeks.

## Resolved decisions

The memo left five owner decisions open. All five were answered on 2026-08-27.

1. **Catalog location — deferred by design.** Start with a disposable cache under
   `$XDG_CACHE_HOME`. Run the benchmark. Promote it to a tracked in-vault artifact only if the
   read path demonstrably works. This touches no gate and is trivially reversible.
   Sequencing dissolves the advisors' one genuine disagreement: the location does not need
   deciding before the approach earns one.
2. **Silent failure — a desktop notification.** In scope for this plan, not deferred.
3. **Port vs. invent — evaluate adapting `~/Sync/Wiki`'s machinery first.** Done; see
   [What recon corrected](#what-recon-corrected-in-the-memo), finding C. The verdict is that
   the *script* is not portable and its *bugs* do not transfer either, because the project
   runner is bash with no lock. What W3 takes is one idea: write a durable, visible artifact
   when a run fails.
4. **`dng` — out of scope.** It is unregistered in qmd, absent from the lint vault list, and
   last committed 2026-06-08. Forward-looking counts are over the **8** vaults in the lint
   list, not the memo's 9. Historical measurements keep their original scope and are labelled.
5. **Music's first unattended promotion run (37 headings) — allowed to run unattended.**
   This decision is closed; see [Deferred](#deferred) item 2, where it applies.

## What recon corrected in the memo

Two read-only scouts re-verified the memo's source claims against current code on 2026-08-27.
All seven of its defect claims are **VERIFIED and still live**. Four supporting details needed
correction, and one of them changes the work.

**A. The scaffold is in a different concept.** The memo cites `scaffold.py:163` and
`scaffold.py:307` with no concept path. The file is `concepts/bc-init-agent/body/scaffold.py`
(`:163` for the first move, `:307` for `## __DATE__`, `:269-271` for the code-span map
targets). **This makes W2 a cross-concept change**, touching `bc-init-agent` as well as
`bc-wiki-maintain`, with both concepts' `CONCEPT.md` needing the update.

**B. Coverage is 4 of 8, not 4 of 9.** The lint list at
`~/.config/agent-concepts/wiki-lint-vaults.txt` holds 8 vaults. Four have promotion timers (CV,
image-maze, public Homeflix, homeflix-prod); four do not (Music, Scripts, codebase-design, sql).
The memo's 9th vault is `dng`, now out of scope; it holds 0 unpromoted headings, so the 68
total is unchanged by dropping it. The memo's separate claim of 5 installed timers vs. 7
resolves the same way: the two extra timers belong to the personal wiki, not to
`bc-wiki-maintain`.

**C. The personal wiki's consolidation script is not portable, and neither are its bugs.**
`~/Sync/Wiki/scripts/wiki_semantic_consolidation.py` (151 lines) is a wrapper around a `pi`
call, not a semantic algorithm. It derives its root from its own file location and hard-codes
`ROOT / "wiki"`, `wiki/_meta`, and the personal category vocabulary
(`sources`/`entities`/`concepts`/`questions`/`syntheses`) into its prompt. A project vault is
root-shaped (`.bc-agent/` with `plans`/`components`/`findings`/`decisions`) with a different
frontmatter schema. Porting it would mean parameterising the root, every vault-relative path,
the prompt template, and the git staging allowlist — at which point little of the original
remains. It does **not** depend on `updated:` frontmatter, which removes one objection to reuse
but does not rescue the rest.

Its two known defects — a stranded PID lock that returned 0 for seven weeks, and an uncaught
`TimeoutExpired` that bypasses the fallback report — are **specific to that Python wrapper**.
`run-promotion.sh` contains no lock at all, and its unit sets `TimeoutStartSec=30min`. W3 must
not import defences against bugs this runner cannot have.

**D. Two smaller figures were off.** `wiki_lint.py`'s exit line is `:526`, not `:527`. The
personal wiki is **383** pages as of 2026-08-27, not 379; its 0 broken / 0 orphan result was
reproduced that day, but under its own linter's rules, not an independent graph check.

## Work items

### W1 — `wiki_lint.py --write-catalog`

Emit one row per eligible page: path, kind, Git date, inbound count, byte size, a deterministic
summary sentence, and keywords from the page's `##` headings. Write to
`${XDG_CACHE_HOME:-$HOME/.cache}/agent-concepts/wiki-catalog/<vault-slug>.tsv`.

Recon inventoried what already exists, which is less than the memo implied:

| Field | Status | Existing code |
|---|---|---|
| path | exists | `rel()` at `wiki_lint.py:62-63` |
| Git date | exists | `git_date()` at `:130-138` — currently called only for active references, would need calling per page |
| inbound count | exists internally | `incoming` counter at `:316`, `:324-330`; `lint()` returns aggregate `orphans`, not the per-page map |
| kind | **new** | — |
| byte size | **new** | — |
| summary sentence | **new** | — |
| heading keywords | **new** | — |

Three fields are reusable and four are new work, plus the CLI mode itself. `kind` derives from
the containing directory. The summary sentence must be **deterministic** — the first sentence of
the page body, taken *after* any YAML frontmatter and truncated — and never model-generated: a
generated-by-LLM field would reintroduce exactly the hand-maintained staleness this design
exists to avoid. Many live pages begin with `---`, so the frontmatter skip is load-bearing, not
defensive.

`<vault-slug>` cannot be `basename`: public Homeflix and homeflix-prod are both `.agent` and
would collide. Derive it from enough of the path to be unique across the lint list.

Invalidation is by content fingerprint or mtime. No hand-maintained field. This extends the
concept's "computed triggers, never recorded triggers" rule to computed *artifacts*, and it is
precisely what keeps the catalog from becoming the next `map.md`.

**Acceptance:**
- `--write-catalog` produces **8 distinct** TSV files, one per lint-list vault, with no slug
  collision between the two `.agent` vaults.
- Each file has a header row and exactly 7 columns; every row carries all 7 fields populated.
- Row count equals the eligible-page count under the rule stated in the mode's `--help`, and
  that rule is stated explicitly rather than left to the reader.
- Every row's Git date equals `git log -1 --format=%cs` for that file.
- For a page whose body starts with YAML frontmatter, the summary column contains body prose,
  not `---` or a frontmatter key.
- Regenerating with no content change produces a byte-identical file.
- **New tests cover `--write-catalog`.** The existing 25 tests in
  `concepts/bc-wiki-maintain/tests/` contain no catalog cases, so "the suite still passes" is
  not coverage of this work; it is only a regression check, and is also required.

### W2 — Make filtering the actual first move

The catalog is inert if the instructions still send agents elsewhere. This is a cross-concept
change with a template half and a live half.

**Templates.** `concepts/bc-init-agent/body/scaffold.py` at `scaffold.py:163` (with the parallel
prose at `:40-45`, `:593`, and `:602`) tells agents to read `index.md` first.
`concepts/bc-wiki-maintain/body/runner/run-promotion.sh` at `run-promotion.sh:122` tells the
promotion writer to read `AGENTS.md`, `index.md`, and `log.md`; image-maze's log alone is 49,767
tokens. Note these are two different readers — the task agent and the promotion writer — and both
need changing.

**Live vaults.** The scaffold is deliberately additive: it "creates only the files that are
missing and leaves every existing file untouched" (`concepts/bc-init-agent/CONCEPT.md`).
Re-running it therefore changes **nothing** in the eight existing vaults, whose `AGENTS.md`
still orders `index.md` first. A template-only change would leave the 4,543-token load in place
on precisely the vault W4 measures, making the benchmark meaningless. The live vault
instructions are in scope. Use the scaffold's existing upgrade-notes path (it prints notes for
the running agent to merge by hand) rather than inventing a migration.

**Cold-cache behaviour.** The prescribed first move must handle a missing or stale catalog by
running `--write-catalog` and then filtering. A first move that assumes a file nobody has
generated is not a read path.

Fallback order on a filter miss: `qmd search` (BM25, no models), then the catalog's
highest-inbound rows as a compact hub list. **Never `qmd query`** — 67 seconds disqualifies it
from any inline path.

**Acceptance:**
- Each named surface — `scaffold.py:163`, `:40-45`, `:593`, `:602`, `run-promotion.sh:122`, and
  each of the 8 live vault `AGENTS.md` — **positively states** that filtering the catalog is the
  first move, names the fallback chain, and excludes `qmd query`. Deleting the `index.md`
  sentence without naming the catalog does not pass.
- image-maze's live `AGENTS.md` no longer names `index.md` as the first read.
- With the TSV deleted, following the prescribed first move regenerates the catalog and uses it.
- Both `CONCEPT.md` files record the change.
- The existing `bc-wiki-maintain` pressure scenario is re-run and still holds, extended with one
  case covering the new first move. This is a deployed discipline rule; the workspace test gate
  applies.

### W3 — Notify when a scheduled run fails

Today nothing tells the user a scheduled run failed. Recon confirmed `OnFailure=` is unset and
`FailureAction=none` on every wiki unit; the only signals are journald, systemd state, and a
committed `status: needs-review` file the user has to go looking for. The seven-week gap
(2026-06-30 → 2026-08-19) is confirmed against Git artifacts, with the retained journal showing
`Lock exists, skipping` then `Finished` on each of 2026-08-12 through 08-18 — the run returned
0, so systemd reported success while nothing happened.

**What counts as a failure here.** `run-promotion.sh` has no lock, so it has no silent-skip path
to defend against. Its early exits are:

- dirty tree (`:42-48`), detection failure (`:59-61`), invalid range (`:83-85`) — all `fail`,
  exit 1. **Notify on these.**
- nothing to promote (`:74-80`) — `exit 0`, a legitimate no-op. **Do not notify.** Treating the
  healthy case as an alert is how notifications get ignored.

Add `OnFailure=` to the `bc-wiki-maintain` and `bc-wiki-lint` unit templates. The notifier must
be **runner-local** and must **exit nonzero if it cannot display**. It must not be
`~/Sync/Scripts/lib/notify.sh`: that helper is documented as a "silent no-op (exit 0)" when
headless, which recreates the exact failure mode this work item exists to close, and this
repository may not depend on one person's machine.

Do **not** port the personal wrapper's PID lock or `TimeoutExpired` handling. Those defend a
Python wrapper's bugs; this runner is bash and its unit already sets `TimeoutStartSec=30min`.

**Acceptance:**
- A deliberately failed run — e.g. a dirty tree, which is an existing exit-1 path — produces a
  visible desktop notification naming the vault and the reason.
- A no-op run (`PROMOTION_REQUIRED=0`) produces no notification.
- If the notifier cannot display, the run fails loudly rather than exiting 0.
- The `OnFailure=` wiring is committed in the runner templates in this repository, not only
  installed locally.

### W4 — The benchmark

This is the go/no-go for steps 2-4. It must be a harness, not an intention: two workers running
it should get comparable numbers.

Fix a question set against image-maze, the largest vault. For each question record the tokens
spent from vault entry to opening the correct page, and whether the correct page was reached.

- **Baseline: 4,543 tokens** — image-maze `index.md` alone, derived as 18,172 bytes ÷ 4.
- **Tokenizer: bytes ÷ 4**, the same derivation, so the comparison is like-for-like. Not an API
  usage counter and not tiktoken; those produce a different number against the same baseline.

**Acceptance:**
- A question file of **exactly 20** questions is committed under
  `concepts/bc-wiki-maintain/tests/`, each with the gold page path that answers it.
- That file is committed **before** any catalog tuning. Otherwise the benchmark measures the
  tuning rather than the approach.
- The runbook names the agent, the loop, and what counts as "opening" a page and as a miss,
  precisely enough that a second operator reproduces it.
- A results artifact records per-question tokens and hit/miss, plus the computed median and
  miss rate.
- **Bars: median ≤800 tokens and miss rate ≤0.30.** Both must hold. A miss rate above 0.30
  falsifies filter-don't-read; the answer then becomes a small generated index that *is* read,
  or a cheap local embedding step — not this design.

## Non-goals

- No bulk automatic linking of prose. Unanimous advisor policy, and note that this is a
  **policy** choice, not a mechanical guarantee — see [Open risks](#open-risks).
- No SQLite FTS and no `wiki_route.py` query wrapper. It would add a third index beside Git and
  qmd, and needs a binary where a shell filter suffices; the largest eligible graph is 151
  pages. Revisit only if W4 shows plain filtering *and* `qmd search` both miss.
- No event-driven or polling dispatcher. Sol proposed a 10-minute poll in Pass 1 and withdrew
  it under cross-examination: the nightly no-ops are a coverage bug, not a latency bug, and
  "log.md quiet for 10 minutes" is a poor session proxy because capture is a cheap mid-task act.
- No `updated:` or `status:` frontmatter field. Freshness stays `git_date`. The evidence is
  next door: the personal wiki carries `updated:` and its daily pass had to repair five pages
  whose value was objectively wrong against `git log`.
- No auto-splitting of large pages. Warn above ~12KB; a split is a rewrite.
- No changes to the promotion gates in this plan.
- No PID lock added to `run-promotion.sh`. If concurrent promotion runs ever become a real
  problem, that is its own change with its own evidence.

## Deferred

Blocked on W4 clearing its bars. Recorded here so the sequence is not lost:

2. **List-driven promotion across all 8 vaults.** One unit looping the existing vault list,
   taking coverage from 4/8 to 8/8. Must skip-and-report per vault, never abort the batch —
   otherwise sql and Scripts failing on `PROMOTION_RANGE=invalid` silently stops the other six.
   Measure: total unpromoted headings, 68 → <10. Music's first run (37 headings) is allowed to
   proceed unattended — [decision 5](#resolved-decisions) is closed, do not re-open it.
3. **Scaffold heading fix plus loud lint.** `scaffold.py:307` emits `## __DATE__` while
   `wiki_lint.py:19` requires `## [YYYY-MM-DD]` — the scaffold has been minting headings its
   own detector cannot read. Fix at the root (scaffold emits `## [__DATE__]`), make
   `wiki_lint.py:526` exit nonzero on `PROMOTION_RANGE=invalid`, and let one explicit human
   edit normalise the 13 existing headings. Widening the parser regex was proposed by two
   advisors and **withdrawn by both** under cross-examination; do not revive it.
   Measure: zero `PROMOTION_RANGE=invalid`.
4. **`map.md` link repair and summary lines.** Emit map targets as real Markdown links so they
   enter the graph, and have lint validate them. `map.md` stays a curated task-bundle layer; it
   is not the link graph and never was. Summary lines on new pages only.

## Open risks

- **The core bet is unmeasured.** Stated plainly because W4 exists to resolve it, not to
  confirm it.
- **Gate 1 does not mechanically prevent automatic linking.**
  `run-promotion.sh:226` is `[[ "$deleted" == '0' ]] && continue`, so a file with zero deleted
  lines short-circuits the byte-prefix check and mid-file insertion passes. This is deliberate —
  the curated `index.md` link appends depend on it — but it means the no-bulk-linking rule is
  policy, not enforcement. Anyone who later relies on "the gate won't let it happen" will be
  wrong. If it must be enforced, something has to actually enforce it.
- **Any in-vault Markdown catalog is exposed to Syncthing conflict copies.**
  `maintenance_report()` (`wiki_lint.py:291-298`) excludes only `_meta/` files prefixed `lint-`,
  `health-check-`, or `semantic-consolidation-`, and `_meta` is not in `SKIP_DIR_NAMES`. A
  `_meta/catalog.sync-conflict-*.md` would enter the page walk and be counted as a page. This
  applies to a tracked *or* gitignored in-vault catalog, and is a direct argument for the cache
  location in decision 1. **This risk is not hypothetical here:** during the session that wrote
  this plan, `docs/research/wiki-autonomy-council/` was renamed to `…_1` mid-session by exactly
  this class of event.
- **`mtime` reliability under Syncthing is unverified.** If mtime is unreliable, the cache
  cannot self-invalidate and must be tracked, which forces decision 1 immediately. Fingerprint
  invalidation is the hedge.
- **W2 edits files in eight other repositories.** The live-vault half is necessary for W4 to
  mean anything, but it is a wider blast radius than a template change and each vault is
  someone's working tree.
- **No advisor reviewed the `~/Sync/Wiki` evidence.** It arrived after Grok and Sol were
  dispatched for Pass 2; only Opus's retry packet contained it, and that run died on quota.
  The sections of the memo resting on it are supervisor analysis, uncrossed by the council.

## What would change this plan

- W4 missing either bar — median above 800 or miss rate above 0.30 — changes the design, not
  just the tuning.
- `qmd search` (BM25, not `query`) measuring fast and accurate on these corpora — the catalog
  shrinks to a fallback for unregistered vaults, and W2 becomes a one-line first-move change.
- Evidence that mtime is unreliable under Syncthing — forces decision 1 now rather than after
  the benchmark.
