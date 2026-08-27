# Agent vault read path — cheap traversal across `bc-init-agent` and `bc-wiki-maintain`

Date: 2026-08-27
Status: active
Verification: nothing implemented yet; W4 is the go/no-go harness (baseline 4,543 tokens, bars: median ≤800 and miss rate ≤0.30)

Derived from the council memo at
[`docs/research/wiki-autonomy-council/03-memo.md`](../../research/wiki-autonomy-council/03-memo.md),
then widened on 2026-08-27 when the owner named the actual goal: **a lot of knowledge the agent
can traverse cheaply and effectively.** Two concepts serve that goal and neither does it alone.
`bc-init-agent` decides the shape knowledge is written into; `bc-wiki-maintain` keeps that shape
true over time. A read path built in one and undermined by the other is not a read path.

## Problem

`bc-wiki-maintain` invests in the write path — promotion, gates, link validation — and that
part works. The council's measurement is that the read path is the bottleneck and barely exists.

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

**Step 1 of the memo's four-step sequence, plus the two things that step depends on and the
memo did not cover:** failure notification (W3), because a system whose failures are invisible
is the failure mode the personal wiki demonstrated for seven weeks; and the `bc-init-agent`
template surfaces (W5), because the scaffold writes the navigation instructions that W2 changes,
and leaving them contradictory would reintroduce the old first move in every new vault.

Memo steps 2 through 4 remain deferred until W4 clears its bars. See [Deferred](#deferred).

## Resolved decisions

The memo left five owner decisions open. All five were answered on 2026-08-27.

1. **Catalog location — deferred by design.** Start with a disposable cache under
   `$XDG_CACHE_HOME`. Run the benchmark. Promote it to a tracked in-vault artifact only if the
   read path demonstrably works. This touches no gate and is trivially reversible.
   Sequencing dissolves the advisors' one genuine disagreement: the location does not need
   deciding before the approach earns one.
2. **Silent failure — a desktop notification.** In scope for this plan, not deferred.
3. **Port vs. invent — evaluate adapting `~/Sync/Wiki`'s machinery first.** Done; see
   [finding C](#what-recon-corrected-in-the-memo). The verdict is that the *script* is not
   portable and its *bugs* do not transfer either, because the project runner is bash with no
   lock. W3 takes one idea: write a durable, visible artifact when a run fails.
4. **`dng` — out of scope.** It is unregistered in qmd, absent from the lint vault list, and
   last committed 2026-06-08. Forward-looking counts are over the **8** vaults in the lint
   list, not the memo's 9. Historical measurements keep their original scope and are labelled.
5. **Music's first unattended promotion run (37 headings) — allowed to run unattended.**
   Closed; see [Deferred](#deferred) item 2, where it applies.

## What recon corrected in the memo

Three read-only recon passes on 2026-08-27 verified the memo's claims and then surveyed both
concepts. All seven of the memo's defect claims are **VERIFIED and still live**.

**A. The scaffold is in a different concept.** The memo cites `scaffold.py:163` and
`scaffold.py:307` with no concept path. The file is `concepts/bc-init-agent/body/scaffold.py`.
This is what makes the plan cross-concept.

**B. Coverage is 4 of 8, not 4 of 9.** The lint list holds 8 vaults. Four have promotion timers
(CV, image-maze, public Homeflix, homeflix-prod); four do not (Music, Scripts, codebase-design,
sql). The 9th vault was `dng`, now out of scope; it holds 0 unpromoted headings, so the 68 total
is unchanged.

**C. The personal wiki's consolidation script is not portable, and neither are its bugs.**
`~/Sync/Wiki/scripts/wiki_semantic_consolidation.py` (151 lines) wraps a `pi` call. It derives
its root from its own file location, hard-codes `ROOT / "wiki"`, and bakes the personal category
vocabulary into its prompt. Its two known defects — a stranded PID lock that returned 0 for seven
weeks, and an uncaught `TimeoutExpired` that bypasses the fallback report — are specific to that
Python wrapper. `run-promotion.sh` contains no lock at all, and its unit sets
`TimeoutStartSec=30min`. W3 must not import defences against bugs this runner cannot have.

**D. Two smaller figures were off.** `wiki_lint.py`'s exit line is `:526`, not `:527`. The
personal wiki is **383** pages as of 2026-08-27, not 379.

## What the vault survey found

The catalog design assumed the live vaults resemble the scaffold template. They do not. This
section is the evidence behind the changes to W1, W2, and W5.

**Directory taxonomy has diverged past the point where a directory name identifies content.**
Across the 8 vaults there are **27 distinct top-level directories**. Only six are universal
(`templates`, `tasks`, `references`, `project`, `decisions`, `conventions`). Seven appear in a
single vault — `temp`, `scripts`, `_meta`, `autoresearch`, `agents` among them — and were
invented by agents over time, not created by any scaffold archetype. Worse, names collide across
archetypes with different meanings: `concepts/` is "distilled explanations in the learner's
words" under the learning archetype but "reusable ideas and patterns" under knowledge; `plans/`
is an ops directory while code vaults put plans in `project/`. A `kind` field derived from a
directory *basename* would silently conflate these.

**The scaffold emits no YAML frontmatter anywhere,** and its page templates open with headings,
`Date:`/`Status:` prose lines, and `**TODO:** fill` placeholders. A deterministic
"first sentence of the body" extractor run against them returns navigation boilerplate or a TODO,
not a summary. This is not a frontmatter-skipping problem; it is that the content the extractor
wants often does not exist yet.

**A third of the benchmark vault is gitignored.** image-maze has 239 Markdown files, of which
**84 are under a gitignored `temp/`** (`.gitignore:9`). `git log -1 --format=%cs` returns empty
for every one, so the catalog's Git-date column would be blank for 35% of that vault. Excluding
ignored paths leaves **155 eligible pages**, which matches the memo's independently derived
"largest eligible graph is 151 pages". Tracked-only is therefore the correct eligibility rule and
it is settled by evidence, not preference.

**The first-move instruction has drifted into at least three variants.** Scripts, CV,
codebase-design, and sql share one line; image-maze and both Homeflix vaults add a parenthetical;
Music's is a different workflow entirely (`index.md` → `plans/` page → its open-questions). Four
of the eight carry a *second* `**START**` paragraph repeating the sequence. The two Homeflix
vaults also lack most base scaffold files, including all four `conventions/` pages. W2 is
therefore eight separate edits, not a find-and-replace.

**Sizes, for the token estimate.** Pages range from 37 (sql) to 239 (image-maze); Markdown bytes
from 37KB to 1.53MB. `log.md` is the largest page in five of eight vaults, reaching **199,069
bytes in image-maze** — roughly 50,000 tokens, which is why `run-promotion.sh` telling its writer
to read the log is expensive.

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

Three fields are reusable and four are new work, plus the CLI mode itself.

**`kind` is the vault-relative directory path, not the basename.** The survey found 27 distinct
directories with colliding names across archetypes. `concepts` alone is ambiguous; `wiki/concepts`
and `concepts` are not. Pages at the vault root get an explicit root kind rather than an empty
field.

**Eligibility is tracked files only.** Exclude anything `git check-ignore` matches, which removes
image-maze's 84 `temp/` pages, and keep the existing `SKIP_DIR_NAMES` exclusions. A page with no
Git date is not a knowledge page; it is an artifact.

**The summary must be deterministic and must degrade honestly.** Take the first sentence of the
page body after any YAML frontmatter. Because the scaffold's templates open with TODOs and
boilerplate, the extractor will often find no real prose — in that case emit the page title
rather than a `**TODO:** fill` string, and never fabricate. Never model-generate this field: a
generated-by-LLM summary would reintroduce exactly the hand-maintained staleness this design
exists to avoid.

**`<vault-slug>` cannot be `basename`:** public Homeflix and homeflix-prod are both `.agent` and
would collide. Derive it from enough of the path to be unique across the lint list.

Invalidation is by content fingerprint or mtime. No hand-maintained field. This extends the
concept's "computed triggers, never recorded triggers" rule to computed *artifacts*, and it is
precisely what keeps the catalog from becoming the next `map.md`.

**Acceptance:**
- `--write-catalog` produces **8 distinct** TSV files, one per lint-list vault, with no slug
  collision between the two `.agent` vaults.
- Each file has a header row and exactly 7 columns; every row carries all 7 fields populated.
- For image-maze specifically, the row count is **155**, not 239: no gitignored `temp/` page
  appears.
- Every row's Git date equals `git log -1 --format=%cs` for that file, and no row has an empty
  date.
- `kind` for a page under a nested `wiki/concepts/` directory is distinguishable from one under a
  top-level `concepts/` directory.
- For a page whose body starts with YAML frontmatter, the summary column contains body prose. For
  a page whose body is still a scaffold TODO, the summary is the page title, not the TODO text.
- Regenerating with no content change produces a byte-identical file.
- **New tests cover `--write-catalog`.** The existing 25 tests in
  `concepts/bc-wiki-maintain/tests/` contain no catalog cases, so "the suite still passes" is not
  coverage of this work; it is only a regression check, and is also required.

### W2 — Make filtering the actual first move in the live vaults

The catalog is inert if the instructions still send agents elsewhere. The scaffold is
deliberately additive — it "creates only the files that are missing and leaves every existing
file untouched" (`concepts/bc-init-agent/CONCEPT.md`) — so re-running it changes **nothing** in
the eight existing vaults. Template changes are W5; this item is the live half, and without it
W4 measures a vault that still loads a 4,543-token index.

Eight separate edits, because the instruction has drifted into at least three variants and four
vaults carry a second `**START**` paragraph:

| Vault | Surface |
|---|---|
| Scripts, CV, codebase-design, sql | `AGENTS.md:21`, shared wording |
| image-maze | `AGENTS.md:26` plus `START` at `:61-62` |
| Homeflix-public, Homeflix-prod | `AGENTS.md:35` plus `START` at `:66-68` |
| Music | `AGENTS.md:26` plus `START` at `:39-41` — a different workflow (`index.md` → `plans/` page → open-questions), so it needs its own rewrite rather than the shared line |

Also change `concepts/bc-wiki-maintain/body/runner/run-promotion.sh` at `run-promotion.sh:122`,
which tells the promotion writer to read `AGENTS.md`, `index.md`, and `log.md`. That is a
different reader from the task agent, and image-maze's log alone is 199,069 bytes.

**Cold-cache behaviour.** The prescribed first move must handle a missing or stale catalog by
running `--write-catalog` and then filtering. A first move that assumes a file nobody has
generated is not a read path.

Fallback order on a filter miss: `qmd search` (BM25, no models), then the catalog's
highest-inbound rows as a compact hub list. **Never `qmd query`** — 67 seconds disqualifies it
from any inline path.

**Acceptance:**
- All 8 live `AGENTS.md` files, and every `START` paragraph among them, **positively state** that
  filtering the catalog is the first move, name the fallback chain, and exclude `qmd query`.
  Deleting the `index.md` sentence without naming the catalog does not pass.
- Music's variant preserves its plans-first intent rather than being overwritten with the shared
  line.
- `run-promotion.sh` no longer directs its writer to read `log.md` wholesale.
- With the TSV deleted, following the prescribed first move regenerates the catalog and uses it.
- `bc-wiki-maintain`'s `CONCEPT.md` records the change.
- The existing `bc-wiki-maintain` pressure scenario is re-run and still holds, extended with one
  case covering the new first move. This is a deployed discipline rule; the workspace test gate
  applies.

### W3 — Notify when a scheduled run fails

Today nothing tells the user a scheduled run failed. Recon confirmed `OnFailure=` is unset and
`FailureAction=none` on every wiki unit; the only signals are journald, systemd state, and a
committed `status: needs-review` file the user has to go looking for. The seven-week gap
(2026-06-30 → 2026-08-19) is confirmed against Git artifacts, with the retained journal showing
`Lock exists, skipping` then `Finished` on each of 2026-08-12 through 08-18 — the run returned 0,
so systemd reported success while nothing happened.

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

Do **not** port the personal wrapper's PID lock or `TimeoutExpired` handling.

**Acceptance:**
- A deliberately failed run — e.g. a dirty tree, an existing exit-1 path — produces a visible
  desktop notification naming the vault and the reason.
- A no-op run (`PROMOTION_REQUIRED=0`) produces no notification.
- If the notifier cannot display, the run fails loudly rather than exiting 0.
- The `OnFailure=` wiring is committed in the runner templates in this repository, not only
  installed locally.

### W4 — The benchmark

This is the go/no-go for the deferred steps. It must be a harness, not an intention: two workers
running it should get comparable numbers.

Fix a question set against image-maze, the largest vault. For each question record the tokens
spent from vault entry to opening the correct page, and whether the correct page was reached.

- **Baseline: 4,543 tokens** — image-maze `index.md` alone, derived as 18,172 bytes ÷ 4.
- **Tokenizer: bytes ÷ 4**, the same derivation, so the comparison is like-for-like. Not an API
  usage counter and not tiktoken; those produce a different number against the same baseline.

**Acceptance:**
- A question file of **exactly 20** questions is committed under
  `concepts/bc-wiki-maintain/tests/`, each with the gold page path that answers it.
- Gold pages are drawn from the **155 eligible** image-maze pages, not from gitignored `temp/`.
- That file is committed **before** any catalog tuning. Otherwise the benchmark measures the
  tuning rather than the approach.
- The runbook names the agent, the loop, and what counts as "opening" a page and as a miss,
  precisely enough that a second operator reproduces it.
- A results artifact records per-question tokens and hit/miss, plus the computed median and miss
  rate.
- **Bars: median ≤800 tokens and miss rate ≤0.30.** Both must hold. A miss rate above 0.30
  falsifies filter-don't-read; the answer then becomes a small generated index that *is* read, or
  a cheap local embedding step — not this design.

### W5 — `bc-init-agent` stops minting the old first move

Every new vault the scaffold creates carries the navigation W2 is removing. Four separate
directives in `scaffold.py` encode the old access verb, and they must change together or the
generated vault contradicts itself:

- `scaffold.py:40-45` — root `AGENTS.md`: "Before making non-trivial changes, read: 1.
  `.bc-agent/index.md` …"
- `scaffold.py:163-164` — vault `AGENTS.md` trigger table: "Read `index.md` → this file →
  `map.md` → `tasks/active.md`"
- `scaffold.py:593` — seeded ADR-0001: "Agents start from `AGENTS.md` and `.bc-agent/index.md`."
- `scaffold.py:602` — `tasks/active.md`: "the first thing the next agent reads after `index.md`."

Two supporting changes fall out of that:

- `upgrade_notes()` currently checks only architecture-runway, codebase-docs, and
  bc-wiki-maintain pointers. It needs a catalog/read-path hint, so that running the scaffold in
  an existing vault tells the agent to merge the new first move by hand — this is the designed
  migration path for additive idempotency, and W2 should use it rather than inventing one.
- `index.md`, `home.md`, and `map.md` templates advertise themselves as the start hub. They need
  to stop contradicting the catalog even if they survive as secondary human-facing surfaces.

**Acceptance:**
- A freshly scaffolded vault's root `AGENTS.md`, vault `AGENTS.md`, ADR-0001, and
  `tasks/active.md` all name catalog filtering as the first move, with the same fallback chain
  W2 uses, and none names `index.md` first.
- Running the scaffold against an existing pre-change vault prints an upgrade note about the read
  path.
- `concepts/bc-init-agent/CONCEPT.md` records the change and its cross-concept dependency on
  `bc-wiki-maintain`.
- `bc-init-agent`'s existing tests still pass, extended with one case asserting the generated
  first move.

## Open decision — does the scaffold's *shape* change too?

W5 as scoped changes only what the scaffold *says*, not what it *builds*. The survey exposes
three shape problems that a deeper change could fix, and the owner has not decided whether to
take them on:

1. **No summary convention.** No template asks for a one-sentence summary, so the catalog's
   summary column degrades to page titles for unfilled pages. Adding a summary-first convention
   to the page templates would make future pages self-describing.
2. **No frontmatter.** There is no machine-readable `kind` on any page; the catalog infers it
   from the path, which the taxonomy divergence makes lossy. Note this pulls against the
   [non-goal](#non-goals) on frontmatter dates — a `kind` field is not a freshness field, but it
   is still hand-maintained state that can drift.
3. **Overlapping taxonomy.** `project/`, `research/`, `findings/`, `references/`, and
   `conventions/` overlap by their own generated descriptions; `plans/` means different things by
   archetype.

**The argument against doing this now:** additive idempotency means scaffold shape changes reach
**only new vaults**. All eight existing vaults — where the knowledge actually is, and where W4
measures — would be untouched. Shape work is an investment in future vaults, not a fix for
current traversal cost, and it would delay the benchmark that decides whether any of this works.

**Recommendation: defer all three until W4 reports.** If filtering hits its bars against today's
messy taxonomy, the shape problems are less urgent than they look. If it misses, the miss pattern
tells you which of the three actually mattered, instead of guessing now.

## Non-goals

- No bulk automatic linking of prose. Unanimous advisor policy, and note this is a **policy**
  choice, not a mechanical guarantee — see [Open risks](#open-risks).
- No SQLite FTS and no `wiki_route.py` query wrapper. It would add a third index beside Git and
  qmd, and needs a binary where a shell filter suffices; the largest eligible graph is 155 pages.
  Revisit only if W4 shows plain filtering *and* `qmd search` both miss.
- No event-driven or polling dispatcher. Sol proposed a 10-minute poll in Pass 1 and withdrew it
  under cross-examination: the nightly no-ops are a coverage bug, not a latency bug.
- No `updated:` or `status:` frontmatter field. Freshness stays `git_date`. The evidence is next
  door: the personal wiki carries `updated:` and its daily pass had to repair five pages whose
  value was objectively wrong against `git log`.
- No auto-splitting of large pages. Warn above ~12KB; a split is a rewrite.
- No changes to the promotion gates in this plan.
- No PID lock added to `run-promotion.sh`.
- No retroactive restructuring of the 8 live vaults' directory taxonomy. The catalog adapts to
  the taxonomy that exists; it does not demand one.

## Deferred

Blocked on W4 clearing its bars:

2. **List-driven promotion across all 8 vaults.** One unit looping the existing vault list,
   taking coverage from 4/8 to 8/8. Must skip-and-report per vault, never abort the batch —
   otherwise sql and Scripts failing on `PROMOTION_RANGE=invalid` silently stops the other six.
   Measure: total unpromoted headings, 68 → <10. Music's first run (37 headings) is allowed to
   proceed unattended — [decision 5](#resolved-decisions) is closed, do not re-open it.
3. **Scaffold heading fix plus loud lint.** `scaffold.py:307` emits `## __DATE__` while
   `wiki_lint.py:19` requires `## [YYYY-MM-DD]` — the scaffold has been minting headings its own
   detector cannot read. Fix at the root (scaffold emits `## [__DATE__]`), make
   `wiki_lint.py:526` exit nonzero on `PROMOTION_RANGE=invalid`, and let one explicit human edit
   normalise the 13 existing headings. Widening the parser regex was proposed by two advisors and
   **withdrawn by both** under cross-examination; do not revive it.
4. **`map.md` link repair and summary lines.** Emit map targets as real Markdown links so they
   enter the graph, and have lint validate them. `map.md` stays a curated task-bundle layer.
5. **Scaffold shape changes** — see [Open decision](#open-decision--does-the-scaffolds-shape-change-too).

## Open risks

- **The core bet is unmeasured.** W4 exists to resolve it, not to confirm it.
- **Gate 1 does not mechanically prevent automatic linking.** `run-promotion.sh:226` is
  `[[ "$deleted" == '0' ]] && continue`, so a file with zero deleted lines short-circuits the
  byte-prefix check and mid-file insertion passes. This is deliberate — the curated `index.md`
  link appends depend on it — but the no-bulk-linking rule is policy, not enforcement. Anyone who
  later relies on "the gate won't let it happen" will be wrong.
- **Any in-vault Markdown catalog is exposed to Syncthing conflict copies.**
  `maintenance_report()` (`wiki_lint.py:291-298`) excludes only `_meta/` files prefixed `lint-`,
  `health-check-`, or `semantic-consolidation-`, and `_meta` is not in `SKIP_DIR_NAMES`. A
  `_meta/catalog.sync-conflict-*.md` would enter the page walk and be counted as a page. This is
  a direct argument for the cache location in decision 1, and **it is not hypothetical**: during
  the session that wrote this plan, `docs/research/wiki-autonomy-council/` was renamed to `…_1`
  mid-session by exactly this class of event.
- **`mtime` reliability under Syncthing is unverified.** If mtime is unreliable, the cache cannot
  self-invalidate and must be tracked, forcing decision 1 immediately. Fingerprint invalidation
  is the hedge.
- **W2 edits files in eight other repositories.** Necessary for W4 to mean anything, but a wider
  blast radius than a template change, and each vault is a working tree.
- **W5 changes a concept with its own pressure tests and deploy targets.** `bc-init-agent` is
  deployed; its test gate applies independently of `bc-wiki-maintain`'s.
- **Two Homeflix vaults are not scaffold-shaped.** They lack all four `conventions/` pages,
  ADR-0001 under its scaffold filename, `research/README.md`, and the `.obsidian/` metadata. Any
  work assuming a complete base vault will not find one there.
- **No advisor reviewed the `~/Sync/Wiki` evidence.** It arrived after Grok and Sol were
  dispatched for Pass 2; only Opus's retry packet contained it, and that run died on quota.

## What would change this plan

- W4 missing either bar — median above 800 or miss rate above 0.30 — changes the design, not just
  the tuning.
- `qmd search` (BM25, not `query`) measuring fast and accurate on these corpora — the catalog
  shrinks to a fallback for unregistered vaults, and W2 becomes a one-line first-move change.
- Evidence that mtime is unreliable under Syncthing — forces decision 1 now rather than after the
  benchmark.
- A W4 miss pattern concentrated on pages with degenerate summaries or ambiguous `kind` — that
  would promote the [scaffold shape changes](#open-decision--does-the-scaffolds-shape-change-too)
  from deferred to required.
