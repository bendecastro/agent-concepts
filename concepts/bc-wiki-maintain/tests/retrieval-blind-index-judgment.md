# Blind index judging

I read only `questions-blind.tsv` and the vault `index.md` before making these picks. The quoted text below is copied from `index.md`; no answer-key or vault page was opened.

| # | Question | Chosen vault-relative path | Exact `index.md` line that drove the choice | Confidence | Optional second choice |
|---:|---|---|---|---|---|
| 1 | Where should I record a new durable fact, and what must I do before ending the work? | `AGENTS.md` | “- Agent maintainer instructions -> AGENTS.md — read this; you maintain this wiki” | high | — |
| 2 | What should I do when I cannot inspect the actual picture before writing its metadata? | `agents/image-seo-agent.md` | “- Project-local agent prompts: README/loading -> agents/README.md, SEO optimizer -> agents/seo-agent.md, Image SEO agent -> agents/image-seo-agent.md, image-maze adapter -> agents/image-maze-context.md (Claude Code wrappers in `.claude/agents/`)” | high | — |
| 3 | Which corner sizes should I use for a button, a panel, and a status dot? | `conventions/styling-radius-scale.md` | “- Border-radius token scale -> conventions/styling-radius-scale.md — `$radius-sm/md/lg/pill`; use tokens, never literals” | high | — |
| 4 | What names should payment adapters emit for subscription lifecycle events? | `decisions/adr-0003-provider-first-subscription-architecture.md` | “- ADR-0003: Provider-first subscription architecture -> decisions/adr-0003-provider-first-subscription-architecture.md — generic provider/event/entitlement first, then CCBill as first real provider” | medium | `project/plans/digital-chest-unlock/ccbill-subscription-options.md` |
| 5 | Did the first cleanup turn up an approach we need to keep on record? | `research/free-improvement-review-2026-07-12.md` | “- Free improvement review 2026-07-12 -> research/free-improvement-review-2026-07-12.md — second-pass candidates beyond the #144–#147 hardening PRDs: sitemap render scale, LQIP meta bloat, DCU observability, security headers, WP-Cron reliance” | medium | `research/free-improvement-review-2026-07-30.md` |
| 6 | How should a mouse click differ from a touch tap in the fullscreen viewer? | `decisions/adr-0019-desktop-mouse-click-dismisses-fullscreen.md` | “- ADR-0019: A mouse click dismisses the fullscreen viewer -> decisions/adr-0019-desktop-mouse-click-dismisses-fullscreen.md — desktop overrule of ADR-0017” | high | `decisions/adr-0017-fullscreen-gesture-vocabulary-v2.md` |
| 7 | If a caller leaves out rate limiting, should the referral flow still allow traffic? | `decisions/adr-0029-dcu-missing-fraud-sensitive-ports-fail-closed.md` | “- ADR-0029: DCU missing fraud-sensitive ports fail closed -> decisions/adr-0029-dcu-missing-fraud-sensitive-ports-fail-closed.md — rate_limit_* deny; prior_event_exists treats slot as used (#228)” | high | — |
| 8 | Which WordPress adapter should we extract first, and why? | `project/arch-review/architecture-adapter-split-arch-review.md` | “- Architecture Adapter Split — architecture review -> project/arch-review/architecture-adapter-split-arch-review.md” | high | `project/architecture-module-map.md` |
| 9 | Which WordPress publish actions actually enter the delay in v1? | `project/prds/automatic-publish-queue-prd.md` | “- Automatic Publish Queue PRD -> project/prds/automatic-publish-queue-prd.md” | medium | `project/prds/publish-cadence-reliability-prd.md` |
| 10 | How will we keep the PHP and JavaScript copies of the queue rules from drifting apart? | `project/arch-review/automatic-publish-queue-adapter-arch-review.md` | “- Automatic Publish Queue Adapter — architecture review -> project/arch-review/automatic-publish-queue-adapter-arch-review.md” | medium | `project/prds/automatic-publish-queue-prd.md` |
| 11 | When should the small vibration fire during a drag, and when should it stay silent? | `project/prds/mobile-gesture-suite-v2-prd.md` | “- Mobile Gesture Suite v2 PRD -> project/prds/mobile-gesture-suite-v2-prd.md — pinch-zoom + 1× gate, chrome toggle, Pinch Close, Pack Peek Sheet, grabber, long-press guard, Commit Tick (#115, slices #116–#123)” | high | — |
| 12 | What should a retry do after WordPress accepted an upload but the response was lost? | `project/prds/pipeline-reliability-privacy-prd.md` | “- Pipeline Reliability and Privacy PRD -> project/prds/pipeline-reliability-privacy-prd.md — parent #145; slices #152–#156 **complete** (living requirements all verified)” | high | — |
| 13 | When the chest opens inside fullscreen, which controls own focus and Escape? | `project/prds/frontend-modal-accessibility-prd.md` | “- Frontend Modal Accessibility PRD -> project/prds/frontend-modal-accessibility-prd.md — parent #146; slices #160–#163 **complete** (closeout #163)” | medium | `decisions/adr-0025-browser-driven-fullscreen-exit-closes-viewer.md` |
| 14 | How should a cached preview be refreshed when its source image changes? | `project/plans/current-pack-thumbnail-plan.md` | “- Current pack thumbnail plan -> project/plans/current-pack-thumbnail-plan.md — **complete** current-image display thumbnail, verified-load persistence, and broken-image fallback” | high | — |
| 15 | What code checks must run on the pipeline and theme before release, and how strict are they? | `project/prds/toolchain-static-analysis-hardening-prd.md` | “- Toolchain and Static Analysis Hardening PRD -> project/prds/toolchain-static-analysis-hardening-prd.md — parent #190; build-path guard #191, strict TypeScript #192, PHPStan level 5 #193, adapter coverage #194–#195, docs closeout #196 (slice map -> project/plans/toolchain-static-analysis-hardening/tasks.md)” | high | `conventions/validation.md` |
| 16 | What should the old download URL do when live mode is on? | `project/prds/pack-download-surface-consolidation-prd.md` | “- Pack Download Surface Consolidation PRD -> project/prds/pack-download-surface-consolidation-prd.md — parent **#216** **complete**; #221 `d826a07`, #222 `08552ce`, #223 `6d25616`” | high | — |
| 17 | Which parts live in Git, which stay on the local machine, and which remain server state? | `conventions/file-layout.md` | “- File layout -> conventions/file-layout.md” | medium | `project/plans/launch-plan.md` |
| 18 | Where do authored theme files become the WordPress theme, and what output must I never edit by hand? | `conventions/file-layout.md` | “- File layout -> conventions/file-layout.md” | medium | `decisions/adr-0024-npm-fallback-may-not-produce-tracked-dist.md` |
| 19 | What environment setting controls the site URLs in local versus hosted WordPress? | **NO CANDIDATE** | NO USABLE INDEX LINE: `index.md` has no entry naming site URLs or the relevant environment setting. | low | — |
| 20 | What compliance work is still missing before serving explicit material? | `research/adult-content-compliance-research.md` | “- Adult-content mode compliance research -> research/adult-content-compliance-research.md — Google/SafeSearch, age-verification laws, 2257, RTA, card-network rules” | medium | `project/prds/adult-mode-prd.md` |

**Evidence note:** the quoted `index.md` lines below come from another repository. Their
Markdown links are transcribed as `title -> path` so this workspace's linter does not read
them as links here. Wording and paths are otherwise verbatim.

## Index-only outcome summary

- Confident single candidate (high confidence, no second choice): **7/20**.
- Ambiguous field (a plausible second row was worth recording, or confidence was medium): **12/20**.
- Nothing usable in `index.md`: **1/20** (question 19).

These are retrieval judgments from the index alone, not claims about the contents of the selected pages. I did not open any selected page afterward, so there are no post-selection corrections.

Commit: none
Branch: none

## Acceptance report

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Completed a 20-row table with vault-relative paths (or NO CANDIDATE), exact index excerpts, confidence, and optional second choices."
    }
  ],
  "changedFiles": [
    "/tmp/bc-swarm/2026-08-27-filter-vs-cat/blindjudge.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "read questions-blind.tsv and vault .bc-agent/index.md; nl -ba vault .bc-agent/index.md",
      "result": "passed",
      "summary": "Read only the supplied questions and vault index for judging; prohibited answer-key files were not opened."
    }
  ],
  "validationOutput": [
    "20 questions are represented in the table, numbered 1 through 20.",
    "Commit: none; Branch: none."
  ],
  "residualRisks": [
    "The choices are intentionally index-only retrieval judgments; selected pages were not opened and contents were not independently verified."
  ],
  "noStagedFiles": true,
  "diffSummary": "Created the blind-judging artifact only; no repository files were edited.",
  "reviewFindings": [
    "no blockers found in the required blind-judging artifact"
  ],
  "manualNotes": "The hidden answer-key and other prohibited benchmark files were not opened."
}
```
