---
name: code-review
description: Review a diff or completed change for independent Spec fidelity and Standards quality; also use when receiving review feedback or deciding whether comments should be implemented.
---

# Code Review

Code review is technical evaluation, not emotional performance. Verify feedback against the codebase; request reviews with enough context for an independent reviewer to judge the diff.

## Two-axis diff review

For a branch, work-in-progress diff, PR, or completed task, review two independent axes:

- **Spec** — does the change faithfully implement the issue, PRD, ticket, or acceptance criteria without omissions or scope creep?
- **Standards** — does it follow repository conventions and avoid material code-quality, integration, test, portability, security, or documentation problems?

### 1. Pin the review packet

Use the caller’s explicit base SHA/ref. If none is supplied, ask for one; an AFK driver must pass the recorded base SHA. Capture:

- `git diff <base>...HEAD` for committed work, or `git diff <base>` for an uncommitted worktree;
- commit list or changed-file list;
- issue/spec/acceptance criteria and domain context;
- repository standards sources and validation commands/results.

Stop if the base does not resolve or the diff is empty. Never review a vague “latest changes” blob.

### 2. Review independently

Run read-only Spec and Standards reviewers in parallel. They must not edit files, commit, push, close issues, mutate labels, reset a worktree, or manage its lifecycle.

**Spec reviewer:** report missing/partial requirements, behavior not requested, and apparently implemented behavior that is wrong. Cite the requirement and diff hunk for each finding.

**Standards reviewer:** apply repository standards first. When no project rule settles it, flag material smells as labelled judgment calls—not hard violations: mysterious names, duplicated logic, feature envy, data clumps, primitive obsession, repeated conditionals, shotgun surgery, divergent change, speculative generality, message chains, and needless middle-men. Check observable tests, error handling, integration, portability/security, migrations, compatibility, and docs when relevant. Tooling-enforced style is not a review finding.

Classify findings as **Critical**, **Important**, or **Minor** and include a precise file/hunk, why it matters, and evidence. If either axis lacks the evidence needed to assess the change, that is blocking—not an excuse to guess.

### 3. Keep reports separate

Present findings under `## Spec` and `## Standards`. Do not merge or rerank them: code may meet the spec while violating standards, or vice versa. Critical and Important findings block landing; Minors are recorded but may be consciously deferred.

### Findings are not obligations

A reviewer prompted to find gaps will report some even when the work is sound — producing findings is what it was asked to do. Chasing every finding causes over-engineering: extra abstraction layers, defensive code for impossible states, tests for cases that can't happen. So reviewers flag only gaps that affect correctness or the stated requirements (everything else is a labelled judgment call, per the Standards rules above), and fixers treat anything below Critical/Important as optional — pushing back with evidence beats padding the code. This matters most in AFK runs, where nobody is watching a remediation spiral.

## AFK slice gate

Inside `/bc-drain-issues`, both axes independently approve a worker’s uncommitted, GREEN worktree before its initial commit, push, or close. The driver owns reviewer dispatch and passes the full review packet. One remediation and re-review cycle is allowed; a second material rejection or ambiguity parks the slice. If a non-fast-forward push requires a rebase that changes the reviewed committed diff, the driver re-reviews that diff before a retrying push/close; a material post-rebase finding parks it rather than opening another remediation cycle.

## Requesting review

Use before merging, after a major task, after a complex bug fix, or when stuck and a fresh perspective could catch mistakes. Prepare the fixed review packet above; do not make reviewers infer requirements or verification from chat history.

## Receiving review

Before implementing feedback:

1. Read all feedback.
2. Restate unclear requirements or ask before changing code.
3. Verify against codebase reality.
4. Evaluate whether it is sound for this codebase.
5. Implement one item at a time and test each fix.
6. Push back with technical evidence when feedback is wrong or over-scoped.

Never respond with performative agreement (`You're absolutely right`, `Great point`, `Thanks`). Either act, ask a precise question, or give technical reasoning.

## External reviewer skepticism

External feedback is a suggestion to evaluate, not an order. Check whether it:

- Breaks existing behavior or compatibility.
- Conflicts with user/project decisions.
- Adds unused “proper” infrastructure. Grep for actual usage; if unused, ask whether to remove/defer instead.
- Assumes context the reviewer did not have.

If you cannot verify a suggestion, say what evidence is missing and ask whether to investigate, ask the reviewer, or proceed.

## GitHub review comments

When replying to inline GitHub review comments, reply in the thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`) rather than as a top-level PR comment.
