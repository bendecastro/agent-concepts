---
test_kind: pressure
test_status: partial # 2026-11-19 open-report check + Decisions record: with 6/6 vs without 2/6 (control only), Terra low, n=2 (tests/pressure-retro-decisions.md); batch carry-over untested. Earlier 2026-11-19 live batch run on beelink wrote a valid n=20 report; usefulness awaits owner verdict
tested: 2026-11-19
deployed: yes
---
# Concept: retro

Owner-invoked retrospective over one Pi session or a batch of them. It reads targeted slices of the session logs, child-run transcripts, swarm manifests and the time report, then proposes environment changes — checks, review standards, concept/kernel clauses, Scripts tools, owner-stated memory — ordered by severity, each with a named home and a recurrence count. It changes nothing until the owner picks. Adapted from Matt Pocock's `retro` skill (MIT).

## Design decisions

- **Reports carry their decisions.** A report is decided once it has `## Decisions` (one line per proposal: acted with commit/file, declined, deferred with trigger). Interactive runs show an undecided latest report first; headless batches carry its proposals over under `## Still undecided from <date>`, outside the sample. Why: weekly reports went unanswered with no record of what was acted on. Owner-approved 2026-11-19.

- **Owner-invoked only, as upstream.** Upstream sets `disable-model-invocation: true` and `allow_implicit_invocation: false`. Kept: a retro is costly, and the moment to run one is the owner's call. The model's part is the kernel's 👣 offer at the end of a substantial session (see `agent-kernel` § recap), not invoking the skill.
- **Adapted, not vendored.** Upstream assumes Claude Code's session store, a `CODING_STANDARDS.md` and a reviewer agent. Here the evidence is Pi's session JSONL, `subagent-artifacts/`, `bc-swarm` manifests and `bc-agent-time-report`, and the reviewer standards live in `code-review`.
- **Wall time and rework added as a category and listed first.** The owner's main loss is time: waits, sleep-polling, reruns, rate-limit stalls, subagent rework rounds (see the agent-time-sinks entries in `log.md`, 2026-11-19). Upstream's seven categories do not name it.
- **Batch mode.** Upstream reviews one session. The owner wants a weekly run over many sessions; batch scope (`since <date>`, `last M`, optional project) plus a report file (`--report`, `RETRO_REPORT_DIR`, then `${TMPDIR:-/tmp}/retro/`) serves it. The automation that schedules it is out of scope here.
- **Batch sampling with a denominator.** A trial all-project batch (2026-11-19) had no sampling rule, so its counts had no denominator, and the full time report overflowed tool output. The body samples by time, independent of project: the 18 parent sessions with the most active time (`bc-agent-time-report --sessions`, or JSONL timestamps as fallback) plus 2 seeded random picks, 20 in all. An earlier rule ranked projects first; its second trial (2026-11-19) landed 8 of 10 samples in one project, and the owner chose project-independent time ranking so a single-project week still gets a full sample. Size 20 is for first runs; the owner may lower it.
- **Report path wins.** The same trial got a conflicting output destination from its caller and skipped the report. Batch mode now always writes the report, `--report` first, and names its path on the last line.
- **"Adopt only what recurs" made mechanical.** This workspace's Tune operation adopts only recurring failures. Batch mode counts sessions per finding; single-session mode labels one-offs.
- **Every proposal names a home.** Upstream's homes (AGENTS.md pointers, `CODING_STANDARDS.md`, checks, skills) mapped to the owner's: project check/CI/`./scripts/gate`, `code-review`, a concept or kernel clause in this workspace (which then needs a pressure test), a Scripts tool, or memory/preferences only when the owner said it.
- **`writing-for-agents` dropped.** Upstream's step 1 loads it. Here `prompting-agents` owns instruction wording, so the body points there.
- **Transcripts are data.** Not in upstream. Session logs hold tool output and fetched text; the body forbids saving instructions read from them into memory.

## Provenance

- [`docs/research/raw/ingested/pocock-retro-upstream/`](../../docs/research/raw/ingested/pocock-retro-upstream/SOURCE.md) — MIT snapshot of `mattpocock/skills` at `5863806dd4e15c63174bee4e7515a4256792ecfa`: `retro/SKILL.md` (adapted), `agents/openai.yaml`, and `writing-for-agents` (evidence only).
- [AI Hero — /retro](https://www.aihero.dev/skills-retro) — author's usage write-up: proposes only, owner-invoked.
- [`docs/research/raw/pocock-pr-bottleneck-talk/`](../../docs/research/raw/pocock-pr-bottleneck-talk/SOURCE.md) — talk where `/retro` was announced (session, PR+session, or a week of PRs).
- `AGENTS.md` § Tune — "adopt only what recurs".
- `concepts/prompting-agents/body/SKILL.md` — wording of gates and Why lines.

## Tests

[`tests/pressure-retro-decisions.md`](tests/pressure-retro-decisions.md) — open-report check and Decisions record, old vs new body.

[`tests/pressure-retro.md`](tests/pressure-retro.md) — without vs with the body on an anonymised session excerpt.

## Deploy

Deployed via `scripts/deploy-local-skills.py` to the shared bus (`~/.agents/skills/retro`, `~/.pi/agent/skills/retro`, `~/.claude/skills/retro`). Batch changes await a pressure re-test.
