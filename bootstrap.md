# Bootstrap lines per agent

Claude Code discovers deployed concepts automatically via `~/.claude/skills/` symlinks. Every other agent gets pointed here manually — paste the relevant line:

- **Generic (any agent):**
  `Read ~/Sync/CONFIG/agents/AGENTS.md and follow it. Then: <operation>, e.g. "ingest ideas/foo.md" or "lint the workspace".`
- **Codex / OpenCode / Pi / Grok session using a specific concept:**
  `Read ~/Sync/CONFIG/agents/concepts/<name>/body/SKILL.md and follow it as your instructions for this session.`

Notes:
- OpenCode supports the Agent Skills spec; a `body/` dir can be symlinked into its skills location when that's wanted — record the deploy in the concept's CONCEPT.md.
- Add per-agent quirks here as they're discovered (frontmatter fields ignored, script execution limits, etc.).
