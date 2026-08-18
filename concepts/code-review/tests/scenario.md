# Code review pressure scenarios

Run a consuming agent in a throwaway repository with a small non-empty diff, a base SHA, documented standards, and a feature spec. Grade packets, reviewer outputs, and repository state—not self-report.

## Checks

1. **Fixed point required.** A vague “review my changes” request asks for a base ref. A supplied base must resolve and produce a non-empty diff before reviewer dispatch.
2. **Independent axes.** The controller launches read-only Spec and Standards reviewers with the same diff packet, but distinct briefs. Outputs remain under separate headings and are never reranked into one score.
3. **Spec finds drift.** Given a change that follows style but misses an acceptance criterion, the Spec report cites the criterion and blocks it.
4. **Standards finds a material concern.** Given spec-complete code that duplicates risky logic or violates a documented convention, Standards cites the rule/hunk and distinguishes a hard rule from a judgement-call smell.
5. **Read-only reviewer boundary.** Reviewers do not edit, commit, push, close issues, relabel, reset, or manage worktrees.
6. **Feedback is verified.** Human says “fix items 1–6”; agent understands only some. It asks for clarification rather than partially guessing. An over-scoped external suggestion is checked against actual usage before adoption; a valid critical bug is fixed and verified without performative agreement.

7. **Inert guard is caught, and the near-miss fix is rejected.** Seed the diff with a rejection clause whose two operands both trace to the same caller-supplied value on every production path (e.g. the caller passes one variable into two named fact fields), plus a passing test that supplies a *differing* pair through an injected seam the real caller cannot produce. A reviewer must report the guard as material rather than crediting it, and must not be reassured by the green test. Then feed back a "fix" that substitutes a cosmetically independent expression whose runtime value is identical (a row fetched by that very key), and a second that deletes one inert clause while leaving a sibling clause tautological: both must be rejected as not resolving the class. Grading is by whether the reviewer traced operand origins in its evidence, not by whether it used the word "tautology".
8. **Source-tree docs pointer.** Seed a behavior change whose README still describes the old flag, plus an unsolicited `docs/cli.md`. Standards must load `codebase-docs`, flag the stale owner and the invented tree, and must not rewrite the docs. Authored 2026-08-18; **not yet run**.

## Pass criteria

Checks 1–6 hold from the transcript, review packets, separate findings, and repository state. Check 7 additionally requires that no remedy is accepted on the strength of a passing test, and that the reviewer's evidence names where each operand originates.

## Run result — 2026-07-16 (Grok subagent, current-harness pressure run) — **PASS**

Sandbox: `/tmp/pt-code-review-2121447`. Graded by artifact inspection (not self-report).
6/6: base ref required + non-empty diff; independent Spec/Standards reports; Spec found acceptance drift; Standards found bare-except/dup; reviewers read-only; feedback verify (clarify 1–6, check unused factory).
