# Delivery reconnaissance

_Scout report from the planning run, 2026-11-25. Raw search output is fenced as text._

README.md:29-48: “You need Git and Python 3”; clone, export `AGENT_CONCEPTS`, run `python3 scripts/deploy-local-skills.py [--dry-run]`. Shared bus always installed, optional Pi/Claude mirrors; repeat `--skip` selects exclusions, not an allowlist. docs/bootstrap.md and docs/harnesses.md do not exist; actual paths are docs/guides/bootstrap.md and docs/guides/harnesses.md.

README.md:13-22: Pi and Claude get own folder; Composer/Cursor, Grok, OpenCode and Muse read shared bus; OpenCode slash commands need plugin, Muse kernel copy is manual; Codex uses instructions/pointers, Gemini manual and untested. README.md:4-6 says edits propagate through symlinks; deleting/moving checkout breaks links. `scripts/deploy-local-skills.py` lines 67-89 replaces any existing symlink even if unrelated, skips existing regular files unless forced, and refuses replacement of directories. This is a collision/overwrite risk. `scripts/deploy-local-skills.py` lines 52-57 discovers private overrides and creates four compatibility aliases. No clean uninstall is documented in README.

## Cross-skill dependencies (direct path matches)
```text
concepts/writing-plans/body/SKILL.md:10:Plan [kernel Storage safety](../../agent-kernel/body/AGENT-KERNEL.md#storage-safety): guarded pytest without custom basetemp, health gates and proven worktree cleanup; plan targeted task checks and shared baseline/landin
concepts/code-review/body/SKILL.md:10:Apply [kernel Storage safety](../../agent-kernel/body/AGENT-KERNEL.md#storage-safety) before parallel review; reuse recorded checks for the exact tree, with only targeted guarded pytest repros for findings. Why: reviewers 
concepts/code-review/body/SKILL.md:36:**Spec reviewer:** report missing/partial requirements, behavior not requested, and apparently implemented behavior that is wrong. Cite the requirement and diff hunk for each finding. Check each new or changed property-bas
concepts/code-review/body/SKILL.md:38:Audit the report's tdd [Test levels block](../../tdd/body/SKILL.md#test-levels) against the diff. Each of these is a finding: a missing block — a packet with code changes but neither a Test levels block nor `Test-levels:` 
concepts/code-review/body/SKILL.md:40:**Standards reviewer:** apply repository standards first. When no project rule settles it, flag material smells as labelled judgment calls—not hard violations: mysterious names, duplicated logic, feature envy, data clumps,
concepts/using-git-worktrees/body/SKILL.md:10:Apply [kernel Storage safety](../../agent-kernel/body/AGENT-KERNEL.md#storage-safety): health-check before either creation path, reuse the once-per-base baseline, and record integration proof before cleanup. Why: n
concepts/finishing-development-branch/body/SKILL.md:10:Apply [kernel Storage safety](../../agent-kernel/body/AGENT-KERNEL.md#storage-safety) for guarded checks and recorded cleanup proof, and [Verification](../../agent-kernel/body/AGENT-KERNEL.md#verification)
concepts/bc-autoresearch-loop/body/SKILL.md:12:Use targeted correctness checks and guarded pytest under [kernel Storage safety](../../agent-kernel/body/AGENT-KERNEL.md#storage-safety); health-check and share the full landing run rather than running a suite eac
concepts/prompting-agents/body/SKILL.md:50:Why: broad descriptions auto-trigger on ordinary questions; loading must not silently authorize costly workflows. From Cloudflare’s security-audit-skill; see [security-audit](../../security-audit/body/SKILL.md#choose-
concepts/executing-plans/body/SKILL.md:10:Apply [kernel Storage safety](../../agent-kernel/body/AGENT-KERNEL.md#storage-safety) in preflight and verification: guarded pytest and health before full suites/isolation/fan-out; apply [Verification](../../agent-kern
concepts/bc-swarm/body/SKILL.md:14:Apply [kernel Storage safety](../../agent-kernel/body/AGENT-KERNEL.md#storage-safety) before fan-out/worktree creation and after integration; copy guarded pytest and [Verification](../../agent-kernel/body/AGENT-KERNEL.md#veri
concepts/bc-swarm/body/SKILL.md:107:**Test levels travel with the code** ([tdd Test levels](../../tdd/body/SKILL.md#test-levels)):
concepts/subagent-driven-development/body/SKILL.md:10:Apply [kernel Storage safety](../../agent-kernel/body/AGENT-KERNEL.md#storage-safety) at preflight and completion; include guarded pytest, targeted tests and shared full-suite evidence in every implementer/
concepts/tdd/body/SKILL.md:8:Use targeted RED/GREEN checks through guarded pytest under [kernel Storage safety](../../agent-kernel/body/AGENT-KERNEL.md#storage-safety); health-check before a full suite, not each cycle. Why: fast feedback does not require repea
concepts/dispatching-parallel-agents/body/SKILL.md:10:Apply [kernel Storage safety](../../agent-kernel/body/AGENT-KERNEL.md#storage-safety) before dispatch/isolation; pass guarded pytest and [Verification](../../agent-kernel/body/AGENT-KERNEL.md#verification) 
concepts/diagnosing-bugs/body/SKILL.md:12:Use targeted guarded pytest under [kernel Storage safety](../../agent-kernel/body/AGENT-KERNEL.md#storage-safety), including health preflight before full suites. For Btrfs storage incidents use the machine's storage he
concepts/bc-pipeline-to-done/body/SKILL.md:39:Apply [kernel Storage safety](../../agent-kernel/body/AGENT-KERNEL.md#storage-safety) before full baseline/landing suites, worktree creation and multi-worker launch; include guarded pytest in packets and record lan
concepts/bc-pipeline-to-done/body/SKILL.md:125:- the handoff contains tdd's [Test levels block](../../tdd/body/SKILL.md#test-levels) with a non-empty L1, L2 and L3 line; a missing or empty block fails the gate. Whether each line is true is the Spec reviewer's 
```
## External dependencies and platform signals (selected evidence)
```text
concepts/council-chain/body/SKILL.md:10:If `~/.config/agent-concepts/overlays/council-chain.md` exists, read it: it names this machine's roster, map-scout model and which advisors are sandboxed.
concepts/council-chain/body/SKILL.md:27:The council changes over time. Never hard-code advisor names in a chain. Run `subagent({ action: "list" })` and take every executable profile whose name starts with `council-`. If the overlay sets a roster, apply it to that list: a named list keeps only those 
concepts/council-chain/body/SKILL.md:39:Run every map scout (one, or several splitting a large codebase) on a strong model with high reasoning effort: the overlay's model if it names one, otherwise the strongest model you can run, rather than the scout role's default route. Why: every advisor judges
concepts/using-git-worktrees/body/SKILL.md:30:If the harness provides native worktree/isolation support (for example a worktree flag/tool or Pi subagent `worktree: true`), use that instead of manual `git worktree add`. Native tools know where workspaces live and how they are cleaned up.
concepts/improve-codebase-architecture/body/SKILL.md:35:- **Without the table**, write it to a temp directory, never the repo: resolve `$TMPDIR`, then `/tmp`, then `%TEMP%` on Windows, and name it `architecture-review-<timestamp>.html`.
concepts/code-review/body/SKILL.md:120:When replying to inline GitHub review comments, reply in the thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`) rather than as a top-level PR comment.
concepts/qmd/body/SKILL.md:2:name: qmd
concepts/qmd/body/SKILL.md:3:description: Search local Markdown knowledge bases (agent wikis, notes, project vaults) with qmd local hybrid search. Use when you need prior decisions, concepts, or notes — one query across all registered collections beats walking directory trees. Also covers who may ru
concepts/qmd/body/SKILL.md:6:# qmd — local hybrid search over Markdown knowledge bases
concepts/qmd/body/SKILL.md:8:[qmd](https://github.com/tobi/qmd) is an on-device search engine (BM25 + vector embeddings + LLM
concepts/qmd/body/SKILL.md:13:rejected ideas, concepts, findings. Check availability with `qmd collection list` (is qmd
concepts/qmd/body/SKILL.md:19:- `qmd query "<terms>"` — hybrid + reranking, best quality; the default. Add `--intent "<what
concepts/qmd/body/SKILL.md:22:- `qmd search "<terms>"` — BM25 keyword only, fast, no LLM; use for exact identifiers.
concepts/qmd/body/SKILL.md:23:  `qmd vsearch` — semantic only.
concepts/qmd/body/SKILL.md:28:- Retrieve: `qmd get "#<docid>"` (docids appear in results), `qmd get <path>:<from>:<count>` for
concepts/qmd/body/SKILL.md:29:  line ranges, `qmd multi-get "<glob>"` for batches.
concepts/qmd/body/SKILL.md:37:Do not run `qmd init` inside a repo, even though upstream docs suggest it. A project-local
concepts/qmd/body/SKILL.md:38:`.qmd/` **shadows the entire global registry** from anywhere inside that repo (verified v2.5.3) —
concepts/qmd/body/SKILL.md:43:If you inherit a repo that already has one, `.qmd/` should be gitignored entirely: its
concepts/qmd/body/SKILL.md:53:  `qmd collection add` outside that file, or machines drift apart and a query means something
concepts/qmd/body/SKILL.md:55:- **Freshness:** run `qmd update && qmd embed` on a schedule (a daily user timer works well). In
concepts/qmd/body/SKILL.md:60:  setup is `qmd pull && qmd embed` (~2GB one-time model download, Node ≥ 22).
concepts/qmd/body/SKILL.md:62:> This workspace's own setup keeps `qmd-collections.yml` in a synced repo and applies it with a
concepts/plan-slicing/body/SKILL.md:13:Work from whatever is already in the conversation. If the caller passes a ticket reference (number, URL, or path), fetch it (`gh issue view <n> --comments`) and read the full body and comments.
concepts/to-tickets/body/SKILL.md:11:**Issue tracker: GitHub**, via the `gh` CLI. Slices that are ready for an agent to grab are published with the `ready-for-agent` label.
concepts/to-tickets/body/SKILL.md:19:   gh issue create --title "<slice title>" --label ready-for-agent --body-file <path>
concepts/triage/body/SKILL.md:56:2. **Check redundancy and prior rejection.** Search the codebase by domain concept for an existing implementation. Read the items in the work-dropped folder if present; surface any similar rejected request or dropped work. If qmd is installed and a global collection 
concepts/to-spec/body/SKILL.md:11:**Issue tracker: GitHub**, via the `gh` CLI. A PRD parent issue is a planning/coordination artifact, not drainable work; `ready-for-agent` is reserved for implementation slices created by `/to-tickets` or `/bc-plan-to-pipeline`.
concepts/to-spec/body/SKILL.md:19:   gh issue create --title "<PRD: feature name>" --body-file <path>
concepts/teach/body/SKILL.md:231:To open files for the user, detect the platform: `open` (macOS), `xdg-open` (Linux).
concepts/bc-work-sync/body/SKILL.md:30:Discover work only from the project's own docs, located through the "Where things go" table in `.bc-agent/AGENTS.md`: requirements (PRD), the decisions folder (decision log and ADRs), research, and the ideas file. Add open GitHub issues (`gh issue list --state 
concepts/bc-work-sync/body/SKILL.md:65:4. Get an independent review of the diff (a fresh reviewer subagent, or the owner when none is available), apply the fixes, re-run step 2 and commit them.
concepts/bc-work-sync/body/SKILL.md:66:5. Publishing: run the owner's publish check, `python3 "$AGENT_CONCEPTS/scripts/publish-check.py" --repo "$PWD" --remote "$(git remote get-url origin)" --branch "$(git branch --show-current)"`. Then check the matched rule's `when:` conditions yourself. If there
concepts/bc-swarm/body/SKILL.md:3:description: Aggressively delegate investigation, analysis, and review to parallel subagents under a durability contract, so a lost tool result or a dead terminal never destroys the work. Use when the user says bc-swarm, swarm, go wide, fan out, or asks for heavy/ag
concepts/bc-swarm/body/SKILL.md:8:If `~/.config/agent-concepts/overlays/bc-swarm.md` exists, read it: it supplies tool names for the generic steps below that this machine's agent instructions do not already name. It never changes behaviour, and the project's own instructions take precedence.
concepts/bc-swarm/body/SKILL.md:32:**The routing decision: name the tracks at the decision point, and decide where each one goes.** List the independent tracks you found; show the dispatched ones in chat. For every dispatched track, name the role and the effective model plus thinking route, in this 
concepts/bc-swarm/body/SKILL.md:117:For implementation fan-out, stop and use `subagent-driven-development` or `bc-pipeline-to-done`. They already own worker packets, spec and standards review, worktree isolation, and rework loops. Why: a thinner parallel-implementation path competing with those will
concepts/bc-wiki-maintain/body/SKILL.md:39:The detector's `qmd registration` line checks the visible layout's two search collections: one
concepts/bc-wiki-maintain/body/SKILL.md:41:`.bc-agent/` (qmd skips hidden path parts, so the first cannot index it).
concepts/bc-wiki-maintain/body/SKILL.md:42:`wiki_lint.py <vault-root> --qmd-entry <slug>` prints both entries for the collections file.
concepts/bc-wiki-maintain/body/SKILL.md:88:17/20 misses for full-sentence qmd searches (Wilson 95% CI `[0.64, 0.95]`) versus 5/20 for the
concepts/bc-wiki-maintain/body/SKILL.md:109:For a deliberate **cross-vault** lookup, use qmd with every collection named explicitly and the
concepts/bc-wiki-maintain/body/SKILL.md:113:qmd search "term one term two" -c vault-a -c vault-b --format files -n 15
concepts/bc-wiki-maintain/body/SKILL.md:116:Never run an unscoped qmd search: it can return rows from unrelated corpora. Resolve
concepts/bc-wiki-maintain/body/SKILL.md:117:collection keys from the qmd registry; never derive one from a `.agent` or `.bc-agent` directory
concepts/bc-wiki-maintain/body/SKILL.md:118:basename. `qmd search` may exit 0 while returning `[]`, so an exit status is not an answer signal.
concepts/bc-wiki-maintain/body/SKILL.md:119:Never use `qmd query`; its model-expansion and reranking path is not suitable for an inline read.
concepts/bc-wiki-maintain/body/SKILL.md:153:Use qmd only for a deliberate cross-vault lookup, with every collection named explicitly:
concepts/bc-wiki-maintain/body/SKILL.md:156:qmd search "term one term two" -c vault-a -c vault-b --format files -n 15
concepts/bc-wiki-maintain/body/SKILL.md:159:Never run qmd unscoped, guess a collection from a `.agent`/`.bc-agent` basename, treat exit 0
concepts/bc-wiki-maintain/body/SKILL.md:160:or `[]` as proof of an answer's absence, or use `qmd query`. If `wiki_search.py` cannot run,
concepts/bc-wiki-maintain/body/SKILL.md:341:vault; do not modify qmd registry policy, other repositories, or the personal wiki from this
concepts/show-me/body/SKILL.md:143:(using `xdg-open` on Linux or `open` on macOS). Do not commit it unless asked.
concepts/bc-plan-to-pipeline/body/SKILL.md:61:   gh issue create --title "PRD: <feature name>" --body-file <summary-with-pointer>
concepts/bc-plan-to-pipeline/body/SKILL.md:75:   gh issue create --title "<slice title>" --label ready-for-agent --body-file <path>
concepts/bc-plan-to-pipeline/body/SKILL.md:77:   Then record the real numbers. With a table: write the final breakdown into the item's `## Steps` (a large item's `plan.md`), each unchecked step with slice title, its issue `#NN`, blocked-by references and user stories covered; a small item's single s
concepts/bc-reflect/body/SKILL.md:10:If `~/.config/agent-concepts/overlays/bc-reflect.md` exists, read it: it supplies tool names and paths for the generic steps below that this machine's agent instructions do not already name. It never changes behaviour, and the project's own instructions take prec
concepts/bc-reflect/body/SKILL.md:41:- Pi session logs: list `~/.pi/agent/sessions/` before assuming a folder name. Current folders use `--@-<path under ~ with / as ->--/` (`@` represents `~`); legacy folders use `--<absolute path with / as ->--/`. Their `*.jsonl` files hold one JSON event per line:
concepts/bc-reflect/body/SKILL.md:53:1. **Wall time and rework** — waits, sleep/poll loops, reruns of the same failing command, rate-limit stalls, subagent rework rounds, a full suite run where a targeted test would do. _When_ the time report or transcript shows a long stretch with little progress.
concepts/subagent-driven-development/body/SKILL.md:2:name: subagent-driven-development
concepts/subagent-driven-development/body/SKILL.md:15:- The harness supports subagents or equivalent fresh-context workers.
concepts/subagent-driven-development/body/SKILL.md:60:- Ignoring a blocked subagent or forcing the same failed prompt again.
concepts/subagent-driven-development/body/SKILL.md:61:- Trusting subagent success reports without checking diff and verification.
concepts/council-mode/body/SKILL.md:16:Run `subagent({ action: "list" })`, then choose 2-3 executable advisor names that start with `council-`. The prefix is convention only. Never use more than four advisors. If the user has no `council-*` profiles, point them to [examples/agents/](examples/agents/
concepts/council-mode/body/SKILL.md:32:3. Launch one async workflow script for Pass 1 with the script inside the call: `subagent({ async: true, options: { script: "<js using runs.all>" } })`. Do not use the `workflow: true` form, which needs a separate ```` ```js workflow ```` block in the same repl
concepts/bc-init-agent/body/SKILL.md:68:   - GitHub readiness: whether `gh` exists/auths and whether `gh repo view` works when an origin exists.
concepts/bc-init-agent/body/SKILL.md:104:Steps 9 and 10 apply to **learning and knowledge** vaults only for now; skip both for code, ops and hybrid. Why: qmd registration and `bc-wiki-maintain` expect a vault with an index, which visible-layout projects no longer have; a later work package of the vi
concepts/bc-init-agent/body/SKILL.md:106:9. **Register the project for global search (default yes, opt-out).** New projects are searchable by default; append to the qmd collections file and apply it with the setup command — see the `qmd` concept. Ask only if the user wants this project **excluded** 
concepts/bc-init-agent/body/SKILL.md:108:     `python3 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/wiki_lint.py" "<repo-root>/.bc-agent" --qmd-entry <slug>`.
concepts/bc-init-agent/body/SKILL.md:112:     work paths. Why two: qmd skips every hidden path part, so a collection rooted at the
concepts/bc-init-agent/body/SKILL.md:140:     Afterwards the lint's `qmd registration:` line reads `registered` (or `unindexed` until the
concepts/bc-init-agent/body/SKILL.md:143:     `--qmd-entry` output.
concepts/bc-init-agent/body/SKILL.md:155:    timer, the new wiki will not promote overnight. This is not qmd:
concepts/bc-init-agent/body/SKILL.md:156:    `bc-qmd-refresh.timer` only refreshes search indexes. `/bc-wiki-maintain`
concepts/seo/body/SKILL.md:65:host-specific — a subagent call, a separate session, or one model wearing both
```
## Harness details
3:This workspace is canonical at `concepts/<name>/body/`. Harness-specific deployment should expose that canonical body without copying it. When a harness cannot consume an Agent Skills directory directly, point the session at the body file with an explicit bootstrap prompt.
11:| Claude Code | `agent-kernel` answer-first posture delta refreshed 2026-08-12; deployed for `teach`, `seo`, the workshop pipeline (`grilling`, `domain-modeling`, `to-spec`, `to-tickets`, `tdd`, `codebase-design`), the extracted disciplines `prd-drafting`/`plan-slicing`, the scaffolder `bc-init-a
12:| Pi | Kernel-derived global instructions in `~/.pi/agent/AGENTS.md` (tracked; answer-first posture refreshed 2026-08-12); bulk-deployed local concept skills with `scripts/deploy-local-skills.py`; `council-mode` also deploys a prompt symlink `~/.pi/agent/prompts/council.md` and needs the `pi-suba
14:| Codex | `agent-kernel` delta deployed; answer-first posture refreshed 2026-08-12; validated 2026-06-12 for smoke + scenario 5 repo-instruction no-push variant; specialized concepts via AGENTS.md reference or manual bootstrap | Kernel delta lives in `~/.codex/AGENTS.md` (→ synced `CONFIG/.codex/
15:| OpenCode | `agent-kernel` delta deployed (answer-first posture refreshed 2026-08-12); local concept skills bulk-deployed via `~/.agents/skills/`; canonical skills are also slash-invocable | Kernel delta lives in `~/.config/opencode/AGENTS.md`; `scripts/deploy-local-skills.py` creates relative c
16:| Grok | `agent-kernel` delta deployed 2026-07-12 and answer-first posture refreshed 2026-08-12 (`~/.grok/AGENTS.md` → synced `CONFIG/.grok/AGENTS.md`; sessions + memory synced too; built-in-prompt diff pending); skills bulk-deployed via `~/.agents/skills/` (same bus as Pi/Composer) | Grok scans 
17:| Muse Code | Kernel delta deployed 2026-11-02; skills already on the shared bus (verified `muse skills list`: 51/51 bus ids at `$HOME/.agents/skills/<name>/SKILL.md`) | Skills: no extra symlink — Muse scans `~/.agents/skills/` (and `~/.claude/skills/` at lower priority). Kernel: regular-file cop
18:| Gemini | Unknown/manual | Use generic bootstrap until tested | Treat frontmatter as metadata | Add quirks after first use. |
20:`bc-work-sync` (2026-11-16) is deployed to `~/.agents/skills`, `~/.pi/agent/skills` and `~/.claude/skills` after its pressure scenarios passed. The same change makes `bc-init-agent`'s visible-layout scaffold copy `body/work_index.py` into each project as `.bc-agent/scripts/work_index.py`; that co
22:The `herdr` reference skill was deployed 2026-07-22 to the shared bus plus Pi and Claude Code symlinks. Composer, OpenCode, Grok, and Muse consume the shared-bus copy; active sessions must restart to refresh discovery.
24:The Obsidian format reference concepts `obsidian-markdown`, `obsidian-bases`, and `json-canvas` were accuracy-checked, mutation-boundary pressure-tested, and deployed 2026-08-17 through `scripts/deploy-local-skills.py` to the shared bus plus Pi and Claude Code symlinks. Their bodies teach file fo
26:The `bc-swarm` go-wide concept was pressure-tested **PASS 4/5** and deployed 2026-08-18 through `scripts/deploy-local-skills.py` to the shared bus plus Pi and Claude Code symlinks. The routing decision also names each child's role + routing-name model + thinking in chat and on the manifest (annou
28:The `agent-kernel` sync-safety rule (survey synced folders for machine-local state; ask before editing ignore files unless asked) passed scenario 12 on Luna max and Grok 4.6 high and was propagated 2026-10-10 to all five global files; Cursor gets it only through the `syncthing` skill.
30:The `agent-kernel` question-format and two-line recap rules were pressure-tested (scenario 10, PASS on Luna max and Grok 4.6 high after two tunes) and propagated 2026-09-23 to all five global instruction files: Pi, Codex, Grok, and OpenCode (CONFIG `6627160`) plus `~/.claude/CLAUDE.md` in its poi
34:On 2026-11-15 the recap became `🏁` / `👣` / `📦` (the delivery line only when something was made for use; committed-only work is not delivered), pressure-tested on Sonnet 5.5 low (owner's substitute for Luna max) and propagated to Pi, Codex, Grok, OpenCode and Muse (CONFIG) plus `~/.claude/CLAUDE.m
36:The `plain-language` discipline was pressure-tested **PASS** 6/6 and deployed 2026-08-18 through `scripts/deploy-local-skills.py` to the shared bus plus Pi and Claude Code symlinks. It is unofficial ISO 24495-1 / IPLF reader-outcome guidance for human-facing prose only; restart sessions after dep
38:The `handoff` concept was pressure-tested **PASS 7/7** (after two tunes) and deployed 2026-08-21 through `scripts/deploy-local-skills.py` to the shared bus plus Pi and Claude Code symlinks. It is the seam *between* harnesses, so it carries a portability property none of the other concepts need: *
42:- **Canon stays harness-neutral.** Edit `concepts/<name>/body/`, not a deployed copy or generated harness variant.
44:- **Bootstrap beats copying.** If a harness lacks native skills, use a paste/read instruction that points at the canonical file instead of duplicating the concept.
47:- **OpenCode commands stay thin.** Slash commands for CONFIG concepts only load the canonical Agent Skill; workflow instructions stay in `concepts/<name>/body/`. The global plugin generates wrappers dynamically and never replaces an explicit command.
49:- **Test by consuming harness.** Pressure-test discipline concepts in the current harness by default so the run spends this session's/provider's tokens and validates the harness actually being used. Keep reasoning/thinking low for pressure runs unless the user explicitly asks otherwise. If a pres
66:- Whether Gemini has a durable skills directory worth symlink-deploying.
67:- Grok/Composer auto-invocation pressure runs for discipline concepts (discovery verified 2026-07-04; gate adherence not yet re-tested on these harnesses).
68:- Muse user-rules load was installed 2026-11-02; a live session recap/`git` clash pressure run has not been done.
70:Copied kernel-delta drift (including Muse) is WARN-only in lint when pairs are configured in private `~/.config/agent-concepts/kernel-copies.json`; see example (`docs/examples/kernel-copies.example.json`).
71:Project skill-copy drift is also WARN-only when repositories are configured in private `~/.config/agent-concepts/skill-copies.json`; see example (`docs/examples/skill-copies.example.json`) for plain paths and per-repo `intentional` skill-name allowlists. Comparisons prefer private overrides over pub
## Install tests

## Interpretation and risks

53 public SKILL.md bodies exist (not the same as deployed count: status exclusions, aliases and private overrides apply). Direct relative paths above resolve when read from the canonical checkout body, but copying an individual body without its sibling concept tree breaks them; agents reading through a symlink may interpret relative Markdown paths from the exposed directory rather than the canonical file, depending on harness. `$AGENT_CONCEPTS` script references require the complete checkout and exported environment. Concept bodies without such references are not thereby proven standalone: named skill handoffs, scripts in supporting files and optional tools still matter. Treat direct path results as a lower-bound dependency map, not a full transitive graph.

`scripts/deploy-local-skills.py` lines 158-185 only filters and adds/updates current links; skipping, changing deployed status or removing a source does not prune existing links. To remove, manually delete corresponding links including aliases and harness mirrors. Existing third-party symlinks of matching names are overwritten without `--force`; examples of generic collision-prone names include tdd, code-review, brainstorming, grilling, research, triage and qmd; README.md:18 explicitly notes Grok bundled-skill shadowing. Collision likelihood is not measured.

Verification: README.md:64,69-71 and scripts/gate:12-17 describe lint, portability and Python tests; CI `.github/workflows/gate.yml:7-20` uses Ubuntu Python 3.13, pytest/hypothesis and GNU coreutils. Pressure test records are checked, not rerun (README.md:69-71); docs/status.md records test state, not proof of present-day interoperability. Existing deployment tests, if listed above, are unit tests, not evidence of end-to-end installation into a stranger's actual harnesses; no fresh real-harness install was verified in this reconnaissance. Python minimum version was not determined; CI covers 3.13, not all Python 3. Bash gate uses `mapfile` and process substitution (scripts/gate:1,16), an issue for stock macOS Bash 3.2; Windows is unverified and symlink permissions may matter.

Residual limits: sampled bodies and direct-path search do not enumerate every dependency or every model/platform assumption; no deployment or tests executed and no external harness was exercised. Quoted excerpts above are source search output with line references; long lines truncated at 260–300 characters.
