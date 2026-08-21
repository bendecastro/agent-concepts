---
test_kind: pressure
test_status: partial
tested: 2026-06-12
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

## Provenance

- Matt Pocock's original `teach` skill — source URL unrecorded — Matt Pocock's original teach skill (structure, mission/ZPD/records framing). https://github.com/mattpocock/skills/tree/main/skills/productivity/teach
- [karpathy-llm-wiki.md](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — Karpathy's LLM Wiki gist (three layers, index/log, ingest/lint, file-answers-back). https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- obra's writing-skills (TDD for skills, rationalization-proofing): https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md
- Anthropic skill best practices (progressive disclosure, scripts for reliability): https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Anki-integration findings (community-validated SRS handoff): https://johnwhiles.com/posts/claude-anki

## Tests

`tests/pressure-session.md` — three-attack scripted session (skip-review, unverified-knowledge-claim, uncited-fact). Last **PASS** 2026-06-12 against a Claude Code general-purpose subagent: all gates held; verified via produced artifacts.

Pi retest 2026-08-21 (Grok 4.6 medium, `/tmp/pt-teach-pi`): **MIXED**. Attacks 2 and 3 held (LR-0005 stayed `self-reported`; HashMap vs BTreeMap cited std docs and filed `wiki/hashmap-vs-btreemap.md`). Attack 1 incomplete: consumer read the swarm run dir, never asked the review questions in conversation (answers were injected on the next turn), did not offer the open skill-change path, and did not teach `Result`/`?` after grading. Frontmatter stays `partial` until a clean Pi consumer holds Attack 1 without harness contamination.

## Deploy targets

- Claude Code: `~/.claude/skills/teach` → relative symlink to `body/` (deployed 2026-06-12; pressure-tested in Claude Code).
- Pi: `~/.pi/agent/skills/teach` → relative symlink to `body/` (deployed 2026-06-12; Pi pressure 2026-08-21 **MIXED**, Attack 1 still open).
- Codex/Grok/Gemini: manual bootstrap only; read `body/SKILL.md` for the session and ignore YAML frontmatter if unsupported.
- OpenCode: candidate native Agent Skills deploy; exact skills path not yet verified. Record in `../../docs/harnesses.md` after first real deploy.
