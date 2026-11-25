# Requirements: guardrails method

## Problem

Short-lived agents make a project slower, bigger or more tangled one change at a time, and nothing
stops them: a project has tests for behaviour but no agreed limits for speed or size and no checks
for its structure. Each agent re-decides (or never decides) what "fast enough" means. The design
framework already solves the same problem for how an interface looks; nothing does it for speed,
size or structure.

## Solution

A new `guardrails` concept (a skill agents load on demand) holding one method for every guardrail:
performance budgets, fitness functions (checks for a structural property) and the ratchet. Each
project keeps a `docs/guardrails/README.md` page listing its targets, budgets and checks; the
checks themselves run inside the project's existing `scripts/gate`. Performance is the first and
most detailed section. Agents set limits themselves and record them as their own choice, which
the owner may change.

## User stories

1. As the owner, I want every project's speed, size and structure limits written on one page, so I can see and change them without reading code.
2. As the owner, I want agents to set limits without asking me, so guardrails appear without my effort, and to mark each limit as the agent's choice, so I know which ones I may want to change.
3. As an agent, I want to know where a rule belongs (a lint rule, an artifact check or a timing test), so I add the cheapest check that catches the problem.
4. As an agent, I want a way to set a limit from today's measurement that tolerates measurement noise, so the check neither flaps nor lets real slowdowns through.
5. As an agent fixing a speed, size or structure regression, I want to add a check that catches it in the same change, so the same mistake cannot come back.
6. As an agent setting up a project, I want to add checks for well-known problems of the project's stack, so common mistakes are caught before they happen.
7. As an agent in an older project, I want to copy the empty page in when it is missing, so guardrail work does not need a full re-scaffold.
8. As an agent running an improvement loop (`bc-autoresearch-loop`), I want to measure the same way the guardrails do, so a kept improvement tightens the right limit.

## Requirements

- The skill SHALL trigger when an agent sets or changes a speed, size, memory or structure limit; adds or changes a check protecting such a property; fixes a regression in one; or sets up a project's guardrails.
- The method SHALL classify each check as static (inspects source or settings), artifact (measures a built output without running the program) or dynamic (runs the program and measures), and say to prefer the cheapest kind that reliably catches the problem.
- Without an existing limit, the agent SHALL measure today's value with enough repeated runs to estimate noise, set the limit at that value plus a noise allowance, and fail anything worse (ratchet). After a verified improvement it SHALL tighten the limit.
- User-facing targets (for example time per frame, page load, interaction delay) SHALL be set by the agent from published guidelines, citing the source on the page; the method SHALL name a few well-sourced defaults (RAIL frame budget, Core Web Vitals) from `docs/research/2026-11-25-performance-guardrails/`. A target can be split into smaller per-step allowances (budget decomposition).
- Every limit and check SHALL be recorded on `docs/guardrails/README.md` with the measure, the limit, its source and who chose it (agent or owner), in the same commit as the check that enforces it. An agent SHALL NOT change a limit the owner chose without asking.
- After fixing a speed, size or structure regression that a check could catch, the agent SHALL add that check in the same change and mention it in one line of its report.
- At project setup, and when it first adds the page, the agent SHALL add checks for well-known, well-sourced problems of the project's stack (for example blocking I/O in an Electron main process, bundle size for a web app), each ratcheted so existing shortfalls do not fail the gate; it SHALL NOT add checks for problems it cannot name a source or a past bug for.
- Fitness functions SHALL follow the same page and ratchet rules; design-consistency checks stay on the project's design page (`docs/design/README.md`), and the guardrails page links to it rather than copying them.
- `bc-init-agent` SHALL create an empty `docs/guardrails/README.md` (sections: targets, budgets, checks, where a rule lives, how to measure) and a `.bc-agent/map.md` line routing guardrail work to it, for the same archetypes that get `docs/design/README.md`; it SHALL NOT create any measuring script.
- In a project without the page, the agent SHALL copy the page text from `bc-init-agent`'s scaffold in its own commit the first time guardrail work comes up.
- `bc-autoresearch-loop` SHALL point to the guardrails skill for measuring and noise, and a kept improvement SHALL tighten the matching limit on the page.

## Out of scope

- A shared benchmark tool or measuring script in the scaffold.
- Telemetry from real users' devices.
- Adding the page to existing projects in a sweep.
- Renaming other uses of "gate".

## Testing

Pressure test per `AGENTS.md`'s test rule, on the configured pressure-test model, without and with
the concept. Scenarios: an agent fixing a slowdown who is told "just fix it, no time for a check";
an agent asked to set a budget who is tempted to ask the owner or invent a number without
measuring; an agent tempted to change an owner-chosen limit to make a failing check pass. Scaffold
changes get unit tests in `concepts/bc-init-agent/tests/` like the design README's.

## Decisions (grill, 2026-11-25)

General method rather than performance only; its own concept, with the page from `bc-init-agent`;
the agent sets all limits (measured ratchet by default, user-facing targets from published
guidelines) and records them as its choice; the scaffold adds only the empty page; existing
projects get the page on first need; checks are added both at setup for well-known stack problems
and after each fixed regression.
