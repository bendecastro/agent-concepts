---
name: bc-drain-issues
description: Autonomously drain a repo's ready-for-agent GitHub issue queue — pick the next unblocked issue, build it test-first in a fresh subagent, commit/push/close, and repeat until the queue is empty. Run after /bc-plan-to-issues.
disable-model-invocation: true
argument-hint: "[max-iters] (optional cap, default 20)"
---

# Drain Issues (AFK executor)

Drain the `ready-for-agent` issue queue autonomously. For each unblocked issue, dispatch a **fresh subagent** that builds just that slice test-first, validates it, commits, pushes `master`, and closes the issue — then move to the next. Designed to run unattended (AFK) after `/bc-plan-to-issues` has produced the queue.

**Fresh-subagent-per-issue is deliberate:** it forces every issue to be self-contained — the entire handoff is the issue body + `CONTEXT.md` + the repo, nothing else — and it prevents context rot across a long queue. The per-issue contract lives in [execute-issue.md](execute-issue.md); hand it to each subagent.

## Preflight — run once, before the loop
Stop and report if any check fails. AFK means nobody is here to answer a prompt mid-run, so everything that needs a human decision happens here, up front.

1. **Repo & branch.** Confirm you're in the target git repo on branch `master` (the only branch `publish.yaml` authorizes for trunk-based push). Capture the remote URL.
2. **Push authorization.** Run:
   ```
   python3 ~/Sync/CONFIG/agents/scripts/publish-check.py --repo "$PWD" --remote "<remote-url>" --branch master
   ```
   - **exit 0** → push authorized; proceed.
   - **exit 2** → push is NOT authorized for this repo. Do **not** push. Either **abort** and tell the user to pre-authorize the repo in `policies/publish.yaml` (copy the `image-maze-push-and-close-after-agent-work` rule, swapping `paths`/`remotes`), or — only if the user pre-agreed to a local-only run — continue in **commit-only-local mode** (commit per slice, never push, never close issues; report the branch at the end). **Never edit `publish.yaml` to authorize yourself** (self-amendment immunity).
3. **Claim coordination.** Hard parallel safety requires a remote Git claim namespace. Labels, assignees, comments, and kanban/project columns are advisory — two agents can race them. Before a parallel/AFK run, confirm the user or `publish.yaml` authorizes pushing and deleting coordination branches named `bc-drain-claims/issue-<n>` on the shared origin. If not authorized, **stop** unless the user explicitly chose single-run mode; single-run mode is not safe with another drain already running.
4. **Labels.** Ensure `ready-for-agent`, `needs-human`, and `in-progress-agent` exist (`gh label create` if missing). `in-progress-agent` is only a visible hint; the claim branch is the lock.
5. **Caps.** Note `max-iters` (arg, default 20) and the circuit-breaker threshold (default **3** consecutive parks). These bound a runaway or systemically-broken run.

## Driver loop
Repeat until a stop condition fires:

1. **Find candidates:** list *oldest OPEN* `ready-for-agent` issues whose every "Blocked by #NN" references a **closed** issue. Skip `needs-human`, `in-progress-agent`, and anything still blocked by an open issue. Prefer issues with a latest `## Agent Brief` comment/body; if a candidate is vague or lacks concrete acceptance criteria, do not guess — relabel/route it through `/triage` or PARK with `needs-human`. (`gh issue list --label ready-for-agent --state open`, then read each candidate's brief/body, "Blocked by", and blocker state.)
2. **Atomically claim one candidate:** try candidates in order until one claim succeeds.
   - Create a unique no-worktree claim commit from the current tree, e.g. `claim_commit=$(printf 'bc-drain claim issue #%s\nrun: %s\n' "$n" "$RUN_ID" | git commit-tree "$(git rev-parse HEAD^{tree})" -p HEAD)`.
   - Push it without force to `refs/heads/bc-drain-claims/issue-$n`: `git push origin "$claim_commit:refs/heads/bc-drain-claims/issue-$n"`.
   - Success means this run owns issue `#<n>`. Failure means another runner claimed it first; skip it and try the next candidate. Do not work an issue unless the claim push succeeded.
   - After a successful claim, add `in-progress-agent` and comment `Claimed by <harness/user/run id>` for humans. These are advisory breadcrumbs; never treat them as the lock.
3. **Stop conditions** — terminate the loop, then report:
   - No eligible unclaimed issue (queue drained, or only blocked/parked/claimed issues remain).
   - `max-iters` reached.
   - **Circuit-breaker:** N consecutive issues parked → stop. A run of parks means something systemic is broken (bad base state, broken env); continuing just burns tokens and makes noise.
4. **Execute** the claimed issue in a **fresh subagent** (your harness's subagent/Task tool), loaded with `execute-issue.md` + the issue number + the repo path. The subagent returns exactly one of: **LANDED** (committed/pushed/closed) or **PARKED** (commented + relabeled `needs-human`, nothing pushed).
5. **Release the claim:** after LANDED or PARKED, delete the claim branch (`git push origin --delete bc-drain-claims/issue-<n>`) and remove `in-progress-agent`. If cleanup fails, report the stale claim branch explicitly; a later runner may reclaim only after a human confirms it is stale.
6. **Tally:** reset the consecutive-park counter on LANDED; increment it on PARKED.
7. Loop.

## End-of-run report
Summarize: issues **LANDED** (with commit shas) and **PARKED** (with the stuck reason), issues still **blocked**, and **why the loop stopped** (drained / max-iters / circuit-breaker). In commit-only-local mode, name the branch to review.
