# Plans

Plans are durable design and implementation records. Their lifecycle is encoded in the directory path.

| Folder | Meaning |
|---|---|
| `proposed/` | The plan is not approved or started. |
| `active/` | The plan is approved, but implementation or verification remains open. |
| `implemented/` | The plan is complete and its rationale remains useful. |
| `rejected/` | The proposal was considered and declined; keep it only while it prevents a plausible repeated mistake. |
| `archived/` | The plan is historical and no longer current; archived files are frozen. |

Each plan carries a `Status:` line matching its lifecycle folder; `scripts/lint.py` checks that agreement. Move a plan when its lifecycle changes, rather than copying it or maintaining a second status list. Current behavior belongs in the owning README, reference page, or concept; plans retain the design reasoning and execution record.

The lifecycle folders are intentionally not subdivided by topic yet. Stable filenames and the `bc-` prefixes are sufficient at the current scale.
