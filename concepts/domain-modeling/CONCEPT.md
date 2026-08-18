# Concept: domain-modeling

Model-invoked discipline for actively building and sharpening a project's domain model: challenge vague/conflicting terms into canonical names, stress-test with edge cases, cross-check claims against code, and persist the result into `CONTEXT.md` (a pure glossary) and — at a high bar — ADRs. The doc-writing engine behind the stateful `grill-me`.

## Design decisions

- **Glossary stays pure.** `CONTEXT.md` holds concepts and canonical names only — no file paths, schema, or specs. Mixing implementation in is the failure mode that makes the glossary rot and stop being a shared *language*; it's enforced as a rule with a refuted excuse in the pressure tests.
- **ADR three-part bar.** An ADR is written only when the decision is costly to reverse AND would puzzle a future reader AND reflects a real trade-off. Without the bar, agents emit trivial ADRs that bury the load-bearing ones.
- **Inline, not batched.** Captured the moment a term crystallizes; batching to session end loses early decisions. This is what makes `grill-me` genuinely stateful rather than a transcript dump.
- **Body is an adaptation, not a copy.** The upstream `domain-modeling/SKILL.md` was only recoverable as a faithful summary (see provenance); this body is reconstructed from that summary plus the catalog description, re-voiced to match this workspace.
- **Alternatives and supersede, not a notes-every-change gate (2026-08-18).** From DeepSeek Agent Notes, grilled and cut to two ideas: when an ADR *is* written, record genuine alternatives and why they lost; never rewrite an accepted ADR into a different decision — supersede and cross-link. The three-part bar is unchanged. Why: the code reconstructs the winner; only the record can carry what was given up, and a silent rewrite hides the reversal.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) `captured-skills.md` — `domain-modeling` section (**summary only**, not verbatim) + the verbatim `grill-with-docs` body that composes it. https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md
- [skillsskillsproductivityteach at main.md](https://github.com/mattpocock/skills/tree/main) — catalog #2 "shared language" failure mode and the `CONTEXT.md` before/after example (materialization cascade).
- [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) `.agents/notes/README.md` at commit `99f6f02` — alternatives-mandatory and supersede-don't-rewrite; the required-every-change gate was inspected and rejected. See `raw/ingested/deepseek-harness/SOURCE.md`.

## Tests

`tests/accuracy-check.md` — checks the body faithfully encodes the three disciplines (challenge / stress-test / cross-reference), the pure-glossary rule, the multi-context `CONTEXT-MAP.md` layout, the ADR three-part bar, and the 2026-08-18 alternatives / supersede clauses. Discipline behavior is pressure-tested transitively via `grill-me` (attacks 2–4 there target this skill). The new ADR clauses are accuracy-checked only; no dedicated pressure rerun yet.

## Deploy targets

- Claude Code: `~/.claude/skills/domain-modeling` → relative symlink to `body/`.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../harnesses.md`.
