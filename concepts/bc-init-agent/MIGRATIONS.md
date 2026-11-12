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
[the visible-layout plan](../../docs/plans/implemented/bc-init-agent-visible-layout.md)). The agent
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
  migration moved (`/decisions`, `/research`, `/project`, `/components`, ...), since their files
  now live in `<slug>-project`. Otherwise append both blocks. Then run the setup command (see the
  `qmd` concept). `wiki_lint.py "<repo>/.bc-agent"` then reports `qmd registration: registered`.
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
non-Homeflix maps (Music, Scripts, image-maze, CV, codebase-design, and sql) have in-vault targets
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
   | codebase-design | 21 → 18 |
   | image-maze | 15 → 13 |

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
