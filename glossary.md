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
- **public skill** — a skill people outside this repository can install: any concept not marked `deployed: no`, except kernels; its name starts with `bc-`.
- **needed skills** — the other skills a skill refers to by name and that every install method installs with it.
- **install method** — one way to install the public skills into an agent: a Claude Code plugin, a Codex plugin, the Pi package, `npx skills`, or the contributors' clone-and-link script. Use one per agent.
- **release** — a tagged version of the public skills (`vMAJOR.MINOR.PATCH`) that install methods point at; never `master`.
- **fresh-install test** — the CI check that installs with each install method into an empty home folder and checks what a stranger would find.

- **work data** — the records about work items that a dashboard can read: stage, steps, who holds an item, its history, review and gate results, and time and cost; the work index script prints them as JSON.
- **Held by line** — the `Held by:` line in a work item naming the agent working on it and since when; written when the agent starts and removed when it stops.
- **Spent line** — the `Spent:` line in a finished work item's Outcome giving its estimated time, tokens and cost, read from the agent tools' session files.

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
- **drain** — an unattended run that works through the eligible tickets (ready work items or issues) one by one until none are left or a stop condition fires.
- **claim** — the marker an agent sets on a ticket before working on it, so no other agent takes it: a claim branch on the Git remote, or, with no remote, the committed move of the work item to the active folder.
- **Ready for agent** — the line `Ready for agent: yes` in a work item: the owner's consent that an unattended drain may build it; written only when every step states its done-criteria and what is out of scope.
- **Waiting on owner** — the line `Waiting on owner: <question>` in a parked work item: the decision a drain needs before it can continue; the item loses its ready line until the owner answers.
- **rework** — fixing the defects a gate or review sent back.
- **landing** — the final merge, push and close of reviewed work, done by the run's driver.
- **PRD** — a product requirements document: what to build and why, written before the work is split into slices (bc-prd-drafting).
- **ADR** — an architecture decision record: a short note of one design decision and its reasons, kept in `docs/decisions/` (bc-domain-modeling).
- **preflight** — the checks and owner decisions made before an unattended run starts (bc-pipeline-to-done).

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
- **driver** — the agent that runs a drain: it claims tickets, sends them to workers and reviewers, and does the landing (bc-pipeline-to-done).
- **orchestrator** — a skill the owner starts that runs a sequence of other skills, such as bc-plan-to-pipeline or bc-pipeline-to-done.
- **council** — a group of read-only advisors whose findings the parent weighs.
- **advisor** — one member of a council: a read-only subagent, ideally on its own model, whose profile name starts with `council-` (bc-council-mode).
- **worktree** — a separate checkout of the repository where a worker makes changes without touching the main one.

## Code design and testing

- **module** — anything with an interface and an implementation, at any scale: a function, a class, a package or a slice across layers (bc-codebase-design). _Avoid_: unit, component, service.
- **interface** — everything a caller must know to use a module correctly: its types, but also its rules, ordering, errors, required settings and performance (bc-codebase-design). _Avoid_: API, signature.
- **depth** — how much behaviour a caller or test gets per piece of interface it has to learn; a **deep module** hides a lot of behaviour behind a small interface (bc-codebase-design).
- **shallow module** — a module whose interface is nearly as complex as its implementation, close to a pass-through (bc-codebase-design).
- **seam** — a place where behaviour can be changed without editing at that place; where a module's interface sits (bc-codebase-design). _Avoid_: boundary.
- **adapter** — a concrete thing that fills an interface at a seam; the word names its role, not what is inside it (bc-codebase-design).
- **test level** — one of three kinds of testing a change must account for: example tests, property-based tests and formal verification (bc-tdd).
- **property-based test** — a test that states a rule that must always hold and lets a tool try many generated inputs to break it; Level 2 (bc-tdd).
- **formal verification** — a machine-checked proof that code meets its rule for every input; Level 3, off unless the owner turns it on for a component (bc-tdd).

## Design consistency

- **design framework** — the method that lets short-lived agents build a project's interface consistently without the owner re-deciding the same things: tokens, design pages, checks and screenshot review.
- **design token** — a named value (a colour, size or spacing) defined once and used everywhere by name, never typed in as a literal.
- **design page** — a page in the project's `docs/design/` stating the current design choice on one topic, and whether the owner or an agent made it.
- **capture rule** — the hard rule that a visible change is not done until screenshots of every surface it reaches are taken and critiqued against the screenshot checklist.

## Performance guardrails

- **guardrail** — an automated check that stops a quality, such as speed, from getting worse.
- **fitness function** — a guardrail for a property of the system's design or architecture, such as "the UI layer never calls the database"; the industry term.
- **performance budget** — a fixed limit on a speed or size measure, such as time per frame or download size.
- **hot path** — the code that runs so often (for example every frame) that small costs there add up.
- **baseline** — the measured value that later measurements are compared against.
- **ratchet** — a check that accepts existing shortfalls but rejects anything worse, and tightens its baseline after a real improvement.
- **budget decomposition** — splitting a user-facing target, such as time per frame, into smaller allowances for each step that shares it.
- **guardrails page** — a project's `docs/guardrails/README.md`: its targets, limits and checks, each marked as the owner's or an agent's choice.
- **noise** — the natural variation between repeated measurements of the same thing.
- **measurement harness** — the repeatable setup that runs a measurement the same way each time; not the same thing as an agent's harness.
