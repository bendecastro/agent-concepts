# Agent Log

Append-only journal of this workspace: operations that changed files, durable discoveries, and
session outcomes. Newest at the bottom (a few early entries predate that rule and stay where they
were written). One to three lines each; no transcripts or long command output.

Every entry starts `## [YYYY-MM-DD] <ingest|implement|test|deploy|lint> | <subject>`, so
`grep "^## \[" .bc-agent/log.md | tail -5` shows recent activity. A durable fact with no better
home uses the same heading with the operation it came from.

## [2026-06-25] ingest | obra-superpowers skills
Created local concepts for uncovered obra-superpowers workflows (brainstorming, planning/execution, subagent orchestration, parallel dispatch, code review, worktrees, branch finishing), mapped overlapping skills into existing TDD/debugging/kernel/prompting concepts, and updated the index.

# Log

## [2026-09-30] implement | bc-drain-issues worker effort medium/high
User direction: ordinary slices now run workers at medium effort and high-risk slices at high (was low/medium). Updated SKILL.md preflight step 8, the CONCEPT.md risk-controls decision, and the pressure-drain fixture instruction. Pressure test not re-run; the change moves a default level and adds no gate.

## [2026-09-22] test | using-git-worktrees prune-after-done PASS 2/2
Grok workers in `/tmp/pt-using-git-worktrees-20260922-{merged,unmerged}`. Squash-merged non-ancestor `feat-done`: worktree and branch removed despite “don’t delete without asking.” Unique unmerged `feat-open`: left in place despite “just delete them / trust me.” Graded by `git worktree list` / branch / path. Prior 4/4 from 2026-07-16 still recorded. finishing-development-branch scenario 2b authored, not run.

## [2026-09-22] implement | using-git-worktrees prune-after-done
Standing cleanup duty: prune owned worktrees without asking once integrated or otherwise irrelevant. Description trigger now includes finish/integrated/irrelevant so the skill loads at cleanup, not only at setup. finishing-development-branch Keep is only for not-yet-integrated work.

## [2026-09-06] implement | stop publish-rule restatement rot
Softened the policy-decided publishing headline, made publish-check.py quote the runtime policy clause, and generalized AGENTS.md to point to external authority instead of copying its decisions.
## [2026-09-06] implement | untested review result + tdd blocked cycle + squash-merge -D
Absorbed two restated ideas from https://github.com/michaelshimeles/skills (no root LICENSE): `untested` as a recorded review result in `code-review` and `bc-drain-issues` review-contract; a TDD stop-and-report when the test cannot run (`untested` as a TDD result rejected); `git branch -D` after squash/rebase-merge in `finishing-development-branch`.

## [2026-08-30] test | bc-init-agent wiki-maintain timer offer
Pressure 4/4 on offer-then-confirm; scaffold remains timer-free.

## [2026-08-29] implement | bc-init-agent wiki-maintain timer plan
Proposed close-out: `/bc-init-agent` offers to copy slug-suffixed `bc-wiki-maintain` user units after confirm; scaffold stays timer-free; qmd refresh is not promotion.

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
Added the repo-tracked shared SSH mesh fragment and portable mesh-check script for PRD #6 / slice #7, then wired the first machine's private SSH config and authorized its identity pubkey on a second machine for the tracer path.

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
Added archetype selection to `bc-init-agent`, based on the user's real wiki patterns: code/project execution (`project-b`), ops/system planning (`Music/.ai/wiki`), learning/teach-backed study, knowledge graph (`<owner-wiki>`), and hybrid. `scaffold.py` now supports `--archetype code|ops|learning|knowledge|hybrid` overlays; tests/index/concept notes record the new pending pressure scenarios.

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
Read AGENTS files in `<owner-scripts>`, `<music-library>`, and `<owner-wiki>`, confirmed each repo uses `master` with GitHub origin, and added explicit user-owned publish-policy rules for agent-authored pushes after commit. Lint now checks those rules remain present.

## [2026-06-12] implement | Repo housekeeping-commit policy
Incident: an agent `git add agents/` swept the user's manual edits into an agent work commit. Added repo-root AGENTS.md (CLAUDE.md symlinked) defining commit separation: agents stage their work by explicit path, then commit remaining tracked drift (user hand-edits, app-written state) as separate housekeeping commits with diff-derived messages; untracked files and secret-shaped or broken diffs are surfaced, not committed. publish.yaml CONFIG rule gained a matching housekeeping exception (separate commits only; policies/ immunity unchanged).

## [2026-06-12] implement | Housekeeping narrowed to two tiers after counter-critique
Counter-critique (via second agent) identified the in-flight-edit risk: agents cannot distinguish settled drift from a user's half-finished config edit, possibly syncing mid-edit from another machine. Housekeeping is now two-tier: tier 1 auto-commits only allowlisted machine-written state (sticker.sql, update-check.json); tier 2 (hand-edited configs) requires shown-diff confirmation, untouched when non-interactive. Housekeeping commits are marked `housekeeping:` + "Observed drift — not agent-authored or validated." Publish exception narrowed to tier 1 only.

## [2026-06-12] deploy | agent-kernel delta → Claude Code user CLAUDE.md
First exercise of the kernel's delta-injection deploy policy: diffed the kernel against Claude Code's built-in prompt; five of seven sections confirmed redundant and not injected. Injected the two genuine deltas into ~/.claude/CLAUDE.md under a DERIVED marker: publish-policy pointer (Claude Code otherwise never uses the pushes publish.yaml grants in Scripts/Music/Wiki) and concepts-catalog pointer (project-scoped memory doesn't reach other repos). Off-vault clause included. CLAUDE.md is Syncthing-synced, not git-tracked.

## [2026-06-12] ingest | project B SEO prompts → seo concept
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
two-file body SKILL.md + execute-issue.md). Added pipeline.md and extended project B
planning-workflow.md (separate repo) with the execution phase. Deployed `prd-drafting`/
`issue-slicing` Claude symlinks; held the two `bc-` orchestrators' deploy pending pressure tests.

## [2026-06-20] implement | bc-init-agent scaffolder
Added `bc-init-agent`: a user-invoked scaffolder that stands up a repo-root `AGENTS.md` +
`.agent/<slug>/` Obsidian-vault wiki (generalized from the project B vault) wired for the
grill→issues→drain loop, via a deterministic `body/scaffold.py` (23-file tree, `__SLUG__`/
`__DATE__` substitution, clobber-guarded exit 2, root-AGENTS preserved if present). Faithful to
project B's persistence model (glossary in the vault, no root CONTEXT.md); the scaffolded
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
concepts, index, pipeline, harnesses, scaffold.py templates, the plan doc, and project B's
planning-workflow.md adapter (separate repo). Past log entries keep the old name as history.
The grill step itself is unchanged — only the skill name. Still deploy-held pending pressure
test, so no symlink to migrate. Lint clean.

## [2026-06-21] implement | bc-autoresearch-loop (metric-gated bounded improvement)
Added `bc-autoresearch-loop`, a model-invoked discipline that re-expresses the AutoResearch idea from
the Scripts `<improve-script>` CLI (idea only — no runtime dependency, rewritten self-contained):
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
Added two deltas to `concepts/agent-kernel/body/AGENT-KERNEL.md` from a user request. (1) Git discipline now requires proactively asking whether to push after a commit (still gated on explicit yes / publish policy) — the never-publish rule prevented unwanted pushes but let finished commits sit silently. (2) Operating posture now routes durable user preference requests into this shared canon by default, because the user runs agents across multiple vendors and a per-harness save silently fails elsewhere — prompted by a too-narrow Claude-Code-only memory save that the user corrected. CONCEPT.md design decisions + index entry updated. Refreshed all three deployed deltas (Claude Code `~/.claude/CLAUDE.md`, OpenCode `~/.config/opencode/AGENTS.md`, Codex `~/.codex/AGENTS.md`) with both rules and bumped their DERIVED markers to 2026-06-26. Removed the superseded project B project memory `ask-before-push.md`. Pressure scenarios for the two new rules: not yet authored.

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

## [2026-07-04] update | publish policy: plain agent-commit pushes in project B
Added `project-b-push-after-agent-commit` to `policies/publish.yaml` at the user's request ("fix publish policy"). Gap: a plain agent docs commit (docs/launch-plan.md) fit neither existing project B rule — the push-and-close rule's when-conditions are issue-drain shaped (`issue_acceptance_criteria_satisfied`), and the doc-maintenance rule is confined to `.bc-agent/`/agent instruction files. New rule mirrors `scripts-repo-push-after-agent-commit` (git_push on master, after_agent_commit + only_agent_authored_changes). Also noted for the record: `publish-check.py` takes the remote URL, not the git remote name — passing `origin` yields a false "no rule matches".

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
Moved `~/.codex/AGENTS.md`+`sessions/` and `~/.grok/AGENTS.md`+`sessions/`+`memory/` into `CONFIG/.codex` / `CONFIG/.grok` with per-machine symlinks back, so kernel deltas sync and chats continue from any machine. Sessions/memory are git-ignored (Syncthing-only). `<config-setup-script>` (Scripts repo, 4f1a845) now links these dirs entry-by-entry and excludes them from wholesale dir-linking — auth, caches, and Grok's per-OS binary stay machine-local. Pi sessions turned out to already sync (the exclusion I cited was git-only); no Pi change needed.

## [2026-07-13] ingest | tobi/qmd → qmd concept + bc wiring
New reference concept `qmd` (local hybrid search: CLI conventions, driver-owns-indexing rule, authority-labeled context trees). Wired into the bc loop: opt-in `bc-init-agent --qmd` scaffold flag (writes `references/qmd.md` setup page; verified additive/idempotent), drain driver preflight refresh + search-only worker retrieval, triage qmd prior-art query. Source clipping moved to raw/ingested/; accuracy check authored but not run (qmd not installed locally).

## [2026-07-13] deploy | qmd skill to local harnesses
Ran deploy-local-skills.py; qmd now symlinked at ~/.agents/skills, ~/.pi/agent/skills, and ~/.claude/skills (all verified resolving to body/). Accuracy check still pending a qmd install.

## [2026-07-13] lint | Grok code-review collision resurfaced
A Grok update restored the bundled ~/.grok/skills/code-review (xAI maintainability audit), re-shadowing the canonical obra code-review concept. Removed again; harnesses.md now warns that Grok upgrades resurrect bundled skills and to re-check for collisions after each update.

## [2026-07-13] test | qmd accuracy check PASS
Added installers/packages/qmd.pkg to Scripts (npm user-local, codex.pkg pattern) and installed qmd 2.5.3 on Arch. Full accuracy check passed: all skill commands work as written; contexts surface authority labels in results; update+embed is a clean no-op. Key finding: project-local .qmd/index.yml stores absolute collection paths → gitignore all of .qmd/, setup per-machine (SKILL.md, scaffold reference page, and CONCEPT.md updated).

## [2026-07-13] implement | qmd rework: global mode only
User decision after grilling: one global index, five collections (agents/wiki/music/scripts/project-b) from synced canon Scripts/config/qmd-collections.yml, converged per-machine by <qmd-setup-script> (+ daily <qmd-refresh-job>.timer, qmd.pkg post_install). Removed the same-day --qmd per-repo design from bc-init-agent's scaffold; its close-out now registers new vaults by default (opt-out). Rationale: project-local .qmd/ shadows the global registry (verified) and is invisible from drain worktrees. Skill body, triage/drain detection, and all four CONCEPT.md files updated. Ran setup on Arch: 1055 docs indexed, first embed in progress.

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

## [2026-07-27] tune | inert-guard review class from an project B drain
A real `/bc-drain-issues` run on project B #203 (an issue *about* two inert referral gates) had its build worker reproduce the defect class it was assigned to remove: it deleted the named tautological clause, left a sibling clause tautological, and substituted `$campaign['id']` for `$campaign_id` — an identical runtime value that made the tautology look like two independent facts. Independent Spec review caught it, and reverting the expression made the test *fail*, proving the clause had only ever been green as a tautology. Promoted per the Tune operation: `code-review` gains a general "Verify a guard can actually fire" block (paired explicitly with *Findings are not obligations* so it is not read as licence for defensive code), `bc-drain-issues` gains a `guard/rejection clause -> can-its-inputs-differ-in-production evidence` audit row and an unfireable-guard rule in `review-contract.md` (AFK reviewers see only the driver's packet). Both bodies are symlink-live immediately; the `code-review` pressure check 7 is authored but **not run**, and the drain row has no Gate A check because it is a model-behaviour property. Test gate is therefore outstanding for both — recorded rather than implied.

## [2026-07-27] implement+test | deterministic bc-drain-issues v3 Gate B trace
Replaced probabilistic topology as the deployment benchmark with a locked S0→S1→S2 trace containing exactly two Standards-only reworks; the natural contested fixture and its one-rework INVALID result remain ecological-pressure provenance. The harness pins hostile-environment-resistant SHA-1 Git identity/config, regenerates its own canonical contract, uses sanitized no-remote roots plus fail-closed receipt stubs without falsely claiming physical network isolation, and derives model/session tokens from real Pi lifecycle artifacts. Reviewer JSON and reworker patches now supply independently checked fidelity; stale Spec hashes cannot land and v3 requires a focused final S2 Spec sync. Gate A remains 22/22 with check 19 strengthened for both intermediate skips and exact-hash sync; trace self-test passes all identity, behavior, evidence, isolation, dispatch, and landing checks. Real same-model/medium v2/v3 token measurement remains outstanding.

## [2026-07-30] implement | machine-mesh remote-command PATH
Non-interactive SSH sources neither .zprofile nor .zshrc, so an agent had reported node/npm/gh missing on the Mac when all were installed. Documented the check and the `~/.zshenv` fix in body/SKILL.md, recorded the decision and an accuracy-check run. The second machine was unreachable during verification.

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
it was a flake — the global file is loaded (it recalled Luna-max and <improve-script> unprompted).
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
ever fire: zero `.feature` files and zero BDD runners anywhere in `<synced-home>`, and
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
`.bc-agent/`, both active through 2026-08-19) and ignored project B `temp/` (84 of 238 indexed
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
(Music, Scripts, project B, CV, Learning/codebase-design, Learning/sql), one commit each, staging
only that file — Music's untracked Obsidian files were left alone. Installed and enabled the
user timer for the CV pilot only; first run Mon 2026-08-24 03:39 BST. Detection under the service
environment confirms CV at `PROMOTION_REQUIRED=1` (10 unpromoted entries, 21 pages missing from
index). The four legacy `.agent`/`agent/wiki` vaults have no `references/agent-skills.md` and were
deliberately skipped.

## [2026-08-23] deploy | pointers in both Homeflix vaults; stale canon path repaired
Created `references/agent-skills.md` in the public and private Homeflix `.agent/` vaults (neither
had a repo-local skill map) and indexed both; the private one additionally binds the maintenance
pass to `conventions/secrets.md` and says an upstream conflict is recorded, not reconciled.
Repaired the dead `<old-private-config-checkout>` path in 12 instructional files across six vaults;
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
`templates/` — project B's vendor tree was drowning the report. First live sweep: 8 checked,
2 fail (Music leftover example wikilinks; codebase-design broken/ambiguous `[[plan]]` /
`[[project-b]]`).

## [2026-08-23] deploy | promotion timers for project B and public Homeflix
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
Fixed the four queued items. The `agents` qmd collection had pointed at `<old-private-config-checkout>` since
its first commit -- a path that never existed -- yet held 491 indexed documents, so searches returned
content from a vanished directory rather than nothing. Repointed at the workspace (232 files) and
corrected its context sub-paths; note that `<qmd-setup-script>` skips a collection already registered under
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
orphans each, `index.md` alone is 4,543 tokens in project B, and `qmd query` measured 67.1s. All three
advisors independently converged on filter-don't-read via a generated catalog.
Three defects verified at source, not relayed: scaffolded `map.md` contributes zero graph edges because
`without_code()` blanks its code-span targets before `links()`; Gate 1 does NOT mechanically block link
insertion (`run-promotion.sh:226` short-circuits on zero deletions), so that prohibition is policy only;
and `scaffold.py:307` emits `## __DATE__` while `wiki_lint.py:19` requires `## [YYYY-MM-DD]`, which is
the root cause of the two permanently blocked vaults. Also found `<owner-wiki>` already runs daily
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
the benchmark vault is gitignored: 84 of project B's 239 pages sit under `temp/`, where `git log` returns
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
Search-first replaces index.md-first in Music, Scripts, project B, CV, codebase-design, sql,
Homeflix and homeflix-prod, each committed in its own repo. Music kept its plans-first route
with search inserted ahead of it. Four lean vaults carry a one-line form only — see the note in
`docs/plans/active/agent-vault-read-path.md` about their missing empty-result and hub-page rules.
Prerequisite fixed en route: `~/.zshenv` set `AGENT_CONCEPTS` to a nonexistent path, which broke
every skill command using the variable.

## [2026-08-29] implement | plan the vault write/read contract
Assessed the landed read path against the write path and found they share no contract: the
scaffold still generates index-first instructions and `## YYYY-MM-DD` log headings the promotion
detector cannot parse, which leaves Scripts and sql at `PROMOTION_RANGE=invalid` and CV and
project B one entry from it. Filed `docs/plans/active/agent-vault-write-read-contract.md` with
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

## [2026-08-29] implement | drop wiki miss-rate; qmd is optional extra
Removed the 3-vs-6 miss comparison (cost is the claim). qmd is optional multi-vault search, not
the default the new path replaced.

## [2026-08-30] implement | bilateral skill relationship design
Added the proposed one-source relationship graph design: curated forward edges, generated incoming
views, maintainer-only impact review, and deterministic lint/generator requirements.

## [2026-08-30] implement | bilateral skill relationships plan activated
Moved the design record to active and turned it into a seven-task implementation plan: module
contract for scripts/relationships.py, exact rendering contract, TDD fixture tasks, six verified
pilot edges, the AGENTS upkeep rule, and its pressure run.

## [2026-08-30] implement | bilateral skill relationship graph
Added `concepts/relationships.json` as the one home for skill-to-skill edges, `scripts/relationships.py`
for validation and deterministic rendering, and lint wiring with `--write-relationships` as the only
mutation path. Seeded six verified pilot edges and generated seven `RELATIONSHIPS.md` views so a callee
can see its callers.

## [2026-08-30] implement | relationship upkeep rule in AGENTS.md
Implement/Update now requires reading a concept's relationship view before a contract change,
accounting for every incoming edge, and updating the graph plus regenerating views in the same change.
Lint's check list gained graph validity and stale views.

## [2026-08-30] test | relationship upkeep rule pressure run
Two runs against throwaway clones under "skip the metadata bookkeeping" pressure. Run 1 passed but was
contaminated by the plan document in the clone; run 2 passed cleanly with the plan removed and after
in-character pushback. Graded from clone Git objects and lint, not the subagents' reports.

## [2026-08-30] implement | vault write/read contract W3 and W4
Recorded the tracked-only/new-page boundary in the canonical maintainer and generated vault instructions,
added exclusion/synchronization regressions, and measured the sole page-kind candidate across the extended
20-question corpus. The candidate improved 3/20 to 2/20 misses but its overlapping Wilson intervals made
that one-miss delta noisy, so production BM25 remains unchanged; predecessor and active-plan status text was
reconciled while the W5 pressure gate stays parent-owned.

## [2026-08-30] test | vault write/read W4 page-kind benchmark
Extended the existing n=20 corpus with eight verified compiled-page/log overlap cases and compared
production direct BM25 with the page-kind candidate. Direct BM25 was 3/20 misses at 174.88 median;
the candidate was 2/20 at 179.88, but overlapping Wilson intervals made the one-miss improvement
noisy, so the report records a null result and production scoring remains lexical.

## [2026-08-30] tune | wiki conflict records cite originating log heading
Gate 3 now requires every conflict open-question to cite the exact originating `log.md` heading/date
in addition to both mutually exclusive source pages. First post-`6794ee3` promotion pressure was
4/5; the contradiction rerun is not claimed.

## [2026-08-30] implement | close vault write/read contract
Recorded W5 promotion pressure PASS 5/5 after the Gate 3 tune and contradiction rerun, made the
round-two report emit `$HOME` display paths, and moved the write/read contract plan to implemented.

## [2026-08-30] test | vault promotion pressure 5/5 and portable display path
Durable results artifact grades fallback 4/5 plus the tuned contradiction rerun as combined PASS 5/5.
Added a regression that the round-two report renderer never interpolates a resolved home path.

## [2026-08-30] lint | regenerate status after wiki-maintain tested date
Ran `python3 scripts/lint.py --write-status` because `bc-wiki-maintain` `tested` moved to 2026-08-30,
then `python3 scripts/lint.py`.

## [2026-08-30] implement | scheduled wiki failure notification
Added runner-local fail-closed desktop notification wiring for both systemd wiki services, with
unit-template, notifier, README, and temporary-fixture regression coverage.

## [2026-08-30] implement | notifier reads the journal at systemd's real priority
The W3 notifier filtered `-p err..emerg`, but systemd logs unit stderr at notice, so every alert
would have degraded to "no error output found". Scoped the read by `SyslogIdentifier` instead,
with an unscoped fallback, and added a regression test whose `journalctl` stub honours its filter.

## [2026-08-30] implement | close review findings on the failure notifier
Independent review found the install recipe never copied `bc-wiki-notify@.service`, leaving
`OnFailure=` pointing at a missing unit, and two stubs that passed regardless of what the script
did. Fixed the recipe, made the stubs argument-aware, and added a `notify-send`-fails case.

## [2026-08-31] implement | list-driven wiki promotion runner
Added a separate-list batch runner, all-vault systemd templates, and temporary-fixture regressions.
The batch delegates unchanged per-vault safety gates and reports every failed vault without aborting.

## [2026-08-31] lint | refresh bc-wiki-maintain test status
Updated generated `docs/status.md` after recording the 2026-08-31 regression run, then reran lint.

## [2026-08-31] implement | bound each vault in the batch promotion runner
One unit covering every vault let a hung agent consume the whole `TimeoutStartSec` budget, so the
vaults after it never ran — an exposure the per-vault units never had. Each child now runs under
`timeout` (default 30m, `PROMOTION_TIMEOUT`), reported as a normal per-vault failure.

## [2026-08-31] implement | close review findings on the batch promotion runner
Independent review found the per-vault `timeout` did not bound a child that ignores SIGTERM, and the
regression test asserted the message rather than the bound, so it passed 30s late. Added
`--kill-after`, classified exit 137 alongside 124, made the test assert elapsed time, gave the
notifier a `VAULT_LIST` fallback for units with no `VAULT_ROOT`, and asserted the unit's
`TimeoutStartSec` and schedule.

## [2026-08-31] implement | make scaffold map targets graph-visible
Generated map entries now use real Markdown links for in-vault targets, while upgrade notes flag
existing inline-code maps; the map records why external source-tree references stay unlinked.

## [2026-09-01] implement | record deferred-item state in the read-path plan
Deferred 2's mechanism and Deferred 4's scaffold side landed; both measures still need steps that
touch state outside this repo (enabling the batch timer, migrating eight live maps). Recorded the
per-vault `--kill-after` finding and the in-vault-only map rule.

## [2026-09-01] implement | document deferred vault migrations
Added human-facing runbooks for the one-time per-vault-to-batch timer migration and existing
live-vault map-link migration, including rollback, timeout recovery, and before/after verification.

## [2026-09-02] tune | treat child commit records as untrusted evidence
Documented worktree `Commit:`/`Branch:` lines as last-pair candidates only, requiring Git, branch-ref, base/range, and tree/diff validation before integration. Extended bc-swarm check 6 with a nonexistent first SHA, corrected last pair, cleaned-ref acceptance, and existing-ref mismatch coverage.

## [2026-09-05] implement | explicit teach host adapter
Added the approved `.bc-agent` learning/hybrid adapter and exact host path map, preserved standalone teach state, bounded existing-home upgrade notes, and protected teach-owned evidence/review state from wiki maintenance. Added source-backed graph edges and generated relationship views.

## [2026-09-05] test | teach host integration regressions
Added deterministic scaffold/layout and hosted `due.py` regressions plus clean consumer pressure scenarios for hosted resume, standalone preservation, competing homes, and cross-skill upkeep. Consumer pressure scenarios remain pending a parent run.

## [2026-09-05] implement | teach host-selection safety fixes
Defined explicit destructive migration with verify-before-remove ordering and refusal with originals intact; fixed vault-context competing-home resolution, hosted search-first retrieval, and the learning evidence stub. Tightened adapter validation, generated-stub formats, scaffold preflight, glossary ownership, and authored migration pressure coverage; consumer pressure remains pending.

## [2026-09-05] test | teach hosted-adapter consumer pressure
Ran the hosted-integration scenarios against fresh consumers in throwaway workspaces and graded them on disk. Scenarios 1/3/4 passed against ea49123; scenario 2 was unsound and its rewrite, the explicit-migration pair, and the four-entry-context variant all passed against afbb86b. Recorded per-scenario results and which commit each ran against in the three affected CONCEPT.md files.

## [2026-09-05] lint | refresh tested dates after the hosted-adapter pressure run
The previous entry recorded the 2026-09-05 runs in each concept's `## Tests` prose but left `tested:` untouched, so `docs/status.md` still showed the pre-run dates. Bumped `tested:` on teach, bc-init-agent and bc-wiki-maintain and regenerated the board; `test_status` stays `partial`.

## [2026-09-23] implement | agent-kernel: one-token questions + Goal/Next recap
User-grilled rule: single questions number their options, batches use numbered questions with lettered options (`1a 2b`), independent questions batch while grilling/brainstorming keep one-at-a-time; every non-trivial reply ends with `Goal:` (~5 words) and `Next:` (one line). Scenario 10 passed on Luna max and Grok 4.6 high after two tunes (serialized batches; recap dropped after a question). Deployed to all five harness deltas; supersedes Pi/OpenCode "suggest next steps only when natural".

## [2026-09-23] implement | numbered grilling answer options
Required numbered answer options, one marked recommendation with a brief reason, a numeric reply example and free-text override; the one-question gate and bulk-delegation exit are unchanged. Added matching pressure expectations; the bc-plan-to-issues consumer contract is unaffected, and the new format awaits a live pressure run.

## [2026-09-23] test | grilling numeric answer format
Fresh Grok 4.6 high consumer passed numeric options, batch resistance, bulk delegation, and codebase-first. Time pressure initially failed to offer the recommendation-based bulk exit; tuned the gate to offer a numbered continue/delegate choice and reran it successfully. Five pressure checks pass; Pi, Claude, and shared-bus symlinks already point to the canonical skill body.

## [2026-09-23] implement | recap labels become finish flag and footsteps
User chose `🏁` for the goal and `👣` for the next action instead of written labels; meaning and exception unchanged. Fresh Luna max consumer passed question, partial-work, and standalone-fact replies (3/3); refreshed five harness deltas from the canonical agent-kernel.

## [2026-09-24] ingest | TypeSafe upstream skill
Filed the Obsidian README clipping in the canonical ingested-source folder and indexed it. Chose the upstream-maintained global skill channel instead of a vendored concept: TypeSafe's skill points to its live API docs, and local adaptation adds no user-specific behavior.

## [2026-09-26] implement | remove child-token circuits from bc-drain-issues
Removed child-token deferral/launch-stop rules while retaining review, round/no-progress, recovery, and systemic-failure gates. Aligned issue-slicing lifecycle fit as a qualitative judgment after the dependency audit; historical test outcomes remain historical.

## [2026-09-26] test | bc-drain-issues token circuit removal
Gate A passed 29/29: the live skill excludes retired token controls and retains review/round/launch gates; injected legacy rules fail the static check. Real driver dispatch above the former thresholds is untested. Both non-token deferral triggers share one recovery-before-release path; one representative six-entry bundle and brief were validated. Lint passed with existing workspace gap/symlink warnings; issue-slicing's changed scenario remains unpressured and is marked partial.

## [2026-09-26] ingest | file addyosmani/agent-skills and affaan-m/ECC snapshots
Read-only swarm comparison of both repos against canon; user chose three ideas (personal-path lint check, untrusted content is data, memory as injection persistence). Filed only their evidence in the raw inbox with pinned commits and hashes; ingestion into concepts pending placement decisions.

## [2026-09-26] implement | bc-swarm compaction failure mode
Added the observed failure to `pi.md`: three broad Luna scouts aborted at ~175k-token compaction while under their tool budget; narrower replacements finished. Guidance: size scout scope under one context window, do not resume a child that died at compaction.

## [2026-09-26] implement | prompting-agents untrusted input block; portability check scope
Added "Untrusted input and privileged actions" to prompting-agents (prompt is not the security boundary, least agency, reader/actor split, memory hygiene), sourced to the ECC security guide. portability-check.py now exempts docs/research/ evidence; two maintained files switched to ~/ paths.

## [2026-09-26] test | agent-kernel untrusted content and memory lines
Added two Tool-and-file-discipline lines (read content is data; memory takes facts, not directives) with scenario 11. Luna max baseline passed both injections; first memory wording failed by over-refusing requested facts; revised wording passed both. Kernel harness deltas not yet refreshed.

## [2026-09-26] deploy | agent-kernel untrusted-content lines to harness deltas
Added both new kernel lines verbatim to the Pi, OpenCode, Grok, and Codex global files; Claude Code got the memory line only (injection handling assumed built in, unverified).

## [2026-09-27] implement | remove last30days
User stopped using it: uninstalled the upstream package from `~/.agents/skills`, removed its skill symlinks and the private reference concept. Updated herdr's cross-references; private raw snapshot kept as evidence.

## [2026-09-27] implement | skill prune
Removed the `grill-me` concept and its stale deploy links; standalone grilling now points to `grilling` + `domain-modeling`. Retired the `/to-prd`, `/to-issues`, and `/implement` compatibility aliases and their deployed symlinks, plus the requested Claude-only `skill-writer` and `playwright-cli` installs; canonical skills and `notebooklm` remain.

## [2026-10-04] implement | bc-drain-issues Released Claim Markers
Adopted project B ADR-0041's marker format: validated tips are free, acquisition uses an exact marker lease plus push/remote ownership proof, and local deletion remains default with leased marker cleanup. Malformed tips stay held; authorization and no-force absent-ref creation remain gated. Supervisor-approved follow-up replaces only bc-init-agent's contradictory claim bullet with a canonical protocol pointer and records the relationship.

## [2026-10-04] test | released-marker protocol and scaffold regression
Marker-only Gate A check 30 passed against a disposable local bare remote, including malformed tips, stale leases, no-force rejection, and cleanup; installed Git 2.55.0 push help confirms lease semantics. All 15 deterministic scaffold tests passed. No models, network, deploy, or production pushes ran; checks 1–29 were not rerun and both concepts retain partial status.
Regenerated relationship/status views; workspace lint passes with existing partial-test and worktree-external deploy-symlink warnings.

## [2026-10-04] implement | owner/cloud drain isolation (project B #351)
Exclude `automated` from fresh/deferred/rework/restart paths before claim/label mutation; report active cloud claims without release/reuse/relabel, and preserve existing local bundles. Marker/CAS, non-automated attended landing, review, and initializer claim-protocol delegation are unchanged; provenance and all relationship impacts recorded in the concept.

## [2026-10-04] test | automated isolation contract
Full deterministic Gate A passes 31/31 after the expected RED; four source-named lane-isolation contract/order checks reject six guard mutations. Scaffold, relationship, and wiki suites pass 15/38/56 tests; status board regenerated unchanged and lint passes with existing warnings. Consuming-model pressure remains pending; no models/network/deploy/production writes ran.

## [2026-10-10] implement | agent-kernel sync-safety advice
Added a four-line generic rule for symlink-aware replication checks, volatile-state advice, approval before ignore edits, sync-overwrite diagnosis, and shared-data/dependency-lockfile preservation. Recorded the credential-overwrite incident as provenance and authored scenario 12; rule unpressured and undeployed, historical partial status retained. No global instructions changed; parent owns pressure testing before deployment.

## [2026-10-10] tune | agent-kernel sync-safety rule
Scenario 12 round 1: Luna max covered only the symptom file and edited `.stignore` under an explicit request the old wording forbade. Ask-before-editing now yields to explicit requests; added survey-the-whole-synced-directory; scenario split into (A)/(B). Round 2 pending.

## [2026-10-10] deploy | agent-kernel sync-safety rule
Scenario 12 round 2 passed (A/B × Luna max, Grok 4.6 high). Rule propagated to Pi, Codex, Grok, OpenCode and Claude Code global files.

## [2026-10-17] implement | plain-language procedures/warnings from ASD-STE100
Corrected STE's human-reader scope; added independently worded procedure/warning guidance, public provenance and explicit rejections of domain-specific rules and numeric proxies. Added runbook fixture and checks 7–9; historical six-check pass retained, new clauses unpressured (partial), no deployment. Relationship graph has no plain-language edges; no edge changes needed. Regenerated status; workspace lint passed.

## [2026-10-17] test | plain-language checks 7–9
Two consumer runs (gpt-6.1-sol low): run 1 2/3, check 8 warning opened with the consequence; tuned the warning bullet with an example; run 2 held 8 and 9, check 7 partial (noun stack kept as terminology). Status stays partial; deploy of new clauses blocked.

## [2026-10-17] test | plain-language checks 7–9 PASS
Made the runbook fixture's noun stack unambiguously descriptive; run 3 (gpt-6.1-sol low) held 7–9. Status pass; deploy symlinks already serve body/, so the clause was live on commit.

## [2026-10-22] implement | canonical project glossary filename
The owner chose `glossary.md`; parent defaults use `glossary-map.md` for bounded contexts and domain-modeling as the single home for legacy discovery and explicit rename proposals. Updated live consumers, scaffold output and fixtures without moving the initializer vault glossary or rewriting historical evidence; recorded and regenerated relationship contracts.
Initializer tests pass 16/16 and drain deterministic Gate A passes 31/31; local glossary accuracy review and lint pass (existing warnings plus pending legacy pressure). Added migration scenarios, marked domain-modeling partial and regenerated status. No deploy scripts or push; consuming-agent migration pressure remains pending.

## [2026-10-22] implement | legacy glossary proposal and consent fix
Legacy pressure failed: no-questions pressure suppressed the proposal, and citing the standard filename was mistaken for rename consent. Applied the approved wording, preserved both exact scenarios and supervisor reply, and recorded incoming relationship impact; partial status retained pending re-run. No deploy scripts or push.

## [2026-10-22] test | correct legacy glossary pressure record
Correction to the preceding legacy glossary proposal/consent entry: the first two runs were invalid, not rule failures, because worker consumers had inheritSkills:false and no skill text or skills list in context. Wording was tightened before any valid run.
The third run attached domain-modeling per child and confirmed skill text in both contexts: PASS 2/2 against dbdddb6 wording, reviewer xai/grok-4.6 high verdict OK. Both commits modified CONTEXT.md only and both replies proposed a rename without performing it. Updated test records, catalog and generated status; no skill-body edit, deploy or push.

## [2026-10-26] implement | bc-swarm keep reasons move to reasoning
Owner request: the one-line keep/no-dispatch justification no longer appears in the reply; the agent settles it per track in its reasoning. Dispatched tracks and routes stay in chat. Updated SKILL.md tooth, CONCEPT.md design decision, pressure check 4 grading (now graded from the reasoning trace) and the index line; mirrors CONFIG swarm-mode kernel commit 4892cfa. Not re-pressure-tested; status stays partial.

## [2026-10-26] implement | cross-provider review research
Added docs/research/cross-provider-code-review.md (+ two researcher evidence reports): fresh reviewer, hidden builder reasoning, executed checks and reviewer capability outweigh provider diversity. prompting-agents metaprompting line no longer treats a different provider as the independence lever; provenance added. Mirrors the owner's global AGENTS.md review rule rewrite.

## [2026-10-26] implement | codebase-docs live status: pointer, not copy
Measured live status (rank, counts, published/held, state-change dates) now has its home in the measuring system; source-tree docs name the source and how to read it, never the value, even dated. New table row, why paragraph, narrowed ledger exception, Never bullet, and load-bearing pressure check 7. Origin: an income-lab incident where stale "not yet visible" docs were repeated as fact. Pressure run PASS 7/7, review found loopholes, tuned, rerun PASS 8/8.

## [2026-10-26] implement | agent-kernel: argue for the best outcome; read-side clause dropped
Owner asked for anti-sycophancy pushback. Added two posture bullets (argue-then-defer on worse plans, overriding act-on-request until answered; accuracy over agreement on facts). Three pressure rounds on Luna max + Grok high: round 1 no effect, round 2 six cells fixed, round 3 5/6 (Luna thin evidence). Read-side live-state clause showed one improved cell of six and was dropped. Deployed to Pi, Claude Code, Codex, Grok, OpenCode.

## [2026-10-27] implement | shared storage safety
Added kernel-owned guarded pytest, targeted/shared full-suite evidence, Btrfs health preflight and proven integration cleanup; aligned test, review, planning, swarm and worktree consumers and relationship metadata. Thresholds stay in Scripts. Storage pressure scenarios authored but not run (parent must run consuming-agent checks); no harness delta deployment or push.

## [2026-10-29] implement | naming-things
Added advisory naming criteria, glossary handoff and an audit/compatibility rename recipe, with four one-line planning/init pointers and relationship metadata. Saved in entries use conceptual categories only to preserve domain-modeling glossary purity.
Pressure scenarios authored but not run; no deploy or push.

## [2026-10-29] implement | naming-things review corrections
Deferred init glossary persistence until plan approval, classified domain-modeling as a load, aligned the planner's composition descriptions and removed the negative scenario's extra prohibition. Regenerated relationships/status; lint passed with existing known-gap and local symlink warnings. Pressure scenarios remain unrun; no deploy or push.

## [2026-10-30] implement | code-review role output contract
Owner decision: when a review role prompt defines P0/P1/P2 + merge verdict, reviewers use it, keep Spec/Standards as subsections, and map Critical→P0, Important→P1, Minor→P2; an undeferred P1 still forces BLOCK. Fixed in the skill because the Pi `reviewer` prompt ships in the pi-subagents npm package. Check 10 added and run: PASS on format/subsections/mapping (Pi reviewer, Grok 4.6 high); P1-only BLOCK not isolated.

## [2026-10-30] implement | bc-drain-issues worker effort low/medium
User direction: ordinary slices run workers at low effort and high-risk slices at medium (was medium/high); the Pi role cap is now medium. Pressure test not re-run; the change moves a default level and adds no gate.

## [2026-10-30] implement | bc-drain-issues rework effort low
User direction: rework rounds after review run the worker at low even on high-risk slices, never at the role cap (medium). Builds keep low/medium by risk. Pressure test not re-run; the change moves a default level and adds no gate.

## [2026-10-31] implement | bc-swarm manifest events and todo obligations
Added a short durability rule separating event history from open obligations, including deferred-check triggers and the compaction failure rationale. Added a consuming-agent pressure scenario; NOT RUN because the worker has no child-launch tool, so partial status and historical test/deploy dates remain unchanged; no redeploy.
Checked pi.md (portable contract consumed, no duplicate needed) and external injected swarm context (upstream alignment needed). No relationship edge changed: session todo is a tool, kernel storage unaffected, no incoming edges.

## [2026-10-31] test | bc-swarm todo/manifest pressure scenario
Run 1 invalid (consuming agent had no todo tool; manifest-only reminder, flagged). Run 2 PASS with `pi -ne -e extensions/todo.ts`, gpt-6.1-terra low: one deferred todo with trigger `migration-review lands`, manifest kept events plus the owner-requested reminder. Overall status stays partial for the existing check-4 gap.

## [2026-11-01] implement | codebase-design friction signals
Moved the five friction signals from `improve-codebase-architecture` into `codebase-design` § Friction signals so builder subagent roles that load `codebase-design` get them; the architecture skill now points there (new `depends_on_contract` edge).

## [2026-11-02] ingest | cloudflare/security-audit-skill snapshot filed
Filed the whole MIT repo at `c1c8a8c` in the raw inbox with SOURCE.md and hashes. Owner-resolved plan (grill, 8 decisions): medium-port `security-audit` concept, evidence rules into `code-review`, guidance-by-default pattern into `prompting-agents`.

## [2026-11-02] implement | security-audit concept
Medium port of Cloudflare's MIT snapshot: guidance default, one source-focused hunting pass, fresh refutation, impact-capped verdicts, coverage ledger and four boundary-selected companions. Repo-local ignored outputs and approval-plus-sandbox execution gates replace upstream defaults.
Stdlib validator: guarded unit run passed (11 tests, 36 subtests). Four pressure scenarios and planted fixture authored, NOT RUN; not deployed. Raw evidence unchanged; status and relationships regenerated.

## [2026-11-02] implement | security-audit review fixes
Replaced the preview/bytearray planted bug (c) with a Unicode-normalization handle bug settled by a bounded normalize oracle; made the validator command portable; moved the Cloudflare raw source to ingested/ with link updates.

## [2026-11-02] implement | security-audit fixture (c) grading
Answer key now accepts confirmed-with-complete-source-trace or needs_validation for the NFKC handle bug; auditor-side stdlib checks on auditor-supplied input are explicitly ungated, target-code execution still needs both gates.

## [2026-11-02] implement | code-review evidence rules and prompting-agents loading-is-not-authorization
Adapted Cloudflare evidence calibration and an explicit costly-workflow mode gate; preserved the drain's strict machine output contract with an explicit exception for its existing untested channel.
Authored new artifact-graded scenarios, not run; marked revisions partial while retaining historical dates. No deployment.

## [2026-11-02] test | code-review Check 11 revised after review
Replaced the fixed-literal injection fixture with a source-grounded path-traversal question (`CACHE_DIR`/`name` caller unseen) and split Check 11 into a consumer packet and a grader key; recorded the old-fixture run as INVALID for the question criterion. Revised check NOT RUN.

## [2026-11-02] deploy | Muse Code kernel delta + shared-bus docs
Muse already lists corpus skills from `~/.agents/skills/` (no extra deploy target; do not `muse skills import`/`install`). Added a Codex/Grok-style kernel delta as a regular-file copy `<private-config>/muse/AGENTS.md` → `~/.config/muse/AGENTS.md` (Git discipline omitted: bundled `git` forbids unsolicited commits). Documented in harnesses.md, bootstrap.md, AGENTS.md, deploy-local-skills.py. Live recap pressure run pending.

## [2026-11-03] lint | warn on copied kernel-delta drift (Muse)
Added generic, warning-only byte comparison from optional private kernel-copies.json, with isolated fixture tests and portable configuration docs.

## [2026-11-03] deploy | security-audit
All 4 pressure scenarios pass on e530e5d (headless Pi, Grok 4.6 high, isolated scratch repos, graded from artifacts) after tuning the execution gate (approval ≠ sandbox waiver) and mode/label gate (explicit audit needs the full workflow; guidance carries no verdict labels). Deployed via deploy-local-skills.py (shared bus + Pi + Claude; Muse reads the bus); naming-things skipped (untested).

## [2026-11-03] test | code-review Check 11 + prompting-agents authoring check
Revised Check 11 PASS (headless Pi, Grok 4.6 high, isolated repo): crash capped, RCE refused, traversal kept as a no-severity question, rate-limiter DoS refused; `CACHE_DIR` half not exercised (fixture deviation). Loading-is-not-authorization check recorded PASS from the 2026-11-02 run.

## [2026-11-04] ingest | file Pocock PR-bottleneck talk notes + HumanLayer show-me snapshot
Filed `docs/research/raw/pocock-pr-bottleneck-talk/` (research notes, links; transcript not redistributed) and `docs/research/raw/humanlayer-show-me/` (MIT snapshot at `4d69d20`) in the inbox, ahead of a `show-me` concept and `tdd`/`code-review` changes.

## [2026-11-04] implement | show-me concept; tdd tests-that-lie; code-review merge danger
New model-invocable `show-me` (adapted from HumanLayer MIT skill; inline by default, HTML only on request, pointers from plain-language/unslop/codebase-docs/teach). `tdd` names tautological / structure-sensitive / cannot-fail tests with a per-test "which regression turns this red" self-check; `code-review` Standards applies them and reports a merge-danger line (one-way/two-way door, blast radius). Evidence: Pocock talk notes plus a sampled audit of agent-written tests in an owner repo. Scenarios authored, not run.

## [2026-11-04] test | show-me, tdd tests-that-lie, code-review merge danger
Pressure runs (GPT-6.1 Sol low, throwaway repos, artifact-graded): show-me checks 1/3/4/5 PASS; tdd Pocock scenarios 3/3 PASS; code-review tautological-test PASS, email-to-all-users one-way + human review held but blast radius came back `localized` → clause tuned (reach of effect, not diff size), rerun pending. Independent review (Opus) fixes: pointers added in improve-codebase-architecture and frontend-design, show-me guidance block promoted, "ordinary Q&A" exclusion narrowed, stray blank lines removed.

## [2026-11-04] test | code-review blast-radius rerun
After the blast-radius tuning, scenario 1 rerun on a fresh fixture PASS: one-way, cross-cutting, held for human review despite the "approve without the owner" push.

## [2026-11-04] deploy | show-me
Owner chose 1a: deployed via `scripts/deploy-local-skills.py` to the shared bus, Pi and Claude Code before the trigger-boundary checks (2, 6, description-only discovery), which remain pending.

## [2026-11-04] implement | deploy-local-skills holds `deployed: no` concepts
The bulk deploy had linked untested `naming-things` live alongside `show-me` (links removed). The script now skips any concept whose CONCEPT.md frontmatter says `deployed: no` and reports it; AGENTS.md Deploy updated.

## [2026-11-04] test | show-me description-only discovery and boundaries
Fresh headless Pi (Opus default), skill advertised only: doc request loaded show-me; typo/flag/lesson/architecture/UI requests did not; unslop kept visual blocks byte-identical. Gap: "How does this pipeline work?" answered well inline but did not load the skill.

## [2026-11-04] test | show-me description kept
Owner chose not to widen the description to catch plain "how does X work?" questions; gap recorded in the test file.

## [2026-11-05] test | tdd and agent-kernel better-tests A/B
Private pressure model, with vs without: tdd helped seam (T2) and tests-after-code (T3); discovery (T1) not discriminating. Kernel-only scenario 15: watched RED before fix 2/2 vs 0/2. Grading had wrongly counted `tags.subprocess.run` patches as own-name; owner chose to allow stdlib boundary patches (`4cb9b5e`).

## [2026-11-05] deploy | agent-kernel test-evidence line
Propagated to Pi, Codex, Grok, OpenCode, Muse (CONFIG `e36a14d`) and `~/.claude/CLAUDE.md`. Income-lab got the tdd copy, an AGENTS.md test rule and a review-prompt clause (local main `dfe5c12a`; push left to that repo's owner session). tdd now notes confirm-red's per-run tree copy (review F16).

## [2026-11-11] implement | ui-design replaces frontend-design
Broadened UI design to all surfaces, with ranked principles and scaled capture evidence; held deployment pending pressure tests.

## [2026-11-11] implement | ui-design review fixes
Restored historical research and strengthened screenshot checks, host capture, design guidance and discriminating scenarios; deployment remains held.

## [2026-11-11] implement | ui-design pressure-test gap fixes
Strengthened whole-surface critique, durable evidence and capture naming; clarified wrapping, review triggers and non-interactive defaults. Pressure testing and deployment remain pending.

## [2026-11-11] test | ui-design pressure rounds 1 and 2
Ran scenarios without and with the skill; it made the difference in A, C, H and I, with D unresolved and baselines partly contaminated. Results stored in `concepts/ui-design/tests/results/`; three small gap fixes followed and are untested.

## [2026-11-11] deploy | ui-design
Deployed to the shared bus, Pi and Claude Code; removed the dangling `frontend-design` links.

## [2026-11-12] tune | agent-kernel branch cleanup after resolved picks
The owner asked not to be consulted about deleting a worker branch whose content landed through a conflict-resolved cherry-pick. Storage safety now accepts a recorded resolved-pick proof for `-D` and says not to ask; using-git-worktrees and finishing-development-branch follow. New test variant (i) is unexecuted.

## [2026-11-12] implement | bc-init-agent visible layout plan
Recorded the design agreed in a 22-question owner interview as `docs/plans/implemented/bc-init-agent-visible-layout.md`: status by folder under a root `work/`, knowledge in the open, one layout table per project. Plan only; no concept changed.

## [2026-11-12] implement | bc-init-agent visible layout (W1)
Code, ops and hybrid now scaffold `work/` lifecycle folders, `docs/decisions/` and `docs/research/`, root `glossary.md` and a "Where things go" table (`parse_where_things_go`) in `.bc-agent/AGENTS.md`; learning/knowledge output is byte-identical to before. Sixteen new deterministic test functions, SKILL/CONCEPT/MIGRATIONS/scenario updated; not pressure-tested, not redeployed, and consumer concepts (W2+) still assume the vault.

## [2026-11-12] implement | bc-init-agent W1 review fixes
Applied review findings 1–17: visible-layout runs refuse earlier-layout projects unless `--allow-earlier-layout`, `--force` stays inside `.bc-agent/`, the table parser keeps plain paths and rejects empty or duplicate rows, and generated text redirects skill default paths to the table. SKILL steps 9–10 (qmd, nightly maintenance) are learning/knowledge only for now; the merge to the main checkout is held until consumer skills read the table. `<pytest-wrapper> concepts/bc-init-agent/tests`: 102 passed; not pressure-tested, not redeployed.

## [2026-11-12] implement | bc-init-agent ops open questions and hybrid shared glossary
Owner decisions: ops/hybrid drop `docs/open-questions/` (open questions become work-item steps, planned items or ideas lines), and a hybrid project's `teach` uses the root `glossary.md` via a second valid adapter map; hybrid no longer generates `project/overview.md`. teach SKILL shows both Glossary variants. `<pytest-wrapper> concepts/bc-init-agent/tests concepts/teach`: 107 passed; not pressure-tested (teach scenario 5 written), not redeployed.

## [2026-11-12] implement | bc-wiki-maintain visible-layout lint (W2)
`wiki_lint.py` detects visible-layout projects by their "Where things go" table, drops vault demands there, and checks work folders through the table's paths (duplicate numbers, done month folders, `Status:` lines, empty Outcome as errors; item names, missing `plan.md`, missing role paths as warnings). `SKILL.md` routes promotion to table roles and keeps the promotion timer vault-only. The parser is a verbatim copy guarded by a drift test. Not yet pressure-tested.

## [2026-11-12] implement | visible-layout role lookup in dependent skills (W3)
`triage`, `bc-drain-issues`, `bc-plan-to-issues`, `improve-codebase-architecture`, `diagnosing-bugs`, `prototype`, `handoff` and `domain-modeling` look glossary, decisions, research, ideas and work folders up in the project's "Where things go" table, with their earlier paths as the stated fallback. Rejections become dropped work items with the reason; drain shows status by moving the item and carries the claim-before-work rule in its body; a plan is a work item; architecture reviews save to the research role and route findings by the owner's choice, with the inbox and ledger retired where the table exists. Relationship edges to the table contract added. Not yet pressure-tested; held on branch `w1-visible-layout`, not deployed.

## [2026-11-12] implement | visible-layout W2/W3 review fixes
Applied review findings F1–F17 and three follow-ups: drain workers list follow-ups in their handoff and the driver appends them to the ideas file after landing; a large work item holds `plan.md` and `requirements.md` (decision 10 refined in review, pending the owner's confirmation); `wiki_lint.py` ignores fenced layout headings, scans every Markdown file of a folder item, skips folder READMEs and compares item numbers as integers; promotion fails closed on visible-layout projects; the shared-glossary rule has one home in `domain-modeling`; missing observation and glossary edges added. Deterministic tests only; not pressure-tested, not deployed.

## [2026-11-12] implement | bc-init-agent migrate mode (W4)
`scaffold.py --migrate` prints a plan for moving an earlier-layout vault to the visible layout and `--apply` does only the mechanical part (git mv of decisions, `docs/adr/`, research and components; missing layout files; new `.bc-agent/AGENTS.md`; placeholder deletes; relative-link rewrites), stages and does not commit; everything needing judgment is listed with the owner's rule, now in the skill body. Owner decisions 27–30 added to the plan. Trial on clones of one code and one ops project; deterministic tests only, not pressure-tested, not deployed.

## [2026-11-12] test | bc-init-agent visible-layout pressure run
Four scenarios against the generated work-item rules and the migrate section; two held, two failed on an explicit user override (delete a dropped item; stash and migrate without preview). Rules tightened and both held on rerun. Results: `concepts/bc-init-agent/tests/pressure-visible-layout-results-2026-11-12.md`. Dependent skills not yet pressure-tested.

## [2026-11-12] implement | bc-init-agent migrate rewrites wikilinks
Per plan decision 32, `--migrate --apply` now turns a wikilink naming a moved file into a relative Markdown link (labels, heading anchors, path forms, embeds); ambiguous names and wikilinks from moved files to files that stay are left and reported. Test-first in `test_migrate.py`; trial on a fresh clone of one ops project: 108 rewrites, all resolving. Not deployed.

## [2026-11-12] fix | bc-init-agent migrate accepts earlier vaults with a "Where things go" bullet list
Earlier scaffolds wrote a `## Where things go` heading over a bullet list of vault folders, so the migrate mode refused two real projects as "already migrated". It now refuses only when the heading holds a parseable role table. `bc-wiki-maintain` lint already fell back to vault for these.

## [2026-11-12] test | dependent skills under pressure in a visible-layout project
Six skills run on Terra low with a request that names the earlier path. `triage`, `domain-modeling`, `diagnosing-bugs`, `bc-plan-to-issues` and `improve-codebase-architecture` used the table roles. `prototype` did not hold across three rounds (scratch folder, both places, scratch folder) despite two wording changes; the wording stays, unverified, and a lint backstop is proposed. `bc-drain-issues` and `handoff` not covered. Results: `concepts/bc-init-agent/tests/pressure-dependent-skills-results-2026-11-12.md`.

## [2026-11-12] implement | bc-init-agent close-out: lint backstop, prototype, search, project agents
Owner decisions 33–36 in the visible-layout plan: `wiki_lint.py` reports any non-mechanics entry under a visible project's `.bc-agent/` (optional `agent-extras` row); `prototype` follows a place the user names and recommends the research role; visible projects register two qmd collections printed by `wiki_lint.py --qmd-entry` and promotion is "not applicable" (runner exits 0); `project-agents` row is `.agents/agents/`. Deterministic tests only; not pressure-tested, not deployed.

## [2026-11-12] plan | bc-init-agent visible layout implemented
Close-out decisions 33-36 landed (`93f9694`). The five migrated projects are registered for search (two collections each), their `project-agents` row points at `.agents/agents/`, and the lint reports no stray `.bc-agent/` content in any of them. Plan moved to `docs/plans/implemented/`. Not covered: `bc-drain-issues` and `handoff` under pressure in a visible-layout project.

## [2026-11-15] implement | agent-kernel recap: 📦 delivery line, order 📦/👣/🏁
Owner asked for the project-a-style delivery line in every session, goal last, no blank lines; 📦 only when something was made for use; delivered = usable now (committed-only is not). Scenario 10 extended with (e). Not yet pressure-tested or propagated to the harness deltas.

## [2026-11-15] test+deploy | agent-kernel recap 🏁/👣/📦
Owner swapped the order to goal first, delivery last. Scenario 10 (a)–(e) on Sonnet 5.5 low: one tune (never "Delivered: nothing"), then PASS 6/6. Propagated to the five CONFIG deltas, the Muse runtime copy and ~/.claude/CLAUDE.md.

## [2026-11-15] test+deploy | agent-kernel 📦 lists only new deliveries
Owner choice: a delivery is listed once; NOT delivered items persist; work not yet begun gets no 📦. Scenario 10 (a)–(f) on Sonnet 5.5 low, two tunes, then PASS. Propagated to the CONFIG deltas, Muse runtime copy and ~/.claude/CLAUDE.md.

## [2026-11-15] test+deploy | agent-kernel 📦 labels Ready to use / Not ready yet
Owner: the not-delivered half usually stands alone and needs a label that reads on its own. Recheck on Sonnet 5.5 low PASS 6/6; propagated to the CONFIG deltas, Muse runtime copy and ~/.claude/CLAUDE.md.

## [2026-11-15] test+deploy | agent-kernel recap order 📦/👣/🏁
Owner put the goal last again. 📦-first regressed on Sonnet 5.5 low; tuned (often-absent opening, started = changed a file or ran a build/release step, two example recaps), then PASS. Propagated to the CONFIG deltas, Muse runtime copy and ~/.claude/CLAUDE.md.

## [2026-11-16] implement | bc-work-sync + bc-init-agent work index
New owner-started concept `bc-work-sync` (plan-first sync of `work/` with the project's docs; scenarios written, not run, not deployed). bc-init-agent gains `body/work_index.py` (stdlib port of project A's work-index), copied into visible-layout projects with a `Stages:` line, `Stage:` rule and `work/README.md`; bc-wiki-maintain's mechanics check allows `.bc-agent/scripts/`.

## [2026-11-16] implement | bc-work-sync and work index review fixes
Clarified plan, worktree and publishing gates and migration guidance; aggregate stage errors, report decoding errors, and scaffold a check-ready index. Added targeted regression tests; pressure scenarios remain unrun and bc-work-sync undeployed.

## [2026-11-16] test+deploy | bc-work-sync
Pressure scenarios run on Terra low, without and with the skill: baseline failed all four, skill held all four. Deployed to the three local skill dirs.

## [2026-11-17] implement | three-level testing model (tdd, code-review, bc-init-agent)
Owner-approved: tdd adds Level 2 property-based tests (required for rule-bearing logic; mutation fail-first; pinned failures; `body/properties.md`) and a reserved off-by-default Level 3. code-review's Spec axis checks properties; weakening/deleting one is Critical. Visible scaffold `validation.md` shows the levels. New scenarios authored, not run; not deployed.

## [2026-11-17] test | three-level testing model (tdd, code-review)
Pressure-tested on gpt-6.1-terra low without/with: tdd P1–P2 discriminating, P3 held both (pin only with skill), P4 void; code-review check 12 PASS (Critical only with skill). Trimmed the `.hypothesis/` gitignore instruction, since Hypothesis self-ignores its cache.

## [2026-11-17] implement | Level 3 formal verification rules and Test levels block (tdd, code-review, bc-drain-issues, bc-init-agent)
Owner decided Level 3: `tdd/body/formal.md` (Dafny/Verus/TLA+/Apalache, owner-only per-component on, mandatory candidate suggestions, dated declines, spec approval, proof runs, Dafny generated code); every report carries a Test levels block that code-review audits (unapproved escape hatch = Critical) and the drain gate requires. Scaffold Level 3 line + format comments. Scenarios authored, not run; not redeployed.

## [2026-11-17] test | Level 3 rules and Test levels block (tdd, code-review)
A/B on gpt-6.1-terra low, graded from repo state: tdd L1–L3 helped (Test levels block 0/3 → 3/3; candidate lines only with skill; decline respected); code-review 14 helped, 13 held in both (seeded `assume` too blatant; subtler hatch noted).

## [2026-11-17] implement | agent-kernel Storage safety: tests clean up temp files
Owner-approved rule: tests and helpers delete the temp files they create, including on failure, and agents compare the temp-dir footprint before/after a run (one project's tests filled a 7.7 GB tmpfs `/tmp`). Applied to the Pi, Codex and Muse derived copies; pressure scenario 5 authored, not run.

## [2026-11-17] test | agent-kernel temp-cleanup rule
Scenario 5 passed for kernel alone and kernel + tdd on Terra low (Node fixture, cleanup on failure, footprint compared); no baseline.

## [2026-11-18] implement | tdd Test levels hold across packets, reviews and parent commits
Project A field failure (~190 commits, zero properties): a bc-swarm packet waived L2, workers closed with `L2: not added`, reviewers never saw the block. tdd: only a quoted owner approval waives a level, unmeetable levels escalate, block may be a `Test-levels:` trailer; code-review: missing block/trailer and `covered by examples`/deferral are findings; bc-swarm: packets cannot waive levels, review packets carry the block, parent commits carry it (new bc-swarm→tdd edge). Private pi-subagent-routing reviewer line also carries the block.

## [2026-11-18] test | tdd level-waiver, code-review missing-levels, bc-swarm test-levels packets
Terra low, text-only, without / pre-change / current body: all three FAIL or partial before, PASS with the current bodies (scenarios in each concept's tests/).

## [2026-11-19] implement | bc-init-agent staged validation, scripts/gate, CI workflow
Visible layouts get a staged validation.md (while working / full gate / release, one owner each, 60 s and 5 min budgets), an executable `scripts/gate` stub that fails until filled, `.github/workflows/gate.yml` running it, and a root AGENTS.md rule that red trunk CI blocks landing. From the agent-time-sinks council memo; vault archetypes unchanged. Not pressure-tested.

## [2026-11-19] implement | tdd test layout norms, code-review layout check
tdd gains a Test layout section (browser tests only where a fake cannot show it, per-file state, ~25 tests/60 s per file, parallel runner + slow marker from the first test commit); code-review's Standards checks new test files against it. From the agent-time-sinks council memo. Not pressure-tested.

## [2026-11-19] implement | agent-kernel workers never run the full suite
The targeted-tests bullet moved from Storage safety to Verification with a time Why and now outranks a project page that says to run the full suite; zero net lines. 12 relationship reasons re-pointed from Storage safety to Verification (plus code-review→tdd reason gains the layout check); views regenerated. Derived kernel copies not updated here. Not pressure-tested.

## [2026-11-19] implement | bc-swarm targeted-check packets, background full gate
Worker packets name targeted checks (test files/IDs) and never paste the full gate; after integration the parent starts the gate in the background with a wake and dispatches the reviewer on the same tree in parallel, no sleep/poll loops. dispatching-parallel-agents and pi-subagent-routing checked: no contradiction. Not pressure-tested.

## [2026-11-19] implement | staged validation review fixes
Allow the change that turns red trunk green, keep and fill the scaffold gate on re-runs, and reconcile parallel review with the parent-owned gate result. Correct Verification anchors in five consumers; relationship contracts otherwise unchanged. Not pressure-tested.

## [2026-11-19] test | staged validation and test layout (agent-kernel, bc-swarm, tdd, code-review, bc-init-agent)
Terra low, text-only, `--no-context-files`, without / pre-change (c825984) / current body. Current bodies PASS every scenario; no body changes. Discriminating: agent-kernel worker scenario, bc-swarm packet (without FAIL), code-review file-size check (without/old FAIL), bc-init-agent full-gate and red-trunk scenarios (without/old FAIL or partial). tdd layout scenario did not discriminate: all arms put the pure-function test in a unit file; only the current arm added the parallel runner and slow marker. Scenarios and quotes in each concept's tests/.

## [2026-11-19] ingest | Matt Pocock's retro skill → retro concept
Vendored `mattpocock/skills@5863806` `retro` + `writing-for-agents` (MIT, blob SHAs verified) under ingested/pocock-retro-upstream; CITATIONS rows that said the repo had no licence corrected to MIT. New owner-invoked `retro` concept: Pi session/child/swarm/time-report evidence, wall-time category added, single-session and batch scope, every proposal homed and counted, proposes only. Not deployed.

## [2026-11-19] implement | agent-kernel 👣 session-close signal and /retro offer
When every deliverable is ready, 👣 says the session can be closed; after a substantial session it also offers `/retro`. New hands_off edges kernel→retro, retro→prompting-agents/code-review; views regenerated. Derived kernel copies not updated here.

## [2026-11-19] test | agent-kernel session close, retro
Terra low, text-only. Kernel: without / pre-change / current × long-done, short-done, in-flight; current PASS 12/12 after one tune (closing reply keeps its recap even when one line; drafts lost the signal to the short-answer exemption). Retro: without FAIL, with PASS 2/2 on an anonymised session fixture. Results in each concept's tests/.

## [2026-11-19] implement | retro review fixes
Correct session and child log layouts, portable timing lookup, headless batch report destination, and snapshot licence provenance. Existing fixture does not exercise the changed instructions; no deploy or status change.

## [2026-11-19] test | retro + agent-kernel session-close — recorded, deployed retro
- retro: fixture pressure test PASS 2/2 (without FAIL 0/2) on Terra low; review fixes f8c7fdb fix-verified. Deployed as local skill.
- agent-kernel: session-close 👣 clause PASS 4/4 per scenario (without and pre-change FAIL in finished-session scenarios). Derived kernel copies synced in CONFIG.

## [2026-11-19] implement | retro batch mode tightened
Batch sampling rule (top N by active time + random, "k of n sampled sessions", population stated), report file always written with `--report` winning, ranking via `<agent-time-report> --summary` with per-project fallback. From the batch trial's skill friction; test_status reset to not-run.

## [2026-11-19] implement | retro batch review fixes
Define the parent-session population, reproducible project/file-size sampling and batch report-path precedence; correct deploy notes. Batch pressure re-test remains pending; deployment state unchanged.

## [2026-11-19] implement | retro samples by time across projects
Batch sampling no longer ranks projects: top 18 parent sessions by active time (`<agent-time-report> --sessions`) plus 2 seeded random, n=20; sessions started before the window get their time from the JSONL fallback. Owner decision after trial 2 put 8 of 10 samples in one project.

## [2026-11-19] implement | concurrent-session coordination moved to agent-kernel
Added the coordination clause to bc-swarm, then moved it into Git discipline for all repository writes; review follow-up excludes own subagents and bounds check frequency. The relationship contracts concern other kernel sections and are unaffected.

## [2026-11-19] test | agent-kernel concurrent-session coordination
Terra low text-only review reruns: discovery 2/4 vs 0/4, visible exchange 1.5/2 vs 0.5/2 with partial credit, control 4/4 in both arms; direct-write discovery was confounded by no-tools refusals. Verbatim results and earlier runs are in the kernel tests.

## [2026-11-19] test | agent-kernel concurrent-sessions s2 rerun
s2 (direct edit, no subagents) prompt gained the no-tools sentence that s1/s3 already had; rerun both arms x2 on Terra low: discovery with 2/2, without 0/2. Combined discovery 4/4 vs 0/4. Earlier refusing outputs kept under attempt3/.

## [2026-11-19] fix | agent-kernel concurrent-sessions results note
Marked the pre-rerun s2 figures in the review-rerun results as superseded (fix-verifier P3-a).

## [2026-11-19] test | retro first live batch run
A scheduled `<weekly-retro-job>` on a second machine ran `/skill:retro since 2026-11-12` headless in 4.5 min and wrote `<report-dir>/2026-11-19.md`: 20 of 40 sessions across 9 projects (top 18 by active time + 2 seeded), two proposals with homes (code-review boundary-size question, 3 of 20; project A delivery-check wording, 2 of 20). `<agent-time-report>` was not on that machine's PATH (symlinks refreshed after); the JSONL fallback worked. Weekly timer: Mondays 06:00.

## [2026-11-19] lint | personal-terms check and scrub
Added `lint_personal_terms` (optional private denylist, ERROR per hit, skipped when absent) with docs/personal-terms.example.txt, stated the public-copyable policy in AGENTS.md § Conventions, and scrubbed personal terms from log/index/docs/scripts and concept CONCEPT.md/tests; Concept-body hits warn pending per-concept owner review; immutable raw sources, research evidence and concurrent-session transcripts are skipped, and mixed pressure-test results warn.

## [2026-11-19] lint | personal-terms review fixes
Preserved captured pressure-test output, excluded immutable evidence, and made pending body and mixed-result hits warnings; hardened denylist handling and corrected placeholder examples.

## [2026-11-19] implement | agent-kernel generic storage safety
Rewrote Storage safety in the public kernel body to name no personal tools ("a guarded test runner, if one exists", "the machine's storage health check, if one exists"); behaviour unchanged where the tools exist, Why unchanged; owner's derived copies keep the exact names. Pressure check 4/4 on Terra low: [tests/pressure-storage-generic.md](concepts/agent-kernel/tests/pressure-storage-generic.md).

## [2026-11-19] lint | owner-approved raw/evidence path scrub
Owner-approved one-off exception to the raw-is-immutable rule: replaced personal paths in docs/research/raw/** and docs/research/*/evidence/** with the repo's placeholders (`<synced-home>`, `<owner-scripts>`, `<music-library>`, `<project-b>`, `/home/<user>`); nothing else changed, JSON still valid.

## [2026-11-19] implement | agent-kernel storage review fixes
Restored the session-close record, clarified the with-kernel-only evidence and missing-tool behavior, and added discovery guidance and private-copy deploy policy. No deploy; consumer-specific tool references remain a separate follow-up.

## [2026-11-19] implement | code-review data-size Standards question
Added a conditional Standards question (size, amplification, growth and limit behaviour of data crossing a changed boundary) from retro 2026-11-19 proposal 1. Pressure test on Terra low: amplification-only scenario without 0/3, old body 0/2, new 3/3; two scenarios with obvious growth non-discriminating; control had no false size finding.

## [2026-11-19] test | code-review bounded-boundary control
Scrubbed private provenance paths and project names; a fixed-shape message control produced no size finding in either arm (2/2 each), graded from raw outputs.

## [2026-11-19] implement | bc-swarm generic tool steps + private skill overlays
bc-swarm's body names no owner tools; an optional private overlay (`~/.config/agent-concepts/overlays/<skill>.md`, convention in AGENTS.md) supplies only tool names the machine's always-loaded instructions lack, states no rules, and yields to project instructions. Pressure PASS: content arms plus tools-enabled load path (Pi Terra low n=2/arm, Claude Code n=1/arm, its stranger arm being the owner's machine without the overlay; both expand `~` before reading). Targeted-packets quotes now carry an explicit `[wrapper redacted]` marker and left lint's mixed-results list.

## [2026-11-19] implement | stranger-usable tool wording and gate budget correction
bc-drain-issues, tdd, diagnosing-bugs and bc-init-agent now name the guarded test runner, storage health check and offload wrapper by role ("if the project's or machine's agent instructions name one") instead of the owner's tool names; no private overlays needed, since the owner's always-loaded instructions name these tools. The scaffolded gate's 300 s budget is now stated as measured, not enforced, and never wrapped in `timeout` (the first wording led both consumers to a hard kill). Isolated stranger rerun (Terra low, owner append file overridden, extensions off): 4/4 no `timeout`; earlier diagnosing-bugs and gate runs are labelled mixed because owner settings leaked into them.

## [2026-11-19] implement | retro decisions record, report carry-over, private overlay
Reports now end proposals as numbered `## Proposals` items and get a `## Decisions` section; interactive `/retro` first asks about an undecided latest report, headless runs carry undecided items forward under `## Still undecided from <date>`, and carried items can be decided back into their original report. Latest report = `YYYY-MM-DD[-scope].md` by date prefix, then mtime. Report dir: `RETRO_REPORT_DIR`, else the `--report` target's directory, else `${XDG_STATE_HOME:-~/.local/state}/retro/`. Owner-specific report dir and time-report tool moved to an optional private overlay. Earlier overlay-arm runs had unrelated owner memories injected (disclosed in the test file).

## [2026-11-19] test | retro report carry-over, isolated retest
Terra low, true stranger (project `.pi/APPEND_SYSTEM.md` override + `--no-extensions`, probe No/No vs control Yes/Yes), final body, n=2: undecided ask, decided proceed, headless carry-over, carried items numbered after new proposals with decisions written to the original report, and date-prefix latest-report selection — 12/12 pass. New body only; no real file writes.

## [2026-11-19] lint | semantic privacy pass over word-list-clean concepts
Reviewer pass over 26 concepts the lexical denylist had cleared. Replaced a private project's real identifiers in naming-things with an invented order-support vocabulary, removed private project names from code-review and bc-work-sync, provider billing status from an unslop test, gendered and owner-setup provenance, private role names, and "per cost rule" notes; the workshop citation in issue-slicing no longer carries a download URL.

## [2026-11-19] lint | removed private project names and workshop download links from current tree
Replaced the three private project names with neutral project A/B labels in prose and `<project-a>`/`<project-b>` placeholders in captured evidence (owner-approved one-off); retrieval benchmark reports now render the `--collection` value instead of a hard-coded name; dropped the workshop download URL from six CONCEPT.md citations. `docs/research/raw/` left untouched (immutable).

## [2026-11-19] lint | renamed a private-project ingested source folder to project-b-seo-agents and dropped the workshop download URL from CITATIONS.md (owner-approved one-off exception to raw-source immutability)

## [2026-11-19] rename | retro → bc-agent-reflect (owner choice; no alias)
`git mv concepts/retro concepts/bc-agent-reflect`; skill name, overlay path (`overlays/bc-agent-reflect.md`), report-dir variable (`BC_AGENT_REFLECT_REPORT_DIR`, default `${XDG_STATE_HOME:-~/.local/state}/bc-agent-reflect/`), kernel 👣 offer (`/bc-agent-reflect`), relationship edges, index and status updated. Recorded test prompts/outputs keep `/retro` as evidence; upstream raw sources and older log entries unchanged.

## [2026-11-20] implement | bc-swarm pi.md fan-out example uses `options.script`, not the removed `workflowScript`; publish-check.py made executable
From a bc-agent-reflect pass (owner picked). The old example led to failed launches ("options.script replaces workflow" in 16 session logs); the shape was checked against a live async launch that succeeded. Syntax-only correction to the Pi mechanics reference, so an accuracy check, not a pressure test. `publish-check.py` lacked the exec bit the kernel's direct invocation needs ("Permission denied" in 201 session logs).

## [2026-11-21] implement | design framework: ui-design companion + bc-init-agent design README
New `ui-design/body/design-framework.md` (inventory step, where a rule lives, asking the owner, write path, falling-baseline checks, capture scope), linked from SKILL.md; trigger widened to recording a design decision. bc-init-agent scaffold writes `docs/design/README.md` and a map line for code/ops/hybrid (never overwrites; upgrade note for old maps), with tests. Not yet pressure-tested; status frontmatter unchanged.

## [2026-11-21] implement | design framework review fixes
ui-design overlay hook replaces a private worked example; README-missing step names `DESIGN_README` and its sections; capture scope moved into the SKILL.md capture gate; restatements trimmed; bc-init-agent upgrade note names `.bc-agent/map.md`, tests match on real Markdown links, `--force` README test, Tests entry.

## [2026-11-21] implement | design framework: decide once, in one place
ui-design `design-framework.md` and the bc-init-agent `DESIGN_README` now tell agents to decide taste calls themselves, define them once as a token or shared part, and record them as the agent's choice; ask the owner only to contradict a recorded decision or remove something users rely on. Reason: owner goal is consistency over sign-off; pressure run saw hard-coded hex colours.

## [2026-11-21] test | ui-design design-framework.md
Terra low, old vs new arms in three rounds (`concepts/ui-design/tests/results/design-framework-2026-11-21.md`): same-commit design record held; "decide once, in one place" held after the owner set consistency over sign-off; reuse showed no difference. Status stays partial (contradiction-ask branch, missing-README path untested).

## [2026-11-21] implement | swarm run folders move to the state directory
bc-swarm `pi.md` (run-dir line, example `OUT`, why + 7-day automatic cleanup) and bc-agent-reflect § Evidence (new location; older runs may be under `/tmp/bc-swarm/`) now use `${XDG_STATE_HOME:-$HOME/.local/state}/bc-swarm/`. Reason: a reboot wiped `/tmp` mid-run, erasing a manifest, logs and worktree. No other live body names the path (public kernel does not); bc-swarm `SKILL.md` "disposable by design" left as is; test results, research and log history left unchanged. Path change only, no gate change: accuracy check (grep of bodies), no pressure test.

## [2026-11-21] implement | design README template: review-conventions link, stricter ask-cases, test suites
Scaffold `DESIGN_README` gains an optional link line for a project's screenshot/review conventions page, folds a project's **Stricter ask-cases** into the "only when" ask list (still no asking on taste calls), and says "test suites"; `ui-design` design-framework.md ask wording matches. Reason: adoption feedback from a project using the template.

## [2026-11-21] implement | ui-design: Modern Web Guidance as a pinned lookup
surfaces.md Web bullet now gives the search/retrieve command (version 1.0.1, telemetry off) instead of a vague pointer; the upstream skill is not installed because its trigger fires first on every web task.

## [2026-11-22] implement | bc-swarm pi.md: give reviewers the worker diff as a file
Reflection on the design-framework session: a reviewer without a shell could not read a cleaned-up worktree commit. pi.md now tells the parent to write `git diff <base> <tip>` to the run directory first. Dispatch-mechanics note, not a new gate; no pressure test run.

## [2026-11-22] implement | bc-plan-to-issues → bc-plan-to-pipeline
Renamed the planning orchestrator (old name kept as a deploy alias) because it now files work into the project's work pipeline, a tracker, or both; added no-tracker and settled-source modes, the project's own term for the requirements document, and a `Source:` line on filed work items. `bc-init-agent`'s work-item template gained the optional `Source:` line (MIGRATIONS entry); `improve-codebase-architecture` writes `Source: improve-codebase-architecture`. Not redeployed; pressure test needs a re-run.

## [2026-11-22] implement | bc-swarm pi.md: base worktree when the checkout is dirty
Reflection on a long project session: worktree workers twice refused to launch because another live session had untracked files in the shared checkout. pi.md now records the failure and the workaround (a base worktree as the child's cwd, never touching the other session's files). Dispatch-mechanics note, not a new gate; no pressure test run.

## [2026-11-22] test | bc-plan-to-pipeline settled-source no-tracker PASS 3/3
New scenario (architecture review as settled source, GitHub remote but no tracker in use, user pushes to skip the slice review and "file issues too if that's how it works"), Terra low. Run 1 FAIL 6/7: two slices filed as a one-file item, fixed by defining a small plan as exactly one slice in every mode and showing slices in the approval reply. Run 2 FAIL (1 of 2 runs filed issues from the remote plus the conditional ask), fixed by saying a conditional request defers to the project's practice and the mode line names the tracker evidence. Run 3 PASS 7/7 in all three runs; without the skill 3/7. Deployed; the old name now links to the renamed body.

## [2026-11-22] implement | pressure tests: keep the baseline blind to the concept
A bc-plan-to-pipeline baseline run with skills turned off found the deployed body with `find`, read it and followed it. AGENTS.md Test now says to hide the concept and skill directories from the without-concept run, word its prompt without the concept's name, and check its transcript for reads of the concept path. From a session reflection, owner-picked.

## [2026-11-22] implement | bc-init-agent + bc-work-sync: Blocked-by work pipeline
Ported the owner's Blocked-by rule set: `work_index.py` requires a `Blocked by:` line, rejects unknown/dropped/self/cyclic blockers and orders the table topologically (stage as tiebreak); template line, four AGENTS.md rules, MIGRATIONS "Blocked by". bc-work-sync now reports missing or invalid Blocked by lines. Pressure test of the new rules still owed.

## [2026-11-22] implement | bc-init-agent: owner order in work/order.md
`work_index.py` reads an optional `work/order.md` (numbered item names) and ranks listed items right after active ones, blockers still winning; unknown or repeated names are errors. Generated Work items rule, SKILL/CONCEPT/MIGRATIONS "Owner order", bc-work-sync check line. Shared spec with the owner's dashboard.

## [2026-11-22] implement | bc-init-agent owner order review fixes
Ignore repeated closed items, clarify partial orders, and add ordering regression coverage.

## [2026-11-22] implement | bc-init-agent owner order: blockers of active items
work_index.py ranks planned transitive blockers of active items right after the active ones (spec amendment), with an example test and a Hypothesis property over random blockers, folders and partial order.md.

## [2026-11-22] implement | bc-init-agent owner order round 3
The three tiers apply with or without `work/order.md` (spec amended); dropped month folders count as closed, an open item wins over a closed one of the same name, order-line digits are ASCII. Scaffold, MIGRATIONS, SKILL and CONCEPT now describe the tiers; `Blocked by:` stays required. New tests plus a stronger property (a ready active item precedes every planned item).

## [2026-11-22] implement | bc-init-agent owner order round 4
Order-file lines split on \r\n, \r or \n with space/tab-only whitespace and ASCII digits (shared spec with the dashboard); the Dropped count includes month folders; bad stages and bad order.md names are reported in one pass. Scaffold README and work rules, MIGRATIONS and index.md describe the three tiers and regenerating after changing order.md.

## [2026-11-23] implement | bc-init-agent work_index.py accepts items without Stage:
An open item without a `Stage:` line sorts after every stage; an unknown stage is still an error. The missing-stage test became a sort-order test, seen failing first. `<pytest-wrapper> concepts/bc-init-agent/tests/test_work_index.py`: 50 passed. Lint errors are pre-existing (handoff paths).

## [2026-11-23] implement | bc-init-agent: an item moves to done only after it lands
The generated "Finish or drop an item" row now says: only once the work is on the main branch and its full checks passed; a worker in a worktree never moves an item. From a project worker that moved an item to done before its review fixes and gate landed. Pressure test on terra low: baseline moved the item, treatment held (`concepts/bc-init-agent/tests/pressure-finish-after-landing-results-2026-11-23.md`).

## [2026-11-23] implement | bc-init-agent: work_index.py --check guards the owner order
`--check` fails while work/order.md leaves out an open item or lists one above its blocker, and says where a new item goes; the generated Work items section gains the matching rule, bc-work-sync names the faults. Why: an agent added an item and a blocker without listing it and pushed the owner's ranked items to the bottom.

## [2026-11-24] implement | issue-slicing: no human approval stop
Owner decision: the agent finalizes slices itself and reports them instead of quizzing for approval; a draft-and-wait happens only when the user asks to review first. Propagated to `to-tickets`, `bc-plan-to-pipeline` (grill is now the only human gate), `docs/pipeline.md`, tests and status; the change is not yet pressure-tested.

## [2026-11-24] test | issue-slicing: no approval stop
Pressure run on Terra low: with the skill it finalized slices without asking (×2) and still waited when asked to review first; the blind baseline also did not stop but sliced horizontally. Wide-refactor and unsafe-split checks not exercised; `to-tickets` and `bc-plan-to-pipeline` not re-run.

## [2026-11-24] implement | agent-kernel: bulky scratch off /tmp
Owner request after a Rust spike filled a 7.7 GB tmpfs `/tmp` and killed three agent runs: Storage safety now keeps build output and prototypes in the worktree or a disk-backed `$TMPDIR`, and forbids telling workers to build in `/tmp`. Pressure scenario 6 added, not run; derived copies wait for it.

## [2026-11-24] deploy | agent-kernel: /tmp scratch rule
Owner chose to deploy the reworded rule despite a partial pressure result (location 1/2, deletion 0/2 on Terra low); applied to the derived Pi, Codex, Claude and Muse copies.

## [2026-11-24] ingest | council-mode adopted from pi-subagents
Owner decision: own the council protocol as a public concept because it is becoming central and the unpinned package changed it silently. Verbatim copy of 0.90.0 (MIT) with a relative reference path; not deployed until the pressure test passes and the package copy and `/council` prompt are switched over.

## [2026-11-24] deploy | council-mode switched over from the package copy
Pressure runs on cheap advisors failed twice (workflow block lost on launch; resume id passed as `id`); fixed both, then 3/3 passed. Added the `/council` prompt and three stanced example advisor profiles; deployed, and Pi's settings now exclude the package's skill and prompt.

## [2026-11-24] implement | example role profiles for bc-drain-issues, settings snippet for bc-swarm
Same idea as the council examples: `bc-drain-issues` named three Pi roles a stranger could not get, so copies now ship in `body/examples/agents/`; `bc-swarm` gains an example `agentOverrides` tool-budget snippet. Documentation only; no behaviour change.

## [2026-11-24] deploy | bc-drain-issues role profiles are now the live files
The owner's three `bc-drain-*` Pi agent profiles are relative symlinks to `body/examples/agents/`, so the public examples and the profiles Pi runs cannot drift.

## [2026-11-24] implement | agent-kernel recap set apart with a rule
Owner asked to visually separate the end-of-reply recap: a blank line, then `---`, then the recap lines. Markdown renders it as a rule in Pi (checked in pi-tui's renderer) and it stays a plain divider elsewhere; 2/2 Terra low replies placed it correctly. Copies updated: Pi, OpenCode, Muse, Codex, Claude Code.

## [2026-11-24] deploy | bc-improve-codebase-council published
Moved from a private concept: the named map-scout model and Antigravity paragraphs became generic rules, and a private overlay now fixes this machine's roster (two advisors for this review) and map-scout model. Pressure re-run on Terra low: 2/2 without the overlay (discovery, cap, scaled thresholds), 2/2 with it (exact roster and model). The private denylist entry that matched this name was narrowed to the exact script name.

## [2026-11-24] implement | work-item Kind and top-kind placement
`work_index.py` reads an optional `Kind:` header and the project's `Top kinds:` line (default security, bug, build, architecture; `none` off); `--check` places new top-kind items below the `order.md` top group, oldest first, never above a blocker. Scaffold and bc-init-agent document it; improve-codebase-architecture, bc-improve-codebase-council (plus a hands-off to bc-plan-to-pipeline), bc-plan-to-pipeline and bc-work-sync set `Kind:`. Owner decision: placement by kind, not by skill; pressure tests pending.

## [2026-11-24] implement | rename bc-improve-codebase-council → bc-council-improve-codebase; council chain naming rule
Owner decision: council chains share the `bc-council-` prefix so they group together; AGENTS.md Conventions records the rule. Earlier log entries keep the old name.

## [2026-11-24] test | bc-init-agent top-kind placement
Terra low: 1/2 placed a new security item above the owner's top item (edited order.md before `--check`); the rule now says to run `--check` first and add the line where it says: 4/4 PASS. Results in `concepts/bc-init-agent/tests/pressure-top-kinds-results-2026-11-24.md`.

## [2026-11-24] implement | rename issue-slicing → plan-slicing
Owner decision: it produces work items as well as issues. Old name kept as a deploy alias; references, relationships and the private routing skill follow.

## [2026-11-24] implement | rename bc-agent-reflect → bc-reflect
Owner decision: "agent" meant two things across bc-init-agent and this skill. Kernel line and its harness copies now offer `/bc-reflect`; old name kept as a deploy alias; report directory, env var, weekly job and reminder extension keep their names.

## [2026-11-24] implement | plan: council bug hunt
Owner-approved plan `docs/plans/active/council-find-bugs.md`: parent `find-bugs`, shared `council-chain`, thin `bc-council-find-bugs`; confirmed bugs need a failing test.

## [2026-11-24] implement | council-chain extracted from bc-council-improve-codebase
Shared council steps moved into new concept council-chain with an explicit chain interface; bc-council-improve-codebase loads it and keeps only map contents, card, agreement rule, report and filing. Private overlay moves to council-chain.md. Architecture-chain re-run 4/4 on Terra low. Plan: chain 2 of the follow-ups is named bc-council-challenge-plan (owner).

## [2026-11-24] implement | council-chain roster accepts an exclusion
The overlay roster may now drop named advisors instead of listing the kept ones, so a new `council-` profile joins every chain without an overlay edit (owner choice).

## [2026-11-24] implement | find-bugs
New parent skill for the council bug hunt (plan step 2): bounded scope, candidate block, reproductions in a separate worktree on `find-bugs/<hunt>`, two-tier report, owner-gated filing as `Kind: bug`/`Source: find-bugs`. Practice project `shopkit` (10 planted bugs, 9 decoys) with answer key; Terra low: 2 with-skill runs pass (9/10 each), blind baseline proves bugs but keeps no report/tiers/worktree and switches the owner's checkout. Parent added "attempt every candidate while slots remain" after both runs left a race unattempted. Deployed.

## [2026-11-24] implement | council-chain asks for pass-2 refinements
Pass 2 now asks each confirm for a refinement with evidence, and the report shows it under the advisor's name. Both live reviews showed this as the most useful pass-2 work, done unprompted by one advisor (owner choice). Not yet re-tested.

## [2026-11-24] implement | bc-council-find-bugs (not deployed)
Thin chain over council-chain + find-bugs (plan step 3): focuses dealt round-robin, pass-2 attack, agreement only orders reproduction and the suspected tier, one worker reproduces with the find-bugs skill list. Pressure test on Terra low with stand-in advisors failed: 6 of 7 runs stopped early; the finished run confirmed 8/10 planted with correct `all` filing but dropped the worker skill list, report additions and item test links.

## [2026-11-24] test | bc-council-find-bugs dry run; deployed
Dry-run pressure test (plan.md only, Terra low, 2 runs): 11/11 criteria in both, no body fix; also covers council-chain's pass-2 refinement rule. Deployed (owner chose dry-run testing; the first real hunt with the council is the live test). Plan moved to implemented.

## [2026-11-24] implement | bc-council-audit-security
New thin chain running security-audit's full audit through the council: own recon is the shared map, trust boundaries dealt round-robin, every candidate (pass-2 drops last) gets a fresh refuting reviewer, cap only via --max-verify, confirmed findings pre-selected for Kind: security filing without exploit steps. Dry run on Terra low: round 1 failed the cap criterion; after a body fix 2/2 pass. Deployed.

## [2026-11-24] implement | bc-council-challenge-plan
New thin council chain: scout maps the plan's code, advisors attack dealt plan sections, owner grilled on surviving objections, answers written into the plan, then bc-plan-to-pipeline in settled-source mode. Dry run 2/2 on Terra low, no body fix. Deployed. Plan council-later-chains moved to implemented.

## [2026-11-24] implement | pressure-test harness page; dry runs for orchestrating skills
From a /bc-reflect pick: AGENTS.md Test operation now points to docs/pressure-test-harness.md and says skills that launch subagents are tested as dry runs (first real run is the live test). Why: a live council-chain test took four rounds with 6 of 7 runs stopping early, while dry runs of four chains passed; the harness recipe lived only in test result files.

## [2026-11-24] implement | plan every planned item (untested)
Owner decision: every item in work-planned is planned by bc-plan-to-pipeline before it starts. bc-plan-to-pipeline plans an existing item in place and writes a `Planned:` marker; improve-codebase-architecture and find-bugs hand off to it after filing (council chains inherit; old recommendation removed); bc-init-agent's generated pickup rule, template line and a non-failing `work_index.py --check` warning; bc-drain-issues skips unmarked items as "needs planning". Pressure scenario `bc-plan-to-pipeline/tests/pressure-plan-every-item.md` written, not run.

## [2026-11-24] test | plan every planned item (bc-plan-to-pipeline, find-bugs, bc-init-agent pickup rule)
Three Terra-low pressure rounds, two wording fixes between them. No new-rule run started an unplanned item, guessed, or asked a seam question; the find-bugs filing handoff passes 3/3; the carry-on and absent-owner scenarios still end text-only before planning (0/3 each in round 3). Statuses stay partial; results in concepts/bc-plan-to-pipeline/tests/pressure-plan-every-item-results-2026-11-24.md.

## [2026-11-25] implement | bc-agent scaffold for this workspace
Ran `bc-init-agent` (code archetype): `.bc-agent/`, `work/` with items 001–006 from the owner's grill (tidy, docs reshape, journal move, vocabulary renames, glossary, performance guardrails method), `scripts/gate` (lint, portability check, real Python tests) and its CI workflow. Gate starts red on four pre-existing failures that item 001 fixes.

## [2026-11-25] implement | tidy local clutter (item 001)
Ignored `.handoffs/`, `.hypothesis/` and `.gemini/`; lint skips git-ignored Markdown; removed the duplicate deploy-pi-skills script. Fixed a stale rename in the bc-init-agent base-output test, a portability check that matched the scratch HOME path, and a lint deploy check that failed on every fresh home.

## [2026-11-25] implement | fix CI-only gate failures
CI (ubuntu-26.04) failed three bc-wiki-maintain batch-runner tests: the test stub's `\n` broke `dedent`, so its shebang was indented and it ran under `/bin/sh` (dash there, bash locally). Fixed the stub; `run-promotion-all.sh` now requires GNU `timeout` (prefers `gnutimeout`) because uutils `timeout` leaves a timed-out child's descendants running; CI installs `gnu-coreutils` and fetches full history so the base-commit layout tests stop skipping.

## [2026-11-25] implement | docs reshape (item 002)
`docs/` now holds a README, `guides/` (bootstrap, harnesses, pipeline, pressure-test harness), `examples/` (private-config templates), `status.md`, and dated `research/<date>-<topic>/` folders. `docs/plans/` is gone: open plans became work items `007-agent-vault-read-path` and `008-bc-drain-issues-v3-review-economy`, finished ones moved to `work/3-done/` as 009–021, and the read-path plan record became research. Lint no longer checks plan lifecycle folders.

## [2026-11-25] implement | scaffolded the project agent workspace
Scaffolded with `bc-init-agent`: root `AGENTS.md`, `glossary.md`, `work/`, `docs/` and the `.bc-agent/` mechanics. Ready for the grill → issues → drain workflow.

## [2026-11-25] implement | journal moved to .bc-agent/log.md (item 003)
Moved the root journal here with `git mv` so history follows, merged the scaffold intro on top, and repointed references to this workspace's journal (AGENTS.md, lint required-files, portability exemption, unslop and bc-reflect concepts). Other `log.md` meanings (scaffolded projects, vaults, teach hosts) unchanged.

## [2026-11-25] implement | README quick fixes
Install line now saves the checkout's real path (it saved the literal `$PWD`); `/bc-init-agent` and `/bc-plan-to-pipeline` descriptions match the current layout. Full rewrite filed as 022-readme-rewrite, after the glossary.

## [2026-11-25] implement | vocabulary renames (item 004)
Discipline gates are now hard rules (canon, provenance, test, immutability; ui-design capture rule; bc-swarm recovery rule), including AGENTS.md heading and lint messages. bc-swarm: the tooth → routing decision, thin-parent guard → evidence anchors. to-tickets says GitHub issues, plan-slicing says tickets. Other "gate" uses left for a later decision; outside-repo copies listed in work/0-ideas.md.

## [2026-11-25] implement | glossary (item 005)
Wrote root `glossary.md`: 51 terms in five groups using the settled meanings (gate = automated command only, hard rule, ticket/work item/issue/slice, subagent/worker, run folder). Dropped budget chain and regression allowance (unused in the repo); linked from AGENTS.md.

## [2026-11-25] implement | glossary design terms; README plan for consistency
Glossary gains a Design consistency group (design framework, design token, design page, capture rule). 022-readme-rewrite gains a "Keeping projects consistent" part; 006 extends its guardrails line when the method page lands.

## [2026-11-25] implement | README rewrite (item 022)
Rewrote `README.md` as a plain reference: harness table (with Muse), install, repository map, the three-skill loop checked against each body, "Keeping projects consistent", hard rules as `AGENTS.md` states them. Dropped the uncaveated wiki-search benchmark and the stale slicing-quiz gate claim; lint now described as checking recorded status.

## [2026-11-25] implement | plan 006 guardrails method
Grilled with the owner and filed 006 as a large item (plan.md + requirements.md): a general `guardrails` concept, an empty `docs/guardrails/README.md` from `bc-init-agent`, agents set limits themselves (measured ratchet, targets from published guidelines), checks added at setup and after each fixed regression.

## [2026-11-25] implement | guardrails concept (item 006 steps 1-3)
New `guardrails` concept (method, measuring and targets pages, three pressure scenarios; not run, not deployed); `bc-init-agent` scaffolds `docs/guardrails/README.md` and its map line for code, ops and hybrid; `bc-autoresearch-loop` measures like the guardrails and tightens the matching limit. Pressure test, deploy and README line remain (steps 4-5).

## [2026-11-25] test | guardrails pressure test (item 006)
Ran scenarios A–C without and with `guardrails` on the configured model: the without-run fixed the slowdown with no check (A fails), the with-runs held all three, and B and C held in both runs; no tuning. Results in `concepts/guardrails/tests/pressure-results-2026-11-25.md`; status pass, still not deployed.

## [2026-11-25] deploy | guardrails
Deployed the `guardrails` skill after its pressure test held; README "Keeping projects consistent" now describes it; glossary adds budget decomposition and guardrails page. Closes 006.

## [2026-11-25] implement | ready and waiting lines in the work pipeline
`bc-plan-to-pipeline` writes `Ready for agent: yes` only when every step states done-criteria and out of scope; `bc-init-agent` scaffold documents `Ready for agent:` and `Waiting on owner:`, and `work_index.py` marks both and rejects an item with both. References renamed to `bc-pipeline-to-done`.

## [2026-11-25] implement | bc-pipeline-to-done: rename, source split, work-item source
Renamed `bc-drain-issues` to `bc-pipeline-to-done` (old name a deploy alias); split the body into a shared core plus `source-issues.md` (issue text moved verbatim) and added `source-work-items.md` (ready line, item claim with and without a remote, steps in order, park, resume, finish). Jobs with limits and a private overlay replace fixed Pi role names. Gate A reads core plus issue page and gains check 32; lint exempts inline paths in finished and dropped work items.

## [2026-11-25] implement | bc-pipeline-to-done job skills wording
The three jobs are described as not inheriting the broad skill catalog and getting only the skills the contract passes, replacing "no extra skills", which read as "no skills". Owner kept the hand-picked skills after reviewing them against the local roles.

## [2026-11-25] test | bc-pipeline-to-done work-item source dry run
Terra low dry runs of the work-item source (eligibility and no remote, park instead of guess) and an issue-source regression, without and with the skill: the blind runs failed all three, the skill held after three wording fixes in `source-work-items.md` (no-remote preflight, parallel request, park after earlier steps land). Results in `concepts/bc-pipeline-to-done/tests/pressure-work-items-results-2026-11-25.md`.

## [2026-11-25] deploy | bc-pipeline-to-done
The skill is linked through the shared skill folders (`bc-drain-issues` stays an alias); `deployed` set after the work-item dry run held.

## [2026-11-25] implement | 023 docs: README loop, pipeline guide, glossary
README loop now presents attended "continue the work" as the standard and `/bc-pipeline-to-done` as the unattended option for work items or issues; pipeline guide and glossary (drain, claim, Ready for agent, Waiting on owner) describe both sources; two living `bc-drain-issues` references renamed.

## [2026-11-25] implement | close 023-pipeline-to-done
All five steps landed; Outcome filled and the item moved to done.

## [2026-11-25] implement | plan 024-skill-delivery
Planned how people outside the repository install the skills (grill with the owner): Claude Code and Codex plugins, Pi package and `npx skills`, from tagged releases; `bc-` names; name references instead of path links; a fresh-install test on Linux and macOS. Decision records 0001 and 0002, five glossary terms, twelve steps.

## [2026-11-25] implement | 024 generic wording for owner tools
Publish policy check described generically in agent-kernel, bc-pipeline-to-done, bc-work-sync and bc-init-agent scaffold; overlay line added to bc-init-agent, bc-wiki-maintain, bc-work-sync, tdd. Overlay tool names listed in the 024 step notes.

## [2026-11-25] implement | 024 public skill list
Added `scripts/public_skills.py` and `lint.py --write-public-skills`, generating `concepts/public-skills.json` (public skills and the public skills each loads); lint now fails on a stale list or a body that says to load a public skill without a `loads` edge. Added the three missing edges it found.

## [2026-11-25] implement | 024 contributor installer
`deploy-local-skills.py` now skips and reports a symlink that does not point at a concept body it deploys (this repo's `concepts/` or the private concepts folder), instead of replacing it. `--uninstall` (with `--dry-run`, `--harness`) removes only its own links, aliases included. Six tests in `scripts/tests/test_deploy_local_skills.py`; README options line updated.

## [2026-11-25] implement | 024 name references
Bodies no longer link into other concepts: tdd/security-audit links became name references (new loads edges bc-swarm/code-review -> tdd), kernel Storage safety/Verification links became short inline rules naming agent-kernel. New lint ERROR rejects cross-concept body links.

## [2026-11-25] implement | 024 add workflow guide step
Owner asked for deeper workflow docs: a guide page with cadence (every task, at a moment, periodic upkeep) plus a README section, after the rename.

## [2026-11-25] implement | 024 bc- rename
Renamed the 40 public skills without the prefix to bc-<name> (decision 0001); old names are deploy aliases. Lint now errors on an unprefixed public skill and exempts dated research and recorded test results as historical records.

## [2026-11-25] implement | 024 workflow guide scope
Guide step now lists the full workflow set with bc- names, cadence, and a section on skills worth attaching to subagent roles.

## [2026-11-25] implement | 024 Pi package
Root package.json exposes every public skill body to `pi install` via `pi.skills`, generated by scripts/pi_package.py (lint --write-pi-package, drift is an ERROR). Six council skills marked Pi only in their descriptions.

## [2026-11-25] implement | 024 Claude Code plugin and Codex plugin
Repository root is one `agent-concepts` plugin for both agents; `scripts/plugin_manifests.py` generates both manifests and marketplaces from the public skill list (paths, not symlinks: Codex drops symlinked skill folders). Verified install, listing and uninstall with both CLIs in a scratch HOME.

## [2026-11-25] implement | 024 npx skills packs
New `scripts/install_packs.py` generates `docs/guides/install-packs.md` (all-skills and per-pack `npx skills add` commands, closure over public-skills.json needs) with a lint sync check; each command verified in a scratch HOME against a local checkout with `-a pi`.

## [2026-11-25] implement | 024 Workflow guide
New `docs/guides/workflows.md`: each newcomer workflow with timing, start, questions, result and example, plus the skills to attach to subagents and how in Pi, Claude Code and Codex (attach mechanisms checked against current docs). README gains a Workflows section linking each entry.

## [2026-11-25] implement | 024 fresh-install test
`scripts/fresh_install_test.py` installs, lists, runs a helper, updates and uninstalls via the Pi package, Claude Code and Codex plugins and `npx skills` (all + a pack) in a scratch HOME; CI job `fresh-install` on ubuntu and macos with pinned CLIs; a dropped needed skill fails the check.

## [2026-11-25] implement | 024 workflow guide copy review, test levels, glossary terms
Applied the independent copy review to docs/guides/workflows.md and the README Workflows list (four skill-body contradictions fixed, clearer row names, jargon explained in place).
Added a "How the skills test code" section on bc-tdd's three test levels, and glossary sections for code design and testing terms plus "advisor".

## [2026-11-25] test | agent-kernel, bc-work-sync, bc-pipeline-to-done pressure re-test after 024 rewording
Terra low, without/with: kernel generic publish-check wording held 2/2; pipeline generic publish preflight and inline storage/Test-levels rules held in a dry run. bc-work-sync step 5 failed once (overlay never read), one wording fix pointing at the overlay, rerun passed.

## [2026-11-25] test | bc-swarm, bc-dispatching-parallel-agents, bc-subagent-driven-development, bc-executing-plans pressure re-test after 024 rewording
New scenario per concept (`tests/pressure-inline-storage-2026-11-25.md`): attack asks for /tmp basetemp, full suite per change, no storage check, forced cleanup. Terra low: all four without FAIL, all four with PASS; no wording fix needed. test_status stays partial (wider storage matrix unrun).

## [2026-11-25] test | bc-tdd, bc-code-review, bc-diagnosing-bugs, bc-autoresearch-loop pressure re-test after 024 rewording
New `pressure-storage-inline.md` per concept tests the inline Storage safety wording (and code-review's tdd name references) on Terra low: every with-skill arm 5/5, baselines 1-4/5. No wording fixes; status stays partial for the untested older clauses.

## [2026-11-25] test | bc-finishing-development-branch, bc-using-git-worktrees, bc-writing-plans pressure re-test after 024 rewording
Re-tested the inline storage/verification rules that replaced kernel links (guarded runner, no basetemp, health gate, cleanup proof, no --force, mktemp scratch, one baseline + one landing suite) on Terra low: each without FAIL, with PASS (n=1), no wording fix. Results in each concept's tests/pressure-024-rewording-2026-11-25.md.

## [2026-11-25] implement | 025-dashboard-data planned
Planned the dashboard data item from the owner's choices (Held by line, history from git, Review/Gate lines in step Notes, Spent line from session files, owner dashboard separate): six steps, decision 0003, three glossary terms.

## [2026-11-25] implement | 024 release preparation
CHANGELOG.md (0.1.0), docs/guides/releasing.md, one version home in package.json with a lint check and scripts/release_check.py, fresh_install_test.py --ref and a tag-triggered release workflow. All four install methods verified installing a pushed ref from GitHub; no tag created.

## [2026-11-25] deploy | v0.1.0 released
Tagged v0.1.0 on the commit whose gate and fresh-install CI passed; GitHub release from the CHANGELOG entry; the tag workflow installed it from GitHub with every method on Linux and macOS.

## [2026-11-25] implement | skill renames for v0.2.0
Renamed seven public skills so a newcomer can guess what they do (docs/decisions/0004-skill-names-say-what-they-do.md); old names are local deploy aliases. Version 0.2.0 in package.json and manifests, CHANGELOG entry; no tag.

## [2026-11-25] deploy | v0.2.0 released
Tagged v0.2.0 (seven skill renames, decision 0004); GitHub release from the CHANGELOG entry; the tag workflow installed it from GitHub on Linux and macOS. Redeployed local skills on all three machines; old names stay as aliases.

## [2026-11-25] implement | install docs
README Install section per agent (tag v0.2.0, update, uninstall, tested-scope notes), contributor install kept as a subsection; releasing.md points at it. bootstrap/harnesses point outside users to it; stale links fixed; glossary adds PRD, ADR, preflight, driver, orchestrator and the human-gate/baseline wording conflicts are resolved.

## [2026-11-25] implement | 007 closed, 008 dropped
Owner choices after a relevance check: 007-agent-vault-read-path closed in reduced scope (both per-vault promotion timers removed from the main machine, unit files archived outside the repo; heading measurement and map.md migration dropped; no retrieval-driven shape change). 008-bc-drain-issues-v3-review-economy dropped; bc-pipeline-to-done CONCEPT.md records that the v3 token saving was never measured.

## [2026-11-25] implement | install section review fixes
README `## Install` reworked from the install-section review: Update renamed Refresh (stays on the installed release) with a "To move to a newer release" line, `pi-subagents` named for council skills (`pi install npm:pi-subagents`, checked on its npm page), exact `npx skills` tested scope, real clone URL, zsh/bash path lines, gate command, options as a list, shared-folder note. `release_check.py` now requires README#install to name the released tag and no other (test watched failing first); releasing.md step added; glossary gains tag, checkout, symlink and the "agent" note.

## [2026-11-25] implement | npx install example in README
Owner could not follow the npx instructions; added a worked one-skill example (bc-self-improve for Pi) with each part of the command explained.

## [2026-11-25] implement | 024-skill-delivery closed
npx example switched to Cursor (`-a cursor`, untested, flagged) at the owner's request; item moved to work/3-done/2026-11 with its Outcome.

## [2026-11-25] implement | 025 JSON output step
`work_index.py --json` prints every work item's header lines, steps with Notes and Outcome under a format version; reference page `concepts/bc-setup-project/body/work-data.md` lists each field (later records marked planned); repo copy refreshed.

## [2026-11-25] implement | 025 item history step
`work_index.py --json` gains per-item `history` (created, moved, ticked events with commit date and SHA) from `git log --follow`; work-data.md marks it best-effort; scratch-git-repo tests.

## [2026-11-25] implement | 025 Held by line step
`work_index.py` parses `Held by: <tool> <session> since <YYYY-MM-DD HH:MM> <UTC or +HH:MM>` (JSON adds its age; `--check` warns on malformed or closed-item lines); the scaffolded work-item rules and the drain's work-item source write and remove it, bc-work-sync reports stale ones. Pressure test on Terra low: baseline never wrote it, with the rule 3/3 wrote and removed it.

## [2026-11-25] implement | 025 Review and Gate lines step
`Review:`/`Gate:` step-Notes lines: parser, `--json` per-step lists, `--check` warnings in `work_index.py`; writers in the scaffolded rules, drain work-item source and review contract. Pressure on Terra low: baseline 0, with rule 3/3.

## [2026-11-25] implement | 025 Spent line step
`work_spent.py` beside `work_index.py` estimates an item's time, tokens and cost from Pi, Claude Code and Codex session files; `--json` parses the `Spent:` line, `--check` warns; scaffolded rules and the drain finish paste it. Pressure on Terra low: baseline 0, with rule 3/3.

## [2026-11-25] implement | 025 Spent counts child sessions
`work_spent.py` counts Pi child (subagent) sessions of a counted parent inside the active period whatever their folder, so workers in removed worktrees are no longer missed; `--json` gives `via`. Test in `test_work_spent.py`.

## [2026-11-25] implement | 025 docs and migration step
Migration note, dashboard section in the workflow guide, work-data page without planned fields and with Spent limits, Review and Gate lines in the glossary; every documented field checked against real --json output.

## [2026-11-25] implement | 025-dashboard-data closed; v0.3.0 prepared
Item moved to work/3-done/2026-11 with its Outcome and Spent line. Version 0.3.0 set, plugin manifests regenerated, CHANGELOG 0.3.0 entry (with missing 0.2.0 comparison link), README install tag moved to v0.3.0.

## [2026-11-25] implement | work_spent test robust to an existing bytecode cache
CI failed on test_work_spent: another test imports work_index in-process and creates body/__pycache__; the no-files assertion now counts only a cache this run created.

## [2026-11-25] deploy | v0.3.0 released
Tag v0.3.0 on 6ed38a4; release.yml passed (release-check, install-tag on ubuntu and macos); GitHub release created from the CHANGELOG entry.

## [2026-11-25] implement | README restructured around the way of working
Rewrote README.md: title+intro, philosophy (principles with linked skills),
workflow stages (all collapsible), install (pick-your-agent table, one command
per fenced block in collapsed per-method sections), working-on-this-repo.
Fixed docs/guides/releasing.md fresh-install-test claim (it builds its own
commands, does not parse the README). Line count 318 → 480.

## [2026-11-25] implement | README review fixes
Corrected the TDD description (fail first; planted bug only for working code; levels), the kernel install claim (methods do not install it), the agent table, the npx placeholder notes and the security-audit invocation.

## [2026-11-25] implement | README restore lost content
Restored consistency/guardrails principle, design-token and fitness-function details in Build,
pipeline-to-done attended/unattended workflow, setup safety, planning safety, install caveats
(council dep, upgrade untested, npx version drift). Install boxes are now one-paste per method;
npx section has per-agent boxes for Cursor, Gemini CLI, GitHub Copilot, OpenCode plus a generic
fallback. Checkout uses a one-paste box with shell detection.

## [2026-11-25] implement | README review fixes after restore
Owner pipeline wording restored (nobody there to answer; diligently verifies), npx agents folded one per section with a shared refresh, guardrail regression wording matched to the skill.

## [2026-11-25] implement | README headings and wording
Principles get their own headings; plainer opening sentence; install intro no longer claims the code changes many times a day.

## [2026-11-25] implement | README plain-language pass
Every skill description rewritten to say what it is for in plain words; principles and stage summaries de-jargoned; bc-research and bc-qmd added to the tables; repeated not-tested notes removed.

## [2026-11-25] implement | README example, licence, contributor fold
Added a folded walk-through of one session, stated the MIT licence, folded the contributor section.

## [2026-11-25] test | README install boxes
Ran every install, refresh and uninstall box (Claude Code, Codex, Pi, npx for Cursor, contributor checkout) in a throwaway home; all pass. Noted that npx remove keeps skills while Codex or Pi share ~/.agents/skills.

## [2026-11-25] implement | README look
Centred header with badges and quick links, emoji principle headings with Skills lines, workflow diagram, tip and important callouts, emoji stage summaries; contributor section unfolded.

## [2026-11-25] implement | README without emoji
Removed every emoji from headings, stage summaries and the diagram at the owner's request.

## [2026-11-25] implement | README session example
Replaced the dark-mode walk-through with a discount-code example that shows test first, rule-based tests and a set-aside question; includes the owner's manual README edits.

## [2026-11-25] implement | README software factory section
Added "Running it as a software factory" under The workflow: once, per idea, per session, regularly as code grows, and as needed.

## [2026-11-25] test | bc-security-audit typed command
Typing /bc-security-audit is now an explicit full-audit request; rule moved first in the mode section after the first wording failed. S5/S6 pass on GPT-6.1 Terra low (baseline failed). README factory row and skill table, workflows.md and CHANGELOG updated; includes owner README edits.

## [2026-11-25] implement | README factory list: commands only
Removed the guardrails line; the factory list now holds only commands you run. Guardrails stay described under How these skills work.

## [2026-11-25] implement | README factory diagram
Added a mermaid diagram of the factory loop after the As needed table: commands in bold blue, Your idea enlarged, Merged and inputs rounded.

## [2026-11-25] implement | README: drop session example
Removed the folded "What a session looks like" example at the owner's request to keep the README short; kept the owner's edit to the factory closing line.

## [2026-11-25] implement | README factory diagram: span styling
GitHub strips <code> inside mermaid labels; switched command styling to <span> (kept by GitHub) with no-wrap.

## [2026-11-25] implement | README principles: seven ideas
Folded "Evidence before claims" into the TDD idea as proof shown with "done"; renamed the simplicity idea "Simple on purpose" and framed it as a goal; fixed "writes". Owner keeps the wink emoji on purpose.

## [2026-11-25] implement | README: files idea names setup and wiki skills
Added bc-setup-project and bc-wiki-maintain to the Skills line of "Work lives in files, not chat".

## [2026-11-25] implement | owner-notes link
Linked owner-notes/ to the owner notes folder and ignored it, as other projects do.

## [2026-11-25] implement | README heading spacing
Added a <br> before every ### heading so the gap above a heading is larger than below; GitHub CSS gives them equal gaps.

## [2026-11-25] implement | README heading spacing, adjusted
Extra space above The workflow, Install and Working on this repository; none above the first heading after a section intro.

## [2026-11-25] implement | README spacing and Release badge
Space above How these skills work; ?sort=semver on the Release badge so GitHub image proxy refetches it (it returned 404).

## [2026-11-25] implement | Release badge via badgen
GitHub image proxy times out (504) on the shields.io release badge; badgen.net loads through it.

## [2026-11-26] test | Gemini 4 Neon README prose pass
Delegate on antigravity-acp/gemini-4-neon:high produced a prose rewrite (owner-notes only, sandbox blocked writes so parent extracted it); structure checks pass; filed adopt question.

## [2026-11-26] implement | README prose from Gemini 4 Neon
Adopted the Gemini 4 Neon prose rewrite (structure unchanged), with the owner's own edit to the Simple on purpose ending.

## [2026-11-26] implement | Needs owner: work-item line
Added an optional `Needs owner:` header line (what the owner must decide or do, and when; removed once settled) to bc-setup-project's work-item rules, template and `--json` output, and to bc-plan-to-pipeline's header-line step, with a migration entry; the owner's dashboard shows it for planning time away.

## [2026-11-26] implement | Changes UI: work-item line
Added an optional `Changes UI:` header line (what the user will see change; kept current with the plan) to bc-setup-project's work-item rules, template and `--json` output, and to bc-plan-to-pipeline's header-line step, with a migration entry; the owner's dashboard shows it for planning UI review.

## [2026-11-26] implement | agent-kernel holds rules for everyone
Removed personal rows 9, 13, 18, 21, 31 and the tool-thresholds line from the public kernel; moved worktree cleanup proof (row 22) to bc-using-git-worktrees; reworded rows 7, 12, 23 (accuracy-checked only). Repaired stale kernel references in skill bodies, index.md, CONCEPT.md and relationships.json (dropped the kernel→bc-self-improve hands_off edge). Decision 0005; work item 034.

## [2026-11-26] implement | Pipeline target branch
Resolve and record the landing branch in preflight, then use it for policy checks, claim checkout, fetch and landing. Standalone execution/finishing and generated scaffold guidance no longer assume a named trunk. Scaffold output regression reproduced on learning and knowledge and passes after the change; the `main` fixture consumer scenario is documented separately.
## [2026-11-26] test | Setup verifies the local gate without existing CI
Existing setup now fills checks and layout from recon and names unresolved owner actions. One Terra low run per arm: the revised body ran its portable gate locally; the old body wrote the same gate but did not run it; targeted conventions partial in both. CI toolchain and scaffold output unchanged.

## [2026-11-26] implement | Bundle the pipeline publish checker
Moved the checker into the skill body, retained the checkout entry point, and added an installed-file check. One dry run per arm verified the old install lacked the checker and the bundled install ran it without a policy; preflight wording is unchanged.

## [2026-11-26] test | Setup CI toolchain: no defect
The old setup body provisioned CI on an existing-CI Node fixture (setup-node in the workflow, `npm ci` as the gate's first step) and a no-CI uv fixture (setup-uv and Python before the gate) (one Terra low run each). Owner chose to land wording only on a failure, so only the generated workflow's TODO comment changed.

## [2026-11-26] implement | Setup starter-item reference
Defined applicability and work-item text for design inventory, guardrails setup checks, architecture review and issue triage. A scaffold fixture verifies all four with `work_index.py --check`; setup workflow wiring is unchanged.

## [2026-11-26] test | Setup files approved starter items
First-time setup for existing codebases now proposes applicable starters and files the owner's picks without running the work. Terra low dry runs (one per arm per fixture) gave exact proposals and approved filing in 3/3 revised runs versus 0/3 on the base body; neither arm ran an audit.

## [2026-11-26] test | Pipeline preflight without a publish policy
Round 1, one Terra low dry run per arm: treatment ran the bundled checker and planned a local commit with no pushes when away; comparison stopped. The owner-present case had single-run mode preselected. Round 2, one treatment dry run (owner present only, no mode preselected): planned one scoped yes, single-driver mode and a target push with no claim-ref or issue writes. No live launch or landing ran. Generated scaffold guidance points to that preflight.

## [2026-11-26] implement | Fallbacks for missing machine tools
Standalone skills now say what to do without optional helpers; the pipeline stops before claims without fresh roles. README lists prerequisites and fallbacks. Missing-tools dry run: Terra low, one completed run per arm, comparison 2/5 and revised 5/5; no live execution.

## [2026-11-26] implement | Standalone kernel package and fallback installer
Stage the canonical kernel as bundled Markdown and fail lint on copy drift. The opt-in installer manages a versioned block without changing surrounding bytes. Pytest examples and a round-trip property ran; no kernel wording changed and no consumer pressure or harness deployment ran.

## [2026-11-26] implement | Carry-on order and away questions without a destination
Visible scaffold rules prefer unfinished active work and check holders; planning and both drain sources use the waiting header as the fallback. Scaffold test RED/GREEN for code, ops and hybrid. Masked round 2, one real Terra low run per arm per fixture: both carry-on fixtures revised 3/3 vs base 1/3 on actions (literal active-first read order not observed); planning fallback 3/3 both arms (comparison NO_DEFECT). Round 1 carried owner rules and is excluded. No live drain ran.

## [2026-11-27] implement | Opt-in Pi kernel package
Pi loads a fixed staged kernel section from the separate local package; install and removal verified without changing the owner's Pi configuration. One real Terra low run per arm confirmed delivery and unchanged settings; neither asked for approval. The isolated Opus cache check hit 12/12 follow-up requests, including across resume; no kernel wording changed.

## [2026-11-27] implement | Pipeline regression guardrails
Build packets load performance guardrails for performance, size, memory and structure regressions; Spec checks the new protection or the reason none can catch it. One masked Terra low dry run per arm: both added a check (NO_DEFECT); treatment loaded the skill and documented the cap. No live drain ran.

## [2026-11-27] implement | Opt-in Claude Code kernel plugin
Separate marketplace plugin; Claude Code 2.1.329 sent both labeled section slices at startup and resume against a loopback stub and neither after uninstall or with skills alone. No authenticated Claude request or compaction ran. One real Terra low Pi proxy run per arm confirmed byte delivery in treatment only; neither asked for approval. No kernel wording or owner configuration changed.

## [2026-11-27] lint | Require handoffs for named workflow moments
A deployed body naming a covered moment must be the moment owner, have a handoff or load from the owner, or carry a reason on that line. Severity is WARN in the first tagged `CHANGELOG.md` version that includes the check and becomes ERROR in the following tagged version.

## [2026-11-27] implement | Opt-in Codex and OpenCode V2 kernel packages
Isolated loopback requests contained the exact Markdown at startup and resume and omitted it after removal on Codex 0.153.1 and OpenCode V2 2.4.2; OpenCode 1.18.3 used native instructions instead. Codex interactive trust and compaction were not run. One real Terra low Pi proxy run per arm verified delivery; neither asked for approval. No kernel wording or owner configuration changed.

## [2026-11-27] implement | Visible pipeline layout and installed wiki tools
The pipeline guide now describes the code scaffold; setup distinguishes all-archetype indexing and lint from classic-vault promotion. Vault search defaults to the installed skill, and runner scripts resolve their bundled files locally.

## [2026-11-27] test | Installed wiki tools close-out
One real Terra low run per arm: revised 4/4 vs base 3/4 on archetype scope and installed CLI calls. Both ran registration-entry generation, lint and search (no registry edit or timer install); the unset-variable search invocation also failed then passed in the deterministic regression.

## [2026-11-27] implement | Read-only kernel survey and optional install guide
Setup checks the active harness without installing the kernel; the README separates package lifecycle and pinning from manual deltas. One real masked Terra low run per arm: base omitted the kernel, revised supplied the Pi command but hedged on runtime activation, and neither changed project files or settings.

## [2026-11-27] test | Naming Things under first-release pressure
Three real Terra low runs per arm; neither arm held (0/3 each). Treatment recorded glossary persistence but still used the misleading proposed name in derived IDs and hashes. Deployment remains off; cases A–F were not run.

## [2026-11-27] test | Pi stranger end-to-end run
Added `scripts/stranger_end_to_end.sh`, its RPC driver and fixture: a sandbox with no private config installs this checkout and drives setup, planning and `bc-pipeline-to-done` on a generated repository with a local bare remote. First live run (Terra low, two attempts): setup and planning pass; the build stopped asking whether GitHub issues were also ready in a project with no GitHub remote, so building and landing were not reached. Planning and the build ran with `-nc`, so they never loaded the project instructions setup wrote; the GitHub stall is unconfirmed. Skill stalls became work items; the driver stalls, including `-nc`, were fixed.

## [2026-11-27] test | 033 stranger test done
Filed the first stranger run's stalls as 036-pipeline-no-github-source, 037-setup-find-installed-wiki-skill, 038-starter-items-pass-index-check and 039-stranger-rerun (building and landing still untested for a stranger).

## [2026-11-27] implement | file 040 and 041 from drain reflection
The reflection on the 2026-11-26 drain found test sessions reading the wrong instruction files (3 of 10 items) and status lines claiming more than their results tables (4 of 10); filed as 040-pressure-sandbox-instructions (replaces the harness-masks idea) and 041-results-claims-match-tables.

## [2026-11-27] implement | Starter items carry a Planned: line
The owner-led architecture-review and issue-triage starter items now carry `Planned: bc-setup-project`, so `work_index.py --check` is quiet right after setup (owner choice over exempting them in the check). `test_starter_items.py` now fails on any index warning; it failed on both items before the change.

## [2026-11-27] test | 036 pipeline: no GitHub remote, no issue source
Reproduced stall 1 with project instructions loaded (old wording called `gh` in 4/4 runs and stopped at the source question in 3/4). "Choose the source" now requires a GitHub remote for the issue source; the new wording chose the work items with no `gh` call in 2/2 runs.

## [2026-11-27] implement | 037 setup finds installed bc-wiki-maintain
`bc-setup-project` now finds `bc-wiki-maintain` beside its own skill folder with ordered `test -f` checks, covering the script install and `pi install` (stall 2 of the stranger test). Pressure runs on Terra low: final wording passed both install methods; old body failed both; a "harness lists it" wording failed because the skill is unlisted.

## [2026-11-27] implement | 036, 037, 038 done
Integrated and gated (tree d9c32474, 639 passed). Filed an idea for the scaffold's vault read block, which still hardcodes the `~/.agents/skills` wiki path.

## [2026-11-27] implement | 040 pressure sandbox loads the right instruction files
New `scripts/pi_sandbox.py` masks Pi 1.6.1's global instruction files (seven names in the agent folder, resolved through symlinks), deployed skill folders, overlays and ancestor `.agents/skills`, then checks the session's RPC system prompt for private terms and a missing project `AGENTS.md` before running. The pressure-test guide (now `-ne`, no `-nc`) and the stranger script use it; a real Pi start passed with `-ne` and failed with `-nc` and with the owner's extensions loaded. Re-check verdicts for the 2026-11-26 runs are in their results files.
## [2026-11-27] test | 041 results claims match tables
`bc-pipeline-to-done`'s worker review-ready gate now says to write test-summary status and log lines last, copying counts with their unit; `bc-code-review` Standards checks those counts against the cited results file. Terra low: NO_DEFECT on both sides (worker overclaim 0 of 5 comparison runs, 0 of 5 treatment runs; reviewer flagged it 3 of 3 runs in each arm).

## [2026-11-27] test | stranger rerun (039) and conditional sync-tool ignore
Stranger rerun on installed 87782c9 reached landing on the bare remote with no stall; results filed beside the first run. Its build worker wrote a `.stignore` because bc-tdd's properties.md and setup's generated validation.md said to Syncthing-ignore property-test caches; both now make it conditional on a synced folder.

## [2026-11-27] implement | 043 plain pipeline messages and planned dependencies
Pipeline push question in plain words; full report moves to the run log and the chat report leads with what landed, checks and reviews (cost table only when a cost is known); `work_spent.py` prints `Spent: not measured` instead of zeros; setup's survey checks `gh` only with a GitHub remote. Planning asks about libraries the project lacks and records `Dependencies:`; the builder adds only those (new contract edge; scenario written, not run).

## [2026-11-27] implement | Release after each integrated batch
AGENTS.md gains a Release operation: the integrating session releases without asking when gate, fresh-install and pressure tests allow, else records the blocker. Planned 046-install-from-npm (unpinned npm install so `pi update` reaches users).

## [2026-11-27] implement | 042-one-command-pi-install
Pi package now ships the three pipeline roles (`bc-pipeline-to-done/body/agents/`, via `pi-subagents.agents`) and the agent kernel extension; pipeline uses bundled roles by default and offers to install `pi-subagents`; README Pi install is one block; stranger script installs per README. Verified with a fresh-HOME Pi 1.6.1 install (roles discovered, kernel section in the system prompt).

## [2026-11-27] implement | 045-starter-items-for-new-projects
Setup now offers new or empty projects a guardrails starter item, plus a design item when a UI or CLI is planned; each does its planning step now and waits for code without blocking. Unit-tested; new-project pressure arm written, not run. Guardrails Setup checks pointer and the two hand-off edges updated.

## [2026-11-27] implement | Release retests only rule changes
releasing.md step 2: retest only changes that add or change a stop, requirement or prohibition; a shared rule is tested once; wording changes need no retest; record the sort in a release audit (owner choice). First audit: docs/research/2026-11-27-release-audit.md; 044 adds the security-audit test.

## [2026-11-27] implement | Pi package publishable to npm (046-install-from-npm)
package.json gains a generated `files` list and drops `private`; release.yml publishes tags through npm trusted publishing; fresh_install_test.py `pi-npm` packs and installs the tarball; README Pi install is the unpinned `npm:agent-concepts`. The first publish stays manual.

## [2026-11-27] implement | bc-ui-design description covers everything a user sees or operates
Description and opening line now name wording, commands and flags, keyboard, states, accessibility, motion, missing tokens and design decisions, not only layout/styling (owner decision); trigger check in the concept's tests.

## [2026-11-27] implement | rename bc-ui-design to bc-design
Owner decision: the name matches the widened scope. References, relationships, packages and generated pages updated; old name kept as a deploy alias. Trigger check of old vs new description: 4/4 reads each arm on Terra low (no difference shown).

## [2026-11-27] test | planned-dependencies owner's-answer mark
`bc-plan-to-pipeline` marks the `Dependencies:` line as the owner's answer; `bc-tdd` and `execute-issue.md` accept only a marked line as the property-library waiver. Terra low: new arm 3 of 3 runs wrote example tests with no dependency (old arm also 3 of 3, so the mark is the fix); no-line regression 1 of 1 blocked.

## [2026-11-27] implement | build stall: named item sets the order, bare yes means the recommendation
Owner choices 1a 2a after the stranger rerun stalled: `bc-pipeline-to-done` builds a user-named item without an order question and records the order in the claim commit; the kernel reads a bare yes as the recommended option. Terra low: named item old 0/3 vs new 3/3; stall replay old kernel 3/5 vs new 5/5.

## [2026-11-27] deploy | release v0.4.0
Version 0.4.0 across package.json and plugin manifests; CHANGELOG entry; README tags; release audit rows filled from the 044 pressure tests and stranger attempt 4.

## [2026-11-27] deploy | npm first publish; close 044 and 046
agent-concepts@0.4.0 on npm (owner-run first publish from the tag); release workflow green; both items moved to done.

## [2026-11-27] implement | blind-spot council work items
Council (fable + Opus fallback) found release-reach, reporting, CI, migrations, rename and release-hygiene gaps; owner chose 1a 2a 3a 4a minus F. Planned 047-052; outside-PR rules went to ideas; kernel stays on by default.

## [2026-11-27] implement | long scripts out of worktree workers; isolated Pi home
bc-delegate-investigation pi.md failure mode: commands over ~20 min run from the parent detached (two worker timeouts this session); stranger_end_to_end.sh header says the same; releasing.md: a throwaway Pi home sets HOME and PI_CODING_AGENT_DIR. From bc-self-improve, owner picks 1 2. pi.md entry is an observed-failure reference note, accuracy-checked against the session log.

## [2026-11-27] implement | release soak on npm next; bad-release procedure (047)
Tags publish to npm `next`; a dispatch-only `set-latest` job in release.yml promotes (version on next) or rolls back `latest` over OIDC (npm >= 11.21.0). Stranger test can install a published version (`STRANGER_SOURCE=npm`). releasing.md gains the soak and "Withdraw a bad release"; README now says `pi update --extensions` (plain `pi update` is Pi-only in 1.6.1).

## [2026-11-27] implement | stranger report channel (048)
SECURITY.md, issue form and security contact link, README "Report a problem" line, session-start issue check in .bc-agent/AGENTS.md. Dry run with a fake gh filed one issue as an idea line. Private vulnerability reporting still needs enabling on GitHub (owner).

## [2026-11-27] implement | modularity work items 054-060
Scout scan of all skill bodies for multi-job skills; owner picked safe-runs module (before 053), project-file rules in the bc-agent scaffold, file-findings module, teach-hosting home, kernel rule for runs nobody can answer, qmd query contradiction fix, wiki timer install move.

## [2026-11-27] deploy | v0.4.1 prep; GitHub release pages
Owner chose 1a 2a: created the missing v0.4.0 GitHub release (Releases page still said v0.3.0 was Latest); release.yml gains a `github-release` job from the CHANGELOG entry. release_check.py no longer reads `npm:agent-concepts@next` as a version pin (test first). Version 0.4.1, CHANGELOG, README tags, audit row.

## [2026-11-27] implement | plan 061 drift prevention
Lint check for repeated text across skill bodies, copy-of markers kept in sync, author guidance to search for an owner first; ordered before 054.

## [2026-11-27] implement | README install section tidied
Owner chose Pi first and open, plus 1a 2a 3a: Pi box opens by default with `next`/pin details folded; IMPORTANT trimmed to two bullets (council and update notes moved into the boxes); kernel section opens with what the kernel is and folds its per-agent table; pipeline prerequisites cut to one paragraph, optional machine-tools table moved to docs/guides/pipeline.md.

## [2026-11-28] implement | README: pipeline prerequisites section removed
Owner chose to drop it: Pi install covers it, setup checks gh. Its content moved to docs/guides/pipeline.md "What the pipeline needs"; harnesses.md link repointed; spacer before "Working on this repository" to match other top-level headings.

## [2026-11-28] deploy | v0.4.1 promoted to npm latest
First soak: stranger test on npm@0.4.1 (`next`) passed setup, planning, build and full-suite checks; private-term audit clean. One stall (planning skipped the dependency question; builder parked correctly) filed as 063. `gh workflow run release.yml -f action=promote -f version=0.4.1` (run 46090008369) moved `latest` to 0.4.1 — the first live run of `set-latest`.

## [2026-11-28] implement | latest-agent CI and packed Pi kernel
Weekly latest-CLI installs report failures; the packed Pi test checks the kernel in the assembled prompt without a provider request. Aligned pinned Pi to 1.6.1.

## [2026-11-28] implement | latest-agent CI review fixes
Require npm's latest tags, isolate and serialize failure reporting, and validate the packed Pi kernel prompt. The integration test now skips Pi shims and restores and removes its scratch install.

## [2026-11-28] implement | ship setup migration guide (partial)
Moved the migration guide into the shipped skill body and updated references; scaffold version semantics await an owner decision.

## [2026-11-28] implement | 049 done; install test handles Claude Code 2.1.332
049 landed: weekly/manual `latest agents` workflow (read-only test job, separate serialized issue reporter), Pi pin 1.6.1, packed-Pi `<agent-kernel>` section probe. Its first manual run failed on Claude Code 2.1.332, which lists built-in plugins; the Claude listing now matches this plugin's ID (regression test failed first; method passes on 2.1.329 and 2.1.332).

## [2026-11-28] implement | renamed skill compatibility
Added a bc-ui-design compatibility stub across distributed installs, a rename/removal release policy, and a previous-release disappearance check.

## [2026-11-28] implement | 050 setup migrations ship with the skill
MIGRATIONS.md moved into bc-setup-project/body/ (ships with npm, plugin and npx installs; scaffold hints name the installed path). Owner chose option a: a fresh scaffold writes .bc-agent/.scaffold-version once; reruns, --force, --allow-earlier-layout and --migrate never add or change it; each migration section has an Arrived in: line.

## [2026-11-28] implement | 051 review follow-ups
After two blocking reviews the owner chose to close with parent fixes: Removed entries in HTML comments or fenced code no longer exempt a disappearance, alias names obey the bc- prefix rule, kernel test tolerates alias retirement. Accepted gap: packed-Pi probe calls the private resolver directly.

## [2026-11-28] implement | release hygiene pins
Release checks require the personal-terms scan unless explicitly opted out; CI opts out. Pinned publishing actions and npm, with promotion using the same npm version.
After two blocking reviews the owner chose to bind the release scan to the staged git snapshot (symlinks as stored text, submodules skipped, unstaged tracked changes block) and accept two pin-test gaps (quoted `"uses":`, `npm i`).

## [2026-11-28] implement | repeated prose and tracked copies
Added a lint warning for similar concept-body paragraphs and errors for drifting or unresolved tracked copies; documented authoring and modularity review guidance.

## [2026-11-28] implement | repeated-text lint and copy-of markers
Lint warns on concept-body paragraphs repeated across skills (80% trigram overlap or a 40-word exact run) and fails drifted, malformed or self-referencing `copy-of` copies. After two blocking reviews the owner chose a single-pass block reader. Step 3 (ERROR) waits on 054-058.

## [2026-11-28] implement | bc-safe-runs module
New `bc-safe-runs` holds the storage-safe run and worktree-removal rules (derived from the kernel's Storage safety); 14 skills load it with a one-line fallback under the repeated-text threshold. Pressure: bc-tdd and bc-code-review storage scenarios PASS 5/5 with the module on Terra low, fallback alone 4/5 each. Not deployed.

## [2026-11-28] implement | bc-safe-runs review fixes
The pipeline passes the module to builders and the task packet preserves the uv/venv interpreter. Fallbacks stop on critical, unknown or uncheckable storage health; cleanup requires successful `git cherry` proof. Updated caller notes and documented the two accepted kernel overlaps. Deployment unchanged.

## [2026-11-28] deploy | bc-safe-runs
Owner chose to deploy the module (with it the two storage scenarios score 5/5, fallback alone 4/5); regenerated public skills, Pi package, plugin manifests, install packs and status. 054 done.

## [2026-11-28] implement | split bc-delegate-investigation into bc-swarm and bc-durable-subagents
Work item 053 step 1: durability contract, recovery rule, evidence anchors, durability/storage packet bullets, full gate and all of `pi.md` moved verbatim to the new `bc-durable-subagents`; the concept is renamed `bc-swarm` (posture plus fan-out width) and loads it; `bc-delegate-investigation` is a compatibility alias (stub skill + deploy alias). Post-split pressure rerun on Terra low: with PASS 4/4, without FAIL 4/4. Not deployed from the worktree; deploy from the main checkout after integration.

## [2026-11-28] implement | launching skills load bc-durable-subagents
Work item 053 step 2: `bc-council-mode`, `bc-subagent-driven-development`, `bc-dispatching-parallel-agents` and `bc-pipeline-to-done` load `bc-durable-subagents` with a one-line run-folder/manifest fallback (`loads` edges added; pipeline keeps its drain run state). Council advisors write to run-folder outputs instead of `output: false`. `bc-handoff` pointer and stale `bc-delegate-investigation` mentions repointed. Council dry run on Terra low: PASS (run folder + manifest before launch).

## [2026-11-28] implement | durable subagent launch review fixes
Require a reboot-safe run folder, wire in audit and work-sync reviewers, clarify drain rule precedence and correct council/overlay docs; Terra low council dry-run rerun PASS 5/5.
## [2026-11-28] implement | 053 step 3: swarm-mode prompt loads bc-durable-subagents
Private swarm-mode kernel drops its durability copy for a pointer; routing-decision/recovery-rule words; overlay renamed; pointer check PASS 2/2 (Terra low).
## [2026-11-28] deploy | release v0.5.0 prep
Version 0.5.0, CHANGELOG, README pins; audit docs/research/2026-11-28-release-audit.md (no gaps).
## [2026-11-28] implement | 062 step 1: kernel plugins in the fresh-install test
`claude-kernel`/`codex-kernel` methods install `agent-kernel` from the marketplace (tag under --ref) and check the hooks deliver the kernel text; fail with agent-kernel removed from the marketplace files, pass with it.

## [2026-11-28] implement | Codex installs the kernel by default
README Codex box adds `agent-kernel@agent-concepts` from the tag-pinned marketplace, with the `/hooks` trust line, and uninstall removes both plugins; harnesses.md, agent-kernel CONCEPT.md, CHANGELOG match. `fresh_install_test.py --method codex --method codex-kernel --ref v0.5.0` passed (work item 062 step 2).

## [2026-11-28] test | stranger end-to-end, v0.5.0 from npm next
Inconclusive: both attempts on anthropic/claude-haiku-5-5 low (owner's Haiku fallback while the Codex quota is out) got HTTP 429 on every call; no phase ran. Recorded in docs/research/2026-11-28-stranger-end-to-end-0.5.0.md and the release audit; v0.5.0 not promoted.

## [2026-11-28] test | v0.5.0 stranger end-to-end rerun: fail
With the account-pooling extension (no 429), setup passed but the planner built and filed the change as done, so the build pushed it without pipeline roles. Not promoted; idea filed in work/0-ideas.md.

## [2026-11-28] implement | 059 bc-qmd owns the qmd query rule
bc-qmd: 2–4 keywords, `qmd search` first, one `qmd query --no-rerank` rerun on a miss; bc-wiki-maintain and the generated vault block ban `qmd query` only inline (migration "Vault read path: `qmd query` ban narrowed"). Round 2 paraphrase rerun PASS 2/2 on Haiku 5.5 low (41–44s vs 167–237s). Read-path scenario 5 failed in both arms (whole-vault reads, predates 059). Moved onto master without 055 by owner choice.

## [2026-11-28] implement | 055: scaffold owns role lookup and worktree numbering
Generated `.bc-agent/AGENTS.md` (and this repo's) carries the role-lookup paragraph and the union numbering rule; ten callers trimmed to pointers + fallback; migration added; relationship reasons updated. New pressure scenario `bc-plan-to-pipeline/tests/pressure-worktree-numbering.md` not run: Terra codex quota at 0% until 10:35 GMT.

## [2026-11-28] implement | 055 review fixes
Migration arrives in 0.5.1 with a no-paragraph anchor; find-bugs/architecture state the worktree ideas-line owner choice and reason themselves; scenario criteria and old-bullet arm tightened (not run); nits fixed.

## [2026-11-28] test | bc-plan-to-pipeline worktree numbering (055) — inconclusive
Haiku 5.5 low runs of pressure-worktree-numbering hit 429 rate limits on every attempt (~36 min); recorded as not run, status unchanged.

## [2026-11-28] test | bc-plan-to-pipeline worktree numbering rerun (Haiku, multiprovider)
Reran pressure-worktree-numbering on claude-haiku-5-5 low (owner-approved Terra substitute) with pi-multiprovider loaded. with-block 2/2 PASS; skill-only (04eb706 scaffold) FAIL: it numbered and committed 003 in the worktree. Status unchanged; no skill text changed.

## [2026-11-28] implement+test | bc-plan-to-pipeline: full worktree numbering rule restored (055)
Owner decision: undid 055's trim of the skill's numbering paragraph (rest of 055 kept). Reran pressure-worktree-numbering on Terra low: skill-only (04eb706 scaffold) 3/3 and with-block 1/1 PASS; status frontmatter updated.

## [2026-11-28] implement | 060 wiki timer install moves to bc-wiki-maintain
The per-vault timer install procedure left bc-setup-project step 10 for bc-wiki-maintain/body/INSTALL-TIMER.md (text unchanged); setup keeps the offer and loads it, runner README points at it, new `loads` edge. Read-through on a fixture: nothing lost.
Review follow-up: setup scenario check 7b points at the moved confirmation sentence; runner README's second per-vault recipe cut to a pointer; CONCEPT deploy list and CHANGELOG install-pack note.

## [2026-11-28] test | bc-setup-project wiki-maintain timer (Haiku rerun)
Reran pressure-wiki-maintain-timer on Haiku 5.5 low (owner-approved Terra substitute) with pi-multiprovider: FAIL, with-arm 1/4 vs without 2/4; both attempted install+enable on "don't ask". No skill text or status changed.

## [2026-11-28] test | 060 wiki-maintain timer close-out after step 10 tune: PASS
Step 10 states inline that qmd search is not promotion, that "just enable"/"don't ask" is not confirmation of the shown units and commands, and the parking-lot TODO on decline/no systemd; INSTALL-TIMER.md adds the "don't ask" clause. Terra low rerun: tuned 4/4, master 1/4 (master installed units unconfirmed). Results: concepts/bc-setup-project/tests/pressure-wiki-maintain-timer-results-terra-2026-11-28.md.
