# Retrieval benchmark — image-maze question set

Pre-registered 2026-08-27, **before** any harness or retrieval method was built or tuned
against it. Authored by an agent given only the vault contents and told nothing about the
methods under test, so the wording cannot flatter one of them.

Vault: `image-maze/.bc-agent`, 155 eligible pages (tracked Markdown, `temp/` excluded).
Gold pages were sampled proportionally across top-level directories, spread across commit
dates, with at least a third drawn from the oldest third of the vault.

Fairness property: **15 of the 20 questions share zero rare content words with their gold
page** (rare = the exact token appears in 3 or fewer eligible pages). The set does not hand
lexical matching an easy win.

Known skew, from the author's own adversarial review: `project/` supplies 10 of 20 rows and
is PRD-heavy; no question targets `tasks/`, `templates/`, `specs/`, or raw sources; dates
cluster around the 2026-07-12 documentation commit; questions ask for explicit policy more
often than the vague half-remembered queries people type while debugging. Question 6 is the
weakest — neighbouring ADRs describe the same gesture vocabulary.

| # | Question | Gold page | Dir | Last commit |
|---|---|---|---|---|
| 1 | where should I record a new durable fact, and what must I do before ending the work? | `AGENTS.md` | vault root | 2026-06-26 |
| 2 | what should I do when I cannot inspect the actual picture before writing its metadata? | `agents/image-seo-agent.md` | agents | 2026-06-21 |
| 3 | which corner sizes should I use for a button, a panel, and a status dot? | `conventions/styling-radius-scale.md` | conventions | 2026-07-09 |
| 4 | what names should payment adapters emit for subscription lifecycle events? | `decisions/adr-0003-provider-first-subscription-architecture.md` | decisions | 2026-06-21 |
| 5 | did the first cleanup turn up an approach we need to keep on record? | `decisions/adr-0005-architecture-deepening-no-rejected-designs.md` | decisions | 2026-06-26 |
| 6 | how should a mouse click differ from a touch tap in the fullscreen viewer? | `decisions/adr-0019-desktop-mouse-click-dismisses-fullscreen.md` | decisions | 2026-07-26 |
| 7 | if a caller leaves out rate limiting, should the referral flow still allow traffic? | `decisions/adr-0029-dcu-missing-ports-fail-closed.md` | decisions | 2026-07-30 |
| 8 | which WordPress adapter should we extract first, and why? | `project/arch-review/architecture-adapter-split-arch-review.md` | project | 2026-06-26 |
| 9 | which WordPress publish actions actually enter the delay in v1? | `project/prds/automatic-publish-queue-prd.md` | project | 2026-06-26 |
| 10 | how will we keep the PHP and JavaScript copies of the queue rules from drifting apart? | `project/prds/architecture-deepening-round-3-prd.md` | project | 2026-07-03 |
| 11 | when should the small vibration fire during a drag, and when should it stay silent? | `project/prds/mobile-gesture-suite-v2-prd.md` | project | 2026-07-08 |
| 12 | what should a retry do after WordPress accepted an upload but the response was lost? | `project/prds/pipeline-reliability-privacy-prd.md` | project | 2026-07-12 |
| 13 | when the chest opens inside fullscreen, which controls own focus and Escape? | `project/prds/frontend-modal-accessibility-prd.md` | project | 2026-07-12 |
| 14 | how should a cached preview be refreshed when its source image changes? | `project/prds/lqip-metadata-hygiene-prd.md` | project | 2026-07-13 |
| 15 | what code checks must run on the pipeline and theme before release, and how strict are they? | `project/prds/toolchain-static-analysis-hardening-prd.md` | project | 2026-07-26 |
| 16 | what should the old download URL do when live mode is on? | `project/prds/pack-download-surface-consolidation-prd.md` | project | 2026-07-30 |
| 17 | which parts live in Git, which stay on the local machine, and which remain server state? | `project/plans/launch-plan.md` | project | 2026-08-17 |
| 18 | where do authored theme files become the WordPress theme, and what output must I never edit by hand? | `references/theme-build-flow.md` | references | 2026-07-12 |
| 19 | what environment setting controls the site URLs in local versus hosted WordPress? | `references/wordpress-local-env.md` | references | 2026-08-17 |
| 20 | what compliance work is still missing before serving explicit material? | `research/adult-content-compliance-research.md` | research | 2026-07-08 |

## W4 log-overlap extension

The round-two query file marks eight of these 20 questions as `log-overlap` cases. Each marked
case targets a non-root compiled page; the benchmark verifies that the gold page and the
append-only `log.md` share an exact contiguous run of at least six normalized tokens before
measuring the incumbent and the page-kind candidate. The remaining 12 rows retain the original
round-two query protocol, so the experiment stays n=20 rather than adding a second question set.
