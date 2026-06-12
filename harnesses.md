# Harness compatibility

This workspace is canonical at `concepts/<name>/body/`. Harness-specific deployment should expose that canonical body without copying it. When a harness cannot consume an Agent Skills directory directly, point the session at the body file with an explicit bootstrap prompt.

For always-on base instructions, use `concepts/agent-kernel/body/AGENT-KERNEL.md`; it is deliberately a small Markdown include, not an on-demand skill.

## Compatibility matrix

| Harness | Current status | Discovery/deploy method | Frontmatter handling | Notes |
|---|---|---|---|---|
| Claude Code | Deployed for `teach`, `seo` | Relative symlink: `~/.claude/skills/<name>` → `../../Sync/CONFIG/agents/concepts/<name>/body` | Native Agent Skills metadata | Best-supported path today; keep symlink targets relative and inside `concepts/`. |
| Pi | Deployed for `teach` | Relative symlink: `~/.pi/agent/skills/<name>` → `../../../agents/concepts/<name>/body` from the synced CONFIG vault | Native Agent Skills metadata; unknown frontmatter ignored | Future Pi sessions discover `teach`; use `/skill:teach` to force-load if auto-selection misses. |
| Codex | AGENTS.md reference or manual bootstrap | Prefer an `AGENTS.md` at the right repo level that points to this workspace/concept; manual bootstrap also works | Treat frontmatter as plain metadata unless the harness adds skill support | Codex merges `~/.codex` and repo `AGENTS.md` files from root to CWD; deeper files override earlier ones. |
| OpenCode | Candidate native skill deploy | If/when enabled, symlink the `body/` directory into OpenCode's skills location; otherwise manual bootstrap | Verify Agent Skills frontmatter behavior per install | Record the exact path/behavior here after first real deploy. |
| Grok | Manual bootstrap only | Paste/read `SKILL.md` for the session | Treat frontmatter as metadata | No official durable skill-discovery path recorded yet. |
| Gemini | Unknown/manual | Use generic bootstrap until tested | Treat frontmatter as metadata | Add quirks after first use. |

## Portability rules

- **Canon stays harness-neutral.** Edit `concepts/<name>/body/`, not a deployed copy or generated harness variant.
- **Frontmatter is optional metadata.** Agent Skills-aware harnesses may use it; other harnesses should ignore the YAML block and follow the Markdown body.
- **Bootstrap beats copying.** If a harness lacks native skills, use a paste/read instruction that points at the canonical file instead of duplicating the concept.
- **Kernel stays tiny.** Always-injected base context should come from `agent-kernel`; keep specialized workflows as on-demand skills/concepts.
- **Record every real deploy.** When a concept is made discoverable without manual paste, update this file, the concept's `CONCEPT.md`, and `index.md`.
- **Publishing needs publish authorization.** Harness/project trust only permits loading instructions; push/PR/release actions require current user instruction or a matching rule in `policies/publish.yaml`.
- **Test by consuming harness.** Pressure-test discipline concepts in at least one harness before marking deployed there; record which harness ran the test.

## Bootstrap prompt patterns

Use `~` rather than hardcoded home paths; this directory syncs across machines.

- Base prompt include:
  `Include ~/Sync/CONFIG/agents/concepts/agent-kernel/body/AGENT-KERNEL.md in the harness's main agent instructions.`
- Workspace maintenance:
  `Read ~/Sync/CONFIG/agents/AGENTS.md and follow it. Then: <operation>.`
- Concept session, any manual harness:
  `Read ~/Sync/CONFIG/agents/concepts/<name>/body/SKILL.md fully. Ignore any YAML frontmatter if your harness does not support Agent Skills metadata. Follow the Markdown body as your instructions for this session.`
- Discipline concept test:
  `Act as the consuming agent for ~/Sync/CONFIG/agents/concepts/<name>/body/SKILL.md in a throwaway workspace. Run the scenario in tests/<test>. Produce artifacts, then grade by file inspection, not self-report.`

## Unknowns to resolve

- Exact OpenCode skills directory and whether symlinked support files/scripts are preserved.
- Whether additional concepts should be deployed into Pi's global skills directory or stay manual-bootstrap.
- Any Grok/Gemini durable instruction-discovery mechanism worth supporting.
