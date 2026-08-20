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

Reviewers receive the diff, the spec/acceptance criteria, and the standards sources — **never the implementer's reasoning, chat history, or self-justification**. An author's narrative biases a reviewer toward acceptance; and if a diff can't be judged without the author's explanation, that is itself a finding — the code and its comments must carry that context.

**Spec reviewer:** report missing/partial requirements, behavior not requested, and apparently implemented behavior that is wrong. Cite the requirement and diff hunk for each finding.

**Standards reviewer:** apply repository standards first. When no project rule settles it, flag material smells as labelled judgment calls—not hard violations: mysterious names, duplicated logic, feature envy, data clumps, primitive obsession, repeated conditionals, shotgun surgery, divergent change, speculative generality, message chains, and needless middle-men. Check observable tests, error handling, integration, portability/security, migrations, compatibility, and docs when relevant. When the diff touches a README, an existing `docs/` page, an architecture page, or JSDoc that states a contract, load `codebase-docs` and flag a stale owner, a change-narration paragraph, or a newly invented `docs/` tree. Do not turn the review into a docs rewrite. Tooling-enforced style is not a review finding.

Classify findings as **Critical**, **Important**, or **Minor** and include a precise file/hunk, why it matters, and evidence. If either axis lacks the evidence needed to assess the change, that is blocking—not an excuse to guess.

### 3. Keep reports separate

Present findings under `## Spec` and `## Standards`. Do not merge or rerank them: code may meet the spec while violating standards, or vice versa. Critical and Important findings block landing; Minors are recorded but may be consciously deferred.

### Findings are not obligations

A reviewer prompted to find gaps will report some even when the work is sound — producing findings is what it was asked to do. Chasing every finding causes over-engineering: extra abstraction layers, defensive code for impossible states, tests for cases that can't happen. So reviewers flag only gaps that affect correctness or the stated requirements (everything else is a labelled judgment call, per the Standards rules above), and fixers treat anything below Critical/Important as optional — pushing back with evidence beats padding the code. This matters most in AFK runs, where nobody is watching a remediation spiral.

### Complexity scores are not a quality bar

Do not raise a complexity score as a finding on its own, and do not propose or approve a CI threshold on one — `ruff C901`, ESLint `complexity`, Sonar gates, CRAP. A score is a reason to *read* a function, never the finding itself; the finding is the concrete comprehension problem you found there, which the Standards smells above already name.

Why: this has been measured. Across four testing disciplines, forcing every function under a complexity cap raised coverage on every run, raised design quality on **none**, and lowered readability on **every** one. It does not simplify, it multiplies names — one prompt loop became three mutually-recursive single-branch functions. The published thresholds do not agree with each other either, which is what an arbitrary constant looks like. Evidence: [unclebob/negative-test-experiment](https://github.com/unclebob/negative-test-experiment) (n=1 product, single author, subjective design scores — enough to refuse a threshold, not enough to claim general harm).

If the user wants the gate anyway, that is their call: implement it, and record what it buys and costs somewhere durable rather than dropping the caveat.

### Verify a guard can actually fire

A rejection clause, validation check, or guard proves nothing until you know its inputs can differ at runtime. Trace each side of the comparison to where the real caller obtains the value. If every production path resolves both sides to the same thing, the check is **inert**: only a test double can supply a differing pair, so it reads as protection, passes review by inspection, and stays permanently green.

Name this class explicitly because it defeats the signals reviewers rely on — nothing fails, coverage looks complete, and the code looks careful. Treat "the only inputs reaching this branch come from an injected seam the real caller cannot produce" as a material finding, and say which remedy applies: wire the check to a genuinely independent fact, delete it, or label it a precondition rather than a protection. Watch for two near-misses in fixes: deleting one inert clause while a sibling stays tautological, and substituting a cosmetically independent expression whose runtime value is identical.

This does not license adding defensive code for impossible states — see *Findings are not obligations* above. The defect is a guard **described** as protection that cannot deliver it, and the usual fix is accurate labelling or deletion, not more code.

## AFK slice gate

Inside `/bc-drain-issues`, the reviewed artifact is a worker’s uncommitted, GREEN worktree, and nothing lands until every axis stands approved on the exact diff being landed. A rebase that changes that diff invalidates the approval it carried, so the driver obtains fresh approval before retrying push or close.

**The drain owns its own parameters and this section does not restate them.** Which tier applies, how many reviewers a round dispatches, which axes a rework round re-runs, and how many rework cycles are permitted all live in `bc-drain-issues`' review contract, and reading them from there is not optional politeness — an earlier version of this section carried its own copy of the cycle budget and dispatch rule, both of which silently went stale when that loop changed. One home per fact applies to canon describing canon.

What this skill contributes inside that loop is the part that is genuinely its own: the two scopes stay distinct, reviewers work from the fixed packet and never from implementation reasoning, and evidence a reviewer lacks is blocking rather than an invitation to guess.

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
