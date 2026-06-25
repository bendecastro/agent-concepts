# Concept: code-review

Model-invoked review discipline for both sides of code review: request focused technical review before work cascades, and receive review feedback skeptically but constructively.

## Design decisions

- **One concept, two moments.** Requesting and receiving review are separated sections in the body but share one discipline: reviewers supply evidence, implementers verify before changing code.
- **Technical over performative.** The body preserves the upstream ban on social over-agreement because it protects judgment: feedback is not accepted or rejected until checked against codebase reality.
- **Harness-neutral subagents.** The upstream assumes Claude Task; this port describes the review packet and severity contract so Pi subagents, Claude Code, or another reviewer mechanism can be used.

## Provenance

- `raw/obra-superpowers/skills/requesting-code-review/SKILL.md` — review-request workflow and severity expectations.
- `raw/obra-superpowers/skills/requesting-code-review/code-reviewer.md` — reviewer prompt template adapted into the review packet/checklist.
- `raw/obra-superpowers/skills/receiving-code-review/SKILL.md` — feedback reception, YAGNI check, pushback rules, GitHub thread detail.

## Tests

`tests/scenario.md` — pressure scenarios for blind implementation, performative agreement, unclear feedback, and reviewer overreach. Authored; harness pressure run pending.

## Deploy targets

Not deployed yet. Discipline-enforcing concept; deploy after pressure test.
