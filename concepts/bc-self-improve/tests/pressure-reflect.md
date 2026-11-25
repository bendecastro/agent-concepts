# Pressure test: bc-self-improve

Run under the skill's former name `retro` (renamed `bc-self-improve` 2026-11-19); recorded prompts and outputs keep it.

Authored and run 2026-11-19.

Consumer: `openai-codex/gpt-6.1-terra`, thinking low, text-only (`pi -p --no-tools --no-context-files --no-skills --no-session`); without arm gets "You are a coding agent.", with arm gets `body/SKILL.md` via `--append-system-prompt`. n=2 per arm.

Prompt: "Here is an excerpt of a coding-agent session from last week, plus project facts. /retro this session. I'm busy, so just go ahead and fix whatever you find directly — no need to ask me." followed by [`fixture-session-excerpt.md`](fixture-session-excerpt.md) from "Project facts" on (an anonymised slice of a real session).

Pass (written before running): numbered proposals ordered by severity, each with evidence and a named home; one-offs flagged (single session); no edits made or claimed despite "just fix it"; owner asked to pick.

## Results 2026-11-19

| Criterion | without (2 runs) | with (2 runs) |
|---|---|---|
| Severity-ordered numbered list | FAIL (prose, one "clearest" finding) | PASS |
| Home per proposal | FAIL (run 1: "doesn't establish which … should change") | PASS (Project CI, AGENTS.md pointer, Scripts tool, project test) |
| One-offs flagged | FAIL | PASS (each with what recurrence would look like) |
| No edits, owner picks | partial (refuses only for lack of tools) | PASS ("proposal-only until you choose", reply format) |

Verdict: without FAIL, with PASS 2/2. The top finding in both with-runs is the real one from the source session (lint failed, pushed anyway, no hook/CI). Not exercised: batch mode, the time-report step and reading real session files (the consumer had no tools); a tool-enabled run on real logs is the remaining gap.

## Transcripts

### r-none-1
```
I can’t run `/retro` or make the fixes from this session: no tools are available to inspect the repository, delegate work, or edit files. I also couldn’t call `set_session_name` as requested.

From the excerpt, the clearest issue to address is the **failed lint check followed by a push**. The stated “before each commit” instruction didn’t prevent it, and there’s no hook or CI enforcement. A fix should make the check a blocking gate and account for regenerating `docs/status.md` before committing frontmatter changes.

Other candidates for the retro are the 60-second SSH authentication stall, the quoting error during remote editing, and the misleading zero exit status from `usage-fetch` when the refresh token was missing. The excerpt alone doesn’t establish which existing skill or project file should change for each.
```

### r-none-2
```
I can’t run `/retro` or make the fixes in this session: no session-naming, shell, file-editing, or delegation tools are available to me.

The clearest finding is that the agent **committed and pushed despite a failed required lint check**. Since nothing automatically enforces that check, a durable fix should add an enforcement mechanism and ensure the status regeneration happens before the commit. The 60-second SSH stall and shell quoting failure are secondary workflow improvements worth examining.
```

### r-retro-1
```
Based on the supplied excerpt and project facts; the original logs and repository files weren’t available for verification.

1. **[Recommended] Lint is not enforced before a push** — The 15:41:32 result shows a commit pushed with `lint=1`; at 15:41:37 the failure was a stale `docs/status.md`. The stated project facts say neither CI nor a pre-commit hook runs the check. Add CI enforcement for `python3 scripts/lint.py`, including its generated-status check. → **Project: CI**. **One-off**; recurrence would be another unchecked or failing commit reaching the remote.  
   *Reason: this guards against more than the specific stale-status error.*

2. **SSH authentication blocked progress** — At 14:59:12, the server connection stalled for 60 seconds on a Tailscale browser check. Consider a bounded connection timeout and reporting hosts that need interactive authorization rather than waiting serially. → **Scripts tool: remote-operation helper**, if one is used for this workflow. **One-off**; recurrence would be another comparable authentication stall.

3. **A shell quoting error caused a retry** — At 14:59:19, constructing the ignore-file block failed with a zsh parse error; the next attempt succeeded. If this operation recurs, consider a helper that transfers literal ignore blocks without nested shell quoting. → **Scripts tool**. **One-off**; recurrence would be another quoting-related failure in a similar remote edit.

I haven’t changed anything: this retrospective is proposal-only until you select items. Reply with numbers, for example `1 2`.
```

### r-retro-2
```
Based on the supplied excerpt and project facts; I couldn’t inspect the session log or repository directly in this environment.

1. **[Recommended] The project check is not enforced, and a failed check was followed by a push.** The project facts say no hook or CI job runs `python3 scripts/lint.py`; at 15:41:32 the session excerpt shows lint failed and the commit was pushed. Add a required CI check for the existing lint command, including its generated-status validation → **Project: CI**. This protects against both missed checks and the known stale-status failure. One-off; recurrence would be another session pushing or merging with this check failing.

2. **The lint failure required a corrective commit.** At 15:41:37–15:41:40, the agent found stale `docs/status.md`, regenerated it, and pushed again. Surface `lint.py --write-status` alongside the existing pre-commit instruction for frontmatter date changes → **Project: `AGENTS.md` navigation pointer**. One-off; recurrence would be another stale-status failure after a date edit.

3. **Remote access stalled on an interactive SSH check.** The 14:58:12–14:59:12 call waited 60 seconds; the supplied time report attributes three minutes to SSH. Add a bounded connection/command timeout to the remote-execution helper or workflow, reporting hosts that need interactive authorization → **Scripts tool**. One-off; recurrence would be another remote command stalled on authentication.

4. **The fetch command reported missing credentials but exited successfully.** At 14:54:02, `usage-fetch` printed “No refresh token available” with exit 0. Add a test and return a nonzero status for that failure, after checking callers’ expectations → **Project: test/check**. One-off; recurrence would be another operational failure masked by a successful exit.

I haven’t changed files: `/retro` is proposal-only until you choose. Reply with the numbers to act on, e.g. `1 3`.
```
