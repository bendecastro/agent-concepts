---
test_kind: pressure
test_status: partial # project paths looked up by role 2026-11-12 (visible layout); not yet pressure-tested
tested: 2026-08-21
deployed: 2026-06-21
---
# Concept: triage

User-invoked intake gate for the bc loop. It moves issues/PRs through a small state machine, verifies claims, grills when needed, writes drain-ready Agent Briefs, and records rejected enhancement concepts with their reason in the project's work-dropped folder (`.bc-agent/out-of-scope/` in projects without a "Where things go" table).

## Design decisions

- **Intake, not execution.** `triage` produces better work for `bc-plan-to-issues` or `bc-drain-issues`; it does not build the feature itself.
- **Agent Brief as AFK contract.** A `ready-for-agent` label alone is too weak. The latest Agent Brief comment is the spec the drain subagent can rely on.
- **Out-of-scope is project memory.** Rejections belong in the work-dropped folder only when they are durable enhancement decisions, not temporary deferrals or already-built features.
- **qmd-assisted prior-art check, gated on a covering global collection.** The redundancy/prior-rejection step uses `qmd query` when qmd is installed and a global collection covers the repo's vault (`qmd collection list` path match), because semantic search catches prior ADRs/rejections that exact-name greps miss; with no coverage the manual reading path is unchanged. See `concepts/qmd/` (added 2026-07-13; global-mode rework same day).
- **Project paths are looked up by role (2026-11-12).** The body names the glossary, decisions, work-dropped and ideas roles and resolves them in the project's "Where things go" table in `.bc-agent/AGENTS.md`; without a table it uses the paths it used before (`.bc-agent/project/overview.md` Glossary or `glossary.md`, `.bc-agent/decisions/` or `docs/adr/`, `.bc-agent/out-of-scope/`). With a table a rejection is a numbered work item in work-dropped with the reason under `## Outcome`, created only from the main checkout, and a repeat request is added to the existing item's prior requests. A missing `planning-workflow.md` means canonical labels. In a hybrid project the glossary is shared with `teach`; the body points to `domain-modeling`'s shared-glossary rule rather than restating it (W3 review, 2026-11-12). A rejection found from a worktree is an ideas line, and the issue stays open until the dropped item exists, so the reason cannot survive only as that line. Provenance: decisions 8, 10–12, 20 and 25 in [the bc-init-agent visible-layout plan](../../docs/plans/implemented/bc-init-agent-visible-layout.md).
- **State labels stay canonical but mappable.** The body uses Pocock's five-state vocabulary while allowing repo-local mappings from the bc scaffold.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) — upstream Matt Pocock `triage`, `AGENT-BRIEF.md`, and `OUT-OF-SCOPE.md` captured 2026-06-21.
- `concepts/bc-drain-issues/` — Agent Brief requirements are tightened so drainable issues are self-contained.
- `concepts/grilling/` and `concepts/domain-modeling/` — used when triage needs to resolve missing decisions.

## Tests

`tests/scenario.md` — pressure scenario for issue intake: it must not mark vague issues ready, must write an Agent Brief for drainable issues, and must use the work-dropped folder (`.bc-agent/out-of-scope/` without a table) only for rejected enhancements. A second scenario (added 2026-11-12, not yet run) checks that a visible-layout project records the reason when a request is dropped. Pressure-tested 2026-08-21 **PASS 5/5** (Pi/Grok 4.6; stub `gh`; also closed the already-implemented fixture gap — #14 `wontfix` without poisoning out-of-scope).

## Deploy targets

- Claude Code: `~/.claude/skills/triage` → relative symlink to `body/` (deployed 2026-06-21).
- Pi: `~/.agents/skills/triage` and `~/.pi/agent/skills/triage` → relative symlinks to `body/` (deployed 2026-06-21).
- Other harnesses: manual bootstrap until tested.
