---
name: bc-find-bugs
description: Hunt a named area (or a small whole repo) for wrong behaviour, reproduce the strongest candidates as failing tests on a hunt branch, and report Confirmed and Suspected bugs for the owner to file.
disable-model-invocation: true
argument-hint: "[area] [--since <ref>] [--max-repro N]"
---

# Find Bugs

Find code that does the wrong thing, and prove it. A bug counts as **confirmed** only when a reproduction you ran failed for the reason you stated. Everything else is **suspected**, however sure you feel. Why: a confident reading is not evidence; a failing test is, and a fix can start from it.

This skill hunts and reports. It does not fix bugs and does not edit production code.

## 1. Scope

- **Area**: the folder, module or feature the owner names. With no area, hunt the whole repo only when it is small (roughly a few thousand lines of source); otherwise ask which area. Why: deep reading of a bounded area finds real bugs; a large repo spreads the reading thin.
- `--since <ref>`: limit the hunt to code changed since that ref (`git diff --name-only <ref>...HEAD`), reading unchanged callers as needed.
- `--max-repro N`: how many candidates to reproduce (default 12).

Name the hunt `<YYYY-MM-DD>-<area-slug>`; it names the branch and the report.

## 2. Hunt

Read the code and its tests. Look for wrong behaviour of every kind:

- **inputs and edge cases**: empty, zero, negative, boundaries, off-by-one, rounding, unicode, duplicates;
- **error and failure paths**: swallowed exceptions, partial failure, wrong fallback, cleanup skipped on error;
- **state and data lifecycle**: lost or duplicated writes, stale caches, mutation of shared or default values, data dropped on save/load;
- **concurrency and ordering**: unguarded shared state, check-then-act, order-dependent results;
- **contracts between modules**: units, indexing, None vs empty, a caller assuming what a callee does not promise.

Read what a name, docstring, test or caller says the code should do, then check the code does that. Code that looks wrong is not a bug until you can state an input whose actual result differs from the expected one; many odd-looking lines are correct. Why: a candidate without a concrete wrong result cannot be reproduced and wastes a reproduction slot.

A security hole seen in passing goes in the report as a candidate with `Kind: security` and a pointer to the `bc-security-audit` skill; do not audit further. Slowness is out of scope.

Write each candidate in this form:

```
### <id> <one-line title>
Kind: bug | security
Location: <path>:<line(s)>
Evidence: <quoted code lines>
Claim: <what goes wrong, in behaviour terms>
Reproduction: input <...>; steps <...>; expected <...>; actual <...>
```

Rank candidates by the strength of the quoted evidence.

## 3. Reproduce

Load `bc-safe-runs`. Else: guarded test runner (fallback `pytest`; no custom `--basetemp`), `mktemp -d` outside `/tmp`, targeted tests; configured storage check before full suites, worktrees, fan-out: stop if critical or unknown, or if the check cannot run.

Work in a separate git worktree on a new branch `find-bugs/<hunt-name>` (`git worktree add -b bc-find-bugs/<hunt-name> <path>`). Never write reproductions in the owner's checkout. Why: the branch is what the filed items point at, and the owner's tree stays untouched.

Take the strongest candidates in rank order, up to `--max-repro` (default 12). For each, spend at most 10 minutes:

1. Write the reproduction: a test in the project's own test framework, in a new file named for the hunt (e.g. `tests/test_find_bugs_<area>.py`), one test per candidate named for it. With no test framework, a small script under `find-bugs/` that prints the wrong result and exits non-zero.
2. Assert the **expected** behaviour, so the test fails while the bug exists and passes once it is fixed. Do not assert the buggy result.
3. Run it and read the failure. Keep it only if it fails for the stated reason: the assertion about the claimed wrong result fails, not an import error, typo, wrong fixture or a different bug. Why: a test that fails for another reason proves nothing about the claim (see `bc-tdd`: watch it fail for the right reason).
4. If it passes, the code is probably right: delete the test and move the candidate to suspected with "reproduction passed" or drop it if the reading was wrong. If it fails for another reason and you cannot fix the test in the time left, delete it and mark the candidate suspected with that reason.

Commit the kept reproductions on the hunt branch. The project's suite on that branch now fails exactly in the kept tests; say so in the commit message.

Candidates beyond the limit stay suspected, marked "not attempted". While slots remain, attempt every candidate, including concurrency and ordering ones (drive the interleaving with threads, a barrier or a patched boundary); a candidate you tried and could not reproduce in time is "could not reproduce in 10 minutes: <why>", never "not attempted". Why: in the first test both runs left a race "not attempted" with three slots unused.

## 4. Report

Write the report as Markdown, `find-bugs-report.md` at the root of the hunt worktree, committed on the hunt branch, and show its path. Sections:

1. **Scope**: area, `--since` ref if any, commit hunted, branch name.
2. **Confirmed**: for each kept reproduction, the candidate block plus the test path and name on the branch and the failing output (the assertion lines).
3. **Suspected**, ranked by evidence: each candidate block plus why it is not confirmed ("not attempted", "reproduction passed", "could not reproduce in 10 minutes: <why>", "needs <environment>").
4. **Security** candidates, if any, each pointing at `bc-security-audit`.
5. The filing question, last: "Confirmed bugs are pre-selected for filing. Reply `all` to file them, or name the ones to file, the suspected ones to investigate, and any to reject with a reason."

## 5. File (after the owner answers)

Load `bc-file-findings` and file as it says. Else: wait for the owner's pick (an answer in the invoking message is the pick); chosen → numbered work-planned items, rejected → work-dropped with the reason, the rest → ideas lines, numbered only from the main checkout, each placed in `work/order.md`, then `work_index.py --check`; then plan each filed item with `bc-plan-to-pipeline` in the same reply; without a project work pipeline, file nothing and say so.

What this hunt supplies to it:

- **Chosen** is every confirmed bug (`all`) plus each suspected bug the owner picks. Each item gets `Kind: bug` and `Source: find-bugs`, the hunt branch name, and for a confirmed bug the test path and name and the failing output; a picked suspected bug becomes an investigation item stating it is unconfirmed and quoting the evidence.
- **Security candidates picked** → items with `Kind: security`, pointing at `bc-security-audit`.
- Ideas lines point at the report on the hunt branch. Keep the hunt branch: filed items point at it. Without a pipeline, keep the report and hunt branch.
- When planning a filed item, each reproduction test settles its test seam.
