# Concept: code-review

Model-invoked review discipline for both sides of code review: independently assess a fixed diff for Spec fidelity and Standards quality, then request/receive feedback skeptically and constructively.

## Design decisions

- **Two independent axes.** Fixed-diff review separates Spec fidelity from Standards quality, using parallel read-only reviewers and separate reports so one pass cannot mask the other.
- **One concept, two moments.** Requesting and receiving review are separated sections in the body but share one discipline: reviewers supply evidence, implementers verify before changing code.
- **Technical over performative.** The body preserves the upstream ban on social over-agreement because it protects judgment: feedback is not accepted or rejected until checked against codebase reality.
- **Harness-neutral subagents.** The upstream assumes Claude Task; this port describes the review packet, read-only authority boundary, independent axes, and severity contract so Pi subagents, Claude Code, or another reviewer mechanism can be used.
- **Reviewer context isolation made explicit (2026-07-16).** From Bun's Zig→Rust rewrite: reviewers get the diff + spec + standards, never the implementer's reasoning or self-justification — the author's narrative biases toward acceptance, and this isolation (not adversarial framing) is the load-bearing mechanism of Bun's split-context review. Was implicit in the packet rules; now stated.
- **Inert-guard verification is a named review class (2026-07-27).** Field evidence from a real drain: a guard whose two sides both resolve to the same production value reads as protection, passes review by inspection, and stays green forever because only a test double can supply a differing pair. It defeats every signal a reviewer normally trusts, so it needs naming rather than leaving it to general diligence. Deliberately paired with *Findings are not obligations* in the body, because the two could otherwise be read as contradictory: this block does not ask for defensive code against impossible states — it says do not credit protection that cannot fire, and the fix is usually accurate labelling or deletion. Also names the two near-miss fixes observed (deleting one inert clause while a sibling stays tautological; substituting a cosmetically independent expression with an identical runtime value).
- **Assume-the-code-is-wrong stance considered and rejected (2026-07-16).** Bun told reviewers to assume the code is wrong and only hunt bugs. Rejected here because it directly conflicts with "Findings are not obligations": a reviewer prompted to find defects manufactures them, and in AFK runs nobody filters the padding — Bun had a human reading reviewer output; this workspace's bounded remediation cycle + severity gating extract the hunt-hard value without the spiral.

## Provenance

- `raw/ingested/obra-superpowers/skills/requesting-code-review/SKILL.md` — review-request workflow and severity expectations.
- `raw/ingested/obra-superpowers/skills/requesting-code-review/code-reviewer.md` — reviewer prompt template adapted into the review packet/checklist.
- `raw/ingested/obra-superpowers/skills/receiving-code-review/SKILL.md` — feedback reception, YAGNI check, pushback rules, GitHub thread detail.
- Matt Pocock upstream `skills/engineering/code-review/SKILL.md` at `391a2701dd948f94f56a39f753f8eea9a859c87` — fixed-point review packet, independent Spec/Standards axes, and separate aggregation. https://github.com/mattpocock/skills/blob/391a2701dd948f94f56a39f753f8eea9a859c87/skills/engineering/code-review/SKILL.md
- `raw/ingested/anthropic-claude-code-best-practices.md` — "Findings are not obligations": reviewer-incentive caution (a gap-hunting reviewer reports gaps even in sound work; chasing all findings over-engineers), bounding reviewers to correctness/stated requirements. Protects the AFK slice gate from remediation spirals. (ingested 2026-07-12)
- Field observation, `bendecastro/image-maze` issue #203, landed `f4a1e02` (2026-07-27) — a `/bc-drain-issues` run whose Spec reviewer proved that the clause surviving the original inert-guard fix was *itself* a production tautology, and that the first implementation had disguised it by swapping an identical-valued expression. Source of the "Verify a guard can actually fire" block. (field evidence, no `raw/` file)
- `raw/ingested/bun-in-rust-zig-port-writeup.md` — Bun's Zig→Rust rewrite (Jarred Sumner, 2026-07-08): split-context adversarial review at fleet scale; adopted the reviewer context-isolation rule, rejected the assume-wrong stance (see design decisions). (ingested 2026-07-16)

## Tests

`tests/scenario.md` — pressure scenarios for independent Spec/Standards review, fixed-point validation, blind implementation, performative agreement, unclear feedback, and reviewer overreach. Checks 1–6 pressure-tested 2026-07-16 **PASS** (Grok).

Check 7 (inert guard caught; cosmetic and partial fixes rejected) was authored 2026-07-27 and is **not yet run** — the block is in the body and therefore live for any consumer, but its pressure test is outstanding. Field-observed once (image-maze #203, where a real reviewer did catch it unprompted, and a worker did produce both near-miss fixes), which motivated the block but is not a substitute for the gate.

## Deploy targets

Not deployed yet. Discipline-enforcing concept; deploy after pressure test.
