# Work sync plan format

One message, in chat, before any write. Leave out a section with nothing in it, and say "nothing to change" when every section is empty.

```md
## Work sync plan — <project>, <date>

Sources read: <requirements path>, <decisions path> (latest entry: <number/date>), <research path>, <ideas path>, open issues: <yes/no, count>.
Stages: <the Stages: line, or "none; propose adding `Stages: now, next, later, unscheduled`">

### New items
| # | Title | Stage | From |
| --- | --- | --- | --- |
| new | <title> | <stage> | <doc and section, or issue #N> |

### Moves
- work item <NNN>: <from> → <to> — <why: all steps checked / work landed in <short SHA> "<subject>">

### Fixes to existing items
- work item <NNN>: <what changes> — <doc that says so>

### Stale active items
- work item <NNN>: last commit <date> (<N> days) — <proposal>

### Ideas that became items
- `<idea line>` → work item <NNN>: remove the line

### Links by path
- <file:line>: `<path link>` → "work item <NNN>"

### Questions
1. <question, with both sources and their dates>
   1. <recommended option> (recommended)
   2. <other option>

Reply with approvals or changes (for example "all, but 2.2") and answer the questions. Approval does not answer an open question; dependent work remains open. Nothing is written until then.
```

Rules for the plan:

- Every proposed item, move and fix names the doc, issue or commit it comes from. Why: the owner checks a claim against its source, not against your summary.
- Numbers in "New items" stay `new` in the plan; real numbers are assigned when writing, in the main checkout.
- A disagreement between two docs goes under Questions, never under Fixes.
