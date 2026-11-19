---
test_kind: pressure
test_status: partial # 2026-11-19 open-report check + Decisions record: with 6/6 vs without 2/6 (control only), Terra low, n=2 (tests/pressure-retro-decisions.md); headless carry-over new 2/2 vs old 0/2 and overlay load path owner 2/2, stranger 2/2 (tests/pressure-private-overlay.md); no real file writes tested. Earlier 2026-11-19 live scheduled batch run wrote a valid n=20 report; usefulness awaits owner verdict
tested: 2026-11-19
deployed: yes
---
# Concept: retro

Owner-invoked retrospective over one Pi session or a batch of them. It reads targeted slices of the session logs, child-run transcripts, swarm manifests and a session time report when the machine has one, then proposes environment changes — checks, review standards, concept/kernel clauses, Scripts tools, owner-stated memory — ordered by severity, each with a named home and a recurrence count. It changes nothing until the owner picks. Adapted from Matt Pocock's `retro` skill (MIT).

## Design decisions

- **Reports carry their decisions.** A report is decided once it has `## Decisions` (one line per proposal: acted with commit/file, declined, deferred with trigger). Interactive runs show an undecided latest report first; headless batches carry its proposals over under `## Still undecided from <date>`, outside the sample. Why: weekly reports went unanswered with no record of what was acted on. Owner-approved 2026-11-19.

- **Owner-invoked only, as upstream.** Upstream sets `disable-model-invocation: true` and `allow_implicit_invocation: false`. Kept: a retro is costly, and the moment to run one is the owner's call. The model's part is the kernel's 👣 offer at the end of a substantial session (see `agent-kernel` § recap), not invoking the skill.
- **Adapted, not vendored.** Upstream assumes Claude Code's session store, a `CODING_STANDARDS.md` and a reviewer agent. Here the evidence is Pi's session JSONL, child-run transcripts, `bc-swarm` manifests and a session time-report tool if the machine has one (else JSONL timestamps), and the reviewer standards live in `code-review`.
- **Wall time and rework added as a category and listed first.** The owner's main loss is time: waits, sleep-polling, reruns, rate-limit stalls, subagent rework rounds (see the agent-time-sinks entries in `log.md`, 2026-11-19). Upstream's seven categories do not name it.
- **Batch mode.** Upstream reviews one session. The owner wants a weekly run over many sessions; batch scope (`since <date>`, `last M`, optional project) plus a report file (`--report`, else the report directory) serves it. The automation that schedules it is out of scope here.
- **Batch sampling with a denominator.** A trial all-project batch (2026-11-19) had no sampling rule, so its counts had no denominator, and the full time report overflowed tool output. The body samples by time, independent of project: the 18 parent sessions with the most active time (from a session time-report tool, or JSONL timestamps as fallback) plus 2 seeded random picks, 20 in all. An earlier rule ranked projects first; its second trial (2026-11-19) landed 8 of 10 samples in one project, and the owner chose project-independent time ranking so a single-project week still gets a full sample. Size 20 is for first runs; the owner may lower it.
- **Report path wins.** The same trial got a conflicting output destination from its caller and skipped the report. Batch mode now always writes the report, `--report` first, and names its path on the last line.
- **"Adopt only what recurs" made mechanical.** This workspace's Tune operation adopts only recurring failures. Batch mode counts sessions per finding; single-session mode labels one-offs.
- **Every proposal names a home.** Upstream's homes (AGENTS.md pointers, `CODING_STANDARDS.md`, checks, skills) mapped to the owner's: project check/CI/`./scripts/gate`, `code-review`, a concept or kernel clause in this workspace (which then needs a pressure test), a Scripts tool, or memory/preferences only when the owner said it.
- **`writing-for-agents` dropped.** Upstream's step 1 loads it. Here `prompting-agents` owns instruction wording, so the body points there.
- **Transcripts are data.** Not in upstream. Session logs hold tool output and fetched text; the body forbids saving instructions read from them into memory.

- **Owner specifics in a private overlay.** The body names no owner tool or path; one line tells the agent to read `~/.config/agent-concepts/overlays/retro.md` if it exists, which names the owner's session time-report tool and report directory. Why: the repository must work as-is for a stranger (`AGENTS.md` § Conventions), while the owner's agents keep their tool names. Owner decision 2026-11-19.
- **Report directory default `${XDG_STATE_HOME:-~/.local/state}/retro/`, overridable by `RETRO_REPORT_DIR`.** The open-report check needs one directory that every run reads and writes. A per-project `./retro/` would split one cross-project batch history across repositories and drop files into working trees; `${TMPDIR:-/tmp}` (the earlier default) is wiped, losing undecided reports, and disagreed with where the check read. The XDG state directory is per-user, persistent and outside any repository.
- **Two report-name forms.** Default batch reports are `YYYY-MM-DD-<scope>.md`; a scheduled job may pass a date-only `--report YYYY-MM-DD.md`, which external readers of that directory may rely on. The open-report check matches both by date prefix and excludes the run's own `--report` target, so a same-day rerun does not carry over its own report. The decided/proposals interface (`## Decisions` line; `1. ` items under `## Proposals`) is fixed, and the body now tells the writer to produce it.

## Provenance

- [`docs/research/raw/ingested/pocock-retro-upstream/`](../../docs/research/raw/ingested/pocock-retro-upstream/SOURCE.md) — MIT snapshot of `mattpocock/skills` at `5863806dd4e15c63174bee4e7515a4256792ecfa`: `retro/SKILL.md` (adapted), `agents/openai.yaml`, and `writing-for-agents` (evidence only).
- [AI Hero — /retro](https://www.aihero.dev/skills-retro) — author's usage write-up: proposes only, owner-invoked.
- [`docs/research/raw/pocock-pr-bottleneck-talk/`](../../docs/research/raw/pocock-pr-bottleneck-talk/SOURCE.md) — talk where `/retro` was announced (session, PR+session, or a week of PRs).
- `AGENTS.md` § Tune — "adopt only what recurs".
- `concepts/prompting-agents/body/SKILL.md` — wording of gates and Why lines.

## Tests

[`tests/pressure-retro-decisions.md`](tests/pressure-retro-decisions.md) — open-report check and Decisions record, old vs new body.

[`tests/pressure-private-overlay.md`](tests/pressure-private-overlay.md) — headless carry-over (old vs new body) and overlay load path (owner vs stranger).

[`tests/pressure-retro.md`](tests/pressure-retro.md) — without vs with the body on an anonymised session excerpt.

## Deploy

Deployed via `scripts/deploy-local-skills.py` to the shared bus (`~/.agents/skills/retro`, `~/.pi/agent/skills/retro`, `~/.claude/skills/retro`). Batch changes await a pressure re-test.
