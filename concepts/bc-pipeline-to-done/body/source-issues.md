# Issue source

The GitHub issue source of [bc-pipeline-to-done](SKILL.md). The unit of work is one issue, its claim key is `issue-<n>`, and its contract is the issue body or latest `## Agent Brief`. Everything here is specific to issues; the claim protocol, packets, review, landing, recovery and safety live in [SKILL.md](SKILL.md).

## Where issues and work items meet

When the project has no "Where things go" table, there are no work items: the issue tracker alone carries status and the project keeps its existing bookkeeping. Ideas and observations then go to `.bc-agent/research/architecture-observations.md` or the path the project instructions declare (see [Optional architecture observation](SKILL.md#optional-architecture-observation)).

With a table, work items are the source of truth and GitHub issues are optional pointers to them: an item records its issue on its `Issue:` line, and a large item's `plan.md` names each slice's issue in its step. The drain still selects work from issues; an item without an issue is not drained. Find an issue's item by searching the work stage folders for `#<n>` on an `Issue:` line or in a step.

## Cloud-lane provenance gate

Before selection, recovery, rework, or any claim/label mutation, read the issue's current labels. If `automated` is present, skip the issue: `automated` is the repo's cloud-lane provenance label, and cloud-build consumes both owner and automated issues. An issue without `automated` is still cloud-lane work — skipped, reported, and never released, deleted, reused, or relabelled, exactly like `automated` — when any of: its held claim tip (a non-marker claim commit) names `branch=cloud-build/issue-<n>` in its body; the issue carries `in-progress-agent` with a `cloud-build-run` comment; it has an open PR from head branch `cloud-build/issue-<n>`. A `cloud-build-run` comment alone, with a valid released-marker or absent ref, no `in-progress-agent`, and no open cloud PR, is history, not a live claim — the issue follows the normal owner path. Check labels first, then the read-only claim-tip body, then comments and PRs, before any recovery disposition or mutation; the read-only tip read for provenance authorizes no adoption, restore, release, or cleanup. Report any active claim (a held ref or `in-progress-agent`) on an `automated` issue; likewise, on an issue that is cloud-lane under the three live signals above, report any cloud-lane claim, `cloud-build-run` comment, or PR and never release, delete, reuse, or relabel that claim, including marker cleanup. It is cloud-lane work, not untouched or abandoned local work, even when local state is absent. If provenance (labels, claim tip, comments, or PRs) cannot be read, report and skip without mutation. Why: shared claim refs do not prove local ownership, and restart cleanup must not steal cloud work.

Leave pre-existing in-flight local bundles exactly as they are: no migration or deletion. Skipping automated or other cloud-lane work never authorizes cleanup of its surviving worktrees or recovery evidence. Non-automated issues without a held cloud-claim tip, without `in-progress-agent` with a `cloud-build-run` comment, and without an open `cloud-build/issue-<n>` PR retain the claim fences, recovery, review, owned-claim release, and attended driver landing below. A valid Released Claim Marker tip is still FREE, but an issue with an open `cloud-build/issue-<n>` PR or `in-progress-agent` with a `cloud-build-run` comment is still cloud-lane for selection.

## States

- `READY`: open and eligible (`ready-for-agent`).
- `IN_PROGRESS`: claimed build/review/rework (`ready-for-agent` + `in-progress-agent`; the remote claim branch is authoritative).
- `LANDED`: approved, committed, pushed, and closed.
- `HUMAN_BLOCKED`: requires a human decision, unavailable access/resource, contract clarification, or irreparable issue-local environment repair that only a human can perform (remove ready/in-progress; add `needs-human`).
- `REWORK_DEFERRED`: findings remain agent-fixable but the rework-round limit or no-progress rule is exhausted (keep ready, remove in-progress, add `rework-for-agent`, and post an Agent Rework Brief).
- `SYSTEMIC_FAILURE`: repeated tooling/base/environment failure; stop the run and explicitly classify affected issues.

A review rejection is not by itself a human blocker. Preserve useful fixable work through recovery rather than relabeling it `needs-human` or discarding its worktree.

## Preflight

Add these to the core preflight:

- Ensure `ready-for-agent`, `rework-for-agent`, `needs-human`, and `in-progress-agent` exist.
- Confirm issue/comment/close access and the ability to inspect PRD parent/children. A blocked, claimed, deferred, or open child keeps its parent open.

## Resuming an interrupted run

Apply the cloud-lane provenance gate above — labels, then the read-only claim-tip body, then comments and PRs — before marker classification and before any adoption, restore, release, or cleanup. The read-only claim-tip body read for cloud-claim provenance is part of that gate, not a recovery disposition. Also check issues carrying `in-progress-agent` even when their ref is absent, so active automated or other cloud-lane work is reported rather than treated as free local work. Only non-automated issues enter the recovery dispositions below, and never an issue with cloud-lane provenance.

For the core's untouched disposition:

- **Neither, and the issue is untouched** — release the claim and `in-progress-agent`, then treat it as `READY`. This disposition never applies to a cloud-lane claim: an untouched issue has no held cloud-claim tip naming `branch=cloud-build/issue-<n>`, no `in-progress-agent` with a `cloud-build-run` comment, and no open `cloud-build/issue-<n>` PR.

## Select

Exclude `automated` before classification or claim, and likewise any cloud-lane issue (held cloud-claim tip, `in-progress-agent` with a `cloud-build-run` comment, or open `cloud-build/issue-<n>` PR), for fresh, deferred, and `rework-for-agent` candidates alike; apply the cloud-lane provenance gate before any recovery or mutation, not after bundle restore or marker reuse. List oldest open candidates and parse dependencies from issue bodies and comments, including dependency headings and inline `blocked by` / `depends on` / `requires` / `after` / `prerequisite` references. Select only when every dependency is closed and neither claimed nor in flight. Skip `needs-human`, live claims (not valid marker refs), in-flight issues, and unresolved dependencies.

With a table, skip an issue whose work item is still in work-planned without a `Planned:` line, before claim, and report it as "needs planning"; file one note where the owner sees questions (the project's or the machine's instructions name the place) naming the item and that it needs `bc-plan-to-pipeline`. Do not run that planning yourself: it asks the owner questions, and this run is AFK. Why: the project's pickup rule requires every planned item to be planned before it starts, and a drain must never stall waiting on it.

Prioritize `rework-for-agent` candidates with a valid local recovery bundle. Otherwise prefer a concrete latest `## Agent Brief`; vague or decision-incomplete work becomes `HUMAN_BLOCKED`, not guessed work.

## Claim marks

After the claim ref proves ownership, add `in-progress-agent` and leave a run-id breadcrumb on the issue.

## Deferral

Post a portable comment:

```text
## Agent Rework Brief
Base SHA: <sha>
Unresolved findings: <compact list>
Validation: <summary and durable evidence references>
Next agent: <specific next actions>
```

Keep `ready-for-agent`, add `rework-for-agent`, remove `in-progress-agent`, mark it ineligible for the rest of this run, and release only after the bundle validates. If safe capture fails, retain evidence and follow the recovery contract's fail-safe handling—never silently delete useful work.

## Landing

After the core landing steps commit and push, the driver:

6. closes the issue with commit and validation evidence;
7. releases worktree, local branch, and claim, and removes both `in-progress-agent` and `ready-for-agent` from the closed issue (closing does not clear labels); then evaluates PRD closeout.

**Work-item update in the landing commit.** With a table, show the issue's progress by where its item sits and which steps are checked, in the same commit as the work: check the issue's step in the item; if the item is still in work-planned, `git mv` it to work-active; if this landing completes the item, fill its `## Outcome` with what landed (issue numbers, earlier commits, validation; the commit that moves the item is the landing commit, so it cannot cite its own SHA) and `git mv` it into the work-done month folder `<year>-<month>/` (create the month folder when missing). Never write a `Status:` line or a live-cursor page such as `.bc-agent/tasks/active.md`. Why: the folder is the status, so a written status can only disagree with it, and a separate bookkeeping commit leaves a window in which the tree shows finished work as active. This update is the only content in the landing commit outside the reviewed diff; it touches nothing but the item. If no item names `#<n>`, change no work file and report "no work item" for that issue; do not create one in the landing commit, because creating an item is planning, outside the reviewed diff. Without a table, skip it.

Close a parent PRD only when every child is completed and none is open, blocked, deferred, claimed, or in flight.

## Blocked

For `HUMAN_BLOCKED`, post a comment the human who will unblock can act on: the decision or missing access first, the options and what happens if they pick each, then the exact evidence. Leave SHAs, paths, and commands untouched. Do not load `plain-language`. Then remove ready/in-progress and add `needs-human`. For `SYSTEMIC_FAILURE`, stop new launches, let active children reach a safe boundary, preserve/classify each issue, and report stale resources rather than guessing or destructive cleanup.

## Report

Also report parent PRDs closed/open. Report active automated claims separately as cloud-lane work left untouched, including `in-progress-agent` without a held ref. In local-only mode, name the review branch and do not close issues.
