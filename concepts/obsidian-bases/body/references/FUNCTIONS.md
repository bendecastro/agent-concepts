# Bases functions and formulas reference

Define reusable formulas under `formulas`, then reference them as `formula.name` in view order or display properties.

```yaml
formulas:
  total: 'price * quantity'
  status_icon: 'if(done, "✅", "⏳")'
  created: 'file.ctime.format("YYYY-MM-DD")'
  days_old: '(now() - file.ctime).days'
  days_until_due: 'if(due, (date(due) - today()).days, "")'
```

## Common functions

| Function | Purpose |
|---|---|
| `date(string)` | Parse a date value. |
| `now()` | Current date and time. |
| `today()` | Current date at midnight. |
| `if(condition, yes, no?)` | Conditional result. |
| `duration(string)` | Parse a duration. |
| `file(path)` | Resolve a file value. |
| `link(path, display?)` | Build a link value. |

For exhaustive function signatures, consult the [official formulas documentation](https://help.obsidian.md/formulas) and the pinned upstream reference at [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills/blob/a1dc48e68138490d522c04cbf5822214c6eb1202/skills/obsidian-bases/references/FUNCTIONS_REFERENCE.md); use official Obsidian documentation as the authority when syntax changes.

## Dates and durations

Subtracting dates returns a Duration, not a number. Access a field before applying numeric functions:

```yaml
formulas:
  age_days: '(now() - file.ctime).days'
  rounded_age: '(now() - file.ctime).days.round(0)'
  due_days: 'if(due, (date(due) - today()).days, "")'
```

Do not round or divide a Duration directly. Guard optional properties before parsing or subtracting them; a Base usually spans notes with incomplete frontmatter.

Date arithmetic accepts duration strings such as `"1 day"`, `"7d"`, or `"2 weeks"`:

```yaml
formulas:
  tomorrow: 'today() + "1 day"'
  next_week: 'today() + "7d"'
```

Use single-quoted YAML strings when the expression contains double-quoted string literals. If a formula includes YAML-special characters, quote the complete expression and validate the parsed YAML before relying on it.
