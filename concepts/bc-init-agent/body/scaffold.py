#!/usr/bin/env python3
"""Scaffold a project's agent workspace + root AGENTS.md for the grill→issues→drain workflow.

Code, ops and hybrid (the visible layout) get work items in `work/`, decisions and
research in `docs/`, a root `glossary.md`, and agent mechanics only in `.bc-agent/`,
whose "Where things go" table names every path. Learning and knowledge keep the
`.bc-agent/` Markdown/Obsidian vault: the glossary lives in project/overview.md, ADRs
in decisions/, and conventions/planning-workflow.md redirects planning persistence
into the vault. TODO stubs (validation, file-layout) are filled by the first agents.

Idempotent and additive: creates only the files that are missing and leaves every
existing file untouched, so it is safe to re-run and safe to plug into a project
that already has files (including a hand-written root AGENTS.md). It NEVER deletes
anything. Existing files are overwritten only when explicitly forced: --force for
files under .bc-agent/, --force-root for the root AGENTS.md; nothing else is ever
overwritten. A visible-layout run on a project with earlier-layout paths under
.bc-agent/ writes nothing unless --allow-earlier-layout is given. --dry-run reports
without writing.

--migrate (code, ops, hybrid; needs an explicit --archetype) is the one exception to
"never deletes": it plans moving an earlier-layout vault in a clean git repository to
the visible layout and prints the plan; with --apply it performs only the mechanical
part (git mv, generated files, placeholder deletes, link rewrites), stages it and does
not commit. Everything else is listed for judgment and left untouched.

Usage:
  scaffold.py --root <repo-root> --slug <project-name> [--date YYYY-MM-DD]
              [--archetype code|ops|learning|knowledge|hybrid]
              [--force] [--force-root] [--allow-earlier-layout] [--dry-run]
  scaffold.py --root <repo-root> --slug <project-name> --archetype code|ops|hybrid
              --migrate [--apply]
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import subprocess
import urllib.parse
from pathlib import Path

SLUG = "__SLUG__"
DATE = "__DATE__"


# --- explicit teach host adapter (learning/hybrid overlays) -------------------
# This is a pointer and storage map, not a second copy of teach's pedagogy.
TEACH_ADAPTER_MARKER = "<!-- teach-host-adapter: v1 -->"
TEACH_ADAPTER = """<!-- teach-host-adapter: v1 -->
# Teach Skill Host Adapter

This file is the explicit opt-in marker for the standalone `teach` skill to use this
existing `.bc-agent` vault. It is a thin adapter, not a copy of teach's instructions,
a generic configuration framework, or a migration command. `bc-init-agent` owns the
host schema and orientation; `teach` owns the mapped pedagogy, evidence, and spaced
review state.

Read the canonical teach instructions and formats from
`<agent-concepts>/concepts/teach/body/`. Resolve those paths against this vault root.
Do not invoke `bc-init-agent` from `teach`, move standalone files, or create a second
learning/knowledge home. If a standalone teach workspace and this host both contain
state, stop and ask the user which home to use; preserve the standalone home by default.
A valid adapter has this exact first line and the complete hosted path table below; a
prefix-only or altered-map file is incomplete and is not a host contract.

## Hosted teach path map

When invoked from the project root, `<teach-root>` is `.bc-agent`; when invoked from inside
that vault, `<teach-root>` is the current `.bc-agent` directory. All paths below are relative
to `<teach-root>`:

| Teach surface | Hosted path | Owner |
|---|---|---|
| Mission | `learning/plan.md` (no hosted `MISSION.md`) | `teach` |
| Review queue | `learning/review.md` | `teach` |
| Learning records | `learning/records/` | `teach` |
| Lessons and session artifacts | existing `sessions/` (never `learning/sessions/`) | `teach` |
| Notes | `learning/notes.md` | `teach` |
| Raw sources | existing `sources/` | `teach` |
| Compiled knowledge / wiki concepts | existing `concepts/` | `teach` |
| Resource catalog | `references/teach-resources.md` | `teach` |
| Glossary | the existing Glossary section of `project/overview.md` | `teach` |
| Catalog and history | shared `index.md` and `log.md` | `bc-init-agent` host schema; `teach` updates teach entries |

With a valid marker, host search-first retrieval is for knowledge pages and learning records:
use the host's canonical search path, never the index as a lookup. `teach` may directly read
mapped known state (mission, review queue, and notes) plus shared `index.md`/recent `log.md`
for session orientation and bookkeeping; those are not knowledge lookups. When this marker is
valid, `teach` owns the Glossary section of `project/overview.md`; planning and maintenance
skills must leave that section alone, while non-glossary host sections remain available to
host maintenance.

## Explicit destructive migration — only on a user request

Choosing the host for reading or writing is not migration. Only perform this operation when
the user explicitly asks to **consolidate** or **migrate** the standalone teach workspace into
this host, never because a marker was discovered or as part of another action. This operation
is destructive: it copies/moves content into the host and then **deletes the standalone
originals**. Tell the user plainly that the originals will be deleted before doing it.

Use a copy-then-verify sequence. Inventory every existing standalone item, prepare its mapped
host destination, and preflight every destination for collisions and writability before any
write. Verify that every destination is complete before removing any original; for directories,
verify every content-bearing file, not merely the directory. Content-bearing records, sources,
knowledge pages, and session artifacts must arrive byte-identical (compare bytes or hashes).
The mission, notes, queue, catalog/history, glossary, and resource catalog may be reformatted
to their host formats, but verify every source item, row, entry, or glossary term is represented.
Do not overwrite unrelated host content or proceed through a destination conflict.

If any destination is missing, incomplete, conflicting, or unwritable, stop and report the
failure with **all standalone originals intact**; delete nothing. Only after every mapped
destination passes verification may the corresponding standalone files and directories be
removed. Choosing the host without an explicit migration request leaves every standalone file
untouched.

| Standalone source | Hosted destination (relative to `<teach-root>`) | Verification |
|---|---|---|
| `MISSION.md` | `learning/plan.md` | mission content represented in the host mission format |
| `REVIEW.md` | `learning/review.md` | every review item and scheduling value represented |
| `learning-records/*` | `learning/records/` | each record arrives byte-identical |
| `lessons/*` | existing `sessions/` | each lesson/session artifact arrives byte-identical |
| `NOTES.md` | `learning/notes.md` | every note represented |
| `sources/*` | existing `sources/` | each source arrives byte-identical |
| `wiki/*` | existing `concepts/` | each knowledge page arrives byte-identical |
| `RESOURCES.md` | `references/teach-resources.md` | every catalog entry represented |
| `GLOSSARY.md` | Glossary section of `project/overview.md` | every term and definition represented |
| `index.md` | shared `index.md` | every teach catalog entry represented without replacing host orientation |
| `log.md` | shared `log.md` | every teach history entry represented without replacing host history |

The host's `AGENTS.md`, `index.md`, and `log.md` remain shared orientation/catalog
surfaces. `bc-wiki-maintain` may search host context and promote ordinary host evidence,
but it must not fabricate learning evidence, edit teach-owned records or Glossary terms, or
advance the review queue. Raw sources remain immutable. Existing host files are authoritative
in place; this marker alone implies no migration or copied pedagogy.
"""


def _hybrid_teach_adapter() -> str:
    """The adapter for a visible-layout hybrid host: only the glossary differs.

    The glossary is the project's root `glossary.md`, shared with the project, so a
    hybrid project keeps one vocabulary instead of a second teach-only glossary.
    """
    text = TEACH_ADAPTER
    for old, new in (
        ("| Glossary | the existing Glossary section of `project/overview.md` | `teach` |",
         "| Glossary | the project's root `glossary.md` (`../glossary.md`), shared with the project | the project; `teach` adds and refines learner terms |"),
        ("""valid, `teach` owns the Glossary section of `project/overview.md`; planning and maintenance
skills must leave that section alone, while non-glossary host sections remain available to
host maintenance.""",
         """valid, the Glossary is `glossary.md` at the project root, one level above `<teach-root>`,
shared with the project: `teach` adds and refines the terms the learner needs there, in the
file's one-line format, and does not remove or redefine project terms without asking;
`domain-modeling` and planning skills keep using the same file."""),
        ("| `GLOSSARY.md` | Glossary section of `project/overview.md` | every term and definition represented |",
         "| `GLOSSARY.md` | the project's root `glossary.md` (`../glossary.md`) | every term represented in the one-line format; no project term removed or redefined without asking |"),
        ("""but it must not fabricate learning evidence, edit teach-owned records or Glossary terms, or
advance the review queue.""",
         """but it must not fabricate learning evidence, edit teach-owned records, or advance the
review queue. The shared root `glossary.md` is a project file: keep the terms the learner
needs when maintaining it."""),
    ):
        if old not in text:
            raise RuntimeError(f"TEACH_ADAPTER text changed; update replacement {old!r}")
        text = text.replace(old, new)
    return text


TEACH_ADAPTER_HYBRID = _hybrid_teach_adapter()


def _teach_adapter_map_rows(text: str) -> tuple[tuple[str, str, str], ...] | None:
    """Return the hosted map rows from a marker, or None when its table is malformed."""
    lines = text.splitlines()
    try:
        heading = lines.index("## Hosted teach path map")
    except ValueError:
        return None

    rows: list[tuple[str, str, str]] = []
    table_started = False
    for line in lines[heading + 1:]:
        if not table_started:
            if line.startswith("| Teach surface | Hosted path | Owner |"):
                table_started = True
            continue
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells == ["---", "---", "---"]:
            continue
        if len(cells) != 3:
            return None
        rows.append((cells[0], cells[1], cells[2]))

    return tuple(rows) if table_started else None


def is_valid_teach_adapter(text: str) -> bool:
    """Use one structural rule for scaffold upgrade notes and host selection."""
    return (
        text.startswith(TEACH_ADAPTER_MARKER + "\n")
        and _teach_adapter_map_rows(text) in {
            _teach_adapter_map_rows(TEACH_ADAPTER), _teach_adapter_map_rows(TEACH_ADAPTER_HYBRID)}
        and bool(_teach_adapter_map_rows(text))
    )


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
- For `grilling` + `domain-modeling` or `bc-plan-to-issues` → `bc-drain-issues` work, apply
  `conventions/planning-workflow.md`: it maps generic `glossary.md`/`docs/adr/` persistence
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
- When `references/teach-skill.md` exists, read it before using `teach`: it is the
  explicit adapter for the host's learning paths. `teach` owns the mapped pedagogy,
  evidence, review state, and the Glossary section of `project/overview.md`; this vault
  owns host schema/orientation. Host search-first is for knowledge and learning-record
  retrieval. Teach may directly read mapped known mission/review/notes state and the shared
  catalog/recent history for session bookkeeping; those are not hub lookups. Do not create
  a second `learning/sessions/` directory or migrate a standalone teach workspace. A host
  choice alone never migrates it; destructive migration is teach's separate, explicit-request
  operation and deletes originals only after destination verification.
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

Link only targets that resolve inside this vault; leave external source-tree references as
inline code because they cannot participate in this graph.

## Always useful

- [project/overview.md](project/overview.md)
- [references/commands.md](references/commands.md)
- [conventions/validation.md](conventions/validation.md)

## Planning / workflow work

- [conventions/planning-workflow.md](conventions/planning-workflow.md)
- [conventions/architecture-runway.md](conventions/architecture-runway.md)
- [references/agent-skills.md](references/agent-skills.md)
- [conventions/git-and-commit-policy.md](conventions/git-and-commit-policy.md)
- [conventions/validation.md](conventions/validation.md)
- [log.md](log.md)

## Research or PRD work

- [conventions/planning-workflow.md](conventions/planning-workflow.md)
- [project/overview.md](project/overview.md)
- [research/README.md](research/README.md)
- [templates/plan.md](templates/plan.md)

## File / layout work

- [conventions/file-layout.md](conventions/file-layout.md)
- [references/paths.md](references/paths.md)

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
detail. When `references/teach-skill.md` is a valid adapter, `teach` owns this Glossary section
and `bc-plan-to-issues` and maintenance leave it unchanged. Without that adapter,
`domain-modeling` (paired with `grilling` directly or used through `bc-plan-to-issues`) maintains
this as the project's `glossary.md`-equivalent. Keep it a pure glossary.

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
`glossary.md` / `docs/adr/` files. See `$AGENT_CONCEPTS/docs/pipeline.md` for the loop.

## Planning intent trigger

When the human sounds like they are planning codebase work — feature ideas, refactor
direction, architecture strategy, implementation approach, or issue slicing — ask whether
they want to enter `/bc-plan-to-issues` before writing implementation code. If the request is
architectural runway rather than a settled feature, offer `/improve-codebase-architecture`
first. If they clearly ask for a concrete edit/fix, proceed normally.

## Canonical repo-local planning surfaces

- **Glossary / domain facts:** the Glossary section of `project/overview.md` (or a dedicated
  `project/glossary.md` if it grows). Without a valid teach adapter, this is this project's
  `glossary.md`-equivalent and `domain-modeling` / `bc-plan-to-issues` maintain it. With the adapter,
  `teach` owns the Glossary section; planning and maintenance skills leave that section alone.
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
persist to generic `glossary.md` / `docs/adr/`, persist here instead:

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
- **Claim before work.** Follow `/bc-drain-issues`' authorized claim protocol: no-force create-if-absent or lease-guarded reuse of a Released Claim Marker; skip a lost race before dispatch.
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

The generated `references/teach-skill.md` is an explicit, thin adapter for the
standalone `teach` skill. It maps teach's mission to `learning/plan.md`, its review
queue to `learning/review.md`, records to `learning/records/`, notes to
`learning/notes.md`, raw sources to `sources/`, compiled knowledge to `concepts/`,
resources to `references/teach-resources.md`, the glossary to the existing Glossary
section of `project/overview.md`, and catalog/history to the shared `index.md`/`log.md`.
When the adapter is valid, teach owns that Glossary section; planning and maintenance
skills leave it alone. Lessons and session artifacts use the existing `sessions/`
directory; never create `learning/sessions/`. The adapter does not copy teach pedagogy
or migrate standalone state. A host choice alone never migrates it; teach's separate
explicit migration operation is destructive and verifies destinations before deleting
standalone originals.

- `learning/` — host learning paths and the teach-owned mission/review/records/notes.
- `sources/` — immutable raw source material.
- `concepts/` — compiled knowledge pages.
- `questions/` — open questions only; teach review prompts belong in `learning/review.md`.
- `sessions/` — dated tutoring/session notes and lesson artifacts.
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
- `learning/` / `sources/` / `concepts/` / `sessions/` for teaching and study. When the
  teach adapter is present, use its exact mapping and keep `sessions/` shared; do not
  create `learning/sessions/` or a second review/knowledge home.
- In hybrid learning/knowledge work, immutable raw material stays in the existing `sources/`
  and compiled source/entity/concept/synthesis pages stay under the existing `concepts/` tree;
  do not add a parallel `raw/` or `wiki/` tree.
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
            "learning/plan.md": "# Mission: TODO\n\nThis is the hosted mission surface for `teach`; the skill owns its pedagogy and keeps the mission concrete. Use `<agent-concepts>/concepts/teach/body/MISSION-FORMAT.md` for the format.\n\n## Why\n\nTODO.\n\n## Success looks like\n\n- TODO.\n\n## Constraints\n\n- TODO.\n\n## Out of scope\n\n- TODO.\n\nThe hosted review queue lives at `learning/review.md`; do not create a second `REVIEW.md`.\n",
            "learning/review.md": "# Review Queue\n\nThe `teach` skill owns this spaced-repetition queue. Use `<agent-concepts>/concepts/teach/body/REVIEW-FORMAT.md` and its `due.py` script; keep review state here rather than in `questions/` or a root `REVIEW.md`.\n",
            "learning/notes.md": "# Teach Notes\n\nThe `teach` skill owns learner preferences and session notes here. This is the hosted counterpart of standalone `NOTES.md`; do not create a duplicate root notes file.\n",
            "learning/records/.gitkeep": "",
            "sources/README.md": "# Sources\n\nImmutable raw source material for the hosted `teach` knowledge layer. The `teach` skill owns ingestion and citations; preserve source files once saved.\n",
            "concepts/README.md": "# Concepts\n\nCompiled knowledge pages for the hosted `teach` knowledge layer. Cite the existing `sources/` material; do not create a parallel `wiki/` for this learning workspace.\n",
            "questions/README.md": "# Questions\n\nOpen questions only. Teach review prompts and scheduling belong in `learning/review.md`; all learning evidence belongs in `learning/records/`.\n",
            "sessions/README.md": "# Sessions\n\nThe existing shared directory for dated tutoring/session notes and lesson artifacts from `teach`. Do not create `learning/sessions/`.\n",
            "references/teach-skill.md": TEACH_ADAPTER,
            "references/teach-resources.md": "# Teach Resources\n\nThe hosted resource catalog for `teach`. Use `<agent-concepts>/concepts/teach/body/RESOURCES-FORMAT.md`; raw material belongs in the existing `sources/` directory.\n",
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
        for name in ("ops", "learning"):
            files |= {path: text for path, text in archetype_files(name).items() if path != "archetype.md"}
        files |= {
            "concepts/entities/README.md": "# Entities\n\nPeople, projects, tools, organizations, services, and libraries compiled from the existing immutable `sources/` directory.\n",
            "concepts/syntheses/README.md": "# Syntheses\n\nCross-source summaries, maps, contradictions, and evidence gaps compiled under the existing `concepts/` knowledge home.\n",
        }
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


# --- visible layout (code, ops, hybrid) ----------------------------------------
# Project knowledge and the work lifecycle live in ordinary folders at the repo
# root; `.bc-agent/` keeps agent mechanics only. Learning and knowledge
# archetypes keep the vault above unchanged.

VISIBLE_ARCHETYPES = frozenset({"code", "ops", "hybrid"})
WORK_STAGES = ("1-planned", "2-active", "3-done", "4-dropped")
WHERE_THINGS_GO_HEADING = "## Where things go"
# Stable role keys of the "Where things go" table. Other skills look a role up
# with parse_where_things_go() instead of assuming a path.
LAYOUT_ROLES = (
    "work-planned", "work-active", "work-done", "work-dropped", "ideas",
    "decisions", "research", "glossary", "requirements", "architecture",
    "project-skills", "project-agents",
)

_BASE_ROWS = (
    ("work-planned", "work/1-planned/", "agreed work that has not started"),
    ("work-active", "work/2-active/", "work in progress; several items may be active"),
    ("work-done", "work/3-done/", "finished work, always inside a `<year>-<month>/` folder such as `2026-03/`"),
    ("work-dropped", "work/4-dropped/", "abandoned work and rejected requests, with the reason"),
    ("ideas", "work/0-ideas.md", "undecided ideas and observations, one line each"),
    ("decisions", "docs/decisions/", "one numbered decision record per file"),
    ("research", "docs/research/", "one `<date>-<slug>/` folder per investigation"),
    ("glossary", "glossary.md", "canonical names for the project's domain concepts"),
    ("requirements", "docs/PRD.md", "product-level spec, created on first need; a feature's requirements live in its work item"),
    ("architecture", "ARCHITECTURE.md", "created on first need"),
    ("project-skills", ".agents/skills/", "created on first need; one `local-<name>/` folder per skill, with a README naming shared copies and how to refresh them"),
    ("project-agents", "", "not yet decided; ask the owner before creating project-specific agents"),
)
_OPS_ROWS = (
    ("components", "docs/components/", "verified state of real systems, hosts, tools and services"),
)
_TEACH_ROWS = (
    ("teach-workspace", ".bc-agent/references/teach-skill.md", "path map of the hosted `teach` workspace; `teach` owns `learning/`, `sources/`, `concepts/`, `sessions/`, `questions/` and `index.md` under `.bc-agent/`, and shares the project's `glossary.md`"),
)


def layout_rows(archetype: str) -> tuple[tuple[str, str, str], ...]:
    rows = _BASE_ROWS
    if archetype in {"ops", "hybrid"}:
        rows += _OPS_ROWS
    if archetype == "hybrid":
        rows += _TEACH_ROWS
    return rows


def where_things_go_table(archetype: str) -> str:
    lines = ["| Role | Path | Notes |", "| --- | --- | --- |"]
    for role, path, note in layout_rows(archetype):
        lines.append(f"| {role} | {f'`{path}`' if path else '—'} | {note} |")
    return "\n".join(lines)


_WHERE_THINGS_GO_LINE = re.compile(r"^" + re.escape(WHERE_THINGS_GO_HEADING) + r"[ \t]*\r?$", re.M)
_UNDECIDED_PATH_CELLS = {"", "—", "-"}


def parse_where_things_go(text: str) -> dict[str, str]:
    """Map each role key of a "Where things go" table to its path.

    Paths are relative to the project root. A backticked path is unwrapped; a plain
    path is returned stripped; only `—`, `-` or an empty cell means "no decided path"
    and maps to an empty string. Raises ValueError when the heading line is missing,
    when the section has no table rows, or when a role appears twice.
    """
    match = _WHERE_THINGS_GO_LINE.search(text)
    if not match:
        raise ValueError(f"no {WHERE_THINGS_GO_HEADING!r} section")
    section = re.split(r"^## ", text[match.end():], maxsplit=1, flags=re.M)[0]
    result: dict[str, str] = {}
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 2 or cells[0] == "Role" or set(cells[0]) <= {"-", ":", " "}:
            continue
        role, path = cells[0], cells[1]
        if role in result:
            raise ValueError(f"role {role!r} appears twice in {WHERE_THINGS_GO_HEADING!r}")
        if path.count("`") >= 2:
            path = path.split("`")[1].strip()
        result[role] = "" if path in _UNDECIDED_PATH_CELLS else path
    if not result:
        raise ValueError(f"{WHERE_THINGS_GO_HEADING!r} section has no table rows")
    return result


VISIBLE_ROOT = """# Agent instructions for __SLUG__

Before non-trivial work, read `.bc-agent/AGENTS.md`. It holds the "Where things go" table
and the work-item rules; pick further context with `.bc-agent/map.md`.

## At a glance

- `work/` — what is planned, active, done and dropped. The folder an item sits in is its status.
- `docs/decisions/`, `docs/research/` — decision records and investigations.
- `glossary.md` — the project's vocabulary. Use its terms in code, issues and docs.
- `.bc-agent/` — agent mechanics only: instructions, conventions, references, templates, log.

## Planning loop trigger

If the request sounds like planning future work (feature ideas, architecture direction,
slicing, "what should we build"), pause and ask whether to enter `/bc-plan-to-issues`
before implementing. A concrete edit or fix proceeds normally. When the question is
architectural runway, check `.bc-agent/conventions/architecture-runway.md` and offer
`/improve-codebase-architecture` first. Skill map: `.bc-agent/references/agent-skills.md`.

## Scope rules

- Project knowledge goes where the table says, in the same commit as the work it describes.
- Source-tree README files, other `docs/` pages and JSDoc follow `codebase-docs`. It does
  not apply to the paths named in the "Where things go" table: those are records.
- Keep personal, cross-project and machine-global knowledge out of this repository.
- No secrets or `.env` values anywhere in tracked files.

## Publishing

Push commits or close issues only when a rule in the user-owned publish policy
(`~/.config/agent-concepts/publish.yaml`) authorizes it. No matching rule: ask.
"""

VISIBLE_AGENTS = """# __SLUG__ — agent session protocol

Read this file before non-trivial work. Project knowledge lives in ordinary folders at the
repository root so people can browse it; `.bc-agent/` holds agent mechanics only.

## Where things go

Paths are relative to the repository root. Skills look a role up in this table instead of
assuming a path, so change a path here when the project keeps something elsewhere.

__TABLE__

__DEFAULT_PATH_RULE__

## Work items

A work item is one feature or plan. Template: [templates/work-item.md](templates/work-item.md).

- **The folder is the status.** Move an item between stage folders with `git mv`, in the
  same commit as the work that changes its state. Why: the tree then always shows what is
  planned, active, done and dropped, with nothing else to keep in step.
- **No `Status:` line in an item.** Why: a written status can disagree with the folder.
- **Finished items go into `work/3-done/<year>-<month>/`** (for example `work/3-done/2026-03/`);
  create the month folder when it is missing, and never put an item directly in `3-done/`.
  Why: one rule from the first item on means the folder never needs reorganizing.
- **Dropped work and rejected requests go to `work/4-dropped/`**, with the reason under
  `## Outcome`. Why: a recorded "no, because" stops the same idea being re-argued.
  Asked to delete an item instead, move it anyway and write what you know, even if that is
  only "Dropped <date>; no reason given". Why: a deleted item frees its number for reuse, so
  older references to that number would point at a different item.
- **Names are `<3-digit number>-<slug>`**, for example `012-search-ranking`. The next number
  is the highest number in any stage folder, including the month folders under `3-done/`,
  plus one. Why: a short number is easy to cite and survives a rename of the slug.
- **Only the main checkout creates numbered items.** Working in a git worktree, add a line
  to `work/0-ideas.md` instead. Why: two worktrees cannot see each other's numbers and
  would pick the same one.
- **A small item is one file; a large one is a folder** `NNN-slug/` holding `plan.md` (its
  `## Steps` are the slices) and `requirements.md`, plus any evidence worth keeping. The folder
  moves as a whole. Why: everything about a feature stays in one place through its whole
  life, and the steps already are the slice map, so separate slice files would drift.
- **Several items may be active at once.**
- **GitHub issues are optional.** When one exists, record its number on the item's `Issue:`
  line. Why: the folders are the source of truth; an issue is a pointer to them.
- **Undecided ideas and observations** are one line each in `work/0-ideas.md`. An idea
  becomes a numbered item in `work/1-planned/` once someone decides to do it.
- **Open questions live in work items.** An unanswered question that blocks a piece of work
  is a step in that work item. A standalone question that someone must investigate is a
  planned work item whose answer lands in `docs/research/`. One not worth an item yet is a
  line in `work/0-ideas.md`. Why: `work/` stays the single place that shows what is pending.

## Keep it current

| When you… | Do this |
| --- | --- |
| Start non-trivial work | Read the items in `work/2-active/`, then pick context with [map.md](map.md). |
| Begin agreed work | Create the item from the template, or `git mv` it from `1-planned/` to `2-active/`. |
| Finish a step | Check its box in the item. |
| Finish or drop an item | Fill `## Outcome`, then `git mv` it to its done month folder or to `4-dropped/`. |
| Make an architectural or hard-to-reverse choice | Add a numbered record under `docs/decisions/` from [templates/adr.md](templates/adr.md). |
| Investigate something at length | Write it up in a dated folder under `docs/research/`. |
__OPS_KEEP_CURRENT__| Sharpen domain vocabulary | Update `glossary.md`. |
| Learn a recurring command | Add it to [references/commands.md](references/commands.md). |
| Learn a durable fact with no better home | Append one to three lines to [log.md](log.md). |
| Find a page that is wrong | Fix it in the same commit. Never leave a stale claim. |

## Discipline

- Do not invent facts. Mark anything unverified as unverified.
- Inspect `git status` first, stage only your own changes, and commit before finishing.
- Validation commands: [conventions/validation.md](conventions/validation.md). Git and
  publishing: [conventions/git-and-commit-policy.md](conventions/git-and-commit-policy.md).
"""

HYBRID_TEACH_SECTION = """
## Hosted teach workspace

This project also hosts a `teach` learning workspace inside `.bc-agent/`. Read
[references/teach-skill.md](references/teach-skill.md) before using `teach`: it is the
explicit adapter for the host's learning paths. `teach` owns the mapped pedagogy,
evidence and review state. There is one glossary: `glossary.md` at the repository root,
shared with the project. `teach` adds and refines the terms the learner needs there and
does not remove or redefine project terms without asking.
Host search-first is for knowledge and learning-record retrieval. Teach may directly read
mapped known mission/review/notes state and the shared catalog/recent history for session
bookkeeping. Do not create a second `learning/sessions/` directory or migrate a standalone
teach workspace.

The read path below applies to teach knowledge pages and learning records under `.bc-agent/`.
Project orientation is the "Where things go" table above, not `index.md`; `index.md`
catalogs only the teach workspace.

"""

VISIBLE_MAP = """# Context Map

Choose the smallest set of pages for the task. Link only targets that resolve inside this vault
(`.bc-agent/`); name files outside it in inline code, relative to the repository root.

## Always useful

- [AGENTS.md](AGENTS.md)
- [references/commands.md](references/commands.md)
- [conventions/validation.md](conventions/validation.md)

## Planning and workflow

- [templates/work-item.md](templates/work-item.md)
- [conventions/architecture-runway.md](conventions/architecture-runway.md)
- [references/agent-skills.md](references/agent-skills.md)
- [conventions/git-and-commit-policy.md](conventions/git-and-commit-policy.md)
- [log.md](log.md)

## Decisions and layout

- [templates/adr.md](templates/adr.md)
- [conventions/file-layout.md](conventions/file-layout.md)
__OPS_MAP__
## Outside this folder

Work items are in `work/` (ideas in `work/0-ideas.md`), decision records in
`docs/decisions/`, investigations in `docs/research/`, and vocabulary in `glossary.md`.
The "Where things go" table in `AGENTS.md` is the full list.
"""

VISIBLE_FILE_LAYOUT = """# File Layout

Where project knowledge and work items go: the "Where things go" table in
[AGENTS.md](../AGENTS.md).

> **TODO:** record the real source and build paths once known.

## Agent guidance

- Confirm source/build relationships before editing generated-looking files.
- The four `work/` stage folders keep their `.gitkeep` file permanently. Why: git drops an
  empty folder, and every stage must stay visible even when it holds no items.
"""

WORK_ITEM = """# <title>

Why: <the problem or goal, in one or two sentences>
Done when: <the observable outcome that means this is finished>
Issue: <optional issue number; delete the line when there is none>

## Steps

- [ ] <first step>

## Outcome

<Filled when the item is finished or dropped: what happened, or why it was dropped.>
"""

IDEAS = """# Ideas

Undecided ideas and observations, one line each, newest at the bottom. An idea that
someone decides to do becomes a numbered work item in `1-planned/`; delete its line here.
"""

GLOSSARY = """# Glossary

Canonical names for this project's domain concepts: one line each, no implementation
detail. Use these terms in code, issues and docs.

_None captured yet._
"""

HYBRID_INDEX = """# __SLUG__ — teach workspace catalog

Catalog of the hosted `teach` workspace in this folder. `teach` adds its entries here.
Project work, decisions and research are not catalogued here; see the "Where things go"
table in [AGENTS.md](AGENTS.md).

- [Teach host adapter](references/teach-skill.md)
- [Teach resources](references/teach-resources.md)
- [Mission](learning/plan.md)
- [Review queue](learning/review.md)
- [Notes](learning/notes.md)
- [Sources](sources/README.md)
- [Concepts](concepts/README.md)
- [Questions](questions/README.md)
- [Sessions](sessions/README.md)
- [Log](log.md)
"""


DEFAULT_PATH_RULE = """When a skill names a default path for one of these roles (for example `docs/adr/`,
`.bc-agent/project/overview.md` or `.bc-agent/out-of-scope/`), use this table's path for that
role instead. Why: shared skills are written for several layouts, and this table is the
project's own answer."""

VISIBLE_OPS_KEEP_CURRENT = """| Check the state of a real system | Update its page under `docs/components/` from [templates/component.md](templates/component.md). |
| Record a finding | Write it under `docs/research/` from [templates/finding.md](templates/finding.md). |
"""

VISIBLE_OPS_MAP = """
## Operations

- [templates/component.md](templates/component.md)
- [templates/finding.md](templates/finding.md)
"""

VISIBLE_TEACH_MAP = """
## Hosted teach workspace

- [references/teach-skill.md](references/teach-skill.md)
- [index.md](index.md)
"""


def _guarded(text: str, replacements: tuple[tuple[str, str], ...], name: str) -> str:
    for old, new in replacements:
        if old not in text:
            raise RuntimeError(f"{name} text changed; update replacement {old!r}")
        text = text.replace(old, new)
    return text


def _visible_log() -> str:
    return _guarded(LOG, (
        ("""- Scaffolded the project agent workspace (root `AGENTS.md` + `.bc-agent/` vault) with
  `bc-init-agent`. Ready for the grill → issues → drain workflow. Validation/file-layout
  stubs still TODO.""", """- Scaffolded the project agent workspace with `bc-init-agent`: root `AGENTS.md`,
  `glossary.md`, `work/`, `docs/` and the `.bc-agent/` mechanics. Ready for the
  grill → issues → drain workflow. Validation/file-layout stubs still TODO."""),
    ), "LOG")


def _visible_agent_skills() -> str:
    return _guarded(AGENT_SKILLS, (
        ("`codebase-docs` — README / existing `docs/` / JSDoc only; not this vault.",
         "`codebase-docs` — README files, other `docs/` pages and JSDoc; not `.bc-agent/` and not the paths named in the \"Where things go\" table in `.bc-agent/AGENTS.md`, which are records."),
        ("- Wiki maintenance: `/bc-wiki-maintain` — compute vault health, find index/search drift, and promote durable log entries without silently resolving contradictions.\n",
         ""),
        ("In code/hybrid wikis, run", "Run"),
    ), "AGENT_SKILLS")


def _visible_runway() -> str:
    replacements = (
        ("For code/hybrid wikis, this page", "This page"),
        ("-- .bc-agent |", "-- docs/research |"),
        ("-- .bc-agent/project .bc-agent/tasks", "-- docs work"),
        ("normal project\nwiki location", "dated folder under\n`docs/research/`"),
        ("\n\nThe `review_tip` lookup is deliberately",
         "\n\nThe snippet uses the default paths. If this project's \"Where things go\" table in\n"
         "`.bc-agent/AGENTS.md` names other paths, substitute the research and work paths from the\n"
         "\"Where things go\" table for `docs/research` and `docs work` before running it; otherwise\n"
         "the count misses the project's real planning surfaces.\n\nThe `review_tip` lookup is deliberately"),
    )
    return _guarded(ARCHITECTURE_RUNWAY, replacements, "architecture runway")


def visible_targets(root: Path, slug: str, date: str, archetype: str) -> list[tuple[Path, str, bool]]:
    """Scaffold targets for archetypes that use the visible layout."""
    has_ops = archetype in {"ops", "hybrid"}
    agents = (VISIBLE_AGENTS.replace("__TABLE__", where_things_go_table(archetype))
              .replace("__DEFAULT_PATH_RULE__", DEFAULT_PATH_RULE)
              .replace("__OPS_KEEP_CURRENT__", VISIBLE_OPS_KEEP_CURRENT if has_ops else ""))
    map_text = VISIBLE_MAP.replace("__OPS_MAP__", VISIBLE_OPS_MAP if has_ops else "")
    if archetype == "hybrid":
        map_text += VISIBLE_TEACH_MAP
    vault_files_: dict[str, str] = {
        "AGENTS.md": agents,
        "map.md": map_text,
        "log.md": _visible_log(),
        "conventions/validation.md": VALIDATION,
        "conventions/file-layout.md": VISIBLE_FILE_LAYOUT,
        "conventions/architecture-runway.md": _visible_runway(),
        "conventions/git-and-commit-policy.md": GIT_POLICY,
        "references/commands.md": ref_stub(
            "Commands", "Recurring project commands. **TODO:** fill as discovered.\n\n_None yet._"),
        "references/agent-skills.md": _visible_agent_skills(),
        "templates/adr.md": TPL_ADR + "\n<!-- Save as `docs/decisions/NNNN-<slug>.md`. -->\n",
        "templates/work-item.md": WORK_ITEM,
    }
    root_files: dict[str, str] = {
        "glossary.md": GLOSSARY,
        "work/0-ideas.md": IDEAS,
        **{f"work/{stage}/.gitkeep": "" for stage in WORK_STAGES},
        "docs/decisions/.gitkeep": "",
        "docs/research/.gitkeep": "",
    }
    if has_ops:
        ops = archetype_files("ops")
        root_files["docs/components/README.md"] = ops["components/README.md"]
        for name in ("component", "finding"):
            vault_files_[f"templates/{name}.md"] = ops[f"templates/{name}.md"]
    if archetype == "hybrid":
        # Exactly the paths the hosted teach adapter maps; nothing else from the vault.
        vault_files_.update(
            {path: text for path, text in archetype_files("learning").items() if path != "archetype.md"})
        vault_files_.update(
            {path: text for path, text in archetype_files("hybrid").items() if path.startswith("concepts/")})
        vault_files_["references/teach-skill.md"] = TEACH_ADAPTER_HYBRID
        vault_files_["index.md"] = HYBRID_INDEX
        vault_files_["AGENTS.md"] = agents + HYBRID_TEACH_SECTION + CANONICAL_VAULT_READ_PATH
    vault = root / ".bc-agent"
    result = [(root / "AGENTS.md", render(VISIBLE_ROOT, slug, date), True)]
    result += [(vault / path, render(text, slug, date), False) for path, text in vault_files_.items()]
    result += [(root / path, render(text, slug, date), False) for path, text in root_files.items()]
    return result


def targets(root: Path, slug: str, date: str, archetype: str = "code") -> list[tuple[Path, str, bool]]:
    """Every file the scaffold owns: (destination, rendered content, is_root_AGENTS)."""
    if archetype in VISIBLE_ARCHETYPES:
        return visible_targets(root, slug, date, archetype)
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


def _teach_notes(root: Path) -> list[str]:
    """Hints about an existing teach adapter or standalone teach state."""
    vault = root / ".bc-agent"
    notes: list[str] = []
    adapter = vault / "references" / "teach-skill.md"
    if adapter.exists():
        try:
            adapter_text = adapter.read_text(encoding="utf-8")
        except OSError:
            adapter_text = ""
        if not is_valid_teach_adapter(adapter_text):
            notes.append(
                "existing references/teach-skill.md is not the explicit v1 teach adapter "
                "(exact first line plus the complete hosted path map); merge the generated "
                "path map by hand after checking existing state"
            )
    standalone_names = {
        "MISSION.md", "REVIEW.md", "GLOSSARY.md", "RESOURCES.md", "NOTES.md",
        "learning-records", "lessons",
    }
    # Compare exact directory entry names: on a case-insensitive filesystem a hybrid
    # project's shared root `glossary.md` would otherwise answer to `GLOSSARY.md`.
    try:
        root_names = {entry.name for entry in root.iterdir()}
    except OSError:
        root_names = set()
    if standalone_names & root_names:
        notes.append(
            "standalone teach state exists outside .bc-agent; do not migrate or copy it "
            "automatically — preserve it and ask the user before choosing between competing homes"
        )
    return notes


EARLIER_LAYOUT_PATHS = (
    "tasks", "decisions", "research", "scratch", "out-of-scope", "home.md",
    "components", "findings", "open-questions", "plans",
    "conventions/planning-workflow.md", "templates/plan.md", "project", "index.md",
)


def earlier_layout_paths(root: Path, archetype: str) -> list[str]:
    """Paths under .bc-agent/ that belong to the earlier vault layout.

    Hybrid legitimately generates `index.md` as its teach catalog, so that is not
    counted for hybrid.
    """
    own = {"index.md"} if archetype == "hybrid" else set()
    vault = root / ".bc-agent"
    return sorted(name for name in EARLIER_LAYOUT_PATHS
                  if name not in own and (vault / name).exists())


def _inside_vault_map_bullet(root: Path, line: str) -> bool:
    """True for an inline-code map bullet whose target is an existing file inside .bc-agent/.

    A bullet naming a path outside the vault (relative to the repository root, as the
    map tells agents to write it) is not a missing link, even before that path exists:
    some project files are created on first need.
    """
    if not line.startswith("- `"):
        return False
    target = line[3:].split("`", 1)[0]
    if not target or target.startswith("../"):
        return False
    return (root / ".bc-agent" / target).is_file()


def upgrade_notes(root: Path, archetype: str) -> list[str]:
    """Manual merge hints for existing files that were intentionally left untouched."""
    vault = root / ".bc-agent"
    notes: list[str] = []
    if archetype in VISIBLE_ARCHETYPES:
        map_path = vault / "map.md"
        if map_path.exists() and any(
                _inside_vault_map_bullet(root, line)
                for line in map_path.read_text(errors="ignore").splitlines()):
            notes.append("`.bc-agent/map.md` should use real Markdown links for in-vault targets")
        legacy = earlier_layout_paths(root, archetype)
        if legacy:
            notes.append(
                "earlier-layout paths exist under .bc-agent (" + ", ".join(legacy) + "); "
                "they were left in place and nothing was moved — migrating them to the visible "
                "layout is a separate, explicit step (see MIGRATIONS.md)")
        agents_path = vault / "AGENTS.md"
        try:
            has_table = agents_path.exists() and bool(parse_where_things_go(agents_path.read_text(errors="ignore")))
        except ValueError:
            has_table = False
        if agents_path.exists() and not has_table:
            notes.append("`.bc-agent/AGENTS.md` has no \"Where things go\" table; skills cannot look paths up until it is added")
        if archetype == "hybrid":
            notes.extend(_teach_notes(root))
        return notes

    # This contract applies to every archetype. Keep it outside the code/hybrid
    # gate below so learning and knowledge vaults receive the same migration hint.
    read_path_checks = [
        (root / "AGENTS.md", "1. `.bc-agent/AGENTS.md`",
         "root AGENTS.md should make `.bc-agent/AGENTS.md` the first read and defer vault retrieval to its canonical search-first path"),
        (vault / "AGENTS.md", "<!-- BEGIN canonical vault read path -->",
         "`.bc-agent/AGENTS.md` should include the canonical search-first vault read path block from `bc-wiki-maintain`"),
        (vault / "map.md", "- [project/overview.md](project/overview.md)",
         "`.bc-agent/map.md` should use real Markdown links for in-vault targets so `bc-wiki-maintain` can validate its graph edges"),
    ]
    for path, needle, message in read_path_checks:
        if path.exists() and not _contains(path, needle):
            notes.append(message)

    if archetype in {"learning", "hybrid"}:
        notes.extend(_teach_notes(root))

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


def _preflight_targets(root: Path, planned: list[tuple[Path, str, bool]]) -> bool:
    """Reject path-type collisions before the additive scaffold writes anything."""
    for destination, _content, _is_root in planned:
        try:
            relative = destination.relative_to(root)
        except ValueError:
            print(f"ERROR: scaffold target is outside root: {destination}")
            return False

        parent = root
        for component in relative.parts[:-1]:
            parent /= component
            if parent.exists() and not parent.is_dir():
                print(f"ERROR: cannot create {destination}: parent is not a directory: {parent}")
                return False
        if destination.exists() and not destination.is_file():
            print(f"ERROR: scaffold target is not a regular file: {destination}")
            return False
    return True

# --- migrate mode: earlier `.bc-agent/` vault layout -> visible layout ----------------

RULE_WORK = ("only work still open becomes numbered work items in `work/` (main checkout, next free "
             "number); finished lists are kept unchanged as one dated record under the research role")
RULE_IDEAS = "meaningful lines move to the ideas file `work/0-ideas.md`"
RULE_DRAFTS = "drafts go inside their parent work item's folder as evidence"
RULE_OVERVIEW = "glossary terms move to `glossary.md`; the rest is split by role"
RULE_PRD = ("project-level -> `docs/PRD.md`; feature-level -> the work item's `requirements.md`")
RULE_FINDINGS = "-> research role (`docs/research/`) as dated folders; take the date from git history"
RULE_QUESTIONS = ("blocking -> a step in its work item; standalone -> a planned item with the answer in "
                  "research; minor -> a line in the ideas file")
RULE_DELETE_CHECKED = "delete after checking for unique content"
RULE_UNRECOGNISED = "unrecognised; decide by hand"
RULE_GENERATED_EDITED = ("differs from the generated version; carry unique local guidance into "
                         "conventions or the work-item template, then delete")
RULE_CLASH = "another file would land at {dest}; rename one by hand, then move both"
RULE_ALREADY_THERE = "an identical copy already exists at {dest}; delete this one after checking links"
RULE_OLD_AGENTS = ("replaced by the generated version; diff the old one (`git show HEAD:.bc-agent/AGENTS.md`, "
                   "recoverable from git history) and carry project-specific rules into the new file")

# Earlier-layout vault folders whose files move unchanged; components only where the archetype has them.
_MIGRATE_MOVERS = {"decisions": "docs/decisions", "research": "docs/research"}
_MIGRATE_OPS_MOVERS = {"components": "docs/components"}
_MIGRATE_GENERATED = {"conventions/planning-workflow.md": PLANNING_WORKFLOW, "templates/plan.md": TPL_PLAN}


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)


def _matches_generated(text: str, template: str, slug: str) -> bool:
    """True when text equals the template rendered for this slug with any ISO date."""
    pattern = re.escape(template.replace(SLUG, slug)).replace(re.escape(DATE), r"\d{4}-\d{2}-\d{2}")
    return re.fullmatch(pattern, text) is not None


def _measure(root: Path, path: str, files: list[str]) -> str:
    if len(files) == 1 and files[0] == path:
        try:
            return f"{len((root / path).read_text(errors='ignore').splitlines())} lines"
        except OSError:
            return "unreadable"
    return f"{len(files)} files"


class MigrationPlan:
    def __init__(self) -> None:
        self.moves: list[tuple[str, str]] = []
        self.creates: list[tuple[str, str]] = []
        self.replaces: list[tuple[str, str]] = []
        self.deletes: list[str] = []
        self.kept: list[str] = []
        self.judgment: list[tuple[str, str, str]] = []
        self.refusals: list[str] = []
        self.link_edits: dict[str, str] = {}  # new path -> rewritten text
        self.link_count = 0
        self.link_files: set[str] = set()  # new paths of files with a rewritten Markdown link
        self.unresolved: list[str] = []
        self.wikilink_count = 0
        self.wikilink_files: set[str] = set()  # new paths of files with a rewritten wikilink
        self.ambiguous_wikilinks: list[str] = []  # file:line of bare names matching several files
        self.stay_wikilinks: list[str] = []  # file:line in a moved file naming a file that stays
        self.other_refs: list[str] = []


_INLINE_LINK = re.compile(r"(\]\()(<[^>\n]*>|[^)\s]+)")
_REF_DEFINITION = re.compile(r"^( {0,3}\[[^\]\n]+\]:[ \t]+)(<[^>\n]*>|\S+)")
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_INLINE_CODE = re.compile(r"(`+)[^`\n]*?\1")
_WIKILINK = re.compile(r"(!?)\[\[([^\[\]\n]+)\]\]")
_URL_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def _map_moved(path: str, file_moves: dict[str, str], dir_moves: dict[str, str]) -> str:
    if path in file_moves:
        return file_moves[path]
    for old_dir, new_dir in dir_moves.items():
        if path == old_dir or path.startswith(old_dir + "/"):
            return new_dir + path[len(old_dir):]
    return path


def _rewrite_target(root: Path, target: str, old_file: str, new_file: str,
                    file_moves: dict[str, str], dir_moves: dict[str, str]) -> str | None:
    """New link text for target, the same text when unchanged, or None when it does not resolve."""
    bracketed = target.startswith("<") and target.endswith(">")
    raw = target[1:-1] if bracketed else target
    if not raw or raw.startswith(("#", "/")) or _URL_SCHEME.match(raw):
        return target
    cut = min((i for i in (raw.find("#"), raw.find("?")) if i >= 0), default=len(raw))
    path_part, suffix = raw[:cut], raw[cut:]
    if not path_part:
        return target
    resolved = os.path.normpath(os.path.join(os.path.dirname(old_file), urllib.parse.unquote(path_part)))
    if resolved.startswith("..") or not (root / resolved).exists():
        return None
    new_target = _map_moved(resolved.replace(os.sep, "/"), file_moves, dir_moves)
    if new_target == resolved and new_file == old_file:
        return target
    new_rel = os.path.relpath(new_target, os.path.dirname(new_file) or ".").replace(os.sep, "/")
    if path_part.endswith("/") and not new_rel.endswith("/"):
        new_rel += "/"
    if os.path.normpath(new_rel) == os.path.normpath(urllib.parse.unquote(path_part)):
        return target
    if "%" in path_part:
        new_rel = urllib.parse.quote(new_rel, safe="/")
    new_raw = new_rel + suffix
    return f"<{new_raw}>" if bracketed else new_raw


def _heading_anchor(heading: str) -> str:
    """GitHub-style anchor: lower-case, punctuation other than - and _ dropped, spaces to hyphens."""
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


def _wikilink_matches(target: str, by_name: dict[str, list[str]]) -> list[str]:
    """Tracked files an Obsidian wikilink target names: by basename, or by path suffix for a path form."""
    target = target.strip().lower()
    name = target.rsplit("/", 1)[-1]
    found = by_name.get(name, []) + by_name.get(name + ".md", [])
    if "/" in target:
        found = [p for p in found if ("/" + p.lower()).endswith("/" + target)
                 or ("/" + p.lower()).endswith("/" + target + ".md")]
    return sorted(set(found))


def _rewrite_wikilinks(line: str, location: str, new_file: str, moved_file: bool, by_name: dict[str, list[str]],
                       file_moves: dict[str, str], plan: MigrationPlan) -> tuple[str, int]:
    """Replace wikilinks naming a moved file with relative Markdown links; report the ones left."""
    code = [m.span() for m in _INLINE_CODE.finditer(line)]
    count = 0
    for match in reversed(list(_WIKILINK.finditer(line))):
        if any(a <= match.start() < b for a, b in code):
            continue
        embed, inner = match.group(1), match.group(2)
        target, _bar, label = inner.partition("|")
        target, _hash, heading = target.rstrip("\\").partition("#")
        if not target.strip():
            continue
        found = _wikilink_matches(target, by_name)
        if not any(p in file_moves for p in found):
            if moved_file and found:
                plan.stay_wikilinks.append(location)
            continue
        if len(found) > 1:
            plan.ambiguous_wikilinks.append(location)
            continue
        old = found[0]
        rel = os.path.relpath(file_moves[old], os.path.dirname(new_file) or ".").replace(os.sep, "/")
        if any(c in rel for c in " ()<>"):
            rel = f"<{rel}>"
        is_markdown = old.lower().endswith(".md")
        if heading and is_markdown:
            rel = rel[:-1] + f"#{_heading_anchor(heading)}>" if rel.startswith("<") \
                else rel + f"#{_heading_anchor(heading)}"
        if embed and not is_markdown:
            new = f"![{label.strip()}]({rel})"
        else:
            new = f"[{label.strip() or target.strip()}]({rel})"
        line = line[:match.start()] + new + line[match.end():]
        count += 1
    return line, count


def _plan_links(root: Path, tracked: list[str], plan: MigrationPlan, dir_moves: dict[str, str]) -> None:
    file_moves = dict(plan.moves)
    # Obsidian resolves a wikilink by bare file name anywhere, or by path suffix.
    by_name: dict[str, list[str]] = {}
    for path in tracked:
        by_name.setdefault(path.rsplit("/", 1)[-1].lower(), []).append(path)
    for old_file in (p for p in tracked if p.endswith(".md")):
        new_file = file_moves.get(old_file, old_file)
        try:
            text = (root / old_file).read_text()
        except (OSError, UnicodeDecodeError):
            continue
        lines = text.split("\n")
        changed = False
        fence: str | None = None
        for number, line in enumerate(lines, 1):
            opener = _FENCE.match(line)
            if fence:
                if opener and opener.group(1)[0] == fence[0] and len(opener.group(1)) >= len(fence):
                    fence = None
                continue
            if opener:
                fence = opener.group(1)
                continue
            code = [m.span() for m in _INLINE_CODE.finditer(line)]
            spans = [(m.start(2), m.end(2)) for m in _INLINE_LINK.finditer(line)]
            ref = _REF_DEFINITION.match(line)
            if ref:
                spans.append((ref.start(2), ref.end(2)))
            for start, end in sorted(spans, reverse=True):
                if any(a <= start < b for a, b in code):
                    continue
                target = line[start:end]
                new = _rewrite_target(root, target, old_file, new_file, file_moves, dir_moves)
                if new is None:
                    plan.unresolved.append(f"{old_file}:{number}")
                elif new != target:
                    line = line[:start] + new + line[end:]
                    plan.link_count += 1
                    plan.link_files.add(new_file)
                    changed = True
            # After the Markdown links, so a link this produces is not rewritten a second time.
            line, wiki = _rewrite_wikilinks(line, f"{old_file}:{number}", new_file, old_file in file_moves,
                                            by_name, file_moves, plan)
            if wiki:
                plan.wikilink_count += wiki
                plan.wikilink_files.add(new_file)
                changed = True
            lines[number - 1] = line
        if changed:
            plan.link_edits[new_file] = "\n".join(lines)


def _plan_other_references(root: Path, plan: MigrationPlan, sources: list[str]) -> None:
    needles = sorted({old for old, _new in plan.moves} | {s + "/" for s in sources})
    if not needles:
        return
    args = ["grep", "-n", "-I", "-F"]
    for needle in needles:
        args += ["-e", needle]
    found = _git(root, *args, "--", ".", ":(exclude)*.md")
    for line in found.stdout.splitlines():
        location, _, text = line.partition(":")
        number, _, text = text.partition(":")
        plan.other_refs.append(f"{location}:{number}: {text.strip()[:100]}")


def plan_migration(root: Path, slug: str, date: str, archetype: str) -> MigrationPlan:
    """Plan the move of an earlier-layout vault to the visible layout. Writes nothing."""
    plan = MigrationPlan()
    tracked = _git(root, "ls-files", "-z").stdout.split("\0")
    tracked = [p for p in tracked if p]
    vault_prefix = ".bc-agent/"
    movers = dict(_MIGRATE_MOVERS)
    if archetype in {"ops", "hybrid"}:
        movers.update(_MIGRATE_OPS_MOVERS)
    generated = visible_targets(root, slug, date, archetype)
    keep_tops = {dest.relative_to(root / ".bc-agent").parts[0]
                 for dest, _c, _r in generated if (root / ".bc-agent") in dest.parents}

    candidates: list[tuple[str, str]] = []  # (old, new)
    source_dirs = {vault_prefix + name: dest for name, dest in movers.items()}
    groups: dict[str, tuple[list[str], str]] = {}

    def judge(path: str, file: str, rule: str) -> None:
        groups.setdefault(path, ([], rule))[0].append(file)

    if any(p.startswith("docs/adr/") for p in tracked):
        source_dirs["docs/adr"] = "docs/decisions"
    for path in tracked:
        if path.startswith(vault_prefix):
            rel = path[len(vault_prefix):]
            top = rel.split("/", 1)[0]
            if top in movers and "/" in rel:
                if rel.endswith("/.gitkeep") or rel == top + "/.gitkeep":
                    plan.deletes.append(path)
                else:
                    candidates.append((path, movers[top] + rel[len(top):]))
            elif top in {"scratch", "out-of-scope"}:
                judge(vault_prefix + top, path, RULE_UNRECOGNISED)
            elif rel in _MIGRATE_GENERATED:
                text = (root / path).read_text(errors="ignore")
                if _matches_generated(text, _MIGRATE_GENERATED[rel], slug):
                    plan.deletes.append(path)
                else:
                    judge(path, path, RULE_GENERATED_EDITED)
            elif top in keep_tops:
                continue
            elif top == "tasks":
                name = rel.split("/")
                if len(name) == 2 and name[1] in {"active.md", "completed.md"}:
                    judge(path, path, RULE_WORK)
                elif len(name) == 2 and name[1] == "parking-lot.md":
                    judge(path, path, RULE_IDEAS)
                elif len(name) > 2 and "draft" in name[1]:
                    judge(vault_prefix + "tasks/" + name[1], path, RULE_DRAFTS)
                else:
                    judge(path, path, RULE_UNRECOGNISED)
            elif top == "plans":
                judge(vault_prefix + "plans", path, RULE_WORK)
            elif top == "project":
                base = rel.split("/")[-1].lower()
                if rel == "project/overview.md":
                    judge(path, path, RULE_OVERVIEW)
                elif "prd" in base:
                    judge(path, path, RULE_PRD)
                elif "-plan" in base or "-tasks" in base:
                    judge(path, path, RULE_WORK)
                else:
                    judge(path, path, RULE_UNRECOGNISED)
            elif top == "findings":
                judge(vault_prefix + top, path, RULE_FINDINGS)
            elif top == "open-questions":
                judge(vault_prefix + top, path, RULE_QUESTIONS)
            elif top in {"home.md", "index.md", ".obsidian"}:
                judge(vault_prefix + top, path, RULE_DELETE_CHECKED)
            else:
                judge(vault_prefix + top, path, RULE_UNRECOGNISED)
        elif path.startswith("docs/adr/"):
            if path.endswith("/.gitkeep"):
                plan.deletes.append(path)
            else:
                candidates.append((path, "docs/decisions/" + path[len("docs/adr/"):]))
        elif path.startswith("docs/plans/"):
            judge("docs/plans", path, RULE_WORK)

    # scratch/ and out-of-scope/ holding only placeholders are deleted, not judged.
    for top in ("scratch", "out-of-scope"):
        key = vault_prefix + top
        if key in groups and all(f.endswith("/.gitkeep") for f in groups[key][0]):
            plan.deletes.extend(groups.pop(key)[0])

    by_dest: dict[str, list[str]] = {}
    for old, new in candidates:
        by_dest.setdefault(new, []).append(old)
    for old, new in candidates:
        if len(by_dest[new]) > 1:
            judge(old, old, RULE_CLASH.format(dest=new))
        elif (root / new).exists():
            if (root / new).is_file() and (root / new).read_bytes() == (root / old).read_bytes():
                judge(old, old, RULE_ALREADY_THERE.format(dest=new))
            else:
                plan.refusals.append(f"destination already exists as a different file: {new} (for {old})")
        else:
            plan.moves.append((old, new))

    move_dests = {new for _old, new in plan.moves}
    move_dirs = {os.path.dirname(new) for new in move_dests}
    for dest, content, _is_root in generated:
        rel = dest.relative_to(root).as_posix()
        if rel in move_dests or (rel.endswith("/.gitkeep") and any(
                d == os.path.dirname(rel) or d.startswith(os.path.dirname(rel) + "/") for d in move_dirs)):
            continue
        if not dest.exists():
            plan.creates.append((rel, content))
        elif rel == ".bc-agent/AGENTS.md":
            if dest.read_text(errors="ignore") != content:
                plan.replaces.append((rel, content))
                judge(rel, rel, RULE_OLD_AGENTS)
        elif not rel.endswith("/.gitkeep") and dest.read_text(errors="ignore") != content:
            plan.kept.append(rel)

    for path, (files, rule) in sorted(groups.items()):
        plan.judgment.append((path, _measure(root, path, files), rule))

    # A folder link is rewritten only when everything in the folder moves.
    unmoved = {old for old, _new in candidates} - {old for old, _new in plan.moves}
    dir_moves = {src: dst for src, dst in source_dirs.items()
                 if not any(path.startswith(src + "/") for path in unmoved)}
    _plan_links(root, tracked, plan, dir_moves)
    _plan_other_references(root, plan, [src for src in source_dirs
                                        if any(old.startswith(src + "/") for old, _new in plan.moves)])
    return plan


def _has_layout_table(text: str) -> bool:
    """True for a parseable role table; earlier vaults used the same heading for a bullet list."""
    try:
        parse_where_things_go(text)
    except ValueError:
        return False
    return True


def _migrate_refusal(root: Path, archetype: str) -> str | None:
    if archetype not in VISIBLE_ARCHETYPES:
        return (f"migrate mode is for code, ops and hybrid; the {archetype} archetype keeps the "
                f".bc-agent/ vault")
    top = _git(root, "rev-parse", "--show-toplevel")
    if top.returncode != 0:
        return f"{root} is not a git repository"
    if Path(top.stdout.strip()).resolve() != root:
        return f"{root} is not the repository root ({top.stdout.strip()})"
    if not (root / ".bc-agent").is_dir():
        return "no .bc-agent/ vault to migrate; run the scaffold without --migrate for a fresh layout"
    dirty = _git(root, "status", "--porcelain", "--untracked-files=all").stdout.splitlines()
    if dirty:
        return "the working tree has uncommitted changes:\n" + "\n".join(f"  {line}" for line in dirty)
    agents = root / ".bc-agent" / "AGENTS.md"
    if agents.is_file() and _has_layout_table(agents.read_text(errors="ignore")):
        return f"{agents} already has a {WHERE_THINGS_GO_HEADING!r} table; the project is already migrated"
    return None


def _print_section(title: str, items: list[str]) -> None:
    print(title)
    for item in items or ["(none)"]:
        print(f"  {item}")


def run_migrate(root: Path, slug: str, date: str, archetype: str, apply: bool) -> int:
    refusal = _migrate_refusal(root, archetype)
    if refusal:
        print(f"ERROR: {refusal}")
        print("Nothing was written.")
        return 1
    plan = plan_migration(root, slug, date, archetype)
    if plan.refusals:
        for message in plan.refusals:
            print(f"ERROR: {message}")
        print("Nothing was written.")
        return 1
    planned = [(root / rel, content, False) for rel, content in plan.creates + plan.replaces]
    if not _preflight_targets(root, planned):
        print("Nothing was written.")
        return 1

    print(f"Repo: {root}")
    print(f"Branch: {_git(root, 'branch', '--show-current').stdout.strip() or '(detached)'}")
    print(f"Archetype: {archetype} (from --archetype)")
    print()
    _print_section("MOVE", [f"{old} -> {new}" for old, new in plan.moves])
    _print_section("CREATE", [rel for rel, _c in plan.creates])
    _print_section("REPLACE", [rel for rel, _c in plan.replaces])
    _print_section("DELETE", plan.deletes)
    _print_section("KEPT (review by hand)", plan.kept)
    _print_section("NEEDS JUDGMENT", [f"{path} — {size} — {rule}" for path, size, rule in plan.judgment])
    verb = "rewrote" if apply else "would rewrite"
    _print_section("LINKS", [f"{verb} {plan.link_count} links in {len(plan.link_files)} files; "
                             f"unresolved: {len(plan.unresolved)} (left as is)"]
                   + [f"  {loc}" for loc in plan.unresolved[:10]]
                   + [f"{verb} {plan.wikilink_count} wikilinks in {len(plan.wikilink_files)} files",
                      f"ambiguous wikilinks (left as is): {len(plan.ambiguous_wikilinks)}"]
                   + [f"  {loc}" for loc in plan.ambiguous_wikilinks[:10]]
                   + ["wikilinks from moved files to files that stay (left as is; they resolve only inside "
                      f"an Obsidian vault): {len(plan.stay_wikilinks)}"])
    shown = plan.other_refs[:50]
    if len(plan.other_refs) > 50:
        shown.append(f"... {len(plan.other_refs) - 50} more")
    _print_section("OTHER REFERENCES", shown)
    print()
    print(f"Totals: {len(plan.moves)} move, {len(plan.creates)} create, {len(plan.replaces)} replace, "
          f"{len(plan.deletes)} delete, {len(plan.kept)} kept, {len(plan.judgment)} need judgment, "
          f"{plan.link_count} link rewrites, {plan.wikilink_count} wikilink rewrites")
    if not apply:
        command = (f"python3 {Path(__file__).resolve()} --root {root} --slug {slug} --date {date} "
                   f"--archetype {archetype} --migrate --apply")
        print(f"Dry run; nothing was written. Apply with: {command}")
        return 0

    for old, new in plan.moves:
        (root / new).parent.mkdir(parents=True, exist_ok=True)
        moved = _git(root, "mv", old, new)
        if moved.returncode != 0:
            print(f"ERROR: git mv {old} {new} failed: {moved.stderr.strip()}")
            print("Stopped part-way; inspect `git status` and undo with `git reset --hard` if needed.")
            return 1
    if plan.deletes:
        _git(root, "rm", "-q", "--", *plan.deletes)
    for old in sorted({os.path.dirname(p) for p, _n in plan.moves} | {os.path.dirname(p) for p in plan.deletes},
                      key=len, reverse=True):
        try:  # git mv leaves emptied source folders behind; remove them, never a non-empty one
            os.removedirs(root / old)
        except OSError:
            pass
    for rel, text in plan.link_edits.items():
        (root / rel).write_text(text)
    for rel, content in plan.creates + plan.replaces:
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(content)
    _git(root, "add", "-A")
    print(f"Applied: moved {len(plan.moves)}, created {len(plan.creates)}, replaced {len(plan.replaces)}, "
          f"deleted {len(plan.deletes)}, rewrote {plan.link_count} links in {len(plan.link_files)} files, "
          f"{plan.wikilink_count} wikilinks in {len(plan.wikilink_files)} files.")
    print("Everything is staged and nothing was committed: work through NEEDS JUDGMENT, then commit "
          "the project in one commit.")
    return 0



def main() -> int:
    ap = argparse.ArgumentParser(
        description="Idempotent: creates only missing files; never deletes, and never "
                    "overwrites existing files unless explicitly forced.")
    ap.add_argument("--root", required=True, help="project (repo) root")
    ap.add_argument("--slug", required=True, help="project display name, kebab-case")
    ap.add_argument("--date", default=_dt.date.today().isoformat())
    ap.add_argument("--archetype", choices=["code", "ops", "learning", "knowledge", "hybrid"], default=None,
                    help="optional wiki archetype layered on top of the base project scaffold "
                         "(default code; required with --migrate)")
    ap.add_argument("--force", action="store_true",
                    help="overwrite existing files under .bc-agent/ (never files outside it, never "
                         "deletes; root AGENTS.md needs --force-root)")
    ap.add_argument("--force-root", action="store_true",
                    help="also overwrite an existing root AGENTS.md")
    ap.add_argument("--allow-earlier-layout", action="store_true",
                    help="code/ops/hybrid: create missing visible-layout files even when earlier-layout "
                         "paths exist under .bc-agent/ (they stay untouched)")
    ap.add_argument("--dry-run", action="store_true", help="report what would happen; write nothing")
    ap.add_argument("--migrate", action="store_true",
                    help="code/ops/hybrid: plan moving an earlier-layout .bc-agent/ vault to the visible "
                         "layout; prints the plan and writes nothing unless --apply is given")
    ap.add_argument("--apply", action="store_true",
                    help="with --migrate: perform the plan and stage it (never commits)")
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    slug = args.slug.strip()
    if not root.is_dir():
        print(f"ERROR: root is not a directory: {root}")
        return 1
    if not slug or slug != slug.lower() or " " in slug:
        print(f"ERROR: slug must be lower-case kebab with no spaces: {slug!r}")
        return 1
    if args.migrate:
        if args.archetype is None:
            print("ERROR: --migrate needs an explicit --archetype (code, ops or hybrid); "
                  "nothing in the earlier vault records it reliably.")
            return 1
        return run_migrate(root, slug, args.date, args.archetype, args.apply)
    if args.apply:
        print("ERROR: --apply only applies to --migrate.")
        return 1
    if args.archetype is None:
        args.archetype = "code"

    if args.archetype in VISIBLE_ARCHETYPES and not args.allow_earlier_layout:
        legacy = earlier_layout_paths(root, args.archetype)
        if legacy:
            print("ERROR: earlier-layout paths exist under .bc-agent (" + ", ".join(legacy) + "); "
                  "nothing was written.")
            print("Migrating them to the visible layout is a separate, explicit step (see MIGRATIONS.md). "
                  "Re-run with --allow-earlier-layout to create the missing visible-layout files beside "
                  "them, leaving every existing file untouched.")
            return 1

    vault = root / ".bc-agent"
    created: list[Path] = []
    overwritten: list[Path] = []
    skipped: list[Path] = []  # existed, left untouched
    planned = targets(root, slug, args.date, args.archetype)
    if not _preflight_targets(root, planned):
        return 1

    for dest, content, is_root in planned:
        exists = dest.exists()
        may_overwrite = args.force_root if is_root else (args.force and vault in dest.parents)
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
            if args.archetype in VISIBLE_ARCHETYPES:
                print(f"\nNOTE: existing {root_agents} was left as-is. Merge the 'read .bc-agent first' "
                      f"pointer into it by hand (see `.bc-agent/AGENTS.md` and its \"Where things go\" table).")
            else:
                print(f"\nNOTE: existing {root_agents} was left as-is. Merge the 'read .bc-agent first' "
                      f"pointer into it by hand (see `.bc-agent/AGENTS.md` and its canonical search-first block).")

    print("\nNext: fill conventions/validation.md + file-layout.md as you learn the project; "
          "read .bc-agent/references/agent-skills.md for the loop skill map; "
          "authorize this repo in policies/publish.yaml if you'll run /bc-drain-issues AFK; "
          "then /triage existing issues or /bc-plan-to-issues to plan the first feature.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
