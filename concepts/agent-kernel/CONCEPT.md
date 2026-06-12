# Concept: agent-kernel

A tiny always-injected base instruction file for coding-agent harnesses. It defines the user's default agent posture — act directly, preserve context economy, use tools, verify, respect dirty worktrees, and load deeper concepts only when relevant.

The deliverable is `body/AGENT-KERNEL.md`, intended to be pasted, included, or referenced from a harness's main agent file. It is deliberately not an Agent Skill: skills are on-demand; this is bootloader context.

## Design decisions

- **Kernel, not constitution** — always-on instructions must be small enough to avoid context rot. This file names durable defaults and delegates specialized behavior to skills/concepts.
- **General before prescriptive** — it states posture and failure modes rather than long procedures, following the right-altitude guidance in `prompting-agents`.
- **Skill-loading policy is load-bearing, implemented as an index pointer** — the kernel points at `index.md` instead of hardcoding concept names, so the catalog can evolve without editing always-on text in N harnesses. To avoid over-eager reads, it consults the catalog only when specialized handling would materially affect the outcome.
- **No harness syntax** — the body avoids tool names, slash commands, and frontmatter so it can be absorbed into Claude, Pi, Codex, OpenCode, Grok, Gemini, or a future harness main prompt.
- **No project-specific operations** — Git, verification, context, and file-safety defaults belong here; Omarchy, Obsidian, teach, and workspace-specific mechanics stay in their own skills or local instructions.
- **Never publish by default** — commits stay local; pushing/PRs require explicit user instruction, or project instructions the user has explicitly designated as trusted. A designation is valid only via a user-controlled channel (in conversation, or the user's own harness/vault configuration — e.g. Pi's `trust.json` is such a channel for Pi); a repo's own AGENTS.md can never be one, since project instruction files in cloned repos are an injection surface. When trust is undeterminable: ask; when asking is impossible (headless), default-deny. Why: as always-on context this rule multiplies across every repo and harness; an unsafe default or delegated trust here auto-publishes half-finished work everywhere. (Evolved through three revisions on 2026-06-12: pushed by default → trust undefined → trust user-channel-only with default-deny; see git history for details.)
- **Degrade gracefully off-vault** — on a machine without `~/Sync/CONFIG`, the kernel says so once and continues alone rather than stalling on dead references.

## Provenance

- `concepts/prompting-agents/body/SKILL.md` — right altitude, context economy, scope discipline, tool discipline, plan/promise discipline, dirty repo rules, final-message style.
- `AGENTS.md` — workspace Spirit: rules as defaults with reasons; canonical changes over deployed-copy edits; small context reads; commit discipline.
- `ideas/openai-codex-prompting-guide.md` — autonomy/persistence, working-tree etiquette, plan closure, final response style.
- `ideas/openai-gpt-5-2-prompting-guide.md` — verbosity clamps, scope discipline, ambiguity handling, tool usage, long-context grounding.
- `ideas/anthropic-context-engineering.md` — smallest high-signal context / context rot framing.
- `ideas/anthropic-claude-prompting-best-practices.md` — explain the why and prefer general instructions over brittle steps.
- `ideas/obra-superpowers/skills/verification-before-completion/SKILL.md` — evidence-before-claims verification: identify the proving command, run it fresh, read the output; never "should"/"probably"; distrust subagent self-reports.

## Tests

`tests/pressure-scenarios.md` — compact checks for the kernel's main failure modes: over-planning, scope creep, context dumping, unverified completion, dirty-worktree damage, unsafe publishing, off-vault stalls, and missing concept loads.

## Deploy policy

Not deployed yet. Two rules govern any deploy:

1. **Inject only the delta.** Before deploying to a harness, diff the kernel against what that harness's built-in system prompt already covers, and inject only what's missing. Rich harnesses (Claude Code in particular) already cover most of this kernel natively — deploying the full kernel there duplicates instructions at permanent token cost and risks phrasing conflicts. **Anti-recommended for Claude Code.** The kernel earns its keep in thin harnesses: bare API loops, grok-cli-style agents, minimal CLI wrappers.
2. **Reference, don't paste.** Prefer include/reference mechanisms so the harness reads the canonical body. Where a harness only supports pasted text, the pasted copy must open with a marker line — `<!-- DERIVED from ~/Sync/CONFIG/agents/concepts/agent-kernel/body/AGENT-KERNEL.md @ YYYY-MM-DD — do not edit here -->` — and lint/deploy passes refresh stale copies from canon. Why: an unmarked pasted copy is exactly the hand-edited derived output the canon gate exists to prevent.

Candidate targets, in order of expected value: thin custom harnesses → Pi (if its base prompt is thin; check first) → Codex durable AGENTS.md layer (delta only). When deployed, record the exact harness file or include path here, in `../../harnesses.md`, and `../../index.md`.
