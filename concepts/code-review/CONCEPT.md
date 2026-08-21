---
test_kind: pressure
test_status: pass
tested: 2026-08-21
deployed: yes
---
# Concept: code-review

Model-invoked review discipline for both sides of code review: independently assess a fixed diff for Spec fidelity and Standards quality, then request/receive feedback skeptically and constructively.

## Design decisions

- **Two independent axes.** Fixed-diff review separates Spec fidelity from Standards quality, using parallel read-only reviewers and separate reports so one pass cannot mask the other.
- **One concept, two moments.** Requesting and receiving review are separated sections in the body but share one discipline: reviewers supply evidence, implementers verify before changing code.
- **Technical over performative.** The body preserves the upstream ban on social over-agreement because it protects judgment: feedback is not accepted or rejected until checked against codebase reality.
- **Harness-neutral subagents.** The upstream assumes Claude Task; this port describes the review packet, read-only authority boundary, independent axes, and severity contract so Pi subagents, Claude Code, or another reviewer mechanism can be used.
- **Reviewer context isolation made explicit (2026-07-16).** From Bun's Zig→Rust rewrite: reviewers get the diff + spec + standards, never the implementer's reasoning or self-justification — the author's narrative biases toward acceptance, and this isolation (not adversarial framing) is the load-bearing mechanism of Bun's split-context review. Was implicit in the packet rules; now stated.
- **Inert-guard verification is a named review class (2026-07-27).** Field evidence from a real drain: a guard whose two sides both resolve to the same production value reads as protection, passes review by inspection, and stays green forever because only a test double can supply a differing pair. It defeats every signal a reviewer normally trusts, so it needs naming rather than leaving it to general diligence. Deliberately paired with *Findings are not obligations* in the body, because the two could otherwise be read as contradictory: this block does not ask for defensive code against impossible states — it says do not credit protection that cannot fire, and the fix is usually accurate labelling or deletion. Also names the two near-miss fixes observed (deleting one inert clause while a sibling stays tautological; substituting a cosmetically independent expression with an identical runtime value).
- **Complexity scores are not a review finding (2026-08-20).** A score is a reason to read a function, never the finding itself, and reviewers neither raise one alone nor propose/approve a CI threshold on it (`ruff C901`, ESLint `complexity`, Sonar, CRAP). Why here rather than in `acceptance-mutation`, where the evidence was ingested: the rule fires when someone proposes or reviews a gate, which is this skill's moment. The measured basis is an eight-run grid where a forced complexity cap raised coverage on every run, raised design on none, and lowered readability on every one; its limits (n=1 product, single author, subjective design scores) are stated inline so the rule refuses a threshold without overclaiming general harm. Carries a comply-with-warning path rather than a refusal, because the user may legitimately want the gate.
- **The AFK slice gate points at the drain instead of copying it (2026-08-20).** The section carried its own copy of `bc-drain-issues`' parameters — "both axes independently approve", "the full review packet", "one remediation and re-review cycle" — and every one of them had gone stale: v3 permits initial review plus three cycles, dispatches a single combined reviewer at tier 1, materializes a scoped packet, and re-dispatches only the axes whose standing approval a deterministic trigger invalidated. Nobody edited this file when that loop changed, which is the whole failure mode. Rewritten to state only what this skill genuinely owns inside the loop (distinct scopes, packet-not-reasoning isolation, missing evidence is blocking, a rebase invalidates approval) and to name `bc-drain-issues` as the home for the numbers. One home per fact applies to canon describing canon — a duplicated parameter is a fact with two homes and no owner.
- **Assume-the-code-is-wrong stance considered and rejected (2026-07-16).** Bun told reviewers to assume the code is wrong and only hunt bugs. Rejected here because it directly conflicts with "Findings are not obligations": a reviewer prompted to find defects manufactures them, and in AFK runs nobody filters the padding — Bun had a human reading reviewer output; this workspace's bounded remediation cycle + severity gating extract the hunt-hard value without the spiral.
- **Source-tree docs pointer (2026-08-18).** When the diff touches README / existing `docs/` / architecture pages / contract JSDoc, Standards loads `codebase-docs` and flags a stale owner, change narration, or an invented `docs/` tree. It does not rewrite docs. Why: otherwise the model-invoked docs skill never fires in the review that would catch drift.

## Provenance

- [obra/superpowers `skills/requesting-code-review/SKILL.md`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/requesting-code-review/SKILL.md) — review-request workflow and severity expectations.
- [obra/superpowers `skills/requesting-code-review/code-reviewer.md`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/requesting-code-review/code-reviewer.md) — reviewer prompt template adapted into the review packet/checklist.
- [obra/superpowers `skills/receiving-code-review/SKILL.md`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/receiving-code-review/SKILL.md) — feedback reception, YAGNI check, pushback rules, GitHub thread detail.
- Matt Pocock upstream `skills/engineering/code-review/SKILL.md` at `391a2701dd948f94f56a39f753f8eea9a859c87` — fixed-point review packet, independent Spec/Standards axes, and separate aggregation. https://github.com/mattpocock/skills/blob/391a2701dd948f94f56a39f753f8eea9a859c87/skills/engineering/code-review/SKILL.md
- [anthropic-claude-code-best-practices.md](https://code.claude.com/docs/en/best-practices) — "Findings are not obligations": reviewer-incentive caution (a gap-hunting reviewer reports gaps even in sound work; chasing all findings over-engineers), bounding reviewers to correctness/stated requirements. Protects the AFK slice gate from remediation spirals. (ingested 2026-07-12)
- Field observation, `bendecastro/image-maze` issue #203, landed `f4a1e02` (2026-07-27) — a `/bc-drain-issues` run whose Spec reviewer proved that the clause surviving the original inert-guard fix was *itself* a production tautology, and that the first implementation had disguised it by swapping an identical-valued expression. Source of the "Verify a guard can actually fire" block. (field evidence, no `raw/` file)
- [bun-in-rust-zig-port-writeup.md](https://bun.com/blog/bun-in-rust) — Bun's Zig→Rust rewrite (Jarred Sumner, 2026-07-08): split-context adversarial review at fleet scale; adopted the reviewer context-isolation rule, rejected the assume-wrong stance (see design decisions). (ingested 2026-07-16)
- [unclebob/negative-test-experiment](https://github.com/unclebob/negative-test-experiment) — eight independent builds of the same product across four testing disciplines, crossed with a forced complexity cap. The measured basis for "Complexity scores are not a quality bar": the cap raised coverage on every run, design on none, readability on none. Ingested from the source below; see [`docs/research/raw/ingested/unclebob-quality-tools/`](../../docs/research/raw/ingested/unclebob-quality-tools/SOURCE.md). (2026-08-20)
- `concepts/codebase-docs/` — source-tree placement / current-state / same-change rules the Standards pointer loads (2026-08-18).

## Tests

`tests/scenario.md` — pressure scenarios for independent Spec/Standards review, fixed-point validation, blind implementation, performative agreement, unclear feedback, and reviewer overreach. Checks 1–6 pressure-tested 2026-07-16 **PASS** (Grok). Checks 7–9 pressure-tested 2026-08-21 **PASS** (Pi/Grok 4.6 medium; naive consumers; graded from `/tmp/pt-code-review-{7,8,9}` and `/tmp/bc-swarm/2026-08-21-gap-close/cr{7,8,9}.md`).

Check 7: reviewer treated `authorize(user_id, user_id)` as an inert production guard, was not reassured by `InjectedSeam.check("u1","u2")`, and rejected both near-misses (`row.owner_id` still `user_id`; `actor_id != actor_id`) with operand-origin traces.

Check 8: Standards loaded `codebase-docs`, flagged the stale README owner and invented `docs/cli.md`, and did not rewrite (`git status` only untracked `BASE.txt`). Drain Gate A check 26 still does not discharge this behavioural check.

Check 9: complexity score was not a finding; the CI-gate-and-split request was refused (comply-with-warning path named, not taken); function not split.

The 2026-08-20 AFK-slice-gate correction adds no scenario. It removed three stale factual claims about `/bc-drain-issues` and replaced them with a pointer; the accuracy of a pointer is checked by `bc-drain-issues`' own gate, and a pressure scenario cannot detect that a duplicated parameter has drifted — only reading both files can, which is why the duplication was removed rather than corrected in place.

## Deploy targets

Deployed to the shared bus, Pi, and Claude Code by `scripts/deploy-local-skills.py`, which deploys every concept carrying a `body/SKILL.md`. This shipped with that bulk deploy rather than by a per-concept decision, so the intended deploy-after-test sequence did not hold here. Current state is in this file's frontmatter; `python3 scripts/lint.py` fails while a deployed concept is untested.
