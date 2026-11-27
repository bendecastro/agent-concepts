---
name: bc-setup-project
description: Scaffold a project's agent workspace (visible work/ and docs/ folders plus .bc-agent/ mechanics, or a .bc-agent vault for learning/knowledge) and a repo-root AGENTS.md so a repo is ready for the plan→issues→drain workflow. Run once per project before /bc-plan-to-pipeline.
disable-model-invocation: true
argument-hint: "[project-slug] (defaults to the repo directory name)"
---

# Init Agent Workspace

Adaptively initialize project-local agent context.

If `~/.config/agent-concepts/overlays/bc-setup-project.md` exists, read it for this machine's tool names.

- **Code, ops and hybrid use the visible layout.** Work items live in `work/` (`0-ideas.md`, then
  `1-planned/`, `2-active/`, `3-done/<year>-<month>/`, `4-dropped/`), decisions and research in
  `docs/decisions/` and `docs/research/`, the vocabulary in root `glossary.md`; `.bc-agent/` holds
  agent mechanics only (instructions, map, log, conventions, references, templates, scripts). Why: people
  browse the repository, not a hidden folder, so knowledge kept out of sight goes stale.
  Project-specific skills and agents go to `.agents/skills/local-<name>/` and
  `.agents/agents/local-<name>.md`, created on first need.
- **The "Where things go" table in `.bc-agent/AGENTS.md` is the single home for these paths.**
  When you or another skill need a location, look the role up there instead of assuming it. Why:
  a project with a justified exception then changes one table, not every skill.
- **Learning and knowledge keep the `.bc-agent/` vault.** Why: `bc-teach` reads exact vault paths;
  changing them is a separate plan.
- **Hybrid also keeps the paths the hosted `bc-teach` adapter maps under `.bc-agent/`**, except the
  glossary: its adapter maps `bc-teach`'s glossary to the project's root `glossary.md`, so a hybrid
  project has one glossary, shared by the project and the learner.

## Operating modes and wiki archetypes

Default to **recon → targeted grill → proposed init plan → scaffold**. Do not blindly scaffold a non-empty folder.

Modes:
- **Recon-only**: when the user wants to inspect/understand the folder first, stop after the environment summary and recommended questions.
- **Plan init**: for empty, ambiguous, or existing projects, inspect first, grill enough to adapt the workspace, and present a concrete init/migration plan before writing.
- **Apply scaffold**: run the deterministic scaffold after the user accepts the plan or when the folder is clearly fresh and the user explicitly asked to initialize now.
- **Migration assist**: for old/messy projects, propose how existing docs/files could seed the roles in the "Where things go" table (learning/knowledge: `.bc-agent/`); move/copy files only after explicit approval.

Archetypes:
- **code** — default project execution workspace: work items (a plan or feature is one item), decision records, research including architecture reviews, validation, commands, architecture-runway nudge tracking, `/bc-plan-to-pipeline` → `/bc-pipeline-to-done`.
- **ops** — operational/system workspace: the code layout plus `docs/components/` (verified state of real systems); findings go to `docs/research/`, plans are work items, and open questions are work-item steps, planned items or ideas lines (the rule is in the generated `.bc-agent/AGENTS.md`); evidence before plan.

### Learning archetype adapter

- **learning** — bc agents helping the human learn. The generated
  `.bc-agent/references/teach-skill.md` is an explicit thin adapter for the existing
  standalone `bc-teach` skill: mission → `learning/plan.md`, review queue →
  `learning/review.md`, records → `learning/records/`, notes → `learning/notes.md`,
  raw sources → `sources/`, compiled knowledge → `concepts/`, resources →
  `references/teach-resources.md`, glossary → the existing Glossary section of
  `project/overview.md`, and catalog/history → shared `index.md` / `log.md`.
  Lessons and session artifacts reuse existing `sessions/`; no `learning/sessions/`
  directory is created. When the marker is valid, teach owns the Glossary section of
  `project/overview.md`; planning and maintenance skills leave it alone. (Hybrid's adapter maps
  the glossary to the root `glossary.md` instead; see **hybrid**.) The adapter points
  at teach; it does not copy pedagogy, auto-run initialization, or migrate standalone files.
  A host choice alone never migrates state; teach's separate explicit migration operation is
  destructive and verifies every destination before deleting standalone originals. `questions/`
  is for open questions only, not a second review queue or evidence store.
- **knowledge** — LLM-maintained knowledge graph: immutable `raw/`, compiled `wiki/sources`, `wiki/entities`, `wiki/concepts`, `wiki/syntheses`, and a wiki log.
- **hybrid** — the ops layout plus a hosted `bc-teach` workspace, for a folder that both ships or operates something and supports learning. The scaffold adds exactly the paths the teach adapter maps under `.bc-agent/` (`learning/`, `sources/`, `concepts/`, `questions/`, `sessions/`, and the teach catalog `index.md`); do not add a parallel learning state tree. Its adapter maps `bc-teach`'s glossary to the project's root `glossary.md`, shared: `bc-teach` adds the terms the learner needs and does not remove or redefine project terms without asking. Project work still goes where the table says, not into the teach paths.

## Process

1. **Locate the project.** Find the repo root (`git rev-parse --show-toplevel`). If choosing a new root, read the user's preferences file when one exists and names a default project location, and suggest that location; otherwise ask. Why: the user decides where projects live, and their preferences file is that decision's one home. If the chosen root is inside a folder replicated by a file-sync tool, warn before scaffolding: the tool replicates `.git` file by file, so two machines can corrupt the repository or leave conflict copies inside it. If not a git repo, ask whether to initialize here, use the folder, or choose another root. Pick the slug from the argument or directory name; confirm ambiguity.

2. **Recon before grilling.** Inspect the environment before asking questions. Keep it bounded; do not crawl huge dependency/build output directories. Check at least:
   - Git state: repo root, branch, dirty status, remotes, existing `AGENTS.md`, existing `.bc-agent/`, `glossary.md`, docs/plans/ADRs. For legacy glossary discovery, follow `bc-domain-modeling`’s legacy glossary rule.
   - GitHub readiness, only when a remote points at GitHub: whether `gh` exists/auths and whether `gh repo view` works. Without a GitHub remote, skip this check and say nothing about `gh` in the survey. Why: a note about an unauthenticated `gh` in a project with no GitHub is noise to a newcomer.
   - Project shape: empty/near-empty vs active vs old/messy; package/build/deploy markers (`package.json`, lockfiles, `pyproject.toml`, `Cargo.toml`, `go.mod`, Docker/Compose, CI, infra, scripts, Makefile/justfile, README).
   - For an existing project with no CI, find the local validation commands the project already uses: check the README, package scripts, Makefile/justfile, then tool configuration and standard commands it supports (e.g. `pyproject.toml` or `Cargo.toml`). Note the declared toolchain, full-suite vs targeted commands, actual source/test/build paths, any known failures, and whether release checks exist. Do not infer a check just from a language marker.
   - If you find no source code, ask in the grill whether the planned project has a user-facing UI or CLI. If you find existing source code, check for a user-facing UI or CLI and, with a GitHub remote, open GitHub issues (`gh issue list` when available). Use the signals in [starter-items.md](starter-items.md); a failed issue lookup is not evidence of open issues.
   - Existing knowledge to seed: README, docs, issue templates, architecture notes, validation commands, deployment notes, old plans/specs.
   - **Kernel in the current harness (read-only).** Check the harness's active package/plugin settings and the always-on instruction files it actually loads (respect overridden config paths and session flags). An enabled kernel package, a matched `<!-- agent-kernel:begin vN -->` / `<!-- agent-kernel:end vN -->` block, or a `# Agent Kernel` heading in loaded instructions counts. On Codex the SessionStart hook must also be trusted; a disabled plugin, a checkout on disk, or a kernel in another harness does not count. If you cannot inspect the active sources, say what you could not verify rather than guessing. If present, say nothing about it.
   - **If missing, report it in the survey and give only the matching install instructions below.** Setup is per project; the kernel belongs to the harness. Do not run an install command, change settings or instructions, or write any project files in response to this finding. Wait for the owner's answer; installation is optional and does not replace normal approval for scaffolding.
     - Pi: the kernel comes with the Agent Concepts Pi package; install that package (`pi install <agent-concepts checkout or package source>`), or turn its kernel extension back on in `pi config` if it was disabled.
     - Claude Code: `claude plugin marketplace add /path/to/agent-concepts`, then `claude plugin install agent-kernel@agent-concepts --scope user`.
     - Codex: `codex plugin marketplace add /path/to/agent-concepts`, then `codex plugin add agent-kernel@agent-concepts`. Review and trust its SessionStart hook with `/hooks`.
     - OpenCode V2: no install CLI; add the absolute path to `packages/agent-kernel-opencode/` to `plugins` in the global `opencode.json(c)` and restart the server. On V1, add the absolute path to the packaged `AGENT-KERNEL.md` to `instructions` instead.
     - Other harnesses (manual fallback): `python3 /path/to/agent-concepts/packages/agent-kernel/install.py /path/to/instructions.md`, using the file that harness actually loads.
     - Substitute the real checkout/instructions paths and tell the owner to start a fresh session. On explicit decline, record one line (no duplicate) in the project's `ideas` file from its “Where things go” table, or its existing parking lot if it has no table. If the file does not exist yet, defer the line until separately approved setup creates it. Silence is not a decline.

3. **Summarize state, choose an archetype, then grill adaptively.** Start by telling the user what you found, what mode you recommend, and which archetype seems to fit. Ask targeted questions one at a time unless the user asks for a full questionnaire. The first fork is purpose: is this workspace mainly for shipping code, operating a system, learning/research, personal knowledge capture, or a hybrid?

   For an **empty or near-empty folder**, establish intent before scaffolding: app/library/config/tooling/content/research; code vs ops vs learning vs knowledge; expected dev/build/deploy shape; GitHub issues vs local planning first; whether to create only agent docs or also propose project source layout; initial feature/mission if known.

   For an **existing active project**, integrate without disruption: which docs are authoritative; whether existing docs should be referenced, copied, or left in place; whether an existing root `AGENTS.md` remains primary; validation/build/test commands agents may trust; deploy/publish actions allowed, forbidden, or manual-only.

   For an **operational/system workspace**, identify components, findings/evidence, decisions, open questions, and planned work. Ask what real-world actions agents may do vs only document for the human.

   For a **learning workspace**, ask the subject, desired outcome, current level, preferred learning cadence, source material, and whether to invoke the `bc-teach` skill for multi-session tutoring records.

   For a **knowledge-graph workspace**, ask the domain boundary, source-ingest policy, raw immutability expectations, entity/concept granularity, and whether this is personal cross-project knowledge or project-local knowledge.

   For an **old/messy project being revived**, treat init as a reconciliation step: cleanup/continuation/archive/rewrite goal; authoritative old plans/specs/ADRs; which files could seed which role in the "Where things go" table (for learning or knowledge vaults: `project/`, `research/`, `decisions/`, `learning/`, `sources/`, `concepts/`, `raw/`); rejected old work belongs in the dropped-work folder with its reason; whether file moves are allowed now or should become a migration plan; what must not be touched.

4. **Propose the init plan before writing.** Name the root, slug, mode, selected archetype, files that will be created, existing files that will be preserved, any manual merge needed for `AGENTS.md`, any existing files proposed for later migration, and open decisions. If the plan includes moving/copying existing docs, separate that from the scaffold and require explicit approval.
   For first-time code, ops or hybrid setup, list exactly the applicable starter items as checked boxes, each with the survey finding that makes it apply. The owner can untick any before approving. For a new or empty project, offer `guardrails-for-new-project`, plus `design-for-new-project` when the owner plans a user-facing UI or CLI, with the reason that checks and design notes cost least before the first code; architecture review and issue triage need existing code.
   Apply `naming-things` when choosing domain or public code names: list them in the init plan and persist glossary entries only after plan approval.
   For code, ops and hybrid, ask whether the project has a product-level specification. Create `docs/PRD.md` only on yes; a feature's requirements belong in its work item, and `ARCHITECTURE.md` is created when the project first needs one. Why: an empty placeholder looks like knowledge and is not; the table already names both homes.

5. **Safe to re-run / plug into an existing project.** The script is **additive and idempotent**: it creates only the files that are missing, leaves every existing file untouched (an existing root `AGENTS.md` is preserved verbatim and flagged for a manual pointer-merge), and **never deletes anything** (the one exception is the explicit migration below). Re-running changes nothing. Use `--dry-run` when previewing an existing or messy project. Existing files are overwritten only when explicitly forced (`--force` for files under `.bc-agent/`, `--force-root` for the root `AGENTS.md`) — don't use those unless the user asks. Nothing else is ever overwritten, not even with `--force`: root `glossary.md`, `work/` and `docs/` hold the project's own content.
   For code, ops and hybrid, when earlier-layout paths exist under `.bc-agent/` (`tasks/`, `decisions/`, `research/`, `components/`, `plans/`, `conventions/planning-workflow.md` and similar), the script writes nothing, names the paths it found and exits non-zero. Why: two sets of homes for the same knowledge would both look current. Tell the user that moving the project to the visible layout is a separate, explicit migration (see **Migrate an existing project** below). Only if the user wants the new files beside the old ones anyway, re-run with `--allow-earlier-layout`: it creates the missing files, leaves every existing file untouched and repeats the note. If the script prints **Upgrade notes for existing files left untouched**, treat them as follow-up work for the current agent: inspect the named files and merge the smallest safe pointer by hand rather than assuming the scaffold alone upgraded old instructions.

6. **Scaffold.** Run the bundled script (it lives next to this file):
   ```
   python3 <skill-dir>/scaffold.py --root "<repo-root>" --slug "<slug>" --archetype "<code|ops|learning|knowledge|hybrid>"
   ```
   Code, ops and hybrid create root `glossary.md`, lifecycle folders under `work/` with a `work/README.md` whose item table `.bc-agent/scripts/work_index.py` generates from each open item's `Blocked by:` line (no item before what it waits for; three tiers: active, then planned items an active item waits on, then other planned items; within a tier the owner's ranking in an optional `work/order.md`, then ready, then most work unblocked) with the `Stages:` line as the tiebreak (an optional `Kind:` line names what an item is; `work_index.py --check` places a new item of a kind on the `Top kinds:` line, default security, bug, build, architecture or `none`, directly below the top-kind run at the top of `order.md`, never above its blocker; `work_index.py --json` prints every item's work data for dashboards, fields in [work-data.md](work-data.md)), `docs/decisions/`, `docs/research/`, `docs/design/README.md` (the entry page of the project's design framework, with empty Pages and Checks lists the project fills; method in the `bc-design` skill's `design-framework.md`) with a `.bc-agent/map.md` line routing design, UI and CLI wording work to it, `docs/guardrails/README.md` (the project's speed, size, memory and structure limits and their checks, with empty Targets, Budgets and Checks lists; method in the `bc-performance-guardrails` skill; no measuring script) with a map line routing guardrail work to it, and `.bc-agent/` mechanics with a Where things go table and work-item template. They also create an executable `./scripts/gate` stub (the full gate; it exits non-zero until its steps are filled), a CI workflow `.github/workflows/gate.yml` that runs it on a clean checkout, and a staged `conventions/validation.md` (while working, full gate, release; one owner each). Hybrid also retains the hosted teach adapter and its mapped paths and catalog; its teach glossary is the root `glossary.md`. Learning and knowledge keep the existing vault including Obsidian metadata. Existing files remain untouched unless forced; no project is migrated by this step.

   **File accepted starter items after the scaffold.** Copy their text from [starter-items.md](starter-items.md) into the project's work-planned folder, filling the stage and date and taking the next item number under its work-item rules. Use an empty `work/order.md` for the first ranking if needed. Write the item files first; run `python3 .bc-agent/scripts/work_index.py --check` before placing their names where it says, never reordering existing entries. Regenerate the index and check again. File the items; do not start them or run any audit during setup, even if the owner says to hurry or asks for the fix now.

7. **Fill validation and layout from recon; apply upgrade notes.** For an existing code, ops or hybrid project:
   - Fill the `./scripts/gate` stub with the verified checks existing CI runs; if there was no CI before setup, use the verified local full-check commands found in step 2. Keep the generated `gate.yml`. Use only commands that run on a clean checkout with the repository's declared toolchain: CI runs the same file. Keep machine-local wrappers (guarded runners, offload) outside the gate, in how the agent invokes it. Run `./scripts/gate` locally before the scaffold commit; a successful individual check is not a gate result. Keep the filled gate if it passes or fails only on known failures recorded as such; report known red as red. If no runnable command was found, leave the non-zero stub, add a planned item to fill the gate, and name that as an owner action. For other failures you cannot resolve, name the failing check and what the owner needs to do. On a new project the stub stays red until the first real test or build command lands; never turn it green with a no-op.
   - Fill `.bc-agent/conventions/validation.md` with the verified targeted commands under **While working** and the verified `./scripts/gate` steps under **Full gate**, keeping the stage owners and budgets. Fill **Release** only if recon found release checks; otherwise keep an explicit TODO and name it in the close-out. Fill `.bc-agent/conventions/file-layout.md` with the actual paths and roles recon confirmed. Name any gap you could not fill rather than guessing checks or paths.
   - Seed other stubs only with verified facts. Do not invent architecture or move old files unless the approved plan includes it.

   For existing projects, read any scaffold upgrade notes and merge small instruction pointers into preserved files when needed (for example linking `architecture-runway.md` from existing `AGENTS.md`, `.bc-agent/AGENTS.md`, or `references/agent-skills.md`). When the notes report earlier-layout paths under `.bc-agent/` (only possible with `--allow-earlier-layout`), leave them in place and say so in the close-out: moving them to the visible layout is a separate migration the user approves.

8. **Wire publish authorization (offer).** `/bc-pipeline-to-done` needs this repo authorized in `publish.yaml` for AFK push. Detect the remote (`git remote get-url origin`). Draft a repo-specific allow rule following the existing publish-policy schema, with `paths`/`remotes` filled from this repo. Show it to the user and **offer to append it** to `~/.config/agent-concepts/publish.yaml` after they confirm. Never push that change (self-amendment immunity) — leave the user to push it. If they decline, record a line in `work/0-ideas.md` for the visible layout, or `tasks/parking-lot.md` for legacy learning/knowledge vaults.

For steps 9 and 10, `wiki_lint.py` and `runner/` sit next to the installed `bc-wiki-maintain`
`SKILL.md`. It loads only by command, so it is not in your skills list; find it from `<dir>`, the
directory this `bc-setup-project` `SKILL.md` was loaded from. Set `wiki_skill_dir` to the first
candidate where `test -f <candidate>/wiki_lint.py` succeeds (`test -f` follows symlinks; do not
use `find`):

1. `<dir>/../bc-wiki-maintain` (the contributor script, `npx skills`: `~/.agents/skills/`)
2. `<dir>/../../bc-wiki-maintain/body` (a `pi install` package: the checkout itself for a local
   path, a folder under `~/.pi/agent/git/` for a git source)

Report the wiki tools unavailable only when both fail.
Use `$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body` only as an explicit checkout override.

9. **Register the project for global search (all archetypes; default yes, opt-out).** New projects are searchable by default; append to the qmd collections file and apply it with the setup command — see the `bc-qmd` concept. Ask only if the user wants this project **excluded** ("should this one stay unindexed?") — e.g. for throwaway or sensitive repos — and then record a line containing "excluded from the global qmd index" and the reason in `.bc-agent/AGENTS.md` (learning/knowledge: `project/overview.md`), which `bc-wiki-maintain`'s lint reads. Skip the setup command if qmd is not installed, but append to the synced YAML anyway so other machines converge. Never `qmd init` inside the repo — project-local indexes shadow the global collections (see the `bc-qmd` skill).
   - **Code, ops and hybrid:** two collections, printed from the project's own table by
     `python3 "$wiki_skill_dir/wiki_lint.py" "<repo-root>/.bc-agent" --qmd-entry <slug>`.
     Append its output under `collections:` unchanged. `<slug>` is rooted at `.bc-agent/` (agent
     mechanics); `<slug>-project` is rooted at the repository with a pattern listing only the
     table's glossary, decisions, research, requirements, architecture, components, ideas and
     work paths. Why two: qmd skips every hidden path part, so a collection rooted at the
     repository cannot index `.bc-agent/`; and a pattern built from the table keeps source,
     media and vendored folders out. For a code project `demo` at `~/Projects/demo` the output is:

     ```yaml
       demo:
         path: ~/Projects/demo/.bc-agent
         pattern: "**/*.md"
         ignore: []
         contexts:
           "/": "Agent mechanics for demo: session protocol and Where things go table, map, journal log"
           "/conventions": "Validation, git, layout and workflow norms — follow these"
           "/references": "Recurring commands, paths, gotchas"

       demo-project:
         path: ~/Projects/demo
         pattern: "{glossary.md,docs/decisions/**/*.md,docs/research/**/*.md,docs/PRD.md,ARCHITECTURE.md,work/0-ideas.md,work/1-planned/**/*.md,work/2-active/**/*.md,work/3-done/**/*.md,work/4-dropped/**/*.md}"
         ignore: []
         contexts:
           "/": "Project knowledge for demo: glossary, work items (the folder is the status), decisions, research"
           "/docs/decisions": "Decision records — binding unless superseded"
           "/docs/research": "Dated investigations and architecture reviews — evidence, not authoritative"
           "/work/1-planned": "Work items agreed but not started; the folder is the status"
           "/work/2-active": "Work items in progress"
           "/work/3-done": "Finished work items by month, each with its Outcome"
           "/work/4-dropped": "Dropped work and rejected requests with the reason — check before proposing similar work"
     ```

     Afterwards the lint's `qmd registration:` line reads `registered` (or `unindexed` until the
     setup command has run on this machine). If the table changes a searchable role's path later,
     the lint reports the pattern as stale; replace the `<slug>-project` pattern with the new
     `--qmd-entry` output.
   - **Learning and knowledge:** one collection for `.bc-agent/` (collection name = the slug; copy an existing entry's shape, contexts stating each directory's *authority level*).

10. **Run wiki lint (all archetypes); offer rolling promotion (learning and knowledge only).**
    Run `python3 "$wiki_skill_dir/wiki_lint.py" "<repo-root>/.bc-agent"` for code, ops, hybrid,
    learning and knowledge. If `$HOME/.config/agent-concepts/wiki-lint-vaults.txt` already exists,
    say it is detection-only and offer to append this vault path; do not install `bc-wiki-lint.timer`.

    For code, ops and hybrid, skip the promotion offer and go to step 11: decisions and
    research go directly to the table's role folders and `log.md` is a plain journal.

    For learning and knowledge, capture into
    `.bc-agent/log.md` is cheap; promotion is not. Without a per-vault user
    timer, the new wiki will not promote overnight. This is not qmd:
    `bc-qmd-refresh.timer` only refreshes search indexes. `/bc-wiki-maintain`
    is the maintenance skill; its systemd templates
    (`$wiki_skill_dir/runner/`) do not install,
    enable, or start themselves.

    Show the user the exact slug-suffixed unit names and env, then **offer to
    install** after they confirm.
    Never copy, enable, or start units without confirmation. Never write the
    unsuffixed `bc-wiki-maintain.service` — that name may already bind another
    vault. Never vendor runner scripts into the project.

    If `systemctl --user` is unavailable, skip install and append a
    TODO in the vault parking lot pointing at `$wiki_skill_dir/runner/README.md`.

    On confirm, copy — do not symlink — the templates to slug-suffixed
    names, edit the placeholders from the runner README (WorkingDirectory,
    VAULT_ROOT, PI_BIN, SyslogIdentifier, ExecStart for a non-default skill directory, the timer's
    `Unit=`), stagger `OnCalendar` at least 15 minutes away from any
    existing `bc-wiki-maintain*.timer`, then reload and enable:

    ```bash
    unit_dir="$HOME/.config/systemd/user"
    slug="<slug>"
    vault="<repo-root>/.bc-agent"
    install -Dm644 "$wiki_skill_dir/runner/bc-wiki-maintain.service" \
      "$unit_dir/bc-wiki-maintain-${slug}.service"
    install -Dm644 "$wiki_skill_dir/runner/bc-wiki-maintain.timer" \
      "$unit_dir/bc-wiki-maintain-${slug}.timer"
    # edit placeholders, then:
    systemd-analyze --user verify "$unit_dir/bc-wiki-maintain-${slug}.service"
    systemd-analyze --user verify "$unit_dir/bc-wiki-maintain-${slug}.timer"
    systemctl --user daemon-reload
    systemctl --user enable --now "bc-wiki-maintain-${slug}.timer"
    systemctl --user status "bc-wiki-maintain-${slug}.timer"
    ```

    Resolve `PI_BIN` with `command -v pi` falling back to `$HOME/.local/bin/pi`.
    If a matching slug-suffixed unit already exists for this `VAULT_ROOT`, report it and skip.
    On decline, append the same TODO as the no-systemd case.

11. **Close out.** Point at the created files, name each starter item filed, and note the wiki-maintain timer offer outcome and any migration plan. For existing code, ops and hybrid projects, record the actual local gate result and name each unresolved gate, validation (including Release) or file-layout gap as a concrete owner action. Next steps for the user: run `/bc-triage` on existing issues or `/bc-plan-to-pipeline` for a new feature; use `/bc-prototype` or `/bc-improve-codebase-architecture` when planning needs evidence/runway; then `/bc-pipeline-to-done` to execute. Commit the scaffold (it's the user's repo — stage the new files explicitly, concise message; don't sweep unrelated drift). <!-- trigger-allow: setup recommends evidence tools for future planning; the planning pipeline does not trigger setup -->

## Migrate an existing project

Use this when a code, ops or hybrid project still has the earlier `.bc-agent/` vault (`tasks/`, `decisions/`, `research/`, `components/`, `plans/` and similar) and the user wants it in the visible layout. A project with no `.bc-agent/` gets an ordinary scaffold instead. Learning and knowledge vaults are not migrated.

1. **Hold the project if it is busy.** Migrate only a clean working tree that no other agent is working in. The script refuses uncommitted changes and lists them; leave them for the user rather than committing or stashing them yourself. This holds when the user, in a hurry, tells you to stash or commit them: name the uncommitted paths and stop until the user has committed or discarded them. A stash is easy to forget, and restoring it after files have moved can conflict. Why: the migration is one reviewable commit, and someone else's half-finished work inside it cannot be reviewed or undone separately.
2. **Dry run first and show the user the plan.** `python3 <skill-dir>/scaffold.py --root "<repo-root>" --slug "<slug>" --archetype "<code|ops|hybrid>" --migrate` writes nothing and prints `MOVE`, `CREATE`, `REPLACE`, `DELETE`, `KEPT (review by hand)`, `NEEDS JUDGMENT`, `LINKS` and `OTHER REFERENCES`. The archetype must be given explicitly. Show the user the plan and wait for approval. If the user says to skip the preview, paste the dry-run output anyway and ask for a one-word go-ahead. Why: applying replaces `.bc-agent/AGENTS.md` and moves files that other tools may name, and reading the plan costs less than untangling a wrong move.
3. **Apply.** Re-run with `--apply`. It moves whole files with `git mv` (vault `decisions/` and an existing `docs/adr/` to `docs/decisions/`, `research/` to `docs/research/`, ops and hybrid `components/` to `docs/components/`), creates the missing visible-layout files, replaces `.bc-agent/AGENTS.md` with the generated one carrying the table, deletes only empty placeholders and unmodified generated files, rewrites relative Markdown links to moved files, and stages everything without committing.
4. **Work through the judgment list.** The script leaves these untouched; apply the rule printed with each:
   - Task lists and plans (`tasks/active.md`, `tasks/completed.md`, `plans/`, `docs/plans/`, `project/*-plan*`, `project/*-tasks*`): only work still open becomes numbered work items, created in the main checkout with the next free number; finished lists are kept unchanged as one dated record in the research folder. Why: writing `Why:` and `Done when:` for finished tasks would be fiction.
   - `tasks/parking-lot.md`: meaningful lines move to the ideas file. Why: an idea is one line until someone decides to do it.
   - Issue drafts: they go inside their parent work item's folder as evidence. Why: a draft belongs to the work it slices, not to a list of its own.
   - `project/overview.md`: glossary terms move to `glossary.md`; the rest is split by role. Why: the project has one glossary.
   - Requirements documents (`project/*prd*`): project-level ones become `docs/PRD.md`, feature-level ones the work item's `requirements.md`. Why: each spec lives with what it specifies.
   - `findings/`: each becomes a dated folder in the research folder, dated from git history. Why: an invented date would mislead every later reader.
   - `open-questions/`: a blocking question becomes a step in its work item, a standalone one a planned item whose answer lands in research, a minor one a line in the ideas file. Why: `work/` stays the one place that shows what is pending.
   - `home.md`, `index.md` (not hybrid, whose `index.md` is the teach catalog) and `.obsidian/`: delete after checking for unique content.
   - The old `.bc-agent/AGENTS.md`: diff it against the new one (`git show HEAD:.bc-agent/AGENTS.md`) and carry project-specific rules into the new file.
   - Files the script did not recognise, generated files the project edited, and filename clashes: decide by hand and tell the user what you decided.
   - `KEPT (review by hand)` files are the project's own versions of generated files; merge any pointer they lack. Apply turns every wikilink that names a moved file into a relative Markdown link; ambiguous wikilinks, wikilinks in moved files that name files that stay, `OTHER REFERENCES` and unresolved links are left as they are, so fix the ones that point at moved files by hand.
5. **Show the user the result, then commit once per project.** Present the staged diff summary and what you did with each judgment item, then make one commit for the project. Why: one commit keeps the migration reviewable and revertible as a unit.

## Notes
- The project workspace is separate from the personal `~/Wiki`.
- If the repo already has a root `AGENTS.md`, the script preserves it — merge in the "read `.bc-agent/AGENTS.md` first" pointer rather than clobbering hand-written instructions.
