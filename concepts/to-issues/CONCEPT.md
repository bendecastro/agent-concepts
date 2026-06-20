# Concept: to-issues

User-invoked orchestrator that breaks a plan/spec/PRD into independently-grabbable **GitHub issues** using tracer-bullet vertical slices, quizzing the user on granularity and dependencies before publishing with the `ready-for-agent` label.

## Design decisions

- **GitHub tracker baked in** (user's decision), same rationale as `to-prd`: `gh` + `ready-for-agent`, no `setup-matt-pocock-skills` indirection. Publishing happens in dependency order so real issue numbers can fill "Blocked by".
- **Vertical slices, not horizontal.** The core discipline: each issue cuts end-to-end through every layer (schema/API/UI/tests) and is independently demoable — the "tracer bullet" from the workshop. Horizontal slices (one layer at a time) are the named anti-pattern, shared with `tdd`.
- **Prefactor first.** "Make the change easy, then make the easy change" — prefactoring is its own first slice.
- **Quiz before publish.** The user approves the breakdown (granularity + dependency graph) before any issues are created; avoids publishing a wrong slicing that then has to be reworked across many issues.
- **Never touch the parent issue.** Explicit guard against closing/modifying the source issue.

## Provenance

- `raw/pocock-skills-upstream/captured-skills.md` — verbatim `to-issues` body and template. https://github.com/mattpocock/skills/blob/main/skills/engineering/to-issues/SKILL.md
- `raw/AI Engineer Workshop 2026.md` — workshop's `/prd-to-issues` step and the tracer-bullet framing.

## Tests

`tests/scenario.md` — verifies vertical (not horizontal) slicing, the quiz-before-publish step, dependency-ordered publication with real `#NN` references, and the no-touch-parent guard. Process orchestrator; scenario authored, full pressure run pending.

## Deploy targets

- Claude Code: `~/.claude/skills/to-issues` → relative symlink to `body/`.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../harnesses.md`.
