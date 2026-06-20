# Test: source accuracy

This is a reference concept — no runtime gates to pressure-test. Its failure mode is drift: blocks that no longer say what their sources said, or invented "patterns" with no provenance.

## Procedure

For each block in `../body/SKILL.md`, locate the corresponding section in the provenance files named in `../CONCEPT.md` and check:

1. The behavioral claim survives the agent-agnostic rewrite (no meaning inversion, no scope inflation).
2. Nothing harness-specific leaked in (tool names, API endpoints, model ids).
3. No block exists without a source section — anything unsourced is a parametric guess and gets removed or sourced.

**Pass:** every block traces; **fail:** any orphan block or meaning drift.

## History

- 2026-06-12 — initial authoring checked against both sources during extraction (same session); first independent re-check due when a new OpenAI guide version is ingested.
- 2026-06-20 — checked new skill-composition block against Matt Pocock skills catalog clipping during ingest; claims are limited to README-level patterns, not the linked skill bodies.
- 2026-06-20 — checked new agent-ready work-shaping block against AI Engineer Workshop clipping; claims are limited to the workshop page summary, not unviewed course content.
- 2026-06-20 — checked project-runway addition against the companion project README; claims are limited to the listed prerequisites, setup, scripts, and stack.
