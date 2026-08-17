# Bases examples

These examples are starting points. Replace property names with the vault's actual schema and validate every expression before writing a Base.

## Active task table

```yaml
filters:
  and:
    - 'file.hasTag("task")'
    - 'file.ext == "md"'

formulas:
  days_until_due: 'if(due, (date(due) - today()).days, "")'
  overdue: 'if(due, date(due) < today() && status != "done", false)'

properties:
  status:
    displayName: Status
  formula.days_until_due:
    displayName: Days until due
  formula.overdue:
    displayName: Overdue

views:
  - type: table
    name: Active tasks
    filters:
      and:
        - 'status != "done"'
    order:
      - file.name
      - status
      - due
      - formula.days_until_due
      - formula.overdue
    groupBy:
      property: status
      direction: ASC
```

## Reading list cards and table

```yaml
filters:
  or:
    - 'file.hasTag("book")'
    - 'file.hasTag("article")'

formulas:
  status_icon: 'if(status == "reading", "📖", if(status == "done", "✅", "📚"))'
  year_read: 'if(finished_date, date(finished_date).year, "")'

views:
  - type: cards
    name: Library
    order:
      - file.name
      - author
      - formula.status_icon
  - type: table
    name: To read
    filters:
      and:
        - 'status == "to-read"'
    order:
      - file.name
      - author
      - pages
      - formula.year_read
```

## Embedding a Base

A Base can be embedded in a Markdown note, including a named view when supported:

```markdown
![[Tasks.base]]
![[Tasks.base#Active tasks]]
```
