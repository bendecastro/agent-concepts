---
test_kind: accuracy
test_status: pass
tested: 2026-08-21
deployed: yes
---
# Concept: bc-prd-drafting

Model-invoked discipline that drafts a PRD from the current conversation + codebase: synthesize (no interview), sketch and confirm the test seams, and write to the standard PRD template. Holds the reusable *writing* behavior; it does NOT publish. The user-invoked `bc-to-spec` wraps it with GitHub publication, and `bc-plan-to-pipeline` carries its output straight into slicing.

## Design decisions

- **Extracted from the then-named `to-prd` (refactor 2026-06-20; renamed `bc-to-spec` 2026-07-11).** Originally the whole PRD behavior lived inside the user-invoked publication orchestrator. It was split so `bc-plan-to-pipeline` can reuse the drafting behavior by inlining a *model-invoked* discipline rather than calling another user-invoked orchestrator (workspace composition boundary; see `bc-prompting-agents`). The former stateful grilling wrapper was removed 2026-09-27; `bc-grilling` + `bc-domain-modeling` remain directly usable.
- **The PRD template lives here, not in the orchestrator.** The template is part of the writing behavior; the orchestrator only publishes the produced doc. One home for the template means no drift between `bc-to-spec` and `bc-plan-to-pipeline`.
- **No interview, by contract.** Drafting synthesizes what's known; if scope is vague it points at `/bc-grilling` + `/bc-domain-modeling`. Keeps the user/model-invoked boundary and the skill single-purpose.
- **Seam-first.** Commits to test seams (prefer existing, highest, fewest — ideal one) and confirms them with the user *before* writing, tying PRDs to the `bc-codebase-design` vocabulary.
- **No file paths / code in the PRD.** They go stale fast; the one exception is a prototype-derived snippet that encodes a decision more precisely than prose.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) `captured-skills.md` — verbatim `to-prd` body and template; this discipline is the writing half of that skill, split out. https://github.com/mattpocock/skills/blob/main/skills/engineering/to-prd/SKILL.md
- AI Engineer Workshop 2026 (Matt Pocock) — workshop's `/write-a-prd` planning step.
- `concepts/bc-prompting-agents/body/SKILL.md` — composition boundary that motivates the split.

## Tests

`tests/accuracy-check.md` — verifies the body faithfully encodes the three behaviors (synthesize-not-interview, seam-check-before-write, template fidelity) and the no-publish boundary. Accuracy-checked 2026-08-21 **PASS** 5/5 against `body/SKILL.md`. Drafting is a writing discipline (low silent-failure risk); pressure-tested transitively via `bc-to-spec` and `bc-plan-to-pipeline`.

## Deploy targets

- Claude Code: `~/.claude/skills/bc-prd-drafting` → relative symlink to `body/`.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../docs/guides/harnesses.md`.
