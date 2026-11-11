---
test_kind: pressure
test_status: not-run
tested: never
deployed: no
---
# Concept: ui-design

## What it is

A cross-surface UI design skill for any visible change, from a single control to a redesign. It starts with task and input needs, established systems and ranked principles, then scales visual critique and capture to the work. Its lean entry points to principles, new work, existing apps and surface-specific capture recipes.

## Design decisions (2026-11-11)

- Replace the previous web-focused concept without an alias. Trigger on any visible user-interface change, not pure explanation diagrams or invisible changes; effort scales with scope.
- Keep one principles-first skill with progressive disclosure. Separate evidence-backed standards from conventions; apply platform metrics only to their domain.
- New work gets a subject-grounded thesis, tokens and anti-attractor critique; landing pages are one case, not the default. Existing applications conform to their theme, components and container behavior, including structured data and states.
- A capture and written per-image checklist critique gate every visible change; small changes need one post-change capture, redesigns and “looks bad” complaints need baseline plus two rounds. Preserve rounds, inspect originals and 1:1 crops, and report unavailable capture as visually unverified.
- Capture in the actual host when it controls sizing. Screenshots cannot prove behavior, keyboard, focus or semantics; check those separately. Model scores are not acceptance criteria.
- Capture recipes are tool-agnostic, not dependent on unavailable skills. Modern Web Guidance remains a web-only pointer; Material Design is an optional system, not a universal default. Stack and harness remain neutral.
- A dedicated designer may work presentation-only, report behavioral bugs, and hand captures to the orchestrator; redesign review is independent and blind to designer reasoning, with located defects rather than scores.
- The rewrite has not passed pressure testing and is held from deployment. Scenarios compare runs without and with the skill on the configured pressure model; previous results do not establish this new contract.
- The prompting-agents quick-reference block remains a concise companion; show-me hands product UI work here, while explanation diagrams stay with show-me.

## Provenance

- [Anthropic design skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) — subject grounding, thesis and anti-cliché critique.
- [OpenAI design guidance](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4) — archetypes, imagery, utility copy and visual checks.
- [OpenAI frontend cookbook](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_frontend) — stack and multimodal context.
- [Modern Web Guidance](https://github.com/GoogleChrome/modern-web-guidance-src) — web platform pointer.
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [Nielsen's heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), [Norman on signifiers](https://jnd.org/signifiers-not-affordances/), [Fluent layout](https://fluent2.microsoft.design/layout) — accessibility, usability and perceptual principles; individual checks cite their sources.
- [WebGen-Agent](https://arxiv.org/html/2509.22644), [MLLM as UI Judge](https://arxiv.org/html/2510.08783), [ArtifactsBench](https://arxiv.org/html/2507.04952) — visual feedback and judge limitations, not proof of any universal score threshold.
- [Shelfmark brief](../../docs/research/front-end-design/brief.md), [visual hill-climb handoff](../../docs/research/front-end-design/theo-ui-hill-climb-handoff.md) — concrete failure modes and capture-loop evidence.
- [prompting-agents](../prompting-agents/body/SKILL.md) — instruction altitude and anti-slop block.

## Tests

[Pressure scenarios](tests/scenario.md) cover the new contract; no run has been performed for this rewrite.

## Deploy targets

When pressure-tested and approved: relative symlinks for the shared bus `~/.agents/skills/ui-design`, Pi `~/.pi/agent/skills/ui-design`, and Claude Code `~/.claude/skills/ui-design`. Not deployed; bulk deployment holds this concept.
