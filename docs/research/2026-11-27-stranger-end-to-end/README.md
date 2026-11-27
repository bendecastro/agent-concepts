# Pi stranger end-to-end test, 2026-11-27

**Result: setup and planning work for a stranger; the build stopped before claiming the item, so building and landing were not tested.** Two attempts ran with the [recipe](../../../scripts/stranger-end-to-end.md): the first attempt, then the one allowed retry for an infrastructure failure. Both installed commit `2caf238` of this repository from a local path, plus Pi 1.6.1 and `pi-subagents` 0.90.0, on `openai-codex/gpt-6.1-terra` at low thinking ([versions and Git state](evidence/git-state.txt)).

**Caveat: the planning and build sessions did not load the project's own instructions.** The test driver started every session with `-nc` (no `AGENTS.md` or `CLAUDE.md` files). That flag was only meant to keep out global instruction files, which the sandbox already replaced with empty files. As a result, planning and the build never saw the `AGENTS.md` and `.bc-agent/AGENTS.md` that setup had just written. In attempt 1, the setup and planning sessions had byte-identical system prompts. A stranger's Pi loads those files by default, and `.bc-agent/AGENTS.md` says "GitHub issues are optional… the folders are the source of truth". So stall 1 below may be caused by the test rather than the skill. The driver no longer passes `-nc`. Setup's grades and stalls 2 and 3 are not affected, because no project instruction files existed before setup ran.

The sandbox check passed in both attempts: no private configuration directory, no host home, no `bc-*` commands on `PATH`, and empty always-loaded instruction files. The system prompt of every session was checked against the owner's private list of personal terms: no matches.

## Grades

| What | Attempt 1 | Attempt 2 | Evidence |
| --- | --- | --- | --- |
| Setup writes project instructions, layout and a passing local check | Pass | Pass | Both committed the setup on `main`. The [generated check script](evidence/attempt1-setup-gate.sh) runs the README's test command; both existing tests passed. |
| Planning writes an item ready for an agent | Pass | Not reached | Attempt 1 wrote [`003-normalize-internal-whitespace`](evidence/attempt1-planned-item.md) with requirements, one step and `Ready for agent: yes`. In attempt 2 the agent asked a second question ("Is that test seam okay?"); the test driver of that run answered only one question, so no item was written. |
| A commit with the change lands on the bare remote's `main` | Fail | Fail | No pipeline child started. The bare remote holds only the fixture commit in both attempts. |
| Workers ran only targeted tests | Not observed | Not observed | No worker ran. |

## Stalls

| # | Where | Evidence | Disposition |
| --- | --- | --- | --- |
| 1 | Build, choosing what to build | Attempt 1 ran `gh issue list` against a project whose only remote is a local path, then stopped: "two work items are marked ready, but I couldn't check whether GitHub issues are also ready because `gh` is unauthenticated." `bc-pipeline-to-done` says "If only one source has ready units, use it. If both do, ask", but never says that a project without a GitHub remote has no issue source. | Unconfirmed (see the caveat): the session never saw the project's statement that issues are optional. Work item: first reproduce with project instructions loaded; then make the pipeline skip GitHub issues when the project has no GitHub remote. |
| 2 | Setup, wiki check | Attempt 1 tested only `$HOME/.agents/skills/bc-wiki-maintain/wiki_lint.py` and printed "wiki lint unavailable at installed skill path". `bc-setup-project` names that directory as the usual place; `pi install` puts the skills in the package's own directory, where the script was present. | Work item: setup finds `bc-wiki-maintain` where the harness actually installed it. |
| 3 | Setup, starter items | Right after setup, the work index printed "warning: 1-planned/002-architecture-review.md has no Planned: line", and the planning session reported it as a pre-existing warning. The starter item setup seeds fails the project's own index check. | Work item: seeded starter items pass the work-index check. |
| 4 | Test driver | Attempt 2's planning stopped after its second question because the driver answered only once. | Fixed here: `stranger_rpc_driver.py` gives the scripted answer first and a neutral go-ahead to up to two later questions; `scripts/tests/test_stranger_rpc_driver.py` covers it. |
| 5 | Test driver | Attempt 1's build reply was a request, not a question ("Please authenticate `gh`, or confirm…"), so the driver did not answer it. | Fixed before attempt 2: the build phase always gets one answer after it first stops. |
| 6 | Prompt capture | The `NODE_OPTIONS` request hook used in earlier pressure tests saved no prompts. Each session's RPC stream carries its system prompt, so the audit used that. | Fixed here: the script saves the system prompts from the RPC stream. Child sessions' prompts are not captured yet, because no child ran. |
| 7 | Worker preflight | The first preflight's log (kept private; the committed [corrected preflight](evidence/sandbox-preflight.txt) is the passing rerun): Pi could not open a mask file created on a `nodev` bind (`EACCES`), and `--no-refresh` was rejected before the `check` subcommand. | Fixed earlier in this change: masks are bound from `/dev/null` data, and the options follow the subcommand. |
| 8 | Coverage | Building and landing were never reached, and planning and the build ran without project instructions. | Fixed in the driver (no `-nc`). Work item: rerun the stranger test with the fixed driver; it also confirms or clears stall 1. |

## Rerun after the fixes (039-stranger-rerun)

**Result: a stranger got from an empty sample repository to a reviewed change on the remote's `main`, with no stall.** One run, no retry, installed commit `87782c9` (after 036 to 040 landed), same Pi, `pi-subagents` and model as above ([versions and Git state](evidence/rerun-git-state.txt)). Every session started through `scripts/pi_sandbox.py`, whose check passed: each session's system prompt held the project's `AGENTS.md`. The audit found no private term in the four saved system prompts.

| What | Result | Evidence |
| --- | --- | --- |
| Setup writes project instructions, layout and a passing local check | Pass | [setup reply](evidence/rerun-setup-reply.md); setup commit on `main` |
| Planning writes an item ready for an agent | Pass | [planning reply](evidence/rerun-plan-reply.md) |
| A commit with the change lands on the bare remote's `main` | Pass | `074e264 Normalize internal label whitespace` and the item-close commit are on the remote's `main`; [build reply](evidence/rerun-build-reply.md), [landed item](evidence/rerun-landed-item.md) |
| Workers ran only targeted tests | Pass | Both worker transcripts ran `python3 -m unittest discover -s tests -p 'test_labels.py'`; the full `scripts/gate` ran only in the driver (baseline and final gate) |
| Review | Pass | Spec and Standards reviewers both approved after one rework round |
| No GitHub source asked about (stall 1) | Pass | The build made no `gh` call and asked no source question |

Findings (no stall):

| # | Where | Evidence | Disposition |
| --- | --- | --- | --- |
| R1 | Build worker, property test | The worker wrote `.stignore` containing `.hypothesis/` into a project no sync tool watched. Source: `bc-tdd`'s `properties.md` said to list such caches "as Syncthing-ignored", and setup's generated `validation.md` repeated it. | Fixed here: both now say to add the cache to a sync tool's ignore list only when the project sits in a synced folder; `test_visible_layout.py` asserts the conditional wording. |
| R2 | Build, pre-review gate | The first worker handoff gave no targeted-test command or raw log path, so the driver sent it back once; the second handoff passed. | Cost one rework round; the gate did its job. No change. |
| R3 | Sandbox | A worker listed processes and saw the outer `bwrap` command line, which holds the host scratch path (under the owner's home). It is a path, not an instruction, and nothing acted on it. | Idea line in `work/0-ideas.md`: hide the outer command line (for example by starting the box from a scratch dir outside the home). |

Child session prompts were captured with the sessions (kept private).

The full session logs and system prompts stay private, outside the repository.

## npm package rerun (044), 2026-11-27

[npm-pack-rerun.md](npm-pack-rerun.md): installing the `npm pack` of the checkout plus `npm:pi-subagents` worked with no copied roles, but every session was refused with HTTP 429 (rate limit), so setup, plan and build were not graded. Rerun needed.
