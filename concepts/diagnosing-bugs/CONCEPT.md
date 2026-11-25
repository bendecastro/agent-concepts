---
test_kind: pressure
test_status: partial # role lookup and ideas-file seam note changed 2026-11-12; not yet pressure-tested
tested: 2026-07-16
deployed: 2026-06-21
---
# Concept: diagnosing-bugs

Model-invoked debugging discipline for hard bugs and performance regressions: build a tight red-capable feedback loop, reproduce/minimise, rank falsifiable hypotheses, instrument, fix with regression coverage, and clean up.

## Design decisions

- **No links into other concepts (2026-11-25).** Installers copy each skill alone, so the body states inline the parts of the kernel's Storage safety rules it relies on and names `agent-kernel` as optional extra context instead of linking into its folder.

- **Feedback-loop gate before hypotheses.** This is the failure mode normal agents hit: plausible code-reading before a bug-specific signal exists.
- **Complements, not replaces, TDD.** TDD is for planned features and simple fixes; diagnosing-bugs handles uncertain failures, flaky bugs, and performance regressions.
- **AFK-compatible parking.** In `bc-pipeline-to-done`, if a bug issue lacks enough detail to build a red-capable loop, the correct result is PARK, not speculative fixing. **PARK is absolute for one-liner AFK bugs** even under "Resolve it" pressure — inventing a bug to fix is a fail (2026-06-21 lesson).
- **Cleanup hard gate.** Temporary `[DEBUG-...]` instrumentation must be gone and `rg`-verified before done; time pressure does not waive Phase 6 (2026-06-21 lesson).
- **Architecture handoff.** Missing regression seams are evidence for `improve-codebase-architecture`, but only after the bug is understood/fixed.

- **Paths by role (2026-11-12).** Glossary, decisions and ideas are looked up in the project's "Where things go" table in `.bc-agent/AGENTS.md`, with the earlier `glossary.md` / `.bc-agent/project/overview.md` and `docs/adr/` / `.bc-agent/decisions/` paths as the fallback when a project has no table. A missing regression seam is also recorded as one ideas-file line, because the architecture review now reads observations there. Attack 5 in `tests/scenario.md` covers it and has not been run. Source: [visible-layout plan](../../work/3-done/2026-11/018-bc-init-agent-visible-layout.md), decisions 20 and 21. The table and its role keys are the contract of `bc-init-agent` (see its `CONCEPT.md`, "Interface").

- **Storage incidents use the machine's health check (2026-11-19).** The Btrfs line names the machine's storage health check (or `btrfs filesystem usage`) instead of the owner's tool. Why: public repository; the owner's tool is named in the owner's always-loaded instructions, so no overlay is needed. The `df` warning and its Why are unchanged.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) — upstream Matt Pocock `diagnosing-bugs/SKILL.md` captured 2026-06-21.
- [obra/superpowers `skills/systematic-debugging/`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/systematic-debugging/) — root-cause-first iron law, four-phase debugging loop, tracing/defense-in-depth/condition-waiting support files, and pressure-test examples; absorbed as reinforcement rather than a duplicate concept.
- `concepts/tdd/` — related red-green mechanics once the regression seam exists.
- `concepts/improve-codebase-architecture/` — follow-up when a bug exposes a bad seam.

## Tests

2026-11-19 (generic storage-check wording): Terra low, text-only, with body, n=2, a stand-in machine instruction naming invented tools; non-regression only, no without-body arm. 2/2 ran the named storage check before `df`-free diagnosis and before the full suite (`/tmp/bc-swarm/2026-11-19-retro-skill/pt-diag/`). Both also prefixed a tool name absent from the body and prompt to the suite command; owner settings leaked into the consumer through the preferences file appended to the system prompt, so these were mixed rather than isolated stranger runs.

`tests/scenario.md` — pressure scenario: red-loop before speculation, PARK underspecified AFK tickets, measure-before-perf-fix, DEBUG cleanup + `rg` verify. **2026-06-21 FAIL**; PARK + cleanup gates hardened; **2026-07-16 PASS** (Grok re-run).

## Deploy targets

- Claude Code: `~/.claude/skills/diagnosing-bugs` → relative symlink to `body/` (deployed 2026-06-21).
- Pi: `~/.agents/skills/diagnosing-bugs` and `~/.pi/agent/skills/diagnosing-bugs` → relative symlinks to `body/` (deployed 2026-06-21).
- Other harnesses: manual bootstrap until tested.

## Storage safety contract

2026-10-27 owner-approved Btrfs ENOSPC prevention update: consume the kernel Storage safety contract; tooling/threshold authority is `<owner-scripts>/docs/disk-management/storage-prevention.md`. New storage pressure scenarios are authored, not run; historical test/deploy dates above do not certify this revision. See [shared scenarios](../agent-kernel/tests/storage-safety.md).
