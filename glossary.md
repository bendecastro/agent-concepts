# Glossary

Canonical names for this project's domain concepts: one line each, no implementation
detail. Use these terms in code, issues and docs. "Avoid" names a word not to use for the
same meaning.

## Concepts and deployment

- **concept** — one unit of agent guidance kept in this repository, with its design reasons, sources and instruction text; the only thing that gets edited.
- **skill** — a concept's instructions as an agent loads them on demand, once deployed. _Avoid_: calling the source unit a skill.
- **kernel** — a concept whose instructions are injected into every session rather than loaded on demand.
- **body** — the part of a concept an agent actually reads; the rest of the concept explains and tests it.
- **raw source** — an article, note or file filed as evidence; never edited once filed.
- **inbox** — the raw sources filed but not yet ingested.
- **ingest** — read a raw source with the owner, carry its useful ideas into concepts, and mark it as taken up.
- **provenance** — the sources a concept's design decisions come from, named in the concept.
- **deploy** — make a concept visible to agents, by linking its body where they look for skills.
- **harness** — the program that runs an agent and decides which tools and files it can see (for example Pi, Claude Code, OpenCode). _Avoid_: agent, for the program.
- **private concept** — a concept kept outside this repository because it cannot be published; it overrides a public concept of the same name.
- **overlay** — an optional private file that adds the owner's own tool names to a public skill; it adds no rules.

## Gates, checks and rules

- **gate** — an automated command that must pass before work counts as done, such as the project's full gate. _Avoid_: gate, for a rule an agent must follow (say hard rule).
- **check** — one automated test of a single property; a gate runs many checks.
- **hard rule** — a rule with a higher bar for change because breaking it is most tempting exactly when it blocks you (canon, provenance, test, immutability, capture and recovery rules). _Avoid_: gate.
- **static check** — a check that inspects source or settings without running the program.
- **artifact check** — a check that measures a built output, such as download size, without running the program.
- **dynamic check** — a check that runs the program and measures what happens.
- **pressure test** — running an agent against scripted temptations to break a concept's rules, once without the concept and once with it, to see whether the concept holds.
- **lint** — this repository's check for mechanical drift, such as broken links, missing sources or stale status pages.

## Tickets and work

- **ticket** — one unit of work in any tracker. Use it in text that does not depend on which tracker.
- **work item** — a ticket in the project's own `work/` folders; its folder is its status.
- **issue** — a ticket on GitHub. _Avoid_: issue, in text that works with any tracker (say ticket).
- **slice** — one thin piece of a plan that works end to end on its own; it becomes a step of a work item, a ticket, or both.
- **drain** — a run that works through the eligible issues one by one until none are left or a stop condition fires.
- **claim** — the marker an agent sets on an issue before working on it, so no other agent takes it.
- **rework** — fixing the defects a gate or review sent back.
- **landing** — the final merge, push and close of reviewed work, done by the run's driver.

## Agents and runs

- **agent** — an AI model working through a harness on a task. _Avoid_: harness, for the agent.
- **parent** — the agent that sends work to other agents and keeps decisions, integration and verification.
- **subagent** — an agent started by a parent to do one task and report back. _Avoid_: child (an accepted synonym; prefer subagent).
- **role** — the kind of job a subagent is given, such as scout, worker or reviewer.
- **worker** — the implementation role: the subagent that changes files. _Avoid_: worker, for any subagent.
- **scout** — the read-only role that maps code or files and reports with evidence anchors.
- **swarm** — working with many subagents in parallel under rules that keep their results recoverable.
- **track** — one independent piece of work that can be given to one subagent.
- **routing decision** — the point where the parent lists every track and names the role, model and thinking level each goes to. _Avoid_: the tooth.
- **evidence anchors** — a file path plus the quoted line that supports each claim a subagent returns. _Avoid_: thin-parent guard.
- **run folder** — the folder holding one swarm run's manifest and artifacts; disposable. _Avoid_: run directory.
- **manifest** — the run folder's list of tracks: who does each, where its artifact goes, and what happened to it.
- **artifact** — the file a subagent writes its result to as it goes; the durable record of that result.
- **packet** — the written task given to a subagent: scope, goal, limits, evidence wanted and output format.
- **council** — a group of read-only advisors whose findings the parent weighs.
- **worktree** — a separate checkout of the repository where a worker makes changes without touching the main one.

## Performance guardrails

- **guardrail** — an automated check that stops a quality, such as speed, from getting worse.
- **fitness function** — a guardrail for a property of the system's design or architecture, such as "the UI layer never calls the database"; the industry term.
- **performance budget** — a fixed limit on a speed or size measure, such as time per frame or download size.
- **hot path** — the code that runs so often (for example every frame) that small costs there add up.
- **baseline** — the measured value that later measurements are compared against.
- **ratchet** — a check that accepts existing shortfalls but rejects anything worse, and tightens its baseline after a real improvement.
- **noise** — the natural variation between repeated measurements of the same thing.
- **measurement harness** — the repeatable setup that runs a measurement the same way each time; not the same thing as an agent's harness.
