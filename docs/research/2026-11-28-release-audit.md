# Release audit since v0.4.1 (2026-11-28)

Sorts each discipline concept's body changes since v0.4.1 into rule changes and wording changes, per [releasing.md](../guides/releasing.md) step 2. `git diff --name-only v0.4.1..HEAD -- 'concepts/*/body/*'` touches 23 concepts in nine commits, all dated 2026-11-28: `fec697b` (050 setup migrations), `8abc1c2` (scaffold version stamp), `f7159d8` (rule-owner search), `0ca52dd` and `2c7cecb` (054 `bc-safe-runs`), `05fe817` and `9e252f2` (053 step 1 split and fan-out width), `d47503a` and `3cc98a4` (053 step 2 durable-subagents loads and reboot-safe run folders). Work items 049, 051 and 052 changed no body. Every test named below was checked against commit times (`git log --format=%ci`): each is recorded in the change commit itself or in a later commit.

## Rule changes and the test that covers them

| Rule | Concepts | Covered by |
|---|---|---|
| Storage-safe run rules move into the new `bc-safe-runs` module; callers load it, with a one-line inline fallback (guarded runner, no custom `--basetemp`, `mktemp -d` outside `/tmp`, targeted tests, storage check before full suites/worktrees/fan-out) | bc-safe-runs, bc-code-review, bc-diagnosing-bugs, bc-dispatching-parallel-agents, bc-executing-plans, bc-finishing-development-branch, bc-optimize-code, bc-pipeline-to-done, bc-subagent-driven-development, bc-tdd, bc-using-git-worktrees, bc-writing-plans, bc-durable-subagents (`0ca52dd` 04:13) | [safe-runs pressure](../../concepts/bc-safe-runs/tests/pressure-safe-runs.md): bc-tdd and bc-code-review scenarios PASS 5/5 with the module, fallback-only arms 4/5 each (results recorded in `0ca52dd`) |
| The same rules newly apply to skills that ran code without them; `bc-council-find-bugs` passes `bc-safe-runs` to its repro worker | bc-find-bugs, bc-prototype, bc-council-find-bugs (`0ca52dd`) | Rule repeated: same safe-runs test; the launch-list part by its builder regression (launch lists `bc-safe-runs`, PASS) |
| Fallback states "stop if critical or unknown, or if the check cannot run"; packet line keeps the uv/venv selected interpreter; pipeline builder launch lists `bc-safe-runs` | all fallback holders above, bc-safe-runs, bc-pipeline-to-done (`2c7cecb` 04:22) | Safe-runs review regressions (recorded `69d1092`, 04:41): fallback health block PASS 3/3 (critical, unknown, broken check), builder with module and packet-line-only PASS |
| Worktree removal: `git cherry` empty output is not proof without ancestry; record tip, landed `HEAD` and proof before removal | bc-safe-runs (`0ca52dd`, `2c7cecb`) | Safe-runs cleanup regression PASS 2/2. Its caveat: the unknown-tip run does not isolate the empty-output clause; that clause is a one-line stop with no judgment, so a read check covers it |
| Recovery before relaunch, manifest before dispatch and child packet bullets now live in `bc-durable-subagents`; any skill that launches subagents loads it | bc-durable-subagents, bc-swarm (`05fe817` 04:36) | [post-split pressure](../../concepts/bc-durable-subagents/tests/pressure-split-2026-11-28.md): with PASS 4/4, without FAIL 4/4 (recorded `05fe817`/`1d3bbfe` 04:45) |
| Fan-out width: one child for a bounded fact or one or two named files, two to four for multi-surface recon; never add an unnamed track to reach a count | bc-swarm (`05fe817`, tightened `9e252f2` 04:48) | [fan-out width](../../concepts/bc-swarm/tests/pressure-fan-out-width.md) run 2 against the tightened wording (recorded `8b9e6d1`, 05:32): narrow PASS 3/3, multi-surface PASS 1/1. Run 1 on the first wording failed the narrow case, which is why it was tightened |
| Launching skills load `bc-durable-subagents` before the first launch; fallback: run folder + `manifest.md` stated in chat; council outputs go to distinct paths in the run folder | bc-council-mode, bc-dispatching-parallel-agents, bc-subagent-driven-development, bc-pipeline-to-done (`d47503a` 05:37); bc-security-audit, bc-work-sync (`3cc98a4` 05:46) | [council dry run](../../concepts/bc-council-mode/tests/dry-run-durable-subagents-2026-11-28.md), criteria 1–4 (first run in `d47503a`); the other five are the same rule repeated and use this test |
| Run folders must survive a reboot (not `/tmp`, not a bare `mktemp -d`) | bc-durable-subagents, bc-council-mode, bc-dispatching-parallel-agents, bc-subagent-driven-development, bc-pipeline-to-done, bc-security-audit, bc-work-sync; bc-safe-runs scratch rule excludes run folders (`3cc98a4` 05:46) | Council dry run review rerun PASS 5/5, criterion 5 (recorded in `3cc98a4`); [swarm-mode pointer check](../../concepts/bc-durable-subagents/tests/swarm-mode-pointer-2026-11-28.md) PASS 2/2, plans under `${XDG_STATE_HOME:-$HOME/.local/state}/bc-swarm/` (recorded `abbcdf1`, 05:50) |
| Pipeline: where `bc-durable-subagents` and the drain differ, the drain's resume and landing rules win | bc-pipeline-to-done (`3cc98a4`) | Read check: a precedence clause that keeps the drain's existing rules in force; it adds no stop |
| Before writing a rule, search concept bodies for its owner; load it, mark a `copy-of`, or split a module | bc-prompting-agents (`f7159d8`) | None — see Gaps |

## Wording changes only

- bc-setup-project: `MIGRATIONS.md` moved into `body/` and linked from the skill; scaffold notes print its absolute path (`fec697b`). Fresh scaffolds write `.bc-agent/.scaffold-version`, and `MIGRATIONS.md` gains "Arrived in" lines plus a section on reading the stamp (`8abc1c2`). The stamp is script output, checked by the gate. `MIGRATIONS.md` describes itself as a human-facing reference, not agent instructions, so it adds no stop.
- bc-handoff: `bc-delegate-investigation` renamed to `bc-durable-subagents` in one table row (`d47503a`).
- bc-durable-subagents / bc-swarm split text (`05fe817`): the inversion, routing decision, boundary and test-levels packet bullets moved unchanged from `bc-delegate-investigation` into `bc-swarm`; `pi.md` and the example JSON were renamed. (The new rules in the same commit are in the table.)
- Kept lines in the 054 callers (`0ca52dd`): text that was in the old inline blocks, now its own line (for example bc-diagnosing-bugs "For Btrfs storage incidents use the machine's storage health check ... not `df`", which v0.4.1 already had).
- bc-council-mode `pass-contracts.md` output-path wording matches the SKILL.md change in the table (`d47503a`).

## Gaps

None open. The bc-prompting-agents rule-owner search sentence (`f7159d8`) was accuracy-checked by the integrating session on 2026-11-28 against `scripts/lint.py` and `docs/guides/modularity-scan-brief.md` ([accuracy check](../../concepts/bc-prompting-agents/tests/accuracy-check.md)); it is a reference concept, so that is the check the test rule asks for.

No other rule change lacks a test or read check recorded after it.

## Residual notes (not gaps)

- The one-line fallback is weaker than the module: the fallback-only arms scored 4/5 in both scenarios (bc-tdd ran raw pytest inside a scratch copy; bc-code-review reran a full suite that `CHECKS.md` had recorded). Every install pack that ships a caller also ships `bc-safe-runs` ([install-packs](../guides/install-packs.md)), so the module form is the one users get. bc-code-review and bc-tdd mark this as `partial`.
- The council and swarm-mode tests are dry runs with no baseline arm. The packets did not exercise the literal `~/.pi/agent/skills/...` path of the swarm-mode pointer (the sandbox masks it).
- Tests recorded in the change's own commit (safe-runs module arms in `0ca52dd`, council criterion 5 in `3cc98a4`) count as run after the change, following the v0.3.0 audit's treatment of bc-code-review.

## Soak on `next` (releasing step 11)

2026-11-28: [stranger end-to-end test of v0.5.0](2026-11-28-stranger-end-to-end-0.5.0.md) is **inconclusive**: both allowed attempts on `anthropic/claude-haiku-5-5` low were refused by the provider (HTTP 429) on every call, so no phase ran. v0.5.0 stays on `next`; not promoted.

2026-11-28 rerun (09:22 UTC, with the operator's account-pooling extension, no 429): **fail**. Setup passed, but the planning session built, committed and filed the change as done instead of leaving a ready item, and the build session pushed it without running any pipeline role. v0.5.0 stays on `next`; not promoted.
