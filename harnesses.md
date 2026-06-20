# Harness compatibility

This workspace is canonical at `concepts/<name>/body/`. Harness-specific deployment should expose that canonical body without copying it. When a harness cannot consume an Agent Skills directory directly, point the session at the body file with an explicit bootstrap prompt.

For always-on base instructions, use `concepts/agent-kernel/body/AGENT-KERNEL.md`; it is deliberately a small Markdown include, not an on-demand skill.

## Compatibility matrix

| Harness | Current status | Discovery/deploy method | Frontmatter handling | Notes |
|---|---|---|---|---|
| Claude Code | Deployed for `teach`, `seo`, the workshop pipeline (`grill-me`, `grilling`, `domain-modeling`, `to-prd`, `to-issues`, `tdd`, `codebase-design`), the extracted disciplines `prd-drafting`/`issue-slicing`, and the scaffolder `bc-init-agent`. **Held (deploy pending pressure test):** `bc-plan-to-issues`, `bc-drain-issues`, `bc-autoresearch-loop`. | Relative symlink: `~/.claude/skills/<name>` → `../../Sync/CONFIG/agents/concepts/<name>/body` | Native Agent Skills metadata | Best-supported path today; keep symlink targets relative and inside `concepts/`. Workshop pipeline deployed 2026-06-20: grill stack pressure-tested; `codebase-design` accuracy-checked; `to-prd`/`to-issues`/`tdd` scenarios authored, full pressure runs pending. Loop refactor 2026-06-20: `prd-drafting`/`issue-slicing` extracted + symlinked; the two `bc-` loop orchestrators built but **not symlinked until their pressure tests hold**. |
| Pi | Bulk-deployed local concept skills with `scripts/deploy-local-skills.py` | Relative symlinks in both `~/.agents/skills/<name>` and `~/.pi/agent/skills/<name>` point to `~/Sync/CONFIG/agents/concepts/<name>/body` | Native Agent Skills metadata; unknown frontmatter ignored | Future Pi sessions discover these skills; if a current session's skill list is stale, read `concepts/<name>/body/SKILL.md` directly. |
| Codex | `agent-kernel` delta deployed; validated 2026-06-12 for smoke + scenario 5 repo-instruction no-push variant; specialized concepts via AGENTS.md reference or manual bootstrap | Kernel delta lives in `~/.codex/AGENTS.md`, Codex's documented global instruction layer. For specialized concepts, prefer an `AGENTS.md` at the right repo level that points to this workspace/concept; manual bootstrap also works. | Global/repo `AGENTS.md`; treat frontmatter as plain metadata unless the harness adds skill support | Codex merges `~/.codex/AGENTS.md` plus repo `AGENTS.md` files from root to CWD; deeper files override earlier ones. Full baseline-vs-injected, off-vault, and policy-allow child runs remain pending. |
| OpenCode | `agent-kernel` delta deployed; skills still manual/candidate native | Kernel delta lives in `~/.config/opencode/AGENTS.md`, which OpenCode rules docs define as global across sessions. If/when native skills are enabled, symlink concept `body/` directories into OpenCode's skills location; otherwise manual bootstrap. | Global `AGENTS.md`; native Agent Skills behavior not yet verified | Exact native skills directory still unknown; kernel deploy verified via tracked global instructions file + `opencode debug paths`. |
| Grok | Manual bootstrap only | Paste/read `SKILL.md` for the session | Treat frontmatter as metadata | No official durable skill-discovery path recorded yet. |
| Gemini | Unknown/manual | Use generic bootstrap until tested | Treat frontmatter as metadata | Add quirks after first use. |

## Portability rules

- **Canon stays harness-neutral.** Edit `concepts/<name>/body/`, not a deployed copy or generated harness variant.
- **Frontmatter is optional metadata.** Agent Skills-aware harnesses may use it; other harnesses should ignore the YAML block and follow the Markdown body.
- **Bootstrap beats copying.** If a harness lacks native skills, use a paste/read instruction that points at the canonical file instead of duplicating the concept.
- **Kernel stays tiny.** Always-injected base context should come from `agent-kernel`; keep specialized workflows as on-demand skills/concepts.
- **Record every real deploy.** When a concept is made discoverable without manual paste, update this file, the concept's `CONCEPT.md`, and `index.md`.
- **Publishing needs publish authorization.** Harness/project trust only permits loading instructions; push/PR/release actions require current user instruction or a matching rule in `policies/publish.yaml`.
- **Test by consuming harness.** Pressure-test discipline concepts in the current harness by default so the run spends this session's/provider's tokens and validates the harness actually being used. Keep reasoning/thinking low for pressure runs unless the user explicitly asks otherwise. If a pressure test must use Claude Code as the subagent harness, invoke Haiku with low thinking (for example `claude -p --model haiku --thinking low ...`) unless the user explicitly asks for a larger Claude model. If a GPT/OpenAI-family harness is used, set low reasoning effort/thinking (for example Pi: `pi -p --model openai/<gpt-model> --thinking low ...`; Codex/OpenAI harnesses: use their low reasoning-effort flag/config). Prefer bounded/non-interactive runs (`--no-session`/ephemeral where available) and minimal context loading so fixture setup doesn't balloon token use.

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
