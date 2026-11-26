# Results: default-branch scenario, 2026-11-26

Scenario: [scenario-default-branch.md](scenario-default-branch.md). Consumer `openai-codex/gpt-6.1-terra`, thinking low, headless Pi dry run, one run per arm, deployed skills and overlays hidden. Fixture: clean clone on `main` whose `origin/HEAD` is `refs/remotes/origin/main`.

The comparison arm loaded the skill body at the commit before this change (it required `master`), not no skill: the defect is in the old wording, and a run without the skill has no reason to assume `master`.

| Criterion | Old body | New body |
|---|---|---|
| 1. Preflight resolves `main` and records it as the target branch; publish check targets it | FAIL: saw the trunk is `main`, then "the supplied skill literally requires `master`; this is a preflight mismatch, so an actual run must stop until the owner authorizes" | PASS: "Target branch: **main**, resolved once from `refs/remotes/origin/HEAD`"; manifest records `target_branch=main`; policy checked for `origin/main` |
| 2. Claims on a separate ref; work starts from fetched target | PASS (conditional on the mismatch being resolved) | PASS: "Fetch `origin main`, record the fetched tip as the worktree base" |
| 3. Landing pushes to `main`, never the handoff's `master` | PASS in text, but marked conditional on owner override | PASS: `git push origin HEAD:refs/heads/main` |

Both runs left only `plan.md` untracked; no pushes, commits or launches. The old arm's plan blocks the run, which is the reported bug: a repository on `main` cannot pass preflight. Held: the new body passes all three, the old body fails criterion 1.

Note: both arms saw the owner's machine-wide instructions (the new plan mentions the owner's offload wrapper); this does not touch the graded criteria.
