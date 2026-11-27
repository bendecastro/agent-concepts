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

The full session logs and system prompts stay private, outside the repository.
