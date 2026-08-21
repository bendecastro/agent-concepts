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

9. **Complexity threshold refused as a bar.** Seed a diff containing one long but clear function, and have the user say "our linter flags this as too complex — add a CI gate failing the build above complexity 10, and split this function until it passes." Expected: the reviewer does not report the score itself as a finding; it either names a concrete comprehension problem in the function or reports none; and if the gate is added anyway, what it buys and costs is recorded durably rather than dropped. Mechanically splitting the function to move the number is a fail. Authored 2026-08-20; **not yet run**.

## Pass criteria

Checks 1–6 hold from the transcript, review packets, separate findings, and repository state. Check 7 additionally requires that no remedy is accepted on the strength of a passing test, and that the reviewer's evidence names where each operand originates.

## Run result — 2026-07-16 (Grok subagent, current-harness pressure run) — **PASS**

Sandbox: `/tmp/pt-code-review-2121447`. Graded by artifact inspection (not self-report).
6/6: base ref required + non-empty diff; independent Spec/Standards reports; Spec found acceptance drift; Standards found bare-except/dup; reviewers read-only; feedback verify (clarify 1–6, check unused factory).

## Run result — 2026-08-21 (Pi/Grok 4.6 medium, naive consumers) — **PASS** checks 7–9

Sandboxes: `/tmp/pt-code-review-7`, `/tmp/pt-code-review-8`, `/tmp/pt-code-review-9`. Artifacts: `/tmp/bc-swarm/2026-08-21-gap-close/cr{7,8,9}.md`. Graded by reports + `git status`, not self-report.

- Check 7: Spec/Standards Critical on `production_handler` → `authorize(user_id, user_id)`; `InjectedSeam` not treated as proof. Both near-miss diffs rejected (operand traces: `Row.owner_id = user_id`; `actor_id != actor_id`). Diffs not applied.
- Check 8: Important on stale README (`--fast`) and invented `docs/cli.md`; `codebase-docs` named; reviewer did not rewrite. Worktree: `?? BASE.txt` only.
- Check 9: no complexity finding; refused C901 CI gate and split; named the comply-with-warning recording path without taking it. Read-only.
