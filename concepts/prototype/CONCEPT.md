---
test_kind: pressure
test_status: partial # writeup home changed to the research role 2026-11-12; not yet pressure-tested
tested: 2026-08-21
deployed: 2026-06-21
---
# Concept: prototype

User-invoked throwaway exploration step for design uncertainty: build a small runnable artifact for logic/state or UI direction, record the answer, then delete or absorb it before production implementation.

## Design decisions

- **Question-first.** The artifact shape follows the question; otherwise prototypes become mini-features.
- **Feeds planning, not drain.** Prototype verdicts become PRD/ADR/issue context; prototype code should not become unattended execution scope unless explicitly absorbed.
- **No polish by design.** Tests and abstractions are intentionally omitted to preserve speed and throwaway semantics.

- **Writeup goes to the research role (2026-11-12).** The prototype writeup is a dated `<date>-prototype-<slug>/` folder in the research role from the project's "Where things go" table, with decisions and requirements roles for verdicts and product-level requirements. Without a table, the earlier homes (`.bc-agent/project/<feature>-notes.md`, an ADR, the PRD) stay as the fallback. The folder-name pattern mirrors the table's `<date>-<slug>/` research convention; the `prototype-` prefix is a choice made here so prototype writeups are recognisable among other research. Expected behaviour 5 in `tests/scenario.md` covers it and has not been run. Source: [visible-layout plan](../../docs/plans/implemented/bc-init-agent-visible-layout.md), decision 20. The table and its role keys are the contract of `bc-init-agent` (see its `CONCEPT.md`, "Interface").
- **A place the user names wins; the skill recommends and offers (owner decision 2026-11-12).** When the user explicitly names another place for the writeup (for example a scratch folder), the skill follows the user, says the research role is where later work will look, and offers to move it. It does not claim to enforce the research role. Why: three pressure rounds showed the model following the user's explicit path over stronger wording each time ([results](../bc-init-agent/tests/pressure-dependent-skills-results-2026-11-12.md)); the deterministic backstop is `bc-wiki-maintain`'s lint, which reports any non-mechanics entry under `.bc-agent/` (such as `scratch/`) in a visible-layout project. Replaced the earlier "research role only, no copy in the named place" sentence.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) — upstream Matt Pocock `prototype/SKILL.md` captured 2026-06-21.
- `concepts/bc-plan-to-issues/` — optional pre-PRD evidence step when grilling exposes design uncertainty.

## Tests

`tests/scenario.md` — pressure scenario: chooses the right branch, marks artifacts throwaway, captures the verdict, and does not leave prototype code disguised as production. Pressure-tested 2026-08-21 **PASS 4/4** (Pi/Grok 4.6; naive consumers, parent-launched because runners have no `subagent` tool). Check 2 (UI variants) was the 2026-06-21 gap and held.

## Deploy targets

- Claude Code: `~/.claude/skills/prototype` → relative symlink to `body/` (deployed 2026-06-21).
- Pi: `~/.agents/skills/prototype` and `~/.pi/agent/skills/prototype` → relative symlinks to `body/` (deployed 2026-06-21).
- Other harnesses: manual bootstrap until tested.
