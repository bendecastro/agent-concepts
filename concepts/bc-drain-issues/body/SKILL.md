---
name: bc-drain-issues
description: Autonomously drain a repo's ready-for-agent and rework-for-agent GitHub issue queue with isolated worktrees, bounded rework, independent review, and driver-owned landing. Run after /bc-plan-to-issues.
disable-model-invocation: true
argument-hint: "[max-iters=20] [max-parallel=3] (optional caps; max-parallel 1 = sequential)"
---

# Drain Issues (AFK executor)

Drain eligible GitHub issues through isolated build, independent Spec and Standards review, bounded same-worktree rework, and driver-owned landing. The driver owns global state and publishing; fresh workers own code/tests/validation only. This separation prevents a worker from publishing its own unreviewed result.

Use these detailed contracts when entering their phases:

- Worker: [execute-issue.md](execute-issue.md)
- Reviewers: [review-contract.md](review-contract.md)
- Deferred-work capture/restore: [recovery-bundle.md](recovery-bundle.md)

The workflow is harness-agnostic. On Pi, use the installed minimal fresh roles `bc-drain-auditor`, `bc-drain-worker` (for build and rework), and `bc-drain-reviewer`; they exclude unrelated inherited context/skills and generic plan/progress conventions. Set model effort explicitly per this contract. Because the minimal roles do not inherit the broad skill catalog, pass the worker disciplines explicitly (`minimal-solution-ladder` on every implementation packet, plus `tdd`, `diagnosing-bugs`, and/or `bc-autoresearch-loop` where applicable); auditor/reviewer roles need none. Bound each read-only auditor/reviewer to four assistant turns and 12 tool calls; mutation-capable workers remain bounded by narrow packets and safe phase-boundary accounting, not arbitrary interruption. Use the configured compact tool descriptions, set top-level `artifacts:false` or an external artifact/session root (including resumed runs), and keep outputs outside issue worktrees. If a harness lacks these roles/controls, use equivalent fresh packets and authority boundaries. These are economy controls, not permission to weaken correctness gates.

## States

- `READY`: open and eligible (`ready-for-agent`).
- `IN_PROGRESS`: claimed build/review/rework (`ready-for-agent` + `in-progress-agent`; the remote claim branch is authoritative).
- `LANDED`: approved, committed, pushed, and closed.
- `HUMAN_BLOCKED`: requires a human decision, unavailable access/resource, contract clarification, or irreparable issue-local environment repair that only a human can perform (remove ready/in-progress; add `needs-human`).
- `REWORK_DEFERRED`: findings remain agent-fixable but a token/round circuit is exhausted (keep ready, remove in-progress, add `rework-for-agent`, and post an Agent Rework Brief).
- `SYSTEMIC_FAILURE`: repeated tooling/base/environment failure; stop the run and explicitly classify affected issues.

A review rejection is not by itself a human blocker. Preserve useful fixable work through recovery rather than relabeling it `needs-human` or discarding its worktree.

## Preflight — before the loop

Stop and report if a required check fails; AFK work must not invent mid-run decisions.

1. Confirm the target repo is clean, on `master`, and capture its remote and base SHA.
2. Run `python3 "$AGENT_CONCEPTS/scripts/publish-check.py" --repo "$PWD" --remote "<remote-url>" --branch master`. Exit 0 authorizes the configured operations. Exit 2 aborts unless the user pre-agreed to commit-only-local mode. Never edit the policy to authorize this run.
3. Confirm no-force creation/deletion of `bc-drain-claims/issue-<n>` is authorized. Without it, stop unless the user explicitly selected single-run mode. Labels/comments are advisory, not locks.
4. Ensure `ready-for-agent`, `rework-for-agent`, `needs-human`, and `in-progress-agent` exist.
5. Confirm issue/comment/close access and the ability to inspect PRD parent/children. A blocked, claimed, deferred, or open child keeps its parent open.
6. Record caps: `max-iters` (default 20), `max-parallel` (default 3), 200k child-token soft cap and 300k hard cap checked only at phase boundaries, initial review plus at most three rework/re-review cycles, and two consecutive token deferrals as the launch circuit.
7. Choose a run artifact root outside every worktree for review packets, `review-packet/issue-<n>/round-<r>/`, and verify it is writable.
8. Set worker effort explicitly: low for ordinary slices, medium for high-risk slices. Never silently inherit a higher AFK parent effort.
9. Verify worktree support and a root outside the checkout, default `${BC_DRAIN_WT_ROOT:-${TMPDIR:-/tmp}/bc-drain-worktrees/$(basename "$PWD")}`. Never build in the main checkout. Fixed-port tooling may require `max-parallel=1`.
10. Choose persistent recovery root `${XDG_STATE_HOME:-$HOME/.local/state}/bc-drain/recovery/<repo-key>/` and verify it can be written safely.
11. If a global qmd collection covers the repo, run `qmd update && qmd embed` once. Workers search it but never re-index.
12. Cache full project baseline validation once per base SHA: command, exit status, failing test IDs, concise summary, raw-log path outside the worktree, and content hash. This separates known failures from regressions without paying for a full suite every round.

## Resuming an interrupted run

A drain dies between phases more easily than it fails: a killed pane, a lost harness session, a restarted machine. Claims, worktrees, and uncommitted diffs all outlive it. Recover before relaunching — dispatching a fresh drain over live state pays again for work already on disk and can strand a reviewed diff that nobody is left to land.

After preflight and before the loop, list `refs/heads/bc-drain-claims/*` on the remote, then the worktree and recovery roots. The remote claims are the authoritative index of what a previous run owned, and they are authoritative precisely because they are the one record that does not live in a context that just proved it can vanish. For each claim:

- **Worktree present with an uncommitted diff** — adopt it. Re-derive the packet, re-run the deterministic pre-review gate, and take full fresh review on every axis. No standing approval survives a run whose reviewer records are gone; an approval is a record, and an unreadable record is not one.
- **Valid recovery bundle** — restore through [recovery-bundle.md](recovery-bundle.md) exactly as for a `rework-for-agent` candidate.
- **Neither, and the issue is untouched** — release the claim and `in-progress-agent`, then treat it as `READY`.
- **Anything else** — leave the claim, report it, and skip the issue for this run. Never release a claim you cannot account for, and never delete a worktree to make an inconsistency go away: the inconsistency is the evidence.

State the run artifact root and the recovery root in the run's opening report, not only in the final one. A path announced only at the end is announced only if the run reaches the end.

## Select, classify, and claim

List oldest open candidates and parse dependencies from issue bodies and comments, including dependency headings and inline `blocked by` / `depends on` / `requires` / `after` / `prerequisite` references. Select only when every dependency is closed and neither claimed nor in flight. Skip `needs-human`, live claims, in-flight issues, and unresolved dependencies.

Prioritize `rework-for-agent` candidates with a valid local recovery bundle. Otherwise prefer a concrete latest `## Agent Brief`; vague or decision-incomplete work becomes `HUMAN_BLOCKED`, not guessed work.

Classify risk cheaply in the driver before claim: **high-risk** means compatibility replacement/retirement, migration/cutover, systemd or external-service semantics, or a broad public acceptance surface. Classification may choose effort and packet shape, but no auditor/worker is dispatched before ownership is acquired.

Record a **review tier** with its classification reason at the same time. High-risk slices are tier 2 (two independent axes). Ordinary slices start at tier 1 (one combined reviewer) and escalate permanently on a pre-review gate rejection or any Critical finding; see [review-contract.md](review-contract.md). Tier is recorded before dispatch and reported per issue so the cheap path stays auditable; it never lowers mid-issue.

Atomically claim by creating a claim commit from the main checkout's tree with `git commit-tree` and pushing it without force to `refs/heads/bc-drain-claims/issue-<n>`. Only the successful creator owns the issue; losers skip it without spending child tokens. Then add `in-progress-agent`, leave a run-id breadcrumb, fetch `origin/master`, and create `bc-drain-work/issue-<n>` in the external worktree root.

For recovered work, follow [recovery-bundle.md](recovery-bundle.md) only after the claim succeeds. A matching base may restore directly; a changed base requires full diff inspection, validation, and full fresh review.

After the claim/worktree (and any restore) succeeds, a high-risk issue gets a fresh bounded read-only contract auditor before implementation. It produces:

```text
requirement -> observable test/check
existing public interface -> preservation test
external semantics -> evidence required
known baseline failure -> unchanged/regressed check
guard/rejection clause -> can-its-inputs-differ-in-production evidence
human-only verification -> explicit deferral
```

The guard row exists because an inert guard is the one defect a green suite actively hides: if both sides of a check resolve to the same value on every production path, only an injected test double can supply a differing pair, so the check passes by inspection and by coverage while protecting nothing. Trace each side to where the real caller obtains it. When the issue is *about* a guard, this row is mandatory for every guard the diff touches, keeps, or relocates — a fix that removes one inert clause while leaving its neighbour tautological has not resolved the class.

For replacement work, inventory the complete old public interface from source, tests, and help output—not merely the issue's new-command list. Map every acceptance criterion to evidence. For executable/loader replacement, include argument/environment/cwd/symlink or installed-launcher topology/path or module-resolution and privilege-boundary behavior, not output alone. When acceptance depends on an external platform's semantics (for example systemd, a database, or an API), verify the claim against available primary documentation such as installed man pages/help or an explicitly authorized authoritative source; repository prose and string-presence tests are not sufficient evidence. Record the source/version or mark verification unavailable. This audit exists because compatibility, launcher-security, and service-semantics omissions can pass narrow new-feature tests and become expensive only after landing. An unresolved product choice becomes `HUMAN_BLOCKED`; clear engineering work continues.

## Build and deterministic pre-review gate

Dispatch a fresh worker with [execute-issue.md](execute-issue.md), issue/Agent Brief, acceptance matrix, worktree, remote identity, base SHA, and baseline summary. Keep validation artifacts outside the project worktree.

When it returns `READY_FOR_REVIEW`, the driver—not a model reviewer—must deterministically verify:

- every acceptance-matrix row has evidence—on a rework round, carried-forward plus newly re-evidenced rows together, with the matrix→file map proving every row the fix touched was actually re-evidenced;
- status, changed-file list, and diff are in scope;
- targeted validation passed and the baseline delta is explicit;
- no files are staged and no unrelated files are present;
- validation evidence and raw logs are outside the worktree.

A passed gate materializes the round's review packet once, outside every worktree: `packet.json` (base SHA, worktree, issue ref, round, `diff_sha256`, axis scope, acceptance-matrix→file map), `diff.patch`, `changed-files.txt`, `acceptance-matrix.json`, `validation.json`, and on re-review `findings-prior.json`. Reviewers consume these paths instead of re-deriving status and diff, and `diff_sha256` is the identity that standing approvals bind to. A gate rejection escalates the issue to tier 2 permanently.

A failed gate returns fixable engineering defects for rework. Product/contract decisions, unavailable access/resources, or irreparable issue-local environment failures requiring human repair become `HUMAN_BLOCKED`; transient/repeated tooling, base, or environment failures stay out of `needs-human` and follow rework or `SYSTEMIC_FAILURE` handling. Do not spend reviewer tokens on mechanically incomplete work.

## Independent lean review and bounded rework

Follow [review-contract.md](review-contract.md). Dispatch fresh read-only reviewers on the round's packet, without the worker's reasoning or parent transcript: two independent axes in parallel at tier 2, one combined reviewer at tier 1. Both axes must stand approved. Minor findings do not block.

Record each approval as a standing record bound to the packet's `diff_sha256`. After a rework round, re-dispatch the axis that raised the findings, plus any axis whose deterministic invalidation trigger fired on the rework delta; an axis holding a standing approval over untouched scope is not asked the same question twice. An unmappable delta invalidates both axes—ambiguity costs a review, never an assumption.

For Critical/Important findings, retain the claim and same worktree. Launch a **fresh compact rework worker** with only the current worktree/base, the round's packet paths, unresolved findings, prior dispositions, validation evidence, and the driver-computed implicated row set (the acceptance-matrix rows those findings touch). It fixes and runs targeted validation, then the deterministic gate, packet refresh, and selective focused re-review repeat. Do not replay an accumulating transcript.

Allow the initial review plus at most three rework/re-review cycles. Continue only if material findings are resolved or the failure class materially changes. The same unresolved material finding after two attempted fixes defers immediately. This progress rule prevents superficially different patches from consuming an unbounded loop while preserving useful implementation state.

After each child returns, account tokens if available:

- Below 200k: normal bounded work.
- At/above 200k soft cap: omit optional broad investigation; use only focused packets and checks.
- At/above 300k hard cap: before launching another child, capture recovery and transition to `REWORK_DEFERRED`.
- If accounting is unavailable, round limits are the portable fallback.

Never interrupt an active mutation-capable child merely to meet a token threshold; only phase boundaries are safe because arbitrary interruption can leave partial filesystem state. Two consecutive token deferrals stop new launches and report `SYSTEMIC_FAILURE` at run level while classifying each issue `REWORK_DEFERRED` unless it independently needs a human.

On deferral, use [recovery-bundle.md](recovery-bundle.md), post a portable comment:

```text
## Agent Rework Brief
Base SHA: <sha>
Unresolved findings: <compact list>
Validation: <summary and durable evidence references>
Next agent: <specific next actions>
```

Keep `ready-for-agent`, add `rework-for-agent`, remove `in-progress-agent`, mark it ineligible for the rest of this run, and release only after the bundle validates. If safe capture fails, retain evidence and follow the recovery contract's fail-safe handling—never silently delete useful work.

## Driver-owned landing

Only after verifying that **every axis holds a standing approval whose `diff_sha256` equals the final reviewed diff**, the driver:

1. inspects status and the exact reviewed diff;
2. runs final relevant/full project validation once (the only full run after the cached baseline);
3. commits only issue-authored changes using project conventions;
4. runs publish authorization again as required;
5. pushes `HEAD:master`;
6. closes the issue with commit and validation evidence;
7. releases worktree, local branch, claim, and labels; then evaluates PRD closeout.

A rebase that changes the reviewed diff changes its hash, so no standing approval covers it: update the base, validate, and obtain fresh focused approval on both axes before push. The driver owns commit/push/close so implementation and rework workers cannot bypass the independent gate.

For `HUMAN_BLOCKED`, post a comment the human who will unblock can act on: the decision or missing access first, the options and what happens if they pick each, then the exact evidence. Leave SHAs, paths, and commands untouched. Do not load `plain-language`. Then remove ready/in-progress and add `needs-human`. For `SYSTEMIC_FAILURE`, stop new launches, let active children reach a safe boundary, preserve/classify each issue, and report stale resources rather than guessing or destructive cleanup.

Release terminal worktrees/branches/claims only when their state is safely landed, blocked without useful local work, or validated in recovery. Never reset/clean the main checkout or another issue's worktree. Close a parent PRD only when every child is completed and none is open, blocked, deferred, claimed, or in flight.

## Recurring-defect tune

When the same failure shape appears across at least two workers/reviews, patch the **run-local dispatch packet** for later workers with additive clarification. Never edit canonical concept files during a drain, weaken gates, or hide a recurring failure. Quote the patch and trigger in the final report; promotion to canon is a later user decision.

## Optional architecture observation

After successful landing, the driver may include at most one optional structural `architecture_observation` field per issue in the final report. Its exact fields are `source`, `module`, `interface_or_seam`, `friction`, `deletion_test`, `evidence`, and `status: open`. Use `codebase-design` vocabulary (`module`, `interface`, `depth`, `seam`, `adapter`) where applicable; record concrete structural friction that survives the deletion test or leaves behavior untestable through an interface, and omit shape-only taste. Bind `source` to the landed issue and commit and current tree; never cite an unlanded worker diff.

Resolve the scaffolded-project inbox at `.bc-agent/research/architecture-observations.md`, or an explicitly declared equivalent path in project instructions. The driver persists it only as a separate driver-owned context-only update after landing, outside the review packet and implementation diff. Report the inbox path and context commit, or report `not persisted` with the reason when the sink is missing or unwritable. This handoff does not dispatch a child and cannot affect review, rework, tier, approval, landing, labels, or issue state.

## Stop and report

Stop when the eligible queue drains, `max-iters` is reached, two consecutive token deferrals occur, or systemic base/tool/environment failures recur. Let active children return to safe boundaries.

Report LANDED commits; HUMAN_BLOCKED reasons; REWORK_DEFERRED issues and bundle/brief status; SYSTEMIC_FAILURE classifications; parent PRDs closed/open; blocked/claimed issues; recurring-defect packet patches; stop reason; per-issue and total child tokens by build/audit/review/rework phases (or `unavailable`); soft/hard crossings; review/rework rounds; repeated-finding circuit events; baseline/final full-validation counts; per-issue review tier with its reason and any escalation trigger; axes dispatched per round and re-reviews skipped by standing approval; and any stale worktrees/claims. Report what resume recovered: claims adopted, bundles restored, claims released as untouched, and claims left in place as unaccountable. Confirm the main checkout is clean. In local-only mode, name the review branch and do not close issues.
