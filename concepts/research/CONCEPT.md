---
test_kind: pressure
test_status: not-run
tested: never
deployed: yes
---
# Concept: research

Model-invoked evidence discipline for technical questions that need more than a quick lookup. It uses primary sources, keeps substantial reading in a background agent, and returns cited findings. Repository notes are deliberate artifacts, not an automatic side effect of asking a question.

## Design decisions

- **Primary-source first.** Official documentation, specifications, source code, first-party APIs, and maintainer statements own technical claims; secondary write-ups may guide discovery but do not establish facts when a primary source exists.
- **Background only when it earns its cost.** Multi-source investigation runs independently so the foreground session can proceed; narrow factual checks stay inline.
- **Durability is opt-in.** A one-off answer stays in chat. A cited note is written only at the user's request, when a project rule requires it, or when the result directly supports a durable decision/PRD/plan.
- **Evidence stays distinct from planning.** Research can inform a PRD or ADR but is neither by itself; the resulting decision is captured through the appropriate planning/domain workflow.

## Provenance

- Matt Pocock upstream `skills/engineering/research/SKILL.md` at `391a2701dd948f94f56a39f753f8eea9a859c87` — background-agent, primary-source, cited-Markdown research spine. https://github.com/mattpocock/skills/blob/391a2701dd948f94f56a39f753f8eea9a859c87/skills/engineering/research/SKILL.md
- `concepts/prompting-agents/body/SKILL.md` — context-economy, source-grounding, and output-shape guidance.

## Tests

`tests/scenario.md` — verifies primary-source sourcing, inline handling for a narrow lookup, background delegation for a substantial investigation, and no unrequested repository note. Discipline-enforcing; pressure-test before deploy.

## Deploy targets

Deployed to the shared bus, Pi, and Claude Code by `scripts/deploy-local-skills.py`, which deploys every concept carrying a `body/SKILL.md`. This shipped with that bulk deploy rather than by a per-concept decision, so the intended deploy-after-test sequence did not hold here. Current state is in this file's frontmatter; `python3 scripts/lint.py` fails while a deployed concept is untested.
