---
test_kind: pressure
test_status: pass
tested: 2026-08-17
deployed: 2026-08-17
---
# Concept: json-canvas

Harness-neutral reference skill for JSON Canvas 1.0 `.canvas` files: nodes, edges, groups, links, IDs, layout, and deterministic validation.

## Design decisions

- **Format guidance, not mutation authority.** The body teaches the open file format and validation invariants. Targeted mutation still requires explicit user intent and an existing safe Obsidian/vault authority; the skill does not grant permission to write a vault.
- **No generic CLI or eval path.** The upstream `obsidian-cli` skill was deliberately excluded because its broad write and live-app evaluation path overlaps the safer `pi-obsidian-vault` boundary. This concept never suggests generic CLI commands or JavaScript evaluation.
- **Progressive disclosure.** The entry body is a short workflow; field details, examples, and layout/validation rules are in `body/references/`.
- **Current authority limitation.** `pi-obsidian-vault` remains Markdown-only. Canvas files are therefore format/validation references unless the consuming harness has an explicit safe structured-file authority; no `.canvas` mutation authority is invented here.
- **Selective ingestion.** The upstream whole-bundle install was rejected for the overlapping CLI authority and unrelated `defuddle` workflow. The complete upstream bundle remains only in the immutable raw snapshot; this concept adapts JSON Canvas 1.0 guidance.

## Provenance

- [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) at pinned commit [`a1dc48e68138490d522c04cbf5822214c6eb1202`](https://github.com/kepano/obsidian-skills/tree/a1dc48e68138490d522c04cbf5822214c6eb1202), licensed MIT. The immutable upstream snapshot is in `raw/ingested/kepano-obsidian-skills/`.
- Official authority: [JSON Canvas 1.0 specification](https://jsoncanvas.org/spec/1.0/) and the [JSON Canvas project](https://github.com/obsidianmd/jsoncanvas).
- The body is an adaptation with examples and validation split into local references; raw upstream content is evidence, never a runtime deploy source.

## Tests

`tests/accuracy-check.md` checks frontmatter, lean/progressive structure, JSON Canvas 1.0 invariants, ID/endpoint/layout guidance, provenance, and deploy state. `tests/pressure-scenario.md` attacks the mutation boundary with direct-write/`eval` pressure while no structured writer exists. **PASS — 2026-08-17**: static checks passed, the adversarial agent refused every bypass, the fixture hash stayed unchanged, and deployment links were verified.

## Deploy targets

Deployed 2026-08-17 through `scripts/deploy-local-skills.py`:

- Shared bus: `~/.agents/skills/json-canvas` → relative symlink to `body/` (Pi, Composer, Grok, OpenCode).
- Pi: `~/.pi/agent/skills/json-canvas` → relative symlink to `body/`.
- Claude Code: `~/.claude/skills/json-canvas` → relative symlink to `body/`.

This concept does not deploy or invoke `obsidian-cli` or `defuddle`; `.canvas` writes remain unavailable through `pi-obsidian-vault` unless a future safe structured-file authority is added.
