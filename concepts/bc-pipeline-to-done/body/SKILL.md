---
name: bc-pipeline-to-done
description: Autonomously build a repo's ready queue (planned work items marked ready for an agent, or ready-for-agent and rework-for-agent GitHub issues) with isolated worktrees, bounded rework, independent review, and driver-owned landing. Run after /bc-plan-to-pipeline.
disable-model-invocation: true
argument-hint: "[max-iters=20] [max-parallel=3] (optional caps; max-parallel 1 = sequential)"
---

# Pipeline to done (AFK executor)

Drain eligible units of work through isolated build, independent Spec and Standards review, bounded same-worktree rework, and driver-owned landing. The driver owns global state and publishing; fresh workers own code/tests/validation only. This separation prevents a worker from publishing its own unreviewed result.

## Choose the source

A unit of work comes from one of two sources, and each source page owns choosing, claim key, contract, parking and finishing for its units:

- **Work items** — [source-work-items.md](source-work-items.md): the project keeps a `work/` pipeline (a "Where things go" table in `.bc-agent/AGENTS.md`) and at least one item carries the line `Ready for agent: yes`.
- **Issues** — [source-issues.md](source-issues.md): the project has a GitHub remote and its GitHub issues carry `ready-for-agent` or `rework-for-agent`. Without a GitHub remote there is no issue source: do not query it or ask about it.

If only one source has ready units, use it. If both do, ask the owner which to drain before preflight; if neither does, report an empty queue and stop. Read only the chosen source page.

The rules below and the shared contracts are written for one unit of work. Where they say "issue", `#<n>` or `issue-<n>`, read the chosen source's unit and claim key (`issue-<n>` for an issue, `item-<slug>` for a work item); where they name a label, comment or close, do what the source page says instead.

Use these detailed contracts when entering their phases:

- Builder: [execute-issue.md](execute-issue.md)
- Reviewers: [review-contract.md](review-contract.md)
- Deferred-work capture/restore: [recovery-bundle.md](recovery-bundle.md)

## Jobs

The workflow is harness-agnostic. It launches three jobs, each a fresh subagent that does not inherit the broad skill catalog and gets only the skills this contract passes:

- **auditor** — read-only, fresh context; audits a high-risk unit's contract before code.
- **builder** — writes only in its own worktree and never commits; builds and reworks.
- **reviewer** — read-only, fresh context; one review axis or the combined review.

By default the jobs run as the roles this skill's Pi package ships (see [roles.md](roles.md)): `bc-drain-auditor`, `bc-drain-worker` (the builder) and `bc-drain-reviewer`. If `~/.config/agent-concepts/overlays/bc-pipeline-to-done.md` exists, read it; roles or models it names for a job override the defaults. Set model effort explicitly per this contract. Because the jobs do not inherit the broad skill catalog, pass the worker disciplines explicitly (`bc-minimal-solution-ladder` and `bc-safe-runs` on every implementation packet, plus `bc-tdd`, `bc-diagnosing-bugs`, and/or `bc-optimize-code` where applicable); auditor and reviewer jobs get none up front: [review-contract.md](review-contract.md) gives the reviewer the `bc-codebase-design` vocabulary and says when to load `bc-codebase-docs`. Bound each read-only auditor/reviewer to four assistant turns and 12 tool calls; mutation-capable workers receive narrow packets and are never arbitrarily interrupted mid-write. Use the configured compact tool descriptions, set top-level `artifacts:false` or an external artifact/session root (including resumed runs), and keep outputs outside unit worktrees. These are economy controls, not permission to weaken correctness gates.

Load `bc-safe-runs`. Else: guarded test runner (fallback `pytest`; no custom `--basetemp`), `mktemp -d` outside `/tmp`, targeted tests; configured storage check before full suites, worktrees, fan-out: stop if critical or unknown, or if the check cannot run.

Load `bc-durable-subagents` for the generic launch rules (manifest before dispatch, async fan-out, child artifacts with `Commit:`/`Branch:` records, recover before relaunch); the drain's claims, run artifact root and recovery root below are its own run state; where they differ, the drain's resume and landing rules below win. Else: before the first dispatch, write the run manifest in a run folder that survives a reboot (use the drain's run artifact root) and state the folder path in chat.

Put the `bc-safe-runs` packet line in every worker or reviewer task. Before releasing an integrated worktree or branch, prove its commits are in `HEAD` (ancestor or patch-equivalent) and record that landing proof in the run manifest. Why: unattended loops multiply storage leaks.

## Claim before work

No auditor, worker, or worktree starts on a unit until the driver has claimed it through the authorized claim protocol in [Select, classify, and claim](#select-classify-and-claim): no-force create-if-absent, or lease-guarded reuse of a Released Claim Marker, with a lost race skipped before dispatch. Local-only and single-driver modes record a local claim instead and never write claim refs. Why: labels, comments and folder moves are advisory across drivers, so the claim ref is the only thing that stops two drivers or machines building the same unit. This rule lives here, in the skill itself, because projects with the visible layout no longer generate `.bc-agent/conventions/planning-workflow.md`, which used to carry the pointer.

## Where project files go

This skill names project files by role: the **work-planned**, **work-active** and **work-done** folders, which hold work items, and the **ideas** file. Resolve each role from the "Where things go" table in the project's `.bc-agent/AGENTS.md`; that file says how. Without the table there are no work items; see [source-issues.md](source-issues.md#where-issues-and-work-items-meet).

## Preflight — before the loop

Stop and report if a required check fails; AFK work must not invent mid-run decisions.

Before any claims, worktrees or baseline validation, verify that the harness can launch fresh subagents and that executable roles are available for all three jobs above. In Pi, check the `subagent` tool and its role list. If the tool is missing, ask once whether to run `pi install npm:pi-subagents`; if the user agrees, run it, then stop and tell them to restart Pi and start the pipeline again; otherwise stop. If a role is missing or does not meet the job's limits, stop, name the job and point to [roles.md](roles.md). In other harnesses, name the missing capability or job and ask the user to configure it. Do not substitute the driver for a required job.

1. Resolve the **target branch** (where work lands) once. An explicit target in the project's instructions wins. Otherwise read `git symbolic-ref refs/remotes/origin/HEAD` and strip `refs/remotes/origin/`. Only when there is no Git remote, use the current named branch (`git symbolic-ref --short HEAD`). If the target cannot be determined, stop and report; do not guess. Confirm the target repo is clean and checked out on that branch. Capture the remote and base SHA and record them with `target_branch` in the run manifest. Use the recorded branch throughout the run, including recovery; if resuming, verify the checkout against the manifest rather than resolving the branch again.
2. For this repo, remote and recorded target branch, run the checker named by the private overlay, or, if none is named, run `python3 <skill-dir>/scripts/publish-check.py --repo <repo> --remote <remote-url> --branch <target-branch>` from the installed skill's copy. A pass authorizes only the configured operations and conditions. Only when the checker explicitly reports that the policy file does not exist:
   - If the owner can answer, ask once per run, in plain words that name no policy file, claim or tier: “May I push finished work to `<remote name>` `<target branch>`?” (for example “May I push finished work to `origin` `main`?”) Record the answer and exact destination in the run manifest. An explicit yes authorizes only this run’s target-branch push and sets single-driver mode in the manifest (`max-parallel=1`, no remote claim-ref writes). If more parallelism was requested, build one unit at a time and say why in the report. The yes does not authorize issue mutations. A no stops the run unless local-only was agreed. On resume, use the recorded decision for the same run and destination; do not ask again.
   - If the owner is away or cannot be asked, record local-only mode, commit locally, push nothing, and report that outcome.

   Otherwise, a denial or missing/unusable check aborts unless the user pre-agreed to commit-only-local mode. Never write or edit the policy to authorize a run. A push that includes a policy change still requires separate, explicit current user instruction covering that change.
3. Skip claim-ref authorization in preflight’s single-driver or local-only mode. Otherwise, confirm no-force creation/deletion of `bc-drain-claims/issue-<n>` is authorized. For marker reuse, also confirm authorization for lease-guarded fast-forward acquisition from a valid marker; optional marker cleanup requires lease-guarded deletion authorization. Both leases must name the exact inspected marker SHA. This never authorizes force-updating a non-marker tip. Without that authorization, stop unless the user explicitly selected single-run mode; in that case record single-driver mode in the manifest and use its limits. Without marker authorization, continue, but report each valid-marker issue and skip it for the run. Why: the marker paths update an existing ref, which a no-force-only policy does not cover, and an unauthorized marker should cost one issue, not the run. Labels/comments are advisory, not locks.
4. Run the chosen source's preflight checks.
5. Record the launch caps: `max-iters` (default 20) and `max-parallel` (default 3; 1 in single-driver or local-only mode), plus the review bound: the stop rule in `bc-code-review`'s Review loops section.
6. Choose a run artifact root outside every worktree for review packets, `review-packet/issue-<n>/round-<r>/`, and verify it is writable.
7. Set worker effort explicitly: low for ordinary slices, medium for high-risk slices. Rework rounds after review run at low even for high-risk slices, never at the role cap: the slice is already built and reviewed, and the rework packet names the findings to fix. Never silently inherit a higher AFK parent effort.
8. Verify worktree support and a root outside the checkout, default `${BC_DRAIN_WT_ROOT:-${TMPDIR:-/tmp}/bc-drain-worktrees/$(basename "$PWD")}`. Never build in the main checkout. Fixed-port tooling may require `max-parallel=1`.
9. Choose persistent recovery root `${XDG_STATE_HOME:-$HOME/.local/state}/bc-drain/recovery/<repo-key>/` and verify it can be written safely.
10. If a global qmd collection covers the repo, run `qmd update && qmd embed` once. Workers search it but never re-index.
11. Cache full project baseline validation once per base SHA: command, exit status, failing test IDs, concise summary, raw-log path outside the worktree, and content hash. This separates known failures from regressions without paying for a full suite every round.

## Resuming an interrupted run

A drain dies between phases more easily than it fails: a killed pane, a lost harness session, a restarted machine. Claims, worktrees, and uncommitted diffs all outlive it. Recover before relaunching — dispatching a fresh drain over live state pays again for work already on disk and can strand a reviewed diff that nobody is left to land.

After preflight and before the loop, list `refs/heads/bc-drain-claims/*` on the remote, then the worktree and recovery roots. The remote claims are the authoritative index of surviving coordination state, not proof that a local run owns every claim, and they are authoritative precisely because they are the one record that does not live in a context that just proved it can vanish. Apply the source's resume checks first (for issues, the cloud-lane provenance gate in [source-issues.md](source-issues.md#resuming-an-interrupted-run)) before marker classification and before any adoption, restore, release, or cleanup. For each ref, inspect its observed tip commit before recovery. A **Released Claim Marker** has subject exactly `bc-drain-claim released`, body lines `issue=<n>`, `run=<run-id>`, `claim=<claim sha>`, and exactly one parent: the released claim commit. Require one of each body field, a nonempty run ID, `issue` matching the ref's issue number, and `claim` equal to that parent SHA. An absent ref or a valid marker tip is **FREE**, not a live claim. Why: cloud runs release by fast-forwarding to this marker because they cannot delete refs.

- **Valid marker tip** — treat the ref as free; acquire through the marker path below before adopting/restoring any surviving local work.
- **Marker-looking but malformed, or unreadable tip** — held/unaccounted: leave it, report it, and skip. Never infer release from the subject alone or guess through missing/mismatched fields or parents.

For remaining held claims, apply these dispositions only with the required claim authorization; otherwise leave them untouched, report and skip:

- **Worktree present with an uncommitted diff** — adopt it. Re-derive the packet, re-run the deterministic pre-review gate, and take full fresh review on every axis. No standing approval survives a run whose reviewer records are gone; an approval is a record, and an unreadable record is not one.
- **Valid recovery bundle** — restore through [recovery-bundle.md](recovery-bundle.md) exactly as for a `rework-for-agent` candidate.
- **Neither, and the unit is untouched** — release the claim and the source's claim marks, then treat it as ready, unless the source page excludes it.
- **Anything else** — leave the claim, report it, and skip the unit for this run. Never release a claim you cannot account for, and never delete a worktree to make an inconsistency go away: the inconsistency is the evidence.

State the run artifact root and the recovery root in the run's opening report, as `bc-durable-subagents` states a run folder before launch.

## Select, classify, and claim
Select the next eligible unit as the chosen source page says, skipping live claims (not valid marker refs) and in-flight units. Prioritize units with a valid local recovery bundle. Vague or decision-incomplete work becomes `HUMAN_BLOCKED`, not guessed work.

Classify risk cheaply in the driver before claim: **high-risk** means compatibility replacement/retirement, migration/cutover, systemd or external-service semantics, or a broad public acceptance surface. Classification may choose effort and packet shape, but no auditor/worker is dispatched before ownership is acquired.

Record a **review tier** with its classification reason at the same time. High-risk slices are tier 2 (two independent axes). Ordinary slices start at tier 1 (one combined reviewer) and escalate permanently on a pre-review gate rejection or any Critical finding; see [review-contract.md](review-contract.md). Tier is recorded before dispatch and reported per issue so the cheap path stays auditable; it never lowers mid-issue.

In local-only or single-driver mode, use one driver and `max-parallel=1`. Check for other drivers and live claims read-only; stop if you cannot rule them out. Record the local claim before dispatch (for work items, follow the source's single-driver claim). Do not create, reuse, release or clean up remote claim refs in this mode. In local-only mode, make no other remote writes either.

Otherwise, atomically claim from the main checkout's tree on the recorded target branch with `git commit-tree` (the coordination ref is still separate):

- **Absent ref** — create a parentless claim commit and push it without force to `refs/heads/bc-drain-claims/issue-<n>` (unchanged create-if-absent path).
- **Valid marker tip** — create the claim commit with parent = marker, then push with `--force-with-lease=refs/heads/bc-drain-claims/issue-<n>:<marker sha>`. Keep it fast-forward; never use plain force or replace a held/malformed tip. Why: the exact lease makes marker reuse a compare-and-swap, so a concurrent claimant cannot be overwritten.

Only a push reporting an update of this exact ref to the new claim SHA **and** `git ls-remote` equality with that SHA proves ownership; a successful but up-to-date push is not ownership proof. A lease rejection is a lost race: skip without spending child tokens, as on a failed no-force creation. Without both proofs, do not dispatch. Then apply the source's authorized claim marks.

Once claimed, fetch the recorded target branch from the recorded remote when present and create `bc-drain-work/issue-<n>` in the external worktree root from the fetched tip (or the local target tip for a no-remote run).

For recovered work, follow [recovery-bundle.md](recovery-bundle.md) only after the claim succeeds. A matching base may restore directly; a changed base requires full diff inspection, validation, and full fresh review.

After the claim/worktree (and any restore) succeeds, a high-risk unit gets a fresh bounded read-only contract auditor before implementation. It produces:

```text
requirement -> observable test/check
existing public interface -> preservation test
external semantics -> evidence required
known baseline failure -> unchanged/regressed check
guard/rejection clause -> can-its-inputs-differ-in-production evidence
human-only verification -> explicit deferral
```

The guard row exists because an inert guard is the one defect a green suite actively hides: if both sides of a check resolve to the same value on every production path, only an injected test double can supply a differing pair, so the check passes by inspection and by coverage while protecting nothing. Trace each side to where the real caller obtains it. When the unit is *about* a guard, this row is mandatory for every guard the diff touches, keeps, or relocates — a fix that removes one inert clause while leaving its neighbour tautological has not resolved the class.

For replacement work, inventory the complete old public interface from source, tests, and help output—not merely the unit's new-command list. Map every acceptance criterion to evidence. For executable/loader replacement, include argument/environment/cwd/symlink or installed-launcher topology/path or module-resolution and privilege-boundary behavior, not output alone. When acceptance depends on an external platform's semantics (for example systemd, a database, or an API), verify the claim against available primary documentation such as installed man pages/help or an explicitly authorized authoritative source; repository prose and string-presence tests are not sufficient evidence. Record the source/version or mark verification unavailable. This audit exists because compatibility, launcher-security, and service-semantics omissions can pass narrow new-feature tests and become expensive only after landing. An unresolved product choice becomes `HUMAN_BLOCKED`; clear engineering work continues.

## Build and deterministic pre-review gate

Dispatch a fresh builder with [execute-issue.md](execute-issue.md), the unit's contract (issue/Agent Brief, or work item and step), acceptance matrix, worktree, remote identity, base SHA, and baseline summary. For a performance, size, memory, or structure regression, include `bc-performance-guardrails` and require the check or explanation from the builder contract. Keep validation artifacts outside the project worktree.

When it returns `READY_FOR_REVIEW`, the driver—not a model reviewer—must deterministically verify:

- every acceptance-matrix row has evidence—on a rework round, carried-forward plus newly re-evidenced rows together, with the matrix→file map proving every row the fix touched was actually re-evidenced;
- status, changed-file list, and diff are in scope;
- targeted validation passed and the baseline delta is explicit;
- no files are staged and no unrelated files are present;
- validation evidence and raw logs are outside the worktree.
- the handoff contains the Test levels block from the `bc-tdd` skill (section Test levels) with a non-empty L1, L2 and L3 line; a missing or empty block fails the gate. Whether each line is true is the Spec reviewer's audit, not the gate's.

A passed gate materializes the round's review packet once, outside every worktree: `packet.json` (base SHA, worktree, issue ref, round, `diff_sha256`, axis scope, acceptance-matrix→file map), `diff.patch`, `changed-files.txt`, `acceptance-matrix.json`, `validation.json`, and on re-review `findings-prior.json`. Reviewers consume these paths instead of re-deriving status and diff, and `diff_sha256` is the identity that standing approvals bind to. A gate rejection escalates the issue to tier 2 permanently.

A failed gate returns fixable engineering defects for rework. Product/contract decisions, unavailable access/resources, or irreparable unit-local environment failures requiring human repair become `HUMAN_BLOCKED`; transient/repeated tooling, base, or environment failures stay out of `needs-human` and follow rework or `SYSTEMIC_FAILURE` handling. Do not spend reviewer tokens on mechanically incomplete work.

## Independent lean review and bounded rework

Follow [review-contract.md](review-contract.md). Dispatch fresh read-only reviewers on the round's packet, without the worker's reasoning or parent transcript: two independent axes in parallel at tier 2, one combined reviewer at tier 1. Both axes must stand approved. Minor findings do not block.

Record each approval as a standing record bound to the packet's `diff_sha256`. After a rework round, re-dispatch the axis that raised the findings, plus any axis whose deterministic invalidation trigger fired on the rework delta; an axis holding a standing approval over untouched scope is not asked the same question twice. An unmappable delta invalidates both axes—ambiguity costs a review, never an assumption.

For Critical/Important findings, retain the claim and same worktree. Launch a **fresh compact rework worker** with only the current worktree/base, the round's packet paths, unresolved findings, prior dispositions, validation evidence, and the driver-computed implicated row set (the acceptance-matrix rows those findings touch). If rework touches a regression fix covered by the guardrails rule above, include the same skill and check requirement. It fixes and runs targeted validation, then the deterministic gate, packet refresh, and selective focused re-review repeat. Do not replay an accumulating transcript.

Load `bc-code-review` and stop the rework loop as its Review loops section says: a finding still reachable after two attempted fixes, or the cycle cap, defers the unit; two blocking reviews in a row on new sequences stop it for replanning, which for a work item the source page records. This progress rule prevents superficially different patches from consuming an unbounded loop while preserving useful implementation state. A review-ready result still passes the deterministic gate and receives independent review regardless of child-token volume; token counts alone neither defer an issue nor stop launches. Continue selecting eligible issues within `max-iters` and `max-parallel`.

On deferral, use [recovery-bundle.md](recovery-bundle.md), then record the deferral as the source page says (for issues, a portable `## Agent Rework Brief` comment and labels). Mark the unit ineligible for the rest of this run, and release only after the bundle validates. If safe capture fails, retain evidence and follow the recovery contract's fail-safe handling—never silently delete useful work.


## Driver-owned landing

Only after verifying that **every axis holds a standing approval whose `diff_sha256` equals the final reviewed diff**, the driver:

1. inspects status and the exact reviewed diff;
2. runs final relevant/full project validation once (the only full run after the cached baseline);
3. commits only unit-authored changes using project conventions, plus the source's progress update (for a work item, its ticked step; for an issue, the work-item update in [source-issues.md](source-issues.md#landing));
4. verifies authorization for the exact recorded destination; for a no-policy yes, use the current run's manifest without re-asking or extending its scope. A changed destination is not authorized. In local-only mode, skip the publish check and all remote writes;
5. pushes with `git push "$remote" "HEAD:refs/heads/$target_branch"` using the manifest values; skips the push in local-only mode;
6. finishes the unit as the source page says (closes the issue, or ticks the step and finishes the item);
7. releases worktree, local branch, and claim only where authorized; preserve any local-only commit on a named branch and report it.

A rebase that changes the reviewed diff changes its hash, so no standing approval covers it: update the base, validate, and obtain fresh focused approval on both axes before push. The driver owns commit/push/close so implementation and rework workers cannot bypass the independent gate.

For `HUMAN_BLOCKED`, park the unit as the source page says: the owner sees the decision or missing access first, the options and what happens if they pick each, then the exact evidence. Leave SHAs, paths, and commands untouched. Do not load `bc-plain-language`. For `SYSTEMIC_FAILURE`, stop new launches, let active children reach a safe boundary, preserve/classify each unit, and report stale resources rather than guessing or destructive cleanup.

Local release remains the no-force deletion of an accounted-for claim after the terminal-state checks below. A valid marker ref may also be deleted as optional cleanup with `--force-with-lease=refs/heads/bc-drain-claims/issue-<n>:<marker sha>`. A moved tip rejects cleanup; leave it alone. Markers left in place are harmless. Why: cleanup must not delete a claim acquired since inspection.

Release terminal worktrees/branches/claims only when their state is safely landed, blocked without useful local work, or validated in recovery. Never reset/clean the main checkout or another unit's worktree.

## Recurring-defect tune

When the same failure shape appears across at least two workers/reviews, patch the **run-local dispatch packet** for later workers with additive clarification. Never edit canonical concept files during a drain, weaken gates, or hide a recurring failure. Quote the patch and trigger in the final report; promotion to canon is a later user decision.

## Optional architecture observation

After successful landing, the driver may include at most one optional structural `architecture_observation` field per unit in the final report. Generate structural candidates separately from report assembly: duplicate candidates may be reduced to at most one report field, while an ordinary landed issue with no structural signal, shape-only observations, and deferred issues emit none. Its exact fields are `source`, `module`, `interface_or_seam`, `friction`, `deletion_test`, `evidence`, and `status: open`. The observation records evidence and friction only; it must never contain a proposed refactor, interface design, or implementation direction. Use `bc-codebase-design` vocabulary (`module`, `interface`, `depth`, `seam`, `adapter`) where applicable; record concrete structural friction that survives the deletion test or leaves behavior untestable through an interface, and omit shape-only taste. Bind `source` to the landed issue and commit and current tree; never cite an unlanded worker diff.

**With the table**, the sink is the project's ideas file. In the main checkout, after landing, append the observation as one line at the bottom, in the file's newest-last order, naming the landed issue and commit and its `module`, `interface_or_seam`, `friction` and `deletion_test` consequence; append in the same step one line for each follow-up the worker's handoff listed (workers never edit the ideas file themselves; see [execute-issue.md](execute-issue.md)). Commit these lines as a separate driver-owned context-only commit after landing, outside the review packet and implementation diff. Report the ideas-file path and that commit, or `not persisted` with the reason when the file is missing or unwritable. Why: the visible layout keeps agents' observations and follow-ups with other undecided ideas, a separate observation inbox is retired there, and a single writer after landing avoids parallel workers conflicting on one file.

**Without the table**, resolve the scaffolded-project inbox at `.bc-agent/research/architecture-observations.md`, or an explicitly declared equivalent path in project instructions. In that inbox the driver writes each new entry by prepending it in the consumer's current newest-first order, so bounded reads cannot hide new observations below older history. This remains a separate driver-owned context-only update after landing, outside the review packet and implementation diff. Report the inbox path and context commit, or report `not persisted` with the reason when the sink is missing or unwritable. Worker follow-ups go in the final report.

In both cases, pass the assembled report, review packet, seeded review/rework dispatches, approval, tier, landing, labels, issue state, and observation through an explicit handoff; return report/context copies carrying only the observation while leaving those authority inputs unchanged. This handoff does not dispatch a child and cannot affect review, rework, tier, approval, landing, labels, or issue state.

## Stop and report

Stop when the eligible queue drains, `max-iters` is reached, or systemic base/tool/environment failures recur. Let active children return to safe boundaries.

Write the full report to the run log (a `report.md` in the run artifact root) and give the user a short chat report drawn from it. The run log records: LANDED commits; HUMAN_BLOCKED reasons; REWORK_DEFERRED units and bundle/brief status; SYSTEMIC_FAILURE classifications; blocked/claimed units; recurring-defect packet patches; stop reason; each dispatched child as `role — launched model + thinking — list-API $` plus the child-run total (or `$unavailable` on a row or the total); review/rework rounds; repeated-finding circuit events; baseline/final full-validation counts; per-issue review tier with its reason and any escalation trigger; axes dispatched per round and re-reviews skipped by standing approval; any stale worktrees/claims; and what resume recovered: claims adopted, bundles restored, claims released as untouched, and claims left in place as unaccountable. Add the source page's report lines. Confirm the main checkout is clean.

The chat report is for someone who may be new to the pipeline. Lead with what landed and where (each unit, its commit, the branch it reached), then whether the checks passed and whether the reviews approved, then anything that needs the user (a blocked unit and its question, a deferred unit, a failure that stopped the run) and why the run stopped. Use plain words; leave out internal terms such as claim commit, review tier, marker or standing approval, recovery and artifact paths, and nothing-to-report lines (no stale claims, no storage check configured). Name the run log path once so the detail can be found. Why: in a stranger's test run, the chat report led with tiers, claims and `$unavailable` rows, which told a newcomer nothing they could act on.

Show the child cost table in chat only when at least one child's cost is known; when every cost is unavailable, the table stays in the run log only. The table lists children, not tokens. A token sum is noise here: cache swamps it, and Luna tokens are not Grok tokens. The comparable unit is list-API dollars. Each row is one dispatched auditor, worker, reviewer, or rework child — drain-phase role (`audit` / `build` / `review-spec` / `review-standards` / `review-combined` / `rework`), the launched model and thinking level, and that child's list-API cost — then `List-API estimate` as their sum:

```text
## Child runs
- #17 build — GPT-5.6 Luna max — $0.27
- #17 review-combined — Grok 4.6 high — $0.17
List-API estimate: $0.44
```

Price by summing the harness per-call `cost.total` when present, otherwise the provider's published input/cached/output rates. Write `$unavailable` rather than inventing a price. These are list equivalents, not subscription debits. Never report a single turn's `totalTokens` as the run. The driver session is not a child row. Child-token totals are not a run-control or report metric.
