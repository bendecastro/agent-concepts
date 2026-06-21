# Writing Agent Briefs

An Agent Brief is the authoritative contract for `/bc-drain-issues`. The original issue body and comments are context; the brief is what the AFK agent should be able to execute.

## Principles

- **Durable over precise:** describe interfaces, behavior, types, and contracts. Avoid file paths and line numbers unless the issue is specifically about a path.
- **Behavioral, not procedural:** say what the system should do, not how to edit it.
- **Complete acceptance criteria:** every criterion should be independently verifiable.
- **Explicit scope boundaries:** name related work that is not part of this issue.

## Template

```md
## Agent Brief

**Category:** bug / enhancement
**Summary:** one-line description

**Current behavior:**
What happens now, or the current state of the PR/diff.

**Desired behavior:**
What should happen after this issue is complete, including edge cases.

**Key interfaces / domain concepts:**
- `TypeOrCommandOrConcept` — what changes and why

**Acceptance criteria:**
- [ ] Specific, testable criterion
- [ ] Specific, testable criterion

**Out of scope:**
- Adjacent thing not included

**Blocked by:**
- `#NN`, or None — can start immediately
```
