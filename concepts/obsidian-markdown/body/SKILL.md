---
name: obsidian-markdown
description: Author and review Obsidian Flavored Markdown with wikilinks, embeds, callouts, properties, tags, comments, and other Obsidian-specific syntax. Use when working with Obsidian Markdown or when a note needs Obsidian-aware formatting.
---

# Obsidian Flavored Markdown

Use this skill for the Obsidian-specific layer on top of CommonMark and GFM. Standard Markdown remains the default for ordinary headings, lists, tables, quotes, emphasis, and code.

## Authority boundary

This is format guidance, not permission to mutate a vault. When an agent-safe Obsidian or vault tool is available, use it for retrieval, validation, creation, editing, moving, or deletion. Never bypass that tool's approval, target, or path-safety rails with shell commands or direct filesystem writes. Do not infer a vault path, bulk-edit notes, overwrite a full note, or impose a note methodology without explicit user/project instruction.

## Workflow

1. Inspect the existing note or the user's explicit target and preserve the vault's established naming, linking, and frontmatter conventions.
2. Draft ordinary Markdown first, then add only the Obsidian extensions the note needs.
3. Use wikilinks for notes inside the vault and normal Markdown links for external URLs. Use embeds only when the referenced file, heading, or block is known.
4. Treat frontmatter, `tags`, `aliases`, and `cssclasses` as optional. Add them only when the user or project requires them; never make a generic template mandatory.
5. Load the focused reference when needed: [properties](references/PROPERTIES.md), [callouts](references/CALLOUTS.md), or [embeds](references/EMBEDS.md).
6. Validate syntax and links with the available safe validator, then check the rendered result in Obsidian when a rendering check is available.

## Core syntax

```markdown
[[Note Name|Display Text]]
[[Note Name#Heading]]
[[Note Name#^block-id]]

![[Note Name#Heading]]
![[image.png|300]]

> [!note] Optional title
> Callout content.

==highlighted text==
```

A block ID is written as `^id` after a paragraph, list, or quote. Obsidian also supports inline and fenced comments, LaTeX math, Mermaid diagrams, footnotes, and inline tags; use the references and official documentation for their exact forms.

## References

- [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown)
- [Internal links](https://help.obsidian.md/links)
- [Embeds](https://help.obsidian.md/embeds)
- [Callouts](https://help.obsidian.md/callouts)
- [Properties](https://help.obsidian.md/properties)
