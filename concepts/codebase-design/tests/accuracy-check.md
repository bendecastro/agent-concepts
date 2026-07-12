# Accuracy check: codebase-design

Reference vocabulary — no runtime gate, so an accuracy check suffices (per AGENTS.md). Verify `body/SKILL.md` against the verbatim capture in `raw/ingested/pocock-skills-upstream/captured-skills.md`:

- [ ] Glossary defines all eight terms faithfully: Module, Interface, Implementation, Depth, Seam, Adapter, Leverage, Locality.
- [ ] Each term keeps its "Avoid" guidance (unit/component/service; API/signature; boundary).
- [ ] Deep-vs-shallow: deep = small interface + lots of implementation; shallow = large interface + thin implementation (avoid).
- [ ] Four principles present: depth-is-a-property-of-the-interface; the deletion test; the interface-is-the-test-surface; one-adapter-hypothetical / two-adapters-real.
- [ ] Three testability rules: accept-don't-create dependencies; return-results-not-side-effects; small surface area.
- [ ] Rejected framings present: depth-as-line-ratio (Ousterhout); "interface" as the TS keyword; "boundary" as DDD bounded context.
- [ ] No invented terms beyond the source. Omissions (DEEPENING.md, DESIGN-IT-TWICE.md) are documented in CONCEPT.md, not silent.
