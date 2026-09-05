---
name: teach
description: Use when the user wants to learn a topic or skill over multiple sessions, with this directory as their dedicated learning workspace or an explicit .bc-agent teach adapter.
argument-hint: "What would you like to learn about?"
---

The user has asked you to teach them something. This is a stateful request — they intend to learn the topic over multiple sessions. (Adapted from Matt Pocock's `teach` skill, with a knowledge layer based on Karpathy's LLM-wiki pattern.)

## Workspace resolution

Resolve the state home before treating the current directory as a teaching workspace.
A valid host marker makes writes resolve inside the existing `.bc-agent` vault, so unrelated
project source code at the project root is not a reason to create root teach files or to block
hosted use. Without a valid marker, **guard first:** if the selected directory contains content
that is clearly not a teaching workspace (source code, a git repo with unrelated files), ask the
user before creating files there — suggest a dedicated directory per topic instead. One mission
per workspace.

### Hosted .bc-agent adapter

Before reading or writing any teaching state, resolve `<teach-root>`:

1. From the current directory, first check for standalone state (`MISSION.md`, `REVIEW.md`,
   `GLOSSARY.md`, `RESOURCES.md`, `NOTES.md`, `learning-records/`, or `lessons/`).
   If any is present, do not select an ancestor host automatically: preserve this standalone
   home and report any marker as a competing home. Otherwise inspect the nearest ancestor
   containing the explicit marker `.bc-agent/references/teach-skill.md`. If the current
   directory is the `.bc-agent` vault, the marker is `references/teach-skill.md`. Read that
   marker before using host paths. A valid marker begins `<!-- teach-host-adapter: v1 -->`;
   it is the opt-in adapter for an existing initializer host, not an instruction to run
   `bc-init-agent`.
2. With a valid marker, use the marked `.bc-agent` directory as `<teach-root>` — this is
   `.bc-agent` when invoked from the project root and the current vault when invoked from
   vault context. Resolve every mapped path below relative to `<teach-root>`.
3. Without a valid marker, use the current directory as `<teach-root>` and keep the
   standalone paths below authoritative. Do not treat an arbitrary `.bc-agent` directory
   as a host and do not auto-run initialization.
4. If standalone teach state and a valid host marker compete, stop before writing, name both
   homes to the user, and ask which one to use. The standalone layout is preserved and wins
   by default; never migrate, copy, or silently displace it. An incomplete marker is not a
   host contract: report the missing adapter and remain standalone until the user explicitly
   chooses and repairs the host.

The host's schema and orientation remain owned by `bc-init-agent`; `teach` owns the mapped
pedagogy, evidence, glossary content, source/knowledge content, and spaced-repetition state.
The marker is intentionally a thin path adapter, not a generic config framework or copied
teach body.

### Hosted path map

With a valid adapter, these logical teach surfaces use the existing host paths:

| Teach surface | Hosted path, relative to `<teach-root>` |
|---|---|
| Mission | `learning/plan.md` (no separate hosted `MISSION.md`) |
| Review queue | `learning/review.md` |
| Learning records | `learning/records/` |
| Lessons and session artifacts | existing `sessions/` (never `learning/sessions/`) |
| Notes | `learning/notes.md` |
| Raw sources | existing `sources/` |
| Compiled knowledge / wiki concepts | existing `concepts/` |
| Resource catalog | `references/teach-resources.md` |
| Glossary | existing Glossary section of `project/overview.md` |
| Catalog and history | shared `index.md` and `log.md` |

Do not create duplicate root `MISSION.md`, `REVIEW.md`, `GLOSSARY.md`, `RESOURCES.md`, or
`NOTES.md` files in a hosted workspace. Do not create `learning/sessions/`; lessons and
session artifacts use the existing `sessions/` directory. The host `index.md` and `log.md`
are shared catalog/history surfaces and must receive teach entries without replacing host
orientation or unrelated project history.

### Standalone path map

Without the adapter, the workspace has three layers plus pedagogy state. These paths and
formats remain unchanged:

**Raw sources (immutable — you read, never modify):**
- `./sources/*` — ingested source material: clipped articles, papers, transcripts. The ground truth that wiki claims cite.
- `RESOURCES.md` — the annotated, vetted catalog of sources and communities. Format: [RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md).

**The wiki (you write and maintain it entirely):**
- `./wiki/*.md` — interlinked markdown concept pages: the compiled, compounding knowledge of this workspace. Format: [WIKI-FORMAT.md](./WIKI-FORMAT.md).
- `GLOSSARY.md` — the canonical terminology, at the root, nowhere else. Format: [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).
- `index.md` — catalog of every page in the workspace: one line each with link and summary, grouped by category. Updated on every write.
- `log.md` — append-only session log. Entries start `## [YYYY-MM-DD] <type> | <title>` where type is `lesson`, `ingest`, `review`, or `lint` — greppable with `grep "^## \[" log.md | tail -5`.

**Pedagogy state:**
- `MISSION.md` — the _reason_ the user is learning this. Grounds every teaching decision. Format: [MISSION-FORMAT.md](./MISSION-FORMAT.md).
- `REVIEW.md` — the spaced-repetition queue. Format: [REVIEW-FORMAT.md](./REVIEW-FORMAT.md).
- `./learning-records/*.md` — ADR-style records of demonstrated understanding, numbered `0001-<dash-case-name>.md`. These drive the zone of proximal development. Format: [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md).
- `./lessons/*.html` — review artifacts produced after a lesson is taught, numbered `0001-<dash-case-name>.html`.
- `NOTES.md` — your scratchpad for user preferences and working notes.

Create directories lazily, only when first written to, in whichever path home the adapter resolves.

## Session Ritual

Every session starts the same way, before any new material:

1. Read the resolved mission, notes, `index.md`, and the last few `log.md` entries under
   `<teach-root>`. In hosted mode these are `learning/plan.md`, `learning/notes.md`, and
   the shared host catalog/history. Open knowledge pages and learning records only as the
   index points you to them — do not skim everything.
2. **Review first.** Run `python3 <this skill's directory>/scripts/due.py <resolved review queue>`
   — in hosted mode the queue is `learning/review.md`; standalone remains `REVIEW.md`. It
   does the date math and prints what's due with next-interval suggestions. Quiz the user on
   up to 3 due items (free recall, in conversation), then update the resolved review queue
   with the dates the script suggested. **Ask only one question per message and wait for the
   learner's answer before asking the next**; batching questions increases working-memory
   load and weakens the feedback loop. If the user fails an item, that may be today's lesson.
3. Only then proceed — to a lesson, an ingest, or a lint, whichever the session calls for.
4. Before the session ends, append a teach entry to the resolved `log.md` and update the
   resolved `index.md` if pages changed; preserve unrelated host history and orientation.

If the resolved mission is missing or vague, your first and only job is to interview the user
about why they want to learn this. Push back on vagueness — "ship a Rust CLI to my team" beats
"learn Rust." A bad mission is worse than no mission.

## Gates

These gates exist because their failure modes are in-the-moment rationalization — the moment a gate is inconvenient is the moment your judgment about it is least reliable, so the predictable temptations are pre-refuted below. They bind the impulse of the moment, not your considered judgment: if you conclude a gate itself is wrong for this user or this topic, say so to the user and propose changing this skill, but keep following the current gate for this session unless the user explicitly approves changing course. Openly evolving the rule is legitimate; quietly skipping it never is.

**Review-first gate.** No new material until due review items are quizzed and the resolved review queue is updated (`REVIEW.md` standalone, `learning/review.md` hosted). Not valid excuses: "the user seems eager to start" (review takes two minutes; eagerness survives it), "the user is short on time" (then review IS the session — it's the highest-value two minutes available), "the user asked for a specific topic" (review first, then teach it), "they clearly remember this" (that feeling is fluency, not storage — the whole point is testing it). A skipped review silently kills the queue, and the queue is what makes this skill work across sessions. If the user explicitly refuses review after you've quizzed once, note it in the resolved notes file and move on — respect beats nagging.

**Evidence gate.** No `demonstrated` learning record without demonstrated understanding. Not valid excuses: "they said they know it" (spot-check with one question first), "their answer was mostly right" (probe the wrong part — that's where the misconception lives), "I explained it clearly so they must have it" (coverage is not learning), "crediting them keeps the session positive" (an over-credited record makes every future lesson land above their head — generosity now is cruelty later). Self-reported prior knowledge may be recorded only as `Status: self-reported`, with an explicit note that future sessions must spot-check before relying on it.

**Citation gate.** No durable factual claim in a wiki page or lesson artifact without a source behind it. Conversational explanations should be grounded in the wiki or vetted sources; durable pages need explicit citations. Not a valid excuse: "this is common knowledge" — if it's truly common, a source takes thirty seconds to find; if you can't find one, it was a parametric guess.

## Philosophy

Deep learning needs three things:

- **Knowledge** — compiled once from vetted sources into the wiki, then kept current. Never trust your parametric knowledge for factual claims; cite wiki pages, which cite sources.
- **Skills** — built through effortful retrieval with tight feedback loops.
- **Wisdom** — from real practitioners. Delegate to communities (see RESOURCES-FORMAT.md); respect it if the user opts out.

Distinguish **fluency strength** (in-the-moment retrieval, feels like mastery, isn't) from **storage strength** (long-term retention, the real goal). Build storage strength with desirable difficulty: retrieval practice, spacing (via the resolved review queue), and interleaving related skills.

For *acquiring* knowledge, difficulty is the enemy — it eats working memory. For *practicing* skills, difficulty is the tool. Keep explanations easy and practice hard.

## Operations

### Lessons (the default)

The primary unit of teaching is an **in-conversation lesson**, not a generated file. The agent grading free-form answers in real time is a tighter feedback loop than any static quiz. A lesson:

1. Teaches one tightly-scoped thing tied to the mission, sized to a single tangible win, inside the user's zone of proximal development.
2. Draws its knowledge from the wiki (ingesting a source first if the wiki doesn't cover it), presenting the minimum needed, with citations.
3. Drives practice through **free recall**: ask the user to explain, predict, or produce — then give immediate, specific feedback. Ask **one question per message**, wait for the answer, give feedback, and only then ask the next question; never present a batch of numbered questions. Prefer open questions over multiple choice; recognition is not recall. If you do use multiple choice, distractors must be *plausible misconceptions*, not length-matched filler.
4. For physical/real-world skills (yoga, cooking, lifting), walk the user through the steps and have them self-report against concrete checkpoints.
5. Names one primary source — the single best resource to read or watch next.

**Afterwards**, write the lesson artifact to the resolved lesson/session directory as a clean,
readable HTML page (think Tufte) summarizing what was taught, linking to the relevant knowledge
pages and the primary source. Use `./lessons/` standalone and the existing `sessions/` directory
hosted; never create `learning/sessions/`. If the artifact contains any interactive element,
**verify it works before delivering it** — open it and test the interaction, or keep it static.
To open files for the user, detect the platform: `open` (macOS), `xdg-open` (Linux).

Then update state: fold durable knowledge into the resolved knowledge directory, add an item to
the resolved review queue (`REVIEW.md` standalone or `learning/review.md` hosted), write a
learning record only if the evidence bar was met, and append the session to the resolved `log.md`.

### Ingest

When the user brings a source (or you find one filling a gap in the resolved resource catalog):
vet it per the protocol in RESOURCES-FORMAT.md, save the material to the resolved raw-source
directory (`./sources/` in both modes), read it, and **discuss the key takeaways with the user**
— ingestion is itself teaching. Then write a source summary and affected concept pages in the
resolved knowledge directory (`./wiki/` standalone or `./concepts/` hosted), flag contradictions
with existing claims rather than silently overwriting, update the resolved resource catalog and
shared/standalone `index.md`, and log it. One source may touch many pages — that maintenance is
your job, not the user's.

### File answers back

When the user asks a question mid-session and the answer required real synthesis — a comparison,
a connection across pages, an analysis — file it into the resolved knowledge directory as a page
(`./wiki/` standalone or `./concepts/` hosted) instead of letting it evaporate into chat history.
Explorations should compound like everything else.

### Lint

Periodically (a reasonable default: every ~5 sessions, or when the user asks), health-check the workspace:

- Contradictions between knowledge pages, or between knowledge and the resolved glossary
  (`GLOSSARY.md` standalone; the Glossary section of `project/overview.md` hosted).
- Claims superseded by newer sources — and learning records that need `Status: superseded` as a result.
- Orphan knowledge pages with no inbound links; concepts mentioned often but lacking a page.
- Stale review-queue items and dead links in the resolved resource catalog.
- Gaps the mission needs that no source covers — append to that catalog's `## Gaps`.

Report findings to the user, fix the mechanical ones, and log the pass.

## Zone of Proximal Development

Each lesson should feel "challenged just enough." If the user names what they want to learn, teach that. Otherwise, derive the next step from learning records + mission. Hold a high evidence bar: a half-right answer is not demonstrated understanding — probe with a follow-up before crediting it. Be especially suspicious of your own inclination to be generous; sycophantic grading corrupts every future session's difficulty calibration.

## Mission Drift

Missions change as understanding deepens — this is normal and good signal. Confirm with the user,
update the resolved mission (`MISSION.md` standalone; `learning/plan.md` hosted), and write a
learning record capturing why it shifted.

## Notes

Record how the user likes to be taught (pace, depth, format preferences, opt-outs) in the resolved
notes file (`NOTES.md` standalone; `learning/notes.md` hosted) so future sessions don't re-learn it.
