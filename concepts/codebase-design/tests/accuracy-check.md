# Accuracy check: codebase-design

Reference vocabulary — no runtime gate, so an accuracy check suffices (per AGENTS.md). Verify `body/SKILL.md` against the verbatim capture in [mattpocock/skills](https://github.com/mattpocock/skills) `skills/engineering/codebase-design/SKILL.md`:

- [x] Glossary defines all eight terms faithfully: Module, Interface, Implementation, Depth, Seam, Adapter, Leverage, Locality.
- [x] Each term keeps its "Avoid" guidance (unit/component/service; API/signature; boundary).
- [x] Deep-vs-shallow: deep = small interface + lots of implementation; shallow = large interface + thin implementation (avoid).
- [x] Four principles present: depth-is-a-property-of-the-interface; the deletion test; the interface-is-the-test-surface; one-adapter-hypothetical / two-adapters-real.
- [x] Three testability rules: accept-don't-create dependencies; return-results-not-side-effects; small surface area.
- [x] Rejected framings present: depth-as-line-ratio (Ousterhout); "interface" as the TS keyword; "boundary" as DDD bounded context.
- [x] No invented terms beyond the source. Omissions (DEEPENING.md, DESIGN-IT-TWICE.md) are documented in CONCEPT.md, not silent.

## Run result — 2026-08-21 — **PASS**

Compared `body/SKILL.md` to live `https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/codebase-design/SKILL.md` (114 lines at `/tmp/mattpocock-codebase-design-SKILL.md`). Artifact: `/tmp/bc-swarm/2026-08-21-gap-close/cd-acc.md`. Parent spot-checked local glossary lines 12–18 against the scout quotes. Condensation (not fails): Relationships section and ASCII diagrams omitted locally; CONCEPT.md still names the two expansion files.
