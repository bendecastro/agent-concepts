# Properties reference

Properties are YAML frontmatter at the beginning of a note. They are optional: use the vault's existing schema when one exists, and do not add a generic schema merely because a note can have one.

```yaml
---
title: Project Alpha
date: 2026-08-17
tags:
  - project
  - active
aliases:
  - Alpha
status: in-progress
rating: 4.5
completed: false
due: 2026-08-31T14:30:00
---
```

Common value shapes include:

| Shape | Example |
|---|---|
| Text | `title: Project Alpha` |
| Number | `rating: 4.5` |
| Checkbox | `completed: false` |
| Date | `date: 2026-08-17` |
| Date/time | `due: 2026-08-31T14:30:00` |
| List | `tags: [project, active]` or a YAML list |
| Internal link | `related: "[[Other Note]]"` |

Inline tags use forms such as `#project` and `#nested/topic`. In frontmatter, tags are normally a list of tag strings. Tags may contain letters, numbers (not as the first character), underscores, hyphens, and `/` for nesting.

`tags`, `aliases`, and `cssclasses` are common Obsidian properties, not a universal project contract. Preserve existing key names, value types, date conventions, and ordering when editing a note.

See the official [properties documentation](https://help.obsidian.md/properties).
