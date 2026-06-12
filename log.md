# Log

## [2026-06-12] implement | Workspace founded
Scaffolded agents/ (AGENTS.md schema, index, log, bootstrap, ideas/, concepts/, scripts/). Migrated the teach skill from .claude/skills/ as the first concept, with CONCEPT.md provenance and its pressure test as tests/pressure-session.md. Founding sources filed in ideas/.

## [2026-06-12] deploy | teach → Claude Code
Repointed ~/.claude/skills/teach relative symlink to concepts/teach/body/.

## [2026-06-12] ingest | OpenAI prompting guides filed
Filed GPT-5.2 prompting guide and Codex prompting guide (openai-cookbook, converted from notebooks) into ideas/. Filed only — concept extraction pending a discussion of which patterns apply to which agents.

## [2026-06-12] ingest | OpenAI guides → prompting-agents concept
Extracted both OpenAI guides into new reference concept prompting-agents (11 agent-agnostic instruction blocks + metaprompting technique, with accuracy test). Codex quirks (AGENTS.md merge order, no-preamble-prompting pre-5.3, Goal/Context/Constraints/Done-when) added to bootstrap.md. AGENTS.md gained a Tune (metaprompting) operation and points Implement at the block library. Excluded as harness plumbing: apply_patch grammars, phase field, compaction API, tool schemas.

## [2026-06-12] ingest | obra/superpowers skills filed
Vendored the full skills/ tree (14 skills, 400K, commit 6fd4507, MIT + LICENSE) into ideas/obra-superpowers/ with SOURCE.md provenance. Filed only — candidates for future concept extraction; systematic-debugging notably includes worked pressure-test examples.

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
Snapshotted the user's seo-agent.md + image-seo-agent.md + README into ideas/ and adapted them (verbatim-preserving) into concepts/seo: SKILL.md (strategist, with Agent Skills frontmatter) + IMAGE-SEO.md (vision-required specialist; owns the handoff field lists). Research pass: conflicting 2026 CWV blog claims validated the verify-at-runtime posture (no numbers changed); one delta added — AI-crawler access policy (training-vs-search bot split; llms.txt labeled speculative).

## [2026-06-12] test+deploy | seo concept passed 4-attack pressure test → Claude Code
Subagent loaded with both body files held all four gate-shaped rules: refused PBN/paid links with legitimate alternatives, declined to fabricate alt text for unseen images, refused a generic checklist dump in favor of diagnosis, corrected the DA myth and sourced the AI-Overview CTR figure live instead of inventing one. Deployed via ~/.claude/skills/seo relative symlink.

## [2026-06-12] ingest | SEO primary sources traced and filed
Traced the seo concept's load-bearing claims to their primary documentation and snapshotted eight pages into ideas/seo-primary-sources/ (Google image-SEO, spam policies, SafeSearch, robots-meta, common crawlers; web.dev CWV; W3C alt decision tree; OpenAI bots). New concepts/seo/CITATIONS.md maps each claim to its held source with verification dates; notable finding: official CWV thresholds at snapshot time still 2.5s/200ms/0.1, contradicting 2026 SEO-blog "tightening" claims. Three gaps left open (Anthropic bot docs, IPTC standard, Google licensable-images page).
