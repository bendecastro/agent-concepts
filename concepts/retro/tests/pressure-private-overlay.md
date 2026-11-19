# Pressure test: headless carry-over and private overlay (2026-11-19)

The body names no owner tool or path; the owner's session time-report tool and report directory live in the optional private overlay `~/.config/agent-concepts/overlays/retro.md`. Consumer model: `openai-codex/gpt-6.1-terra`, thinking low, n=2 per arm. Raw outputs: run dirs `pt-d/` and `pt-overlay/`.

## (d) Headless batch with an undecided latest report

Consumer: `pi -p --no-session --no-context-files --no-skills --no-tools --model openai-codex/gpt-6.1-terra --thinking low --append-system-prompt <arm>`. Prompt opens "You cannot run tools in this reply.", embeds the undecided 2026-11-19 report (2 proposals, no `## Decisions`) as the latest report in `~/.local/state/retro/`, says no owner is present, and gives `/skill:retro since 2026-11-19 --report ~/.local/state/retro/2026-11-26.md`; asks what it does first and how the report starts.

Pass (written before running): does not ask for picks; plans the report to open with `## Still undecided from 2026-11-19`, the old report's path, and its proposals verbatim.

| Arm | Result |
|---|---|
| old (body before the open-report check) | 0/2 — both start with the new sample and title; no carry-over section ("compare the prior report's findings against new evidence") |
| pre-split (open-report check, owner paths) | 2/2 |
| new (this body) | 2/2 — "I would not ask for picks in this headless run"; `## Still undecided from 2026-11-19`, path, both proposals verbatim; both also excluded the `--report` target from "latest" |

## Overlay load path (tools enabled)

Consumer: `pi -p --no-session --no-context-files --no-skills --tools read --model openai-codex/gpt-6.1-terra --thinking low --append-system-prompt body/SKILL.md --mode json`. Prompt: owner types `/retro since 2026-11-19`; follow the skill including files it says to read; name (1) the report directory checked, (2) how sessions are ranked by active time, (3) where the report goes; invent no tools. STRANGER arm: overlay file moved aside for the run, then restored.

Pass: OWNER reads the overlay through the read tool and names the owner's report directory and the overlay's `--sessions --since` invocation. STRANGER names no owner tool or path, uses `$RETRO_REPORT_DIR` / `${XDG_STATE_HOME:-~/.local/state}/retro/` and the JSONL-timestamp fallback.

Result: **OWNER 2/2, STRANGER 2/2.** All four called `read` on the overlay path first. Owner runs named "`[owner report dir]`" and "`[owner time tool] --sessions --since 2026-11-19`" with the JSONL fallback for missing files. Stranger runs: "No session time-report tool has been identified … use a short Python script to sum intervals … excluding gaps over 600 seconds"; "The optional retro overlay was absent."

Not exercised: real file writes and a tools-enabled batch over real logs; Claude Code load path.
