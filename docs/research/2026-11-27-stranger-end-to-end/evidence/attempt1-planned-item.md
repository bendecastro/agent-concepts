# Normalize internal label whitespace

Why: Labels with inconsistent internal spacing should normalize to the same readable form.
Done when: `normalize` collapses internal Python whitespace while preserving its existing API and other behavior.
Stage: unscheduled
Blocked by: nothing
Kind: feature
Source: bc-plan-to-pipeline
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Requirements

### Problem and solution

Labels such as `  Next   Up  ` currently retain inconsistent internal spacing. Normalize each run of Python whitespace to one ordinary space, in addition to the existing surrounding-whitespace removal and lowercasing.

### User stories

1. As a caller, I want labels with different whitespace runs to normalize consistently, so equivalent labels have the same representation.
2. As a caller, I want empty and all-whitespace labels to remain empty, so blank input stays blank.
3. As a caller, I want punctuation and the public API unchanged, so existing usage remains compatible.

### Implementation and testing decisions

Keep the public `normalize(label: str) -> str` interface and lowercase behavior. Treat Python whitespace consistently, including spaces, tabs, newlines and Unicode whitespace; do not alter punctuation. Test externally observable behavior through the existing public function and unittest suite, including mixed whitespace, existing case and trimming behavior, empty and all-whitespace input, and punctuation.

### Out of scope

New APIs, punctuation normalization, other label transformations, and unrelated refactoring.

## Steps

- [ ] **Normalize internal label whitespace** — Blocked by: nothing. User stories: 1–3. Done when the public function returns `next up` for `  Next   Up  `, collapses mixed Python whitespace to ordinary spaces, preserves lowercasing and punctuation, returns an empty string for empty or all-whitespace input, and the existing and new behavioral tests pass. Out of scope: API changes, punctuation normalization, other label transformations, and unrelated refactoring.

## Outcome

_To be filled when finished or dropped._
