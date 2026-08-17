# Concept: obsidian-markdown

Harness-neutral reference skill for Obsidian Flavored Markdown (OFM): wikilinks, embeds, callouts, properties, tags, comments, and other syntax that extends CommonMark/GFM.

## Design decisions

- **Format guidance, not mutation authority.** The body teaches syntax and validation. It routes vault reads and writes through an existing agent-safe Obsidian/vault tool when available and explicitly forbids bypassing approval or path-safety rails with shell/direct writes.
- **No mandatory note methodology.** Frontmatter, tags, aliases, and CSS classes are optional unless the user or project already requires them. Existing vault conventions win.
- **Progressive disclosure.** The entry body is a short workflow and syntax spine; callouts, embeds, and property details live under `body/references/`.
- **Selective ingestion.** The upstream whole-bundle install was rejected because `obsidian-cli` would overlap the safer `pi-obsidian-vault` mutation boundary and `defuddle` is a generic network/content-extraction workflow. Only this low-risk format skill was adapted into a canonical concept; the raw snapshot retains the complete upstream tree for audit.

## Provenance

- [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) at pinned commit [`a1dc48e68138490d522c04cbf5822214c6eb1202`](https://github.com/kepano/obsidian-skills/tree/a1dc48e68138490d522c04cbf5822214c6eb1202), licensed MIT. The immutable upstream snapshot is in `raw/ingested/kepano-obsidian-skills/`.
- Official authorities: [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown), [internal links](https://help.obsidian.md/links), [embeds](https://help.obsidian.md/embeds), [callouts](https://help.obsidian.md/callouts), and [properties](https://help.obsidian.md/properties).
- The body is an adaptation, not a deploy symlink to raw upstream material. The raw snapshot includes excluded `obsidian-cli` and `defuddle` for evidence only.

## Tests

`tests/accuracy-check.md` checks frontmatter, progressive references, core OFM forms, optional methodology wording, mutation-authority rails, upstream provenance, and deploy state. **PASS — 2026-08-17** after focused static checks and nine-link deployment verification.

## Deploy targets

Deployed 2026-08-17 through `scripts/deploy-local-skills.py`:

- Shared bus: `~/.agents/skills/obsidian-markdown` → relative symlink to `body/` (Pi, Composer, Grok, OpenCode).
- Pi: `~/.pi/agent/skills/obsidian-markdown` → relative symlink to `body/`.
- Claude Code: `~/.claude/skills/obsidian-markdown` → relative symlink to `body/`.

The concept does not deploy or invoke `obsidian-cli` or `defuddle`.
