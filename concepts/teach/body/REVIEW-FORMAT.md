# REVIEW.md Format

`REVIEW.md` is the spaced-repetition queue. It is what turns "spacing" from a stated principle into a mechanism. It lives at the workspace root and is checked at the start of every session, before new material.

## Template

```md
# Review Queue

| # | Prompt | Source | Last reviewed | Interval | Due |
|---|--------|--------|---------------|----------|-----|
| 1 | Explain why RPE 8 means two reps in reserve | LR-0003 | 2026-06-10 | 4d | 2026-06-14 |
| 2 | From memory: the three drivers of hypertrophy | LR-0001 | 2026-06-08 | 9d | 2026-06-17 |
```

- **Prompt** — a free-recall cue, phrased so the agent can ask it verbatim. Never a yes/no question.
- **Source** — the learning record or wiki page it came from.
- **Interval** — the current gap; **Due** = last reviewed + interval.

## Computing what's due

Never do the date arithmetic in your head. Run `python3 <skill dir>/scripts/due.py REVIEW.md` — it prints the due items and the exact next due date for each outcome (recalled / hard / failed). Copy those dates into the table.

## Scheduling

Use a simple expanding schedule (no algorithm worship needed):

- New item: due in **2 days**.
- Recalled correctly: roughly **double** the interval (2 → 4 → 9 → 20 → 45 days). Cap at 60 days.
- Recalled with difficulty: keep the interval the same.
- Failed: reset to **2 days**, and consider making it the focus of today's lesson.

Convert all dates to absolute dates (the agent knows today's date; the file must not contain "next week").

## Rules

- **Review before teaching.** 2–3 due items per session, every session. If nothing is due, say so and move on.
- **One concept per item.** If a prompt needs a compound answer, split it.
- **Retire items** that survive two 45–60 day intervals — move them to a `## Retired` section rather than deleting, so re-entry is cheap if the topic resurfaces.
- **Keep it under ~30 active items.** If it grows past that, consolidate overlapping prompts; an unworkable queue gets skipped, and a skipped queue is worse than a short one.

## Anki users

`REVIEW.md` only schedules reviews when a session happens; Anki nags daily on its own. If the user uses Anki (ask once, record the answer in `NOTES.md`), offer to export review items as cards instead — via AnkiConnect if their Anki is running, otherwise a genanki-generated `.apkg`. Anki then owns scheduling: keep `REVIEW.md` only as the export ledger (which items have been exported), and skip the in-session review ritual for exported items.
