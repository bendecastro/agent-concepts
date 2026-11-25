---
test_kind: pressure
test_status: partial
tested: 2026-06-21
deployed: 2026-06-21
---
# Concept: bc-autoresearch-loop

Model-invoked discipline for objective, bounded code improvement: pick one reproducible metric, lock a correctness check, and iterate one bounded change at a time — keeping a change only when correctness still holds **and** the metric provably improved, reverting otherwise. Self-contained (works in any repo). The conditional optimization step the `bc-drain-issues` per-issue agent runs when a slice targets a measurable improvement. The `bc-` prefix is the user's personal namespace.

## Design decisions

- **Idea borrowed, rewritten — no dependency on the `<improve-script>` script (user's instruction).** The principle comes from the user's `<owner-scripts>/bin/utils/<improve-script>` + `AI/autoresearch-loop.md` ("the harness owns truth; the agent proposes bounded changes; a valid iteration proves correctness AND metric improvement"). But that CLI is Scripts-repo-specific (domains `images`/`playlists`, state under `AI/autoresearch/`). This skill **re-expresses the discipline self-contained** so it works in any repo and doesn't break if that script changes — it never shells out to `<improve-script>`.
- **Both-gates-or-revert is the whole point.** A change survives only if correctness still passes *and* the metric beats the threshold; failing either reverts. Without the dual gate, an AFK agent "optimizing" is a regression generator. This is the discipline's load-bearing rule.
- **Don't optimize blind.** If no objective metric can be named, the skill stops rather than chasing "looks faster." This is what makes it safe to wire into an autonomous loop conditionally — no metric ⇒ it doesn't run.
- **One bounded change per iteration** so regressions are attributable and reverts are clean; **correctness before performance**; **no win-by-deleting-output**. These are the named failure modes from the source playbook, kept as guards.
- **Measures like the guardrails (2026-11-25).** Baselining points to the `guardrails` skill's `measuring.md` for runs and noise, and a kept change tightens the matching limit on the project's guardrails page when it has one, so an improvement is locked in rather than lost to the next regression (item 006). Owner-chosen limits are left to the owner. Not pressure-tested.
- **Model-invoked discipline.** Like `tdd`, it's reachable by an orchestrator (the `bc-drain-issues` per-issue agent inlines it) and by the user mid-task. Not a user-only orchestrator.

## Provenance

- `<owner-scripts>/bin/utils/<improve-script>` + `<owner-scripts>/AI/autoresearch-loop.md` + `<owner-scripts>/docs/utils/<improve-script>.md` — the AutoResearch principle and its agent rules (one bounded change, correctness+metric, dry-run/shadow for expensive runtimes, record baseline/current/speedup). **Inspiration only — deliberately not a runtime dependency.**
- `concepts/tdd/` — sibling model-invoked discipline; same composition pattern (inlined by the executor).
- `concepts/prompting-agents/body/SKILL.md` — gate/guard phrasing.

## Tests

`tests/pressure-autoresearch-loop.md` — attacks the gates: keep-without-measuring, a metric win that breaks a test (must revert — correctness first), a "win" by deleting required output (must reject), no objective metric available (must STOP, not optimize blind), bundled multi-change (must do one bounded change). Discipline-enforcing → must hold before deploy. **Run 2026-06-21 in Pi: PASS** with artifact-verified revert/keep behavior and recorded metric/correctness checks.

## Deploy targets

- Claude Code: `~/.claude/skills/bc-autoresearch-loop` → relative symlink to `body/` (deployed 2026-06-21).
- Pi: `~/.agents/skills/bc-autoresearch-loop` and `~/.pi/agent/skills/bc-autoresearch-loop` → relative symlinks to `body/` (deployed 2026-06-21).
- Other harnesses: manual bootstrap until a real deploy is tested; record in `../../docs/guides/harnesses.md`.

## Storage safety contract

2026-10-27 owner-approved Btrfs ENOSPC prevention update: consume the kernel Storage safety contract; tooling/threshold authority is `<owner-scripts>/docs/disk-management/storage-prevention.md`. New storage pressure scenarios are authored, not run; historical test/deploy dates above do not certify this revision. See [shared scenarios](../agent-kernel/tests/storage-safety.md).
