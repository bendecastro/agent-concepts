# Concept: codebase-design

Model-invoked **reference vocabulary** for designing deep modules: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface. Shared language the other engineering skills (`tdd`, `to-prd`) reach for so terminology stays consistent across the suite.

## Design decisions

- **Vocabulary discipline, not a process.** The value is everyone using the same words — Module, Interface, Implementation, Depth, Seam, Adapter, Leverage, Locality — and *not* substituting "component/service/API/boundary". The "Rejected framings" section is load-bearing: it pins down what the terms deliberately do NOT mean (esp. depth-as-leverage vs Ousterhout's line-ratio, and "seam" not "boundary").
- **Reference concept → accuracy check, not pressure test.** Per AGENTS.md, concepts with no runtime gate need only an accuracy check, not a scripted pressure scenario.
- **Expansion files not ported.** Upstream has `DEEPENING.md` (dependency categories, replace-don't-layer testing) and `DESIGN-IT-TWICE.md` (parallel sub-agents design the interface several ways, then compare). Left out for now to keep the body a single self-contained glossary; the "Going deeper" pointers were dropped rather than left as broken links. Port them later if the deep-dive is wanted — they're summarized in the raw capture.

## Provenance

- `raw/ingested/pocock-skills-upstream/captured-skills.md` — verbatim `codebase-design/SKILL.md` (glossary, principles, testability, rejected framings); `DEEPENING.md`/`DESIGN-IT-TWICE.md` noted but not captured in full. https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md
- Underlying sources: John Ousterhout, *A Philosophy of Software Design* (deep modules); Michael Feathers (seams).

## Tests

`tests/accuracy-check.md` — confirms the glossary terms, the deep-vs-shallow framing, the four principles (depth-is-interface, deletion test, interface-is-test-surface, one-vs-two-adapter), the testability rules, and the rejected framings are present and faithful.

## Deploy targets

- Claude Code: `~/.claude/skills/codebase-design` → relative symlink to `body/`.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../harnesses.md`.
