# Index

## Concepts

- [teach](concepts/teach/CONCEPT.md) — multi-session learning tutor with SRS queue, knowledge wiki, and discipline gates (defaults with a principled exit). Status: deployed+tested. Deployed: Claude Code (symlink, 2026-06-12). Tested: 2026-06-12 ×2 (incl. gate-challenge attack), all gates held.
- [prompting-agents](concepts/prompting-agents/CONCEPT.md) — reference library: altitude-first principles (right altitude, explain-the-why, general-over-prescriptive, context economy), eval-tested instruction blocks, technique repertoire, metaprompting. Status: implemented+tested. Not deployed (consumed in-place). Tested: 2026-06-12, accuracy check at authoring.

## Tooling

- [scripts/lint.py](scripts/lint.py) — mechanical drift checks for concept/index/provenance/test/link/deploy hygiene.

## Ideas

- [karpathy-llm-wiki.md](ideas/karpathy-llm-wiki.md) — Karpathy's LLM Wiki gist. Ingested → teach (2026-06-12).
- [pocock-teach-skill-original.md](ideas/pocock-teach-skill-original.md) — Matt Pocock's original teach skill. Ingested → teach (2026-06-12).
- [openai-gpt-5-2-prompting-guide.md](ideas/openai-gpt-5-2-prompting-guide.md) — OpenAI's latest flagship prompting guide: verbosity/output-shape control, scope-drift prevention, ambiguity & hallucination handling, compaction, agentic steerability, tool parallelism. Ingested → prompting-agents (2026-06-12).
- [openai-codex-prompting-guide.md](ideas/openai-codex-prompting-guide.md) — how OpenAI prompts their own coding agent: autonomy/persistence, editing constraints, plan tool, final-message style, AGENTS.md usage, compaction. Ingested → prompting-agents + bootstrap.md Codex quirks (2026-06-12).
- [obra-superpowers/](ideas/obra-superpowers/SOURCE.md) — snapshot of Jesse Vincent's 14 superpowers skills (commit 6fd4507, MIT): TDD, systematic-debugging (with its own pressure tests + creation log), brainstorming, writing-plans/executing-plans, subagent-driven-development, code review pair, verification-before-completion, writing-skills + Anthropic best practices. Filed 2026-06-12, not yet ingested (the test-gate pattern in AGENTS.md already derives from writing-skills).
- [anthropic-claude-prompting-best-practices.md](ideas/anthropic-claude-prompting-best-practices.md) — Anthropic's official prompting reference for current Claude models (clarity, examples, XML structuring, thinking, agentic systems). Ingested → prompting-agents altitude principles (2026-06-12); more remains extractable.
- [anthropic-claude-code-best-practices.md](ideas/anthropic-claude-code-best-practices.md) — official Claude Code best practices (context management, plan/execute separation, constraints as guardrails). Filed 2026-06-12, not yet ingested.
- [anthropic-context-engineering.md](ideas/anthropic-context-engineering.md) — Anthropic engineering essay on context engineering for agents ("smallest set of high-signal tokens"); widely cited successor framing to prompt engineering. Ingested → prompting-agents right-altitude section + AGENTS.md Spirit (2026-06-12).
- [google-boonstra-prompt-engineering-v7.pdf](ideas/google-boonstra-prompt-engineering-v7.pdf) — Google/Lee Boonstra prompt engineering whitepaper v7 (45 pp): sampling params, zero/few-shot, system/role/contextual prompting, step-back, CoT, self-consistency, ToT, ReAct, APE. Ingested → prompting-agents technique repertoire (2026-06-12); sampling-params material unused so far.

## Gaps

- xAI/Grok official prompting guidance: the grok-code-fast-1 guide was removed from docs.x.ai after the model's deprecation (May 2026), and no successor guide for Grok Build / grok-build-0.1 was found yet. Re-search when xAI publishes one; until then Grok prompting falls back to the agent-agnostic blocks in prompting-agents.
