# Bootstrap lines per agent

Claude Code discovers deployed concepts automatically via `~/.claude/skills/` symlinks. Every other agent gets pointed here manually — paste the relevant line:

- **Generic (any agent):**
  `Read ~/Sync/CONFIG/agents/AGENTS.md and follow it. Then: <operation>, e.g. "ingest ideas/foo.md" or "lint the workspace".`
- **Codex / OpenCode / Pi / Grok session using a specific concept:**
  `Read ~/Sync/CONFIG/agents/concepts/<name>/body/SKILL.md and follow it as your instructions for this session.`

Notes:
- OpenCode supports the Agent Skills spec; a `body/` dir can be symlinked into its skills location when that's wanted — record the deploy in the concept's CONCEPT.md.
- Add per-agent quirks here as they're discovered (frontmatter fields ignored, script execution limits, etc.).

## Per-agent quirks

**Codex** (from OpenAI's Codex prompting guide, see `ideas/openai-codex-prompting-guide.md`):
- AGENTS.md discovery: concatenates `~/.codex` plus every AGENTS.md from repo root down to CWD; later (deeper) files override earlier ones. So a concept can be deployed to Codex by referencing it from an AGENTS.md at the right directory level — no skills directory needed.
- The model is specifically trained to adhere to AGENTS.md content — durable rules belong there, not in the task prompt.
- Do NOT add instructions asking pre-5.3 Codex models for upfront plans, preambles, or mid-task status updates — this causes it to stop before the task is complete. (gpt-5.3-codex and later handle promptable updates fine.)
- Task prompts: OpenAI's recommended frame is Goal / Context / Constraints / Done-when.
