# Concept: triage

User-invoked intake gate for the bc loop. It moves issues/PRs through a small state machine, verifies claims, grills when needed, writes drain-ready Agent Briefs, and records rejected enhancement concepts in `.bc-agent/out-of-scope/`.

## Design decisions

- **Intake, not execution.** `triage` produces better work for `bc-plan-to-issues` or `bc-drain-issues`; it does not build the feature itself.
- **Agent Brief as AFK contract.** A `ready-for-agent` label alone is too weak. The latest Agent Brief comment is the spec the drain subagent can rely on.
- **Out-of-scope is project memory.** Rejections belong in `.bc-agent/out-of-scope/` only when they are durable enhancement decisions, not temporary deferrals or already-built features.
- **qmd-assisted prior-art check, gated on a covering global collection.** The redundancy/prior-rejection step uses `qmd query` when qmd is installed and a global collection covers the repo's vault (`qmd collection list` path match), because semantic search catches prior ADRs/rejections that exact-name greps miss; with no coverage the manual reading path is unchanged. See `concepts/qmd/` (added 2026-07-13; global-mode rework same day).
- **State labels stay canonical but mappable.** The body uses Pocock's five-state vocabulary while allowing repo-local mappings from the bc scaffold.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) — upstream Matt Pocock `triage`, `AGENT-BRIEF.md`, and `OUT-OF-SCOPE.md` captured 2026-06-21.
- `concepts/bc-drain-issues/` — Agent Brief requirements are tightened so drainable issues are self-contained.
- `concepts/grilling/` and `concepts/domain-modeling/` — used when triage needs to resolve missing decisions.

## Tests

`tests/scenario.md` — pressure scenario for issue intake: it must not mark vague issues ready, must write an Agent Brief for drainable issues, and must use `.bc-agent/out-of-scope/` only for rejected enhancements. Scenario authored; full harness run pending.

## Deploy targets

- Claude Code: `~/.claude/skills/triage` → relative symlink to `body/` (deployed 2026-06-21).
- Pi: `~/.agents/skills/triage` and `~/.pi/agent/skills/triage` → relative symlinks to `body/` (deployed 2026-06-21).
- Other harnesses: manual bootstrap until tested.
