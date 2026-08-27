# Retrieval fallback benchmark — direct BM25 and shell count ranking

Run date: 2026-08-28. Target vault: `/home/ben/Sync/Work/Development/wp-theme-builds/localhost/image-maze/.bc-agent`. The target vault was read-only; no qmd mutation command was run.

## Result

Eligibility produced **155 tracked Markdown pages**. The eligibility source is the `concepts/bc-wiki-maintain/body/wiki_search.py` function `tracked_markdown_paths` (lines 64–111), which calls `git ls-files`, filters the existing skip directories, and applies `git check-ignore --no-index`; the benchmark asserts 155 pages for this vault.

The inherited round-two bars are median <=800 context tokens and miss rate <=0.30, both required. New methods cap output at 15 paths so a broad result remains within the protocol's usable 1–15-row width; the qmd same-cap control is rerun with `-n 15`. Tokens are UTF-8 stdout bytes / 4, matching the `Attempt.tokens` property in `run_retrieval_benchmark_round2.py` (lines 103–115).

| Method | Median tokens | Misses | Miss rate | Wilson 95% CI | Cost bar | Miss bar | Overall observed | Source |
|---|---:|---:|---:|---|:---:|:---:|:---:|---|
| `A_index_read (round 2 blind correction)` | 4543.00 | 6/20 | 0.30 | [0.15, 0.52] | fail | pass | FAIL | `retrieval-results-round2.md` |
| `B_index_agent_filter (round 2)` | 113.75 | 14/20 | 0.70 | [0.48, 0.85] | pass | fail | FAIL | `retrieval-results-round2.md` |
| `C_qmd_agent_filter (round 2, n=20)` | 499.75 | 6/20 | 0.30 | [0.15, 0.52] | pass | pass | PASS | `retrieval-results-round2.md` |
| `D_catalog_agent_filter (round 2)` | 743.50 | 8/20 | 0.40 | [0.22, 0.61] | pass | fail | FAIL | `retrieval-results-round2.md` |
| `C_qmd_same_cap15 (this run)` | 499.75 | 4/20 | 0.20 | [0.08, 0.42] | pass | pass | PASS | this run |
| `E_shell_count_ranked` (shell pipeline, cap 15) | 164.50 | 3/20 | 0.15 | [0.05, 0.36] | pass | pass | PASS | this run |
| `F_bm25_direct` (stdlib script, cap 15) | 171.12 | 3/20 | 0.15 | [0.05, 0.36] | pass | pass | PASS | this run |

The four first rows are copied from the committed round-two measurements; they are comparison context, not silently rerun values. `A` uses the independent blind correction in `retrieval-results-round2.md` (line 168); `B`, `C`, and `D` use its summary table (lines 13–17).

## Per-question measurements

Each cell lists every attempt as `query: tokens / rows / hit-or-miss / trigger, wall seconds`; the final `=>` is total charged output and final hit. A second attempt is run only when the first has zero rows or more than 15 rows. Gold paths and queries come unchanged from `retrieval-questions.md` and `retrieval-queries-round2.tsv`.

| # | Gold | Primary -> reformulation | E shell count | F direct BM25 | QMD same-cap control |
|---:|---|---|---|---|---|
| 1 | `AGENTS.md` | `durable fact` -> `ending work` | 'durable fact': 152.00t/15 rows/hit, r9/usable-width, 3.483s => 152.00t/hit | 'durable fact': 124.50t/15 rows/hit, r1/usable-width, 0.541s => 124.50t/hit | 'durable fact': 558.25t/14 rows/hit, r2/usable-width, 0.739s => 558.25t/hit |
| 2 | `agents/image-seo-agent.md` | `picture metadata` -> `writing metadata` | 'picture metadata': 150.50t/15 rows/hit, r1/usable-width, 3.387s => 150.50t/hit | 'picture metadata': 172.25t/15 rows/hit, r2/usable-width, 0.484s => 172.25t/hit | 'picture metadata': 251.00t/6 rows/hit, r1/usable-width, 0.603s => 251.00t/hit |
| 3 | `conventions/styling-radius-scale.md` | `corner sizes` -> `button panel` | 'corner sizes': 105.25t/8 rows/hit, r3/usable-width, 3.355s => 105.25t/hit | 'corner sizes': 59.50t/7 rows/hit, r1/usable-width, 0.420s => 59.50t/hit | 'corner sizes': 70.75t/2 rows/hit, r1/usable-width, 0.616s => 70.75t/hit |
| 4 | `decisions/adr-0003-provider-first-subscription-architecture.md` | `subscription lifecycle` -> `payment adapters` | 'subscription lifecycle': 168.50t/15 rows/hit, r4/usable-width, 3.841s => 168.50t/hit | 'subscription lifecycle': 170.00t/15 rows/hit, r3/usable-width, 0.614s => 170.00t/hit | 'subscription lifecycle': 300.00t/7 rows/hit, r3/usable-width, 0.655s => 300.00t/hit |
| 5 | `decisions/adr-0005-architecture-deepening-no-rejected-designs.md` | `cleanup approach` -> `keep record` | 'cleanup approach': 160.50t/15 rows/MISS/usable-width, 3.749s => 160.50t/MISS | 'cleanup approach': 151.75t/15 rows/MISS/usable-width, 0.661s => 151.75t/MISS | 'cleanup approach': 75.75t/2 rows/MISS/usable-width, 0.689s => 75.75t/MISS |
| 6 | `decisions/adr-0019-desktop-mouse-click-dismisses-fullscreen.md` | `mouse click` -> `touch tap` | 'mouse click': 177.50t/15 rows/hit, r1/usable-width, 3.634s => 177.50t/hit | 'mouse click': 181.75t/15 rows/hit, r1/usable-width, 0.591s => 181.75t/hit | 'mouse click': 285.25t/7 rows/hit, r1/usable-width, 0.664s => 285.25t/hit |
| 7 | `decisions/adr-0029-dcu-missing-ports-fail-closed.md` | `rate limiting` -> `referral traffic` | 'rate limiting': 194.25t/15 rows/hit, r14/usable-width, 3.411s => 194.25t/hit | 'rate limiting': 173.75t/15 rows/hit, r1/usable-width, 0.441s => 173.75t/hit | 'rate limiting': 712.75t/15 rows/hit, r1/usable-width, 0.655s => 712.75t/hit |
| 8 | `project/arch-review/architecture-adapter-split-arch-review.md` | `WordPress adapter` -> `extract first` | 'WordPress adapter': 170.50t/15 rows/hit, r3/usable-width, 3.467s => 170.50t/hit | 'WordPress adapter': 180.00t/15 rows/hit, r1/usable-width, 0.524s => 180.00t/hit | 'WordPress adapter': 702.75t/15 rows/hit, r1/usable-width, 0.688s => 702.75t/hit |
| 9 | `project/prds/automatic-publish-queue-prd.md` | `publish delay` -> `actions v1` | 'publish delay': 147.50t/15 rows/hit, r1/usable-width, 3.203s => 147.50t/hit | 'publish delay': 182.75t/15 rows/hit, r5/usable-width, 0.420s => 182.75t/hit | 'publish delay': 281.75t/6 rows/hit, r3/usable-width, 0.588s => 281.75t/hit |
| 10 | `project/prds/architecture-deepening-round-3-prd.md` | `JavaScript queue` -> `PHP rules` | 'JavaScript queue': 152.50t/15 rows/hit, r11/usable-width, 3.075s => 152.50t/hit | 'JavaScript queue': 169.25t/15 rows/MISS/usable-width, 0.684s => 169.25t/MISS | 'JavaScript queue': 362.25t/8 rows/MISS/usable-width, 0.666s => 362.25t/MISS |
| 11 | `project/prds/mobile-gesture-suite-v2-prd.md` | `vibration drag` -> `stay silent` | 'vibration drag': 171.50t/15 rows/hit, r2/usable-width, 2.994s => 171.50t/hit | 'vibration drag': 174.25t/15 rows/hit, r1/usable-width, 0.316s => 174.25t/hit | 'vibration drag': 209.75t/5 rows/hit, r1/usable-width, 0.569s => 209.75t/hit |
| 12 | `project/prds/pipeline-reliability-privacy-prd.md` | `upload response` -> `retry lost` | 'upload response': 149.50t/15 rows/hit, r8/usable-width, 3.326s => 149.50t/hit | 'upload response': 202.75t/15 rows/hit, r1/usable-width, 0.352s => 202.75t/hit | 'upload response': 441.25t/10 rows/hit, r2/usable-width, 0.555s => 441.25t/hit |
| 13 | `project/prds/frontend-modal-accessibility-prd.md` | `focus Escape` -> `chest fullscreen` | 'focus Escape': 172.50t/15 rows/hit, r2/usable-width, 3.241s => 172.50t/hit | 'focus Escape': 163.75t/15 rows/hit, r2/usable-width, 0.455s => 163.75t/hit | 'focus Escape': 640.00t/14 rows/hit, r2/usable-width, 0.653s => 640.00t/hit |
| 14 | `project/prds/lqip-metadata-hygiene-prd.md` | `preview source` -> `cache changes` | 'preview source': 196.00t/15 rows/hit, r11/usable-width, 3.566s => 196.00t/hit | 'preview source': 167.00t/15 rows/hit, r1/usable-width, 0.635s => 167.00t/hit | 'preview source': 574.75t/14 rows/hit, r1/usable-width, 0.760s => 574.75t/hit |
| 15 | `project/prds/toolchain-static-analysis-hardening-prd.md` | `code checks` -> `pipeline release` | 'code checks': 185.25t/15 rows/MISS/usable-width, 3.755s => 185.25t/MISS | 'code checks': 175.25t/15 rows/MISS/usable-width, 0.522s => 175.25t/MISS | 'code checks': 679.25t/15 rows/MISS/usable-width, 0.809s => 679.25t/MISS |
| 16 | `project/prds/pack-download-surface-consolidation-prd.md` | `download URL` -> `live mode` | 'download URL': 169.75t/15 rows/hit, r7/usable-width, 3.318s => 169.75t/hit | 'download URL': 177.50t/15 rows/hit, r1/usable-width, 0.438s => 177.50t/hit | 'download URL': 735.25t/15 rows/hit, r1/usable-width, 0.585s => 735.25t/hit |
| 17 | `project/plans/launch-plan.md` | `Git server` -> `local machine` | 'Git server': 184.00t/15 rows/hit, r4/usable-width, 3.687s => 184.00t/hit | 'Git server': 135.75t/15 rows/hit, r1/usable-width, 0.642s => 135.75t/hit | 'Git server': 569.25t/13 rows/hit, r1/usable-width, 0.769s => 569.25t/hit |
| 18 | `references/theme-build-flow.md` | `theme output` -> `authored WordPress` | 'theme output': 140.75t/15 rows/hit, r15/usable-width, 3.475s => 140.75t/hit | 'theme output': 160.75t/15 rows/hit, r1/usable-width, 0.851s => 160.75t/hit | 'theme output': 638.50t/15 rows/hit, r1/usable-width, 0.886s => 638.50t/hit |
| 19 | `references/wordpress-local-env.md` | `site URLs` -> `environment setting` | 'site URLs': 151.50t/15 rows/MISS/usable-width, 3.497s => 151.50t/MISS | 'site URLs': 175.50t/15 rows/hit, r7/usable-width, 0.592s => 175.50t/hit | 'site URLs': 667.50t/15 rows/MISS/usable-width, 0.707s => 667.50t/MISS |
| 20 | `research/adult-content-compliance-research.md` | `compliance material` -> `explicit serving` | 'compliance material': 149.75t/15 rows/hit, r1/usable-width, 3.291s => 149.75t/hit | 'compliance material': 137.25t/15 rows/hit, r1/usable-width, 0.508s => 137.25t/hit | 'compliance material': 157.50t/4 rows/hit, r1/usable-width, 0.777s => 157.50t/hit |

## The simpler thing first: shell pipeline

The measured shell method is a read-only pipeline: `git ls-files -z` supplies tracked paths, `git check-ignore --no-index` removes ignored paths, the existing skip directories are excluded, `rg -i -o --fixed-strings` counts term matches per file, `sort` ranks descending by count, and `head -15` bounds output. Its exact measurement body is the `SHELL_PIPELINE` constant in `run_retrieval_benchmark_fallback.py` (lines 31–52); the compact command shape is the same pipeline rather than a generated file or index.

It returned **3/20 misses**, median **164.50 tokens**, mean **162.47**, and total measured wall time **68.755s** for the 20-question run. These values are the per-question rows above, generated by the fixed shell body; no shell output was edited by hand.

## Direct BM25 fallback implementation

`concepts/bc-wiki-maintain/body/wiki_search.py` is a real tool rather than a benchmark fixture because it solves the qmd-unavailable case directly: it has no qmd dependency, no third-party import, no generated artifact, no cache, and no index. It accepts the vault path and query terms, reads eligible pages at query time, and prints ranked vault-relative paths; `--scores` is optional and the default is paths only.

The score is standard BM25 with k1=1.2 and b=0.75. The implementation tokenizes page content and query terms using the same deterministic tokenizer, computes document frequency and average document length from the current eligible pages, then sorts ties by path. The 15-row default is intentional: it keeps fallback context bounded and satisfies the protocol's usable-width rule without a reformulation caused only by this tool's own output cap.

It returned **3/20 misses**, median **171.12 tokens**, mean **161.76**, and total measured wall time **10.690s** for the 20-question run. The CLI's default output is paths only; its output bytes are the token cost, not the Python process time.

## How close does the fallback get to qmd, and where does it break

At the same 15-row cap, direct BM25 missed 3/20 and qmd missed 4/20. The observed miss-rate difference is 0.05; the corresponding Wilson intervals are [0.05, 0.36] and [0.08, 0.42]. They are inside noise at n=20; the fallback should not be described as more accurate than qmd from this sample. Against the inherited qmd n=20 row (6/20 misses), it is also within the same small-sample uncertainty.

The shell count pipeline and direct BM25 had miss sets computed from the per-question rows. Shell misses: Q5, Q15, Q19. Direct BM25 misses: Q5, Q10, Q15. qmd same-cap misses: Q5, Q10, Q15, Q19. The exact failing queries and top paths remain visible in the per-question cells.

The breaks are semantic rather than speed-related. Term-frequency ranking cannot retrieve a page when the frozen query words are absent or use a different vocabulary; it also surfaces broad project documents when common terms occur everywhere. BM25 reduces the long-document `log.md` problem through length normalization, but it cannot invent synonyms or resolve a policy question whose words do not occur in the gold page. The shell pipeline has the same lexical ceiling and is more vulnerable to common-term frequency ties; on this corpus its measured accuracy happened to match direct BM25.

## Recommendation

Use qmd keyword search as the default. When qmd is unavailable, recommend the **stdlib BM25 script** as the installed fallback: it matches the shell pipeline's observed 3/20 miss rate while completing the 20-question run materially faster, enforces the benchmark's tracked/ignored eligibility in one batch, and has explicit deterministic ranking and tests. Keep the shell pipeline as a zero-deployment emergency fallback when the concept body is not installed; it is empirically comparable here, but its one-line form is harder to reproduce with all eligibility checks and its per-file `git check-ignore` loop is slower.

The recommendation is deliberately not an accuracy overclaim. Both fallbacks are close to qmd in this 20-question sample, and all differences from qmd are inside Wilson noise. The script's advantage is operational: no qmd, no cache, no generated catalog, no stale state, and a single portable implementation of the eligibility contract.

## Reproduction

```sh
python3 concepts/bc-wiki-maintain/tests/run_retrieval_benchmark_fallback.py \
  "$HOME/Sync/Work/Development/wp-theme-builds/localhost/image-maze/.bc-agent" \
  --collection image-maze
```

The fallback itself is invoked as:
```sh
python3 concepts/bc-wiki-maintain/body/wiki_search.py "$VAULT" -n 15 "term one"
```
It reads only the supplied vault. The benchmark's qmd control uses `qmd search` read-only; it does not call qmd `update`, `embed`, `init`, `cleanup`, `collection`, or `context` commands.

## Evidence ledger

- Eligibility and skip names: `concepts/bc-wiki-maintain/body/wiki_search.py`, lines 22–26 quote `SKIP_DIR_NAMES = {".git", ".obsidian", "scratch", "temp", "node_modules", "vendor"}` and `DEFAULT_LIMIT = 15`; lines 64–111 quote the `git ls-files` and `git check-ignore --no-index` calls.
- BM25 formula and deterministic ordering: `concepts/bc-wiki-maintain/body/wiki_search.py`, lines 131–163 quote `inverse_document_frequency = math.log(...)` and `scores.sort(key=lambda item: (-item.score, item.relative))`.
- Compact default output and required vault/query arguments: `concepts/bc-wiki-maintain/body/wiki_search.py`, lines 166–200 quote `parser.add_argument("vault")`, `default=DEFAULT_LIMIT`, and `print(result.relative)`.
- Frozen questions and two-attempt protocol: `concepts/bc-wiki-maintain/tests/run_retrieval_benchmark_fallback.py`, lines 1–6 quote `only read-only operations`; lines 142–150 quote `if first.attempt.rows == 0 or first.attempt.rows > FLOOD_LIMIT` and the two-attempt cost sum. The imported round-two rule is `run_retrieval_benchmark_round2.py`, lines 533–552.
- Prior comparison rows: `concepts/bc-wiki-maintain/tests/retrieval-results-round2.md`, lines 13–17 quote the prior A/B/C/D rows; its blind correction at lines 164–172 quotes A = 6/20 and C = 6/20.
- Shell pipeline source: `concepts/bc-wiki-maintain/tests/run_retrieval_benchmark_fallback.py`, lines 31–52 quote `git -C "$REPO" ls-files -z`, `rg -i -o --fixed-strings`, `sort`, and `head -15`.
- New shell and BM25 per-question measurements: this report's table above, produced by the committed benchmark command in `run_retrieval_benchmark_fallback.py`.
