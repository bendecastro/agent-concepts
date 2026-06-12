# Index

## Concepts

- [teach](concepts/teach/CONCEPT.md) — multi-session learning tutor with SRS queue, knowledge wiki, and discipline gates. Deployed: Claude Code (symlink, 2026-06-12). Tested: 2026-06-12, all gates held.
- [prompting-agents](concepts/prompting-agents/CONCEPT.md) — reference library of eval-tested instruction blocks (scope discipline, autonomy, ambiguity, plan/promise discipline, final-message style, metaprompting) for authoring concepts and agent configs. Not deployed (consumed in-place). Tested: 2026-06-12, accuracy check at authoring.

## Ideas

- [karpathy-llm-wiki.md](ideas/karpathy-llm-wiki.md) — Karpathy's LLM Wiki gist. Ingested → teach (2026-06-12).
- [pocock-teach-skill-original.md](ideas/pocock-teach-skill-original.md) — Matt Pocock's original teach skill. Ingested → teach (2026-06-12).
- [openai-gpt-5-2-prompting-guide.md](ideas/openai-gpt-5-2-prompting-guide.md) — OpenAI's latest flagship prompting guide: verbosity/output-shape control, scope-drift prevention, ambiguity & hallucination handling, compaction, agentic steerability, tool parallelism. Ingested → prompting-agents (2026-06-12).
- [openai-codex-prompting-guide.md](ideas/openai-codex-prompting-guide.md) — how OpenAI prompts their own coding agent: autonomy/persistence, editing constraints, plan tool, final-message style, AGENTS.md usage, compaction. Ingested → prompting-agents + bootstrap.md Codex quirks (2026-06-12).
- [obra-superpowers/](ideas/obra-superpowers/SOURCE.md) — snapshot of Jesse Vincent's 14 superpowers skills (commit 6fd4507, MIT): TDD, systematic-debugging (with its own pressure tests + creation log), brainstorming, writing-plans/executing-plans, subagent-driven-development, code review pair, verification-before-completion, writing-skills + Anthropic best practices. Filed 2026-06-12, not yet ingested (the test-gate pattern in AGENTS.md already derives from writing-skills).
