# Log

## [2026-06-12] implement | Workspace founded
Scaffolded agents/ (AGENTS.md schema, index, log, bootstrap, ideas/, concepts/, scripts/). Migrated the teach skill from .claude/skills/ as the first concept, with CONCEPT.md provenance and its pressure test as tests/pressure-session.md. Founding sources filed in ideas/.

## [2026-06-12] deploy | teach → Claude Code
Repointed ~/.claude/skills/teach relative symlink to concepts/teach/body/.

## [2026-06-12] ingest | OpenAI prompting guides filed
Filed GPT-5.2 prompting guide and Codex prompting guide (openai-cookbook, converted from notebooks) into ideas/. Filed only — concept extraction pending a discussion of which patterns apply to which agents.

## [2026-06-12] ingest | OpenAI guides → prompting-agents concept
Extracted both OpenAI guides into new reference concept prompting-agents (11 agent-agnostic instruction blocks + metaprompting technique, with accuracy test). Codex quirks (AGENTS.md merge order, no-preamble-prompting pre-5.3, Goal/Context/Constraints/Done-when) added to bootstrap.md. AGENTS.md gained a Tune (metaprompting) operation and points Implement at the block library. Excluded as harness plumbing: apply_patch grammars, phase field, compaction API, tool schemas.
