# Concept: code-review

Model-invoked review discipline for both sides of code review: independently assess a fixed diff for Spec fidelity and Standards quality, then request/receive feedback skeptically and constructively.

## Design decisions

- **Two independent axes.** Fixed-diff review separates Spec fidelity from Standards quality, using parallel read-only reviewers and separate reports so one pass cannot mask the other.
- **One concept, two moments.** Requesting and receiving review are separated sections in the body but share one discipline: reviewers supply evidence, implementers verify before changing code.
- **Technical over performative.** The body preserves the upstream ban on social over-agreement because it protects judgment: feedback is not accepted or rejected until checked against codebase reality.
- **Harness-neutral subagents.** The upstream assumes Claude Task; this port describes the review packet, read-only authority boundary, independent axes, and severity contract so Pi subagents, Claude Code, or another reviewer mechanism can be used.
- **Reviewer context isolation made explicit (2026-07-16).** From Bun's Zig→Rust rewrite: reviewers get the diff + spec + standards, never the implementer's reasoning or self-justification — the author's narrative biases toward acceptance, and this isolation (not adversarial framing) is the load-bearing mechanism of Bun's split-context review. Was implicit in the packet rules; now stated.
- **Assume-the-code-is-wrong stance considered and rejected (2026-07-16).** Bun told reviewers to assume the code is wrong and only hunt bugs. Rejected here because it directly conflicts with "Findings are not obligations": a reviewer prompted to find defects manufactures them, and in AFK runs nobody filters the padding — Bun had a human reading reviewer output; this workspace's bounded remediation cycle + severity gating extract the hunt-hard value without the spiral.

## Provenance

- `raw/ingested/obra-superpowers/skills/requesting-code-review/SKILL.md` — review-request workflow and severity expectations.
- `raw/ingested/obra-superpowers/skills/requesting-code-review/code-reviewer.md` — reviewer prompt template adapted into the review packet/checklist.
- `raw/ingested/obra-superpowers/skills/receiving-code-review/SKILL.md` — feedback reception, YAGNI check, pushback rules, GitHub thread detail.
- Matt Pocock upstream `skills/engineering/code-review/SKILL.md` at `391a2701dd948f94f56a39f753f8eea9a859c87` — fixed-point review packet, independent Spec/Standards axes, and separate aggregation. https://github.com/mattpocock/skills/blob/391a2701dd948f94f56a39f753f8eea9a859c87/skills/engineering/code-review/SKILL.md
- `raw/ingested/anthropic-claude-code-best-practices.md` — "Findings are not obligations": reviewer-incentive caution (a gap-hunting reviewer reports gaps even in sound work; chasing all findings over-engineers), bounding reviewers to correctness/stated requirements. Protects the AFK slice gate from remediation spirals. (ingested 2026-07-12)
- `raw/ingested/bun-in-rust-zig-port-writeup.md` — Bun's Zig→Rust rewrite (Jarred Sumner, 2026-07-08): split-context adversarial review at fleet scale; adopted the reviewer context-isolation rule, rejected the assume-wrong stance (see design decisions). (ingested 2026-07-16)

## Tests

`tests/scenario.md` — pressure scenarios for independent Spec/Standards review, fixed-point validation, blind implementation, performative agreement, unclear feedback, and reviewer overreach. Pressure-tested 2026-07-16 **PASS** (Grok).

## Deploy targets

Not deployed yet. Discipline-enforcing concept; deploy after pressure test.
