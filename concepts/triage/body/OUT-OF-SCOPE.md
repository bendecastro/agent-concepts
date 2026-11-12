# Recording rejected requests

Record a rejected enhancement in the project's **work-dropped** folder (resolved as in [SKILL.md](SKILL.md#where-project-files-go)) so future triage can dedupe recurring requests and see why the decision was made. Record the reason every time: a rejection without one cannot be re-evaluated and will be re-argued.

## With a "Where things go" table

The rejection is a work item in the work-dropped folder, named and numbered by the work-item rules in `.bc-agent/AGENTS.md` (`<3-digit number>-<slug>.md`; next number is the highest across all stage folders plus one) and written from `.bc-agent/templates/work-item.md`. One item per rejected concept, not per issue:

```md
# Dark mode

Why: users asked for a dark theme (#42).
Done when: not applicable; rejected.
Issue: #42

## Steps

## Outcome

Rejected: this project does not support dark mode or user-facing theming. <Durable, substantive reason: project scope, technical constraints, or strategic decisions, not temporary workload.>

Prior requests:
- #42 — "Add dark mode support"
```

Create numbered items only from the main checkout. Why: two git worktrees cannot see each other's numbers and would pick the same one. In a worktree, add a one-line note to the ideas file instead and tell the maintainer the rejection still needs recording.

## Without a table

Use `.bc-agent/out-of-scope/<concept>.md`, one file per concept:

```md
# Dark Mode

This project does not support dark mode or user-facing theming.

## Why this is out of scope

Durable, substantive reason. Reference project scope, technical constraints, or strategic decisions — not temporary workload.

## Prior requests

- #42 — "Add dark mode support"
```

## Rules

- Check the work-dropped folder during triage before recommending new work.
- When a new request matches an existing record, add the issue to its prior requests instead of creating a second record. Why: one record per concept keeps the reason in one place.
- Record only rejected enhancements, not bugs and not already-implemented features.
- If the maintainer reconsiders, edit or remove the record and proceed through normal triage; with a table, `git mv` the item to the work-planned folder and replace the rejection under `## Outcome` with a note that it was reconsidered.
