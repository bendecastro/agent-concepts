# Bases syntax reference

A `.base` file is YAML. The top-level sections are optional, but each must use the expected shape.

```yaml
filters: <filter string or recursive filter object>
formulas:
  formula_name: <expression>
properties:
  property_name:
    displayName: Display name
summaries:
  summary_name: <expression>
views:
  - type: table
    name: View name
    order:
      - file.name
      - status
```

## Filters

A filter can be one expression:

```yaml
filters: 'status == "active"'
```

Or a recursive object with exactly one logical key at each level:

```yaml
filters:
  and:
    - 'status == "active"'
    - or:
        - 'file.hasTag("project")'
        - 'file.inFolder("Projects")'
    - not:
        - 'file.hasTag("archived")'
```

Operators include `==`, `!=`, `>`, `<`, `>=`, `<=`, `&&`, `||`, and `!`. Quote filter expressions whenever YAML punctuation, `:`, `#`, brackets, or nested quotes could change parsing.

## Property namespaces

- **Note properties:** frontmatter values such as `status` or `note.author`.
- **File properties:** metadata such as `file.name`, `file.path`, `file.folder`, `file.ext`, `file.size`, `file.ctime`, `file.mtime`, `file.tags`, `file.links`, `file.backlinks`, `file.embeds`, and `file.properties`.
- **Formula properties:** computed values referenced as `formula.name` after defining `name` under `formulas`.

The `this` value refers to the Base in its main content area, the embedding file when the Base is embedded, or the active file in a sidebar.

## Views

Each view may include `type`, `name`, `limit`, `filters`, `groupBy`, `order`, and `summaries` as appropriate.

```yaml
views:
  - type: table
    name: Active
    limit: 20
    groupBy:
      property: status
      direction: ASC
    order:
      - file.name
      - status
      - formula.days_until_due
    summaries:
      estimate: Sum
```

The format guidance names these view types:

- `table` — properties in ordered columns.
- `cards` — card-style property display.
- `list` — compact ordered entries.
- `map` — location-oriented display; verify the vault's map support and coordinate properties.

## Display names and summaries

Use `properties` to customize display names, including `formula.name` and file properties. Built-in summary names include `Average`, `Min`, `Max`, `Sum`, `Range`, `Median`, `Stddev`, `Earliest`, `Latest`, `Checked`, `Unchecked`, `Empty`, `Filled`, and `Unique`; select a summary compatible with the property's type.
