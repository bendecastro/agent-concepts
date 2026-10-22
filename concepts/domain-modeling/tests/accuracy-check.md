# Accuracy check: domain-modeling

Historical pressure evidence came transitively through the `grill-me` wrapper (attacks 2–4 targeted glossary purity, ADR inflation, and batch-at-the-end); that wrapper was removed 2026-09-27. This file is the standalone source-accuracy check for the body.

Verify `body/SKILL.md` encodes, faithfully to the upstream summary in [mattpocock/skills](https://github.com/mattpocock/skills) `skills/engineering/domain-modeling/SKILL.md`:

- [ ] Three active disciplines present: challenge terminology in real time, stress-test with concrete edge-case scenarios, cross-reference stated logic against actual code.
- [ ] `glossary.md` defined as a **pure glossary** at the repo root, stripped of implementation detail.
- [ ] Multi-context layout: `glossary-map.md` at root → per-bounded-context `glossary.md`.
- [ ] ADR three-part bar: costly to reverse AND would puzzle a future reader AND real trade-offs — all three, else skip.
- [ ] When an ADR is written: genuine alternatives and why each lost; never rewrite an accepted ADR into a different decision — supersede and cross-link. Flagged as a 2026-08-18 design decision in CONCEPT.md (not upstream).
- [ ] "Capture immediately, don't batch" stated explicitly.
- [ ] No invented mechanics beyond the source (the body is an adaptation of a summary; flag any additions as design decisions in CONCEPT.md).

## Filename migration checks (2026-10-22)

- [x] Legacy-only repository: read the existing glossary and propose a rename; do not silently rename or create a second glossary, even under time pressure.
- [ ] Canonical-only repository: use lowercase `glossary.md`; multi-context systems use root `glossary-map.md` and bounded-context `glossary.md`.
- [ ] Vault adapter still uses `project/overview.md` or `project/glossary.md`; generic naming does not move vault content.

The owner decision and parent defaults, not upstream, authorize these filename additions. The [legacy-glossary pressure scenarios](pressure-legacy-glossary.md) passed both legacy-only cases on 2026-10-22 against dbdddb6 wording, with skill text confirmed in both consumers’ contexts. The first two runs were invalid (skill not loaded), not rule failures. This run does not cover canonical-only or vault-adapter fixtures. No deploy is authorized by this check.
