# Wiki Format

`./wiki/*.md` is the compiled knowledge of a standalone workspace: interlinked markdown pages the agent writes and maintains entirely. With the explicit `.bc-agent/references/teach-skill.md` adapter, use the existing `./concepts/` directory in the host vault instead — never create a parallel hosted `wiki/`. The user reads it; the agent owns it. It sits between the raw sources (`./sources/`, and the resolved resource catalog) and the teaching — lessons draw from the knowledge pages, which cite the sources. Knowledge is compiled once on ingest and then *kept current*, not re-derived every session.

### Hosted path substitutions

When hosted, resolve these surfaces relative to `<teach-root>`: raw sources remain `sources/`; compiled wiki pages are `concepts/`; the resource catalog is `references/teach-resources.md`; the glossary is the existing Glossary section of `project/overview.md`; and the shared catalog/history remain `index.md` / `log.md`. The standalone `GLOSSARY.md`, `RESOURCES.md`, and `wiki/` paths remain authoritative only when no valid adapter is present.

## Page types

- **Concept pages** (`hypertrophy.md`, `ownership.md`) — one concept each: a tight explanation, how it relates to neighboring concepts, common misconceptions, citations.
- **Source summaries** (`source-nuckols-volume.md`) — the distilled takeaways of one ingested source, written during ingest.
- **Synthesis pages** (`comparison-tempo-vs-load.md`) — comparisons, analyses, and answers to user questions that were worth keeping.

File names are dash-case. One page, one subject — split pages that sprawl.

## Page conventions

- **Link densely.** Use relative markdown links to other wiki pages (`[progressive overload](./progressive-overload.md)`). The connections are as valuable as the pages. A page nothing links to is a lint finding.
- **Cite everything.** Every factual claim links to a source summary page or an entry in the resolved resource catalog (`RESOURCES.md` standalone or `references/teach-resources.md` hosted). Uncited claims are parametric guesses and don't belong here.
- **Flag contradictions, don't bury them.** When a new source disagrees with an existing claim, state both positions and which source says what. Resolving the contradiction is a conversation with the user, not a silent edit.
- **Use glossary terms.** Once a term is in the resolved glossary (`GLOSSARY.md` standalone or the Glossary section of `project/overview.md` hosted), the knowledge pages use it — including inside other pages' explanations.
- **Keep pages current.** When an ingest or lesson changes the picture, update every affected page in the same pass. Stale pages are worse than missing ones.
- **Printable on demand.** If the user wants a printable cheat sheet (poses, syntax tables, routines), render the relevant knowledge page(s) to a clean HTML file in the resolved lesson/session directory (`./lessons/` standalone or existing `./sessions/` hosted) — the markdown knowledge page remains the source of truth.

## index.md

Lives at the standalone workspace root, or at the host vault root when the adapter is active. It is the shared catalog of every relevant page — knowledge pages, source summaries, learning records, and lesson/session artifacts — one line each:

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

Update the resolved `index.md` on every teach write, preserving unrelated host entries. At session start, read it and drill into pages it points to — never skim the whole workspace.

## log.md

Lives at the standalone workspace root or host vault root. It is append-only and chronological; every session appends at least one teach entry:

```md
## [2026-06-12] lesson | RPE and autoregulation
Taught RPE scale; user demonstrated by rating a recalled set correctly (LR-0004). Added review item #7.

## [2026-06-12] ingest | Nuckols volume article
Vetted and ingested; touched progressive-overload.md, volume.md. Contradicts earlier claim on weekly set ceilings — flagged in volume.md.
```

Entry types: `lesson`, `ingest`, `review`, `lint`. The consistent prefix keeps the resolved log parseable: `grep "^## \[" log.md | tail -5` shows recent activity. Keep entries to 1–3 lines — the log is a timeline, not a journal; insights belong in learning records or knowledge pages.
