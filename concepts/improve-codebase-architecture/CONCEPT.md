---
test_kind: pressure
test_status: partial
tested: 2026-06-21
deployed: 2026-06-21
---
# Concept: improve-codebase-architecture

User-invoked architecture review for the bc loop. It scans for deep-module opportunities, presents visual before/after candidates in a temp HTML report, then grills one chosen candidate into durable planning context.

## Design decisions

- **Review before implementation.** The skill surfaces candidates and grills one; production changes should go through `bc-plan-to-issues` so they become vertical slices.
- **Visual report, not repo artifact.** The report goes to temp storage to avoid committing speculative architecture HTML.
- **Thin artifact clause, not a `plain-language` load (2026-08-18).** The HTML is a document a busy owner scans to pick a candidate. The body names that reader, leads each card with problem + direction, keeps deep-module vocabulary (terms this reader already uses), and puts the ask last. Loading `plain-language` would invite "familiar words" to strip Module/Interface/Depth.
- **Uses existing vocabulary.** Built on `codebase-design` and `domain-modeling`; this keeps architecture suggestions aligned with the user's deep-module language and repo glossary.
- **Bug-seam follow-up.** If `diagnosing-bugs` finds no correct regression seam, this is the structured next move.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) — upstream Matt Pocock `improve-codebase-architecture/SKILL.md` captured 2026-06-21.
- `concepts/codebase-design/` — vocabulary and design principles.
- `concepts/grilling/` and `concepts/domain-modeling/` — used after the user chooses a candidate.
- `concepts/plain-language/body/SKILL.md` — reader-outcome source for the 2026-08-18 HTML artifact clause; the skill itself is not loaded.

## Tests

`tests/scenario.md` — pressure scenario: writes only temp HTML, uses deep-module vocabulary, asks before exploring a candidate, and does not implement or create issues directly. The 2026-08-18 artifact clause adds: each card leads with problem + direction, vocab stays, ask is last. Pressure-tested 2026-06-21 **PASS**; the new clause is expected behavior for the next run, not yet re-tested.

## Deploy targets

- Claude Code: `~/.claude/skills/improve-codebase-architecture` → relative symlink to `body/` (deployed 2026-06-21).
- Pi: `~/.agents/skills/improve-codebase-architecture` and `~/.pi/agent/skills/improve-codebase-architecture` → relative symlinks to `body/` (deployed 2026-06-21).
- Other harnesses: manual bootstrap until tested.
