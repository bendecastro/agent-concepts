---
test_kind: pressure
test_status: pass
tested: 2026-08-17
deployed: 2026-08-17
---
# Concept: obsidian-bases

Harness-neutral reference skill for authoring and validating Obsidian Bases `.base` files: YAML filters, formulas, views, properties, and summaries.

## Design decisions

- **Format guidance, not mutation authority.** The body describes valid `.base` data and deterministic checks. Targeted mutation still requires explicit user intent and an existing safe Obsidian/vault authority; the skill does not grant permission to write a vault.
- **No generic CLI or eval path.** The upstream `obsidian-cli` skill was deliberately excluded because its broad write and live-app evaluation path overlaps the safer `pi-obsidian-vault` boundary. This concept never suggests generic CLI commands or JavaScript evaluation.
- **Progressive disclosure.** The entry body stays lean; schema/filter rules, formula functions, examples, and troubleshooting are in `body/references/`.
- **Current authority limitation.** `pi-obsidian-vault` remains Markdown-only. Bases are therefore format/validation references unless the consuming harness has an explicit safe structured-file authority; no `.base` mutation authority is invented here.
- **Selective ingestion.** The upstream whole-bundle install was rejected for the same overlapping CLI authority and unrelated `defuddle` workflow. The complete upstream bundle remains only in the immutable raw snapshot; this concept adapts the Bases format guidance.

## Provenance

- [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) at pinned commit [`a1dc48e68138490d522c04cbf5822214c6eb1202`](https://github.com/kepano/obsidian-skills/tree/a1dc48e68138490d522c04cbf5822214c6eb1202), licensed MIT. The immutable upstream snapshot is in `docs/research/raw/ingested/kepano-obsidian-skills/`.
- Official authorities: [Bases syntax](https://help.obsidian.md/bases/syntax), [Bases views](https://help.obsidian.md/bases/views), and [formulas](https://help.obsidian.md/formulas).
- The body is an adaptation with long material split into local references; raw upstream content is evidence, never a runtime deploy source.

## Tests

`tests/accuracy-check.md` checks frontmatter, lean/progressive structure, valid YAML schema terms, formula/duration guidance, provenance, and deploy state. `tests/pressure-scenario.md` attacks the mutation boundary with shell/direct/`eval` pressure while no structured writer exists. **PASS — 2026-08-17**: static checks passed, the adversarial agent refused every bypass, the fixture hash stayed unchanged, and deployment links were verified.

## Deploy targets

Deployed 2026-08-17 through `scripts/deploy-local-skills.py`:

- Shared bus: `~/.agents/skills/obsidian-bases` → relative symlink to `body/` (Pi, Composer, Grok, OpenCode).
- Pi: `~/.pi/agent/skills/obsidian-bases` → relative symlink to `body/`.
- Claude Code: `~/.claude/skills/obsidian-bases` → relative symlink to `body/`.

This concept does not deploy or invoke `obsidian-cli` or `defuddle`; `.base` writes remain unavailable through `pi-obsidian-vault` unless a future safe structured-file authority is added.
