# Stranger end-to-end rerun for 066-planning-go-ahead-is-not-build, 2026-11-28

**Result: pass.** Planning answered "Go ahead with the plan." with a ready work item and no code change, and the build session ran the pipeline roles (a builder and a reviewer) and landed the change with its test on the bare remote's `main`. This reruns the failed Haiku run in [the v0.5.0 stranger test](2026-11-28-stranger-end-to-end-0.5.0.md) with the go-ahead rule on master.

Graded by a second worker: the worker that ran the test hit a quota limit after the run finished and before grading. The run was not repeated; every row below is graded from its saved evidence (fixture, bare-remote log, RPC streams, session and subagent transcripts), not from the agents' replies.

## Run, 12:31–13:08 UTC

- Recipe: [stranger-end-to-end.md](../../scripts/stranger-end-to-end.md) with `STRANGER_SOURCE=pack` (the unpacked `npm pack` of master at `575466b`, `agent-concepts-0.5.0.tgz`), as releasing step 11.
- Consumer model: `anthropic/claude-haiku-5-5` at thinking `low`, the owner's choice for this item (the model the failure happened on), not a quota substitution.
- Pi 1.6.1, `pi-subagents` 0.90.0. `pi auth check`: `ready`; probe answered `OK`; isolation `isolation ok`.
- Audit: `grep -Ff <private list>` over the four saved system prompts exited 1 (clean). No HTTP 429 error in any phase.

| Check | Result | Evidence |
|---|---|---|
| Setup | pass | Commit `Set up agent workspace (code archetype)` pushed; fixture has `AGENTS.md`, `work/`, `docs/`, executable `scripts/gate` (`python3 -m unittest discover -s tests`), which the build session later ran green. |
| Planning | pass | One grill question, then the scripted answer ending "Go ahead with the plan." The session's only `write` was `work/1-planned/001-normalize-label-whitespace.md`; its commit `Plan label whitespace normalization as work item 001` (`git add work`) was pushed. No edit to code or tests. The item had `Ready for agent: yes`, Why/Done when, and one step with done-when and out of scope. The second scripted "Go ahead." got a push and "I did not start the build. The next step is `/bc-pipeline-to-done`". |
| Build lands on the bare remote's `main` | pass | Bare `main`: `Claim work item 001` → `Collapse internal whitespace in normalize` (`tinylabels/__init__.py`, `tests/test_labels.py`) → `Finish work item 001` (item in `work/3-done/2026-11/`, review and gate lines filled). |
| Pipeline roles ran | pass | Build session: one `subagent` call to `bc-drain-worker` (builder in a worktree) and one to `bc-drain-reviewer` (combined reviewer, read-only); the driver committed the reviewed diff, ran `scripts/gate` and pushed. |
| Workers ran targeted tests only | pass | The builder ran `python3 -m unittest tests.test_labels` (red, then green); the full check `discover -s tests` ran only in the driver. In this two-file fixture both cover the same file. |
| Stalls | one, resolved by the scripted answer | Build preflight stopped: "the three drain profiles ... exist in the package source but are not installed under `~/.pi/agent/agents/`". After the go-ahead it copied them there. `roles.md` says the package manifest makes them visible, so either discovery from a pack-source install fails or the driver misread it; filed as an idea. |

Compared with the earlier Haiku run: there planning wrote code and tests and filed the item straight into `work/3-done/`, and the build session ran 0 subagents. Here planning stopped at the ready item and the pipeline built it.

Notes, not failures: the empty-string and whitespace-only tests passed before the change, so the step's "seen failing" claim was overstated; the driver recorded this in the item's Outcome. The Outcome cites evidence files under the sandbox's `/tmp`, which do not survive the run.

Evidence (RPC streams, sessions, subagent transcripts, system prompts, fixture, logs) is private, outside the repository.
