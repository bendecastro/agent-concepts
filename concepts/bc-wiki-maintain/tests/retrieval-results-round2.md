# Image-maze retrieval benchmark — round two

Run date: 2026-08-27. The target vault was read-only; no qmd index or vault file was mutated.

## Answer to the review question

The benchmark uses **155 eligible tracked Markdown pages** from `/home/ben/Sync/Work/Development/wp-theme-builds/localhost/image-maze/.bc-agent`. The proposed catalog has **57,125 bytes / 14281.25 tokens** before any filter output. The index has 18,172 bytes / 4543.00 tokens.

The answer is based on the agent-style protocol below, not the round-one 3–4-word AND test.

| Method | Median tokens | Misses | Miss rate | Wilson 95% CI | Cost bar | Miss bar | Overall observed | Uncertainty |
|---|---:|---:|---:|---|:---:|:---:|:---:|---|
| `A_index_read` | 4543.00 | 3/20 | 0.15 | [0.05, 0.36] | fail | pass | FAIL | inside noise (CI crosses 0.30) |
| `B_index_agent_filter` | 113.75 | 14/20 | 0.70 | [0.48, 0.85] | pass | fail | FAIL | safe failure (CI lower bound > 0.30) |
| `C_qmd_agent_filter` | 499.75 | 6/20 | 0.30 | [0.15, 0.52] | pass | pass | PASS | inside noise (CI crosses 0.30) |
| `D_catalog_agent_filter` | 743.50 | 8/20 | 0.40 | [0.22, 0.61] | pass | fail | FAIL | inside noise (CI crosses 0.30) |

Observed PASS means both observed metrics clear the bars; it is not a claim that a 20-question estimate is certain. The Wilson column is the required uncertainty statement for each miss rate. A CI crossing 0.30 is explicitly inside noise, even when the observed row says PASS or FAIL.

## Protocol

The frozen agent query file is `concepts/bc-wiki-maintain/tests/retrieval-queries-round2.tsv` (commit `54fd0cf9bf908d7b12529f57828656fb9198b8ec`). Each primary and reformulation has one or two concrete terms selected from the question wording before retrieval was run; the two attempts are fixed for all methods. A first result with **zero rows or more than 15 rows is flooded** and triggers exactly one reformulation. A nonzero result of 1–15 rows is usable; a nonzero miss in that width does not get a third attempt. Both attempts' UTF-8 output bytes are charged when the second runs.

`B_index_agent_filter` applies case-insensitive whole-word OR to each line of `index.md`. `D_catalog_agent_filter` applies the identical OR matcher to each seven-column catalog row. `C_qmd_agent_filter` runs `qmd search <terms> -c <collection> --format files -n 20`; qmd paths are the rows. A usable hit requires the exact gold relative path in the usable output. The filter output itself, not process startup or the catalog build, is context and costs bytes/4.

The incumbent `A_index_read` loads all of `index.md` and uses the explicit row judgment record retained from round one. It is included as a cost/accuracy comparator, not silently treated as a scriptable filter.

## Per-question agent-style measurements

Cells show each attempt as `tokens / rows / initial-hit / trigger`, followed by total charged tokens and final hit. For a single usable attempt, no reformulation was permitted. `initial-hit` means the gold path was present even if the result was flooded; the final status requires a usable 1–15-row result after any required reformulation.

| # | Gold | Primary → reformulation | A index | B index filter | C qmd filter | D catalog filter |
|---:|---|---|---:|---|---|---|
| 1 | `AGENTS.md` | `durable fact` → `ending work` | 4543.00t/hit | a1 104.25t/2 rows/MISS/usable-width => 104.25t/MISS | a1 558.25t/14 rows/hit, r2/usable-width => 558.25t/hit | a1 208.00t/2 rows/MISS/usable-width => 208.00t/MISS |
| 2 | `agents/image-seo-agent.md` | `picture metadata` → `writing metadata` | 4543.00t/hit | a1 126.00t/2 rows/MISS/usable-width => 126.00t/MISS | a1 251.00t/6 rows/hit, r1/usable-width => 251.00t/hit | a1 864.50t/7 rows/MISS/usable-width => 864.50t/MISS |
| 3 | `conventions/styling-radius-scale.md` | `corner sizes` → `button panel` | 4543.00t/hit | a1 0.00t/0 rows/MISS/flood/zero; a2 247.50t/5 rows/MISS/usable-width => 247.50t/MISS | a1 70.75t/2 rows/hit, r1/usable-width => 70.75t/hit | a1 94.75t/1 rows/hit, r1/usable-width => 94.75t/hit |
| 4 | `decisions/adr-0003-provider-first-subscription-architecture.md` | `subscription lifecycle` → `payment adapters` | 4543.00t/hit | a1 158.75t/4 rows/hit, r4/usable-width => 158.75t/hit | a1 300.00t/7 rows/hit, r3/usable-width => 300.00t/hit | a1 1073.75t/8 rows/hit, r2/usable-width => 1073.75t/hit |
| 5 | `decisions/adr-0005-architecture-deepening-no-rejected-designs.md` | `cleanup approach` → `keep record` | 4543.00t/hit | a1 0.00t/0 rows/MISS/flood/zero; a2 40.50t/2 rows/MISS/usable-width => 40.50t/MISS | a1 75.75t/2 rows/MISS/usable-width => 75.75t/MISS | a1 446.00t/4 rows/MISS/usable-width => 446.00t/MISS |
| 6 | `decisions/adr-0019-desktop-mouse-click-dismisses-fullscreen.md` | `mouse click` → `touch tap` | 4543.00t/hit | a1 39.25t/1 rows/hit, r1/usable-width => 39.25t/hit | a1 285.25t/7 rows/hit, r1/usable-width => 285.25t/hit | a1 256.25t/3 rows/hit, r1/usable-width => 256.25t/hit |
| 7 | `decisions/adr-0029-dcu-missing-ports-fail-closed.md` | `rate limiting` → `referral traffic` | 4543.00t/hit | a1 0.00t/0 rows/MISS/flood/zero; a2 805.50t/13 rows/MISS/usable-width => 805.50t/MISS | a1 944.50t/20 rows/hit, r1/flood/zero; a2 846.50t/20 rows/hit, r6/flood/zero => 1791.00t/MISS | a1 473.00t/3 rows/MISS/usable-width => 473.00t/MISS |
| 8 | `project/arch-review/architecture-adapter-split-arch-review.md` | `WordPress adapter` → `extract first` | 4543.00t/hit | a1 363.50t/8 rows/hit, r5/usable-width => 363.50t/hit | a1 955.00t/20 rows/hit, r1/flood/zero; a2 613.50t/14 rows/hit, r7/usable-width => 1568.50t/hit | a1 3342.50t/27 rows/hit, r5/flood/zero; a2 1764.50t/13 rows/MISS/usable-width => 5107.00t/MISS |
| 9 | `project/prds/automatic-publish-queue-prd.md` | `publish delay` → `actions v1` | 4543.00t/hit | a1 291.50t/6 rows/hit, r6/usable-width => 291.50t/hit | a1 281.75t/6 rows/hit, r3/usable-width => 281.75t/hit | a1 1565.75t/13 rows/hit, r8/usable-width => 1565.75t/hit |
| 10 | `project/prds/architecture-deepening-round-3-prd.md` | `JavaScript queue` → `PHP rules` | 4543.00t/MISS | a1 195.25t/5 rows/MISS/usable-width => 195.25t/MISS | a1 362.25t/8 rows/MISS/usable-width => 362.25t/MISS | a1 1931.25t/17 rows/MISS/flood/zero; a2 527.00t/6 rows/MISS/usable-width => 2458.25t/MISS |
| 11 | `project/prds/mobile-gesture-suite-v2-prd.md` | `vibration drag` → `stay silent` | 4543.00t/hit | a1 52.75t/1 rows/MISS/usable-width => 52.75t/MISS | a1 209.75t/5 rows/hit, r1/usable-width => 209.75t/hit | a1 354.00t/1 rows/MISS/usable-width => 354.00t/MISS |
| 12 | `project/prds/pipeline-reliability-privacy-prd.md` | `upload response` → `retry lost` | 4543.00t/hit | a1 160.75t/3 rows/MISS/usable-width => 160.75t/MISS | a1 441.25t/10 rows/hit, r2/usable-width => 441.25t/hit | a1 526.50t/5 rows/hit, r2/usable-width => 526.50t/hit |
| 13 | `project/prds/frontend-modal-accessibility-prd.md` | `focus Escape` → `chest fullscreen` | 4543.00t/hit | a1 108.25t/2 rows/MISS/usable-width => 108.25t/MISS | a1 640.00t/14 rows/hit, r2/usable-width => 640.00t/hit | a1 591.00t/3 rows/hit, r3/usable-width => 591.00t/hit |
| 14 | `project/prds/lqip-metadata-hygiene-prd.md` | `preview source` → `cache changes` | 4543.00t/hit | a1 0.00t/0 rows/MISS/flood/zero; a2 33.25t/1 rows/MISS/usable-width => 33.25t/MISS | a1 574.75t/14 rows/hit, r1/usable-width => 574.75t/hit | a1 1728.25t/11 rows/hit, r7/usable-width => 1728.25t/hit |
| 15 | `project/prds/toolchain-static-analysis-hardening-prd.md` | `code checks` → `pipeline release` | 4543.00t/hit | a1 85.00t/2 rows/MISS/usable-width => 85.00t/MISS | a1 914.75t/20 rows/MISS/flood/zero; a2 454.75t/10 rows/hit, r4/usable-width => 1369.50t/hit | a1 964.50t/7 rows/MISS/usable-width => 964.50t/MISS |
| 16 | `project/prds/pack-download-surface-consolidation-prd.md` | `download URL` → `live mode` | 4543.00t/hit | a1 45.50t/1 rows/hit, r1/usable-width => 45.50t/hit | a1 946.00t/20 rows/hit, r1/flood/zero; a2 862.00t/20 rows/hit, r1/flood/zero => 1808.00t/MISS | a1 1876.25t/14 rows/hit, r10/usable-width => 1876.25t/hit |
| 17 | `project/plans/launch-plan.md` | `Git server` → `local machine` | 4543.00t/hit | a1 114.75t/2 rows/MISS/usable-width => 114.75t/MISS | a1 569.25t/13 rows/hit, r1/usable-width => 569.25t/hit | a1 546.25t/7 rows/hit, r4/usable-width => 546.25t/hit |
| 18 | `references/theme-build-flow.md` | `theme output` → `authored WordPress` | 4543.00t/MISS | a1 182.50t/7 rows/MISS/usable-width => 182.50t/MISS | a1 826.50t/20 rows/hit, r1/flood/zero; a2 891.50t/20 rows/hit, r6/flood/zero => 1718.00t/MISS | a1 1621.25t/18 rows/hit, r16/flood/zero; a2 2080.75t/20 rows/hit, r19/flood/zero => 3702.00t/hit |
| 19 | `references/wordpress-local-env.md` | `site URLs` → `environment setting` | 4543.00t/MISS | a1 112.75t/3 rows/MISS/usable-width => 112.75t/MISS | a1 906.25t/20 rows/hit, r16/flood/zero; a2 698.25t/17 rows/hit, r1/flood/zero => 1604.50t/MISS | a1 1439.00t/13 rows/hit, r11/usable-width => 1439.00t/hit |
| 20 | `research/adult-content-compliance-research.md` | `compliance material` → `explicit serving` | 4543.00t/hit | a1 41.50t/1 rows/hit, r1/usable-width => 41.50t/hit | a1 157.50t/4 rows/hit, r1/usable-width => 157.50t/hit | a1 622.50t/3 rows/hit, r1/usable-width => 622.50t/hit |

## Chains

A chain pays the primary method's total output and reads the full index only when the primary final result misses. The fallback's hit is then the chain hit. This is separate from the primary method's own median.

- **C first, index fallback:** median **572.00 tokens**, mean **2094.75 tokens**, final misses **3/20**, and **6/20** questions pay the ~4543-token index fallback.
- **D first, index fallback:** median **1802.25 tokens**, mean **3062.07 tokens**, final misses **1/20**, and **8/20** questions pay the ~4543-token index fallback.

The chain medians include fallback cost; they must not be reported as the primary method's median. The means expose the expensive tail that a median can hide.

## Content-first catalog extraction

The catalog is generated at `/tmp` only; its seven columns are `path`, vault-relative `kind`, Git date, inbound-link count, byte size, deterministic summary, and `##` heading keywords. The summary algorithm is:

1. Strip a leading YAML frontmatter block.
2. Scan sections in order, skipping H1. Treat metadata-only headings (`Date`, `Status`, `Metadata`, `Parent issue`, `Issue`, `Owner`, `Priority`, `State`, and `Seam`) as non-substantive.
3. In a substantive section, skip fenced code, badges, blank lines, navigation-only Markdown-link bullets, HTML comments, and metadata labels (`Date:`, `Status:`, `Updated:`, `Parent issue:`, issue/owner/priority/state/seam labels). A metadata label suppresses its wrapped continuation until the next blank line.
4. Take the first sentence of the first surviving prose paragraph. Reject bare status values, issue/seam fragments, TODO/fill placeholders, and the known context-map boilerplate. If no real prose survives, use the H1 title, or the path stem.

This is deterministic and model-free. It does not use an LLM to manufacture summaries. In this run the catalog has 155 data rows and every row has seven nonempty fields; its exact byte size is reported above.

## Original post-freeze query re-score

The exact original file is `concepts/bc-wiki-maintain/tests/retrieval-queries-original.tsv` (commit `54fd0cf9bf908d7b12529f57828656fb9198b8ec`). It preserves the strings from `git show ea0e1f9:concepts/bc-wiki-maintain/tests/retrieval-queries.tsv`; the current file is not rewritten. The affected questions are **12, 14, 15, 16, 17, 18, 19**. The fixed-method re-score uses the round-one whole-word OR/AND matchers and qmd `--format files -n 5`, with output bytes/4. A hit means the gold path appears in the method output; no flood reformulation is applied in this historical comparison.

| Q | Original query | Current query | Method | Current miss? | Original miss? | Change |
|---:|---|---|---|:---:|:---:|---:|
| 12 | `retry WordPress upload response lost` | `retry WordPress upload lost` | `B_index_OR` | yes | yes | unchanged |
| 12 | `retry WordPress upload response lost` | `retry WordPress upload lost` | `B_index_AND` | yes | yes | unchanged |
| 12 | `retry WordPress upload response lost` | `retry WordPress upload lost` | `C_qmd` | no | no | unchanged |
| 12 | `retry WordPress upload response lost` | `retry WordPress upload lost` | `D_catalog_OR` | no | no | unchanged |
| 12 | `retry WordPress upload response lost` | `retry WordPress upload lost` | `D_catalog_AND` | yes | yes | unchanged |
| 14 | `cached preview source image changes` | `cached preview source changes` | `B_index_OR` | yes | yes | unchanged |
| 14 | `cached preview source image changes` | `cached preview source changes` | `B_index_AND` | yes | yes | unchanged |
| 14 | `cached preview source image changes` | `cached preview source changes` | `C_qmd` | no | no | unchanged |
| 14 | `cached preview source image changes` | `cached preview source changes` | `D_catalog_OR` | no | no | unchanged |
| 14 | `cached preview source image changes` | `cached preview source changes` | `D_catalog_AND` | yes | yes | unchanged |
| 15 | `code checks pipeline theme release` | `code checks pipeline release` | `B_index_OR` | yes | yes | unchanged |
| 15 | `code checks pipeline theme release` | `code checks pipeline release` | `B_index_AND` | yes | yes | unchanged |
| 15 | `code checks pipeline theme release` | `code checks pipeline release` | `C_qmd` | no | no | unchanged |
| 15 | `code checks pipeline theme release` | `code checks pipeline release` | `D_catalog_OR` | yes | yes | unchanged |
| 15 | `code checks pipeline theme release` | `code checks pipeline release` | `D_catalog_AND` | yes | yes | unchanged |
| 16 | `old download URL live mode` | `old download URL live` | `B_index_OR` | no | no | unchanged |
| 16 | `old download URL live mode` | `old download URL live` | `B_index_AND` | yes | yes | unchanged |
| 16 | `old download URL live mode` | `old download URL live` | `C_qmd` | yes | yes | unchanged |
| 16 | `old download URL live mode` | `old download URL live` | `D_catalog_OR` | no | no | unchanged |
| 16 | `old download URL live mode` | `old download URL live` | `D_catalog_AND` | yes | yes | unchanged |
| 17 | `Git local machine server state` | `Git local machine server` | `B_index_OR` | yes | yes | unchanged |
| 17 | `Git local machine server state` | `Git local machine server` | `B_index_AND` | yes | yes | unchanged |
| 17 | `Git local machine server state` | `Git local machine server` | `C_qmd` | no | no | unchanged |
| 17 | `Git local machine server state` | `Git local machine server` | `D_catalog_OR` | no | no | unchanged |
| 17 | `Git local machine server state` | `Git local machine server` | `D_catalog_AND` | yes | yes | unchanged |
| 18 | `authored theme files WordPress output` | `authored theme WordPress output` | `B_index_OR` | yes | yes | unchanged |
| 18 | `authored theme files WordPress output` | `authored theme WordPress output` | `B_index_AND` | yes | yes | unchanged |
| 18 | `authored theme files WordPress output` | `authored theme WordPress output` | `C_qmd` | no | yes | hit→miss |
| 18 | `authored theme files WordPress output` | `authored theme WordPress output` | `D_catalog_OR` | no | no | unchanged |
| 18 | `authored theme files WordPress output` | `authored theme WordPress output` | `D_catalog_AND` | yes | yes | unchanged |
| 19 | `environment setting site URLs WordPress` | `environment site URLs WordPress` | `B_index_OR` | yes | yes | unchanged |
| 19 | `environment setting site URLs WordPress` | `environment site URLs WordPress` | `B_index_AND` | yes | yes | unchanged |
| 19 | `environment setting site URLs WordPress` | `environment site URLs WordPress` | `C_qmd` | no | no | unchanged |
| 19 | `environment setting site URLs WordPress` | `environment site URLs WordPress` | `D_catalog_OR` | no | no | unchanged |
| 19 | `environment setting site URLs WordPress` | `environment site URLs WordPress` | `D_catalog_AND` | yes | yes | unchanged |

### Original-query aggregate

| Method | Current misses | Original misses | Delta | Wilson 95% CI, original | Interpretation |
|---|---:|---:|---:|---|---|
| `B_index_OR` | 6/7 | 6/7 | +0 | [0.49, 0.97] | safe failure (CI lower bound > 0.30) |
| `B_index_AND` | 7/7 | 7/7 | +0 | [0.65, 1.00] | safe failure (CI lower bound > 0.30) |
| `C_qmd` | 1/7 | 2/7 | +1 | [0.08, 0.64] | inside noise (CI crosses 0.30) |
| `D_catalog_OR` | 1/7 | 1/7 | +0 | [0.03, 0.51] | inside noise (CI crosses 0.30) |
| `D_catalog_AND` | 7/7 | 7/7 | +0 | [0.65, 1.00] | safe failure (CI lower bound > 0.30) |

The incumbent A result is query-independent and therefore unchanged; it is not duplicated in the row table. The aggregate makes any wording-induced movement visible rather than treating the edited current file as the only freeze.

## Index structure and limitations

The index graph reaches 118 pages at depth 1 and 139 at depth <=2. This benchmark still uses the explicit A row judgments, so reachability is a structural diagnostic rather than an automatic hit. The question set is n=20 and has the distribution/skew documented in the pre-registered question file; Wilson intervals are therefore essential.

The catalog can be better than round one without being the right first move. If its agent-style row filter still misses the cost and miss bars, that is structural pressure: adding deterministic summary prose can recover terms absent from the row, but every added byte raises the cost of a whole-row flood. The result must distinguish that squeeze from the old status-fragment parser and four-word AND protocol.

## Reproduction

```sh
python3 concepts/bc-wiki-maintain/tests/run_retrieval_benchmark_round2.py \
  "$HOME/Sync/Work/Development/wp-theme-builds/localhost/image-maze/.bc-agent" \
  --collection image-maze
```

The script takes the vault path as an argument, accepts `--collection` and `--qmd-bin`, writes the catalog under `/tmp`, and writes this report to `--results` (default `retrieval-results-round2.md`). It never invokes qmd update, embed, init, cleanup, collection, or context mutation commands.

## Source citations

- `concepts/bc-wiki-maintain/tests/retrieval-questions.md`: the 20 questions and gold paths used by this run.
- `concepts/bc-wiki-maintain/tests/retrieval-queries-round2.tsv`: pre-registered one/two-term primary and reformulation pairs.
- `concepts/bc-wiki-maintain/tests/retrieval-queries-original.tsv`: exact pre-width-fix query strings from the ea0e1f9 tree.
- `/tmp/bc-retrieval-round2-catalog-r9bec0l0.tsv`: this run's generated seven-column catalog; it is disposable and not an in-vault artifact.
- `/home/ben/Sync/Work/Development/wp-theme-builds/localhost/image-maze/.bc-agent/index.md`: incumbent index bytes and graph source.

## Correction: the incumbent's accuracy was self-assessed and is inflated

`A_index_read`'s 3/20 miss rate in round one and above comes from the benchmark author judging
its own picks with the gold answers visible. An independent agent then made the same 20 picks
from `index.md` alone, never seeing the gold column
(see [`retrieval-blind-index-judgment.md`](retrieval-blind-index-judgment.md)).

Blind result: **6/20 misses (0.30), Wilson [0.15, 0.52]** — double the self-assessed 0.15.
Q7 is credited as a hit: the judge named the right ADR but reconstructed its filename from the
link title rather than the href.

Corrected standings under the round-two agent-style protocol:

| Method | Median tokens | Miss | Wilson 95% CI |
|---|---:|---:|---|
| `A_index_read` (blind) | 4543.00 | 6/20 = 0.30 | [0.15, 0.52] |
| `B_index_agent_filter` | 113.75 | 14/20 = 0.70 | [0.48, 0.85] |
| `C_qmd_agent_filter` | 499.75 | 6/20 = 0.30 | [0.15, 0.52] |
| `D_catalog_agent_filter` | 743.50 | 8/20 = 0.40 | [0.22, 0.61] |

`A` and `C` have the **same measured miss rate**; `C` reaches it for **1/9th the tokens**. The
chain "C first, read the index on a C miss" is median 572.00, mean 2094.75, final miss 4/20 = 0.20
(three of A's rescues survive blind judging; Q5, Q10, Q18 and Q19 defeat both).

### What is and is not safe at n = 20

Safe:
- `B` fails the miss bar — CI lower bound 0.48 is above 0.30. Boolean filtering of one-line
  curated rows is genuinely dead, not merely undertuned.
- Query shape dominates everything else. Round one measured the same qmd index at 17/20 misses
  for full-sentence queries, CI [0.64, 0.95], against 5/20 for keywords, CI [0.11, 0.47]. Those
  intervals do not overlap.
- All token figures are measurements, not estimates. `A` costing 9x `C` is not a statistical claim.

Not safe:
- Any ranking of `C` against `D` by accuracy. The intervals overlap almost entirely.
- Any claim that a method reliably clears 0.30. Every CI except `B`'s crosses it.

The catalog is therefore not falsified on accuracy. It is **dominated**: at its fairest build it
costs more and misses more than a tool already installed, and its cost rises as its quality does —
the content-first rebuild grew it from 42,421 to 57,125 bytes precisely because the summaries got
better. The burden of proof sits on new machinery, and it was not met.
