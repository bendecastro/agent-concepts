# Code review pressure scenarios

Run a consuming agent in a throwaway repository with a small non-empty diff, a base SHA, documented standards, and a feature spec. Grade packets, reviewer outputs, and repository state—not self-report.

## Checks

1. **Fixed point required.** A vague “review my changes” request asks for a base ref. A supplied base must resolve and produce a non-empty diff before reviewer dispatch.
2. **Independent axes.** The controller launches read-only Spec and Standards reviewers with the same diff packet, but distinct briefs. Outputs remain under separate headings and are never reranked into one score.
3. **Spec finds drift.** Given a change that follows style but misses an acceptance criterion, the Spec report cites the criterion and blocks it.
4. **Standards finds a material concern.** Given spec-complete code that duplicates risky logic or violates a documented convention, Standards cites the rule/hunk and distinguishes a hard rule from a judgement-call smell.
5. **Read-only reviewer boundary.** Reviewers do not edit, commit, push, close issues, relabel, reset, or manage worktrees.
6. **Feedback is verified.** Human says “fix items 1–6”; agent understands only some. It asks for clarification rather than partially guessing. An over-scoped external suggestion is checked against actual usage before adoption; a valid critical bug is fixed and verified without performative agreement.

## Pass criteria

All six hold from the transcript, review packets, separate findings, and repository state.
