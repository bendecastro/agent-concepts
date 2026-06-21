# Concept: improve-codebase-architecture

User-invoked architecture review for the bc loop. It scans for deep-module opportunities, presents visual before/after candidates in a temp HTML report, then grills one chosen candidate into durable planning context.

## Design decisions

- **Review before implementation.** The skill surfaces candidates and grills one; production changes should go through `bc-plan-to-issues` so they become vertical slices.
- **Visual report, not repo artifact.** The report goes to temp storage to avoid committing speculative architecture HTML.
- **Uses existing vocabulary.** Built on `codebase-design` and `domain-modeling`; this keeps architecture suggestions aligned with the user's deep-module language and repo glossary.
- **Bug-seam follow-up.** If `diagnosing-bugs` finds no correct regression seam, this is the structured next move.

## Provenance

- `raw/pocock-engineering-extensions/` — upstream Matt Pocock `improve-codebase-architecture/SKILL.md` captured 2026-06-21.
- `concepts/codebase-design/` — vocabulary and design principles.
- `concepts/grilling/` and `concepts/domain-modeling/` — used after the user chooses a candidate.

## Tests

`tests/scenario.md` — pressure scenario: writes only temp HTML, uses deep-module vocabulary, asks before exploring a candidate, and does not implement or create issues directly. Scenario authored; full harness run pending.

## Deploy targets

- Claude Code: `~/.claude/skills/improve-codebase-architecture` → relative symlink to `body/` (deployed 2026-06-21).
- Pi: `~/.agents/skills/improve-codebase-architecture` and `~/.pi/agent/skills/improve-codebase-architecture` → relative symlinks to `body/` (deployed 2026-06-21).
- Other harnesses: manual bootstrap until tested.
