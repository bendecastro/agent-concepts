# Normalize internal whitespace in labels

Why: Labels with inconsistent internal spacing should normalize to the same value.
Done when: `normalize` collapses runs of Python whitespace to one ordinary space while preserving its existing trimming and lowercase behavior.
Stage: unscheduled
Blocked by: nothing
Kind: feature
Source: bc-plan-to-pipeline
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Requirements

### Problem and solution

Labels such as `"  Next   Up  "` currently retain inconsistent internal spacing. Normalize every run of Python whitespace between label content to a single ordinary space, in addition to trimming surrounding whitespace and lowercasing.

### User stories

1. As a caller, I want labels with different internal whitespace to normalize consistently, so equivalent labels have the same output.
2. As a caller, I want empty and whitespace-only labels to remain empty, and punctuation to remain unchanged, so existing behavior stays predictable.

### Implementation decisions

Keep the existing `normalize(label: str) -> str` public API and its lowercase semantics. Treat Python whitespace consistently, including spaces, tabs and newlines. Do not alter punctuation or introduce other normalization rules.

### Testing decisions

Test observable results through the existing public `normalize` function, using the existing unit-test suite. Cover mixed and repeated whitespace, surrounding whitespace, empty and whitespace-only input, punctuation, and existing lowercase behavior.

### Out of scope

API changes, punctuation changes, other normalization rules, and unrelated refactoring.

## Steps

- [x] **Normalize internal whitespace.** Blocked by: nothing. User stories: 1–2. Done when `"  Next   Up  "` becomes `"next up"`, internal runs of Python whitespace become one ordinary space, empty and whitespace-only inputs return `""`, punctuation is unchanged, and existing lowercase behavior is retained; public-function tests cover these cases and pass. Out of scope: API changes, punctuation changes, other normalization rules, and unrelated refactoring.

  - Review: approved by spec 2026-11-27
  - Review: approved by standards 2026-11-27
  - Gate: pass scripts/gate at 3d20efa 2026-11-27

## Outcome

Implemented in 074e264. The targeted unit and property tests passed, as did `scripts/gate` on the reviewed change.

Spent: 0m active, 0 tokens, cost unknown (estimated; pi no files, claude-code no files, codex no files; other tools not counted)
