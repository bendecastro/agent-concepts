# Embeds reference

Prefix an internal wikilink with `!` to embed a note, section, block, or supported file.

```markdown
![[Note Name]]
![[Note Name#Heading]]
![[Note Name#^block-id]]
![[image.png]]
![[image.png|300]]
![[image.png|640x480]]
![[document.pdf#page=3]]
![[audio.mp3]]
```

A block ID can follow a paragraph or list:

```markdown
- First item
- Second item

^list-id
```

Then embed it with `![[Note Name#^list-id]]`. Bases may be embedded as `![[Tasks.base]]` or, when supported by the file, `![[Tasks.base#View Name]]`.

Use normal Markdown image syntax for external images:

```markdown
![Alt text](https://example.com/image.png)
```

Do not invent a target path. Confirm that the referenced note or file exists through the available safe vault retrieval tool, and preserve the vault's choice of wikilinks versus Markdown links.

See the official [embeds documentation](https://help.obsidian.md/embeds).
