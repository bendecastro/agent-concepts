---
test_kind: pressure
test_status: pass
tested: 2026-07-16
deployed: yes
---
# Concept: bc-to-spec

User-invoked orchestrator that turns the current conversation + codebase understanding into the project’s PRD-format spec and publishes it as a **GitHub parent issue**. No interview — pure synthesis of what's already been discussed; resolve vague scope with `bc-grilling` + `bc-domain-modeling` first. The parent PRD is a coordination artifact; `ready-for-agent` is reserved for implementation slices.

## Design decisions

- **Thin wrapper over `bc-prd-drafting` (refactor 2026-06-20).** The PRD writing behavior — synthesize-not-interview, seam-first, the template, no-stale-specifics — was extracted into the model-invoked `bc-prd-drafting` discipline so `bc-plan-to-pipeline` can reuse it without orchestrator-calls-orchestrator. `bc-to-spec` is now: run `/bc-prd-drafting` → publish. The former `/to-prd` compatibility alias was removed 2026-09-27. Behavior preserved, relocated.
- **GitHub tracker baked in** (user's decision). Upstream defers the tracker vocabulary to a `setup-matt-pocock-skills` configuration step; we hard-wire GitHub via `gh` so there's no per-repo setup skill to port. Parent PRDs are intentionally not `ready-for-agent`; switching trackers later means editing the publish step in this body.
- **No interview, by contract.** `bc-to-spec` deliberately doesn't grill — use `bc-grilling` + `bc-domain-modeling` first when scope is vague. The stateful `grill-me` wrapper was removed 2026-09-27; the underlying disciplines remain directly usable.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) `captured-skills.md` — original `to-prd` body and template (the writing half now lives in `bc-prd-drafting`).
- Matt Pocock upstream `skills/engineering/to-spec/SKILL.md` at `391a2701dd948f94f56a39f753f8eea9a859c87` — current public name and behavior. https://github.com/mattpocock/skills/blob/391a2701dd948f94f56a39f753f8eea9a859c87/skills/engineering/to-spec/SKILL.md
- AI Engineer Workshop 2026 (Matt Pocock) — workshop's `/write-a-prd` planning step.
- `concepts/bc-prd-drafting/` — the extracted drafting discipline this orchestrator wraps.

## Tests

`tests/scenario.md` — process scenario verifying no-interview synthesis, seam-check-before-write, the template sections, and unlabeled `gh issue create` PRD-parent publication. Process orchestrator (lower silent-failure risk than the gate skills); pressure-tested 2026-07-16 **PASS** (Grok).

## Deploy targets

- Canonical deploy: `bc-to-spec`; the former `to-prd` compatibility alias was removed 2026-09-27.
- Claude Code: `~/.claude/skills/bc-to-spec` → relative symlink to `body/`.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../docs/guides/harnesses.md`.
