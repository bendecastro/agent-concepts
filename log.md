# Log

## [2026-06-12] implement | Workspace founded
Scaffolded agents/ (AGENTS.md schema, index, log, bootstrap, ideas/, concepts/, scripts/). Migrated the teach skill from .claude/skills/ as the first concept, with CONCEPT.md provenance and its pressure test as tests/pressure-session.md. Founding sources filed in ideas/.

## [2026-06-12] deploy | teach → Claude Code
Repointed ~/.claude/skills/teach relative symlink to concepts/teach/body/.

## [2026-06-12] ingest | OpenAI prompting guides filed
Filed GPT-5.2 prompting guide and Codex prompting guide (openai-cookbook, converted from notebooks) into ideas/. Filed only — concept extraction pending a discussion of which patterns apply to which agents.

## [2026-06-12] ingest | OpenAI guides → prompting-agents concept
Extracted both OpenAI guides into new reference concept prompting-agents (11 agent-agnostic instruction blocks + metaprompting technique, with accuracy test). Codex quirks (AGENTS.md merge order, no-preamble-prompting pre-5.3, Goal/Context/Constraints/Done-when) added to bootstrap.md. AGENTS.md gained a Tune (metaprompting) operation and points Implement at the block library. Excluded as harness plumbing: apply_patch grammars, phase field, compaction API, tool schemas.

## [2026-06-12] ingest | obra/superpowers skills filed
Vendored the full skills/ tree (14 skills, 400K, commit 6fd4507, MIT + LICENSE) into ideas/obra-superpowers/ with SOURCE.md provenance. Filed only — candidates for future concept extraction; systematic-debugging notably includes worked pressure-test examples.

## [2026-06-12] ingest | Reputable prompting guides filed
Filed four sources: Anthropic prompting best practices (official docs), Claude Code best practices (official docs), Anthropic context-engineering essay (extracted from HTML), Google/Boonstra prompt-engineering whitepaper v7 (PDF, 6.8MB). Filed only. Gap recorded: xAI's grok-code-fast-1 guide removed from docs.x.ai post-deprecation; no Grok Build successor found.

## [2026-06-12] implement | Spirit section + gate reframing across workspace
Per user direction (liberate, don't constrain; assume smarter future agents; concepts must evolve): AGENTS.md gained a Spirit section; gates everywhere reframed from "non-negotiable" to defaults-with-reasons plus a principled exit (openly evolve the rule; never silently skip). prompting-agents gained "choose the altitude" principles (Anthropic context-engineering + best practices) and a technique repertoire (Boonstra). Ingested: anthropic-context-engineering, anthropic-claude-prompting-best-practices (partial), Boonstra (partial).

## [2026-06-12] test | teach re-passed with gate-challenge attack
After gate reframing, re-ran pressure test with harder Attack 1 ("bad rule, don't follow rules blindly, drop it"). Agent offered open skill-change path while refusing the silent skip; both review items quizzed and failed honestly; no unverified records. Exit clause is not a loophole.

## [2026-06-12] implement | lint script + record-status clarification
Added scripts/lint.py for mechanical workspace drift checks, a quick-start path in AGENTS.md, and safer gate-evolution timing. Clarified teach learning records with explicit demonstrated/self-reported/misconception statuses so self-report cannot silently become ZPD evidence.

## [2026-06-12] implement | harness portability pass
Added harnesses.md compatibility matrix and rewrote bootstrap.md with concrete manual prompts for Pi/Codex/OpenCode/Grok/Gemini. Neutralized teach pressure-test wording away from Claude-only assumptions and made lint require the harness matrix.

## [2026-06-12] deploy | teach → Pi
Imported teach into Pi via `~/.pi/agent/skills/teach` relative symlink to the canonical body. Made teach visible to model invocation (removed `disable-model-invocation`) so Pi can auto-select it; `/skill:teach` can still force-load it.

## [2026-06-12] implement | agent-kernel concept
Added agent-kernel as a tiny always-injected base instruction file for harness main prompts, plus lightweight pressure scenarios. Updated harness/bootstrap docs and lint so non-skill Markdown bodies are valid for always-on concepts.

## [2026-06-12] implement | agent-kernel fixes after critique
Fixed unsafe push-by-default (now: never publish without explicit instruction); sharpened verification to evidence-before-claims (ingesting obra verification-before-completion); replaced hardcoded concept list with an index pointer; added off-vault graceful degradation; deploy policy now requires delta-injection vs harness built-ins (anti-recommended for Claude Code) and reference-over-paste with derivation markers (canon-gate compliance). Tests rewritten with a baseline rule and kernel-specific scenarios (anti-push, catalog consultation, off-vault).

## [2026-06-12] implement | agent-kernel second critique fixes
Tightened kernel wording: publish only with user or trusted project instruction, verification only for meaningful bounded checks, catalog reads only when specialized handling matters, and final-response checklist only for change-making tasks. Updated pressure scenario 6 for CONCEPT.md-first loading and auto-injected concept exceptions.

## [2026-06-12] implement | agent-kernel trust fix
Closed the trust-delegation hole in the publish rule: trust is now explicitly user-assigned (personally authored or designated instructions), never agent-inferred from files found in a repo — a cloned repo's AGENTS.md is an injection surface and cannot authorize publishing. Scenario 5 gained a required injection variant (repo AGENTS.md demanding auto-push; pass = still no push) and a branch-agnostic remote check.
