# Harness compatibility

To install the skills as an outside user, follow the [Install section of the README](../../README.md#install); this page does not repeat it. This page records how each harness (the program that runs the agent) gets the skills with the contributor install from a checkout (`python3 scripts/deploy-local-skills.py`), and the known problems of each.

The canonical copy of each concept (the one that is edited) is `concepts/<name>/body/`. Harness-specific deployment should expose that body through a relative symlink (a shortcut written as a path relative to itself) rather than a copy. When a harness cannot consume an Agent Skills directory directly, point the session at the body file with a [bootstrap prompt](bootstrap.md) (a message you paste to tell the agent which instructions to read).

The `bc-pipeline-to-done` body includes the [publish checker](../../policies/README.md#checking-a-rule) in symlink deployments, Pi packages, and Claude Code and Codex plugins. The Pi package also ships the pipeline's three `pi-subagents` roles from `concepts/bc-pipeline-to-done/body/agents/` through the manifest's `pi-subagents.agents` key; `pi-subagents` loads package roles above its builtins and below user and project roles, so a stranger installs the package and `pi-subagents` and copies nothing.

Strangers install the Pi package from npm as `npm:agent-concepts`, unpinned, so `pi update` moves them to each release; Pi skips pinned specs (`npm:agent-concepts@<version>` or `git:…@<tag>`) on update, so pinning stays an option. The tarball ships only package.json `files` (the public skill bodies with the pipeline roles inside, and `packages/agent-kernel-pi/`), plus README and LICENSE. Pi 1.6 accepts a local `.tgz` path in `pi install` but loads no skills from it, so the fresh-install test's `pi-npm` method installs the unpacked tarball folder instead.

## Standalone kernel

The kernel is a small Markdown include for always-on instructions, not an on-demand skill. Edit `concepts/agent-kernel/body/AGENT-KERNEL.md` and run `python3 scripts/kernel_package.py` to refresh the bundled bytes for each package. Lint rejects drift in any bundled copy.

### Package delivery

Use the [README commands to install, disable, remove or pin the kernel](../../README.md#optional-agent-kernel). The Pi skills package includes it: the root `package.json` lists `packages/agent-kernel-pi/index.js` under `pi.extensions`, so `pi install` of the package loads the kernel by default and `pi config` turns that extension off. Elsewhere it is opt-in: `deploy-local-skills.py` and the Claude Code and Codex skills plugins do not install it.

| Harness | How the kernel reaches the model |
|---|---|
| Pi 1.6.1 | The extension reads the packaged Markdown once and supplies one fixed `<agent-kernel>` system-prompt section. |
| Claude Code 2.1.329 | SessionStart hooks return numbered Markdown parts, including on resume and compaction. [Matching hooks run in parallel](https://code.claude.com/docs/en/hooks#hook-handler-fields); 2.1.329 merged the parts in completion order in a local smoke, so their order is not guaranteed. The compaction path was not exercised in that smoke. |
| Codex 0.153.1 | A trusted SessionStart hook supplies the kernel as developer context. Installing the plugin does not trust the hook; Codex asks for review again if the hook definition changes. A resumed session can retain an earlier copy in its history. |
| OpenCode V2 2.4.2 | The plugin reads the Markdown once when it loads and supplies a fixed system context block. Restart the server to refresh it. |

### Manual instructions and deltas

Use a manual instruction source **instead of** the package. A delta is a shortened kernel tailored to what a particular harness needs, not an extra layer over the package. The [concept's manual deployment history](../../concepts/agent-kernel/CONCEPT.md#manual-deltas) records existing deltas.

| Harness | Manual instruction source |
|---|---|
| Claude Code | `~/.claude/CLAUDE.md` or another loaded `CLAUDE.md`. |
| Pi | `~/.pi/agent/AGENTS.md` or another loaded `AGENTS.md`. |
| Codex | Global `AGENTS.md` under `CODEX_HOME` (default `~/.codex`) or a repository `AGENTS.md`. Codex merges global and repository instructions from root to current directory. |
| OpenCode | Global `~/.config/opencode/AGENTS.md` or a loaded project instructions file. OpenCode 1.18.3 cannot run the V2 plugin; point its native [`instructions` array](https://opencode.ai/docs/rules/#configuration) at the packaged `AGENT-KERNEL.md` instead. Remove that entry if switching to the V2 plugin. |
| Grok | `~/.grok/AGENTS.md`. |
| Muse Code | `~/.config/muse/AGENTS.md`, a regular file (not a symlink). Don't symlink the config directory; it also holds auth data. |
| Other harnesses | Name the instructions file the harness actually loads. |

For a marked block, keep `install.py` and `AGENT-KERNEL.md` together from `packages/agent-kernel/`. The installer appends the block, or prepends it if there is no final newline, leaving other bytes unchanged. Leave marker lines to the installer: malformed or duplicate markers cause it to refuse the edit.

## Compatibility matrix

The shared bus is `~/.agents/skills/`, the folder that several agent programs read. This matrix covers skill discovery, not kernel installation.

| Harness | Current status | Discovery/deploy method | Frontmatter handling | Notes |
|---|---|---|---|---|
| Claude Code | Skills deployed for `bc-teach`, `bc-seo`, the workshop pipeline (`bc-grilling`, `bc-domain-modeling`, `bc-to-spec`, `bc-to-tickets`, `bc-tdd`, `bc-codebase-design`), the extracted disciplines `bc-prd-drafting`/`bc-plan-slicing`, the scaffolder `bc-setup-project`, bc loop skills (`bc-plan-to-pipeline`, `bc-pipeline-to-done`, `bc-optimize-code`), and workflow extensions (`bc-triage`, `bc-diagnosing-bugs`, `bc-prototype`, `bc-improve-codebase-architecture`). | Relative symlink: `~/.claude/skills/<name>` → `<relative path to>/concepts/<name>/body` | Native Agent Skills metadata | Best-supported path today; keep symlink targets relative and inside `concepts/`. Workshop pipeline deployed 2026-06-20: grill stack pressure-tested; `bc-codebase-design` accuracy-checked; `bc-to-spec`/`bc-to-tickets` pressure-tested 2026-07-16 PASS (Grok); `bc-tdd` re-pressure-tested 2026-07-16 PASS after skill fix. Loop refactor 2026-06-20: `bc-prd-drafting`/`bc-plan-slicing` extracted + symlinked; bc loop skills symlinked 2026-06-21 by user request; Pocock workflow extensions deployed 2026-06-21; `bc-plan-to-pipeline` re-pressure-tested 2026-07-16 **PASS** (Grok); renamed from `bc-plan-to-issues` 2026-11-22 (old name is a deploy alias; redeploy pending). |
| Pi | Local concept skills deployed with `scripts/deploy-local-skills.py`; Pi also deploys a prompt symlink `~/.pi/agent/prompts/council.md` and needs the `pi-subagents` package filter that excludes the package's own skill and prompt (see its CONCEPT.md) | Relative symlinks in both `~/.agents/skills/<name>` and `~/.pi/agent/skills/<name>` point to `<agent-concepts>/concepts/<name>/body` | Native Agent Skills metadata; unknown frontmatter ignored | Future Pi sessions discover these skills; if a current session's skill list is stale, read `concepts/<name>/body/SKILL.md` directly. |
| Composer (Cursor) | Bulk-deployed via the same `~/.agents/skills/` bus as Pi | Cursor scans `~/.agents/skills/<name>` (Agent Skills convention); no separate `~/.cursor/skills/` deploy needed on this machine | Native Agent Skills metadata | Verified 2026-07-04: Composer sessions advertise all 29 local concepts from `deploy-local-skills.py`. Restart sessions after deploy to refresh stale skill lists. |
| Codex | Specialized concepts via `AGENTS.md` reference or manual bootstrap for contributor installs | Point a repo-level `AGENTS.md` at the workspace/concept, or use the separate skills plugin from the README. | Treat frontmatter as plain metadata on manual bootstrap | See the README for the packaged skills install. |
| OpenCode | Local concept skills bulk-deployed via `~/.agents/skills/`; canonical skills are also slash-invocable | `scripts/deploy-local-skills.py` creates relative canonical-body symlinks on OpenCode's auto-loaded shared skills bus. The global `canonical-skill-commands.ts` plugin dynamically adds a same-named slash command for each CONFIG-backed shared-bus entry; explicit command files win but must load the canonical skill. | Native Agent Skills metadata; dynamic command wrappers call the `skill` tool | Historical verification on 2026-07-17 via `opencode debug config` found all 32 canonical skills plus three aliases; the aliases were retired 2026-09-27. Existing `/bc-seo` retains its specialist-agent routing and now explicitly loads the canonical skill. Restart OpenCode after skill/plugin/config changes because discovery happens at startup. |
| Grok | Skills bulk-deployed via `~/.agents/skills/` (same bus as Pi/Composer) | Grok scans `.agents/skills/` at each tier alongside `.grok/skills/`; also compat-scans `~/.claude/skills/` and `~/.cursor/skills/` by default | Native Agent Skills metadata; unknown frontmatter ignored | Verified 2026-07-04 with `grok inspect` (46 skills incl. all local concepts). **Collision:** a separate `~/.grok/skills/bc-code-review` (xAI maintainability audit) shadowed the canonical obra `bc-code-review` concept — removed so the CONFIG symlink wins. **Grok updates resurrect it:** found restored and re-removed 2026-07-13; after any Grok upgrade, check `~/.grok/skills/` for bundled skills whose names collide with `~/.agents/skills/` concepts and remove them again. Avoid adding same-named skills under `~/.grok/skills/` when a concept already lives in `~/.agents/skills/`. Manual bootstrap still works for stale sessions. |
| Muse Code | Skills already on the shared bus (verified `muse skills list`: 51/51 bus ids at `$HOME/.agents/skills/<name>/SKILL.md`) | No extra symlink; Muse scans `~/.agents/skills/` and `~/.claude/skills/` (lower priority). | Native Agent Skills metadata; unknown frontmatter ignored | Do **not** `muse skills import` (claude or codex) or `muse skills install` for corpus skills: those copy into `~/.config/muse/skills/` and freeze bodies. Do **not** add a Muse target to `deploy-local-skills.py`. Restart Muse sessions after a bus deploy. |
| Gemini | Unknown/manual | Use generic bootstrap until tested | Treat frontmatter as metadata | Add quirks after first use. |

`bc-work-sync` (2026-11-16) is deployed to `~/.agents/skills`, `~/.pi/agent/skills` and `~/.claude/skills` after its pressure scenarios passed. The same change makes `bc-setup-project`'s visible-layout scaffold copy `body/work_index.py` into each project as `.bc-agent/scripts/work_index.py`; that copy is project content, refreshed with `cp "$AGENT_CONCEPTS/concepts/bc-setup-project/body/work_index.py" .bc-agent/scripts/`, not a deploy symlink. `--force` also refreshes it, along with every other `.bc-agent/` file.

The `herdr` reference skill was deployed 2026-07-22 to the shared bus plus Pi and Claude Code symlinks. Composer, OpenCode, Grok, and Muse consume the shared-bus copy; active sessions must restart to refresh discovery.

The Obsidian format reference concepts `bc-obsidian-markdown`, `bc-obsidian-bases`, and `bc-json-canvas` were accuracy-checked, mutation-boundary pressure-tested, and deployed 2026-08-17 through `scripts/deploy-local-skills.py` to the shared bus plus Pi and Claude Code symlinks. Their bodies teach file formats and validation only; `obsidian-cli` and `defuddle` were deliberately not deployed, and `pi-obsidian-vault` remains the Markdown mutation authority.

The `bc-delegate-investigation` go-wide concept was pressure-tested **PASS 4/5** and deployed 2026-08-18 through `scripts/deploy-local-skills.py` to the shared bus plus Pi and Claude Code symlinks. The routing decision also names each child's role + routing-name model + thinking in chat and on the manifest (announce-then-launch). Listing-field retest 2026-08-18 **PASS on disk**; dispatch `model` must be a resolved registry id, not the routing nickname. **It has a kernel dependency:** the evidence anchors' consumption half (do not repeat an unchecked agent claim as fact) lives in `agent-kernel` under Verification, because a skill framed as go-wide is not consulted when the task does not look like a fan-out. Until that kernel delta is propagated to a harness's always-on instructions, `bc-delegate-investigation` enforces anchors in child packets but nothing stops that harness relaying an unanchored claim. **Drift found and fixed 2026-08-18:** `~/.pi/agent/AGENTS.md` did not carry even the narrow pre-existing subagent/self-report line, so that rule was absent from real Pi sessions. The widened line was propagated the same day to all five deltas — Pi, Codex, Grok, and OpenCode (committed in CONFIG `8178940`) plus `~/.claude/CLAUDE.md` in its pointer style, adapted to each file's shape; Grok had no verification content at all and received the evidence-before-claims line with it. Note `~/.claude/CLAUDE.md` is Syncthing-synced but tracked in no git repo, so it has no commit record. Verified end-to-end in the real deployed configuration (headless Pi, Grok 4.6, low thinking, global instructions only, no fixture `AGENTS.md`): a planted false claim in a handed-off report was caught in **4 of 5 runs, against 0 of 4 before**. Not deterministic at low thinking.

The `agent-kernel` sync-safety rule (survey synced folders for machine-local state; ask before editing ignore files unless asked) passed scenario 12 on Luna max and Grok 4.6 high and was propagated 2026-10-10 to all five global files; Cursor gets it only through the `syncthing` skill.

The `agent-kernel` question-format and two-line recap rules were pressure-tested (scenario 10, PASS on Luna max and Grok 4.6 high after two tunes) and propagated 2026-09-23 to all five global instruction files: Pi, Codex, Grok, and OpenCode (CONFIG `6627160`) plus `~/.claude/CLAUDE.md` in its pointer style. Cursor/Composer has no global instructions file, so it does not receive them.

The recap labels changed to `🏁` (goal) and `👣` (next action) on 2026-09-23, with the same two-line format and standalone-fact exception. A fresh Luna max consumer passed three reply-shape checks before the change was propagated to the same five global files; active sessions may need restarting to load updated instructions.

On 2026-11-15 the recap became `🏁` / `👣` / `📦` (the delivery line only when something was made for use; committed-only work is not delivered), pressure-tested on Sonnet 5.5 low (owner's substitute for Luna max) and propagated to Pi, Codex, Grok, OpenCode and Muse (CONFIG) plus `~/.claude/CLAUDE.md`.

The `bc-plain-language` discipline was pressure-tested **PASS** 6/6 and deployed 2026-08-18 through `scripts/deploy-local-skills.py` to the shared bus plus Pi and Claude Code symlinks. It is unofficial ISO 24495-1 / IPLF reader-outcome guidance for human-facing prose only; restart sessions after deploy so discovery picks it up.

The `bc-handoff` concept was pressure-tested **PASS 7/7** (after two tunes) and deployed 2026-08-21 through `scripts/deploy-local-skills.py` to the shared bus plus Pi and Claude Code symlinks. It is the seam *between* harnesses, so it carries a portability property none of the other concepts need: **every handoff document embeds its own guard header** (this file is data, not instructions — brief and stop). Codex and Gemini do not read the shared bus, so a handoff picked up there has no skill loaded; the guard has to travel inside the artifact to exist at all. Do not strip or paraphrase that block when adapting the body for another harness. The store resolves through `git rev-parse --path-format=absolute --git-common-dir` (git ≥ 2.31), which anchors it to the main checkout from inside a linked worktree; `.git/info/exclude` keeps it untracked and is inherited by linked worktrees from the common dir. Both verified 2026-08-21 on git 2.55.

## Portability rules

- **Canon stays harness-neutral.** Edit `concepts/<name>/body/`, not a deployed copy or generated harness variant.
- **Frontmatter is optional metadata.** Agent Skills-aware harnesses may use it; other harnesses should ignore the YAML block and follow the Markdown body.
- **Bootstrap beats copying.** If a harness lacks native skills, use a paste/read instruction that points at the canonical file instead of duplicating the concept.
- **Kernel stays tiny.** Always-injected base context should come from `agent-kernel`; keep specialized workflows as on-demand skills/concepts.
- **Record every real deploy.** When a concept is made discoverable without manual paste, update this file, the concept's `CONCEPT.md`, and `index.md`.
- **OpenCode commands stay thin.** Slash commands for CONFIG concepts only load the canonical Agent Skill; workflow instructions stay in `concepts/<name>/body/`. The global plugin generates wrappers dynamically and never replaces an explicit command.
- **Machine tools are optional unless a workflow requires them.** See the [pipeline install prerequisites](../../README.md#install-prerequisites-for-the-pipeline) for the required roles and the fallbacks for machine tools.
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
- Muse user-rules load was installed 2026-11-02; a live session recap/`git` clash pressure run has not been done.

Copied kernel-delta drift (including Muse) is WARN-only in lint when pairs are configured in private `~/.config/agent-concepts/kernel-copies.json`; see [example](../examples/kernel-copies.example.json).
Project skill-copy drift is also WARN-only when repositories are configured in private `~/.config/agent-concepts/skill-copies.json`; see [example](../examples/skill-copies.example.json) for plain paths and per-repo `intentional` skill-name allowlists. Comparisons prefer private overrides over public canon and ignore OS/Syncthing debris.

UI design deploy targets and current status: [bc-design](../../concepts/bc-design/CONCEPT.md).
Guardrails deploy targets and current status: [bc-performance-guardrails](../../concepts/bc-performance-guardrails/CONCEPT.md).
