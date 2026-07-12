## [2026-06-25] ingest | obra-superpowers skills
Created local concepts for uncovered obra-superpowers workflows (brainstorming, planning/execution, subagent orchestration, parallel dispatch, code review, worktrees, branch finishing), mapped overlapping skills into existing TDD/debugging/kernel/prompting concepts, and updated the index.

# Log

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
The previous entry's cleanup (999e220) removed symlinks that were dangling on the Mac but valid on Linux — and both ~/.claude/skills and ~/.pi/agent/skills live in synced folders, so the deletions propagated and broke find-skills/last30days/omarchy deploys on the desktop. Restored: ~/.claude/skills links to ../../.agents/skills/<name>; ~/.pi links to ../../../../../.agents/skills/<name> (relative, replacing the old hardcoded /home/ben omarchy path — the original lint complaint); deployed ~/.agents/skills/{find-skills,last30days} on the Mac. Remaining Mac-only lint danglers for omarchy are by design (Linux-only skill); lesson: a deploy symlink inside a synced dir may be dangling on this machine and valid on another — verify per-machine before deleting.
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
