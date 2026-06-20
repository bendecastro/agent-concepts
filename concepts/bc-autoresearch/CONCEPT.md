# Concept: bc-autoresearch

Model-invoked discipline for objective, bounded code improvement: pick one reproducible metric, lock a correctness check, and iterate one bounded change at a time — keeping a change only when correctness still holds **and** the metric provably improved, reverting otherwise. Self-contained (works in any repo). The conditional optimization step the `bc-drain-issues` per-issue agent runs when a slice targets a measurable improvement. The `bc-` prefix is the user's personal namespace.

## Design decisions

- **Idea borrowed, rewritten — no dependency on the `bc-improve` script (user's instruction).** The principle comes from the user's `~/Sync/Scripts/bin/utils/bc-improve` + `AI/autoresearch-loop.md` ("the harness owns truth; the agent proposes bounded changes; a valid iteration proves correctness AND metric improvement"). But that CLI is Scripts-repo-specific (domains `images`/`playlists`, state under `AI/autoresearch/`). This skill **re-expresses the discipline self-contained** so it works in any repo and doesn't break if that script changes — it never shells out to `bc-improve`.
- **Both-gates-or-revert is the whole point.** A change survives only if correctness still passes *and* the metric beats the threshold; failing either reverts. Without the dual gate, an AFK agent "optimizing" is a regression generator. This is the discipline's load-bearing rule.
- **Don't optimize blind.** If no objective metric can be named, the skill stops rather than chasing "looks faster." This is what makes it safe to wire into an autonomous loop conditionally — no metric ⇒ it doesn't run.
- **One bounded change per iteration** so regressions are attributable and reverts are clean; **correctness before performance**; **no win-by-deleting-output**. These are the named failure modes from the source playbook, kept as guards.
- **Model-invoked discipline.** Like `tdd`, it's reachable by an orchestrator (the `bc-drain-issues` per-issue agent inlines it) and by the user mid-task. Not a user-only orchestrator.

## Provenance

- `~/Sync/Scripts/bin/utils/bc-improve` + `~/Sync/Scripts/AI/autoresearch-loop.md` + `~/Sync/Scripts/docs/utils/bc-improve.md` — the AutoResearch principle and its agent rules (one bounded change, correctness+metric, dry-run/shadow for expensive runtimes, record baseline/current/speedup). **Inspiration only — deliberately not a runtime dependency.**
- `concepts/tdd/` — sibling model-invoked discipline; same composition pattern (inlined by the executor).
- `concepts/prompting-agents/body/SKILL.md` — gate/guard phrasing.

## Tests

`tests/pressure-autoresearch.md` — attacks the gates: keep-without-measuring, a metric win that breaks a test (must revert — correctness first), a "win" by deleting required output (must reject), no objective metric available (must STOP, not optimize blind), bundled multi-change (must do one bounded change). Discipline-enforcing → must hold before deploy.

## Deploy targets

- Claude Code: `~/.claude/skills/bc-autoresearch` → relative symlink to `body/`. Deploy only after the pressure test holds.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../harnesses.md`.
