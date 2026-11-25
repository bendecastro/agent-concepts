# Agent Skill Map

Date: 2026-11-25

The bc loop skills are canonical in `$AGENT_CONCEPTS/concepts/<skill>/body/SKILL.md`
and are normally deployed into `~/.pi/agent/skills/<skill>` and `~/.agents/skills/<skill>`
via symlink. Do not vendor/copy their bodies into this repo; use this page as the repo-local
map so agents know what to invoke.

## Planning/execution loop

- `/bc-plan-to-pipeline` — interactive planning front: grill → domain capture → PRD → issue slices.
- `/bc-drain-issues` — AFK executor for `ready-for-agent` issue queues.
- `/improve-codebase-architecture` — optional architecture runway before planning/slicing.

## Supporting skills used by the loop

- Intake/evidence: `/triage`, `/prototype`.
- Planning disciplines: `grilling`, `domain-modeling`, `prd-drafting`, `plan-slicing`, `codebase-design`.
- Source-tree docs: `codebase-docs` — README files, other `docs/` pages and JSDoc; not `.bc-agent/` and not the paths named in the "Where things go" table in `.bc-agent/AGENTS.md`, which are records.
- Execution disciplines: `tdd`, `diagnosing-bugs`, `bc-autoresearch-loop`.

## Agent behavior

If the user's request sounds like planning future codebase work, ask whether to enter
`/bc-plan-to-pipeline` before implementing. Offer `/improve-codebase-architecture` first when
the main uncertainty is architecture/seams. Run the computed check in
`conventions/architecture-runway.md` and give the optional architecture-runway nudge when its
planning-surface signal reaches the threshold.
