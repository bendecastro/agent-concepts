# Image-maze retrieval benchmark results

Run date: 2026-08-27. The target vault was read-only. The frozen keyword file was
committed before this harness ran; see the commit record in the parent run artifact.

## Result

The vault supplied **155 eligible tracked Markdown pages**. The harness read `$IMAGE_MAZE_VAULT/index.md` as the incumbent and generated a **42,421-byte** seven-column catalog at `/tmp/bc-retrieval-catalog-9p2kndtj.tsv` only. Frozen query commit: `f18492510492b7036c29e06af63c98b502397683`.
The index graph reaches 118 pages at depth 1 and 139 at depth <=2; the benchmark does not infer a hit from reachability alone: A_index_read uses the explicit row judgments below.

Cost is UTF-8 stdout bytes / 4 for search/filter output. A_index_read is the full index byte size / 4; no follow-on page is opened because each judgment is whether the index row identifies the gold page. The bars are median <= 800 tokens and miss rate <= 0.30, and both are required.

| Method | Median tokens | Miss rate | Median <= 800? | Miss <= 0.30? | Passes both? |
|---|---:|---:|:---:|:---:|:---:|
| `A_index_read` | 4543.00 | 0.15 (3/20) | no | yes | no |
| `B_index_grep_AND` | 0.00 | 1.00 (20/20) | yes | no | no |
| `B_index_grep_OR` | 206.25 | 0.75 (15/20) | yes | no | no |
| `C_qmd_keywords` | 165.50 | 0.25 (5/20) | yes | yes | **yes** |
| `C2_qmd_sentence` | 59.75 | 0.85 (17/20) | yes | no | no |
| `D_catalog_grep_AND` | 0.00 | 1.00 (20/20) | yes | no | no |
| `D_catalog_grep_OR` | 1359.75 | 0.45 (9/20) | no | no | no |

### Method interpretation

- `A_index_read` is the incumbent: the full curated index is loaded once per question and the row is judged.
- `B_index_grep_AND` and `B_index_grep_OR` filter the same index rows with the frozen keywords.
- `C_qmd_keywords` searches the complete active qmd collection with frozen keywords; rank is returned order.
- `C2_qmd_sentence` repeats qmd search with the complete natural-language question, documenting query-shape sensitivity.
- `D_catalog_grep_AND` and `D_catalog_grep_OR` filter the generated TSV; catalog construction is not context cost.

## Per-question measurements

Each cell is `tokens / hit-or-miss`; qmd cells also include `rank` and grep cells include matching row count.

| # | Gold page | Frozen keywords | A index | B AND | B OR | C keywords | C2 sentence | D AND | D OR |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `AGENTS.md` | `durable fact ending work` | 4543.00 / hit | 0.00 / MISS, 0 rows | 122.00 / MISS, 3 rows | 170.50 / hit (r1), 5 rows | 143.00 / hit (r1), 4 rows | 0.00 / MISS, 0 rows | 509.75 / MISS, 6 rows |
| 2 | `agents/image-seo-agent.md` | `inspect picture metadata` | 4543.00 / hit | 0.00 / MISS, 0 rows | 126.00 / MISS, 2 rows | 0.00 / MISS (no rank), 0 rows | 0.00 / MISS (no rank), 0 rows | 0.00 / MISS, 0 rows | 721.00 / MISS, 6 rows |
| 3 | `conventions/styling-radius-scale.md` | `corner sizes button panel` | 4543.00 / hit | 0.00 / MISS, 0 rows | 247.50 / MISS, 5 rows | 70.75 / hit (r1), 2 rows | 24.00 / MISS (no rank), 1 rows | 0.00 / MISS, 0 rows | 1004.50 / hit, 8 rows |
| 4 | `decisions/adr-0003-provider-first-subscription-architecture.md` | `payment adapters lifecycle events` | 4543.00 / hit | 0.00 / MISS, 0 rows | 35.75 / MISS, 1 rows | 124.75 / hit (r2), 3 rows | 24.00 / MISS (no rank), 1 rows | 0.00 / MISS, 0 rows | 722.50 / hit, 7 rows |
| 5 | `decisions/adr-0005-architecture-deepening-no-rejected-designs.md` | `cleanup approach keep record` | 4543.00 / hit | 0.00 / MISS, 0 rows | 40.50 / MISS, 2 rows | 75.75 / MISS (no rank), 2 rows | 24.00 / MISS (no rank), 1 rows | 0.00 / MISS, 0 rows | 688.75 / MISS, 7 rows |
| 6 | `decisions/adr-0019-desktop-mouse-click-dismisses-fullscreen.md` | `mouse touch fullscreen viewer` | 4543.00 / hit | 0.00 / MISS, 0 rows | 352.50 / hit, 9 rows | 213.25 / hit (r1), 5 rows | 24.00 / MISS (no rank), 1 rows | 0.00 / MISS, 0 rows | 824.50 / hit, 9 rows |
| 7 | `decisions/adr-0029-dcu-missing-ports-fail-closed.md` | `rate limiting referral traffic` | 4543.00 / hit | 0.00 / MISS, 0 rows | 805.50 / MISS, 13 rows | 232.25 / hit (r1), 5 rows | 24.00 / MISS (no rank), 1 rows | 0.00 / MISS, 0 rows | 2854.00 / hit, 28 rows |
| 8 | `project/arch-review/architecture-adapter-split-arch-review.md` | `WordPress adapter extract first` | 4543.00 / hit | 0.00 / MISS, 0 rows | 589.00 / hit, 12 rows | 246.75 / hit (r2), 5 rows | 51.25 / MISS (no rank), 2 rows | 0.00 / MISS, 0 rows | 2045.75 / hit, 22 rows |
| 9 | `project/prds/automatic-publish-queue-prd.md` | `WordPress publish actions delay` | 4543.00 / hit | 0.00 / MISS, 0 rows | 354.50 / hit, 8 rows | 72.25 / hit (r1), 2 rows | 72.25 / hit (r1), 2 rows | 0.00 / MISS, 0 rows | 1998.00 / hit, 21 rows |
| 10 | `project/prds/architecture-deepening-round-3-prd.md` | `PHP JavaScript queue rules` | 4543.00 / MISS | 0.00 / MISS, 0 rows | 236.75 / MISS, 6 rows | 71.00 / MISS (no rank), 2 rows | 0.00 / MISS (no rank), 0 rows | 0.00 / MISS, 0 rows | 1421.50 / MISS, 17 rows |
| 11 | `project/prds/mobile-gesture-suite-v2-prd.md` | `vibration drag silent` | 4543.00 / hit | 0.00 / MISS, 0 rows | 52.75 / MISS, 1 rows | 160.50 / hit (r1), 4 rows | 70.00 / MISS (no rank), 2 rows | 0.00 / MISS, 0 rows | 0.00 / MISS, 0 rows |
| 12 | `project/prds/pipeline-reliability-privacy-prd.md` | `retry WordPress upload lost` | 4543.00 / hit | 0.00 / MISS, 0 rows | 63.00 / MISS, 2 rows | 73.50 / hit (r1), 2 rows | 24.00 / MISS (no rank), 1 rows | 0.00 / MISS, 0 rows | 1184.25 / MISS, 12 rows |
| 13 | `project/prds/frontend-modal-accessibility-prd.md` | `chest fullscreen focus Escape` | 4543.00 / hit | 0.00 / MISS, 0 rows | 967.25 / MISS, 23 rows | 239.50 / hit (r2), 5 rows | 209.50 / MISS (no rank), 5 rows | 0.00 / MISS, 0 rows | 2541.50 / MISS, 25 rows |
| 14 | `project/prds/lqip-metadata-hygiene-prd.md` | `cached preview source changes` | 4543.00 / hit | 0.00 / MISS, 0 rows | 0.00 / MISS, 0 rows | 209.75 / hit (r1), 5 rows | 104.50 / MISS (no rank), 3 rows | 0.00 / MISS, 0 rows | 1867.25 / MISS, 18 rows |
| 15 | `project/prds/toolchain-static-analysis-hardening-prd.md` | `code checks pipeline release` | 4543.00 / hit | 0.00 / MISS, 0 rows | 337.00 / MISS, 6 rows | 240.50 / hit (r1), 5 rows | 68.25 / MISS (no rank), 2 rows | 0.00 / MISS, 0 rows | 1298.00 / MISS, 13 rows |
| 16 | `project/prds/pack-download-surface-consolidation-prd.md` | `old download URL live` | 4543.00 / hit | 0.00 / MISS, 0 rows | 142.00 / hit, 5 rows | 228.50 / MISS (no rank), 5 rows | 113.00 / MISS (no rank), 3 rows | 0.00 / MISS, 0 rows | 1559.00 / hit, 13 rows |
| 17 | `project/plans/launch-plan.md` | `Git local machine server` | 4543.00 / hit | 0.00 / MISS, 0 rows | 299.75 / MISS, 8 rows | 105.50 / hit (r1), 3 rows | 68.50 / hit (r1), 2 rows | 0.00 / MISS, 0 rows | 1536.25 / hit, 19 rows |
| 18 | `references/theme-build-flow.md` | `authored theme WordPress output` | 4543.00 / MISS | 0.00 / MISS, 0 rows | 245.50 / MISS, 9 rows | 201.75 / hit (r1), 5 rows | 150.00 / MISS (no rank), 4 rows | 0.00 / MISS, 0 rows | 1750.25 / hit, 19 rows |
| 19 | `references/wordpress-local-env.md` | `environment site URLs WordPress` | 4543.00 / MISS | 0.00 / MISS, 0 rows | 175.75 / MISS, 5 rows | 217.25 / hit (r1), 5 rows | 0.00 / MISS (no rank), 0 rows | 0.00 / MISS, 0 rows | 1989.75 / hit, 19 rows |
| 20 | `research/adult-content-compliance-research.md` | `compliance missing explicit material` | 4543.00 / hit | 0.00 / MISS, 0 rows | 87.00 / hit, 2 rows | 112.75 / MISS (no rank), 3 rows | 70.00 / MISS (no rank), 2 rows | 0.00 / MISS, 0 rows | 600.75 / hit, 3 rows |

## A_index_read judgment record

These are human-readable judgments against the exact index rows, made after the frozen query file was committed and before interpreting the other methods. `hit` means the row lets an agent identify the declared gold page; it does not claim that the row contains the answer itself.

| # | Structural reachability | Hit? | Judgment |
|---:|---|:---:|---|
| 1 | depth 1 | yes | Agent maintainer instructions is the only row naming the wiki maintenance protocol. |
| 2 | depth 1 | yes | Image SEO agent is the only row naming the image-metadata prompt. |
| 3 | depth 1 | yes | Border-radius token scale names the requested corner-size convention. |
| 4 | depth 1 | yes | Provider-first subscription architecture names provider/event/entitlement design. |
| 5 | depth 1 | yes | Architecture deepening — no rejected designs names the record of discarded approaches. |
| 6 | depth 1 | yes | The row explicitly says a mouse click dismisses the fullscreen viewer. |
| 7 | depth 1 | yes | The row explicitly says rate_limit_* denies when fraud-sensitive ports are missing. |
| 8 | depth 1 | yes | Architecture Adapter Split — architecture review names the requested extraction decision. |
| 9 | depth 1 | yes | Automatic Publish Queue PRD names the only page governing v1 publish delay scope. |
| 10 | unreachable | no | The Round 3 PRD path does not occur in index.md; no row can identify it. |
| 11 | depth 1 | yes | Mobile Gesture Suite v2 PRD names the gesture behavior family containing the vibration rule. |
| 12 | depth 1 | yes | Pipeline Reliability and Privacy PRD names the page governing lost-response retries. |
| 13 | depth 1 | yes | Frontend Modal Accessibility PRD names the page governing nested focus and Escape. |
| 14 | depth 1 | yes | LQIP Metadata Hygiene PRD names the cache-refresh policy page. |
| 15 | depth 1 | yes | Toolchain and Static Analysis Hardening PRD lists the requested pipeline/theme checks. |
| 16 | depth 1 | yes | Pack Download Surface Consolidation PRD names the legacy download-route policy. |
| 17 | depth 1 | yes | Launch plan is the indexed page that partitions deployment and content control. |
| 18 | unreachable | no | The theme-build-flow path does not occur in index.md; no row can identify it. |
| 19 | unreachable | no | The wordpress-local-env path does not occur in index.md; no row can identify it. |
| 20 | depth 1 | yes | Adult-content mode compliance research names the page containing the outstanding compliance inventory. |

## Mechanism and evidence

- The incumbent's structural ceiling is visible from `$IMAGE_MAZE_VAULT/index.md`: the graph reached 118 pages at depth 1 and 139 by depth 2, while the eligible-page count was 155. The A table separates this ceiling from the stricter row-specific judgment.
- The generated catalog is 42,421 bytes (10605.25 tokens by the benchmark rule), versus 18,172 bytes (4543.00 tokens) for the index. Reading the generated catalog wholesale therefore costs more than reading the incumbent.
- Keyword qmd search missed 5/20 questions; full-sentence qmd search missed 17/20. The per-question qmd output is retained in the table as stdout byte cost and returned rank, rather than treating a command exit status as a hit. Keyword top-path counts: [('AGENTS.md', 1), ('conventions/styling-radius-scale.md', 1), ('decisions/adr-0014-theme-owned-dcu-backend.md', 1), ('decisions/adr-0019-desktop-mouse-click-dismisses-fullscreen.md', 1), ('decisions/adr-0029-dcu-missing-ports-fail-closed.md', 1)]; sentence top-path counts: [('log.md', 7), ('agents/seo-agent.md', 2), ('AGENTS.md', 1), ('conventions/validation.md', 1), ('project/architecture-module-map.md', 1)].
- The catalog's seven fields are always populated. When a page has no `##` heading, its deterministic H1/path title is used for the heading-keyword field rather than inventing prose.
- The benchmark freezes query formulation instead of selecting a better term after a miss. This is important because both grep and BM25 are sensitive to query shape; no result was re-tuned.

## Runbook and definitions

Run from the repository root with the read-only image-maze vault path:

```sh
python3 concepts/bc-wiki-maintain/tests/run_retrieval_benchmark.py \
  "$HOME/Sync/Work/Development/wp-theme-builds/localhost/image-maze/.bc-agent" \
  --collection image-maze
```

The harness reads the question/gold table from `concepts/bc-wiki-maintain/tests/retrieval-questions.md` and the frozen keywords from `retrieval-queries.tsv`. It never edits the vault. It enumerates tracked Markdown files with `git ls-files`, excludes the existing skip directories (`.git`, `.obsidian`, `scratch`, `temp`, `node_modules`, `vendor`), and writes the seven-column catalog to `/tmp`.

Exact retrieval commands issued for each question are:

```sh
qmd search "<frozen keywords>" -c image-maze --format files -n 5
qmd search "<full question>" -c image-maze --format files -n 5
```

For B and D, a line is an AND match when every frozen keyword occurs as a case-insensitive whole word; an OR match requires any keyword. This is the fixed-string grep meaning implemented by the harness with word boundaries so `Git` does not match the middle of `digital`. A grep hit requires the exact gold relative path in a matching line. qmd rank is the first returned `qmd://image-maze/<path>` row whose path equals the gold path (with the qmd space-to-hyphen alias allowed); absence from five rows is a miss.

A page is considered opened only when its bytes would be placed in the agent context. For A, only the complete index bytes are counted and no page is opened after the row judgment. For B/D, only matching stdout lines are counted. For qmd, only command stdout is counted; stderr, process startup, and qmd's on-disk index are not context. Catalog generation CPU/disk work is reported but excluded from context tokens because the proposed design asks agents to filter the artifact, not read its build.

A miss means the declared gold path is not identified by the method's allowed output. A_index_read's human judgment is the exception to path-string matching and is exposed in the judgment table.

## Methodological weaknesses

- The question set is 20 items and has known skew recorded in `retrieval-questions.md`; it is evidence, not a universal query distribution.
- A_index_read is necessarily a human judgment, not a model replay. Another operator may disagree on whether a terse row is enough; the reasons and structural reachability make that disagreement visible.
- B/D use frozen keywords chosen before retrieval, but the benchmark does not measure an interactive agent's ability to refine a miss. Allowing refinement after each result would be a different protocol.
- qmd's result ranking can change if its index becomes stale. This run uses the installed `image-maze` collection and records the exact command; no qmd update/embed mutation was performed.
- The catalog summary extractor is deterministic and intentionally conservative. Its generated rows are a benchmark representation, not evidence that a production W1 implementation should copy every parser detail.

## Source citations

- `concepts/bc-wiki-maintain/tests/retrieval-questions.md`: the pre-registered table supplies each question and gold path; its vault note says "155 eligible pages (tracked Markdown, `temp/` excluded)."
- `$IMAGE_MAZE_VAULT/index.md`: the incumbent source begins `# image-maze Agent Wiki` and its navigation begins at `## Start here`; the byte count and graph counts above were measured from this exact file and its linked pages.
- `/tmp/bc-retrieval-catalog-9p2kndtj.tsv`: generated scratch artifact with the seven columns specified by the benchmark; its byte count and row contents are the source for the catalog measurements above.
