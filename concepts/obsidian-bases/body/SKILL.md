---
name: obsidian-bases
description: Author and validate Obsidian Bases .base files with YAML filters, formulas, views, properties, and summaries. Use when a task involves Bases or database-like views over notes.
---

# Obsidian Bases

A `.base` file is YAML describing one or more views over note properties and file metadata. This skill covers the format and validation; it is not a permission to mutate a vault.

## Authority boundary

For an existing vault, use the available safe Obsidian/vault authority for retrieval, validation, and any targeted write. A write requires explicit user intent and an explicit safe target. Do not use generic Obsidian CLI commands, JavaScript evaluation, shell redirection, or direct filesystem writes to bypass approval and path-safety rails. Do not overwrite an existing Base or create a broad batch operation by inference.

## Workflow

1. Identify the exact `.base` target and inspect its current schema and the properties it references. Preserve project naming and view conventions.
2. Draft valid YAML with only the sections needed: `filters`, `formulas`, `properties`, `summaries`, and `views`.
3. Use a filter string or a recursive filter object with exactly one logical key (`and`, `or`, or `not`) at each object level. Quote expressions containing YAML-special characters or nested quotes.
4. Reference note properties directly, file metadata as `file.*`, and formulas as `formula.*`. Guard formulas against missing properties.
5. Validate YAML, formula references, view types, property names, and summary compatibility. If Obsidian is available, open the Base and check that every view renders.
6. Load the focused references as needed: [schema and filters](references/SYNTAX.md), [functions and formulas](references/FUNCTIONS.md), [examples](references/EXAMPLES.md), and [troubleshooting](references/TROUBLESHOOTING.md).

## Minimal shape

```yaml
filters:
  and:
    - 'status == "active"'
    - 'file.hasTag("project")'

formulas:
  days_until_due: 'if(due, (date(due) - today()).days, "")'

properties:
  status:
    displayName: Status
  formula.days_until_due:
    displayName: Days until due

views:
  - type: table
    name: Active work
    order:
      - file.name
      - status
      - formula.days_until_due
```

The supported view types in the upstream format guidance are `table`, `cards`, `list`, and `map`. A map view needs the relevant location properties and the map support expected by that vault.

## References

- [Obsidian Bases syntax](https://help.obsidian.md/bases/syntax)
- [Obsidian Bases views](https://help.obsidian.md/bases/views)
- [Obsidian formulas](https://help.obsidian.md/formulas)
- [Schema and filters](references/SYNTAX.md)
- [Functions and formulas](references/FUNCTIONS.md)
- [Examples](references/EXAMPLES.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)
