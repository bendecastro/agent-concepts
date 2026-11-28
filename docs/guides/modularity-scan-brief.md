# Modularity scan brief

Skills live in `concepts/<name>/body/` (entry SKILL.md plus linked files);
`concepts/relationships.json` lists existing `loads` edges.

Which skills do more than one job, such that splitting out one job as its own small
skill would let other skills load it instead of restating or lacking it?

For each skill in your group:
1. Name its distinct jobs: blocks a reader could follow on their own.
2. For generic jobs, search all concept bodies with `rg` for skills that restate
   them (near-duplicate wording or the same rules), or need them and lack them.

Report only candidates with evidence: proposed module and job; source skill,
section and quoted line; each restating skill and quoted line; skills it would help
and why; rough word count; risk and retesting cost (see `test_status` in
`CONCEPT.md`); and a split/leave verdict with reasons. Also list blocks repeated
in three or more skills that have no natural parent skill.

Read slices rather than whole huge files. Append findings as you go. Report at
most eight candidates, strongest first, in plain language.

## Tracked copies

Before writing a rule, use `rg` to search concept bodies for its owner; if owned
elsewhere, load it or mark a tracked `copy-of`, and if already held by two other
concepts, split it into a module. Place `<!-- copy-of: <concept>#<anchor> -->`
on its own line before the copied paragraph. It covers the next paragraph; the
source is the first paragraph after the heading with that anchor in that concept's
body Markdown; the anchor must be unique within that concept. Lint compares the paragraphs after whitespace normalization and
reports a missing source, missing anchor or mismatch as an error. Paragraphs of
at least 40 words with at least 80% shared word trigrams warn if not tracked.
