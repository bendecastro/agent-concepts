# One bc-safe-runs skill holds the storage-safe test and worktree-removal rules that eleven skills restate

Why: The storage-safe preamble (guarded test runner, `mktemp -d` not `/tmp`, targeted tests only, storage health check) is restated in 11 skill bodies with drifting wording, because children do not load the kernel that owns it; `bc-find-bugs`, `bc-council-find-bugs` and `bc-prototype` run code without it. The "prove commits are in HEAD before removing a worktree" rule is restated in 6.
Done when: `bc-safe-runs` holds both rule sets; every former copy keeps one inline line plus a `loads` edge; the three skills lacking it load it; the inline-storage pressure scenarios of `bc-tdd` and `bc-code-review` pass against the new form.
Stage: now
Blocked by: nothing
Kind: architecture
Source: modularity scan 2026-11-27 (run ~/.local/state/bc-swarm/2026-11-27-agents-modularity/memo.md), owner pick 1 (candidate A)
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Requirements

- Callers today (`rg -l "guarded test runner" concepts/*/body`): bc-code-review, bc-delegate-investigation, bc-diagnosing-bugs, bc-dispatching-parallel-agents, bc-executing-plans, bc-finishing-development-branch, bc-optimize-code, bc-pipeline-to-done, bc-subagent-driven-development, bc-tdd, bc-writing-plans. Worktree-proof copies: `rg -l patch-equivalent concepts/*/body`; `bc-using-git-worktrees` § Cleanup keeps the full recipe and the module links it.
- Keep a one-line inline fallback in each caller (a skipped load must still leave a safe default); edit `concepts/relationships.json` and regenerate; keep the agent-kernel Storage safety section as the source the module derives from (note the derivation).
- Lands before 053-split-swarm-and-durable-subagents, which then loads it.

## Steps

- [x] Create `bc-safe-runs` and replace the restated blocks. Done when lint passes, `rg "guarded test runner" concepts/*/body` hits only the module and one-line fallbacks, and the re-run `bc-tdd/tests/pressure-storage-inline.md` and the matching bc-code-review scenario hold on the pressure-test model.

## Outcome

Done 2026-11-28. `bc-safe-runs` holds the storage-safe run rules and the prove-commits-in-HEAD rule; 14 skills load it (the pipeline builder gets it in its packet) and keep a one-line fallback that stops on critical or unknown storage health. Pressure runs on the pressure-test model: with the module 5/5 for both the bc-tdd and bc-code-review storage scenarios, fallback alone 4/5 each, so the owner chose to deploy it (shared bus, Pi, Claude, npm package). Review asked for builder wiring, the `git cherry` wording and stronger fallbacks; fix-verifier approved. Repeated-text warnings fell from 25 to 5. Three regression scenarios added after review are written but not yet run.
