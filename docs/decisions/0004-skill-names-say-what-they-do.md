# 0004: Skill names say what they do

Date: 2026-11-25
Status: accepted

## Context

Some public skill names made sense only to someone who already knew the skill: `bc-swarm`, `bc-show-me`, `bc-autoresearch-loop`, `bc-init-agent` and `bc-guardrails` do not tell a newcomer what they get, `bc-reflect` does not say that its point is improving how the agent works, and `bc-council-improve-codebase` does not say what it improves. A newcomer picks a skill from a list of names, so a name they cannot guess is a skill they do not use.

## Decision

Seven skills are renamed, chosen by the owner:

| Old name | New name |
| --- | --- |
| `bc-reflect` | `bc-self-improve` |
| `bc-swarm` | `bc-delegate-investigation` |
| `bc-autoresearch-loop` | `bc-optimize-code` |
| `bc-show-me` | `bc-explain-visually` |
| `bc-init-agent` | `bc-setup-project` |
| `bc-council-improve-codebase` | `bc-council-improve-architecture` |
| `bc-guardrails` | `bc-performance-guardrails` |

The rule for naming a skill: a skill you run is named verb-object (what it does to what); a reference skill names its topic; a widely known term is kept even when it is not verb-object. So `bc-grilling`, `bc-unslop` and `bc-tdd` stay because the terms are known, and `bc-pipeline-to-done`, `bc-plan-to-pipeline`, `bc-to-spec` and `bc-to-tickets` stay because each already says what it turns into what. The council convention (`bc-council-<verb-object>`, in `AGENTS.md`) still holds.

## Consequences

- Release 0.2.0 carries the new names. The old names stay as aliases only on installs made with `scripts/deploy-local-skills.py`; plugin, Pi package and `npx skills` users must switch to the new names.
- Every current reference changes; historical records (past log entries, finished work items, dated test results, research evidence) keep the old names.
- Private overlays are looked up by skill name (`overlays/<skill-name>.md`), so an overlay for a renamed skill must be renamed to be read.
- `bc-delegate-investigation` keeps its run folder under `~/.local/state/bc-swarm/`, so tools that sweep or read those folders keep working.

## Alternatives considered

- Keep the names and explain them in the README: the name is what a newcomer sees in a skill list, so the explanation arrives too late.
- Rename every skill to verb-object: well-known terms such as `bc-tdd` are clearer than any longer description.
