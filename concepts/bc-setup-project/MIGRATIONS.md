# One-time migrations

This file holds procedures for an existing initialized vault. It is a human-facing reference, not
an injected agent instruction. The scaffold remains additive: it creates the new form for a new
vault and reports a manual upgrade note for an existing one, but it does not rewrite live files.

## Visible layout

Running the current scaffold with `--archetype code`, `ops` or `hybrid` on a project that already
has the earlier vault layout writes nothing: it names the earlier-layout paths it found under
`.bc-agent/` and exits non-zero. The paths it looks for are `tasks`, `decisions`, `research`,
`scratch`, `out-of-scope`, `home.md`, `components`, `findings`, `open-questions`, `plans`,
`conventions/planning-workflow.md`, `templates/plan.md` and `project`, and for code and ops also
`index.md` (hybrid generates it as its teach catalog). A `.bc-agent/project/overview.md` from an
earlier hybrid scaffold holds a separate teach glossary; hybrid now shares the root `glossary.md`,
so its terms move there when the project is migrated. `open-questions` is detected because the
visible layout has no open-questions folder: open questions become work-item steps, planned work
items or lines in `work/0-ideas.md`. Why: creating the visible homes
beside the old ones would leave two glossaries, two decision homes and two status mechanisms.

`--allow-earlier-layout` restores the additive behaviour: the scaffold creates the missing
visible-layout files, leaves every existing file byte-identical (including a custom
`.bc-agent/AGENTS.md`), and prints the same paths as an upgrade note. It also notes when
`.bc-agent/AGENTS.md` has no "Where things go" table.

### Migrate mode

`scaffold.py --migrate` moves one project to the visible layout (work package W4 of
[the visible-layout plan](../../work/3-done/2026-11/018-bc-init-agent-visible-layout.md)). The agent
procedure, including the rule for each judgment class, is in the skill body under
"Migrate an existing project"; this section records what the script does and does not do.

- Without `--apply` it writes nothing and prints the plan. With `--apply` it performs the plan,
  stages it and does not commit.
- It refuses, writing nothing, when the root is not a git repository root, the working tree is not
  clean, there is no `.bc-agent/`, `.bc-agent/AGENTS.md` already has a "Where things go" table, the
  archetype is learning or knowledge, or a destination already exists as a different file.
  `--archetype` must be explicit: nothing in an earlier vault records it reliably.
- Moves (`git mv`, content unchanged except links): vault `decisions/` and root `docs/adr/` to
  `docs/decisions/`, vault `research/` to `docs/research/`, and for ops and hybrid vault
  `components/` to `docs/components/`. Two files that would land on the same path, or a file whose
  identical copy is already at the destination, are listed for judgment instead.
- Creates the missing visible-layout files; replaces only `.bc-agent/AGENTS.md`; lists other
  generated files the project already has under "kept, review by hand".
- Deletes only `.gitkeep` files in moved folders, `scratch/` and `out-of-scope/` holding nothing
  else, and `conventions/planning-workflow.md` and `templates/plan.md` when they equal the current
  generator's text for any date. Earlier generator versions differ, so in practice those two
  usually land in the judgment list.
- Rewrites relative Markdown links (inline and reference definitions, outside code fences and
  inline code) in every tracked `.md` file whose target moved, and links inside moved files.
  A folder link is rewritten only when the whole folder moved. Link labels are not changed.
- Rewrites every `[[wikilink]]` (outside code) whose target moves into a relative Markdown link
  from the containing file's new place: `[[name|label]]` keeps the label, `[[name#Heading]]` gets a
  GitHub-style anchor, a Markdown embed becomes a plain link and a moved image embed becomes
  `![](path)`. Targets resolve as Obsidian does: bare name by basename (case-insensitive, `.md`
  optional) anywhere in the repository, path form by path suffix. Why: the Obsidian settings are
  retired, and plain links resolve in any viewer and for agents (plan decision 32).
- Reports and leaves: unresolved Markdown links, a bare wikilink name matching more than one file
  when one of them moves, wikilinks in moved files that name files that stay (they resolve only
  inside an Obsidian vault), wikilinks to files that stay, and literal old paths in other tracked
  text files.
- After apply and commit, `--migrate` refuses (the table exists), and the ordinary scaffold no
  longer names the moved folders as earlier layout; folders still awaiting judgment are named.

A 2026-11-12 trial on clones of one code and one ops project (not the projects themselves) moved a
`docs/adr/` with 29 link rewrites, and showed that an Obsidian-linked ops vault has about a hundred
wikilinks to moved files; a rerun on a fresh clone of that ops project rewrote 108 wikilinks in 27
files, none ambiguous, all resolving, and left 32 wikilinks from moved files to files that stay.

### Search, promotion and project agents after migration (owner decisions 2026-11-12)

A project already migrated to the visible layout needs these follow-ups, done by hand on the machine
that holds the synced qmd collections file:

- **Register for search.** Print the entries from the project's own table and compare them with
  the collections file:

  ```bash
  python3 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/wiki_lint.py" "<repo>/.bc-agent" --qmd-entry <slug>
  ```

  If the project already has a `<slug>` collection rooted at `.bc-agent/`, keep it (the setup
  command will not re-point an existing name at a new path) and append only the printed
  `<slug>-project` block; drop stale contexts from the old entry that name vault folders the
  migration moved (`/decisions`, `/bc-research`, `/project`, `/components`, ...), since their files
  now live in `<slug>-project`. Otherwise append both blocks. Then run the setup command (see the
  `bc-qmd` concept). `wiki_lint.py "<repo>/.bc-agent"` then reports `qmd registration: registered`.
- **Project agents row.** Edit the one table row in `.bc-agent/AGENTS.md` from
  `` | project-agents | — | not yet decided; ask the owner before creating project-specific agents | ``
  to
  `` | project-agents | `.agents/agents/` | created on first need; one `local-<name>.md` file per agent, beside `.agents/skills/` | ``.
  Nothing else changes; the folder is created when the first agent is.
- **Promotion: nothing to do.** Promotion is retired for the visible layout, and the runner exits
  0 with "promotion is not applicable" for such a project. A per-project promotion timer or a
  `wiki-promotion-vaults.txt` entry for it can be removed at leisure; leaving it costs one no-op
  run per night. Keep the lint-list entry.

## Migrate existing `map.md` files to graph-visible links

### Why this is a separate migration

The current `scaffold.py` template emits real relative Markdown links, but its additive write rule
leaves every existing `map.md` untouched. `upgrade_notes()` reports the missing generated link as a
manual merge hint. This procedure applies that one-time change to the eight vaults listed by the
machine-local lint configuration.

The source of vault paths is:

```bash
vault_list="$HOME/.config/agent-concepts/wiki-lint-vaults.txt"
test -r "$vault_list"
grep -Ev '^[[:space:]]*(#|$)' "$vault_list"
```

That file is machine-local. Work through its current non-comment entries; do not copy vault paths
from another machine or add a path merely because it appears in a different local list.

### Rule: link only targets inside the vault

For each bullet in `map.md`, inspect the first backtick-delimited path. Convert an entry only when
that path resolves to an existing page **inside the vault root**. Use the same vault-relative path
as both the label and the link target:

```markdown
- `project/overview.md`
```

becomes:

```markdown
- [project/overview.md](project/overview.md)
```

Do not convert every backtick in the file; code examples and prose are not map edges. Leave a path
that points outside the vault as an inline-code span, even when the corresponding file exists at
the repository root. `wiki_lint.resolve_link()` recognises pages in the vault graph; converting an
outside path literally creates a broken-link finding, while a corrected parent-relative link still
cannot add an edge to this vault.

Both Homeflix maps have 15 out-of-vault source-tree rows. Leave those rows inline code. The six
non-Homeflix maps (Music, Scripts, project B, CV, bc-codebase-design, and sql) have in-vault targets
that can become links.

### Per-vault procedure

Repeat this sequence for every entry in `wiki-lint-vaults.txt`. Each entry is a separate Git
working tree. Replace the example value below with the selected entry; do not run the procedure
while the repository has unrelated changes.

```bash
export AGENT_CONCEPTS="$HOME/path/to/agent-concepts"
vault="$HOME/path/to/your/project/.bc-agent"  # replace with one lint-list entry
repo_root="$(git -C "$vault" rev-parse --show-toplevel)"
vault_prefix="$(git -C "$vault" rev-parse --show-prefix)"
git -C "$repo_root" status --short --untracked-files=all
```

A non-empty status is a stop: clean or commit the unrelated work before changing the map. The
promotion runner also requires the complete containing repository to be clean, not merely the
vault directory.

1. Capture the pre-migration report. `wiki_lint.py --json` emits `broken_links`,
   `ambiguous_links`, and `orphans`; exit status 1 is allowed when a report already contains a
   detector finding, but an invalid vault or another status is an error.

   ```bash
   before="$(mktemp)"
   before_status=0
   python3 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/wiki_lint.py" \
     "$vault" --json >"$before" || before_status=$?
   (( before_status == 0 || before_status == 1 )) || exit "$before_status"
   python3 - "$before" <<'PY'
   import json
   import sys
   report = json.load(open(sys.argv[1], encoding="utf-8"))
   for key in ("broken_links", "ambiguous_links", "orphans"):
       print(f"{key}={len(report[key])}")
   PY
   ```

2. Edit only the selected map:

   ```bash
   $EDITOR "$vault/map.md"
   ```

   For each map row, verify that the target resolves under `$vault` before changing its syntax.
   Keep the existing section headings, labels, annotations, and duplicate rows. The migration is
   a syntax change, not a map redesign.

3. Review the exact diff and ensure no other working-tree file changed:

   ```bash
   git -C "$repo_root" diff --check -- "${vault_prefix}map.md"
   git -C "$repo_root" diff -- "${vault_prefix}map.md"
   git -C "$repo_root" status --short --untracked-files=all
   ```

4. Capture the post-migration report and compare it with the saved report:

   ```bash
   after="$(mktemp)"
   after_status=0
   python3 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/wiki_lint.py" \
     "$vault" --json >"$after" || after_status=$?
   (( after_status == 0 || after_status == 1 )) || exit "$after_status"
   python3 - "$before" "$after" <<'PY'
   import json
   import sys
   before = json.load(open(sys.argv[1], encoding="utf-8"))
   after = json.load(open(sys.argv[2], encoding="utf-8"))
   for key in ("broken_links", "ambiguous_links"):
       old, new = len(before[key]), len(after[key])
       if new != old:
           raise SystemExit(f"{key} changed: {old} -> {new}")
   old_orphans, new_orphans = len(before["orphans"]), len(after["orphans"])
   if new_orphans > old_orphans:
       raise SystemExit(f"orphans increased: {old_orphans} -> {new_orphans}")
   print(f"broken_links={len(after['broken_links'])}")
   print(f"ambiguous_links={len(after['ambiguous_links'])}")
   print(f"orphans={old_orphans} -> {new_orphans}")
   PY
   ```

   The surveyed expectation is **0 new broken and 0 new ambiguous** in the six standard vaults.
   The invariant is that broken and ambiguous counts stay at their pre-migration values (0 in
   every surveyed vault). For the six standard maps, the plan's expected orphan changes are:

   | Vault | Orphans before → after |
   |---|---:|
   | Scripts | 7 → 3 |
   | CV | 12 → 8 |
   | sql | 17 → 13 |
   | Music | 12 → 9 |
   | bc-codebase-design | 21 → 18 |
   | project B | 15 → 13 |

   Both Homeflix maps carry 15 out-of-vault source-tree rows that stay inline code. Do not force
   an orphan reduction there; a rise in broken links means an outside target was converted by
   mistake. If any invariant fails, restore the map, inspect the target classification, and rerun
   the report before continuing.

5. Commit the map change in that repository only. Confirm the staged path before committing:

   ```bash
   git -C "$repo_root" add -- "${vault_prefix}map.md"
   git -C "$repo_root" diff --cached --name-only
   git -C "$repo_root" commit -m "wiki: make map links graph-visible"
   git -C "$repo_root" status --short --untracked-files=all
   ```

   The final status must be clean before the next scheduled promotion. Do not stage or commit
   unrelated work. The promotion runner refuses a dirty repository, so leaving an uncommitted map
   edit in place blocks that vault on the next scheduled pass.

### Completion check

Repeat the per-vault report and commit sequence for all eight current lint-list entries. The
migration is complete only when every selected repository has a clean working tree and its
post-migration report preserves the broken/ambiguous invariant. Future vaults receive graph-visible
maps directly from `scaffold.py`; this procedure is only for existing additive installations.

## Work index

Since 2026-11-16 the visible-layout scaffold also writes `.bc-agent/scripts/work_index.py`, a
`work/README.md` with a generated empty index, a `Stages:` line and a `Stage:` rule in the Work
items section of `.bc-agent/AGENTS.md`, "run the index" in three Keep-it-current rows, and a
`Stage:` line in the work-item template. To adopt it in an existing visible-layout project:

1. First run the scaffold with `--dry-run`: an additive re-run recreates any scaffold file the
   project deleted on purpose. Then re-run (`scaffold.py --root <project> --archetype <archetype>`).
   It creates the script and `work/README.md` when missing and leaves existing files alone. To
   refresh just the script, run `cp "$AGENT_CONCEPTS/concepts/bc-setup-project/body/work_index.py" .bc-agent/scripts/`.
   `--force` also refreshes it, along with every other `.bc-agent/` file.
2. In `.bc-agent/AGENTS.md`, add the project's stages in order on a `Stages:` line in the Work
   items section (default `now, next, later, unscheduled`), the `Stage:` rule and the
   Keep-it-current additions from a fresh scaffold; add `Stage:` under `Done when:` in
   `.bc-agent/templates/work-item.md`.
3. Give every item in `work/1-planned/` and `work/2-active/` a `Stage:` line directly under
   `Done when:`, then run `python3 .bc-agent/scripts/work_index.py`. It fails, naming the item,
   while any open item has a missing or unknown stage. An existing `work/README.md` needs the
   `<!-- work-index:start -->` and `<!-- work-index:end -->` markers added where the table goes.
4. Add `python3 .bc-agent/scripts/work_index.py --check` to the project's lint or CI, so a stale
   table fails the build.

The `bc-work-sync` skill proposes these steps in its plan when a project lacks them.

## Blocked by

Since 2026-11-22 every open work item in a visible-layout project names what it waits for on a
`Blocked by:` line under `Stage:`: full item names, comma-separated, or `nothing`. The script
rejects a missing line, an unknown or dropped blocker, a self-block and a cycle, and orders the
table topologically (active, then ready, then most open items unblocked, then stage, then name),
with `#`, `Waits on` and `Unblocks` columns. The generated `.bc-agent/AGENTS.md` gains four rules
(every open item has a `Blocked by:` line; a building block gets its own item; look for overlap
before creating an item; one item, one deliverable). To adopt it in an existing visible-layout
project:

1. Copy the script: `cp "$AGENT_CONCEPTS/concepts/bc-setup-project/body/work_index.py" .bc-agent/scripts/`.
   Its tests live in the concept (`tests/test_work_index.py`); a project that keeps its own copy
   of tests for the script updates them in the same change.
2. Add `Blocked by: <full names of the items this waits for, such as 012-search-ranking, or "nothing">`
   under `Stage:` in `.bc-agent/templates/work-item.md`.
3. In the Work items section of `.bc-agent/AGENTS.md`, copy the four rules from a fresh scaffold,
   and say in the `Stage:` rule that the table is ordered by `Blocked by:` with the stage as the
   tiebreak. Update any prose in `work/README.md` that says the table is ordered by stage.
4. Give every item in `work/1-planned/` and `work/2-active/` a real `Blocked by:` line: read each
   item and name the items whose result it needs, or `nothing`. Do not write `nothing` everywhere
   to get the script to pass; the order is only as true as these lines. Where two items wait on
   one step of a third, split that step into its own item first.
5. Run `python3 .bc-agent/scripts/work_index.py`. It fails, naming the item, until every open item
   has a valid line; then `--check` passes.

The `bc-work-sync` skill reports open items with no `Blocked by:` line and blockers naming unknown
or dropped items.

## Owner order

Since 2026-11-22 `work_index.py` reads an optional `work/order.md`: the owner's ranking of open
items, top first, one numbered line each (`1. 012-search-ranking`); other lines are ignored.
The table has three tiers: active items, then planned items an active item is (transitively)
blocked by, then other planned items. Within a tier, listed items come in list order, before
unlisted ones; an item still never comes before an open item it is blocked by. Done and dropped
names (month folders included) are skipped unless an open item has the name; an unknown or
repeated name is an error. The tiers apply with or without the file, so blockers of active items
can move up even in a project with no `order.md`. To adopt it in an existing project:

1. Copy the script: `cp "$AGENT_CONCEPTS/concepts/bc-setup-project/body/work_index.py" .bc-agent/scripts/`.
2. Optionally copy the `work/order.md` rule from a fresh scaffold's `.bc-agent/AGENTS.md` into the
   Work items section, and replace any older summary of the table order in the `Stage:` and
   `Blocked by:` rules and in `work/README.md` with the fresh scaffold's wording (three tiers;
   regenerate after changing `order.md`).
3. Run `python3 .bc-agent/scripts/work_index.py`, then `--check`.

Since 2026-11-23 `--check` also fails while `order.md` leaves out an open item or lists an item
above one it waits on, and the fresh scaffold adds the rule "Never reorder `work/order.md`; place
what you add". A project with an `order.md` re-copies the script (step 1) and the rule (step 2);
a project without one is unaffected.

## Design README

Since 2026-11-21 the code, ops and hybrid scaffold also writes `docs/design/README.md`, the entry
page of the project's design framework (how the product looks and behaves now; its method is the
`bc-ui-design` skill's `design-framework.md`), and a line in `.bc-agent/map.md` routing design, UI and
CLI wording work to it. Learning and knowledge vaults do not get it. To adopt it in an existing
project, one project at a time on its next scaffold run:

1. Re-run the scaffold (`--dry-run` first, as above). It creates `docs/design/README.md` when
   missing and never overwrites an existing one.
2. The existing `.bc-agent/map.md` is left alone, and the scaffold prints an upgrade note while it
   lacks the line. Copy the line from a fresh scaffold's map into the "Outside this folder" section.
3. If the project already keeps design pages elsewhere, list them under Pages in the README rather
   than moving them, unless the owner asks for the move.

## Guardrails README

Since 2026-11-25 the code, ops and hybrid scaffold also writes `docs/guardrails/README.md`, the
page listing the project's speed, size, memory and structure limits and their checks (its method is
the `bc-performance-guardrails` skill), and a line in `.bc-agent/map.md` routing guardrail work to it. Learning and
knowledge vaults do not get it, and no measuring script is scaffolded. Existing projects are not
swept: the `bc-performance-guardrails` skill copies the page text the first time guardrail work comes up. A
scaffold re-run also creates it when missing (never overwriting one) and prints an upgrade note
while the map lacks the line; copy the line from a fresh scaffold's map into "Outside this folder".

## Source line

Since 2026-11-22 the work-item template has an optional `Source:` line under `Issue:`, naming the
skill or review that produced the item (for example `bc-plan-to-pipeline` or
`bc-improve-codebase-architecture`). The scaffold does not rewrite an existing template; to adopt it,
copy the line from a fresh scaffold's `.bc-agent/templates/work-item.md`. Existing items need no
change: the line is optional.

## Work data

Since 2026-11-25 `work_index.py --json` prints every work item's data for a dashboard (fields in
the skill's [work-data.md](body/work-data.md)), the scaffold also writes
`.bc-agent/scripts/work_spent.py`, which estimates an item's time, tokens and cost from the agent
tools' session files, and the Work items rules in `.bc-agent/AGENTS.md` tell agents to write four
lines: `Held by:` while an agent works on an item, `Review:` and `Gate:` in a step's Notes, and
`Spent:` at the end of a finished item's Outcome. To adopt it in an existing project:

1. Copy both scripts: `cp "$AGENT_CONCEPTS"/concepts/bc-setup-project/body/{work_index,work_spent}.py .bc-agent/scripts/`.
   A scaffold re-run (`--dry-run` first) creates `work_spent.py` when missing but leaves an existing
   `work_index.py` alone; `--force` refreshes both, along with every other `.bc-agent/` file.
2. In `.bc-agent/AGENTS.md`, copy the `Held by:`, `Review:`/`Gate:` and `Spent:` rules from the
   Work items section of a fresh scaffold, and its "Begin agreed work", "Finish a step" and
   "Finish or drop an item" rows. Without them agents keep working as before and the lines are
   simply not written.

Existing items need no change. All four lines are optional: an item without them gets `null` for
`held_by` and `spent` and empty `review` and `gate` lists in the JSON, and `--check` does not
warn. Items get a `history` from git with no change at all. Only a malformed line, or a `Held by:`
line left in a done item, gives a `--check` warning.

## Needs owner line

Since 2026-11-26 the Work items rules in `.bc-agent/AGENTS.md` and the work-item template have an
optional `Needs owner: <what the owner must decide or do, and when>` line, for an item that will
need an owner decision or action before or during its build; it is removed once settled.
`work_index.py --json` reports it as `header.needs_owner`. To adopt it in an existing project:

1. In `.bc-agent/AGENTS.md`, copy the `Needs owner:` rule from the Work items section of a fresh
   scaffold, below the `Kind:` rule.
2. Copy the `Needs owner:` line from a fresh scaffold's `.bc-agent/templates/work-item.md` into the
   project's template, below `Kind:`.
3. Copy the script: `cp "$AGENT_CONCEPTS"/concepts/bc-setup-project/body/work_index.py .bc-agent/scripts/`.
4. Add the line to any open item that already needs an owner decision or action.

Without step 3 the line is still written and read from the item file; only the JSON lacks it.
