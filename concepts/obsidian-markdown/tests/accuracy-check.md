# Obsidian Markdown accuracy check

Reference concept with no runtime mutation gate; verify the adapted format guidance against the pinned upstream snapshot and official Obsidian references.

## Checks

1. Parse `body/SKILL.md` frontmatter and confirm `name: obsidian-markdown` matches the directory.
2. Confirm the body links to all three local progressive references and each file exists.
3. Confirm the body teaches wikilinks, embeds, callouts, properties, tags, comments, and `==highlight==` without making frontmatter/tags/aliases mandatory.
4. Confirm the body states that an existing agent-safe Obsidian/vault tool owns mutation and forbids shell/direct-write bypasses.
5. Compare the adapted syntax against the pinned upstream body and the official OFM, links, embeds, callouts, and properties references; resolve any drift before deployment.
6. Confirm the raw snapshot contains the upstream MIT notice and full `skills/` tree, while the deploy symlink resolves to `concepts/obsidian-markdown/body/`, not `raw/`.

## Result — 2026-08-17

**PASS.** Frontmatter, references, syntax coverage, optional methodology wording, mutation-authority rail, pinned provenance, raw snapshot, and deployment target were checked during the selective ingest.
