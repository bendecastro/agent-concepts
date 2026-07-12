# Concept: prompting-agents

A reference library of proven instruction blocks for authoring agent instructions — concept bodies, AGENTS.md files, system prompts, per-agent configs. Exists so workspace authors adapt eval-tested phrasings instead of inventing instruction language from scratch.

## Design decisions

- **Reference type, not discipline type** — it constrains how concepts are *written*, not how an agent behaves at runtime, so the test gate's pressure-scenario requirement doesn't apply. Its test is accuracy: blocks must stay faithful to their sources (see tests/).
- **Agent-agnostic rewrites, not verbatim copies** — OpenAI's blocks reference their tool names (`multi_tool_use.parallel`, `apply_patch`); blocks here are rewritten to the underlying behavior so they apply to any agent. Harness-specific plumbing (apply_patch grammars, `phase` fields, compaction API) deliberately excluded — that's API integration, not prompting.
- **Origin-tagged adaptation** — when a block is copied into a concept or agent config, note where it came from so source updates can propagate.
- **Metaprompting included as a maintenance loop** — the technique (have the underperforming agent propose generalized fixes to its own instructions, adopt only recurring suggestions, test before deploy) composes with this workspace's implement/test operations.
- **Skill suites should preserve user control** — prefer small composable skills with clear invocation boundaries over monolithic process frameworks; separate orchestrators from reusable disciplines so failures are easier to debug and adapt.
- **Agent-ready work is shaped before execution** — ambiguous requirements should be grilled into durable planning context, then sliced into independently testable vertical tracer bullets with fast feedback loops and documented project runways.

## Provenance

- `raw/ingested/openai-gpt-5-2-prompting-guide.md` — verbosity clamps, scope discipline, long-context re-grounding, ambiguity/hallucination handling, user-update specs, tool-usage rules, research-agent appendix. https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide
- `raw/ingested/openai-codex-prompting-guide.md` — autonomy/persistence, loop-breaker, plan closure and promise discipline, final-message style, dirty-worktree etiquette, frontend anti-slop, custom-tool naming guidance, metaprompting. https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide
- `raw/ingested/anthropic-context-engineering.md` — right-altitude principle, context economy / context rot, just-in-time context. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- `raw/ingested/anthropic-claude-prompting-best-practices.md` — explain-the-why ("smart enough to generalize from the explanation"), prefer general instructions over prescriptive steps, examples over rules, self-check. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- `raw/ingested/google-boonstra-prompt-engineering-v7.pdf` — technique repertoire (few-shot, chain-of-thought, step-back, self-consistency, ReAct). https://www.kaggle.com/whitepaper-prompt-engineering
- `raw/ingested/skillsskillsproductivityteach at main.md` — Matt Pocock's broader skills README/catalog: small composable skills, user-invoked vs model-invoked boundary, grilling/shared-language/documented-decision patterns, feedback-loop skills. https://github.com/mattpocock/skills/tree/main
- `raw/ingested/AI Engineer Workshop 2026.md` — workflow framing for AI-assisted feature delivery: grill vague requirements, write PRDs, break work into vertical tracer-bullet issues, execute with TDD human-in-the-loop or AFK, design codebases for agent effectiveness. https://www.aihero.dev/ai-engineer-workshop-2026~dwnll
- `raw/ingested/mattpocockai-engineer-workshop-2026-project.md` — companion project README showing the concrete project runway an agent needs: prerequisites, setup, dev server, test/typecheck/build commands, migration/seed commands, and stack. https://github.com/mattpocock/ai-engineer-workshop-2026-project/tree/main
- `raw/ingested/obra-superpowers/skills/writing-skills/` — skill authoring/testing methodology, description-field discovery warnings, rationalization-resistant discipline phrasing, and pressure-testing technique; aligns with this workspace's Test gate.
- `raw/ingested/obra-superpowers/skills/using-superpowers/` — considered for skill-loading policy; its mandatory “invoke before any response” rule is deliberately not adopted because this workspace uses context-economical, relevance-gated concept loading.
- `raw/ingested/anthropic-claude-code-best-practices.md` — standing-instruction-file hygiene (pruning test, include/exclude, prune-don't-emphasize diagnostics) and the verification-ladder + evidence-over-assertion lines in work shaping; harness-specific session/UI advice deliberately excluded. https://code.claude.com/docs/en/best-practices (ingested 2026-07-12)

## Philosophy

Per the workspace Spirit (AGENTS.md): this library guides rather than constrains. The "choose the altitude" section is load-bearing — constraining blocks are tools for specific, costly failure modes, not a default posture, and every hard rule carries its why so a more capable future agent can generalize or supersede it correctly.

## Tests

`tests/accuracy-check.md` — verify each block traces to its source and hasn't drifted in meaning during agent-agnostic rewriting.

## Deploy targets

None — consumed in-place by agents working in this workspace (the Implement operation in AGENTS.md points here). Not symlinked into any agent's skills directory; manual harnesses can read `body/SKILL.md` via `../../bootstrap.md`.
