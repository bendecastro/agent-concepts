# Accuracy check: domain-modeling

This skill's discipline is pressure-tested transitively through `grill-me` (attacks 2–4 there target glossary purity, ADR inflation, and batch-at-the-end). This file is the standalone source-accuracy check for the body.

Verify `body/SKILL.md` encodes, faithfully to the upstream summary in `raw/pocock-skills-upstream/captured-skills.md`:

- [ ] Three active disciplines present: challenge terminology in real time, stress-test with concrete edge-case scenarios, cross-reference stated logic against actual code.
- [ ] `CONTEXT.md` defined as a **pure glossary** at the repo root, stripped of implementation detail.
- [ ] Multi-context layout: `CONTEXT-MAP.md` at root → per-bounded-context `CONTEXT.md`.
- [ ] ADR three-part bar: costly to reverse AND would puzzle a future reader AND real trade-offs — all three, else skip.
- [ ] "Capture immediately, don't batch" stated explicitly.
- [ ] No invented mechanics beyond the source (the body is an adaptation of a summary; flag any additions as design decisions in CONCEPT.md).
