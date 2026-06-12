# RESOURCES.md Format

`RESOURCES.md` is the curated catalog of trusted sources for this topic. It is the annotation layer over `./sources/` — the directory of actual ingested material (clipped articles, papers, transcripts), which is immutable once saved. Factual claims in the wiki cite these sources, not parametric guesses. Wisdom comes from the communities listed here.

When a source is ingested, save the material itself to `./sources/` (web pages rot; local copies don't) and note its filename in the annotation here.

## Structure

```md
# {Topic} Resources

## Knowledge

- [Book: _The Science and Practice of Strength Training_ — Zatsiorsky & Kraemer](https://example.com)
  Vetted: foundational academic text, widely cited. Use for: periodisation, recovery, intensity zones.
- [Article: "How Much Should I Train?" — Greg Nuckols (Stronger By Science)](https://example.com)
  Vetted: evidence review with primary citations; author is a recognised practitioner. Use for: weekly volume targets. Ingested: `sources/nuckols-volume.md` → [summary](wiki/source-nuckols-volume.md).

## Wisdom (Communities)

- [r/weightroom](https://reddit.com/r/weightroom)
  High-signal subreddit, moderated against bro-science. Use for: programme critique, plateau troubleshooting.
- Local: Tuesday strength class at {gym name}
  Use for: real-time coaching feedback on lifts.

## Gaps

- {Areas the mission needs that no good resource yet covers — drives future search}
```

## Vetting protocol

A resource does not become "high-trust" by being added to this file — it must earn entry. Before adding one, check:

1. **Authority** — is the author a recognised expert, primary source, or peer-reviewed venue? Who else cites them?
2. **Incentive** — is it education or marketing? Content that funnels toward a product sale is suspect.
3. **Citations** — does it cite primary sources itself, or assert from nowhere?
4. **Cross-check** — does at least one independent trusted source agree on its core claims?

Record the vetting outcome in the annotation (`Vetted: ...`). If you cannot vet a source, list it under `## Gaps` as a candidate, not under Knowledge.

## Rules

- **Annotate every entry.** A bare link is useless in three months: one line on what it covers and when to reach for it.
- **Group by Knowledge / Wisdom.** A resource may appear in only one group.
- **Prune ruthlessly.** A resource that turned out wrong, shallow, or off-mission gets removed, not buried. Five sharp sources beat thirty mediocre ones.
- **Record community preferences.** If the user opts out of communities, note it here so future sessions stop proposing them.
