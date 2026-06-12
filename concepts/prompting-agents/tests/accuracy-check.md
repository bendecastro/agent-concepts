# Test: source accuracy

This is a reference concept — no runtime gates to pressure-test. Its failure mode is drift: blocks that no longer say what their sources said, or invented "patterns" with no provenance.

## Procedure

For each block in `../body/SKILL.md`, locate the corresponding section in the provenance files (`ideas/openai-gpt-5-2-prompting-guide.md`, `ideas/openai-codex-prompting-guide.md`) and check:

1. The behavioral claim survives the agent-agnostic rewrite (no meaning inversion, no scope inflation).
2. Nothing harness-specific leaked in (tool names, API endpoints, model ids).
3. No block exists without a source section — anything unsourced is a parametric guess and gets removed or sourced.

**Pass:** every block traces; **fail:** any orphan block or meaning drift.

## History

- 2026-06-12 — initial authoring checked against both sources during extraction (same session); first independent re-check due when a new OpenAI guide version is ingested.
