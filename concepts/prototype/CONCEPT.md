# Concept: prototype

User-invoked throwaway exploration step for design uncertainty: build a small runnable artifact for logic/state or UI direction, record the answer, then delete or absorb it before production implementation.

## Design decisions

- **Question-first.** The artifact shape follows the question; otherwise prototypes become mini-features.
- **Feeds planning, not drain.** Prototype verdicts become PRD/ADR/issue context; prototype code should not become unattended execution scope unless explicitly absorbed.
- **No polish by design.** Tests and abstractions are intentionally omitted to preserve speed and throwaway semantics.

## Provenance

- `raw/ingested/pocock-engineering-extensions/` — upstream Matt Pocock `prototype/SKILL.md` captured 2026-06-21.
- `concepts/bc-plan-to-issues/` — optional pre-PRD evidence step when grilling exposes design uncertainty.

## Tests

`tests/scenario.md` — pressure scenario: chooses the right branch, marks artifacts throwaway, captures the verdict, and does not leave prototype code disguised as production. Scenario authored; full harness run pending.

## Deploy targets

- Claude Code: `~/.claude/skills/prototype` → relative symlink to `body/` (deployed 2026-06-21).
- Pi: `~/.agents/skills/prototype` and `~/.pi/agent/skills/prototype` → relative symlinks to `body/` (deployed 2026-06-21).
- Other harnesses: manual bootstrap until tested.
