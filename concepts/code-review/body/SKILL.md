---
name: code-review
description: Use when requesting technical review of completed code, receiving review feedback, addressing PR comments, or deciding whether reviewer suggestions should be implemented.
---

# Code Review

Code review is technical evaluation, not emotional performance. Verify feedback against the codebase; request reviews with enough context for an independent reviewer to judge the diff.

## Requesting review

Use before merging, after a major task, after a complex bug fix, or when stuck and a fresh perspective could catch mistakes.

Prepare a review packet:

- What changed: 2–5 bullets or task name.
- Requirements/plan: the expected behavior or plan excerpt.
- Git range: base SHA and head SHA, or explicit changed files if no git range exists.
- Verification run: commands and outputs, not claims.

Ask the reviewer to check:

- Plan/requirement alignment.
- Code quality, edge cases, error handling, portability.
- Architecture and integration with surrounding code.
- Tests: behavior coverage, not just mocks.
- Production readiness: migrations, compatibility, docs, security where relevant.

Require severity buckets: **Critical** (must fix), **Important** (fix before proceeding unless consciously deferred), **Minor** (polish). Ask for file references, why it matters, and a clear merge/readiness verdict.

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

## Red flags

Stop and reassess if you are about to:

- Implement unclear multi-item feedback partially.
- Accept external feedback without checking the code.
- Ignore Critical/Important review findings.
- Treat tests passing as proof requirements were met without checking the requirements.
- Argue defensively instead of citing code, tests, compatibility, or scope.
