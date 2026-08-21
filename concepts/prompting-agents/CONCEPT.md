---
test_kind: accuracy
test_status: pass
tested: 2026-08-21
deployed: yes
---
# Concept: prompting-agents

A reference library of proven instruction blocks for authoring agent instructions — concept bodies, AGENTS.md files, system prompts, per-agent configs. Exists so workspace authors adapt eval-tested phrasings instead of inventing instruction language from scratch.

## Design decisions

- **Reference type, not discipline type** — it constrains how concepts are *written*, not how an agent behaves at runtime, so the test gate's pressure-scenario requirement doesn't apply. Its test is accuracy: blocks must stay faithful to their sources (see tests/).
- **Agent-agnostic rewrites, not verbatim copies** — OpenAI's blocks reference their tool names (`multi_tool_use.parallel`, `apply_patch`); blocks here are rewritten to the underlying behavior so they apply to any agent. Harness-specific plumbing (apply_patch grammars, `phase` fields, compaction API) deliberately excluded — that's API integration, not prompting.
- **Origin-tagged adaptation** — when a block is copied into a concept or agent config, note where it came from so source updates can propagate.
- **Metaprompting included as a maintenance loop** — the technique composes with this workspace's implement/test operations and backs the Tune operation in `AGENTS.md`.
- **Metaprompting expanded beyond self-critique (2026-08-17), on local evidence.** The Codex source (and this concept's original block) described one instrument: ask the underperforming agent to propose generalized fixes, adopt what recurs. A `minimal-solution-ladder` pressure run showed the gap — the agent named a required `ceiling:` marker in its chat response while leaving the code unmarked, so by its own account it had complied and self-critique would not have reached it; only grading the committed diff did. The section now carries both instruments, the **locus** generalization (grade the artifact the next reader will meet — the agent's response is not that artifact, and a report-shaped rule launders a mark-the-code rule), mechanism-before-rewrite, and replace-over-append. Independent Grok review of that expansion cut three overclaims, one of which ("recurrence is evidence only across independent runs") would have disqualified the very evidence that motivated it — a repeated failure of the same check is evidence; a repeated *suggestion* inside one session is an echo. Beyond the Codex source: local, and marked as such.
- **Skill suites should preserve user control** — prefer small composable skills with clear invocation boundaries over monolithic process frameworks; separate orchestrators from reusable disciplines so failures are easier to debug and adapt.
- **Agent-ready work is shaped before execution** — ambiguous requirements should be grilled into durable planning context, then sliced into independently testable vertical tracer bullets with fast feedback loops and documented project runways.

## Provenance

- [openai-gpt-5-2-prompting-guide.md](https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide) — verbosity clamps, scope discipline, long-context re-grounding, ambiguity/hallucination handling, user-update specs, tool-usage rules, research-agent appendix. https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide
- [openai-codex-prompting-guide.md](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide) — autonomy/persistence, loop-breaker, plan closure and promise discipline, final-message style, dirty-worktree etiquette, frontend anti-slop, custom-tool naming guidance, metaprompting. https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide
- [anthropic-context-engineering.md](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — right-altitude principle, context economy / context rot, just-in-time context. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- [anthropic-claude-prompting-best-practices.md](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) — explain-the-why ("smart enough to generalize from the explanation"), prefer general instructions over prescriptive steps, examples over rules, self-check. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Lee Boonstra, *Prompt Engineering* whitepaper v7 (Google) — source URL unrecorded — technique repertoire (few-shot, chain-of-thought, step-back, self-consistency, ReAct). https://www.kaggle.com/whitepaper-prompt-engineering
- [skillsskillsproductivityteach at main.md](https://github.com/mattpocock/skills/tree/main) — Matt Pocock's broader skills README/catalog: small composable skills, user-invoked vs model-invoked boundary, grilling/shared-language/documented-decision patterns, feedback-loop skills. https://github.com/mattpocock/skills/tree/main
- [AI Engineer Workshop 2026.md](https://www.aihero.dev/ai-engineer-workshop-2026~dwnll) — workflow framing for AI-assisted feature delivery: grill vague requirements, write PRDs, break work into vertical tracer-bullet issues, execute with TDD human-in-the-loop or AFK, design codebases for agent effectiveness. https://www.aihero.dev/ai-engineer-workshop-2026~dwnll
- [mattpocockai-engineer-workshop-2026-project.md](https://github.com/mattpocock/ai-engineer-workshop-2026-project/tree/main) — companion project README showing the concrete project runway an agent needs: prerequisites, setup, dev server, test/typecheck/build commands, migration/seed commands, and stack. https://github.com/mattpocock/ai-engineer-workshop-2026-project/tree/main
- [obra/superpowers `skills/writing-skills/`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/writing-skills/) — skill authoring/testing methodology, description-field discovery warnings, rationalization-resistant discipline phrasing, and pressure-testing technique; aligns with this workspace's Test gate.
- [obra/superpowers `skills/using-superpowers/`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/using-superpowers/) — considered for skill-loading policy; its mandatory “invoke before any response” rule is deliberately not adopted because this workspace uses context-economical, relevance-gated concept loading.
- [anthropic-claude-code-best-practices.md](https://code.claude.com/docs/en/best-practices) — standing-instruction-file hygiene (pruning test, include/exclude, prune-don't-emphasize diagnostics) and the verification-ladder + evidence-over-assertion lines in work shaping; harness-specific session/UI advice deliberately excluded. https://code.claude.com/docs/en/best-practices (ingested 2026-07-12)

## Philosophy

Per the workspace Spirit (AGENTS.md): this library guides rather than constrains. The "choose the altitude" section is load-bearing — constraining blocks are tools for specific, costly failure modes, not a default posture, and every hard rule carries its why so a more capable future agent can generalize or supersede it correctly.

## Tests

`tests/accuracy-check.md` — verify each block traces to the live URL in Provenance (not a local clipping) and hasn't drifted in meaning during agent-agnostic rewriting. Unfetchable URLs are BLOCKED, not FAIL. Local-only expansions (2026-08-17 metaprompting) are checked against this file. Live-URL run 2026-08-21 **PASS** (Boonstra/Kaggle technique repertoire BLOCKED).

## Deploy targets

Consumed in-place by agents working in this workspace (the Implement operation in AGENTS.md points here), and also deployed as a skill by `scripts/deploy-local-skills.py` along with every other `body/SKILL.md`. Manual harnesses can read `body/SKILL.md` via `../../docs/bootstrap.md`.
