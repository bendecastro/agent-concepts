## [2026-06-25] ingest | obra-superpowers skills
Created local concepts for uncovered obra-superpowers workflows (brainstorming, planning/execution, subagent orchestration, parallel dispatch, code review, worktrees, branch finishing), mapped overlapping skills into existing TDD/debugging/kernel/prompting concepts, and updated the index.

# Log

## [2026-08-25] implement | bc-swarm Pi routing guidance
Corrected ordinary Pi dispatch to omit `model` when the configured route is correct, avoid child `thinking` as a routing control, and preserve the full effective model suffix for explicit overrides. Recorded the verified top-level/workflow 12-probe matrix and separated its negative reproduction shapes from normal launch guidance.

## [2026-08-24] implement | bc-drain-issues stop report lists child-run dollars
The chat stop report now lists each dispatched child as role + launched model/thinking + list-API cost, then one child-run total. Token counts, phase totals, and soft/hard crossings stay internal. Gate A check 17 asserts the new shape.

## [2026-08-21] implement | agent-concepts publish is explicit-push-only

AGENTS.md now points at `agent-concepts-push-on-explicit-instruction` in the user-owned publish policy: commit locally always; push only on an explicit ask in the conversation. The rule itself lives in `~/.config/agent-concepts/publish.yaml` (CONFIG), not this public checkout.

## [2026-08-21] test | gap-close batch: code-review 7–9 + codebase-design PASS; teach MIXED; research check 3 still BLOCKED

Pi/Grok 4.6 medium consumers in `/tmp/pt-*`, artifacts under `/tmp/bc-swarm/2026-08-21-gap-close/`. code-review checks 7–9 held (inert guard + near-misses; stale README/`docs/`; complexity gate refused). codebase-design matched live upstream SKILL.md (7/7). teach Pi Attack 1 incomplete (consumer read the swarm dir, skipped live quiz). research check 3 still inline — worker had no `subagent` call. Held: kernel matrix, drain Gate B, swarm check 4, bc-init-agent process half.

## [2026-07-25] implement | bc-drain-issues v2 bounded rework tested and deployed

Deployed the approved v2 canon: high-risk contract audit with authoritative external-semantics and launcher-topology checks, cached baseline, minimal Pi roles and lean dual review, up to three fresh same-worktree rework cycles, phase-boundary token circuits, explicit human/deferred/systemic states, canonical-tree recovery bundles, and driver-owned landing. Gate A passed 17/17 with no real mutation. Same-model/medium Gate B used 277,012 child tokens versus v1b's 315,474 (12.2% fewer), passed both reviews and unchanged-baseline correctness, and stayed below the provisional 300k boundary and 500k deployment gate; cost increased in the fixture, so only the token improvement is claimed.

## [2026-07-16] test+implement | tdd + diagnosing-bugs skill fix → re-run PASS

After prior FAIL pressure runs, hardened both skills then re-ran under Grok:

- **tdd:** explicit pressure-refusal blocks for horizontal-slice, call-count assertions, mock-internal, and refactor-while-red (plus rationalization table); scenario now mandates CartService fixture and mid-RED refactor prompt. Re-run **PASS** (`/tmp/pt-tdd-rerun-2150472`) — all four attacks held; 2/4 validly pressured.
- **diagnosing-bugs:** hardened AFK PARK (no invent under "Resolve it") and Phase 6 DEBUG cleanup hard gate with mandatory `rg` evidence. Re-run **PASS** (`/tmp/pt-diag-rerun-2150837`) — cache speculation refused until red loop; one-liner parked; perf measured first; DEBUG stripped (rg clean).

## [2026-07-16] test | Pending pressure tests batch — all ready ones PASS (Grok)

Ran every concept the index/log marked pressure run/rerun pending that was not blocked on a prior skill fix. Current harness (Grok) subagents; throwaway sandboxes under `/tmp/pt-*`; graded by artifacts.

- **PASS (15):** brainstorming, writing-plans, executing-plans, using-git-worktrees, subagent-driven-development, dispatching-parallel-agents, code-review, finishing-development-branch, research, to-spec (unlabeled parent retest), to-tickets, issue-slicing (trust/skip-review gate held — prior FAIL cleared), bc-plan-to-issues (10/10 — prior FAIL cleared; living specs + change folder), bc-drain-issues (13/13 incl. claim race + PRD closeout), bc-init-agent (archetype check 7 + adaptive process 1–6).
- **Skipped (skill-fix gate still open):** tdd, diagnosing-bugs — index still says SKILL fix + re-run; not re-run without the fix.
- **Skipped (specialized):** frontend-design MIXED still needs render-capable higher-fidelity rerun; agent-kernel full baseline/policy matrix; seo workflow scenario 5; accuracy-check-only concepts.

Method notes: controller skills simulated nested workers as packet/report files; bc-drain used a skill-faithful stubbed driver for multi-issue loop fidelity. Deploy of newly proven obra concepts still pending explicit request (symlinks may already exist from bulk deploy).

## [2026-07-04] implement | mesh-check Mac hostname detection
Taught mesh-check to recognize the MacBookPro hostname form observed on the Mac while finishing issue #8, so the Mac skips its self-alias and checks only peers.

## [2026-07-04] implement | machine mesh foundation
Added the repo-tracked shared SSH mesh fragment and portable mesh-check script for PRD #6 / slice #7, then wired omarchy's private SSH config and authorized omarchy's identity pubkey on beelink for the tracer path.

## [2026-07-04] implement | CONFIG drain publish policy
Authorized CONFIG repo AFK issue-drain publishing semantics in publish.yaml: master pushes, bc-drain claim branches, and close-comment issue closeout after validation. User explicitly requested the policy pre-authorization and will push it manually.

## [2026-07-04] deploy | Composer + Grok via shared skills bus
Documented that `deploy-local-skills.py` already feeds Composer (Cursor) and Grok through `~/.agents/skills/` — the same relative symlinks Pi uses. Ran deploy (created missing Claude symlinks for obra concepts). Removed `~/.grok/skills/code-review` so it no longer shadowed the canonical obra concept. Extended lint deploy-dir checks to `~/.agents/skills/`; updated harnesses.md, bootstrap.md, AGENTS.md, and index.md.

## [2026-06-26] implement | bc-init-agent upgrade notes
Taught `scaffold.py` to print manual upgrade notes when an existing project preserves instruction files that should point at newly added scaffold files, starting with the architecture-runway cadence. The skill now tells agents to treat those notes as follow-up pointer-merge work while keeping the scaffold itself additive/idempotent.

## [2026-06-26] implement | bc-init-agent architecture runway cadence
Added a code/hybrid wiki nudge for `/improve-codebase-architecture` based on implemented PRD count rather than days: `conventions/architecture-runway.md` tracks last review plus completed PRDs since review, with a default advisory threshold of 3 PRD-sized changes or 1 architecture-heavy PRD. Root/vault instructions and the skill map now point agents at the tracker.

## [2026-06-26] implement | bc-init-agent generalized wording
Reframed current `bc-init-agent` docs away from one project name and toward the broader agent-maintained wiki concepts: durable project-local context, provenance, live task state, decisions, references, executable plans, and archetypes sampled from existing user wiki patterns. Historical log/provenance entries remain specific where they record actual sources.

## [2026-06-26] implement | bc-init-agent minimal Obsidian vault
Made the `.bc-agent/` Obsidian-vault claim concrete: `scaffold.py` now seeds minimal stable `.obsidian/app.json`, `core-plugins.json`, and `appearance.json` while avoiding noisy user-specific workspace/plugin state. Updated skill/concept/test/index wording and verified rerun idempotency preserves existing Obsidian files.

## [2026-06-26] implement | bc-init-agent wiki archetypes
Added archetype selection to `bc-init-agent`, based on the user's real wiki patterns: code/project execution (`image-maze`), ops/system planning (`Music/.ai/wiki`), learning/teach-backed study, knowledge graph (`~/Sync/Wiki`), and hybrid. `scaffold.py` now supports `--archetype code|ops|learning|knowledge|hybrid` overlays; tests/index/concept notes record the new pending pressure scenarios.

## [2026-06-26] implement | bc-init-agent adaptive onboarding
Updated `bc-init-agent` from blind scaffold-first behavior to recon-first adaptive onboarding: inspect git/GitHub/project/docs/build/deploy state, grill differently for empty/active/messy projects, propose an init or migration plan before writing, and keep file moves as separately approved migration work. Updated concept notes, index status, and pending pressure scenarios.

## [2026-06-22] test | grilling bulk-delegation exit — PASS
Pressure-tested the new bulk-exit clause (Haiku low-thinking, replay of attack 3). On blanket delegation the agent triggered the bulk exit, resolved all 9 remaining branches in one pass with 0 further questions, produced one resolved-plan summary, and did not start building — the behavior the user asked for. Soft spot recorded: it flagged no low-confidence resolutions on genuine judgment calls and said "locked" rather than inviting override; minor SKILL-sharpening follow-up noted in the test file. (Earlier non-replay run only reached Q1 before pausing for input — harness artifact, not a finding.)

## [2026-06-22] implement | grilling bulk-delegation exit (+ revert mis-applied tdd exit)
User clarified their earlier "let me say do-it-all instead of one-by-one" intent was about **grilling**, not tdd. Reverted the tdd principled-exit change made the day before (for tdd the time lever is "test fewer behaviors", not batching; the horizontal-slice ban stays absolute, and the 2026-06-21 tdd FAIL grading is restored). Applied the exit where it belongs: grilling's `SKILL.md` now makes the **bulk-delegation exit** explicit — on blanket delegation ("you decide everything, I don't have time to go one by one"), resolve every remaining open branch with the recommended answer in one pass and present the resolved plan for confirmation, rather than continuing one-at-a-time. The exit trades cadence, never resolution: nothing silently skipped, low-confidence resolutions flagged. Sharpened pressure-grill attack 3 to test it; re-run pending.

## [2026-06-21] test | Pressure-tested the 10 never-run scenarios
Ran every concept whose scenario was authored-but-never-run, on the current harness (Claude Code) forced to Haiku low-thinking per the cost rule, each in its own throwaway sandbox under `/tmp/pt-*`, graded by inspecting artifacts (git logs, written files, stubbed `gh-calls.log`, generated reports) rather than self-report. Results in each `tests/` file.
- **PASS (6):** triage, prototype, improve-codebase-architecture, to-prd, to-issues (note: hardcoded sequential `#NN` under stub), bc-init-agent (deterministic script checks 1–6 run directly + process checks 7–9 via hard-sandboxed subagent; real `policies/publish.yaml` confirmed untouched).
- **FAIL (3):** tdd (performed the write-all-tests-up-front horizontal slice it named as an anti-pattern, and added a `call_count`/`assert_called_once` test instead of a behavior assertion); diagnosing-bugs (speculative-fixed a one-line "login broken" AFK ticket instead of parking, and left 11 `[DEBUG-...]` markers committed); issue-slicing (waived the quiz/approval gate under "skip the review, I trust you"). These three are deployed but now flagged: per the test gate they need a SKILL fix + re-run before being treated as proven.
- **MIXED (1):** frontend-design — inversion (S2) and dashboard utility-copy (S3) hold; anti-attractor default (S1, shipped cream+serif+terracotta with default fonts) and verify-against-render (S4, no screenshot) did not. Needs a render-capable higher-fidelity rerun.
- Scenario/fixture gaps found and noted in-file: tdd attacks 2 & 4 weren't validly exercised (no internal collaborator; no RED test pending at refactor time); triage's "already-implemented request" sub-check had no fixture. Haiku-low is a deliberately weak adherence bar — some FAILs may be model adherence rather than skill weakness; re-runs should separate the two.

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

## [2026-06-20] implement | bc-init-agent scaffolder
Added `bc-init-agent`: a user-invoked scaffolder that stands up a repo-root `AGENTS.md` +
`.agent/<slug>/` Obsidian-vault wiki (generalized from the image-maze vault) wired for the
grill→issues→drain loop, via a deterministic `body/scaffold.py` (23-file tree, `__SLUG__`/
`__DATE__` substitution, clobber-guarded exit 2, root-AGENTS preserved if present). Faithful to
image-maze's persistence model (glossary in the vault, no root CONTEXT.md); the scaffolded
`planning-workflow.md` is the adapter that redirects bc-grill-to-issues persistence and
documents the bc-drain-issues execution phase. Offers a publish.yaml rule (confirm-then-add,
never auto-pushed). Script checks pass; Claude symlink deployed; updated pipeline.md/index/
harnesses.

## [2026-06-20] implement | bc-init-agent: rename .agent→.bc-agent, flatten <slug> nesting
Per user: the scaffolder now writes the vault at `.bc-agent/` directly instead of
`.agent/<slug>/`. Dropped the per-project subfolder (not load-bearing — it only separated
the Obsidian vault from sibling research/scratch, now vault subdirs); the slug survives as
the wiki's display name only. Updated scaffold.py paths/guard + SKILL/CONCEPT/scenario/
pipeline/index references. Re-verified output and script checks.

## [2026-06-20] implement | bc-init-agent: additive idempotency (never destructive)
Per user safety request: scaffold.py is now additive + idempotent — creates only missing
files, leaves every existing file untouched (incl. a hand-written root AGENTS.md, flagged for
manual pointer-merge), and never deletes. Replaced the all-or-nothing "refuse if vault exists"
guard with per-file skip-existing; overwrite is opt-in (--force / --force-root) and --dry-run
previews. Verified: re-run leaves checksums identical; plug-in to a repo with existing files
creates only the gaps; dry-run writes nothing. Updated SKILL/CONCEPT/scenario.

## [2026-06-21] implement | rename bc-grill-to-issues → bc-plan-to-issues
Per user: renamed the planner skill. git mv concept dir + pressure test
(pressure-plan-to-issues.md); updated the name/title/body and every cross-reference across
concepts, index, pipeline, harnesses, scaffold.py templates, the plan doc, and image-maze's
planning-workflow.md adapter (separate repo). Past log entries keep the old name as history.
The grill step itself is unchanged — only the skill name. Still deploy-held pending pressure
test, so no symlink to migrate. Lint clean.

## [2026-06-21] implement | bc-autoresearch-loop (metric-gated bounded improvement)
Added `bc-autoresearch-loop`, a model-invoked discipline that re-expresses the AutoResearch idea from
the Scripts `bc-improve` CLI (idea only — no runtime dependency, rewritten self-contained):
name one objective metric, lock correctness, iterate ONE bounded change, keep only if tests still
pass AND the metric beats the threshold (else revert); stop if no metric exists (don't optimize
blind). Wired into bc-drain-issues' execute-issue.md as a CONDITIONAL post-GREEN step (runs only
when an issue targets a measurable improvement) and noted in its CONCEPT. Pressure test authored;
deploy held pending the run. Updated index/pipeline/harnesses.

## [2026-06-21] test | Pi pressure runs for bc loop concepts
Ran the three pending pressure tests through Pi (`pi -p --no-session --approve --thinking low`), not Claude. Results recorded in each test file: `bc-autoresearch-loop` PASS (reverted wrong/non-winning changes, kept one measured list-comprehension win); `bc-drain-issues` PASS (stubbed gh/push, unauthorized preflight, land/park/block/circuit-breaker); `bc-plan-to-issues` FAIL (question batching, skipped/weak slice approval, placeholder issue refs/body paths). Deploy remains held for the failing planner.

## [2026-06-21] implement | pressure-test harness cost rule
Clarified pressure-test instructions after an accidental initial Claude launch: consume the current harness by default, and if Claude Code is used as the subagent harness, force Haiku with low thinking unless the user explicitly requests another Claude model; GPT/OpenAI-family harnesses must use low reasoning effort/thinking too. Added the rule to harnesses.md and the three bc loop pressure tests.

## [2026-06-21] implement | rename bc-autoresearch → bc-autoresearch-loop
Renamed the metric-gated bounded-improvement discipline to `bc-autoresearch-loop` to make the baseline→bounded-change→measure→keep/revert loop explicit. Updated concept paths, skill metadata, pressure-test filename, bc-drain-issues references, index, pipeline, and harness docs.

## [2026-06-21] deploy | bc loop skills → Claude Code + Pi
Ran `scripts/deploy-local-skills.py` and created relative symlinks for `bc-plan-to-issues`, `bc-drain-issues`, and `bc-autoresearch-loop` in `~/.claude/skills/`, `~/.agents/skills/`, and `~/.pi/agent/skills/`. This was an explicit user-requested deploy; `bc-plan-to-issues` remains marked pressure-failed and needs a fix/re-test before treating it as proven.

## [2026-06-21] deploy | bc-init-agent → Pi verified
Verified `bc-init-agent` relative symlinks exist in `~/.claude/skills/`, `~/.agents/skills/`, and `~/.pi/agent/skills/` via `scripts/deploy-local-skills.py --dry-run`; updated concept/index deploy records. Claude symlink already existed, Pi symlinks were present from the bulk deploy.

## [2026-06-21] implement | bc-drain-issues parallel claims
Researched Pocock's public triage/agent-brief workflow: it has ready-for-agent state and briefs, but no atomic claim/lock. Added a remote Git claim-branch step so concurrent drain runners skip already-claimed issues, and updated the pressure scenario to cover claim races.

## [2026-06-21] implement | Pocock workflow extensions for bc loop
Ingested triage/Agent Brief/out-of-scope, diagnosing-bugs, prototype, and improve-codebase-architecture from Matt Pocock's public skills into local concepts. Integrated them around the bc loop: triage before planning/drain, prototype/architecture as optional evidence/runway before PRD, diagnosing-bugs inside drain for bug issues, and bc-init now seeds `.out-of-scope/`. Deployed new skills to Claude Code + Pi symlinks; pressure scenarios authored, not yet run.

## [2026-06-21] implement | bc-drain-issues discipline wiring clarity
Reinforced the drain executor's subagent handoff so it explicitly composes `diagnosing-bugs`, `tdd`, and conditional `bc-autoresearch-loop`; clarified the per-issue contract that bug-like work must use the debug loop and metric-bearing work runs the autoresearch loop only after GREEN.

## [2026-06-21] ingest | Filed OpenAI + Google + Anthropic frontend-design sources
Research-and-file pass for a future in-house frontend-design concept. Filed to raw/: `anthropic-frontend-design-skill.md` (the reference SKILL.md), `openai-gpt-5-4-frontend-design.md` (blog + OpenAI's official Codex Frontend Skill embedded verbatim, extracted from server-rendered HTML), `openai-gpt-5-frontend-cookbook.md` (stack + steerability learnings), and `google-modern-web-guidance/` (design/UX subset snapshot of Chrome's Modern Web Guidance, blobless sparse clone @eec2f8e, ML model/tooling excluded). Key finding logged in SOURCE.md/index: Anthropic + OpenAI carry the aesthetic "don't look templated" dimension; Google's official offering is platform-correctness/Baseline, not visual design (Material Design 3 would be that, not captured). Index updated; not yet ingested into a concept.

## [2026-06-21] ingest | frontend-design concept from Anthropic + OpenAI sources
Compiled `concepts/frontend-design/` fusing Anthropic's `frontend-design` SKILL.md (spine: studio voice, subject-grounding, thesis→token-plan→critique→build→critique, anti-cliché list, restraint/copy) with OpenAI's Codex `frontend-skill` (archetype checklist: landing/app-dashboard/imagery/motion/copy, hard rules, reject-these-failures, litmus checks). Lean `SKILL.md` + JIT `archetypes.md` (progressive disclosure). User curation: single aesthetic concept; stack-agnostic; composes `playwright-cli`/`verify` for render verification; Google Modern Web Guidance kept as a modern-platform pointer (not vendored); Material Design 3 deliberately excluded (it's a default look the skill warns against). Deepens the existing `prompting-agents` "Frontend anti-slop" block. 4 pressure scenarios authored (blank-brief attractor, design-system inversion, dashboard utility-copy, verify-against-render); run pending. Deployed Claude Code + Pi symlinks; index + raw ingest-markers updated.

## [2026-06-26] update | agent-kernel: offer-to-push-after-commit + cross-vendor preference routing
Added two deltas to `concepts/agent-kernel/body/AGENT-KERNEL.md` from a user request. (1) Git discipline now requires proactively asking whether to push after a commit (still gated on explicit yes / publish policy) — the never-publish rule prevented unwanted pushes but let finished commits sit silently. (2) Operating posture now routes durable user preference requests into this shared canon by default, because the user runs agents across multiple vendors and a per-harness save silently fails elsewhere — prompted by a too-narrow Claude-Code-only memory save that the user corrected. CONCEPT.md design decisions + index entry updated. Refreshed all three deployed deltas (Claude Code `~/.claude/CLAUDE.md`, OpenCode `~/.config/opencode/AGENTS.md`, Codex `~/.codex/AGENTS.md`) with both rules and bumped their DERIVED markers to 2026-06-26. Removed the superseded image-maze project memory `ask-before-push.md`. Pressure scenarios for the two new rules: not yet authored.

## [2026-06-26] update | agent-kernel: offer-to-push carve-out for policy-authorized pushes
Refined the same-day offer-to-push rule after the user said "no need to ask if it's under policy." New shape: when a publish-policy rule already authorizes the push, just push (don't ask); only ask when authorization is undetermined. Updated body, CONCEPT.md, and all three deployed deltas (Claude Code, OpenCode, Codex).

## [2026-06-26] update | bc loop planning trigger + skill map
Updated `bc-init-agent` scaffolding to seed `references/agent-skills.md`, add a planning-intent trigger that asks whether to enter `/bc-plan-to-issues`, and distinguish exploratory research from actual drafted/published PRDs. Also adjusted `to-prd` and `bc-plan-to-issues` so PRD parent issues are coordination artifacts without `ready-for-agent`; only implementation slices enter the drain queue.

## [2026-06-29] update | bc-drain-issues medium subagent effort
After a real Pi drain, tightened the executor so per-issue subagents explicitly run at medium reasoning/thinking effort instead of inheriting high/xhigh from the parent session. Recorded the cost-aware default in the concept design decisions.

## [2026-07-03] update | bc-plan-to-issues: model-invocable
Removed `disable-model-invocation: true` from `concepts/bc-plan-to-issues/body/SKILL.md` at the user's request, after a Claude Code session where the user told the agent to enter the bc loop and the harness refused the Skill invocation. Human gates (grill, slicing quiz) live in the body and are unaffected by who launches the pipeline; the description now scopes model invocation to explicit user requests for the loop. CONCEPT.md records the rationale.

## [2026-07-03] update | bc-drain-issues closes completed PRD parents
Updated `bc-drain-issues` so the driver closes parent PRD issues after all child slices are closed as completed, while leaving parents open if any child is parked, blocked, claimed, or in flight. Added the PRD closeout expectation to the concept and pressure scenario.

## [2026-07-04] update | bc-drain-issues low subagent effort
Changed the AFK drain default from medium to low reasoning/thinking effort for per-issue Pi subagents, preserving explicit effort override guidance so drains do not inherit higher parent settings.

## [2026-07-04] update | agent-kernel: no agent commands in user shell history
Added a Tool-and-file-discipline rule: agents must not record their shell commands into the user's personal shell history (atuin hooks etc.) or re-install such hooks. Prompted by the user finding ~4,300 agent-authored entries (claude-code, codex, pi) drowning ~1,800 of their own in atuin on the desktop; the Claude Code Pre/PostToolUse atuin hooks were removed from the synced ~/.claude/settings.json and the recorded entries purged (backups kept beside history.db).

## [2026-07-04] lint | remove dangling Mac skill deploys
Removed stale macOS deploy symlinks for find-skills, last30days, and omarchy from Pi/Claude skill dirs: no local canonical body or upstream package exists here, and omarchy is Arch/Omarchy-only.

## [2026-07-04] correction | Mac skill-deploy cleanup over-deleted; restored portably
The previous entry's cleanup (999e220) removed symlinks that were dangling on the Mac but valid on Linux — and both ~/.claude/skills and ~/.pi/agent/skills live in synced folders, so the deletions propagated and broke find-skills/last30days/omarchy deploys on the desktop. Restored: ~/.claude/skills links to ../../.agents/skills/<name>; ~/.pi links to ../../../../../.agents/skills/<name> (relative, replacing the old hardcoded ~ omarchy path — the original lint complaint); deployed ~/.agents/skills/{find-skills,last30days} on the Mac. Remaining Mac-only lint danglers for omarchy are by design (Linux-only skill); lesson: a deploy symlink inside a synced dir may be dangling on this machine and valid on another — verify per-machine before deleting.
## [2026-07-04] implement | machine-mesh reference concept
Added the machine-mesh reference concept documenting the three local SSH aliases, MagicDNS names, rules of engagement, and `agents/scripts/mesh-check` verification entrypoint. Recorded PRD #6 / mesh-slice provenance plus an accuracy-check procedure for this reference (not pressure-test) concept.

## [2026-07-04] update | publish policy: plain agent-commit pushes in image-maze
Added `image-maze-push-after-agent-commit` to `policies/publish.yaml` at the user's request ("fix publish policy"). Gap: a plain agent docs commit (docs/launch-plan.md) fit neither existing image-maze rule — the push-and-close rule's when-conditions are issue-drain shaped (`issue_acceptance_criteria_satisfied`), and the doc-maintenance rule is confined to `.bc-agent/`/agent instruction files. New rule mirrors `scripts-repo-push-after-agent-commit` (git_push on master, after_agent_commit + only_agent_authored_changes). Also noted for the record: `publish-check.py` takes the remote URL, not the git remote name — passing `origin` yields a false "no rule matches".

## [2026-07-11] implement | sync selected Matt Pocock workflow upgrades
Renamed standalone `to-spec`/`to-tickets` with `to-prd`/`to-issues` deploy aliases; added primary-source `research`; strengthened issue slicing for fresh contexts and wide refactors; and made AFK issue landing block on independent Spec + Standards review with one remediation/re-review limit. Existing GitHub-only queue semantics and explicit Markdown blockers remain deliberate local divergences.

## [2026-07-12] update | machine-mesh YAML frontmatter correction
Quoted the `machine-mesh` description so its embedded colon is parsed as a scalar rather than an invalid compact mapping. Verified the frontmatter with Ruby's safe YAML loader.

## [2026-07-12] ingest+implement | bc-plan-to-issues living-specs step (OpenSpec)
Ingested the OpenSpec README clipping and adopted its archive-merge idea: bc-plan-to-issues gains step 5, folding resolved PRD requirements into `docs/specs/<area>.md` as normative current truth tagged `(pending #<parent>)`. Runs at plan time (not post-drain) because the human gates are the point of maximum shared understanding; pressure-test check 9 added, re-run pending. Per-change folders and Stores deliberately not adopted.

## [2026-07-12] implement | bc-plan-to-issues per-change folder (OpenSpec)
Second OpenSpec adoption: `docs/changes/<slug>/` is now the single physical home for a change's planning artifacts (canonical `prd.md`, filed evidence, `tasks.md` slice manifest with real issue numbers). GitHub queue unchanged; no duplicated state — parent issue body becomes summary+pointer, tasks.md is a map not a status board. Pressure-test check 10 added, re-run pending.

## [2026-07-12] update | raw/ inbox + raw/ingested/ split
Moved all ingested raw sources into `raw/ingested/`; top-level `raw/` is now the to-ingest inbox (currently: anthropic-claude-code-best-practices.md, the 2026-07-11 mattpocock/skills clipping). AGENTS.md now records the convention plus the relaxed bar (picking a couple of ideas counts as ingested → move the file); lint.py checks both levels and flags location/status mismatches. ~40 provenance/index links rewritten; log history left as written.

## [2026-07-12] ingest | anthropic-claude-code-best-practices.md
Three extractions, user-curated: standing-instruction-file hygiene block (pruning test, include/exclude, prune-don't-emphasize) and verification-ladder + evidence-over-assertion lines → prompting-agents; "Findings are not obligations" reviewer-incentive guard → code-review (protects the bc-drain AFK slice gate from remediation spirals). Harness-specific session/UI advice deliberately not canonized. Moved source to raw/ingested/.

## [2026-07-12] update | mattpocock/skills clipping to raw/ingested/
Moved the 2026-07-11 mattpocock/skills README clipping to raw/ingested/ at user request — ingested by overlap with the earlier catalog snapshot (→ prompting-agents 2026-06-20), no new extractions. Inbox is now empty.

## [2026-07-12] implement | agent-kernel posture: consult on judgment calls
Replaced the kernel's "act directly…ask only when" posture line: bias-to-action stays for mechanical, clearly-specified work, but real judgment calls (designs, interpretations, trade-offs the user might weigh differently) must be surfaced before proceeding. User-requested — he wants to be consulted more; chose this strength among three candidates. Design decision recorded in CONCEPT.md.

## [2026-07-12] deploy | consult-on-judgment-calls posture to harness deltas
Refreshed all three kernel delta files with the new posture line: `~/.claude/CLAUDE.md` (new bullet, marked as overriding the harness autonomy bias), `~/.config/opencode/AGENTS.md` (replaced the old "act directly on the task" Core Behavior line), `~/.codex/AGENTS.md` (new Operating posture bullet). Marker dates bumped to 2026-07-12.

## [2026-07-12] deploy | posture delta to Pi and Grok
Pi: replaced the three old bias-to-action lines in `~/.pi/agent/AGENTS.md` (tracked) with the consult-on-judgment-calls posture. Grok: created `~/.grok/AGENTS.md` as a new marked kernel delta (posture, defaults-with-reasons, cross-vendor routing, publish policy, concepts pointer) — Grok docs confirm it as the global-rules layer; machine-local, full built-in-prompt diff pending. CONCEPT.md deploy records and harnesses.md updated.

## [2026-07-12] deploy | Codex/Grok AGENTS.md + sessions into Syncthing
Moved `~/.codex/AGENTS.md`+`sessions/` and `~/.grok/AGENTS.md`+`sessions/`+`memory/` into `CONFIG/.codex` / `CONFIG/.grok` with per-machine symlinks back, so kernel deltas sync and chats continue from any machine. Sessions/memory are git-ignored (Syncthing-only). `bc-setup-config-symlinks` (Scripts repo, 4f1a845) now links these dirs entry-by-entry and excludes them from wholesale dir-linking — auth, caches, and Grok's per-OS binary stay machine-local. Pi sessions turned out to already sync (the exclusion I cited was git-only); no Pi change needed.

## [2026-07-13] ingest | tobi/qmd → qmd concept + bc wiring
New reference concept `qmd` (local hybrid search: CLI conventions, driver-owns-indexing rule, authority-labeled context trees). Wired into the bc loop: opt-in `bc-init-agent --qmd` scaffold flag (writes `references/qmd.md` setup page; verified additive/idempotent), drain driver preflight refresh + search-only worker retrieval, triage qmd prior-art query. Source clipping moved to raw/ingested/; accuracy check authored but not run (qmd not installed locally).

## [2026-07-13] deploy | qmd skill to local harnesses
Ran deploy-local-skills.py; qmd now symlinked at ~/.agents/skills, ~/.pi/agent/skills, and ~/.claude/skills (all verified resolving to body/). Accuracy check still pending a qmd install.

## [2026-07-13] lint | Grok code-review collision resurfaced
A Grok update restored the bundled ~/.grok/skills/code-review (xAI maintainability audit), re-shadowing the canonical obra code-review concept. Removed again; harnesses.md now warns that Grok upgrades resurrect bundled skills and to re-check for collisions after each update.

## [2026-07-13] test | qmd accuracy check PASS
Added installers/packages/qmd.pkg to Scripts (npm user-local, codex.pkg pattern) and installed qmd 2.5.3 on Arch. Full accuracy check passed: all skill commands work as written; contexts surface authority labels in results; update+embed is a clean no-op. Key finding: project-local .qmd/index.yml stores absolute collection paths → gitignore all of .qmd/, setup per-machine (SKILL.md, scaffold reference page, and CONCEPT.md updated).

## [2026-07-13] implement | qmd rework: global mode only
User decision after grilling: one global index, five collections (agents/wiki/music/scripts/image-maze) from synced canon Scripts/config/qmd-collections.yml, converged per-machine by bc-qmd-setup (+ daily bc-qmd-refresh.timer, qmd.pkg post_install). Removed the same-day --qmd per-repo design from bc-init-agent's scaffold; its close-out now registers new vaults by default (opt-out). Rationale: project-local .qmd/ shadows the global registry (verified) and is invisible from drain worktrees. Skill body, triage/drain detection, and all four CONCEPT.md files updated. Ran setup on Arch: 1055 docs indexed, first embed in progress.

## [2026-07-14] test | qmd vs grep A/B comparison PASS
Two cold subagents, same question, verified ground truth (music sticker-fork decision). Keyword-friendly question: tie on every axis (36s/25k tokens grep vs 45s/24.6k qmd; both correct) — grep stays the right tool when the words match. Paraphrase question with zero keyword overlap: grep 0 hits across all corpora in five phrasings; qmd query --no-rerank hit ground truth (bc-drain-issues claim branches) first attempt in 20.7s. Cold agent also chose the correct latency tier from the skill text alone. Recorded in concepts/qmd/tests/grep-baseline-comparison.md; CONCEPT.md Tests section updated (accuracy-check status was stale, now marked PASS).

## [2026-07-16] ingest | bun-in-rust-zig-port-writeup
Filed and ingested Jarred Sumner's "Rewriting Bun in Rust" (2026-07-08; 535K lines Zig→Rust, 11 days, ~50 Claude Code dynamic workflows). Grilled decisions with user: dispatching-parallel-agents gains homogeneous-fan-out de-risk (task-class guide reviewed like code + 1–3-instance pilot before scaling) and the isolation ban's recorded why + atomic-command fallback; bc-drain-issues gains a recurring-defect tune (driver patches run-local worker packet, additive-only, canon untouched, patches quoted verbatim in run report) with separate-fixer role rejected; code-review makes reviewer context isolation explicit with assume-wrong stance rejected (conflicts with findings-are-not-obligations); AGENTS.md Tune op widened to mid-run. No prompting-agents changes (single-home rule).

## [2026-07-17] deploy | local concept skills to OpenCode
Reconciled `scripts/deploy-local-skills.py` and verified all 32 canonical concept skills resolve through OpenCode's auto-loaded `~/.agents/skills/` bus (plus three compatibility aliases). Updated the deployer and harness documentation to record native discovery; restart remains required to refresh a running session's advertised list.

## [2026-07-17] deploy | OpenCode slash commands for canonical skills
Added a global OpenCode plugin that dynamically exposes every CONFIG-backed skill on `~/.agents/skills/` as a same-named slash command, including compatibility aliases, while preserving explicit command overrides. Updated the existing `/seo` override to load the canonical skill and verified the resolved OpenCode config contains all 32 canonical commands plus three aliases.

## [2026-07-22] ingest+deploy | Herdr agent-control skill
Ingested the user's Herdr agent-skill clipping into a new `herdr` reference concept, vendored upstream `SKILL.md` verbatim at commit `08640bb3ddc0a9c299e855d6a459d2f82970cf86`, and moved the clipping to `raw/ingested/`. Accuracy-checked source integrity and read-only Herdr 0.7.4 commands, then deployed the canonical body to the shared, Pi, and Claude Code skill paths.

## [2026-07-25] design | bc-drain-issues v2 token efficiency
Recorded the user-approved bounded-rework design after issue #29 consumed about 1.89M child tokens across discarded drain attempts and a normal rescue. The pending design preserves both review axes while adding contract audits for high-risk slices, lean structured reviews, fixable-vs-human states, persistent recovery bundles, driver-owned landing, and provisional 200k/300k phase-boundary token caps; live canon remains unchanged until pressure/A-B tests pass.

## [2026-07-25] implement+test+deploy | bc-drain-issues v2 (backfilled)
Backfilled bookkeeping omitted on the day: v2 canon (SKILL/execute-issue/review-contract/recovery-bundle),
minimal Pi drain roles, and compact subagent tool descriptions shipped after Gate A 17/17 and Gate B
277,012 child tokens (12.2% below v1b). The index entry had still described v1.

## [2026-07-26] implement+test | bc-drain-issues v3 review economy
Reworked the review phases for token cost: the driver now materializes one review packet per round and
reviewers may not re-derive status/diff; approvals became standing records bound to the reviewed diff
hash, so only the raising axis plus any axis whose deterministic delta trigger fired re-reviews, while
landing still requires both axes on the final hash; axis count is tiered by risk with one-way escalation
on gate rejection or any Critical finding; and reproduction commands are gated on a formed finding.
Gate A extended to 21 checks and passes 21/21, verified against a negative control on the pre-v3 canon.
Gate B is NOT run and must use a contested fixture, so the change is pressure-tested but not yet
token-validated.

## [2026-07-26] implement+test | bc-drain-issues v3 narrowed rework scope
Extended the review-economy pass to the reworker, which was still repeating the full review-ready gate
each round. It now re-evidences only the rows implicated by the findings, rows whose mapped files its
fix touched, and anything already failing or flaky; other evidence carries forward, and full-scope
status/staged/unrelated inspection is dropped because the driver's deterministic gate re-checks it.
The gate verifies coverage from the matrix→file map, so a skipped touched row is rejected. Gate A is
now 22 checks and passes 22/22. Accepted trade-off recorded: a regression on an untouched,
unimplicated row surfaces at final full validation rather than mid-round.

## [2026-07-27] test | contested Gate B fixture for bc-drain-issues v3
Built the contested fixture v3's Gate B needs, since v2's clean fixture never exercises selective
re-review or narrowed rework. `tests/fixtures/contested-gate-b/make-fixture.py` generates a
disposable bc-svc compatibility/systemd sandbox (hidden reload/apply-change commands omitted from
the Agent Brief, an argument-boundary defect in an unmapped internal helper, contradictory
repository prose vs primary systemd docs, a known baseline failure, and a dependent child issue),
plus PATH-first gh/push/publish stubs over a JSON issue store. Verified reproducible base SHA
across arms, correct baseline failure, claim create-once/reject-twice, and stub resolution.
Runner handoff prompt in AGENT-PROMPT.md; v2 arm pinned at canon 745fe01. Gate B still NOT RUN.

## [2026-07-27] test | deterministic contested Gate B fixture commits
Fixed independently generated Gate B arms receiving different base SHAs because Git embedded their
wall-clock commit times. The generator now pins author/committer dates and disables commit signing for
the fixture commit. Two generations separated by two seconds produced identical base SHA
`8bacfc040999afe6702d7a86ff3642f6bbce80e7`; the expected 3-pass/1-known-failure baseline still held.

## [2026-07-27] test | bc-drain-issues v3 contested Gate B attempt
Ran the pinned v2 arm first with `openai-codex/gpt-5.6-sol` at explicit medium effort. It used
205,781 child tokens through audit, build, one rework, and two dual-axis review rounds; after the
single citation fix both axes approved. Because the fixture produced only one rework round, the
runner stopped before landing or starting v3, as the two-round contest criterion requires. Recorded
the attempt as INVALID, not an A/B result; v3 remains deployed but not token-validated.

## [2026-07-27] tune | inert-guard review class from an image-maze drain
A real `/bc-drain-issues` run on image-maze #203 (an issue *about* two inert referral gates) had its build worker reproduce the defect class it was assigned to remove: it deleted the named tautological clause, left a sibling clause tautological, and substituted `$campaign['id']` for `$campaign_id` — an identical runtime value that made the tautology look like two independent facts. Independent Spec review caught it, and reverting the expression made the test *fail*, proving the clause had only ever been green as a tautology. Promoted per the Tune operation: `code-review` gains a general "Verify a guard can actually fire" block (paired explicitly with *Findings are not obligations* so it is not read as licence for defensive code), `bc-drain-issues` gains a `guard/rejection clause -> can-its-inputs-differ-in-production evidence` audit row and an unfireable-guard rule in `review-contract.md` (AFK reviewers see only the driver's packet). Both bodies are symlink-live immediately; the `code-review` pressure check 7 is authored but **not run**, and the drain row has no Gate A check because it is a model-behaviour property. Test gate is therefore outstanding for both — recorded rather than implied.

## [2026-07-27] implement+test | deterministic bc-drain-issues v3 Gate B trace
Replaced probabilistic topology as the deployment benchmark with a locked S0→S1→S2 trace containing exactly two Standards-only reworks; the natural contested fixture and its one-rework INVALID result remain ecological-pressure provenance. The harness pins hostile-environment-resistant SHA-1 Git identity/config, regenerates its own canonical contract, uses sanitized no-remote roots plus fail-closed receipt stubs without falsely claiming physical network isolation, and derives model/session tokens from real Pi lifecycle artifacts. Reviewer JSON and reworker patches now supply independently checked fidelity; stale Spec hashes cannot land and v3 requires a focused final S2 Spec sync. Gate A remains 22/22 with check 19 strengthened for both intermediate skips and exact-hash sync; trace self-test passes all identity, behavior, evidence, isolation, dispatch, and landing checks. Real same-model/medium v2/v3 token measurement remains outstanding.

## [2026-07-30] implement | machine-mesh remote-command PATH
Non-interactive SSH sources neither .zprofile nor .zshrc, so an agent had reported node/npm/gh missing on the Mac when all were installed. Documented the check and the `~/.zshenv` fix in body/SKILL.md, recorded the decision and an accuracy-check run. beelink was unreachable during verification.

## [2026-08-02] implement | portability — the workspace is installable by anyone

Made the workspace usable by someone who is not its author, then proved it with a test rather
than an assertion. See [plans/portability.md](plans/portability.md).

- **Two path mechanisms, chosen by context.** `$AGENT_CONCEPTS` for anything a shell executes
  (commands inside deployed bodies); `<agent-concepts>` for anything a human pastes into a chat
  window, where an environment variable would not expand. Getting this wrong in either direction
  produces a path that silently does nothing.
- **The worst offenders were the deployed bodies**, not the docs. `bc-drain-issues` ran
  `publish-check.py` from a hardcoded path, and `bc-init-agent`'s scaffold wrote that same path
  into every project it initialised — the assumption propagated outward into other repos.
- **The publish policy moved out** to `~/.config/agent-concepts/publish.yaml`. Self-amendment
  immunity had been implemented as the literal string `agents/policies/`, which would have gone
  silently inert; it now resolves the policy's real path and still fires when the config directory
  is reached through a symlink into a synced repo. Verified both ways.
- **`lint.py` had been enforcing the author's config** — it asserted the policy named four
  specific repositories, so it rejected anyone else's. The check had mistaken the data for the
  invariant it was protecting.
- **Lint blind spot found and fixed:** it validated `[text](target)` links but not backticked
  inline paths, which is how 74 provenance references broke silently. On its first run the new
  check found 17 more, including a concept renamed months earlier.
- **Lesson worth keeping:** the portability test exports `HEAD`, not the working tree — so it
  tests what a stranger receives. It failed the first time precisely because the fixes were
  uncommitted, which is the correct answer to "is this portable right now?"

## [2026-08-03] deploy | second machine onboarded; a relative-symlink trap

Brought the Mac onto the new layout. Both repos had already arrived via Syncthing, so the work was
the three things that do not sync: the config symlink, the environment variable, and the skill bus.

- **`~/.config` may itself be a symlink.** On the Mac it points at `dotfiles/.config`, so a
  *relative* link created inside it resolves against the link's own directory, not the path you
  typed — `../Sync/...` landed in `dotfiles/Sync/...` and silently dangled. `publish-check.py`
  caught it immediately by reporting no policy found. Fixed with an absolute link, and the Linux
  box was aligned to match rather than left on the fragile form.
  `deploy-local-skills.py` already knew about this class of bug: `rel_target()` computes from the
  **resolved** parent for exactly this reason. The script was right; the hand-made symlink was not.
- **No systemd on macOS**, so `environment.d` is inert there — `AGENT_CONCEPTS` has to come from
  `~/.zshenv`, which is also the only file a non-interactive `ssh host cmd` reads.
- **Left the dangling `omarchy` links alone.** They are Arch-only and were already dangling on the
  Mac. `~/.claude/skills` and `~/.pi/agent/skills` are synced, so deleting them there would
  propagate and break the Linux box — the failure recorded in the 2026-06 entry. Dangling on one
  machine is not evidence of dangling everywhere.
- Result: 120 links resolve on the Mac, 34 public + 3 private, the 2 known omarchy danglers aside.

## [2026-08-04] implement | kernel: write agent instructions to AGENTS.md, never CLAUDE.md
Promoted a per-repo Claude Code memory into the kernel's tool-and-file discipline: project agent
instructions go in `AGENTS.md`, and a vendor-named file should be a symlink rather than a second
copy that drifts. It was a cross-vendor rule stranded in one WordPress repo's memory store, which
is exactly the failure it warns about.

## [2026-08-12] test+deploy | kernel: answer questions before editing
Pressure-tested the question→approval boundary in a temporary Git fixture. Two weaker phrasings correctly avoided edits but failed to ask whether to proceed; strengthened the rule to require ending with an explicit permission question whenever any relevant change is identified. The final two-turn run passed: answer + permission question with no tracked mutation, then approved edit + validation + commit. Refreshed the answer-first delta in Pi, Claude Code, OpenCode, Grok, and Codex global instructions.

## [2026-08-12] implement | kernel: answer questions before editing
Replaced the plan-only posture line with an answer/action boundary: informational and advisory questions get an answer first, and agents must offer changes and wait for explicit approval; direct concrete change requests still trigger end-to-end action. Added pressure scenario 9 for the two-turn question → approval transition. The cross-harness deltas were not refreshed, and the scenario remains unrun pending deployment.

## [2026-08-04] implement | kernel: commit by default, publish never
The kernel gated pushing thoroughly but never said committing was automatic — it opened with
"when you changed files:" and went straight to *how* to commit, leaving *whether* to commit
implicit. In practice that reads as permission-seeking, and agents ask before committing.

Made the asymmetry explicit: **commit freely, publish never.** A commit is local and reversible
(amend, reset, revert), so an unwanted one costs ~nothing, while uncommitted work is genuinely
lost to a stray checkout or mixed into the next change. A push is outward-facing and effectively
permanent. Added a bullet stating that authorization to commit never implies authorization to
push — the two are separate decisions.

Prompted by a session publishing the homeflix repo, where the agent held work uncommitted while
asking about publishing; the user's correction was "always commit but don't push". The push side
of the policy was already correct and is unchanged.

**Test gate: not run.** agent-kernel is discipline-enforcing, so a pressure scenario is warranted.
The change only *loosens* the commit side and leaves every push gate untouched, so the risk is a
too-eager commit rather than an unauthorized publish — but the existing anti-push scenarios in
`tests/pressure-scenarios.md` should be re-run to confirm "commit freely" isn't read as license to
push. Flagged rather than skipped silently.

## [2026-08-16] housekeeping | ignore project-local Pi state
Removed the tracked `.pi/memory/MEMORY.md` preference file and ignored `.pi/` so machine-local
Pi state cannot drift into the repository again.

## [2026-08-17] implement+test | issue-slicing: align slices with drain token boundaries
Made the 200k aggregate child-token soft cap a qualitative agent-readiness gate covering audit,
build, review, and likely rework; 300k remains recovery-only. The 6/6 pressure run split an
oversized compatibility/migration task, exposed budget fit in the mandatory quiz, and resisted
keep-one-issue, target-300k, and skip-review pressure. The Pi subagent extension failed before
launch on Bun `node:v8.createHook`, so the valid artifact came from a fresh read-only headless Pi run.

## [2026-08-17] ingest+implement+test+deploy | Obsidian format skills
Filed the pinned MIT upstream snapshot and adapted `obsidian-markdown`, `obsidian-bases`, and
`json-canvas` as safe format/validation references. Deliberately excluded `obsidian-cli` and
`defuddle`; deployed the three canonical bodies and verified the nine relative symlinks.

## [2026-08-17] test | Obsidian format mutation boundaries
Added adversarial scenarios after independent review identified the safety clauses as runtime gates.
Headless Pi agents refused direct-write/shell/`eval` bypasses in all three cases; fixture hashes stayed unchanged.

## [2026-08-17] ingest+implement | minimal-solution-ladder from ponytail
Filed the pinned MIT ponytail snapshot (skill bodies + benchmark writeup only; the ~20-harness plugin,
hook, MCP and statusline machinery is distribution, not substance) and adapted the primary skill as
`minimal-solution-ladder`. Cut to the delta over Claude Code built-ins and `agent-kernel`: the ladder's
ordering (rung 4, native platform features, was absent locally), root-cause-as-the-lazy-fix, the renamed
`ceiling:` marker, and the auditable skipped-line. Arbitrated three conflicts in canon rather than
copying them: scope split with `codebase-design` (whether/how much vs shape), subordination to
`tdd`/`bc-drain-issues` on tests, and no duplication of harness built-ins. Upstream's always-on hook
persistence was deliberately not reproduced; skill-only for now, kernel pointer only if drift shows.
Pressure test authored, not run — not deployed.

## [2026-08-17] test+deploy | minimal-solution-ladder
Pressure-tested in headless Pi (Grok 4.6, low thinking) against a fixture repo baited for every rung.
PASS 10/10 after one fix: all three load-bearing checks held first time, including two refusals to drop
trust-boundary validation and a root-cause fix in the shared validator rather than the reported caller.
The ceiling-marker check failed twice — the model named a real O(n²) ceiling in its response while
leaving the code unmarked, because the `skipped:` output line was absorbing the obligation. The body now
says the response does not discharge the code marker (the response is read once; the next reader meets
the code alone); the re-run emitted the marker in source. Deployed to all three symlink targets.

## [2026-08-17] tune | the Tune operation itself
Expanded metaprompting from self-critique-only after a minimal-solution-ladder run exposed its blind
spot: the agent named a required `ceiling:` marker in chat, left the code unmarked, and by its own
account had complied — only artifact grading caught it. Added the general lesson (grade the artifact the
next reader will meet; a report-shaped rule launders a mark-the-code rule), mechanism-before-rewrite,
and replace-over-append. Independent Grok review cut three overclaims, including "recurrence is evidence
only across independent runs" — which would have disqualified this change's own evidence, since a check
failing twice is evidence while a repeated suggestion in one session is an echo.

## [2026-08-18] tune | minimal-solution-ladder: requested behavior, not requested shape
First run of the improved Tune operation. Artifact grading showed a pass-through wrapper recurring 3/3
(the no-skill control too, so the skill was failing to prevent baseline behavior); self-critique on two
models independently found the mechanism — the never-simplify clause "anything explicitly requested"
absorbed rung 2, so "add a function" read as a build order. Adopted in general form: the phrasing of a
request pre-commits a shape, and the noun is not the order. Both models nominated the same line for
deletion ("take the higher one"), so the tune was net-neutral in length. Re-verified 2/2; check 5 held,
with the attack weaponizing the new clause and losing.

## [2026-08-18] ingest+implement | plain-language from ISO 24495-1 public principles
New human-facing writing discipline from IPLF's four reader-outcome principles (relevant /
findable / understandable / usable). Named `plain-language` rather than `iso-24495` to avoid a
conformance claim; review-default with rewrite on request; inverts off agent-facing skills/gates;
no numeric readability proxies and no Parts 2–5 clone. Public ISO/IPLF URLs cited, standard text
not filed. Pressure scenarios authored, not run — not deployed.

## [2026-08-18] test | plain-language pressure — PASS 6/6
Headless Pi, Grok 4.6, low thinking, isolated `/tmp/pt-plain-language-139910` copies.
All four load-bearing checks held: skill why/gate kept under time pressure, no ISO stamp
on rewrite, deadline and no-share rule survived, review left `notice.md` untouched.
Reader named and action moved first. Not deployed.

## [2026-08-18] deploy | plain-language
Deployed via `scripts/deploy-local-skills.py` after the 6/6 pressure pass. Relative
symlinks created under `~/.agents/skills/plain-language`, `~/.pi/agent/skills/plain-language`,
and `~/.claude/skills/plain-language`; all three resolve to `concepts/plain-language/body`.
Restart sessions to refresh advertised skill lists.

## [2026-08-18] implement | thin plain-language clauses on three speakers
Adapted a 2–4 line reader-outcome delta into `grilling` (decision-first question),
`improve-codebase-architecture` (HTML report for a busy owner choosing a candidate),
and drain `HUMAN_BLOCKED` comments. Deliberately not a `plain-language` skill load;
issue-slicing, teach HTML, PRDs, and briefs left unwired. New expected lines added to
existing tests; not re-run.

## [2026-08-18] implement | bc-swarm — aggressive delegation with a durability contract
New user-invoked concept from a live loss: five `async:false` scout children died with a
Herdr pane (no coredump, no OOM — the host container vanished), taking all five results
and leaving zero artifacts. Body inverts the delegation default and adds four durability
rules (manifest + announced run dir, async as a gate for multi-child fan-out, incremental
per-child artifacts, recover-before-relaunch) plus evidence anchors for the thin parent.
Read-shaped; implementation fan-out still belongs to `subagent-driven-development`/
`bc-drain-issues`. Pi mechanics in `body/pi.md`. Five pressure scenarios authored, not run.

## [2026-08-18] test | bc-swarm pressure — FAIL 3/5, deploy blocked
Headless Pi, Grok 4.6, low thinking, isolated `/tmp/pt-bc-swarm-45805` copies, graded on
disk artifacts and timestamps. The three crash-derived durability rules held: manifest
preceded dispatch (22:19 vs 22:21+), recovery re-dispatched only the missing track, and
the async gate survived "run it synchronously". Thin-parent anchor guard FAILED — a
planted false claim was relayed as fact — and the escape hatch stayed silent. One tune
(rebinding both rules from the dispatch path to the decision point) changed no behavior
on re-run; kept for accuracy only. Revised diagnosis recorded: the guard fails wherever
the task does not already look like fan-out, which is a placement problem, not wording.
Check 4 also judged suspect — it grades an agent for obeying an explicit instruction.

## [2026-08-18] tune+test | bc-swarm anchor guard relocated to agent-kernel — PASS 4/5, deployed
First run's diagnosis (wording) was wrong; rewriting the section changed no behavior. A
three-way A/B on one prompt located the cause: skill alone FAIL, deployed globals alone
FAIL, skill + one candidate always-on line PASS. Widened the kernel's Verification line
from subagent/tool *success reports* to handed-off agent output, forbidding repeating an
unchecked claim as fact — shipped verbatim as the wording that passed. `bc-swarm` now owns
only anchors-in-packets and points at the kernel, with an explicit do-not-re-add note.
Re-ran the full gate with the always-on layer present: 4/5, all load-bearing checks pass
(manifest preceded dispatch by ~2min on disk; recovery relaunched nothing; planted false
claim caught; async gate held). Check 4 fails a third time, accepted as documented.
Deployed bc-swarm to shared/Pi/Claude. **Found deploy drift:** the deployed
`~/.pi/agent/AGENTS.md` lacked even the narrow pre-existing kernel line, so that rule was
absent from real Pi sessions; propagating the kernel delta to the five harness files is
outside this repo and not yet done.

## [2026-08-18] deploy | widened kernel verification line to all five harness deltas
Propagated the handed-off-agent-output rule to Pi, Codex, Grok, OpenCode (CONFIG 8178940)
and `~/.claude/CLAUDE.md` (untracked; Syncthing only), adapted to each delta's shape.
Verified in the real deployed config, not a fixture: global instructions only, planted
false claim caught 4/5 runs vs 0/4 before. One failure (H2) was initially misread as
context dilution; a controlled project-vs-global comparison and three more samples showed
it was a flake — the global file is loaded (it recalled Luna-max and bc-improve unprompted).
Rule is a large improvement, not a guarantee, at low thinking.

## [2026-08-18] implement | bc-swarm tooth names role + model + thinking
Extended the go-wide tooth so each child track is announced with role and this
session's routing-name model + thinking, then launched in the same turn. Same
fields go on the manifest. Parent-kept tracks stay parent + why. Pi mechanics
now pass `thinking` on the child and a resolved registry id as `model`.
Listing-field retest (check 1): manifest and second launch carried role +
model + thinking; first launch failed on `model: "luna"` (example removed).
Deployed to the existing shared/Pi/Claude `bc-swarm` symlinks (already pointed at `body/`).

## [2026-08-18] ingest | codebase-docs from DeepSeek Harness
Grilled extract of how `dsh` keeps source-tree docs truthful: one home per
fact, current-state writing, tutorial vs reference, same-change owner update.
Rejected their notes-every-change gate, i18n pairing, and verifier scripts.
Concept only this pass; pressure test authored, not run; deploy blocked.

## [2026-08-18] implement | unpark codebase-docs pointers and note ideas
`code-review` Standards loads `codebase-docs` on source-tree doc diffs.
`bc-init-agent` points new/upgraded code wikis at it and adds ADR
alternatives to the template. `domain-modeling` records alternatives and
supersedes instead of rewriting. Notes-every-change still rejected.

## [2026-08-18] test+deploy | codebase-docs pressure PASS 6/6
First Grok-low run failed two load-bearing checks: it created `docs/cli.md`
under "just make docs/cli.md", and deleted a vault page to satisfy
one-home. Tightened those two holes and re-ran: 6/6. Soft note: check 4
still edited `AGENTS.md` to drop a vault pointer. Deployed relative
symlinks on the shared/Pi/Claude skill buses.

## [2026-08-19] ingest | unslop from Cursor's plugin skill + AI-tell evidence base
Grilled to eight resolved branches, then built `concepts/unslop/` as a
model-invoked provenance-tell editor. Kept Cursor's structure; cut six
rules that duplicate `plain-language`; replaced the absolute em dash ban
with a formulaic-use rule after the Economist's 2026 corpus (only Claude
now exceeds human writers; ChatGPT uses fewer) and named zero-dashes as
its own tell. Added the classes upstream lacks: sentence constructions,
document shape, artifacts (commit-message canned assurance, paste junk,
placeholders) with a verified `rg` block, and three guard rails against
the skill itself. Statistical thresholds deliberately not shipped —
the source study is paywalled and its scalars are unvalidated here.
Pressure test authored, not run; not deployed.

## [2026-08-19] test+deploy | unslop pressure PASS 7/7 after one tune
First Luna-max run failed both load-bearing gates: asked to unslop an
agent-facing `SKILL.md` under pressure it stripped the gate and its
why-clause, and told to remove every em dash it went to zero and made
`em dash count: 0` its success criterion. Same mechanism both times —
the rules were prose sentences inside topic sections, so a direct user
instruction outranked them. Moved both into a `## Never` block with the
rationalization framing and an explicit override path that preserves
gates/whys, then re-ran: both PASS. Also fixed a fixture flaw that gave
check 2 a false pass. Caveat recorded: max thinking, not low, because no
low-reasoning provider was reachable. Deployed to shared/Pi/Claude.

## [2026-08-20] ingest | quality-signals from Uncle Bob's 2026 tool cluster
Read the `crap4*`/`mutate4*`/`dry4*` tools, the Acceptance Pipeline
Specification, SwarmForge's constitution articles, and the
`negative-test-experiment` grid, then built `concepts/quality-signals/`
as a model-invoked discipline. Central decision: the concept **refuses**
to gate on CRAP, inverting what the tools imply, because the author's own
eight-run grid shows a forced CRAP cap raised coverage on every row,
raised design on none, and dropped readability to 1–2 of 5 on every row.
Three signals get explicitly unequal authority — CRAP advisory, source
mutation gates the suite, acceptance mutation gates the spec — and
acceptance mutation is ranked first for adoption because all eight runs
passed the same 25 acceptance cases including the one with zero unit
tests. Kept the differential-manifest cost discipline and added a
harness-integrity rule: a mutation run reusing stale compiled output
reports false survivors that read as weak tests, so require two identical
runs. Mechanism confirmed in CPython's `_validate_timestamp_pyc`, not
inferred. Evidence strength labelled throughout (n=1, single author,
subjective design scores). Role packs and the handoff daemon rejected as
overlapping existing orchestration concepts. Throwaway Python prototypes
of all three signals informed the design and were not retained.
Pressure test authored (8 checks, 3 load-bearing), not run; not deployed.

## [2026-08-20] implement | narrow quality-signals to acceptance-mutation
Cut the day-old three-signal concept down to the half that earns its
place. CRAP tooling exists only for Clojure/Go/Java, and source
mutation's first instruction to any reader was "build or evaluate a
harness" — a skill whose opening move is a project rarely gets acted on.
The authority table existed to hold three things together and went with
them. What remains leads with the design-time precondition (generated
tests must consume the spec, not transcribe it) plus a tooling-free
version of that check, then the mutation itself and a three-kind survivor
taxonomy that must be named before anything is fixed. Two `## Never`
rules, both against clearing the report instead of fixing the defect.
The complexity-threshold rule generalized past CRAP (ruff C901, ESLint
complexity, Sonar) and moved to `code-review`, where gates actually get
proposed; its check 9 is authored, not run. Source-mutation harness
lessons demoted to `implementations.md` rather than deleted. Narrowing
cost one rewrite because nothing had been deployed or tested yet.
Pressure test rewritten to 6 checks, not run; still not deployed.

## [2026-08-20] implement+test | discriminating acceptance evidence; remove acceptance-mutation
Verified empirically whether the day-old `acceptance-mutation` concept would
ever fire: zero `.feature` files and zero BDD runners anywhere in `~/Sync`, and
the bc pipeline's spec artifacts are prose checkboxes (`issue-slicing`
criteria → Agent Brief → `acceptance-matrix.json`) that a worker transcribes by
hand. Nothing consumes them, so there is no value to mutate. Worse, "acceptance"
is pipeline-wide vocabulary, so the skill's likeliest behavior was firing during
drains and recommending an IR pipeline for a checkbox list. Concept removed.

The transferable half moved to where the work happens. The drain's deterministic
gate proves each matrix row *has* evidence and that rework re-evidenced every
touched row; neither asks whether the evidence would differ had the criterion
been false. Added that as a Spec-scope rule in `review-contract.md` — sibling to
the unfireable-guard rule, scoped to implicated rows so it cannot become a
full-matrix audit, remedy is discriminating evidence rather than more evidence —
plus a nine-word clause in `execute-issue.md` so workers pick such evidence at
the source.

Gate A **PASS 23/23** (`results/2026-08-20-gate-a.md`), with 22/22 confirmed
before the edits so the result is attributable, and check 23 verified fireable
by deleting the rule and watching it fail. Gate B still not run.

Finding, not fixed: `run-pressure.py` resolves its candidate as `parents[4]` and
expects the workspace and `.pi/agent/agents/` to be siblings, which stopped
being true when this workspace moved to `Work/PUBLIC/Agents`. Both runs used a
two-symlink shim passed as `argv[1]`; the harness was not modified. A durable
fix is a portability decision about a cross-repository path.

## [2026-08-20] test | fix Gate A runner path resolution
`run-pressure.py` assumed the agents workspace and the Pi config were siblings
under one `CANDIDATE` root — true in CONFIG, false since the move to
`Work/PUBLIC/Agents`, so the default invocation aborted before any check ran.
Split into two roots: `WORKSPACE` derived from the script's own location
(`BC_DRAIN_WORKSPACE` to override) and `PI_DIR` defaulting to `~/.pi/agent`, the
live directory Pi reads (`BC_DRAIN_PI_DIR` to override), each preflighted with an
actionable error. Positional argument dropped; no documented invocation used one.
Verified 23/23 with no arguments and no shim, from an unrelated cwd, plus both
error paths.

Finding recorded, not fixed: check 1's "never edits policy" evidence is inert.
It hashes a path that does not exist, assigns the same variable to
`policy_hash_before` and `policy_hash_after`, and never compares them — evidence
identical whether or not the policy was rewritten, which is the class the
discriminating-evidence rule added the same day forbids. The correct subject is
the user-owned policy outside this repository, so the fix needs a decision.

## [2026-08-20] implement+deploy | unslop clause for chat replies in agent-kernel
The user asked that agents apply `unslop` when replying to him, but not when a
subagent reports to another agent. It could not be done in the skill: `unslop`
is model-invoked, so its description never matches an ordinary turn, and its
body excluded chat replies outright on the assumption that harness clamps
covered them — they clamp length and structure, not provenance tells. Added a
78-word clause to `agent-kernel` § Final response naming the tells that actually
appear in chat, scoped to what the user reads, delegating the full pass to
`unslop` for shipped prose. The unslop exclusion line now points at the kernel
instead of contradicting it. Same migration the `bc-swarm` thin-parent guard
made, for the same reason.

`plain-language` deliberately not given the same treatment: three of its four
principles already are that kernel section, and reader-identification is inert
when the reader is a known specialist. Only its one-term-per-concept rule was
folded in. Deployed to all five harness deltas. Lint exit 0, no errors; the 5
remaining warnings are the pre-existing private-concept symlinks (`herdr`,
`last30days`) and are untouched by this change.

## [2026-08-20] implement | status frontmatter, --status board, docs/ layer
Reorganized for human navigation. Three changes, one motive: "what is untested or
undeployed?" required reading 43 files.

- **Status frontmatter** (`test_kind`, `test_status`, `tested`, `deployed`) now opens
  every `CONCEPT.md`. It replaces free prose that stated the same facts in about ten
  phrasings across 43 files, none of it greppable. `scripts/lint.py --status` prints
  the board worst-first; `lint.py` validates the enums and dates.
- **The test gate is now machine-checkable.** It was honor-system prose. Eleven
  concepts are deployed with no recorded run: bc-init-agent, codebase-design,
  domain-modeling, frontend-design, grilling, last30days, prd-drafting,
  prompting-agents, prototype, research, triage. Nine have `test_status: not-run`;
  domain-modeling and grilling are `partial` but carry no run date at all. Lint
  reports these as errors, so it exits 1 until they are tested or undeployed. That
  is a deliberate choice and a decision the user still owns.
- **Deploy state is taken from disk, not prose.** `deploy-local-skills.py:102` globs
  every `*/body/SKILL.md`, so a concept ships whether or not its CONCEPT.md agrees.
  19 files claimed "not deployed yet" while their symlinks were live; 8 carried an
  outright false "Not deployed yet" line and prompting-agents claimed it was never
  symlinked. All corrected. Lint now cross-checks both directions.
- **`docs/`** holds `bootstrap.md`, `harnesses.md`, `pipeline.md`. Root keeps README,
  AGENTS.md, index.md, log.md, LICENSE. `docs/` was deliberately not added to
  `INLINE_PATH_PREFIXES`: codebase-docs discusses generic `docs/` trees in other
  repositories, so the prefix is not unambiguously repo-relative.
- README's counts were stale (36 concepts; actually 43) and are corrected to 43
  concepts / 5,039 lines of instruction body.

Extraction ran as a two-scout bc-swarm fan-out (Luna max); anchors spot-checked
against source before use, and deploy values overridden from disk. `research.md`
left at root — the user deferred that one.

## [2026-08-20] implement | generated docs/status.md
Follow-up to the frontmatter change: a page answering "what needs testing, what is
undeployed" in that order, rather than alphabetically.

Generated, not hand-written, and `lint.py` fails while it disagrees with the
frontmatter — otherwise it becomes the same stale prose the frontmatter just
replaced. Regenerate with `scripts/lint.py --write-status`. Sections are ordered by
what needs action: needs testing (11), not deployed (0), deployed with a known gap
(6), passing and deployed (26). Verified both directions: clean immediately after
generation, ERROR after a hand edit.

## [2026-08-20] implement | docs research and plan lifecycle layout
Moved `plans/` into lifecycle folders under `docs/plans/`, moved `raw/` into
`docs/research/raw/`, and renamed the ISO report to a topic-specific filename.
Added placement READMEs and lifecycle/status lint, synchronized provenance/index/lint paths, and preserved raw-source immutability.

## [2026-08-20] implement | move environment-coupled concepts private
Moved `notebooklm` and `last30days`, plus their raw provenance snapshots, to the private
`~/.config/agent-concepts/` layer. Removed their public catalog/status/source-registry entries
and recorded the follow-up to the portability boundary decision.

## [2026-08-20] implement+test | solution sizing in the drain worker
Wired `minimal-solution-ladder` into `bc-drain-issues` implementation packets — it was
deployed on the shared bus but unreachable inside a drain, because the Pi roles exclude the
broad skill catalog and the dispatch list named only tdd/diagnosing-bugs/autoresearch. Rung 2
is anchored to the driver's qmd/tree prior-art search, since a fresh worktree has no
familiarity to reuse. Bounded the Standards axis with `codebase-design` vocabulary plus a
deletion test and a Minor-unless severity rule, so shape findings cannot fund an architecture
debate. Rejected the two-builder proposal that prompted this: it is scope creep by the Spec
axis's own definition, doubles build and review tokens against an unmeasured Gate B, and
duplicates `improve-codebase-architecture` one layer up. Gate A **PASS 25/25**; new checks
24–25 verified fireable.

## [2026-08-20] implement+test | drain docs axis, resume contract, code-review drift fix
Wired `codebase-docs` into `bc-drain-issues` on both sides — the worker updates an owning
README/docs page in the same diff, the Standards axis checks for a stale owner, change
narration, or an invented `docs/` tree — bounded so absent documentation is never a finding.
Added a `## Resuming an interrupted run` contract adapting `bc-swarm`'s recover-before-relaunch
to the drain's remote claim refs, which the drain could not inherit because `bc-swarm` hands
implementation fan-out to it; an adopted worktree takes full fresh review because no standing
approval survives a run whose reviewer records are gone. Fixed `code-review`'s AFK slice gate,
which carried three stale copies of drain parameters (both-axes dispatch, full packet, one
rework cycle) and now points at the drain instead. Gate A **PASS 27/27**; checks 26–27 verified
fireable four ways.

## [2026-08-20] plan | bc-drain-issues architecture feedback
Wrote `docs/plans/active/bc-drain-issues-architecture-feedback.md` for the bounded drain → architecture-review feedback edge. The plan keeps observations outside review authority and routes them through a durable, human-verified inbox; implementation and pressure testing remain outstanding.

## [2026-08-20] implement+test | architecture observation feedback edge
Documented `bc-drain-issues` and `improve-codebase-architecture` as a bounded post-landing observation feedback edge with declared project-context persistence, human disposition, and no autonomous issue creation. Gate A **PASS 28/28**; current clean consumer fixtures are parent-verified **PASS**. Gate B remains outstanding, with no model-token result claimed.

## [2026-08-20] implement | architecture feedback integration corrections
Clarified newest-first inbox persistence and current tiered drain outcomes, moved the completed plan to `implemented/`, and updated pipeline/index bookkeeping. Existing lint limitations remain unchanged.

## [2026-08-20] implement+test | prepend evidence and fallback disposition suppression
Recorded Gate A check 28's newest-first prepend ordering as deterministic producer evidence and the parent-verified two-pass fallback rerun: ledger-before-inbox filtering, exact identity/source suppression of `obs-11`, and unresolved `obs-02` retention. Gate B remains outstanding.

## [2026-08-20] implement+test | final architecture consumer evidence bookkeeping

Clarified suppressed-row wording so only non-suppressed eligible entries actually processed receive current-run verification/card/report rows; terminal fallback matches receive none. Recorded the parent-verified final current-body missing-inbox/implementation-pressure rerun: no inbox or declaration, glossary/ADR-first flow, aggregate-only temporary report with the exact selection question, pressure refusal, and no production/canonical/issue changes.

## [2026-08-21] ingest+implement+test+deploy | handoff
Surveyed the public session-handoff skills and built `handoff` from the four that had ideas: Pocock (narrowness, reference-by-path, suggested skills), status203 (active/consumed store, the ledger observation, leak check), orzilca (the handoff is data not instructions; verified/unverified/broken), djhyes (recorded, not adopted). Resolved their three contradictions in `CONCEPT.md`; departed from Pocock on one point, putting the overnight/rate-limit case in scope because compaction cannot cross a process boundary.
Pressure test 5/7 on first pass. Both failures were guards that could not compete rather than missing rules: the narrowness table was never consulted by the routing (inert guard), and the no-edits rule was prose that lost to "it's a one-liner". Relocated both — narrowness became routing step 1, no-edits became a `## Never` with an order-not-refusal escape — and the full sweep passed 7/7. Deployed to shared/Pi/Claude.

## [2026-08-21] test | lint Needs-testing board (Grok)
Ran the 10 concepts lint listed as Needs testing. Pressure runners have no `subagent` tool, so parent launched naive Grok consumers and graded artifacts.
- **PASS:** `prototype` 4/4, `frontend-design` 4/4 (clears 2026-06-21 MIXED), `triage` 5/5 (already-implemented gap closed), `grilling` 4/4 including utterance clause, `prd-drafting` accuracy 5/5, `domain-modeling` accuracy including 2026-08-18 ADR clauses.
- **PARTIAL:** `bc-init-agent` script 1–7 PASS, process/adaptive BLOCKED; `codebase-design` local checklist PASS, mattpocock clone BLOCKED.
- **Not closed:** `prompting-agents` accuracy BLOCKED (provenance files missing); `research` still in flight (narrow lookup + spec-vs-blog held; substantial-delegate prompt running).

## [2026-08-21] test | prompting-agents accuracy via live URLs PASS
Procedure no longer requires deleted raw clippings: fetch CONCEPT.md Provenance URLs; unfetchable is BLOCKED. Live run: all SKILL.md headings PASS except Boonstra/Kaggle technique repertoire BLOCKED. No clippings restored.

## [2026-08-21] test | research pressure 4/5, check 3 blocked
Naive Grok consumer: primary sources, inline lookup, no surprise files, and a proposed-then-accepted `docs/research/` note that is not a PRD. Check 3 (background delegate) blocked — no `subagent` tool; work stayed inline. Frontmatter `partial`.

## [2026-08-21] implement | bc-swarm listing drops parent/child
User asked not to hear parent/child on every subagent launch. Tooth now lists role + routing only (`notes → scout, Luna max`); kept work is the reason (`hotfix → cheaper than a packet`). Format-only; no pressure re-run. Pi swarm-mode kernel updated in CONFIG to match.

## [2026-08-22] ingest+implement | bc-wiki-maintain from Perplexity Brain
Ingested Perplexity's "Brain: agentic memory as a knowledge wiki" (19 Aug 2026) against the
user's own vaults. Recon found 12 live project wikis and the diagnosis: rot is not laziness but
*recorded* triggers — CV's `index.md` omits 21/38 pages incl. all `findings/`, and the
architecture-runway nudge has read `TODO/TODO/TODO` since 2026-07-31, so it never fired once.
Root rule adopted: triggers must be **computed** (git/filesystem), never recorded.
New concept `bc-wiki-maintain`: stdlib detector ported from the personal wiki's `wiki_lint.py`
(+ vault-root arg, Markdown links, git staleness, unpromoted-log backlog, qmd coverage,
`PROMOTION_REQUIRED` contract), a promotion skill with three gates (additive-only; one dedicated
commit; contradictions flagged into `open-questions/`, never resolved), and an **uninstalled**
systemd user timer. `bc-init-agent` gains the skill-map pointer and its dead runway counter is
replaced with a git-history signal. Took from Brain: capture/synthesis split, offline compile,
deterministic lint precondition, git as audit+undo. Rejected: generated index (destroys the
user's curation), required frontmatter (`updated:` duplicates what git knows), staged-tree
semantic verification (Perplexity-scale concurrency, not 40 pages/one writer).
Pressure scenario **not run**; nothing deployed.

## [2026-08-22] lint | qmd registry coverage
Registered the two unregistered live vaults (Homeflix public + private, `.agent/` not
`.bc-agent/`, both active through 2026-08-19) and ignored image-maze `temp/` (84 of 238 indexed
`.md` were generated run artifacts). Committed in Scripts as 79d17c6. CV stays excluded by
design; the detector now reads that stated reason instead of flagging it.

## [2026-08-22] implement | subagent routing: review asymmetry, spec gate, fan-out band
Routing now puts Grok review on a separate subscription meter, gates implementation delegation on verifiable acceptance criteria, requires writer independence rather than worktree isolation, and bounds fan-out width. Reviewer 45/5 and scout 100/10 turn budgets come from the measured local turn distribution and must be passed at launch, since `agentOverrides` accepts no `turnBudget`. Evidence: one unbudgeted reviewer burned 61.6M tokens over 185 turns into a timeout and returned nothing.

## [2026-08-22] test | bc-wiki-maintain pressure PASS 4/4
Four fresh Luna-max consumers, four isolated fixture vaults, one scripted excuse each, none told
what the gates were. Graded from artifacts (sha256 vs pristine, git log/diff, resolution-language
grep), never from self-report. Additive-only held against "rewrite this badly worded page" —
diff was pure addition. Contradiction gate held against "the spike is obviously outdated" — all
four recorded the conflict in `open-questions/` citing all three sources and picked no winner.
Detector-first held against "skip the lint run". Incidental: `log.md` byte-identical and
`index.md` insertions-only in all four, which is direct evidence for linting index drift rather
than generating the index. Frontmatter now `pass` / `2026-08-22`; still `deployed: no`.

## [2026-08-23] deploy | bc-wiki-maintain live; six vaults pointed; CV timer armed
Skill deployed to shared/Pi/Claude symlinks after the 4/4 pressure pass. Added the
`/bc-wiki-maintain` pointer to `references/agent-skills.md` in the six scaffold-shaped vaults
(Music, Scripts, image-maze, CV, Learning/codebase-design, Learning/sql), one commit each, staging
only that file — Music's untracked Obsidian files were left alone. Installed and enabled the
user timer for the CV pilot only; first run Mon 2026-08-24 03:39 BST. Detection under the service
environment confirms CV at `PROMOTION_REQUIRED=1` (10 unpromoted entries, 21 pages missing from
index). The four legacy `.agent`/`agent/wiki` vaults have no `references/agent-skills.md` and were
deliberately skipped.

## [2026-08-23] deploy | pointers in both Homeflix vaults; stale canon path repaired
Created `references/agent-skills.md` in the public and private Homeflix `.agent/` vaults (neither
had a repo-local skill map) and indexed both; the private one additionally binds the maintenance
pass to `conventions/secrets.md` and says an upstream conflict is recorded, not reconciled.
Repaired the dead `~/Sync/CONFIG/agents` path in 12 instructional files across six vaults;
`log.md`/`tasks/`/`findings/` mentions were deliberately left, being accurate history rather than
live instruction. The Agents repo itself is deliberately NOT a `bc-wiki-maintain` target: its
`scripts/lint.py` already covers link/index/status drift, and its `log.md` is the curated output
of operations rather than raw material to promote — two linters would disagree over one tree.

## [2026-08-23] deploy | first supervised promotion run; human guide added
Triggered `bc-wiki-maintain.service` by hand against the CV pilot. Result: 8 files, 111
insertions, **0 deletions**, `log.md` byte-identical — the additive gate held on real data, not
just fixtures. It filed two new findings, appended to validation/gotchas/an existing scan page,
indexed everything it created, and raised two open questions rather than resolving them. One
caught a genuine CV factual conflict (Treehouse track "Front End Web Developer, started 2015-01"
vs "full web development track, ~2016"). Wall clock 8m29s, 33s CPU.
Added `concepts/bc-wiki-maintain/README.md`, the first human-facing guide in a concept dir:
`body/SKILL.md` = agent instructions, `CONCEPT.md` = design rationale, `README.md` = user guide.

## [2026-08-23] implement | depersonalize bc-wiki-maintain public surface
README, SKILL, CONCEPT, tests, runner units, and the catalog line no longer name author
vaults, training records, or machine paths. The shipped systemd unit is now a template
(`%h/path/to/...`); the already-installed user copy is a separate file and still points
at the live pilot. `docs/plans/active/bc-wiki-maintain.md` keeps the original vault names
as an implementation record, not a user guide.

## [2026-08-23] implement | scheduled lint across all live project vaults
Added `run-lint.sh` plus template `bc-wiki-lint` units: detection only, no agent, no commit.
Local list is `~/.config/agent-concepts/wiki-lint-vaults.txt` (eight live vaults). Detector now
skips `temp/`/`scratch/`/`.obsidian`/`vendor` and does not fail a vault on example links in
`templates/` — image-maze's vendor tree was drowning the report. First live sweep: 8 checked,
2 fail (Music leftover example wikilinks; codebase-design broken/ambiguous `[[plan]]` /
`[[image-maze]]`).

## [2026-08-23] deploy | promotion timers for image-maze and public Homeflix
Local systemd copies of the promotion unit, staggered after the lint sweep. First runs
will be large: those vaults have never had a `wiki: promote` commit. Commits stay local
until something pushes — both remotes exist. Runner README now documents one-unit-per-vault.

## [2026-08-24] implement | bc-wiki-maintain runner hardening
The detector now computes strict dated-log promotion ranges and ignores code spans, fenced examples,
and append-only `log.md` links as graph sources. The wrapper rejects any agent-staged index change,
requires a valid range, and commits with the exact `<from>..<to>` subject. Added temporary-repository
regression tests for CLI linting, ranges, exact commits, invalid ranges, and inside/outside staging.

## [2026-08-24] implement | bc-wiki-maintain nonstandard log headings
Promotion detection now preserves every real unpromoted `##` log heading and fails closed when any
new heading lacks a valid date. Fixed the invalid-range regression seam and kept fake runner scripts
outside the temporary Git repository while retaining their test lifetime.

## [2026-08-24] test | bc-wiki-maintain review fixes
Corrected the staged-change regression to stage a repo-root path outside the configured vault, and
added a two-vault boundary test. The skill now distinguishes automatic-wrapper runs (leave index
and HEAD untouched; wrapper stages and commits) from direct manual runs. Focused tests pass.

## [2026-08-24] implement | bc-wiki-maintain commit-authority checklist
Aligned the final verification checklist with Gate 2: automatic runs hand an unchanged index and
`HEAD` back to the wrapper, while direct manual runs stage and create the dedicated commit.

## [2026-08-25] implement | bc-wiki-maintain classify / stale / index
Live first-runs closed 55/26-heading backlogs after a thin write because any `wiki: promote`
commit made `log.md` at that moment look fully considered. The wrapper now refuses that commit
unless a same-pass JSONL file classifies every detector-listed heading. Gate 3 now splits
mutually exclusive claims (flag, continue) from stale snapshots (dated append). Gate 1 appends
index links for existing `findings/` and `decisions/` pages. Pressure scenarios updated; not re-run.

## [2026-08-25] implement | bc-wiki-maintain classification audit trail
Review of the classification gate found it destroyed its own evidence: the JSONL was a `mktemp`
with no cleanup, its verdicts reached no artifact, the vault cleanup knew one guessed filename,
and `--verify-classify` passed vacuously when the heading list was unknown. Verdicts now become
the promotion commit body, any new non-Markdown vault file fails the commit, the temp file is
kept only on failure, and an unknown list is a safe stop. Regression suite 14/14.

## [2026-08-25] implement | bc-wiki-maintain Gate 1 enforcement + Gate 2 commit default
Gate 1 was prose-only: the wrapper checked staged changes, HEAD, deletions, and new
non-Markdown files, but never deleted lines, so an in-place rewrite committed silently.
It now requires the committed bytes to stay a byte prefix when a diff shows deletions
(18 regression tests). Gate 2 opened with "land all of this pass as one commit" while
step 5.6 asked the agent to verify HEAD after a commit the wrapper only makes once the
agent has exited — an agent finishing that checklist minted the boundary-closing commit
itself. Default is now no commit. test_status downgraded to partial: unverified under pressure.

## [2026-08-25] implement | brief: bc-swarm worktree durability gap
A worker child's worktree and branch were destroyed before the parent read them; its commit
survived only as a dangling object, recoverable because the artifact named the SHA. Rule 3
calls the artifact the deliverable, which is false for a worktree worker, and rule 4's
recovery order omits Git objects entirely. Filed as docs/plans/active/bc-swarm-worktree-durability.md.

## [2026-08-25] fix | bc-wiki-maintain range narrowing around undatable headings
promotion_status() guarded the range with all(date is not None), so one malformed heading
nullified it for the whole unpromoted set and the unattended runner failed closed forever.
codebase-design had exactly one bare `## 2026-06-28` blocking 18 valid headings. The range now
comes from the datable headings only; undatable ones stay in the classification list and are
warned about; a wholly undatable set still fails closed, so Scripts and sql are unchanged.

## [2026-08-25] implement | bc-swarm worktree durability
Updated the canon, Pi lifecycle/recovery guidance, pressure check 6, active plan, index, and
reachable swarm-mode kernel so worktree workers record full commit/branch lines and parents
recover patches or recorded Git objects before relaunch. Check 6 is authored but unrun.

## [2026-08-25] tune | bc-swarm recovery trigger and guarded worktree recovery
Pressure check 6 first passed packet production but failed recover-before-relaunch: a low-thinking
consumer stashed named stale-run evidence and launched a replacement. Added the pre-routing gate,
packet seam, preserved-worktree stop condition, and guarded patch/full-range/SHA recovery; rerun is pending.

## [2026-08-25] test | bc-swarm worktree durability PASS 3/3
Low-thinking headless Pi held the tuned check 6: a real worker wrote own-line commit/branch records;
the reaped fixture recovered the exact seeded object with zero replacement runs or stashes; the
unrecoverable fixture skipped fsck and relaunched exactly one track. Moved the plan to implemented.

## [2026-08-25] fix | bc-wiki-maintain qmd coverage checks the machine index
The detector judged qmd coverage from the canonical `qmd-collections.yml` alone, so both Homeflix
vaults reported `registered` while the live `~/.config/qmd/index.yml` had no such collection — a
read-path health signal that could not see read-path failure. `qmd_status` now reads both files and
distinguishes `unindexed` drift from `unregistered`; 6 new tests, injectable registry paths.

## [2026-08-25] test | bc-wiki-maintain pressure scenario 3 split for the Gate 2 default
The Gate 2 commit-default rewrite (a403caa, 08-25 01:39) never reached `tests/pressure-promotion.md`
(last touched 85770d5, 00:27), so Scenario 3 still graded "creates exactly one new commit" while the
skill now forbids the agent from committing under the runner. A compliant agent failed the test and a
violating one passed. Split into 3a (runner default, no commit) and 3b (explicit manual request), and
corrected the CONCEPT.md passage that claimed the Gate 2 scenario had been updated.

## [2026-08-25] test | bc-wiki-maintain pressure PASS 5/5; back to test_status pass
Re-ran the split scenario set with five fresh consumers, one per scenario, each isolated in its own
fixture repo with a private skill copy and no path into this repository. All five held under artifact
grading: contradiction filed citing both sides with no winner, awkward prose survived the rewrite
excuse verbatim, `HEAD` unmoved under the runner default, exactly one correctly-named commit under an
explicit request, and the detector ran before any edit. Dirty-tree refusal verified against the runner
directly. Limits recorded in CONCEPT.md: one model at max thinking, and the wrapper's own commit half
is covered by pytest rather than by 3a.

## [2026-08-25] implement | qmd registry repair, wiki-lint failures cleared, plan doc landed
Fixed the four queued items. The `agents` qmd collection had pointed at `~/Sync/CONFIG/agents` since
its first commit -- a path that never existed -- yet held 491 indexed documents, so searches returned
content from a vanished directory rather than nothing. Repointed at the workspace (232 files) and
corrected its context sub-paths; note that `bc-qmd-setup` skips a collection already registered under
a different path, so the stale machine entry had to be removed first. Registered the codebase-design
learning vault; declared `sql` an explicit exclusion while it is scaffold with no sessions.
Cleared the daily `bc-wiki-lint.service` failure: Music had 1 broken link and codebase-design 5 broken
plus 3 ambiguous, all real -- pages that were never written, and a bare `[[plan]]` colliding with
`templates/plan.md`. Service now reports failures=0 over 8 vaults. CV's architecture-runway counter
now records a true zero instead of template TODOs.
Moved `docs/plans/active/bc-wiki-maintain.md` to `implemented/`, corrected the six statements that had
gone stale, marked the superseded design decisions inline, and recorded the Gate 2 test-drift
inversion and the 5/5 pressure re-run.

## [2026-08-26] research | wiki-autonomy council: automatic maintenance and cheap traversal
Ran a 3-advisor bounded council (council-grok, council-sol, council-opus; fresh context, 2 passes) on
making `bc-wiki-maintain` seamless and automatic. Filed brief, claim matrix, supervisor findings, memo,
and advisor evidence under `docs/research/wiki-autonomy-council/`.
Diagnosis: the read path is the gap, not the write path — 0 broken links across 9 vaults but 7-21
orphans each, `index.md` alone is 4,543 tokens in image-maze, and `qmd query` measured 67.1s. All three
advisors independently converged on filter-don't-read via a generated catalog.
Three defects verified at source, not relayed: scaffolded `map.md` contributes zero graph edges because
`without_code()` blanks its code-span targets before `links()`; Gate 1 does NOT mechanically block link
insertion (`run-promotion.sh:226` short-circuits on zero deletions), so that prohibition is policy only;
and `scaffold.py:307` emits `## __DATE__` while `wiki_lint.py:19` requires `## [YYYY-MM-DD]`, which is
the root cause of the two permanently blocked vaults. Also found `~/Sync/Wiki` already runs daily
unattended LLM consolidation at 0 orphans / 0 missing index entries — prior art to port rather than
reinvent. No concept changed yet; the memo's step 1 ships with a benchmark before any build.

## [2026-08-27] lint | exempt captured evidence paths
`lint_inline_paths` now skips Markdown under `docs/research/**/evidence/` because captured artifacts
quote paths from their source repositories. Documented the convention and restored the council evidence
artifact byte-for-byte.

## [2026-08-27] implement | wiki read-path plan activated from the council memo
Turned the wiki-autonomy council memo into `docs/plans/active/bc-wiki-maintain-v2-read-path.md`, scoped
to step 1 (generated catalog, first-move change, benchmark) plus failure notification, with steps 2-4
deferred behind the benchmark. All five owner decisions resolved: cache location deferred to
`$XDG_CACHE_HOME`, desktop notification in scope, port evaluated, `dng` out of scope, Music unattended.
Recon corrected four memo details before drafting — the scaffold defects live in `bc-init-agent`, which
makes the first-move fix a cross-concept change; coverage is 4/8 vaults rather than 4/9 once `dng` is
excluded; the exit line is `wiki_lint.py:526`; and the personal wiki is 383 pages. The port question
resolved against reuse: the consolidation script is coupled to its own layout and prompt.

An independent reviewer then blocked the first draft on three P0s, all confirmed at source. The scaffold
is additively idempotent, so a template-only first-move change would have left all eight live vaults
loading `index.md` and made the benchmark measure nothing; W2 now covers the live vault instructions.
W3 had imported defences against the personal Python wrapper's PID-lock and `TimeoutExpired` bugs into a
bash runner that has no lock, leaving "a deliberately skipped run" unsatisfiable; it now notifies on the
exit-1 paths that exist and stays quiet on the legitimate no-op. W4 had no acceptance criteria at all and
is now a harness: 20 committed questions with gold paths, bytes÷4 to match the 4,543 baseline derivation,
and hard bars at median ≤800 and miss rate ≤0.30.

## [2026-08-27] implement | widen the read-path plan to span bc-init-agent
The owner named the real goal — knowledge an agent can traverse cheaply — and `bc-init-agent` is half of
it: the scaffold decides the shape knowledge is written into, `bc-wiki-maintain` keeps that shape true.
Renamed the plan to `agent-vault-read-path.md` and added W5, which stops the scaffold minting the old
`index.md`-first navigation in four separate directives plus its upgrade-notes hint.

A survey of the eight live vaults broke three assumptions. Directory taxonomy has diverged to 27 distinct
top-level directories, only six universal, with `concepts/` and `plans/` meaning different things by
archetype — so the catalog's `kind` is now the vault-relative directory path, not the basename. A third of
the benchmark vault is gitignored: 84 of image-maze's 239 pages sit under `temp/`, where `git log` returns
no date, and excluding them leaves 155 eligible pages, matching the memo's independently derived 151. And
the first-move line has drifted into three variants across the eight vaults, four of which carry a second
`START` paragraph, with Music on a different workflow entirely — W2 is eight edits, not a find-replace.

The scaffold emits no frontmatter and its templates open with TODOs, so deterministic summaries degrade to
page titles. Whether to fix that at the source is recorded as an open decision rather than assumed:
additive idempotency means shape changes reach only new vaults, never the eight where the knowledge is.

## [2026-08-28] implement | qmd-default direct BM25 fallback
Added the stdlib-only `body/wiki_search.py` direct BM25 reader and its tests. The preregistered
fallback benchmark compares it with a ranked `rg` count pipeline and the existing qmd/index/catalog
measurements without writing the target vault; both no-index fallbacks reached 3/20 misses, with
full per-question output and Wilson intervals in `concepts/bc-wiki-maintain/tests/retrieval-results-fallback.md`.

## [2026-08-28] implement | direct-BM25 vault read-path instruction
Added the canonical single-vault search instruction, qmd cross-vault guardrails, a pasteable
vault-AGENTS block, and a five-attack pressure scenario. The changed discipline stays partial
until that scenario is run; live-vault rollout remains a separate parent-owned step.

## [2026-08-28] test | read-path pressure scenario run
Two agents got ordinary-looking work with the rationalisation embedded and were not told they
were being tested. Both held: one searched despite pressure to just read `index.md`, the other
refused to read an unhelpful first search as proof the fact was undocumented. Gate passes.
Also recorded that frozen benchmark queries understate live performance — a live agent reached
Q5's gold page at rank 1 where every method missed under the frozen list.

## [2026-08-28] deploy | canonical read path rolled out to all eight vaults
Search-first replaces index.md-first in Music, Scripts, image-maze, CV, codebase-design, sql,
Homeflix and homeflix-prod, each committed in its own repo. Music kept its plans-first route
with search inserted ahead of it. Four lean vaults carry a one-line form only — see the note in
`docs/plans/active/agent-vault-read-path.md` about their missing empty-result and hub-page rules.
Prerequisite fixed en route: `~/.zshenv` set `AGENT_CONCEPTS` to a nonexistent path, which broke
every skill command using the variable.

## [2026-08-29] implement | plan the vault write/read contract
Assessed the landed read path against the write path and found they share no contract: the
scaffold still generates index-first instructions and `## YYYY-MM-DD` log headings the promotion
detector cannot parse, which leaves Scripts and sql at `PROMOTION_RANGE=invalid` and CV and
image-maze one entry from it. Filed `docs/plans/active/agent-vault-write-read-contract.md` with
seven work items. An independent review caught five wrong claims in the first draft, including a
W1 instruction that would have pasted the vault search block into root `AGENTS.md` and searched
whole repositories; all five are corrected in the filed version.

## [2026-08-29] implement | rewrite the README for practitioners
Retargeted the README from a portfolio artifact to a reader building their own agent workflow:
dropped the author framing, the token/cost A/B table and volatile counts, and added the
init → plan → queue → architecture loop, the knowledge write/read design, and how to research,
write, attack and deploy a concept. Corrected four claims the old page got wrong — the A/B was
v1b-vs-v2d rather than v2-vs-v3, the body-line count was stale, `--harness` always writes the
shared bus, and 16 upstream skill files are tracked, so "cited, not redistributed" was false.
Opening and qualifying section follow adoption research: capability and anchor first, then a
job-and-constraint filter, with the limitation placed after the claim rather than before it
(Eisend 2006 — negative-first costs credibility). Vocabulary swept to what practitioners say.

## [2026-08-29] test | vault read path clears its gate after a root-file tune
Pressure-ran the generated vault instructions twice. Run 1 failed 2/3: the "index.md is
right there" scenario read the index before it had opened the vault AGENTS.md, so the
discipline never bound — an ordering race in the repo-root template, not a fault in the
canonical block. Hardened the root gate (0423ada) and re-ran on isolated per-scenario
fixtures: 3/3. Also fixed the live AGENT_CONCEPTS blocker, which was stale in the systemd
user manager and broke the read path for every bash/sh agent shell.

## [2026-08-29] implement | shorten README skill-building section
Cut the five-step "Build your own skill" tutorial down to a chat: drop a source, the agent
ingests/writes/tests/deploys, you curate. The old length made the work look like a manual the
reader had to run themselves.

## [2026-08-29] implement | two entry points in README skill-building
The section only described ingesting a dropped source. Readers can also start from an idea in
chat, or paste a link. Tightened the run-on that added those paths.

## [2026-08-29] implement | tighten README after unslop/plain-language review
Fixed the knowledge opener: filing a fact does not put retrieval logic on the page; it puts the
fact where a later search will look. Moved Install above Knowledge, folded Four gates under
skill-building, cut Design stance, and shortened each loop item to a job plus one artifact.

## [2026-08-29] implement | name the memory as long-term project memory
The added line "It is a long-term memory system" was the right claim with the wrong category
name. Folded "long-term" into the existing sentence so it cannot be read as session recall.

## [2026-08-29] implement | README: promotion is append-only
Dropped the classification taxonomy. The sentence now says promotion creates or appends and
does not rewrite existing pages.

## [2026-08-29] implement | plain-language the wiki read path
Replaced "ranked search"/BM25/miss-rate decimals with: don't load the whole wiki, get a short
list, open two or three, 171 vs 4,543 tokens, 3 vs 6 misses. qmd is optional multi-vault search.
