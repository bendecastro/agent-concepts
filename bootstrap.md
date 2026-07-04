# Bootstrap lines per agent

Use this file when a harness does not automatically discover a concept from `concepts/<name>/body/`. See [harnesses.md](harnesses.md) for the compatibility matrix and deploy status.

## Generic prompts

- **Always-on base include:**
  `Include ~/Sync/CONFIG/agents/concepts/agent-kernel/body/AGENT-KERNEL.md in the harness's main agent instructions.`
- **Workspace maintenance (any agent):**
  `Read ~/Sync/CONFIG/agents/AGENTS.md and follow it. Then: <operation>, e.g. "ingest raw/foo.md", "lint the workspace", or "implement the teach concept update".`
- **Concept session (manual harness):**
  `Read ~/Sync/CONFIG/agents/concepts/<name>/body/SKILL.md fully. Ignore any YAML frontmatter if your harness does not support Agent Skills metadata. Follow the Markdown body as your instructions for this session.`
- **Concept test (manual harness):**
  `Act as the consuming agent for ~/Sync/CONFIG/agents/concepts/<name>/body/SKILL.md in a throwaway workspace. Run the scenario in ~/Sync/CONFIG/agents/concepts/<name>/tests/<test>. Produce artifacts, then grade by file inspection, not self-report.`

## Harness-specific entry points

### Claude Code

Claude Code discovers deployed concepts automatically via relative symlinks:

`~/.claude/skills/<name>` → `../../Sync/CONFIG/agents/concepts/<name>/body`

Current deploys are recorded in each concept's `CONCEPT.md` and summarized in `index.md` / `harnesses.md`.

### Pi

Pi discovers global skills from `~/.pi/agent/skills/`. `teach` is deployed there as a relative symlink to the canonical body, so future sessions can auto-load it when the user asks to learn something; use `/skill:teach` to force it.

For concepts not yet deployed to Pi, use the generic concept-session bootstrap:

`Read ~/Sync/CONFIG/agents/concepts/<name>/body/SKILL.md fully. Ignore any YAML frontmatter if unsupported. Follow the Markdown body as your instructions for this session.`

For workspace maintenance:

`Read ~/Sync/CONFIG/agents/AGENTS.md and follow it. Then: <operation>.`

### Codex

Codex has the `agent-kernel` delta in `~/.codex/AGENTS.md`, its documented global instruction layer. Prefer durable repo-level `AGENTS.md` references for specialized concepts when working inside a repo; manual bootstrap also works.

Example task frame:

```text
Goal: Use the <name> concept for this session.
Context: The canonical instructions are at ~/Sync/CONFIG/agents/concepts/<name>/body/SKILL.md.
Constraints: Read that file fully; ignore YAML frontmatter if unsupported; follow the Markdown body; do not copy or edit deployed outputs.
Done when: The requested session/task is complete and any canonical changes are made in ~/Sync/CONFIG/agents/.
```

### OpenCode

OpenCode has the `agent-kernel` delta in `~/.config/opencode/AGENTS.md`. If native Agent Skills support is configured for a specialized concept, expose `concepts/<name>/body/` through OpenCode's skills directory and record the exact path in `harnesses.md` and the concept `CONCEPT.md`. Until then, use the generic concept-session bootstrap for specialized concepts.

### Composer (Cursor)

Composer discovers deployed concepts automatically from the shared bus:

`~/.agents/skills/<name>` → `../../Sync/CONFIG/agents/concepts/<name>/body`

Populate that bus with `python3 scripts/deploy-local-skills.py` from this workspace (same command as Pi). Restart Composer sessions after deploy if the skill list is stale. For concepts not yet deployed, use the generic concept-session bootstrap.

### Grok

Grok discovers the same `~/.agents/skills/<name>` symlinks (verified 2026-07-04 via `grok inspect`). Run `python3 scripts/deploy-local-skills.py` to refresh them. Avoid placing same-named skills in `~/.grok/skills/` — that directory outranks the shared bus and will shadow canonical concepts (e.g. the bundled `code-review` maintainability skill vs the obra concept).

For stale sessions or one-off use, the generic concept-session bootstrap still works:

`Read ~/Sync/CONFIG/agents/concepts/<name>/body/SKILL.md fully. Ignore any YAML frontmatter if unsupported. Follow the Markdown body as your instructions for this session.`

### Gemini / other agents

Use the generic concept-session bootstrap. After first real use, update `harnesses.md` with what worked, what frontmatter was ignored, and any script/tool limitations.

## Per-agent quirks

**Codex** (from OpenAI's Codex prompting guide and current docs, see `raw/openai-codex-prompting-guide.md`):
- AGENTS.md discovery: concatenates `~/.codex/AGENTS.md` plus every AGENTS.md from repo root down to CWD; later (deeper) files override earlier ones. So a concept can be deployed to Codex by referencing it from an AGENTS.md at the right directory level — no skills directory needed.
- The model is specifically trained to adhere to AGENTS.md content — durable rules belong there, not in the task prompt.
- Do NOT add instructions asking pre-5.3 Codex models for upfront plans, preambles, or mid-task status updates — this causes it to stop before the task is complete. (gpt-5.3-codex and later handle promptable updates fine.)
- Task prompts: OpenAI's recommended frame is Goal / Context / Constraints / Done-when.
