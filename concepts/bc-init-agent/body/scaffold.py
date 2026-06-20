#!/usr/bin/env python3
"""Scaffold a project-local .bc-agent wiki + root AGENTS.md for the grill→issues→drain workflow.

Inspired by the image-maze `.agent/<project>/` Obsidian-vault wiki, flattened to a single
`.bc-agent/` vault (no per-project nesting). Writes a
generalized schema with TODO stubs (validation, file-layout, paths) that the
project's first agents fill in. Faithful to the image-maze persistence model:
NO root CONTEXT.md — the glossary lives in the vault (project/overview.md), ADRs
in decisions/, plans/PRDs in project/, and conventions/planning-workflow.md is
the adapter that redirects planning persistence into the vault.

Idempotent guard: refuses to overwrite an existing .bc-agent/ vault unless
--force is given. The root AGENTS.md is only written if absent (otherwise the
caller merges the vault pointer by hand) unless --force-root.

Usage:
  scaffold.py --root <repo-root> --slug <project-slug> [--date YYYY-MM-DD] [--force] [--force-root]
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

Before making non-trivial changes, read:

1. `.bc-agent/index.md`
2. `.bc-agent/AGENTS.md` — you are the wiki's maintainer; this is how to keep it live
3. `.bc-agent/map.md`
4. Any linked page relevant to the task

Keep the wiki live as you work: track in-flight work in
`.bc-agent/tasks/active.md`, check off plan steps, record forks as ADRs in
`.bc-agent/decisions/`, and append durable discoveries to `.bc-agent/log.md`
before finishing. See `.bc-agent/AGENTS.md` for the update triggers and protocol.

## Scope rules

- Treat `.bc-agent/` as the source of durable agent context for THIS project only.
- Do not use or update `~/Wiki` for this project unless the human explicitly asks.
- Put all agent-created research, plans, scratch, and generated docs under `.bc-agent/`;
  do not create `docs/`-style notes in source folders or the repo root unless asked.
- Do not store personal, cross-project, or machine-global knowledge here.

## Update rules

- Stable project facts → `.bc-agent/project/`.
- Commands and paths → `.bc-agent/references/`.
- Coding, validation, and workflow norms → `.bc-agent/conventions/`.
- Temporary task context → `.bc-agent/tasks/active.md`.
- Longer research writeups → `.bc-agent/research/`, with durable conclusions summarized back.
- Major irreversible / architectural choices → `.bc-agent/decisions/` (ADRs).
- Brief durable discoveries → `.bc-agent/log.md`.

## Planning & execution workflow

This project is wired for the grill→issues→drain loop. See
`.bc-agent/conventions/planning-workflow.md`:

- `/bc-grill-to-issues` — interactive planning (grill → domain capture → PRD → ready-for-agent issues).
- `/bc-drain-issues` — autonomous (AFK) execution of the ready-for-agent queue.

## Publishing

- Agents may push their own commits and close directly-completed GitHub issues only
  if a matching rule authorizes it in the user-owned publish policy
  (`~/Sync/CONFIG/agents/policies/publish.yaml`). No matching rule ⇒ ask.
"""


# --- vault AGENTS.md (maintainer schema) --------------------------------------
VAULT_AGENTS = """# __SLUG__ Agent Wiki — Maintainer Instructions

> **You are the primary user and maintainer of this wiki.** A human rarely reads it.
> It exists so you — and the next agent — can pick up work mid-flight with the verified
> facts, the decisions, and the live progress intact. **It is a living record, not a
> one-time writeup.** Do project work without updating it and you've left it stale.

This is the project-scoped wiki for `__SLUG__`, local to `.bc-agent/` and detached
from the user's personal `~/Wiki` (see [ADR-0001](decisions/adr-0001-local-project-agent-wiki.md)).
The repo-root `AGENTS.md` holds the scope/where-things-go rules; **this file is the
how-to-maintain schema.**

## The deal: keep it live or it's worthless

Update the wiki *in the same turn* as the work — not "later," not only when asked.

### Update triggers

| When you… | Do this |
|---|---|
| Start non-trivial work | Read `index.md` → this file → `map.md` → `tasks/active.md` and any in-flight plan. |
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
- For `grill-me`/`bc-grill-to-issues` → `bc-drain-issues` work, apply
  `conventions/planning-workflow.md`: it maps generic `CONTEXT.md`/`docs/adr/` persistence
  into this vault's pages.
- **`tasks/active.md` is the live cursor.** Keep it true every session.
- `tasks/parking-lot.md` = deferred ideas. `tasks/completed.md` = dated done-log.
- Plan lifecycle: `Proposed → Approved → In progress → Blocked → Done / Abandoned`.

## Where things go

- `project/` — durable architecture, specs, plans, and the **glossary** (`overview.md`).
- `references/` — commands, paths, gotchas, external links.
- `conventions/` — validation, git, file-layout, planning-workflow.
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

## Start here

- [Agent maintainer instructions](AGENTS.md) — you maintain this wiki
- [Home](home.md)
- [Context map](map.md)
- [Project overview + glossary](project/overview.md)
- [Planning workflow: grill → issues → drain](conventions/planning-workflow.md)
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

Obsidian home note for the local project agent wiki.

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

Use this page to choose the smallest context set for a task. Extend the sections as the
project grows.

## Always useful

- `project/overview.md`
- `references/commands.md`
- `conventions/validation.md`

## Planning / workflow work

- `conventions/planning-workflow.md`
- `conventions/git-and-commit-policy.md`
- `conventions/validation.md`
- `log.md`

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

## __DATE__

- Scaffolded the project agent workspace (root `AGENTS.md` + `.bc-agent/` vault) with
  `bc-init-agent`. Ready for the grill → issues → drain workflow. Validation/file-layout
  stubs still TODO.
"""


OVERVIEW = """# Project Overview

> One-paragraph description of `__SLUG__`: what it is, who it's for, the stack. **TODO:** fill
> this in as the project takes shape.

## Glossary

The project's shared vocabulary — canonical names for the domain concepts, no implementation
detail. `grill-me` / `bc-grill-to-issues` (via `domain-modeling`) maintain this as the
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
`CONTEXT.md` / `docs/adr/` files. See `~/Sync/CONFIG/agents/pipeline.md` for the loop.

## Canonical repo-local planning surfaces

- **Glossary / domain facts:** the glossary section of `project/overview.md` (or a dedicated
  `project/glossary.md` if it grows). This is this project's `CONTEXT.md`-equivalent.
- **ADRs:** numbered files under `decisions/` using `templates/adr.md`.
- **Plans / PRDs:** durable planning artifacts under `project/`, linked from `index.md`.
- **Live cursor:** `tasks/active.md` while work is in flight.
- **Issue tracker:** GitHub issues via `gh`; ready agent work uses the `ready-for-agent` label;
  parked work uses `needs-human`.
- **Session log:** short durable notes appended to `log.md`.

## Planning — `/bc-grill-to-issues`

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
  allow rule in `policies/publish.yaml` (push + issue-close on `master`) or AFK push is
  blocked. **TODO:** confirm this repo is authorized before the first AFK run.
- **Validation gate.** The per-issue agent reads THIS repo's `conventions/validation.md` +
  `references/commands.md` for what "validated" means — not a generic test command. Criteria
  met **and** that validation clean = eligible to land.
- **Trunk-based, not PRs.** Each slice commits → pushes `master` → closes its issue with a
  sha + validation comment. Dependent slices then see prior work immediately.
- **Parking.** A slice that can't complete cleanly is parked: comment on the issue, swap
  `ready-for-agent` → `needs-human`, push nothing partial/RED. A run of consecutive parks
  trips the circuit-breaker and stops the loop.
- **Bookkeeping.** Treat landed slices like any project work: update `tasks/active.md`/
  `completed.md` and append a dated `log.md` line with issue numbers and commits.

## Clean handoff after planning

- Resolved scope in a `project/` plan/PRD page or GitHub parent issue.
- Durable trade-offs in `decisions/`.
- Independent `ready-for-agent` issues ordered by dependency.
- `tasks/active.md` clear or pointing at the in-flight plan.
- A dated `log.md` line with issue numbers and changed pages.
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
  (`~/Sync/CONFIG/agents/policies/publish.yaml`). After pushing, agents may close issues
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
- Agents start from `AGENTS.md` and `.bc-agent/index.md`.
- Personal/global wiki context stays separate.
- Durable discoveries are committed with the project.
"""


ACTIVE = """# Active Tasks

The live cursor for in-flight work. Keep this true every session — the first thing the next
agent reads after `index.md`. See [AGENTS.md](../AGENTS.md).

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

## __DATE__

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


def vault_files() -> dict[str, str]:
    return {
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
        "references/external-links.md": ref_stub(
            "External Links", "Useful external references for this project.\n\n_None yet._"),
        "conventions/planning-workflow.md": PLANNING_WORKFLOW,
        "conventions/validation.md": VALIDATION,
        "conventions/file-layout.md": FILE_LAYOUT,
        "conventions/git-and-commit-policy.md": GIT_POLICY,
        "decisions/adr-0001-local-project-agent-wiki.md": ADR_0001,
        "tasks/active.md": ACTIVE,
        "tasks/parking-lot.md": PARKING,
        "tasks/completed.md": COMPLETED,
        "templates/adr.md": TPL_ADR,
        "templates/plan.md": TPL_PLAN,
    }


def render(text: str, slug: str, date: str) -> str:
    return text.replace(SLUG, slug).replace(DATE, date)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="project (repo) root")
    ap.add_argument("--slug", required=True, help="project slug, kebab-case")
    ap.add_argument("--date", default=_dt.date.today().isoformat())
    ap.add_argument("--force", action="store_true", help="overwrite an existing vault")
    ap.add_argument("--force-root", action="store_true", help="overwrite an existing root AGENTS.md")
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    slug = args.slug.strip()
    if not root.is_dir():
        print(f"ERROR: root is not a directory: {root}")
        return 1
    if not slug or slug != slug.lower() or " " in slug:
        print(f"ERROR: slug must be lower-case kebab with no spaces: {slug!r}")
        return 1

    vault = root / ".bc-agent"
    if vault.exists() and not args.force:
        print(f"REFUSING: vault already exists at {vault} — use --force to overwrite (replaces it), "
              f"or remove/rename the existing .bc-agent first. Nothing written.")
        return 2

    written: list[str] = []

    # root AGENTS.md — only if absent (don't clobber a hand-written one)
    root_agents = root / "AGENTS.md"
    if root_agents.exists() and not args.force_root:
        print(f"NOTE: {root_agents} already exists — NOT overwritten. Merge the vault pointer "
              f"by hand (see the scaffolded `.bc-agent/AGENTS.md` and index for what to point at).")
    else:
        root_agents.write_text(render(ROOT_AGENTS, slug, args.date))
        written.append(str(root_agents))

    for relpath, text in vault_files().items():
        dest = vault / relpath
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render(text, slug, args.date))
        written.append(str(dest))

    # research + scratch dirs
    research = root / ".bc-agent" / "research"
    research.mkdir(parents=True, exist_ok=True)
    (research / "README.md").write_text(render(RESEARCH_README, slug, args.date))
    written.append(str(research / "README.md"))
    scratch = root / ".bc-agent" / "scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    gitkeep = scratch / ".gitkeep"
    gitkeep.write_text("")
    written.append(str(gitkeep))

    print(f"Scaffolded {len(written)} files under {root}:")
    for w in written:
        print(f"  {w}")
    print()
    print("Next: fill conventions/validation.md + file-layout.md as you learn the project; "
          "authorize this repo in policies/publish.yaml if you'll run /bc-drain-issues AFK; "
          "then /bc-grill-to-issues to plan the first feature.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
