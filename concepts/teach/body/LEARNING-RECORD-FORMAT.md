# Learning Record Format

Learning records live in `./learning-records/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc. Create the directory lazily — only when the first record is written.

They are the teaching equivalent of ADRs: they capture demonstrated understanding, disclosed prior knowledge, and corrected misconceptions. They are the input to the zone of proximal development, so their integrity matters more than their volume.

## Template

```md
---
Status: demonstrated # demonstrated | self-reported | misconception | superseded by LR-NNNN
---

# {Short title of what was learned or established}

{1-3 sentences: what was learned, and why it matters for future sessions.}

## Evidence
{How the user demonstrated it: the question they answered, the thing they produced, or the exact prior experience they claimed. Required — a record without evidence/status is a guess, and guesses corrupt future difficulty calibration.}
```

## Status values

- **demonstrated** — the user explained, applied, or produced something that shows understanding. Future sessions may rely on it.
- **self-reported** — the user claimed prior knowledge, but it was not demonstrated. Future sessions must spot-check before using it as the ZPD floor.
- **misconception** — the user exposed a wrong model worth remembering. Do not mark it corrected unless the corrected understanding was later demonstrated.
- **superseded by LR-NNNN** — a later record replaces this one.

## Optional sections

- **Implications** — what this unlocks or rules out for future sessions, when non-obvious.

## The evidence bar

Write a `demonstrated` record only when the user has *demonstrated* understanding — explained it back correctly, applied it to a new case, or produced something that works. Hold the bar deliberately high:

- A half-right answer is not evidence. Probe with a follow-up before crediting.
- Your own generosity is the failure mode: an over-credited record sets the ZPD floor too high and makes every future lesson land above the user's head.
- For disclosed prior knowledge ("I already know X"), record the *depth claimed* as `self-reported` unless a spot-check demonstrates it. Self-reported records are memory aids, not evidence.

## When to write a record

1. The user demonstrated genuine understanding of something non-trivial (per the evidence bar above) — `Status: demonstrated`.
2. The user disclosed prior knowledge — `Status: self-reported`; include claimed depth and what to spot-check before relying on it.
3. A misconception appeared — `Status: misconception`; high-value because it predicts future stumbling blocks. Mark a correction separately only after the corrected understanding is demonstrated.
4. The mission shifted in response to learning — update `MISSION.md` and cross-reference it here.

### What does _not_ qualify

- Material merely covered. Coverage is not learning; wait for evidence.
- Term definitions already captured in `GLOSSARY.md`.
- Session activity logs. Records are decision-grade insights, not a journal.

## Supersession

When a later record contradicts an earlier one, mark the old record `Status: superseded by LR-NNNN` rather than deleting it. How understanding evolved is itself useful signal.

## Index

Every record gets a one-line entry (`LR-0001 — title — demonstrated`) in the workspace `index.md` under `## Learning records`, updated when the record is written or superseded. Sessions read the index and open only relevant records.
