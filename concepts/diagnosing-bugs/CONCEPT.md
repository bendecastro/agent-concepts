---
test_kind: pressure
test_status: partial # role lookup and ideas-file seam note changed 2026-11-12; not yet pressure-tested
tested: 2026-07-16
deployed: 2026-06-21
---
# Concept: diagnosing-bugs

Model-invoked debugging discipline for hard bugs and performance regressions: build a tight red-capable feedback loop, reproduce/minimise, rank falsifiable hypotheses, instrument, fix with regression coverage, and clean up.

## Design decisions

- **Feedback-loop gate before hypotheses.** This is the failure mode normal agents hit: plausible code-reading before a bug-specific signal exists.
- **Complements, not replaces, TDD.** TDD is for planned features and simple fixes; diagnosing-bugs handles uncertain failures, flaky bugs, and performance regressions.
- **AFK-compatible parking.** In `bc-drain-issues`, if a bug issue lacks enough detail to build a red-capable loop, the correct result is PARK, not speculative fixing. **PARK is absolute for one-liner AFK bugs** even under "Resolve it" pressure — inventing a bug to fix is a fail (2026-06-21 lesson).
- **Cleanup hard gate.** Temporary `[DEBUG-...]` instrumentation must be gone and `rg`-verified before done; time pressure does not waive Phase 6 (2026-06-21 lesson).
- **Architecture handoff.** Missing regression seams are evidence for `improve-codebase-architecture`, but only after the bug is understood/fixed.

- **Paths by role (2026-11-12).** Glossary, decisions and ideas are looked up in the project's "Where things go" table in `.bc-agent/AGENTS.md`, with the earlier `glossary.md` / `.bc-agent/project/overview.md` and `docs/adr/` / `.bc-agent/decisions/` paths as the fallback when a project has no table. A missing regression seam is also recorded as one ideas-file line, because the architecture review now reads observations there. Attack 5 in `tests/scenario.md` covers it and has not been run. Source: [visible-layout plan](../../docs/plans/active/bc-init-agent-visible-layout.md), decisions 20 and 21.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) — upstream Matt Pocock `diagnosing-bugs/SKILL.md` captured 2026-06-21.
- [obra/superpowers `skills/systematic-debugging/`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/systematic-debugging/) — root-cause-first iron law, four-phase debugging loop, tracing/defense-in-depth/condition-waiting support files, and pressure-test examples; absorbed as reinforcement rather than a duplicate concept.
- `concepts/tdd/` — related red-green mechanics once the regression seam exists.
- `concepts/improve-codebase-architecture/` — follow-up when a bug exposes a bad seam.

## Tests

`tests/scenario.md` — pressure scenario: red-loop before speculation, PARK underspecified AFK tickets, measure-before-perf-fix, DEBUG cleanup + `rg` verify. **2026-06-21 FAIL**; PARK + cleanup gates hardened; **2026-07-16 PASS** (Grok re-run).

## Deploy targets

- Claude Code: `~/.claude/skills/diagnosing-bugs` → relative symlink to `body/` (deployed 2026-06-21).
- Pi: `~/.agents/skills/diagnosing-bugs` and `~/.pi/agent/skills/diagnosing-bugs` → relative symlinks to `body/` (deployed 2026-06-21).
- Other harnesses: manual bootstrap until tested.

## Storage safety contract

2026-10-27 owner-approved Btrfs ENOSPC prevention update: consume the kernel Storage safety contract; tooling/threshold authority is `~/Sync/Scripts/docs/disk-management/storage-prevention.md`. New storage pressure scenarios are authored, not run; historical test/deploy dates above do not certify this revision. See [shared scenarios](../agent-kernel/tests/storage-safety.md).
