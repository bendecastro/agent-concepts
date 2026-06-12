# Concept: prompting-agents

A reference library of proven instruction blocks for authoring agent instructions — concept bodies, AGENTS.md files, system prompts, per-agent configs. Exists so workspace authors adapt eval-tested phrasings instead of inventing instruction language from scratch.

## Design decisions

- **Reference type, not discipline type** — it constrains how concepts are *written*, not how an agent behaves at runtime, so the test gate's pressure-scenario requirement doesn't apply. Its test is accuracy: blocks must stay faithful to their sources (see tests/).
- **Agent-agnostic rewrites, not verbatim copies** — OpenAI's blocks reference their tool names (`multi_tool_use.parallel`, `apply_patch`); blocks here are rewritten to the underlying behavior so they apply to any agent. Harness-specific plumbing (apply_patch grammars, `phase` fields, compaction API) deliberately excluded — that's API integration, not prompting.
- **Origin-tagged adaptation** — when a block is copied into a concept or agent config, note where it came from so source updates can propagate.
- **Metaprompting included as a maintenance loop** — the technique (have the underperforming agent propose generalized fixes to its own instructions, adopt only recurring suggestions, test before deploy) composes with this workspace's implement/test operations.

## Provenance

- `ideas/openai-gpt-5-2-prompting-guide.md` — verbosity clamps, scope discipline, long-context re-grounding, ambiguity/hallucination handling, user-update specs, tool-usage rules, research-agent appendix. https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide
- `ideas/openai-codex-prompting-guide.md` — autonomy/persistence, loop-breaker, plan closure and promise discipline, final-message style, dirty-worktree etiquette, frontend anti-slop, custom-tool naming guidance, metaprompting. https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide

## Tests

`tests/accuracy-check.md` — verify each block traces to its source and hasn't drifted in meaning during agent-agnostic rewriting.

## Deploy targets

None — consumed in-place by agents working in this workspace (the Implement operation in AGENTS.md points here). Not symlinked into any agent's skills directory.
