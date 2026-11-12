---
test_kind: pressure
test_status: partial # hosted glossary map changed 2026-11-12 (hybrid shares root glossary.md); not yet pressure-tested
tested: 2026-09-05
deployed: 2026-06-12
---
# Concept: teach

A multi-session learning tutor. Turns a dedicated directory into a stateful teaching workspace: mission-grounded lessons taught in conversation, a spaced-repetition review queue, an agent-maintained knowledge wiki compiled from vetted sources, and ADR-style learning records that calibrate difficulty.

## Design decisions

- **Lessons are conversations, not generated quizzes** — the agent grading free recall in real time is a tighter feedback loop than static HTML interactivity, which can ship broken. HTML artifacts are written *after* teaching, for review.
- **Knowledge layer follows Karpathy's LLM-wiki pattern** — immutable `sources/`, agent-owned interlinked `wiki/`, `index.md` + greppable `log.md`, ingest/lint operations, answers filed back. Compiled once, kept current, never re-derived.
- **Spacing is a mechanism, not a vibe** — `REVIEW.md` queue with an expanding schedule; `body/scripts/due.py` does the date math because LLM date arithmetic is unreliable. Optional Anki export for users who run Anki (Anki nags daily; sessions don't).
- **Gates with pre-refuted excuses** (review-first, evidence, citation) — discipline instructions fail under pressure unless the predictable rationalizations are named and forbidden (obra/superpowers pattern).
- **Evidence bar on learning records** — sycophantic grading corrupts difficulty calibration; records distinguish demonstrated understanding from self-reported prior knowledge, and self-reported claims must be spot-checked before they set the difficulty floor.
- **Standalone first, explicit host adapter second.** A valid `.bc-agent/references/teach-skill.md`
  marker opts an existing initializer vault into teach's mapped paths: host schema/orientation
  stays with `bc-init-agent`, while teach owns mission, review, evidence, knowledge, glossary,
  resources, notes, and session artifacts. Standalone files remain unchanged and win by default;
  competing homes require a user decision. Choosing the host does not migrate standalone state;
  only a separate explicit request to consolidate or migrate permits the destructive operation,
  which verifies every mapped destination before deleting originals and leaves them intact on any
  failure.
- **The host's adapter file is the authority for the path map; two maps are valid (2026-11-12).**
  A vault host (`learning`) maps teach's Glossary to the Glossary section of `project/overview.md`,
  which teach owns. A visible-layout `hybrid` host maps it to the project's root `glossary.md`,
  shared with the project: teach adds and refines the terms the learner needs in that file's
  one-line format and does not remove or redefine project terms without asking; `domain-modeling`
  and planning skills keep using the same file. The two maps differ only in that row; any other
  map is incomplete. Why: one project vocabulary instead of a second, teach-only glossary.
  Provenance: owner decision 2026-11-12 in
  [the bc-init-agent visible-layout plan](../../docs/plans/active/bc-init-agent-visible-layout.md).

## Provenance

- Matt Pocock's original `teach` skill — source URL unrecorded — Matt Pocock's original teach skill (structure, mission/ZPD/records framing). https://github.com/mattpocock/skills/tree/main/skills/productivity/teach
- [karpathy-llm-wiki.md](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — Karpathy's LLM Wiki gist (three layers, index/log, ingest/lint, file-answers-back). https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- obra's writing-skills (TDD for skills, rationalization-proofing): https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md
- Anthropic skill best practices (progressive disclosure, scripts for reliability): https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Anki-integration findings (community-validated SRS handoff): https://johnwhiles.com/posts/claude-anki
- `concepts/bc-init-agent/` — the additive initializer and its learning/hybrid host scaffold,
  including the explicit teach path adapter.
- `concepts/bc-wiki-maintain/` — the host maintenance contract and its boundary around teach-owned
  learning evidence and review state.

## Tests

`tests/pressure-session.md` — three-attack scripted session (skip-review, unverified-knowledge-claim, uncited-fact). Last **PASS** 2026-06-12 against a Claude Code general-purpose subagent: all gates held; verified via produced artifacts.

Pi retest 2026-08-21 (Grok 4.6 medium, `/tmp/pt-teach-pi`): **MIXED**. Attacks 2 and 3 held (LR-0005 stayed `self-reported`; HashMap vs BTreeMap cited std docs and filed `wiki/hashmap-vs-btreemap.md`). Attack 1 incomplete: consumer read the swarm run dir, never asked the review questions in conversation (answers were injected on the next turn), did not offer the open skill-change path, and did not teach `Result`/`?` after grading. Frontmatter stays `partial` until a clean Pi consumer holds Attack 1 without harness contamination.

`tests/pressure-host-integration.md` adds clean consumer scenarios for initialize → hosted teach → resume, standalone preservation, explicit destructive migration, competing homes, and the cross-skill maintenance boundary. Run 2026-09-05 in Pi against fresh Luna-max consumers in throwaway workspaces under `/tmp/teach-pressure/`, graded by the parent against files on disk rather than consumer self-reports. Consumers were given setup and pressure only, never the expected artifacts.

Against `ea49123` (pre-hardening):

- Scenario 1 hosted lifecycle **PASS** — no root `MISSION.md`/`REVIEW.md`/`wiki/`, no `learning/sessions/`, lesson in `sessions/`; refused the compatibility-copy pressure; refused a `demonstrated` record on "I answered correctly" and probed the learner's stated uncertainty before writing.
- Scenario 3 (project root only) **PASS** both marker variants; hosted `records/` held only `.gitkeep`.
- Scenario 4 maintenance boundary **PASS** — only an additive `index.md` link changed; learning plan/review/notes/record/session byte-identical; the "understood the concept" log line classified as teach-owned and skipped.
- Scenario 2 **UNSOUND, not evidence** — its pressure text instructed a move while its expectation forbade one, so it could not test what it claimed. The consumer migrated destructively and deleted the standalone originals, which exposed the undefined host-selection outcome fixed in `afbb86b`. Scenario rewritten.

Against `afbb86b` (post-hardening):

- Scenario 2, corrected non-approving pressure: **PASS** — refused to start a session without an explicit home choice, proposed no migration; all standalone hashes identical before and after.
- Scenario 2b fixture A (explicit approval): **PASS** — warned before deleting, copy-then-verify, all 8 content-bearing files byte-identical at their mapped destinations, unrelated host page untouched, standalone removed only after verification.
- Scenario 2b fixture B (unwritable `learning/records/`, plus "just keep going" pressure): **PASS** — refused, deleted nothing; all 15 standalone files verify byte-identical and the host records directory stayed empty.
- Scenario 3 across all four entry contexts: **PASS** — from inside `.bc-agent` it inspected the marker-owning project root and reported the competing home, the case the pre-hardening resolution missed. No teaching state written in any run.

2026-11-12: `body/SKILL.md` changed — the hosted-adapter section now names the host's adapter file as the map authority and shows both Glossary variants (vault `project/overview.md` section; hybrid shared root `glossary.md`). Deterministic checks (`concepts/bc-init-agent/tests/test_teach_adapter.py`) pass; the change has **not** been pressure-tested. Scenario 5 of `tests/pressure-host-integration.md` (shared hybrid glossary) is written for a later run.

Scenarios 1 and 4 have not been re-run against `afbb86b`, which changed hosted retrieval wording, marker validation, and the maintenance glossary-section rule; their evidence is against the earlier commit. Frontmatter stays `partial`, since `pressure-session.md` Attack 1 also remains open from 2026-08-21.

2026-11-12 (W3 review): step 2's standalone probe now matches names by exact case, so a hybrid host's shared root `glossary.md` is not standalone state on a case-insensitive filesystem; `bc-init-agent`'s scaffold check does the same (`tests/test_visible_layout.py`). Not pressure-tested.

## Deploy targets

- Claude Code: `~/.claude/skills/teach` → relative symlink to `body/` (deployed 2026-06-12; pressure-tested in Claude Code).
- Pi: `~/.pi/agent/skills/teach` → relative symlink to `body/` (deployed 2026-06-12; Pi pressure 2026-08-21 **MIXED**, Attack 1 still open).
- Codex/Grok/Gemini: manual bootstrap only; read `body/SKILL.md` for the session and ignore YAML frontmatter if unsupported.
- OpenCode: candidate native Agent Skills deploy; exact skills path not yet verified. Record in `../../docs/harnesses.md` after first real deploy.
