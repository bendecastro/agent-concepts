# Concept: seo

A two-part SEO operator: `body/SKILL.md` is the site-wide strategist (diagnosis-first auditing, prioritized by impact × confidence ÷ effort, across crawl/index/rank/present including GEO and AI-crawler policy); `body/IMAGE-SEO.md` is the per-asset image specialist (vision-required metadata packages: filename, alt, caption, ImageObject JSON-LD, IPTC/XMP, delivery). Built from the user's own prior work on the image-maze project.

## Design decisions

- **One concept, two body files** — the pair shares a handoff contract whose field lists are owned solely by `IMAGE-SEO.md` (single owner so the contract can't drift, per the original README). Splitting into two concepts would put the contract across directory boundaries for no benefit.
- **Verbatim-preserving adaptation** — the source prompts were recently authored, evidence-tiered, and myth-rejecting; the canon copies change only what portability into this workspace requires (frontmatter, cross-reference names, removal of project-specific references). The image-maze project adapter was left in the work repo where its wiki is authoritative.
- **Scoped skill trigger** — the Agent Skills description is intentionally SEO-specific and names image metadata, while excluding generic performance/accessibility/content/analytics work unless the user frames it as SEO. This keeps the long prompt from loading for adjacent tasks.
- **Verify-at-runtime over baked numbers — validated by research** — during ingest (2026-06-12), SEO-blog sources made conflicting claims about 2026 CWV changes ("LCP tightened to 2.0s", "Visual Stability Index", none verifiable against official documentation). The prompts' standing instruction to verify thresholds/statistics at runtime is the correct design; no blog-sourced numbers were baked in; a volatile-facts rule now makes this explicit for thresholds, bot behavior, feature status, and platform policy, and points to `body/CITATIONS.md` so the held source map deploys with the skill.
- **AI-crawler access policy added, but non-absolute** (the one research delta): 2026's training-vs-search bot split (GPTBot vs OAI-SearchBot, ClaudeBot vs Claude-SearchBot, Google-Extended) makes crawler access a deliberate per-site decision; `llms.txt` is not honored by major AI systems as of early 2026 and is labeled speculative. robots.txt remains the working control surface, but provider effects must be verified before claiming exclusion or eligibility.
- **Discipline lives in the prompts already** — diagnose-before-prescribe, no-spam-tactics, see-it-don't-fabricate, and verify-stats-at-runtime are gate-shaped rules; `tests/` formalizes attacks against each and now includes one artifact-producing audit scenario.

## Provenance

- `raw/image-maze-seo-agents/` — snapshot of the user's prompts (authored 2026-06-11) from `~/Sync/Work/Development/wp-theme-builds/localhost/image-maze/.agent/agents/`; the work repo remains a live consumer, not the canon.
- `raw/seo-primary-sources/` — the traced primary-documentation evidence base (Google Search Central, web.dev, W3C WAI, OpenAI bot docs); the claim→source map is [body/CITATIONS.md](body/CITATIONS.md), which also lists the three not-yet-snapshotted gaps.
- AI-crawler/llms.txt delta: web research 2026-06-12 — training-vs-search bot split and llms.txt non-adoption corroborated across multiple sources (e.g. digitalapplied.com AI-crawler decision matrix, nohacks.co AI user-agent landscape, limy.ai llms.txt guide); bot lists change, verify at runtime.
- CWV-claims conflict (reason no numbers were updated): 2026 SEO-blog survey returned contradictory threshold claims; official documentation is the only acceptable source for these, checked at runtime.

## Tests

`tests/pressure-scenarios.md` — attacks on the four gate-shaped rules: spam-tactic pressure, fabricated image metadata, checklist-dump pressure, myth/stale-stat assertion. Last conversational run 2026-06-12 (Claude Code subagent): all held. Artifact-producing workflow scenario run 2026-06-12: pass, verified via artifacts (noindex prioritized, robots AI-bot block flagged not auto-edited, no fabrication for placeholder image).

## Deploy targets

- Claude Code: `~/.claude/skills/seo` → relative symlink to `body/` (deployed 2026-06-12 after pressure test).
- Pi: `~/.pi/agent/skills/seo` → relative symlink to `body/` (deployed 2026-06-12 after narrowing trigger and adding citation map).
- The image-maze work repo currently loads its own copies; migrating its `.claude/agents/` wrappers to point at this canon is a candidate follow-up — decide in that repo, not here.
- Other harnesses: manual bootstrap (`bootstrap.md`); `IMAGE-SEO.md` additionally requires a vision-capable model.
