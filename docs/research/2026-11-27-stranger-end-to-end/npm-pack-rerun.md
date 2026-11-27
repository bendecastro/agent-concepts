# Stranger rerun with the npm package (044), 2026-11-27

**Result: not graded. The install passed; setup, planning and the build never ran because every model call was refused with HTTP 429 (Anthropic account rate limit).** This is an infrastructure stop, not a skill result. The 044 step stays open.

- Consumer: anthropic/claude-haiku-5-5 low (owner choice 2026-11-27 for this release). It was also the stranger's model.
- Installed: commit `5137d11` packed with `npm pack` (`agent-concepts-0.3.0.tgz`), unpacked, and installed with `pi install <unpacked dir>`, which is what `pi install npm:agent-concepts` delivers. Then `pi install npm:pi-subagents` (0.90.0), as the README says. Pi 1.6.1. Run with `STRANGER_SOURCE=pack scripts/stranger_end_to_end.sh`.
- No copied roles: nothing was copied into the sandbox's agent directory. The skills, kernel and roles came from the package only.

## What the files show

| Phase | Evidence | Outcome |
|---|---|---|
| Isolation | `isolation.txt`: `isolation ok` | pass |
| Install | `install.log`: `Installed /box/src/package`, `Installed npm:pi-subagents`; `pi list` shows both packages | pass |
| Auth | `auth-check.txt`: `ready` | pass |
| Setup (16:51–16:52) | 16 turns end with `stopReason: error`, 429 `rate_limit_error`; the fixture has no `AGENTS.md`; `fixture-log.txt` holds only the fixture commit | not run |
| Plan (16:52–16:53) | same 429 errors; no work item | not run |
| Build (16:53–17:14) | 32 turns end with 429 errors; the bare remote's `main` is still the fixture commit | not run |

A model check outside the sandbox after the run also returned the same 429, so the one allowed infrastructure retry was not used: it would hit the same limit.

## Friction a stranger would hit

| # | Where | What happened | Status |
|---|---|---|---|
| N1 | Every phase | When the provider rate-limits, the session ends with an empty reply. `final.txt` is empty for all three phases; the 429 shows only in the RPC stream. A stranger sees nothing happen and no reason. | Pi behavior, not this repository's; recorded only. |
| N2 | Install | The packed tarball is named `agent-concepts-0.3.0.tgz`: `package.json` still says 0.3.0 although it now holds changes made after v0.3.0. The release step must raise the version before publishing. | For the release step. |

Rerun when the Anthropic limit has reset: `EVIDENCE=<new dir> MODEL=anthropic/claude-haiku-5-5 THINKING=low STRANGER_SOURCE=pack scripts/stranger_end_to_end.sh`.
