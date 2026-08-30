#!/usr/bin/env python3
"""Scaffold a project-local .bc-agent wiki + root AGENTS.md for the grill→issues→drain workflow.

Creates a generalized project-local Markdown/Obsidian wiki schema at `.bc-agent/`
(no per-project nesting), with TODO stubs (validation, file-layout, paths) that the
project's first agents fill in. This follows the user's broader agent-maintained
wiki pattern: durable local context, explicit provenance, live task state, decisions,
and executable plans. NO root CONTEXT.md — the glossary lives in the vault
(project/overview.md), ADRs in decisions/, plans/PRDs in project/, and
conventions/planning-workflow.md is the adapter that redirects planning persistence
into the vault.

Idempotent and additive: creates only the files that are missing and leaves every
existing file untouched, so it is safe to re-run and safe to plug into a project
that already has files (including a hand-written root AGENTS.md). It NEVER deletes
anything. Existing files are overwritten only when explicitly forced: --force for
vault files, --force-root for the root AGENTS.md. --dry-run reports without writing.

Usage:
  scaffold.py --root <repo-root> --slug <project-name> [--date YYYY-MM-DD]
              [--archetype code|ops|learning|knowledge|hybrid]
              [--force] [--force-root] [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as _dt
from pathlib import Path

SLUG = "__SLUG__"
DATE = "__DATE__"


# --- root AGENTS.md (project root, points agents at the vault) ----------------
ROOT_AGENTS = """# Agent instructions for __SLUG__

This project has a local, project-scoped agent wiki at `.bc-agent/`.

Before making non-trivial changes, first read:

1. `.bc-agent/AGENTS.md` — this is a mandatory gate before opening any vault page for a fact. Do not use `index.md`, `map.md`, or `log.md` as a lookup shortcut, even if a user says the index is right there, lists everything, search can wait, or they already know this vault. Those are orientation hubs that can omit or preserve superseded facts; the vault instructions define the bounded retrieval and verification path.
2. Any page returned by that search that is relevant to the task
3. `.bc-agent/tasks/active.md` if work is already in flight
4. `.bc-agent/map.md` when choosing additional context

Keep the wiki live as you work: track in-flight work in
`.bc-agent/tasks/active.md`, check off plan steps, record forks as ADRs in
`.bc-agent/decisions/`, and append durable discoveries to `.bc-agent/log.md`
before finishing. See `.bc-agent/AGENTS.md` for the update triggers and protocol.

## Planning loop trigger

If the human's request sounds like planning future codebase work — feature ideas,
architecture direction, implementation strategy, slicing, or "what should we build/change" —
pause before implementing and ask whether they want to enter `/bc-plan-to-issues`.
If they are already asking for a concrete edit/fix, proceed normally. If the request is
about architectural runway, offer `/improve-codebase-architecture` first. For code/hybrid
wikis, also check `.bc-agent/conventions/architecture-runway.md`: if enough PRD-sized
changes have landed since the last architecture review, give a brief optional nudge to run
`/improve-codebase-architecture` before more planning.

See `.bc-agent/references/agent-skills.md` for the local skill map and
`.bc-agent/conventions/planning-workflow.md` for the loop.

## Scope rules

- Treat `.bc-agent/` as the source of durable agent context for THIS project only.
- Do not use or update `~/Wiki` for this project unless the human explicitly asks.
- Put all agent-created research, plans, scratch, and generated docs under `.bc-agent/`;
  do not create `docs/`-style notes in source folders or the repo root unless asked.
- Source-tree README, existing `docs/`, and JSDoc follow `codebase-docs` (one home,
  current state, same-change). Do not apply that skill to this vault.
- Do not store personal, cross-project, or machine-global knowledge here.

## Update rules

- Stable project facts → `.bc-agent/project/`.
- Commands and paths → `.bc-agent/references/`.
- Coding, validation, and workflow norms → `.bc-agent/conventions/`.
- Temporary task context → `.bc-agent/tasks/active.md`.
- Longer research writeups → `.bc-agent/research/`, with durable conclusions summarized back.
- PRDs that were actually drafted/published → `.bc-agent/project/` and/or GitHub parent issues; do not label exploratory research as a PRD.
- Major irreversible / architectural choices → `.bc-agent/decisions/` (ADRs).
- Brief durable discoveries → `.bc-agent/log.md`.

## Planning & execution workflow

This project is wired for the grill→issues→drain loop. See
`.bc-agent/conventions/planning-workflow.md`:

- `/bc-plan-to-issues` — interactive planning (grill → domain capture → PRD → ready-for-agent issues).
- `/bc-drain-issues` — autonomous (AFK) execution of the ready-for-agent queue.

## Publishing

- Agents may push their own commits and close directly-completed GitHub issues only
  if a matching rule authorizes it in the user-owned publish policy
  (`~/.config/agent-concepts/publish.yaml`). No matching rule ⇒ ask.
"""


# --- minimal Obsidian vault metadata ------------------------------------------
# Deliberately tiny/stable: no workspace.json, graph.json, or plugin state.
OBSIDIAN_APP = """{
  "newFileLocation": "current",
  "attachmentFolderPath": "attachments",
  "promptDelete": false
}
"""

OBSIDIAN_CORE_PLUGINS = """[
  "file-explorer",
  "global-search",
  "switcher",
  "graph",
  "backlink",
  "canvas",
  "outgoing-link",
  "tag-pane",
  "page-preview",
  "daily-notes",
  "templates",
  "note-composer",
  "command-palette",
  "slash-command",
  "editor-status",
  "bookmarks",
  "markdown-importer",
  "properties",
  "bases"
]
"""

OBSIDIAN_APPEARANCE = """{
  "baseFontSize": 16,
  "translucency": false
}
"""


# --- vault AGENTS.md (maintainer schema) --------------------------------------
# Keep this block byte-for-byte aligned with bc-wiki-maintain's pasteable vault
# instruction block. The scaffold runs it from the vault directory, where $PWD
# is the boundary that wiki_search.py must search.
CANONICAL_VAULT_READ_PATH = """<!-- BEGIN canonical vault read path -->
## First move: search the vault, do not read the index

For any task that needs a fact from this vault, run from the directory containing this
`AGENTS.md`:

```bash
VAULT_ROOT="$PWD"
python3 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/wiki_search.py" \\
  --limit 15 "$VAULT_ROOT" "term one" "term two"
```

Use **2–4 meaningful content keywords**, not the user's full question. Open the relevant
returned path(s) and verify the answer in the page text. The corpus is tracked Markdown only:
a newly created page is invisible until `git add` registers it with Git. If the fact may be in
an untracked page, do not interpret an empty result as absence; add the page and rerun the
search. Otherwise, if output is empty, reformulate once with a different 2–4 keyword set;
empty output is not proof that this vault lacks the answer. If the top result is `index.md`,
`map.md`, or `log.md`, add a distinguishing term and search again — those are hub/orientation
pages, not answers. Do not grep `index.md` rows for lookup.

Use qmd only for a deliberate cross-vault lookup, with every collection named explicitly:

```bash
qmd search "term one term two" -c vault-a -c vault-b --format files -n 15
```

Never run qmd unscoped, guess a collection from a `.agent`/`.bc-agent` basename, treat exit 0
or `[]` as proof of an answer's absence, or use `qmd query`. If `wiki_search.py` cannot run,
do not read the whole vault; use a bounded lexical candidate search and verify its pages.

Read `index.md` only for broad project orientation ("what is this project?"); never load it
whole or grep its rows to locate a page.
<!-- END canonical vault read path -->
"""

VAULT_AGENTS = """# __SLUG__ Agent Wiki — Maintainer Instructions

> **You are the primary user and maintainer of this wiki.** A human rarely reads it.
> It exists so you — and the next agent — can pick up work mid-flight with the verified
> facts, the decisions, and the live progress intact. **It is a living record, not a
> one-time writeup.** Do project work without updating it and you've left it stale.

This is the project-scoped wiki for `__SLUG__`, local to `.bc-agent/` and detached
from the user's personal `~/Wiki` (see [ADR-0001](decisions/adr-0001-local-project-agent-wiki.md)).
The repo-root `AGENTS.md` holds the scope/where-things-go rules; **this file is the
how-to-maintain schema.**

""" + CANONICAL_VAULT_READ_PATH + """

## The deal: keep it live or it's worthless

Update the wiki *in the same turn* as the work — not "later," not only when asked.

### Update triggers

| When you… | Do this |
|---|---|
| Start non-trivial work | Follow the canonical search-first read path above, then read the relevant returned pages and any in-flight plan. |
| Hear planning intent for codebase work | Before implementing, ask whether to enter `/bc-plan-to-issues`; offer `/improve-codebase-architecture` first for architecture runway. For code/hybrid wikis, check `conventions/architecture-runway.md` and nudge if the PRD-count threshold has been reached. |
| Verify/learn a durable fact | Update the smallest relevant `project/` or `references/` page (dated); append a line to `log.md`. |
| Find a recurring command / path / gotcha | Put it in `references/commands.md` / `paths.md` / `gotchas.md`. |
| Learn something that contradicts a page | Fix the page; note it in `log.md`. Never leave a stale claim. |
| Make an architectural / irreversible choice | Add a numbered ADR in `decisions/` (`Proposed`→`Accepted`); link from `index.md`. |
| Sharpen domain vocabulary | Update the glossary in `project/overview.md` (canonical names; no implementation detail). |
| Begin a multi-step effort | Create a plan (`project/<name>-plan.md`, see `templates/plan.md`); point `tasks/active.md` at it. |
| Finish a step | Check its box in the plan; update `tasks/active.md`. |
| Get blocked | Set the plan `Status: Blocked`; record the blocker in `tasks/active.md`. |
| Finish / abandon a plan | Set `Status: Done`/`Abandoned`; log a line in `tasks/completed.md`; clear `tasks/active.md`. |
| A step fails or is skipped | Say so — in the plan and the log. The record reflects what happened. |

## Plans & the live layer

- A multi-step effort gets a **plan page** under `project/` from `templates/plan.md`.
- For `grill-me`/`bc-plan-to-issues` → `bc-drain-issues` work, apply
  `conventions/planning-workflow.md`: it maps generic `CONTEXT.md`/`docs/adr/` persistence
  into this vault's pages.
- Use `references/agent-skills.md` as the local map of required loop skills and where their
  canonical bodies live in the shared agent-concepts workspace.
- **`tasks/active.md` is the live cursor.** Keep it true every session.
- `tasks/parking-lot.md` = deferred ideas. `tasks/completed.md` = dated done-log.
- Plan lifecycle: `Proposed → Approved → In progress → Blocked → Done / Abandoned`.

## Where things go

- `project/` — durable architecture, specs, plans, actual PRDs, and the **glossary** (`overview.md`).
- `research/` — exploratory notes/reports that may feed a PRD but are not themselves PRDs.
- `references/` — commands, paths, gotchas, external links.
- `conventions/` — validation, git, file-layout, planning-workflow, architecture-runway cadence.
- `decisions/` — ADRs (numbered, with `## Status`).
- `tasks/` — `active.md`, `parking-lot.md`, `completed.md`.
- `log.md` — append-only journal. `index.md` — catalog. `map.md` — context picker.
- Long research → `.bc-agent/research/`; scratch → `.bc-agent/scratch/`.

## Maintenance discipline

- Don't invent facts. Unverified ⇒ say so or park it.
- Smallest relevant page; summarize, don't dump; no secrets / `.env` values.
- Keep everything project-local — never push project context into `~/Wiki`.

## Git discipline

- Inspect `git status` first; stage only your own changes. Commit before finishing.
- Push / close issues only per `conventions/git-and-commit-policy.md` and the user-owned
  publish policy.
"""


INDEX = """# __SLUG__ Agent Wiki

The local, project-scoped agent wiki for `__SLUG__`. Detached from the user's personal
`~/Wiki`; use it only for context about this repository.

## Orientation

This catalog is for broad human-facing orientation. For a fact lookup, follow the
search-first read path in `AGENTS.md` rather than loading this page wholesale.

- [Agent maintainer instructions](AGENTS.md) — you maintain this wiki
- [Home](home.md)
- [Context map](map.md)
- [Project overview + glossary](project/overview.md)
- [Planning workflow: grill → issues → drain](conventions/planning-workflow.md)
- [Architecture runway cadence](conventions/architecture-runway.md)
- [Agent skill map](references/agent-skills.md)
- [Validation](conventions/validation.md)
- [Commands](references/commands.md)
- [ADR-0001: local project agent wiki](decisions/adr-0001-local-project-agent-wiki.md)
- [Active task context](tasks/active.md)
- [Agent log](log.md)

## Scope

This wiki may contain repo-specific architecture, workflow notes, build/validation
facts, project decisions, and recurring commands/gotchas. It must **not** contain
personal wiki content, cross-project preferences, secrets/credentials, or long raw logs.

This wiki is also a standalone Obsidian vault rooted at `.bc-agent/`.
"""


HOME = """# __SLUG__ Agent Wiki Home

Human-facing orientation for the local project agent wiki. For a fact lookup, follow the
search-first read path in `AGENTS.md` rather than treating this page as the source.

- [Agent instructions](AGENTS.md)
- [Index](index.md)
- [Context map](map.md)
- [Agent log](log.md)
- [Active tasks](tasks/active.md)
- [Project overview + glossary](project/overview.md)
- [Commands](references/commands.md)
- [Gotchas](references/gotchas.md)

## Scope reminder

This vault is local to `.bc-agent/` and detached from the user's personal `~/Wiki`.
"""


MAP = """# Context Map

This human-facing map helps choose the smallest context set after the canonical search path
in `AGENTS.md`; it is orientation, not the lookup mechanism. Extend the sections as the
project grows.

## Always useful

- `project/overview.md`
- `references/commands.md`
- `conventions/validation.md`

## Planning / workflow work

- `conventions/planning-workflow.md`
- `conventions/architecture-runway.md`
- `references/agent-skills.md`
- `conventions/git-and-commit-policy.md`
- `conventions/validation.md`
- `log.md`

## Research or PRD work

- `conventions/planning-workflow.md`
- `project/overview.md`
- `research/README.md`
- `templates/plan.md`

## File / layout work

- `conventions/file-layout.md`
- `references/paths.md`

## Decisions

For architectural or durable workflow changes, check `decisions/` before adding a new ADR.

<!-- Add task-type sections (e.g. "Frontend work", "API work") as the project takes shape. -->
"""


LOG = """# Agent Log

Append-only journal of durable discoveries and session outcomes. Newest at the bottom.
One to three lines each; no transcripts or long command output.

## [__DATE__]

- Scaffolded the project agent workspace (root `AGENTS.md` + `.bc-agent/` vault) with
  `bc-init-agent`. Ready for the grill → issues → drain workflow. Validation/file-layout
  stubs still TODO.
"""


OVERVIEW = """# Project Overview

> One-paragraph description of `__SLUG__`: what it is, who it's for, the stack. **TODO:** fill
> this in as the project takes shape.

## Glossary

The project's shared vocabulary — canonical names for the domain concepts, no implementation
detail. `grill-me` / `bc-plan-to-issues` (via `domain-modeling`) maintain this as the
project's `CONTEXT.md`-equivalent. Keep it a pure glossary.

<!-- Term — one-line canonical definition. -->

_None captured yet._

## Agent context policy

All durable agent context for this repository belongs in `.bc-agent/`. This wiki is
detached from the user's personal `~/Wiki` and scoped to this repository only.

## Open questions

- What are the canonical validation commands? (fill `conventions/validation.md`)
- What is the source/build file layout? (fill `conventions/file-layout.md`)
- What is the primary deliverable / target?
"""


PLANNING_WORKFLOW = """# Planning Workflow: grill → issues → drain

Date: __DATE__

This project is wired for the full loop. Use the `bc-` orchestrators with this repo-local
adapter so planning persistence lands in `.bc-agent/` instead of generic
`CONTEXT.md` / `docs/adr/` files. See `$AGENT_CONCEPTS/docs/pipeline.md` for the loop.

## Planning intent trigger

When the human sounds like they are planning codebase work — feature ideas, refactor
direction, architecture strategy, implementation approach, or issue slicing — ask whether
they want to enter `/bc-plan-to-issues` before writing implementation code. If the request is
architectural runway rather than a settled feature, offer `/improve-codebase-architecture`
first. If they clearly ask for a concrete edit/fix, proceed normally.

## Canonical repo-local planning surfaces

- **Glossary / domain facts:** the glossary section of `project/overview.md` (or a dedicated
  `project/glossary.md` if it grows). This is this project's `CONTEXT.md`-equivalent.
- **ADRs:** numbered files under `decisions/` using `templates/adr.md`.
- **Plans / actual PRDs:** durable planning artifacts under `project/`, linked from `index.md`. Only call it a PRD when the PRD drafting/publishing step actually happened; exploratory notes stay under `research/` or as plans.
- **Research / evidence:** exploratory reports, architecture-review HTML summaries, and investigation writeups under `research/` (or temp storage if intentionally throwaway), with durable conclusions summarized back to `project/` / `decisions/`.
- **Skill map:** required loop skills and source paths in `references/agent-skills.md`.
- **Live cursor:** `tasks/active.md` while work is in flight.
- **Issue tracker:** GitHub issues via `gh`; intake uses `needs-triage` / `needs-info`;
  ready agent work uses `ready-for-agent`; claimed work may show `in-progress-agent`;
  parked work uses `needs-human`; durable rejections use `wontfix` plus `.bc-agent/out-of-scope/`.
- **Session log:** short durable notes appended to `log.md`.

## Intake and evidence — `/triage`, `/prototype`, `/improve-codebase-architecture`

- Use `/triage` for existing GitHub issues/PRs before they enter the loop: verify, ask for
  missing info, write an Agent Brief, mark `ready-for-agent`, or record durable rejections in
  `.bc-agent/out-of-scope/`.
- Use `/prototype` when a state model or UI direction needs a throwaway artifact before the
  PRD. Capture the verdict in `project/` or an ADR; don't send prototype code to the drain.
- Use `/improve-codebase-architecture` when a feature or bug needs a deep-module runway before
  slicing. Its report lives in temp storage; durable decisions go into `decisions/` or a plan.
- For code/hybrid wikis, also follow `conventions/architecture-runway.md`: nudge the human to
  consider `/improve-codebase-architecture` after enough PRD-sized implementation work has
  landed since the last review.

## Planning — `/bc-plan-to-issues`

One command runs grill → domain capture → PRD → slices. When the underlying skills would
persist to generic `CONTEXT.md` / `docs/adr/`, persist here instead:

- Canonical terminology → the glossary in `project/overview.md`.
- Costly + surprising + trade-off decision → `decisions/adr-NNNN-<slug>.md` (`templates/adr.md`).
- Multi-step feature direction → a `project/<feature>-plan.md` / `project/<feature>-prd.md`.
- Current progress/blockers → `tasks/active.md`.

The one-question-at-a-time grilling rule and the slicing quiz (the last human gate before
AFK) still apply. Don't write implementation code while major branches remain open.

## Execution — `/bc-drain-issues`

Once planning leaves a `ready-for-agent` queue, `/bc-drain-issues` executes it autonomously
(AFK): per unblocked issue it dispatches a fresh subagent that builds the slice test-first and
lands it **trunk-based**, then moves on.

- **Authorization.** The executor's preflight runs `publish-check.py`. This repo must have an
  allow rule in `policies/publish.yaml` (push + issue-close on `master`) and authorization for
  `bc-drain-claims/issue-<n>` coordination branches, or AFK/parallel push is blocked.
  **TODO:** confirm this repo is authorized before the first AFK run.
- **Validation gate.** The per-issue agent reads THIS repo's `conventions/validation.md` +
  `references/commands.md` for what "validated" means — not a generic test command. Criteria
  met **and** that validation clean = eligible to land.
- **Claim before work.** Concurrent drain runners must first create the remote
  `bc-drain-claims/issue-<n>` branch. If the claim push fails, another runner has the issue;
  skip it and try the next.
- **Trunk-based, not PRs.** Each slice commits → pushes `master` → closes its issue with a
  sha + validation comment. Dependent slices then see prior work immediately.
- **Parking.** A slice that can't complete cleanly is parked: comment on the issue, swap
  `ready-for-agent` → `needs-human`, push nothing partial/RED. A run of consecutive parks
  trips the circuit-breaker and stops the loop.
- **Bookkeeping.** Treat landed slices like any project work: update `tasks/active.md`/
  `completed.md` and append a dated `log.md` line with issue numbers and commits.

## Clean handoff after planning

- Resolved scope in a `project/` plan/actual-PRD page or GitHub parent issue. Parent PRD issues are coordination artifacts; implementation slices get `ready-for-agent`.
- Durable trade-offs in `decisions/`.
- Independent `ready-for-agent` issues ordered by dependency, each with an Agent Brief / concrete acceptance criteria.
- `tasks/active.md` clear or pointing at the in-flight plan.
- A dated `log.md` line with issue numbers and changed pages.
"""


ARCHITECTURE_RUNWAY = """# Architecture Runway Cadence

Date: __DATE__

For code/hybrid wikis, this page gives a computed, optional signal for when to offer
`/improve-codebase-architecture`. The signal comes from Git history; do not maintain a
counter in this file. The goal is to refresh architecture runway after enough durable project
work has accumulated, not after a calendar interval.

## Computed check

Run this before planning, refactor, or seam-adjacent work. It finds the newest commit whose
message names an architecture review, then counts commits touching the durable project and
live-task surfaces after that review:

```sh
review_tip="$(
  git log --format='%H%x09%s' -- .bc-agent |
    awk 'tolower($0) ~ /architecture.?review|arch.?review|improve-codebase-architecture/ { print $1; exit }'
)"
if [ -n "$review_tip" ]; then
  review_range="$review_tip..HEAD"
else
  review_range="HEAD"
fi
planning_commits="$(git log --format='%h %cs %s' "$review_range" -- .bc-agent/project .bc-agent/tasks)"
planning_count="$(printf '%s\\n' "$planning_commits" | sed '/^$/d' | wc -l)"
printf 'Planning-surface commits since the latest recognized architecture review: %s\\n' "$planning_count"
printf '%s\\n' "$planning_commits"
```

The `review_tip` lookup is deliberately fail-safe. If no review commit is recognizable, the
range includes all reachable history and the signal may over-count. Git can count commits and
paths; it cannot prove that a change was PRD-sized. Over-counting produces an optional nudge,
not an unsafe edit. If a review commit uses a different subject, the same fallback applies.

## Nudge heuristic

Give a brief, optional nudge when the current request is planning/refactor/seam-adjacent and
one of these is true:

- `planning_count` is 3 or higher. This is a conservative Git-derived proxy for the former
  three-PRD / PRD-sized-slice threshold, not a claim that Git understands PRD semantics.
- The current work shows structural friction: unclear module boundaries, hard-to-test code,
  repeated bugs around the same seam, or "where should this live?" uncertainty.

A request that is itself architecture-heavy can also qualify from its content. This page does
not pretend to compute that judgment from filenames or commit messages.

Do **not** block concrete fixes. The nudge is advisory:

> Optional architecture runway nudge: Git shows multiple planning-surface changes since the last recognized architecture review. Before planning more work, do you want to run `/improve-codebase-architecture` to look for seams and testability improvements?

## Review record

A review has no hand-maintained entry here. Store the review artifact in the normal project
wiki location and include `architecture review` in the commit subject so the next computed check
can find its boundary. If the subject does not use that wording, the fail-safe fallback simply
counts more history and may nudge again.

## Agent update rules

- Run the computed check when the request is planning/refactor/seam-adjacent; do not edit this
  page to record the result.
- When `/improve-codebase-architecture` runs, commit its review artifact with an explicit
  `architecture review` subject so future checks can establish a new boundary.
- If `references/agent-skills.md` no longer lists `/improve-codebase-architecture`, remove the
  nudge and explain why here.
"""


VALIDATION = """# Validation

> **TODO:** canonical validation commands are not established yet. Fill these in as you learn
> the project; `bc-drain-issues` reads this page to know what "validated" means.

## Build / test validation

```sh
# TODO: the project's real build/test/lint commands, e.g.
# <test command>
# <lint / typecheck command>
# <build command>
```

## Baseline checks

```sh
git status --short
```

## Agent guidance

- After changing files, run the most relevant available validation.
- If no project-specific tests exist yet, verify syntax/structure and summarize what you checked.
- Do not claim build/test/runtime validation was run unless it actually ran.
- Add newly discovered canonical commands here and to `../references/commands.md`.
"""


FILE_LAYOUT = """# File Layout

> **TODO:** record the real top-level paths once known.

Known top-level paths at scaffold time:

- `AGENTS.md` — repo-root instructions pointing agents at this wiki
- `.bc-agent/` — this project-scoped agent wiki

## Agent guidance

- Confirm source/build relationships before editing generated-looking files.
- Keep local project wiki files under `.bc-agent/`.
- Do not add project context to the user's personal `~/Wiki`.
"""


GIT_POLICY = """# Git and Commit Policy

Normal git discipline applies.

## Agent guidance

- Inspect `git status` first; stage and commit only your own changes — never sweep up
  unrelated edits the human has in progress.
- Commit agent-made changes before finishing the task.
- Push / close GitHub issues only when authorized by the user-owned publish policy
  (`~/.config/agent-concepts/publish.yaml`). After pushing, agents may close issues
  directly completed by the pushed work, leaving a comment with the commit SHA and a
  validation summary; never close partially satisfied or adjacent issues.
- Keep commits scoped, with concise messages. Do not rewrite history or re-init Git unless asked.
"""


def ref_stub(title: str, body: str) -> str:
    return f"# {title}\n\n{body}\n"


ADR_0001 = """# ADR 0001: Local Project Agent Wiki

Date: __DATE__

## Status

Accepted

## Context

Agents need durable project context while working in this repository, segregated from and
detached from the user's personal `~/Wiki`.

## Decision

Create a project-local wiki at `.bc-agent/` and a repo-root `AGENTS.md` that instructs
agents to use it as the project-scoped context source. The wiki must not depend on or update
`~/Wiki` unless the user explicitly asks.

## Consequences

- Project context travels with this repository.
- Agents begin with the vault's `AGENTS.md`; its first move is to search the vault using the canonical search path, and `index.md` remains for broad orientation only.
- Personal/global wiki context stays separate.
- Durable discoveries are committed with the project.
"""


ACTIVE = """# Active Tasks

The live cursor for in-flight work. Keep this true every session — the next agent's first
move is the search-first path in [AGENTS.md](../AGENTS.md), then it reads this page when work
is in flight.

## In flight

_None right now._

<!-- For a multi-step effort:
- **Plan:** [project/<name>-plan.md](../project/<name>-plan.md) — Status: In progress
- **On step:** 3 of 7 — <what you're doing now>
- **Blocker:** <none | description>
-->

## Temporary handoff notes

_None right now._
"""


PARKING = """# Parking Lot

Deferred / future ideas and wiki improvements.

- Fill `conventions/validation.md` with canonical commands once discovered.
- Fill `conventions/file-layout.md` once the source/build layout is known.
- Confirm this repo is authorized in `policies/publish.yaml` before the first AFK drain.
"""


COMPLETED = """# Completed Tasks

## [__DATE__]

- Scaffolded the project agent workspace with `bc-init-agent`.
"""


TPL_ADR = """# ADR NNNN: <title>

Date: YYYY-MM-DD

## Status
Proposed   <!-- Proposed | Accepted | Superseded by ADR-XXXX | Rejected -->

## Context
The situation and the question being decided. Link the findings/pages that motivate it.

## Decision
What we chose.

## Alternatives considered
What else we could have done, and why each lost.

## Consequences
What this commits us to, follow-on work, and what it rules out.
"""


TPL_PLAN = """# <Plan name>

Status: Proposed   <!-- Proposed | Approved | In progress | Blocked | Done | Abandoned -->
Updated: YYYY-MM-DD

## Goal
The outcome in one or two sentences. Define what "done" means.

## Current state
Verified reality today. Link relevant `project/`, `references/`, and `decisions/` pages.

## Approach
The chosen strategy in a short paragraph. Link the ADR(s) that justify it.

## Steps
Ordered and staged so each is independently checkable.
- [ ] 1. …
- [ ] 2. …

## Validation
How each milestone is verified (link `conventions/validation.md` / the relevant commands).

## Risks & rollback
What can go wrong and how to undo it.

## Open questions / blockers
Unresolved items. If one blocks the plan, set `Status: Blocked` and note it in `tasks/active.md`.

## Links
The ADRs, references, and project pages this plan rests on.
"""


RESEARCH_README = """# Research

Long-form research writeups and investigation notes live here. Summarize durable conclusions
back into the relevant `.bc-agent/` page and keep the long version here for the trail.
"""


AGENT_SKILLS = """# Agent Skill Map

Date: __DATE__

The bc loop skills are canonical in `$AGENT_CONCEPTS/concepts/<skill>/body/SKILL.md`
and are normally deployed into `~/.pi/agent/skills/<skill>` and `~/.agents/skills/<skill>`
via symlink. Do not vendor/copy their bodies into this repo; use this page as the repo-local
map so agents know what to invoke.

## Planning/execution loop

- `/bc-plan-to-issues` — interactive planning front: grill → domain capture → PRD → issue slices.
- `/bc-drain-issues` — AFK executor for `ready-for-agent` issue queues.
- `/improve-codebase-architecture` — optional architecture runway before planning/slicing.

## Supporting skills used by the loop

- Intake/evidence: `/triage`, `/prototype`.
- Planning disciplines: `grilling`, `domain-modeling`, `prd-drafting`, `issue-slicing`, `codebase-design`.
- Source-tree docs: `codebase-docs` — README / existing `docs/` / JSDoc only; not this vault.
- Execution disciplines: `tdd`, `diagnosing-bugs`, `bc-autoresearch-loop`.
- Wiki maintenance: `/bc-wiki-maintain` — compute vault health, find index/search drift, and promote durable log entries without silently resolving contradictions.

## Agent behavior

If the user's request sounds like planning future codebase work, ask whether to enter
`/bc-plan-to-issues` before implementing. Offer `/improve-codebase-architecture` first when
the main uncertainty is architecture/seams. In code/hybrid wikis, run the computed check in
`conventions/architecture-runway.md` and give the optional architecture-runway nudge when its
planning-surface signal reaches the threshold.
"""


ARCHETYPE_READMES = {
    "ops": """# Operations / System Wiki

Use this archetype when the workspace tracks a real system, service, host, workflow, or local infrastructure rather than one codebase feature pipeline.

- `components/` — verified state of systems/tools/hosts.
- `findings/` — recon and evidence with commands, dates, and conclusions.
- `decisions/` — choices and supersessions.
- `open-questions/` — assumptions that gate plans.
- `plans/` — staged executable plans.
""",
    "learning": """# Learning Wiki

Use this archetype when bc agents are helping the human learn a subject over time.

- `learning/` — goals, syllabus, progress, and review cadence.
- `sources/` — source material and provenance.
- `concepts/` — distilled concepts in the learner's words.
- `questions/` — open questions, misconceptions, and review prompts.
- `sessions/` — dated tutoring/session notes.

Use the `teach` skill for multi-session tutoring and spaced review; keep durable learning state here.
""",
    "knowledge": """# Knowledge Graph Wiki

Use this archetype when the workspace is primarily for source ingest and compounding knowledge.

- `raw/` — immutable dropped source material.
- `wiki/sources/` — one compiled page per source.
- `wiki/entities/` — people, tools, projects, libraries, services.
- `wiki/concepts/` — reusable ideas and patterns.
- `wiki/syntheses/` — cross-source summaries and maps.

Raw sources stay immutable; agents maintain the compiled `wiki/` layer.
""",
    "hybrid": """# Hybrid Wiki

Use this archetype when the repo needs both execution scaffolding and another durable knowledge mode.

Start with the normal `.bc-agent` project workflow, then promote material into the relevant folders:

- `components/` / `findings/` / `open-questions/` for operations-style system work.
- `learning/` / `sources/` / `concepts/` / `sessions/` for teaching and study.
- `raw/` / `wiki/` for knowledge-graph ingest and synthesis.
""",
}


def archetype_files(archetype: str) -> dict[str, str]:
    """Optional archetype-specific seed files layered on top of the base project wiki."""
    common = {"archetype.md": ARCHETYPE_READMES[archetype]} if archetype in ARCHETYPE_READMES else {}
    if archetype == "ops":
        return common | {
            "components/README.md": "# Components\n\nVerified state of real systems, tools, hosts, and services.\n",
            "findings/README.md": "# Findings\n\nEvidence from recon, commands, research, or validation. Include method, date, observations, and conclusion.\n",
            "open-questions/README.md": "# Open Questions\n\nUnverified assumptions that gate or shape plans. Resolve by linking findings/decisions.\n",
            "plans/README.md": "# Plans\n\nExecutable operational plans with current status and checkable steps.\n",
            "templates/component.md": "# __TITLE__\n\n## Verified state\n\nTODO — include date and method.\n\n## Interfaces / dependencies\n\nTODO.\n\n## Gotchas\n\nTODO.\n",
            "templates/finding.md": "# __TITLE__\n\n## Method\n\nTODO — commands, sources, date.\n\n## Observations\n\nTODO.\n\n## Conclusion\n\nTODO.\n",
            "templates/open-question.md": "# __TITLE__\n\n## Question\n\nTODO.\n\n## Why it matters\n\nTODO.\n\n## Resolution\n\nOpen.\n",
        }
    if archetype == "learning":
        return common | {
            "learning/plan.md": "# Learning Plan\n\n## Goal\n\nTODO.\n\n## Current level\n\nTODO.\n\n## Path\n\nTODO.\n\n## Review cadence\n\nUse the `teach` skill for spaced review and durable learning records.\n",
            "sources/README.md": "# Sources\n\nLearning material with provenance and status.\n",
            "concepts/README.md": "# Concepts\n\nDistilled explanations, examples, and connections in the learner's words.\n",
            "questions/README.md": "# Questions\n\nOpen questions, misconceptions, quiz prompts, and review items.\n",
            "sessions/README.md": "# Sessions\n\nDated tutoring/session notes and next review prompts.\n",
            "references/teach-skill.md": "# Teach Skill\n\nUse `teach` for multi-session tutoring. Keep project-local learning artifacts in this vault, not in the global personal wiki unless the human asks.\n",
            "templates/learning-session.md": "# YYYY-MM-DD — Session\n\n## Goal\n\nTODO.\n\n## What changed\n\nTODO.\n\n## Misconceptions / review items\n\nTODO.\n\n## Next\n\nTODO.\n",
        }
    if archetype == "knowledge":
        return common | {
            "raw/README.md": "# Raw Sources\n\nDropped source material. Treat as immutable once ingested; corrections belong in compiled wiki pages.\n",
            "wiki/index.md": "# Compiled Wiki Index\n\nCatalog sources, entities, concepts, and syntheses here.\n",
            "wiki/log.md": "# Wiki Log\n\nAppend ingest, synthesis, and maintenance events here.\n",
            "wiki/sources/README.md": "# Sources\n\nOne compiled page per source with provenance and key claims.\n",
            "wiki/entities/README.md": "# Entities\n\nPeople, projects, tools, organizations, services, libraries.\n",
            "wiki/concepts/README.md": "# Concepts\n\nReusable ideas and patterns synthesized across sources.\n",
            "wiki/syntheses/README.md": "# Syntheses\n\nCross-source overviews, maps, contradictions, and evidence gaps.\n",
        }
    if archetype == "hybrid":
        files: dict[str, str] = dict(common)
        for name in ("ops", "learning", "knowledge"):
            files |= {path: text for path, text in archetype_files(name).items() if path != "archetype.md"}
        return files
    return {}


def vault_files(archetype: str = "code") -> dict[str, str]:
    files = {
        "AGENTS.md": VAULT_AGENTS,
        "index.md": INDEX,
        "home.md": HOME,
        "map.md": MAP,
        "log.md": LOG,
        "project/overview.md": OVERVIEW,
        "references/commands.md": ref_stub(
            "Commands", "Recurring project commands. **TODO:** fill as discovered.\n\n_None yet._"),
        "references/paths.md": ref_stub(
            "Paths", "Important paths in this repo. **TODO:** fill as discovered.\n\n_None yet._"),
        "references/gotchas.md": ref_stub(
            "Gotchas", "Surprising behaviors and traps. **TODO:** fill as discovered.\n\n_None yet._"),
        "references/agent-skills.md": AGENT_SKILLS,
        "references/external-links.md": ref_stub(
            "External Links", "Useful external references for this project.\n\n_None yet._"),
        "conventions/planning-workflow.md": PLANNING_WORKFLOW,
        "conventions/architecture-runway.md": ARCHITECTURE_RUNWAY,
        "conventions/validation.md": VALIDATION,
        "conventions/file-layout.md": FILE_LAYOUT,
        "conventions/git-and-commit-policy.md": GIT_POLICY,
        "decisions/adr-0001-local-project-agent-wiki.md": ADR_0001,
        "tasks/active.md": ACTIVE,
        "tasks/parking-lot.md": PARKING,
        "tasks/completed.md": COMPLETED,
        "templates/adr.md": TPL_ADR,
        "templates/plan.md": TPL_PLAN,
        ".obsidian/app.json": OBSIDIAN_APP,
        ".obsidian/core-plugins.json": OBSIDIAN_CORE_PLUGINS,
        ".obsidian/appearance.json": OBSIDIAN_APPEARANCE,
    }
    files.update(archetype_files(archetype))
    return files


def render(text: str, slug: str, date: str) -> str:
    return text.replace(SLUG, slug).replace(DATE, date)


def targets(root: Path, slug: str, date: str, archetype: str = "code") -> list[tuple[Path, str, bool]]:
    """Every file the scaffold owns: (destination, rendered content, is_root_AGENTS)."""
    vault = root / ".bc-agent"
    out: list[tuple[Path, str, bool]] = [(root / "AGENTS.md", render(ROOT_AGENTS, slug, date), True)]
    for relpath, text in vault_files(archetype).items():
        out.append((vault / relpath, render(text, slug, date), False))
    out.append((vault / "research" / "README.md", render(RESEARCH_README, slug, date), False))
    out.append((vault / "out-of-scope" / ".gitkeep", "", False))
    out.append((vault / "scratch" / ".gitkeep", "", False))
    return out


def _contains(path: Path, needle: str) -> bool:
    try:
        return needle in path.read_text(errors="ignore")
    except OSError:
        return False


def upgrade_notes(root: Path, archetype: str) -> list[str]:
    """Manual merge hints for existing files that were intentionally left untouched."""
    vault = root / ".bc-agent"
    notes: list[str] = []

    # This contract applies to every archetype. Keep it outside the code/hybrid
    # gate below so learning and knowledge vaults receive the same migration hint.
    read_path_checks = [
        (root / "AGENTS.md", "1. `.bc-agent/AGENTS.md`",
         "root AGENTS.md should make `.bc-agent/AGENTS.md` the first read and defer vault retrieval to its canonical search-first path"),
        (vault / "AGENTS.md", "<!-- BEGIN canonical vault read path -->",
         "`.bc-agent/AGENTS.md` should include the canonical search-first vault read path block from `bc-wiki-maintain`"),
    ]
    for path, needle, message in read_path_checks:
        if path.exists() and not _contains(path, needle):
            notes.append(message)

    # These existing upgrade hints depend on the code/hybrid architecture
    # overlay and remain scoped to those archetypes.
    if archetype not in {"code", "hybrid"}:
        return notes

    checks = [
        (root / "AGENTS.md", "architecture-runway.md",
         "root AGENTS.md should point coding/planning requests at `.bc-agent/conventions/architecture-runway.md` for the optional `/improve-codebase-architecture` nudge"),
        (vault / "AGENTS.md", "architecture-runway.md",
         "`.bc-agent/AGENTS.md` should mention the architecture-runway cadence in its planning-intent/update triggers"),
        (vault / "references" / "agent-skills.md", "architecture-runway.md",
         "`references/agent-skills.md` should tell agents to check the architecture-runway cadence when `/improve-codebase-architecture` is relevant"),
        (vault / "index.md", "architecture-runway.md",
         "`index.md` should link to `conventions/architecture-runway.md`"),
        (root / "AGENTS.md", "codebase-docs",
         "root AGENTS.md should point source-tree README/docs/JSDoc at `codebase-docs` and keep that skill off `.bc-agent/`"),
        (vault / "references" / "agent-skills.md", "codebase-docs",
         "`references/agent-skills.md` should list `codebase-docs` for source-tree docs, not the vault"),
        (vault / "references" / "agent-skills.md", "bc-wiki-maintain",
         "`references/agent-skills.md` should list `/bc-wiki-maintain` as the canonical project-vault maintenance skill"),
    ]
    for path, needle, message in checks:
        if path.exists() and not _contains(path, needle):
            notes.append(message)
    return notes


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Idempotent: creates only missing files; never deletes, and never "
                    "overwrites existing files unless explicitly forced.")
    ap.add_argument("--root", required=True, help="project (repo) root")
    ap.add_argument("--slug", required=True, help="project display name, kebab-case")
    ap.add_argument("--date", default=_dt.date.today().isoformat())
    ap.add_argument("--archetype", choices=["code", "ops", "learning", "knowledge", "hybrid"], default="code",
                    help="optional wiki archetype layered on top of the base project scaffold")
    ap.add_argument("--force", action="store_true",
                    help="overwrite existing VAULT files (still never deletes; never touches root AGENTS.md)")
    ap.add_argument("--force-root", action="store_true",
                    help="also overwrite an existing root AGENTS.md")
    ap.add_argument("--dry-run", action="store_true", help="report what would happen; write nothing")
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    slug = args.slug.strip()
    if not root.is_dir():
        print(f"ERROR: root is not a directory: {root}")
        return 1
    if not slug or slug != slug.lower() or " " in slug:
        print(f"ERROR: slug must be lower-case kebab with no spaces: {slug!r}")
        return 1

    created: list[Path] = []
    overwritten: list[Path] = []
    skipped: list[Path] = []  # existed, left untouched

    for dest, content, is_root in targets(root, slug, args.date, args.archetype):
        exists = dest.exists()
        may_overwrite = (args.force_root if is_root else args.force)
        if exists and not may_overwrite:
            skipped.append(dest)
            continue
        if not args.dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content)
        (overwritten if exists else created).append(dest)

    verb = "Would create" if args.dry_run else "Created"
    if created:
        print(f"{verb} {len(created)} file(s):")
        for p in created:
            print(f"  + {p}")
    if overwritten:
        word = "Would overwrite" if args.dry_run else "Overwrote"
        print(f"{word} {len(overwritten)} existing file(s) (forced):")
        for p in overwritten:
            print(f"  ~ {p}")
    if skipped:
        print(f"Left {len(skipped)} existing file(s) untouched:")
        for p in skipped:
            print(f"  = {p}")

    notes = upgrade_notes(root, args.archetype)
    if notes:
        print("\nUpgrade notes for existing files left untouched:")
        for note in notes:
            print(f"  ! {note}")
        print("These are manual merge hints for the agent running the skill; the scaffold stays additive and does not overwrite existing instructions.")

    if not created and not overwritten:
        print("\nNothing to do — the workspace is already present; nothing was created, "
              "overwritten, or deleted.")
        return 0

    if skipped:
        # Most relevant when plugging into an existing project: flag the un-pointed root AGENTS.
        root_agents = root / "AGENTS.md"
        if root_agents in skipped:
            print(f"\nNOTE: existing {root_agents} was left as-is. Merge the 'read .bc-agent first' "
                  f"pointer into it by hand (see `.bc-agent/AGENTS.md` and its canonical search-first block).")

    print("\nNext: fill conventions/validation.md + file-layout.md as you learn the project; "
          "read .bc-agent/references/agent-skills.md for the loop skill map; "
          "authorize this repo in policies/publish.yaml if you'll run /bc-drain-issues AFK; "
          "then /triage existing issues or /bc-plan-to-issues to plan the first feature.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
