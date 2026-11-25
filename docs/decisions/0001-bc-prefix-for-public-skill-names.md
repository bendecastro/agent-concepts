# 0001: The `bc-` prefix for public skill names

Date: 2026-11-25
Status: accepted

## Context

Generic names such as `tdd`, `code-review` and `research` are also used by other skill collections. On a clash, `npx skills` overwrites the earlier skill and Pi keeps the first one it finds and warns. Claude Code plugins avoid this with a `plugin:skill` prefix, but Codex, Pi and `npx skills` have nothing equivalent.

## Decision

Every public skill's name starts with `bc-`. The old names stay as aliases on the owner's machines only; no published package carries them.

## Consequences

- No public name clashes on any agent, by one rule instead of a list of risky names.
- Every reference in bodies, relationships, tests and docs changes once; the move to name references (item `024-skill-delivery`) already touches each of them.
- Historical records (past log entries, finished work items, old test results) keep the old names.

## Alternatives considered

- Prefix only the generic names: less renaming, but a clash can appear later on an unforeseen name, and the naming is uneven.
- Keep the names and document clashes: leaves the silent overwrite in place.
