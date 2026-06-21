# Out-of-Scope Knowledge Base

Store rejected enhancement concepts in `.bc-agent/out-of-scope/` so future triage can dedupe recurring requests and preserve why the decision was made.

## File shape

One file per concept, not per issue:

```md
# Dark Mode

This project does not support dark mode or user-facing theming.

## Why this is out of scope

Durable, substantive reason. Reference project scope, technical constraints, or strategic decisions — not temporary workload.

## Prior requests

- #42 — "Add dark mode support"
```

## Rules

- Check `.bc-agent/out-of-scope/*.md` during triage before recommending new work.
- Write/update it only for rejected enhancements, not bugs and not already-implemented features.
- If the maintainer reconsiders, update or delete the file and proceed through normal triage.
