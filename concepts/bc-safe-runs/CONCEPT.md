---
test_kind: pressure
test_status: pass # 2026-11-28 Terra low: bc-tdd and bc-code-review storage scenarios 5/5 with the module; fallback-only arms 4/5 each (tests/pressure-safe-runs.md)
tested: 2026-11-28
deployed: no
---
# Concept: safe-runs

Model-invoked module that holds the storage-safe run rules (guarded test runner, no custom `--basetemp`, temp-file cleanup, `mktemp -d` scratch never under `/tmp`, targeted tests while working, storage health check before full suites, worktrees and fan-out), the packet line that carries them into worker and reviewer tasks, and the rule to prove a worktree's commits are in `HEAD` before removing it.

## Design decisions

- **One home instead of eleven restatements (2026-11-28, item 054-safe-runs-module).** Children and installed-alone skills do not load the agent kernel, so 11 skills restated its Storage safety rules in drifting wording and 6 restated the worktree-removal proof; `bc-find-bugs`, `bc-council-find-bugs` and `bc-prototype` ran code without them. Each caller now loads this skill and keeps one inline fallback line under 40 words, identical everywhere, so a skipped or missing load still leaves a safe default. Why under 40 words: the repeated-text lint ignores shorter paragraphs, so the fallback does not reintroduce the warnings this module removed.
- **Derived from the kernel, not a replacement for it.** The rules derive from the `agent-kernel` Storage safety and Verification sections; the kernel keeps its copy because it is always loaded where installed. The `depends_on_contract` edge to `agent-kernel` marks that a kernel change must update this module and the fallbacks.
- **Packet line.** Children do not load skills on their own (subagent roles often run without inherited skills), so the module ships one quotable line for worker and reviewer tasks instead of each caller wording its own.
- **Worktree removal keeps its full recipe in `bc-using-git-worktrees` § Cleanup.** The module states the proof rule and names that section for resolved conflict picks and branch deletion, so the recipe is not duplicated.
- **Owner specifics go in a private overlay.** The body names "the guarded test runner the project's or machine's instructions name"; a machine may supply its tool names in `~/.config/agent-concepts/overlays/bc-safe-runs.md`.

## Provenance

- `concepts/agent-kernel/body/AGENT-KERNEL.md` § Storage safety (temp-file cleanup, scratch folders, the 14,000-folder and 5.7 GB `/tmp` incidents) and § Verification (targeted tests, one full suite per integrated tree) — source of the rules.
- The inline storage blocks previously restated in bc-code-review, bc-delegate-investigation, bc-diagnosing-bugs, bc-dispatching-parallel-agents, bc-executing-plans, bc-finishing-development-branch, bc-optimize-code, bc-pipeline-to-done, bc-subagent-driven-development, bc-tdd and bc-writing-plans (item 024 wording), and the worktree-removal proof from `concepts/bc-using-git-worktrees/body/SKILL.md` § Cleanup.
- Modularity scan 2026-11-27 (candidate A, owner pick 1) that found the repetition.

## Tests

`tests/pressure-safe-runs.md` — reruns `concepts/bc-tdd/tests/pressure-storage-inline.md` and `concepts/bc-code-review/tests/pressure-storage-inline.md` against the module form, plus a fallback-only arm per scenario with the module hidden.

## Deploy targets

Not deployed yet: `deployed: no` keeps `scripts/deploy-local-skills.py` from linking it. Until it is deployed, callers' load instruction fails and their one-line fallback applies.
