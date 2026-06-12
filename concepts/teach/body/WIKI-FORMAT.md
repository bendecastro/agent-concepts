# Wiki Format

`./wiki/*.md` is the compiled knowledge of this workspace: interlinked markdown pages the agent writes and maintains entirely. The user reads it; the agent owns it. It sits between the raw sources (`./sources/`, `RESOURCES.md`) and the teaching — lessons draw from the wiki, the wiki cites the sources. Knowledge is compiled once on ingest and then *kept current*, not re-derived every session.

## Page types

- **Concept pages** (`hypertrophy.md`, `ownership.md`) — one concept each: a tight explanation, how it relates to neighboring concepts, common misconceptions, citations.
- **Source summaries** (`source-nuckols-volume.md`) — the distilled takeaways of one ingested source, written during ingest.
- **Synthesis pages** (`comparison-tempo-vs-load.md`) — comparisons, analyses, and answers to user questions that were worth keeping.

File names are dash-case. One page, one subject — split pages that sprawl.

## Page conventions

- **Link densely.** Use relative markdown links to other wiki pages (`[progressive overload](./progressive-overload.md)`). The connections are as valuable as the pages. A page nothing links to is a lint finding.
- **Cite everything.** Every factual claim links to a source summary page or an entry in `RESOURCES.md`. Uncited claims are parametric guesses and don't belong here.
- **Flag contradictions, don't bury them.** When a new source disagrees with an existing claim, state both positions and which source says what. Resolving the contradiction is a conversation with the user, not a silent edit.
- **Use glossary terms.** Once a term is in `GLOSSARY.md`, the wiki uses it — including inside other pages' explanations.
- **Keep pages current.** When an ingest or lesson changes the picture, update every affected page in the same pass. Stale pages are worse than missing ones.
- **Printable on demand.** If the user wants a printable cheat sheet (poses, syntax tables, routines), render the relevant wiki page(s) to a clean HTML file in `./lessons/` style — the markdown wiki page remains the source of truth.

## index.md

Lives at the workspace root. A catalog of every page in the workspace — wiki pages, source summaries, learning records, lessons — one line each:

```md
# Index

## Concepts
- [Progressive overload](wiki/progressive-overload.md) — increasing demand over time; the engine of adaptation
- [RPE](wiki/rpe.md) — perceived-exertion scale; how intensity is prescribed here

## Sources
- [Nuckols — How Much Should I Train?](wiki/source-nuckols-volume.md) — volume landmarks evidence review (ingested 2026-06-12)

## Learning records
- LR-0001 — knows basic barbell lifts from prior gym experience — active
```

Update it on every write. At session start, read the index and drill into pages it points to — never skim the whole workspace.

## log.md

Lives at the workspace root. Append-only, chronological. Every session appends at least one entry:

```md
## [2026-06-12] lesson | RPE and autoregulation
Taught RPE scale; user demonstrated by rating a recalled set correctly (LR-0004). Added review item #7.

## [2026-06-12] ingest | Nuckols volume article
Vetted and ingested; touched progressive-overload.md, volume.md. Contradicts earlier claim on weekly set ceilings — flagged in volume.md.
```

Entry types: `lesson`, `ingest`, `review`, `lint`. The consistent prefix keeps it parseable: `grep "^## \[" log.md | tail -5` shows recent activity. Keep entries to 1–3 lines — the log is a timeline, not a journal; insights belong in learning records or wiki pages.
