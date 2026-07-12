# Concept: code-review

Model-invoked review discipline for both sides of code review: independently assess a fixed diff for Spec fidelity and Standards quality, then request/receive feedback skeptically and constructively.

## Design decisions

- **Two independent axes.** Fixed-diff review separates Spec fidelity from Standards quality, using parallel read-only reviewers and separate reports so one pass cannot mask the other.
- **One concept, two moments.** Requesting and receiving review are separated sections in the body but share one discipline: reviewers supply evidence, implementers verify before changing code.
- **Technical over performative.** The body preserves the upstream ban on social over-agreement because it protects judgment: feedback is not accepted or rejected until checked against codebase reality.
- **Harness-neutral subagents.** The upstream assumes Claude Task; this port describes the review packet, read-only authority boundary, independent axes, and severity contract so Pi subagents, Claude Code, or another reviewer mechanism can be used.

## Provenance

- `raw/ingested/obra-superpowers/skills/requesting-code-review/SKILL.md` — review-request workflow and severity expectations.
- `raw/ingested/obra-superpowers/skills/requesting-code-review/code-reviewer.md` — reviewer prompt template adapted into the review packet/checklist.
- `raw/ingested/obra-superpowers/skills/receiving-code-review/SKILL.md` — feedback reception, YAGNI check, pushback rules, GitHub thread detail.
- Matt Pocock upstream `skills/engineering/code-review/SKILL.md` at `391a2701dd948f94f56a39f753f8eea9a859c87` — fixed-point review packet, independent Spec/Standards axes, and separate aggregation. https://github.com/mattpocock/skills/blob/391a2701dd948f94f56a39f753f8eea9a859c87/skills/engineering/code-review/SKILL.md

## Tests

`tests/scenario.md` — pressure scenarios for independent Spec/Standards review, fixed-point validation, blind implementation, performative agreement, unclear feedback, and reviewer overreach. Authored; harness pressure run pending.

## Deploy targets

Not deployed yet. Discipline-enforcing concept; deploy after pressure test.
