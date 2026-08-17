# Harness compatibility

This workspace is canonical at `concepts/<name>/body/`. Harness-specific deployment should expose that canonical body without copying it. When a harness cannot consume an Agent Skills directory directly, point the session at the body file with an explicit bootstrap prompt.

For always-on base instructions, use `concepts/agent-kernel/body/AGENT-KERNEL.md`; it is deliberately a small Markdown include, not an on-demand skill.

## Compatibility matrix

| Harness | Current status | Discovery/deploy method | Frontmatter handling | Notes |
|---|---|---|---|---|
| Claude Code | `agent-kernel` answer-first posture delta refreshed 2026-08-12; deployed for `teach`, `seo`, the workshop pipeline (`grill-me`, `grilling`, `domain-modeling`, `to-spec`/`to-prd`, `to-tickets`/`to-issues`, `tdd`, `codebase-design`), the extracted disciplines `prd-drafting`/`issue-slicing`, the scaffolder `bc-init-agent`, bc loop skills (`bc-plan-to-issues`, `bc-drain-issues`, `bc-autoresearch-loop`), and workflow extensions (`triage`, `diagnosing-bugs`, `prototype`, `improve-codebase-architecture`). | Relative symlink: `~/.claude/skills/<name>` → `<relative path to>/concepts/<name>/body` | Native Agent Skills metadata | Best-supported path today; keep symlink targets relative and inside `concepts/`. Workshop pipeline deployed 2026-06-20: grill stack pressure-tested; `codebase-design` accuracy-checked; `to-spec`/`to-tickets` pressure-tested 2026-07-16 PASS (Grok); `tdd` re-pressure-tested 2026-07-16 PASS after skill fix. Loop refactor 2026-06-20: `prd-drafting`/`issue-slicing` extracted + symlinked; bc loop skills symlinked 2026-06-21 by user request; Pocock workflow extensions deployed 2026-06-21; `bc-plan-to-issues` re-pressure-tested 2026-07-16 **PASS** (Grok). |
| Pi | Kernel-derived global instructions in `~/.pi/agent/AGENTS.md` (tracked; answer-first posture refreshed 2026-08-12); bulk-deployed local concept skills with `scripts/deploy-local-skills.py` | Relative symlinks in both `~/.agents/skills/<name>` and `~/.pi/agent/skills/<name>` point to `<agent-concepts>/concepts/<name>/body` | Native Agent Skills metadata; unknown frontmatter ignored | Future Pi sessions discover these skills; if a current session's skill list is stale, read `concepts/<name>/body/SKILL.md` directly. |
| Composer (Cursor) | Bulk-deployed via the same `~/.agents/skills/` bus as Pi | Cursor scans `~/.agents/skills/<name>` (Agent Skills convention); no separate `~/.cursor/skills/` deploy needed on this machine | Native Agent Skills metadata | Verified 2026-07-04: Composer sessions advertise all 29 local concepts from `deploy-local-skills.py`. Restart sessions after deploy to refresh stale skill lists. |
| Codex | `agent-kernel` delta deployed; answer-first posture refreshed 2026-08-12; validated 2026-06-12 for smoke + scenario 5 repo-instruction no-push variant; specialized concepts via AGENTS.md reference or manual bootstrap | Kernel delta lives in `~/.codex/AGENTS.md` (→ synced `CONFIG/.codex/AGENTS.md` since 2026-07-12; sessions synced too), Codex's documented global instruction layer. For specialized concepts, prefer an `AGENTS.md` at the right repo level that points to this workspace/concept; manual bootstrap also works. | Global/repo `AGENTS.md`; treat frontmatter as plain metadata unless the harness adds skill support | Codex merges `~/.codex/AGENTS.md` plus repo `AGENTS.md` files from root to CWD; deeper files override earlier ones. Full baseline-vs-injected, off-vault, and policy-allow child runs remain pending. |
| OpenCode | `agent-kernel` delta deployed (answer-first posture refreshed 2026-08-12); local concept skills bulk-deployed via `~/.agents/skills/`; canonical skills are also slash-invocable | Kernel delta lives in `~/.config/opencode/AGENTS.md`; `scripts/deploy-local-skills.py` creates relative canonical-body symlinks on OpenCode's auto-loaded shared skills bus. The global `canonical-skill-commands.ts` plugin dynamically adds a same-named slash command for each CONFIG-backed bus entry, including compatibility aliases; explicit command files win but must load the canonical skill. | Global `AGENTS.md` plus native Agent Skills metadata; dynamic command wrappers call the `skill` tool | Verified 2026-07-17 via `opencode debug config`: all 32 canonical skills plus three aliases have slash commands; existing `/seo` retains its specialist-agent routing and now explicitly loads the canonical skill. Restart OpenCode after skill/plugin/config changes because discovery happens at startup. |
| Grok | `agent-kernel` delta deployed 2026-07-12 and answer-first posture refreshed 2026-08-12 (`~/.grok/AGENTS.md` → synced `CONFIG/.grok/AGENTS.md`; sessions + memory synced too; built-in-prompt diff pending); skills bulk-deployed via `~/.agents/skills/` (same bus as Pi/Composer) | Grok scans `.agents/skills/` at each tier alongside `.grok/skills/`; also compat-scans `~/.claude/skills/` and `~/.cursor/skills/` by default | Native Agent Skills metadata; unknown frontmatter ignored | Verified 2026-07-04 with `grok inspect` (46 skills incl. all local concepts). **Collision:** a separate `~/.grok/skills/code-review` (xAI maintainability audit) shadowed the canonical obra `code-review` concept — removed so the CONFIG symlink wins. **Grok updates resurrect it:** found restored and re-removed 2026-07-13; after any Grok upgrade, check `~/.grok/skills/` for bundled skills whose names collide with `~/.agents/skills/` concepts and remove them again. Avoid adding same-named skills under `~/.grok/skills/` when a concept already lives in `~/.agents/skills/`. Manual bootstrap still works for stale sessions. |
| Gemini | Unknown/manual | Use generic bootstrap until tested | Treat frontmatter as metadata | Add quirks after first use. |

The `herdr` reference skill was deployed 2026-07-22 to the shared bus plus Pi and Claude Code symlinks. Composer, OpenCode, and Grok consume the shared-bus copy; active sessions must restart to refresh discovery.

The Obsidian format reference concepts `obsidian-markdown`, `obsidian-bases`, and `json-canvas` were accuracy-checked, mutation-boundary pressure-tested, and deployed 2026-08-17 through `scripts/deploy-local-skills.py` to the shared bus plus Pi and Claude Code symlinks. Their bodies teach file formats and validation only; `obsidian-cli` and `defuddle` were deliberately not deployed, and `pi-obsidian-vault` remains the Markdown mutation authority.

## Portability rules

- **Canon stays harness-neutral.** Edit `concepts/<name>/body/`, not a deployed copy or generated harness variant.
- **Frontmatter is optional metadata.** Agent Skills-aware harnesses may use it; other harnesses should ignore the YAML block and follow the Markdown body.
- **Bootstrap beats copying.** If a harness lacks native skills, use a paste/read instruction that points at the canonical file instead of duplicating the concept.
- **Kernel stays tiny.** Always-injected base context should come from `agent-kernel`; keep specialized workflows as on-demand skills/concepts.
- **Record every real deploy.** When a concept is made discoverable without manual paste, update this file, the concept's `CONCEPT.md`, and `index.md`.
- **OpenCode commands stay thin.** Slash commands for CONFIG concepts only load the canonical Agent Skill; workflow instructions stay in `concepts/<name>/body/`. The global plugin generates wrappers dynamically and never replaces an explicit command.
- **Publishing needs publish authorization.** Harness/project trust only permits loading instructions; push/PR/release actions require current user instruction or a matching rule in `~/.config/agent-concepts/publish.yaml`.
- **Test by consuming harness.** Pressure-test discipline concepts in the current harness by default so the run spends this session's/provider's tokens and validates the harness actually being used. Keep reasoning/thinking low for pressure runs unless the user explicitly asks otherwise. If a pressure test must use Claude Code as the subagent harness, invoke Haiku with low thinking (for example `claude -p --model haiku --thinking low ...`) unless the user explicitly asks for a larger Claude model. If a GPT/OpenAI-family harness is used, set low reasoning effort/thinking (for example Pi: `pi -p --model openai/<gpt-model> --thinking low ...`; Codex/OpenAI harnesses: use their low reasoning-effort flag/config). Prefer bounded/non-interactive runs (`--no-session`/ephemeral where available) and minimal context loading so fixture setup doesn't balloon token use.

## Bootstrap prompt patterns

Use `~` rather than hardcoded home paths; this directory syncs across machines.

- Base prompt include:
  `Include <agent-concepts>/concepts/agent-kernel/body/AGENT-KERNEL.md in the harness's main agent instructions.`
- Workspace maintenance:
  `Read <agent-concepts>/AGENTS.md and follow it. Then: <operation>.`
- Concept session, any manual harness:
  `Read <agent-concepts>/concepts/<name>/body/SKILL.md fully. Ignore any YAML frontmatter if your harness does not support Agent Skills metadata. Follow the Markdown body as your instructions for this session.`
- Discipline concept test:
  `Act as the consuming agent for <agent-concepts>/concepts/<name>/body/SKILL.md in a throwaway workspace. Run the scenario in tests/<test>. Produce artifacts, then grade by file inspection, not self-report.`

## Unknowns to resolve

- Whether Gemini has a durable skills directory worth symlink-deploying.
- Grok/Composer auto-invocation pressure runs for discipline concepts (discovery verified 2026-07-04; gate adherence not yet re-tested on these harnesses).
