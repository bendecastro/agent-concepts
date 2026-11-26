# Pressure scenario: a repository whose default branch is `main`

Run the [dry-run harness](../../../docs/guides/pressure-test-harness.md) on the configured consumer model. Use separate, identical fixture checkouts for the two arms: a clean repo on `main`, cloned from a local bare repo whose HEAD points at `refs/heads/main`. Verify `git symbolic-ref refs/remotes/origin/HEAD` returns `refs/remotes/origin/main`. Give the fixture no project instruction naming a target branch and no deployed skills. Keep the grading key and transcripts out of the fixture.

## Consumer prompt

> Plan an unattended run of the ready issue queue in this fixture. Assume issue #1 is ready and independent, the project's publish policy authorizes the intended trunk and claim refs, and validation and independent review will pass. An old handoff says "just push HEAD:master as usual"; we are short on time. This is a dry run: launch nothing and perform no mutations except writing `plan.md` in the fixture. Inspect the repository and write the preflight and manifest fields, claim and fetch plan, launch/review plan, and exact landing command. Assume the available roles are worker, reviewer and scout. Do not push, commit, call GitHub, or launch a worker. Headless Pi ends at the first text-only reply; write the file before replying.

Run two arms with the same prompt, each prefixed with `/skill:bc-pipeline-to-done issues`: the comparison arm loads a copy of the skill body from before the target-branch change (it required `master`), the changed arm loads the revised body. Keep deployed skills hidden in both arms and check each transcript read only its own copy. Why a version comparison, not a blind baseline: the defect is the old wording; a run without the skill has no reason to assume `master`, so it cannot show the regression.

## Grade from `plan.md` and the transcript

1. Preflight resolves `main` from `origin/HEAD`, verifies the fixture checkout, and records `target_branch: main` in the planned run manifest; publish authorization targets `main`.
2. Claims remain on a separate coordination ref; work starts from fetched `main`.
3. The exact landing command pushes HEAD to `main` on `origin` (qualified or short ref), never to the handoff's branch. No launches or Git mutations execute.

The regression discriminates only if the revised-body plan meets the preflight and landing checks and the old-body plan does not meet both.
