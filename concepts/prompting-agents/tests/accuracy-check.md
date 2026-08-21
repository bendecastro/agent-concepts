# Test: source accuracy

This is a reference concept — no runtime gates to pressure-test. Its failure mode is drift: blocks that no longer say what their sources said, or invented "patterns" with no provenance.

Local raw clippings were removed from this workspace (citation-only policy). Missing local files are **not** a fail.

## Procedure

For each `##` block in `../body/SKILL.md`, fetch the **live URL** listed for that block in `../CONCEPT.md` Provenance (the upstream link, not a local clipping path) and check:

1. The behavioral claim survives the agent-agnostic rewrite (no meaning inversion, no scope inflation).
2. Nothing harness-specific leaked in (tool names, API endpoints, model ids).
3. No block exists without a source section — anything unsourced is a parametric guess and gets removed or sourced.

If a URL is unfetchable (bot wall, 4xx, empty body), mark that block **BLOCKED**, not FAIL.

Local-only expansions already flagged in `CONCEPT.md` (the 2026-08-17 metaprompting expansion: locus, mechanism-before-rewrite, replace-over-append) are checked against `CONCEPT.md`, not an upstream page.

OpenAI cookbook pages may be fetched as Markdown by appending `.md` when HTML is noisy. Claude Code docs likewise expose `/docs/en/best-practices.md`.

**Pass:** every block traces (or is BLOCKED on fetch, or is a documented local expansion). **Fail:** any orphan block or meaning drift against a successfully fetched source.

## History

- 2026-06-12 — initial authoring checked against both sources during extraction (same session); first independent re-check due when a new OpenAI guide version is ingested.
- 2026-06-20 — checked new skill-composition block against Matt Pocock skills catalog clipping during ingest; claims are limited to README-level patterns, not the linked skill bodies.
- 2026-06-20 — checked new agent-ready work-shaping block against AI Engineer Workshop clipping; claims are limited to the workshop page summary, not unviewed course content.
- 2026-06-20 — checked project-runway addition against the companion project README; claims are limited to the listed prerequisites, setup, scripts, and stack.
- 2026-08-21 — procedure changed from local provenance files to live URLs in CONCEPT.md Provenance (citation-only; clippings not restored). Unfetchable URLs are BLOCKED, not FAIL.
- 2026-08-21 — live-URL run: all `##` blocks PASS against fetched sources except Technique repertoire (Boonstra/Kaggle) **BLOCKED** (landing-page HTML, no whitepaper body). No harness leakage. No orphan `##` blocks. Overall **PASS** under the new rule (BLOCKED ≠ FAIL).
