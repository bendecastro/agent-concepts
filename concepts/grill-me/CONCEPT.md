---
test_kind: pressure
test_status: pass
tested: 2026-06-20
deployed: yes
---
# Concept: grill-me

User-invoked orchestrator for a planning/design grilling session that is **always stateful**: it runs the `/grilling` loop and persists the resolved vocabulary and hard decisions into `CONTEXT.md` + ADRs as it goes, via `/domain-modeling`.

## Design decisions

- **Merged the two upstream orchestrators into one always-stateful skill** (user's decision). Pocock ships a stateless `grill-me` (just "run `/grilling`") plus a separate `grill-with-docs` (`/grilling` + `/domain-modeling`). The user asked for `grill-me` *itself* to be stateful, so we collapsed to a single skill that always writes docs, dropping the stateless variant. Trade-off accepted: no built-in lightweight no-files mode — recovered via an explicit "throwaway session" escape hatch in the body.
- **Persistence is inline, not batched.** Docs are written as decisions crystallize during the interview, matching `domain-modeling`'s "don't batch" rule; batching to the end loses the decisions made early.
- **Workspace guard.** Like `teach`, the body guards against writing project docs into an inappropriate directory (empty scratch dir / unrelated files) — confirm or grill without persisting.
- **Composition boundary respected.** `grill-me` (user-invoked) invokes only model-invoked skills (`grilling`, `domain-modeling`), never another user-invoked orchestrator.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) `captured-skills.md` — verbatim `grill-me` and `grill-with-docs` bodies; this concept is the deliberate merge of the two. https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md and https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md
- [AI Engineer Workshop 2026.md](https://www.aihero.dev/ai-engineer-workshop-2026~dwnll) — workshop names `/grill-me` as the first planning step (stress-test vague requirements).
- [skillsskillsproductivityteach at main.md](https://github.com/mattpocock/skills/tree/main) — catalog: grilling + shared-language (`CONTEXT.md`/ADRs) as the cure for misalignment and verbosity.

## Tests

`tests/pressure-grill-me.md` — exercises the grilling gate **and** the persistence behavior (CONTEXT.md is a pure glossary; ADR only at the three-part bar; inline not batched; workspace guard). This is the centerpiece pressure test; it transitively validates `grilling` and `domain-modeling`. **Run 2026-06-20** against a general-purpose subagent in a throwaway notes-app repo: all gates held, verified by file inspection — one-question gate held under batch/hurry pressure; `CONTEXT.md` stayed a pure glossary (rejected `query_json`/`created_at`/table-row leak); single ADR only for the load-bearing server-storage decision (trivial button-color ADR refused); docs written inline not batched; no code written while branches open (`src/` untouched).

## Deploy targets

- Claude Code: `~/.claude/skills/grill-me` → relative symlink to `body/`. Deploy only after the pressure test holds.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../docs/harnesses.md`.
