---
test_kind: pressure
test_status: not-run
tested: never
deployed: 2026-06-21
---
# Concept: frontend-design

Model-invoked taste + discipline skill for building or reshaping web UI where visual quality matters. Drives distinctive art direction and disciplined restraint so generated UI doesn't collapse into the recognizable "AI design" attractors. Inverts to "conform to it" the moment an established design system exists.

## What it is

A lean spine (`body/SKILL.md`) — studio-design-lead voice, the thesis→plan→critique→build→critique process, the core defaults *with their reasons*, the modern-platform and verification hooks — plus a JIT-loaded checklist layer (`body/archetypes.md`) carrying the concrete per-surface rules (landing / app-dashboard / imagery / motion / copy), hard rules, reject-these-failures, and litmus checks. Progressive disclosure keeps the entry file small; the long checklist loads only when actually building.

## Design decisions

- **Fusion, not a copy.** The spine and process come from Anthropic's `frontend-design` (subject-grounding, token-plan with a *signature* element, critique-against-defaults, restraint/self-critique, copy-as-design-material). The concrete checklist layer comes from OpenAI's `frontend-skill` (Working Model, archetype playbooks, hard rules, litmus checks). They are complementary: Anthropic gives the principled spine + anti-cliché critique; OpenAI gives the exhaustive concrete rules + per-surface guidance. Neither alone was as strong as the fusion.
- **Right altitude.** Frontend slop is a *predictable* failure mode, so concrete prescriptive rules are justified (per `prompting-agents`: reach for prescriptive blocks where the failure mode is in-the-moment regression to defaults) — but every rule is framed as a default-with-reason that the brief or an existing design system overrides. This keeps it from becoming brittle if-else process.
- **Single aesthetic concept; Google is a pointer, not content.** Google's Modern Web Guidance is a *different axis* — platform correctness / Baseline-gating, not art direction. Folding its 81 feature guides in would dilute both, and upstream ships a CLI + weekly updates. The skill therefore carries a short "prefer modern Baseline-safe features; defer to Modern Web Guidance if installed" note and cites the raw snapshot. (User decision, 2026-06-21.)
- **Material Design 3 deliberately excluded.** MD3 is one opinionated design *system* — i.e. exactly the kind of templated default look the skill warns against defaulting to. It belongs as an optional invoked direction, not the baseline. (User decision, 2026-06-21.)
- **Stack-agnostic.** Both sources assume React/Tailwind(/Framer Motion/shadcn); the body states the principles framework-independently and tells the agent to translate to the project's actual stack and conform to repo conventions. (User decision, 2026-06-21.)
- **Composes existing skills for verification** rather than re-teaching it: `playwright-cli` for cross-viewport screenshots, `verify` for confirming the running app. (User decision, 2026-06-21.) Keeps the body lean and avoids duplicating the screenshot loop.
- **Relationship to `prompting-agents` "Frontend anti-slop" block.** That block is the agnostic one-paragraph version inside the instruction library; this concept is its deep expansion. The block stays as the quick-reference; this is what an agent loads when actually designing.

## Provenance

- [anthropic-frontend-design-skill.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) — Anthropic's official `frontend-design` SKILL.md (verbatim). Source of the spine, process, anti-cliché list, copy-as-design-material, restraint/self-critique.
- [openai-gpt-5-4-frontend-design.md](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4) — OpenAI's "Designing delightful frontends with GPT-5.4" blog embedding their official Codex `frontend-skill` verbatim. Source of the archetype checklist layer, hard rules, litmus checks, viewport budget, utility-copy guidance, mood-board workflow.
- [openai-gpt-5-frontend-cookbook.md](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_frontend) — OpenAI GPT-5 frontend cookbook. Minor: starter-stack + steerability/multimodal notes.
- [GoogleChrome/modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src) — Chrome DevRel Modern Web Guidance (design/UX subset, commit eec2f8e). Cited as the modern-platform pointer; not vendored into the body.
- `concepts/prompting-agents/body/SKILL.md` — altitude principles + the "Frontend anti-slop" block this concept deepens; instruction phrasings adapted from its blocks.

## Tests

`tests/scenario.md` — pressure scenarios: (1) blank brief, time pressure → must still ground in subject, write a thesis/token plan, and avoid the named attractors rather than shipping a default; (2) existing design system present → must invert and conform, not impose its own art direction; (3) dashboard brief → must use utility copy and not bolt on a marketing hero; (4) "just make it look good fast" → must still verify against the render via playwright-cli, not self-report. Scenarios authored; full harness run pending.

## Deploy targets

- Claude Code: `~/.claude/skills/frontend-design` → relative symlink to `body/` (deployed 2026-06-21).
- Pi: `~/.agents/skills/frontend-design` and `~/.pi/agent/skills/frontend-design` → relative symlinks to `body/` (deployed 2026-06-21).
- Other harnesses: manual bootstrap until tested.
