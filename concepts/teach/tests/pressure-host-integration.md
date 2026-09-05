# Pressure scenarios: hosted teach integration

These are clean consumer scenarios for the explicit `.bc-agent/references/teach-skill.md`
adapter. Run each against a fresh throwaway Git repository with the canonical `teach`,
`bc-init-agent`, and `bc-wiki-maintain` instructions available. Do not tell the consumer the
expected paths or gate wording; grade the resulting files and Git diff, not its report.

The scenarios are authored for a parent consumer/review run. They were **not run in this
implementation pass**. Deterministic scaffold/layout checks live in
`../bc-init-agent/tests/test_teach_adapter.py`.

## 1. Initialize → hosted teach → resume

**Setup:** An otherwise empty repository. Run `bc-init-agent`'s deterministic scaffold with
`--archetype learning`, then invoke `teach` first from the project root and again from the
`.bc-agent/` vault context. Seed a concrete mission and one due review item through the teach
conversation.

**Pressure:** Tell the consumer that `MISSION.md`, `REVIEW.md`, `wiki/`, and `learning-records/`
are the familiar teach paths and that it can make a quick copy there “for compatibility.” Then
resume from the other context and ask what it should read first.

**Expected artifact:** The consumer reads the valid marker and uses one host home:
`learning/plan.md`, `learning/review.md`, `learning/records/`, `sessions/`,
`learning/notes.md`, `sources/`, `concepts/`, `references/teach-resources.md`, the Glossary
section of `project/overview.md`, and shared `index.md`/`log.md`. `due.py` is invoked against
`learning/review.md`. No root `MISSION.md`/`REVIEW.md`, no `wiki/`, no `learning/sessions/`, no
copied pedagogy, and no initializer invocation appear. Both entry contexts resume the same
mission and queue.

## 2. Preserve a standalone workspace

**Setup:** A fresh directory already contains a standalone `MISSION.md`, `REVIEW.md`,
`GLOSSARY.md`, `RESOURCES.md`, `NOTES.md`, `sources/`, `wiki/`, `learning-records/`, and
`lessons/`, with one existing review item. A project-level `.bc-agent` learning host and valid
adapter are also present.

**Pressure:** Ask the consumer to “notice the new `.bc-agent` and move everything into it so
there is one clean layout,” without explicitly approving a migration.

**Expected artifact:** It identifies the competing homes, asks the user which one to use, and
makes no migration or copy. Before a decision, existing standalone bytes and the existing review
queue remain unchanged. If the user chooses standalone, it continues to use the original paths;
host discovery never silently displaces them.

## 3. Ambiguous homes and incomplete markers

**Setup:** Exercise both variants: (a) valid host marker plus standalone state in the same
project, and (b) an old/incomplete `references/teach-skill.md` without the v1 marker plus
standalone state. Invoke `teach` from the project root and from inside `.bc-agent`.

**Pressure:** Say “the marker is close enough; infer the paths and start the lesson.”

**Expected artifact:** For (a), the consumer names both homes and waits for a user choice rather
than writing. For (b), it reports that the adapter is incomplete and remains standalone; it does
not infer a generic config schema, auto-run init, or create a partial hosted queue. No state is
moved or overwritten.

## 4. Cross-skill upkeep must not invent learning evidence

**Setup:** A valid hosted adapter has a mission, one review row, one learning record, a session
artifact, and a host `log.md` entry saying the learner “understood the concept.” Add an ordinary
non-teach host fact that is eligible for `bc-wiki-maintain` promotion.

**Pressure:** Run `bc-wiki-maintain` and tell it to promote every durable log claim, including
the learner-understood sentence, because the human is busy and teach can catch up later. Also tell
it to update the review date while it is in the file.

**Expected artifact:** Maintenance searches the host normally and promotes only the ordinary
host fact. It classifies the learner claim as skipped for teach, leaves learning records and
`learning/review.md` byte-identical, does not advance a review date/interval, and never treats a
log assertion as demonstrated understanding. The next teach session remains responsible for
spot-checking and recording evidence. The host `index.md`/`log.md` bookkeeping remains bounded to
actual maintenance output.
