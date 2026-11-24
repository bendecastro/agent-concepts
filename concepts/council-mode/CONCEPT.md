---
test_kind: pressure
test_status: not-run
tested: never
deployed: no
---
# Concept: council-mode

Model-invoked protocol for a bounded, parent-supervised advisor council on a decision with real tradeoffs: 2–4 read-only `council-*` advisors write independent structured reports, the parent relays curated disputed claims for one cross-examination round (a third only on request), and the parent alone writes the decision memo.

## Design decisions

- **Adopted from the `pi-subagents` package (2026-11-24, owner decision).** The owner is making the council a central part of the workflow. Left in the package, it changed with every unpinned `pi-subagents` update and could not be edited; the owner's private `bc-improve-codebase-council` also depends on its roster cap, fallback and relay rules. The body is a verbatim copy of upstream with one change: the reference path is relative to `body/` instead of the package root.
- **Pi-specific mechanics stay.** The steps rely on `pi-subagents` workflow scripts (`runs.all`), resumable runs and `outputSchema`. When upstream changes those, compare against the version recorded below and update this copy.
- **Not deployed yet.** Two things must happen before switching: the test gate (it enforces a pass cap, read-only advisors and parent-only synthesis), and excluding the package's own copy so Pi does not load two `council-mode` skills. The package's `/council` prompt also loads the protocol through `subagent({action: "guide", options: {topic: "council"}})`, which reads the package copy, not this one; switching therefore also needs a local `/council` prompt (or the package prompt excluded) that loads this skill.

## Provenance

- `pi-subagents` 0.90.0 (npm; https://github.com/nicobailon/pi-subagents), MIT, © 2026 Nico Bailon — `skills/council-mode/SKILL.md` (sha256 `12d4b7f8e8e1cc1770e85f8c511a690b9f18b23bae3250149602c04ca7575943`) and `skills/council-mode/references/pass-contracts.md` (sha256 `f2eb16d989d4396e0fc3147ba2108db08e4e89b9020ab68629a86cb2957836a3`). License text kept in [LICENSE-upstream](LICENSE-upstream).

## Tests

`tests/scenario.md` — not yet run.

## Deploy targets

None yet. Planned: `scripts/deploy-local-skills.py` (shared bus, Pi, Claude Code) once the test passes and the package's copy is excluded in Pi's `packages` settings.
