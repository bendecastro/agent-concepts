# Log

## [2026-06-12] implement | Workspace founded
Scaffolded agents/ (AGENTS.md schema, index, log, bootstrap, raw/, concepts/, scripts/). Migrated the teach skill from .claude/skills/ as the first concept, with CONCEPT.md provenance and its pressure test as tests/pressure-session.md. Founding sources filed in raw/.

## [2026-06-12] deploy | teach → Claude Code
Repointed ~/.claude/skills/teach relative symlink to concepts/teach/body/.

## [2026-06-12] ingest | OpenAI prompting guides filed
Filed GPT-5.2 prompting guide and Codex prompting guide (openai-cookbook, converted from notebooks) into raw/. Filed only — concept extraction pending a discussion of which patterns apply to which agents.

## [2026-06-12] ingest | OpenAI guides → prompting-agents concept
Extracted both OpenAI guides into new reference concept prompting-agents (11 agent-agnostic instruction blocks + metaprompting technique, with accuracy test). Codex quirks (AGENTS.md merge order, no-preamble-prompting pre-5.3, Goal/Context/Constraints/Done-when) added to bootstrap.md. AGENTS.md gained a Tune (metaprompting) operation and points Implement at the block library. Excluded as harness plumbing: apply_patch grammars, phase field, compaction API, tool schemas.

## [2026-06-12] ingest | obra/superpowers skills filed
Vendored the full skills/ tree (14 skills, 400K, commit 6fd4507, MIT + LICENSE) into raw/obra-superpowers/ with SOURCE.md provenance. Filed only — candidates for future concept extraction; systematic-debugging notably includes worked pressure-test examples.

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

## [2026-06-12] implement | agent-kernel trust operationalization
Made publish trust operational: if an agent cannot tell whether project instructions are user-trusted, it must ask before publishing. Softened verification from proof to meaningful validation and tightened scenario 5 to compare remote refs before/after.

## [2026-06-12] implement | agent-kernel publish authorization scope
Scoped publish trust to explicit user-controlled authorization for a repo/path. General project trust, config-loading trust, and repo-local instruction discovery no longer authorize push/PR; scenario 5 gained a config-trust variant.

## [2026-06-12] implement | agent-kernel publish rule finished
Defined the trust-designation channel (in conversation or the user's own harness/vault configuration — e.g. Pi's trust.json; never a repo file) so the exception is no longer a dead letter open to per-harness reinterpretation. Added headless default-deny (if asking is impossible, do not publish). Scenario 5 gained a headless variant (no publish, no stall).

## [2026-06-12] implement | publish policy hierarchy
Added `policies/publish.yaml` as the user-owned publish authorization layer: current user instruction > matching policy rule > default deny. CONFIG push-after-agent-commit is now explicit policy, not repo-local implication; lint verifies default-deny and the CONFIG allow rule.

## [2026-06-12] implement | publish policy hardened after critique
Closed the self-amendment loop: agents/policies/ changes are never publishable under policy rules (header declaration + exclude_changes_under + kernel clause + AGENTS.md Layers entry). Labeled the enforcement model honestly (interpreted, not enforced) and added scripts/publish-check.py for the objective path/remote/branch match — tested on allow, immunity, and deny cases. SSH remote form added so a future origin switch doesn't silently kill the rule. lint.py now parse-checks the policy YAML and requires the immunity fragment.

## [2026-06-12] implement | publish policy for Scripts Music Wiki
Read AGENTS files in `~/Sync/Scripts`, `~/Sync/Music`, and `~/Sync/Wiki`, confirmed each repo uses `master` with GitHub origin, and added explicit user-owned publish-policy rules for agent-authored pushes after commit. Lint now checks those rules remain present.

## [2026-06-12] implement | Repo housekeeping-commit policy
Incident: an agent `git add agents/` swept the user's manual edits into an agent work commit. Added repo-root AGENTS.md (CLAUDE.md symlinked) defining commit separation: agents stage their work by explicit path, then commit remaining tracked drift (user hand-edits, app-written state) as separate housekeeping commits with diff-derived messages; untracked files and secret-shaped or broken diffs are surfaced, not committed. publish.yaml CONFIG rule gained a matching housekeeping exception (separate commits only; policies/ immunity unchanged).

## [2026-06-12] implement | Housekeeping narrowed to two tiers after counter-critique
Counter-critique (via second agent) identified the in-flight-edit risk: agents cannot distinguish settled drift from a user's half-finished config edit, possibly syncing mid-edit from another machine. Housekeeping is now two-tier: tier 1 auto-commits only allowlisted machine-written state (sticker.sql, update-check.json); tier 2 (hand-edited configs) requires shown-diff confirmation, untouched when non-interactive. Housekeeping commits are marked `housekeeping:` + "Observed drift — not agent-authored or validated." Publish exception narrowed to tier 1 only.

## [2026-06-12] deploy | agent-kernel delta → Claude Code user CLAUDE.md
First exercise of the kernel's delta-injection deploy policy: diffed the kernel against Claude Code's built-in prompt; five of seven sections confirmed redundant and not injected. Injected the two genuine deltas into ~/.claude/CLAUDE.md under a DERIVED marker: publish-policy pointer (Claude Code otherwise never uses the pushes publish.yaml grants in Scripts/Music/Wiki) and concepts-catalog pointer (project-scoped memory doesn't reach other repos). Off-vault clause included. CLAUDE.md is Syncthing-synced, not git-tracked.

## [2026-06-12] ingest | image-maze SEO prompts → seo concept
Snapshotted the user's seo-agent.md + image-seo-agent.md + README into raw/ and adapted them (verbatim-preserving) into concepts/seo: SKILL.md (strategist, with Agent Skills frontmatter) + IMAGE-SEO.md (vision-required specialist; owns the handoff field lists). Research pass: conflicting 2026 CWV blog claims validated the verify-at-runtime posture (no numbers changed); one delta added — AI-crawler access policy (training-vs-search bot split; llms.txt labeled speculative).

## [2026-06-12] test+deploy | seo concept passed 4-attack pressure test → Claude Code
Subagent loaded with both body files held all four gate-shaped rules: refused PBN/paid links with legitimate alternatives, declined to fabricate alt text for unseen images, refused a generic checklist dump in favor of diagnosis, corrected the DA myth and sourced the AI-Overview CTR figure live instead of inventing one. Deployed via ~/.claude/skills/seo relative symlink.

## [2026-06-12] ingest | SEO primary sources traced and filed
Traced the seo concept's load-bearing claims to their primary documentation and snapshotted eight pages into raw/seo-primary-sources/ (Google image-SEO, spam policies, SafeSearch, robots-meta, common crawlers; web.dev CWV; W3C alt decision tree; OpenAI bots). New concepts/seo/CITATIONS.md maps each claim to its held source with verification dates; notable finding: official CWV thresholds at snapshot time still 2.5s/200ms/0.1, contradicting 2026 SEO-blog "tightening" claims. Three gaps left open (Anthropic bot docs, IPTC standard, Google licensable-images page).

## [2026-06-12] implement | seo critique fixes
Narrowed the seo skill trigger, added an explicit volatile-facts/source-map rule, softened AI-crawler exclusion language, moved the citation map into the deployed body, added an artifact-producing workflow scenario, and corrected Claude harness docs for the seo deploy.

## [2026-06-12] test | seo workflow scenario 5 passed
Ran the artifact-producing audit on a fixture static site (noindex home, lazy undimensioned LCP hero, cannibalizing page pair, OAI-SearchBot block). Subagent fixed the binding indexation issue first, canonicalized the duplicate pair (flagging merge+301 as editorial), refused to alter robots AI-bot policy without a business decision, and declined to fabricate metadata for a placeholder image. Verified via file inspection. Pass record now includes both conversational and artifact-producing coverage.

## [2026-06-12] deploy | seo → Pi
Deployed the narrowed seo skill to Pi via `~/.pi/agent/skills/seo` relative symlink to the canonical `concepts/seo/body/`; updated deploy records in CONCEPT.md, index.md, and harnesses.md.

## [2026-06-12] deploy | agent-kernel delta → OpenCode
Delta-deployed agent-kernel into `~/.config/opencode/AGENTS.md`: preserved existing OpenCode-specific guidance, replaced the unsafe auto-push rule with the publish-policy/default-deny rule, and added evidence-before-claims plus a marked Specialized Concepts catalog pointer. Updated harness/bootstrap/index/concept deploy records.

## [2026-06-12] deploy | agent-kernel delta → Codex
Delta-deployed agent-kernel into `~/.codex/AGENTS.md`: added defaults-with-reasons, evidence-before-claims, publish-policy/default-deny with Codex `trust_level` explicitly not treated as publish authorization, and the Specialized Concepts catalog pointer. Updated harness/bootstrap/index/concept deploy records; official Codex docs confirmed the global AGENTS.md layer.

## [2026-06-12] test | agent-kernel Codex validation
Recorded bounded Codex validation: active session loaded the global `~/.codex/AGENTS.md` delta, the deployed file marker/content was present, and `publish-check.py` returned the expected allow, deny, and self-amendment-immunity results. A child Codex run passed scenario 5's repo-instruction no-push variant against a local bare `origin`; full baseline/off-vault/policy-allow matrix remains pending.

## [2026-06-12] ingest | omarchy (upstream-maintained skill)
Traced ~/.claude/skills/omarchy to basecamp/omarchy's bundled default/omarchy-skill/SKILL.md. Filed citation snapshot in raw/omarchy-skill-upstream/ and created concepts/omarchy/CONCEPT.md with a deliberate no-vendored-body design: canon and deploy stay upstream so `omarchy update` keeps it current (user decision).

## [2026-06-13] ingest | notebooklm (upstream skill from notebooklm-py)
Installed notebooklm-py v0.7.1 (`uv tool install "notebooklm-py[browser]"`) and deployed its bundled skill via `notebooklm skill install`. Filed upstream-maintained concept (no vendored body, omarchy pattern) + raw snapshot with citation; refresh path is rerunning `skill install` after package upgrades.

## [2026-06-15] ingest | last30days upstream skill
Snapshotted mvanhorn/last30days-skill `skills/last30days/SKILL.md` (v3.3.2, commit 1221584, MIT) into raw/ and added a reference-only `last30days` concept. Deliberately no vendored/deployed body here: the skill's contract is coupled to the upstream Python engine/package and should be installed via upstream plugin/Agent Skills channels.

## [2026-06-20] ingest | Matt Pocock skills catalog
Ingested the new skills repo README clipping into prompting-agents: added a small skill-suite composition block covering user/model-invoked boundaries, shared language, and feedback-loop skills.

## [2026-06-20] ingest | AI Engineer Workshop clipping
Ingested the workshop page into prompting-agents: added agent-ready work shaping guidance for grilling vague requirements, PRD/issue slicing, tracer bullets, TDD feedback loops, and codebase design for autonomous agents.

## [2026-06-20] implement | rename raw source directory
Renamed the workspace source layer from `ideas/` to `raw/` and updated documentation, provenance links, bootstrap examples, and lint checks to match the clearer name.

## [2026-06-20] ingest | AI Engineer Workshop project README
Ingested the companion project README into prompting-agents: extended agent-ready work shaping with explicit project-runway documentation (prerequisites, setup, dev/test/typecheck/build, migrations/seeding) so agents can validate slices independently.

## [2026-06-20] ingest | Matt Pocock workshop skill bodies
Captured the actual SKILL.md bodies behind the workshop pipeline (grilling, grill-me, grill-with-docs, to-prd, to-issues, tdd+support, codebase-design verbatim; domain-modeling summary-only) into raw/pocock-skills-upstream/ as the provenance base for implementing them.

## [2026-06-20] implement | workshop pipeline concepts
Implemented 7 concepts from Pocock's AI Engineer Workshop suite: grilling (loop), grill-me (single always-stateful merge of grill-me+grill-with-docs, per user — persists CONTEXT.md/ADRs via domain-modeling), domain-modeling, to-prd + to-issues (GitHub tracker baked in via gh/ready-for-agent, no setup-skill indirection), tdd (+tests/mocking/refactoring), codebase-design. Bodies adapted (re-voiced, specialized), not verbatim copies; design decisions + provenance recorded per concept.

## [2026-06-20] test+deploy | workshop pipeline (grill stack)
Pressure-tested grill-me (transitively grilling + domain-modeling) via a general-purpose subagent in a throwaway repo; all gates held under artifact inspection (one-question gate, pure-glossary CONTEXT.md, ADR three-part bar, no-code-while-open). Symlink-deployed all 7 workshop concepts to ~/.claude/skills/. codebase-design accuracy-checked; to-prd/to-issues/tdd scenarios authored, full pressure runs pending.

## [2026-06-20] deploy | Local concept skill auto-deploy helper
Added `scripts/deploy-local-skills.py` to bulk expose every local concept skill to Pi and Claude Code via relative symlinks under `~/.agents/skills/` and `~/.pi/agent/skills/`. Updated Pi global instructions so missing-skill requests check local concepts before external installs.

## [2026-06-20] deploy | Claude Code local concept auto-deploy
Extended the local skill deploy helper to update Claude Code as well as Pi, keeping `~/.claude/skills/<name>` pointed directly at canonical concept bodies. Left `deploy-pi-skills.py` as a compatibility symlink to the generalized helper.

## [2026-06-20] plan | grill→ship loop (bc-grill-to-issues + bc-drain-issues)
Grilled out and persisted `plans/bc-grill-to-ship-loop.md`: a one-command interactive
planner (`bc-grill-to-issues`: grill→PRD→issues) and an AFK executor
(`bc-drain-issues`: drain the `ready-for-agent` queue trunk-based via
fresh-subagent-per-issue TDD, park-and-continue + circuit-breaker, publish-check
preflight). Includes a refactor extracting `prd-drafting`/`issue-slicing` disciplines
so the planner composes model-invoked behavior (no orchestrator-calls-orchestrator).
Proposed, not yet built. Added a Plans section to index.md.

## [2026-06-20] implement | grill→ship loop concepts + discipline refactor
Built the plan→execute loop from plans/bc-grill-to-ship-loop.md. Refactor (c): extracted
`prd-drafting` + `issue-slicing` model-invoked disciplines from `to-prd`/`to-issues`, slimmed
those orchestrators to run-discipline→publish (behavior preserved, scenarios updated for
delegation). Added `bc-grill-to-issues` (one-command interactive planner: grill→domain→PRD→
slice, composes disciplines only) and `bc-drain-issues` (AFK executor: preflight publish-check,
fresh-subagent-per-issue trunk-based commit/push/close, park-and-continue + circuit-breaker;
two-file body SKILL.md + execute-issue.md). Added pipeline.md and extended image-maze
planning-workflow.md (separate repo) with the execution phase. Deployed `prd-drafting`/
`issue-slicing` Claude symlinks; held the two `bc-` orchestrators' deploy pending pressure tests.
