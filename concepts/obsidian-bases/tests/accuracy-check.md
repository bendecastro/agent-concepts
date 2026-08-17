# Obsidian Bases accuracy check

Reference format concept with a mutation-authority boundary. Verify source accuracy statically, then run the adversarial scenario in `pressure-scenario.md` before deployment.

## Checks

1. Parse `body/SKILL.md` frontmatter and confirm `name: obsidian-bases` matches the directory.
2. Confirm the entry body stays lean and links to `SYNTAX.md`, `FUNCTIONS.md`, `EXAMPLES.md`, and `TROUBLESHOOTING.md`.
3. Confirm the references cover YAML structure, recursive `and`/`or`/`not` filters, note/file/formula properties, table/cards/list/map views, formulas, durations, summaries, quoting, and missing-property guards.
4. Confirm all mutation wording requires explicit user intent and a safe authority, and contains no generic CLI or JavaScript-evaluation instructions.
5. Compare the adapted schema and formulas against the pinned upstream body/reference and official Bases syntax, views, and formulas documentation; resolve any drift before deployment.
6. Confirm the raw snapshot contains the upstream MIT notice and full `skills/` tree, while the deploy symlink resolves to `concepts/obsidian-bases/body/`, not `raw/`.

## Result — 2026-08-17

**PASS.** Frontmatter, progressive disclosure, `.base` schema, formula/duration guidance, pinned provenance, raw snapshot, and deployment target were checked during the selective ingest. The mutation-authority boundary then passed `pressure-scenario.md` on 2026-08-17; the fixture hash remained unchanged.
