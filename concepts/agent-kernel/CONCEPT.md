# Concept: agent-kernel

A tiny always-injected base instruction file for coding-agent harnesses. It defines the user's default agent posture — act directly, preserve context economy, use tools, verify, respect dirty worktrees, and load deeper concepts only when relevant.

The deliverable is `body/AGENT-KERNEL.md`, intended to be pasted, included, or referenced from a harness's main agent file. It is deliberately not an Agent Skill: skills are on-demand; this is bootloader context.

## Design decisions

- **Kernel, not constitution** — always-on instructions must be small enough to avoid context rot. This file names durable defaults and delegates specialized behavior to skills/concepts.
- **General before prescriptive** — it states posture and failure modes rather than long procedures, following the right-altitude guidance in `prompting-agents`.
- **Skill-loading policy is load-bearing** — the kernel's most important job is telling the harness when to load `teach`, `prompting-agents`, project `AGENTS.md`, or other local instructions instead of bloating the base prompt.
- **No harness syntax** — the body avoids tool names, slash commands, and frontmatter so it can be absorbed into Claude, Pi, Codex, OpenCode, Grok, Gemini, or a future harness main prompt.
- **No project-specific operations** — Git, verification, context, and file-safety defaults belong here; Omarchy, Obsidian, teach, and workspace-specific mechanics stay in their own skills or local instructions.

## Provenance

- `concepts/prompting-agents/body/SKILL.md` — right altitude, context economy, scope discipline, tool discipline, plan/promise discipline, dirty repo rules, final-message style.
- `AGENTS.md` — workspace Spirit: rules as defaults with reasons; canonical changes over deployed-copy edits; small context reads; commit discipline.
- `ideas/openai-codex-prompting-guide.md` — autonomy/persistence, working-tree etiquette, plan closure, final response style.
- `ideas/openai-gpt-5-2-prompting-guide.md` — verbosity clamps, scope discipline, ambiguity handling, tool usage, long-context grounding.
- `ideas/anthropic-context-engineering.md` — smallest high-signal context / context rot framing.
- `ideas/anthropic-claude-prompting-best-practices.md` — explain the why and prefer general instructions over brittle steps.

## Tests

`tests/pressure-scenarios.md` — compact checks for the kernel's main failure modes: over-planning, scope creep, context dumping, unverified completion, dirty-worktree damage, and missing concept loads.

## Deploy targets

Not deployed yet. Candidate uses:

- Pi: append or include `body/AGENT-KERNEL.md` in the main agent prompt/settings once a safe include mechanism is chosen.
- Codex: reference or paste into an appropriate durable `AGENTS.md` layer.
- Claude Code/OpenCode/Grok/Gemini: absorb into the harness's main agent instruction file if the harness supports durable base prompts.

When deployed, record the exact harness file or include path in this section, `../../harnesses.md`, and `../../index.md`.
