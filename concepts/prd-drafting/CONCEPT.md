# Concept: prd-drafting

Model-invoked discipline that drafts a PRD from the current conversation + codebase: synthesize (no interview), sketch and confirm the test seams, and write to the standard PRD template. Holds the reusable *writing* behavior; it does NOT publish. The user-invoked `to-prd` wraps it with GitHub publication, and `bc-plan-to-issues` carries its output straight into slicing.

## Design decisions

- **Extracted from `to-prd` (refactor 2026-06-20).** Originally the whole PRD behavior lived inside the user-invoked `to-prd`. It was split so the planning orchestrator `bc-plan-to-issues` can reuse the drafting behavior by inlining a *model-invoked* discipline rather than calling another user-invoked orchestrator (workspace composition boundary; see `prompting-agents`). Mirrors how `grilling`/`domain-modeling` back `grill-me`.
- **The PRD template lives here, not in the orchestrator.** The template is part of the writing behavior; the orchestrator only publishes the produced doc. One home for the template means no drift between `to-prd` and `bc-plan-to-issues`.
- **No interview, by contract.** Drafting synthesizes what's known; if scope is vague it points at `/grill-me`. Keeps the user/model-invoked boundary and the skill single-purpose.
- **Seam-first.** Commits to test seams (prefer existing, highest, fewest — ideal one) and confirms them with the user *before* writing, tying PRDs to the `codebase-design` vocabulary.
- **No file paths / code in the PRD.** They go stale fast; the one exception is a prototype-derived snippet that encodes a decision more precisely than prose.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) `captured-skills.md` — verbatim `to-prd` body and template; this discipline is the writing half of that skill, split out. https://github.com/mattpocock/skills/blob/main/skills/engineering/to-prd/SKILL.md
- [AI Engineer Workshop 2026.md](https://www.aihero.dev/ai-engineer-workshop-2026~dwnll) — workshop's `/write-a-prd` planning step.
- `concepts/prompting-agents/body/SKILL.md` — composition boundary that motivates the split.

## Tests

`tests/accuracy-check.md` — verifies the body faithfully encodes the three behaviors (synthesize-not-interview, seam-check-before-write, template fidelity) and the no-publish boundary. Drafting is a writing discipline (low silent-failure risk); pressure-tested transitively via `to-prd` and `bc-plan-to-issues`.

## Deploy targets

- Claude Code: `~/.claude/skills/prd-drafting` → relative symlink to `body/`.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../harnesses.md`.
