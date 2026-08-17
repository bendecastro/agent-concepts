# Bases troubleshooting and validation

Before treating a Base as complete, check:

- YAML parses as one document with the intended top-level keys.
- Every recursive filter object has exactly one of `and`, `or`, or `not`.
- Every `formula.name` reference has a matching `formulas.name` definition.
- Every ordered property exists or is a valid `file.*`, note property, or formula property.
- Optional properties are guarded before date parsing, arithmetic, or string methods.
- Formulas use valid YAML quoting; nested double quotes usually need an outer single-quoted string.
- View `type`, `groupBy`, `limit`, `order`, and `summaries` values match the current official syntax.
- The file remains a `.base` file and is not silently converted to Markdown.

## Frequent errors

### YAML punctuation

Unquoted `:`, `{}`, `[]`, `#`, `?`, `|`, `>`, `=`, or nested quotes can change YAML parsing. Quote the complete expression:

```yaml
# Safe
label: 'if(done, "Yes", "No")'
```

### Undefined formulas

A display property or view order such as `formula.total` is invalid unless `formulas.total` exists. Define it first or remove the reference.

### Duration arithmetic

`now() - file.ctime` produces a Duration. Use `.days`, `.hours`, or another duration field before calling number methods.

### Missing values

Not every note has every property. Guard expressions with `if(property, ..., ...)` instead of assuming a value exists across the entire view.

### Rendering mismatch

A YAML parser can accept a file that Obsidian still rejects semantically. If possible, open the exact Base in Obsidian and inspect each view; report version/plugin limitations rather than silently changing the schema.

For current syntax, defer to the official [Bases syntax](https://help.obsidian.md/bases/syntax), [views](https://help.obsidian.md/bases/views), and [formulas](https://help.obsidian.md/formulas) documentation.
