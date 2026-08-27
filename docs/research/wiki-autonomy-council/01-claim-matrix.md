# Pass 1 claim matrix

Supervisor synthesis, 2026-08-26. Three advisors, fresh context, no peer contact.

Run ids: `advisor-grok` c1790dd1, `advisor-sol` 7fab90ff, `advisor-opus` 79cb8d10.
Workflow 55d098ca-52f8-45f7-a9b1-5301b06f0e82.

## Agreements (unanimous unless noted)

| # | Claim | Notes |
|---|---|---|
| A1 | The read path is the primary defect, not the write path | All three led with it |
| A2 | The fix is a **generated** navigation artifact the agent **filters**, not reads | Opus states the principle: cost becomes O(query) not O(corpus) |
| A3 | The artifact must be computed with no hand-maintained field, invalidated by fingerprint or mtime | Generalizes CONCEPT.md's "computed triggers, never recorded triggers" to computed *artifacts* |
| A4 | Never `qmd query` in the read path (measured 67.1s) | Grok and Opus route to `qmd search` (BM25) as fallback; Sol as low-confidence fallback |
| A5 | Orphan count is the wrong success metric; reachability = presence in the generated catalog | All three said this independently |
| A6 | No automatic prose linker | Gate 1's byte-prefix check mechanically rejects it; Sol's version proposes but never writes |
| A7 | All three write-safety gates stay unchanged | Unanimous; the catalog sits outside them as untracked non-Markdown |
| A8 | Do not convert Music's 197 wikilinks; standardize future links on Markdown | Converge by attrition — a rewrite is forbidden by Gate 1 anyway |
| A9 | Page contract = title + one summary sentence, no date/status frontmatter | Freshness stays `git_date`; a summary duplicates nothing and is underivable. Numbers differ (≤120c / ≤160c / ≤200c / ≤50 words) |

## Disputes relayed to Pass 2

| id | Dispute | Positions | Why material |
|---|---|---|---|
| D1 | Cadence | Nightly, list-driven over all 9 vaults (grok, opus) vs event-driven 10-minute quiet-period dispatcher (sol) | Decides whether a polling daemon gets built. Opus's count: the 4 vaults with timers hold 1 unpromoted heading; the 5 without hold 68 — evidence for coverage, not cadence |
| D2 | Bare-date headings | Widen the parser to accept `## YYYY-MM-DD` (grok, sol) vs keep the human normalization act and make the failure louder (opus) | Two of nine vaults are permanently blocked. CONCEPT.md:96-97 deliberately requires a human act on the append-only log |
| D3 | Catalog location | Gitignored `_meta/` inside the vault (grok, opus) vs `$XDG_CACHE_HOME` outside the repo (sol) | Cold-agent discoverability vs Syncthing conflict copies and proximity to a commit gate |
| D4 | Catalog format | rg-able plain text — TSV (opus) / JSONL (grok) — vs SQLite FTS with a `wiki_route.py` wrapper (sol) | Decides whether the first move is a bare `rg` or requires a tool |
| D5 | Oversized pages | Append to a sibling page instead of growing a >12KB page (grok) vs never split, emit per-section rows so the 70KB map is reachable at ~500 tokens/section (opus) | Affects whether large pages stay traversable without editing them |

## Notable single-advisor findings worth relaying

- **`map.md` is dead weight** (opus, corroborated in part by grok): it exists in all nine vaults from `scaffold.py:262-292`, but writes targets as backticked code spans, so `without_code()` (`wiki_lint.py:23-40`) masks them before `links()` (`:71-79`). It contributes zero graph edges and lint never validates it. image-maze's map lists architecture-runway rounds 4-7 while 8 and 9 exist on disk; Music's is still the scaffold default and omits 34 of its 69 pages. Sol did not address `map.md` at all.
- **The prescribed first move is the bug** (grok): `scaffold.py:163` sends agents to `index.md`, and `run-promotion.sh:122` tells the writer to read `AGENTS.md`, `index.md`, and `log.md` — image-maze's log is 49,767 tokens.
- **qmd's own docs are optimistic** (opus): `concepts/qmd/body/SKILL.md` (lines 29-33) advertises `--no-rerank ≈ 20s` against a measured 67.1s.
- **Catalog omissions should be fatal, zero-inbound advisory** (sol): a clean split between the metric that must hold and the one that is only a smell.

## Supervisor notes

- D5 is closer to complementary than contradictory; both may ship.
- No advisor produced a measured retrieval benchmark. All three flagged the same
  unverified core bet — that filtering a generated keyword table reaches the right
  page — and each proposed a falsification test. That convergence on *what is
  unproven* is the most useful output of Pass 1.
