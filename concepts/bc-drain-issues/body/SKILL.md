---
name: bc-drain-issues
description: Autonomously drain a repo's ready-for-agent GitHub issue queue — pick the next unblocked issue, build it test-first in a fresh subagent, commit/push/close, and repeat until the queue is empty. Run after /bc-grill-to-issues.
disable-model-invocation: true
argument-hint: "[max-iters] (optional cap, default 20)"
---

# Drain Issues (AFK executor)

Drain the `ready-for-agent` issue queue autonomously. For each unblocked issue, dispatch a **fresh subagent** that builds just that slice test-first, validates it, commits, pushes `master`, and closes the issue — then move to the next. Designed to run unattended (AFK) after `/bc-grill-to-issues` has produced the queue.

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
3. **Labels.** Ensure `ready-for-agent` and `needs-human` exist (`gh label create` if missing).
4. **Caps.** Note `max-iters` (arg, default 20) and the circuit-breaker threshold (default **3** consecutive parks). These bound a runaway or systemically-broken run.

## Driver loop
Repeat until a stop condition fires:

1. **Select the next issue:** the *oldest OPEN* `ready-for-agent` issue whose every "Blocked by #NN" references a **closed** issue. Skip `needs-human` issues and anything still blocked by an open issue. (`gh issue list --label ready-for-agent --state open`, then read each candidate's "Blocked by" and check blocker state.)
2. **Stop conditions** — terminate the loop, then report:
   - No eligible issue (queue drained, or only blocked/parked issues remain).
   - `max-iters` reached.
   - **Circuit-breaker:** N consecutive issues parked → stop. A run of parks means something systemic is broken (bad base state, broken env); continuing just burns tokens and makes noise.
3. **Execute** the selected issue in a **fresh subagent** (your harness's subagent/Task tool), loaded with `execute-issue.md` + the issue number + the repo path. The subagent returns exactly one of: **LANDED** (committed/pushed/closed) or **PARKED** (commented + relabeled `needs-human`, nothing pushed).
4. **Tally:** reset the consecutive-park counter on LANDED; increment it on PARKED.
5. Loop.

## End-of-run report
Summarize: issues **LANDED** (with commit shas) and **PARKED** (with the stuck reason), issues still **blocked**, and **why the loop stopped** (drained / max-iters / circuit-breaker). In commit-only-local mode, name the branch to review.
