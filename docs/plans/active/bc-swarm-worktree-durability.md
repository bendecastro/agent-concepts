# Gap: the swarm durability contract does not cover a worktree child's commits

Date: 2026-08-25
Status: active
Verification: first pressure check 6 failed (producer half PASS; recovery half FAIL); recovery-trigger and recovery-safety tune implemented; rerun pending

Hand this file to an agent. It is self-contained; you need no other context to act on it.

## The gap in one sentence

`concepts/bc-swarm/body/SKILL.md` makes a child's **artifact file** durable, but a `worker`
child launched with `worktree: true` puts its real deliverable in a **Git commit on a branch in
a temporary worktree** — and that worktree and branch can be destroyed when the run ends, leaving
the commit unreachable and absent from the parent's tree.

## Evidence (observed 2026-08-25, not hypothetical)

Repo `~/Sync/Work/PUBLIC/Agents`. A `worker` child, run id
`d400723f-5e9a-4320-ac68-eb876b319957`, was launched with `worktree: true`. It completed
successfully and reported committing its work. Then:

- `/tmp/pi-worktree-d400723f-5e9a-4320-ac68-eb876b319957-0` did not exist on disk.
- That path was absent from `git worktree list`.
- No matching branch appeared in `git branch -a`.
- `master` was unchanged; the commit was in no reachable ref.
- `git fsck --no-reflogs --lost-found` listed it as `dangling commit bbaa6e9…`, among ~20 other
  dangling commits from earlier runs.

It was recovered with `git cherry-pick bbaa6e9` **only because the child's artifact file
happened to contain the line `Commit: bbaa6e9 bc-wiki-maintain: enforce additive promotion
diffs`.** Without that SHA, recovery means identifying the right commit among many dangling ones
by inspecting each. Dangling objects are pruned by `git gc`, so the recovery window is finite.

An inconsistency worth investigating rather than assuming: seven *older* `pi-parallel-*`
worktrees from previous runs were still present in `git worktree list` at the same moment. So
worktree teardown is not uniform, and whatever destroyed this one did not destroy those. Find out
what actually reaps them before designing around a guess.

## Gap as of filing

At filing, the portable durability contract treated the artifact as the
worktree worker's deliverable even though the real deliverable was a commit
(and harness patch), and its recovery order stopped after the manifest,
artifacts, and retained runs. It did not require a parent packet to carry the
worker's own-line commit/branch records or define guarded patch, full-range
commit, preserved-worktree, and recorded-SHA recovery before relaunch.

## What to change

Judgment is yours; these are the constraints the evidence establishes, not a prescribed diff.

1. **Make a worktree child's commit identity part of its artifact.** The child must record its
   commit SHA and branch name on their own lines in the artifact — not buried in prose, and not
   only in the returned summary, which dies with the parent. This is the cheap fix and it is what
   saved the run above by accident; make it deliberate.
2. **Add Git object recovery to rule 4's order**, after retained runs and before re-dispatch:
   `git fsck --no-reflogs --lost-found`, matched against the SHA the artifact recorded.
3. **Consider making the parent integrate promptly.** The parent already owns integration and
   verification. The window between "child finished" and "worktree reaped" is the whole exposure;
   a parent that cherry-picks or merges on receipt has no window. Weigh this against the parent
   being told not to block on children.
4. **Do not weaken rule 2.** Async fan-out with distinct `output` paths stays. This gap is
   orthogonal — it is about what a child's deliverable *is*, not about how the fan-out is launched.

## Acceptance

- `concepts/bc-swarm/CONCEPT.md` records the design decision and cites this evidence.
- `python3 scripts/lint.py` passes.
- `log.md` gets a dated entry per this workspace's `AGENTS.md` bookkeeping convention.
- The test gate applies: `bc-swarm` is a discipline-enforcing concept, so a durability rule change
  needs a pressure scenario in `concepts/bc-swarm/tests/` before it is treated as verified.
  Update `test_status` in `CONCEPT.md` frontmatter honestly if it is not re-run.
- If the swarm-mode operator prompt (the injected text that turns swarm mode on) carries its own
  copy of the durability rules, it drifts from the concept unless changed in the same pass. Check
  for that copy and say plainly whether you could reach it.

## Scope guard

Fix the durability contract. Do not redesign roles, routing, fan-out width, or turn budgets.
