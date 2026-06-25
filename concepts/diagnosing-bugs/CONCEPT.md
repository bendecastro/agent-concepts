# Concept: diagnosing-bugs

Model-invoked debugging discipline for hard bugs and performance regressions: build a tight red-capable feedback loop, reproduce/minimise, rank falsifiable hypotheses, instrument, fix with regression coverage, and clean up.

## Design decisions

- **Feedback-loop gate before hypotheses.** This is the failure mode normal agents hit: plausible code-reading before a bug-specific signal exists.
- **Complements, not replaces, TDD.** TDD is for planned features and simple fixes; diagnosing-bugs handles uncertain failures, flaky bugs, and performance regressions.
- **AFK-compatible parking.** In `bc-drain-issues`, if a bug issue lacks enough detail to build a red-capable loop, the correct result is PARK, not speculative fixing.
- **Architecture handoff.** Missing regression seams are evidence for `improve-codebase-architecture`, but only after the bug is understood/fixed.

## Provenance

- `raw/pocock-engineering-extensions/` — upstream Matt Pocock `diagnosing-bugs/SKILL.md` captured 2026-06-21.
- `raw/obra-superpowers/skills/systematic-debugging/` — root-cause-first iron law, four-phase debugging loop, tracing/defense-in-depth/condition-waiting support files, and pressure-test examples; absorbed as reinforcement rather than a duplicate concept.
- `concepts/tdd/` — related red-green mechanics once the regression seam exists.
- `concepts/improve-codebase-architecture/` — follow-up when a bug exposes a bad seam.

## Tests

`tests/scenario.md` — pressure scenario: refuses to hypothesize before a red-capable loop, parks an underspecified AFK bug, cleans debug logs, and recommends architecture review only after evidence. Scenario authored; full harness run pending.

## Deploy targets

- Claude Code: `~/.claude/skills/diagnosing-bugs` → relative symlink to `body/` (deployed 2026-06-21).
- Pi: `~/.agents/skills/diagnosing-bugs` and `~/.pi/agent/skills/diagnosing-bugs` → relative symlinks to `body/` (deployed 2026-06-21).
- Other harnesses: manual bootstrap until tested.
