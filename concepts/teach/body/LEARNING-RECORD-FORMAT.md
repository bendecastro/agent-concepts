# Learning Record Format

Learning records live in `./learning-records/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc. Create the directory lazily — only when the first record is written.

They are the teaching equivalent of ADRs: they capture demonstrated understanding, disclosed prior knowledge, and corrected misconceptions. They are the input to the zone of proximal development, so their integrity matters more than their volume.

## Template

```md
# {Short title of what was learned or established}

{1-3 sentences: what was learned, and why it matters for future sessions.}

## Evidence
{How the user demonstrated it: the question they answered, the thing they produced, the prior experience they cited. Required — a record without evidence is a guess, and guesses corrupt future difficulty calibration.}
```

## Optional sections

- **Status** frontmatter (`active | superseded by LR-NNNN`) — when an earlier understanding turns out wrong and is replaced.
- **Implications** — what this unlocks or rules out for future sessions, when non-obvious.

## The evidence bar

Write a record only when the user has *demonstrated* understanding — explained it back correctly, applied it to a new case, or produced something that works. Hold the bar deliberately high:

- A half-right answer is not evidence. Probe with a follow-up before crediting.
- Your own generosity is the failure mode: an over-credited record sets the ZPD floor too high and makes every future lesson land above the user's head.
- For disclosed prior knowledge ("I already know X"), record the *depth claimed* and spot-check it with one question before treating it as a floor.

## When to write a record

1. The user demonstrated genuine understanding of something non-trivial (per the evidence bar above).
2. The user disclosed prior knowledge — record it with claimed depth so it isn't re-taught.
3. A misconception was corrected — high-value; these predict future stumbling blocks.
4. The mission shifted in response to learning — update `MISSION.md` and cross-reference it here.

### What does _not_ qualify

- Material merely covered. Coverage is not learning; wait for evidence.
- Term definitions already captured in `GLOSSARY.md`.
- Session activity logs. Records are decision-grade insights, not a journal.

## Supersession

When a later record contradicts an earlier one, mark the old record `Status: superseded by LR-NNNN` rather than deleting it. How understanding evolved is itself useful signal.

## Index

Every record gets a one-line entry (`LR-0001 — title — active`) in the workspace `index.md` under `## Learning records`, updated when the record is written or superseded. Sessions read the index and open only relevant records.
