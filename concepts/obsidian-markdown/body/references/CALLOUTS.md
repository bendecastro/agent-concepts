# Callouts reference

Obsidian callouts are blockquotes whose first line begins with `[!type]`. The marker may include a title; `-` or `+` immediately after the type makes the callout collapsed or expanded by default.

```markdown
> [!note]
> A basic callout.

> [!warning] Custom title
> A warning with a visible title.

> [!faq]- Collapsed question
> Details hidden until expanded.

> [!question] Outer callout
> > [!note] Nested callout
> > Nested content.
```

## Common types

| Type | Aliases |
|---|---|
| `note` | — |
| `abstract` | `summary`, `tldr` |
| `info` | — |
| `todo` | — |
| `tip` | `hint`, `important` |
| `success` | `check`, `done` |
| `question` | `help`, `faq` |
| `warning` | `caution`, `attention` |
| `failure` | `fail`, `missing` |
| `danger` | `error` |
| `bug` | — |
| `example` | — |
| `quote` | `cite` |

Custom callout types need CSS in the vault. Do not assume a community plugin or custom CSS exists; a plain supported type is safer when portability matters.

See the official [callouts documentation](https://help.obsidian.md/callouts) for nesting and rendering details.
