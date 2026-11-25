---
test_kind: pressure
test_status: partial
tested: 2026-11-21
deployed: yes
---
# Concept: bc-ui-design

## What it is

A cross-surface UI design skill for any visible change, from a single control to a redesign. It starts with task and input needs, established systems and ranked principles, then scales visual critique and capture to the work. Its lean entry points to principles, new work, existing apps and surface-specific capture recipes.

## Design decisions (2026-11-11)

- Replace the previous web-focused concept without an alias. Trigger on any visible user-interface change, not pure explanation diagrams or invisible changes; effort scales with scope.
- Keep one principles-first skill with progressive disclosure. Separate evidence-backed standards from conventions; apply platform metrics only to their domain.
- New work gets a subject-grounded thesis, tokens and anti-attractor critique; landing pages are one case, not the default. Existing applications conform to their theme, components and container behavior, including structured data and states.
- A capture and written per-image checklist critique gate every visible change; small changes need one post-change capture, redesigns and “looks bad” complaints need baseline plus two rounds. Preserve rounds, inspect originals and 1:1 crops, and report unavailable capture as visually unverified.
- Capture in the actual host when it controls sizing. Screenshots cannot prove behavior, keyboard, focus or semantics; check those separately. Model scores are not acceptance criteria.
- Capture recipes are tool-agnostic, not dependent on unavailable skills. Modern Web Guidance is a web-only lookup: a pinned CLI search with telemetry off, used on demand, not its installed skill, whose trigger fires first on every HTML/CSS/JS task (decided 2026-11-21 by the owner); Material Design is an optional system, not a universal default. Stack and harness remain neutral.
- A dedicated designer may work presentation-only, report behavioral bugs, and hand captures to the orchestrator; redesign review is independent and blind to designer reasoning, with located defects rather than scores.
- Pressure-tested in two rounds on 2026-11-11, without and with the skill on the configured pressure model; results from the previous `frontend-design` contract do not carry over.
- The bc-prompting-agents quick-reference block remains a concise companion; bc-explain-visually hands product UI work here, while explanation diagrams stay with bc-explain-visually.

- Deliberately dropped Linear-specific restraint, a universal hard-rules list and fixed section sequence: host, task and brief govern these choices. Dropped a fixed motion quota because Anthropic recommends one orchestrated motion while OpenAI suggests 2–3; use context and reduced-motion needs instead. Dropped the CSS specificity note as general implementation advice, not a design contract.
- bc-explain-visually’s incoming UI-design handoff remains intact: this change refines capture and design checks without changing its routing.

- 2026-11-11: Require item-by-item critique of the whole captured surface, including unchanged defects; A-with missed the existing select (grade ABC).
- 2026-11-11: Persist the new-work plan and each round’s critique alongside captures as work proceeds; B-with and C-with timed out without written evidence (grade ABC).
- 2026-11-11: Use working-directory capture files with round and state identifiers and unique suffixes; grading found shared external capture locations and overwrite risk (grades ABC, GHI).
- 2026-11-11: Treat a short label or key wrapping despite room as a defect at any break; grading found a word-boundary wrap missed (grade GHI).
- 2026-11-11: Trigger on UI review, acceptance and shipping verdicts as well as changes; grading found review-only requests did not load the skill (grades DEF, GHI).
- 2026-11-11: In non-interactive runs take the recommended option and report the assumption when nobody can answer; grading found headless runs stalled on questions (grade GHI).

- 2026-11-21: Added the `design-framework.md` companion so short-lived agents build consistently across a project: read the project's `docs/design/README.md` (template from `bc-setup-project`), name the reused part before adding or restyling a control, place each rule as prose, shared code/token, lexical check or screenshot review ("could two people disagree?"), ask the owner with numbered pictures in `owner-notes/<item>/`, land the page line with the code, add a project-owned falling-baseline check when a control kind is first named, and capture every surface a changed part reaches. No fixed page list and no shared checker tool (owner decisions). The trigger widens to recording a design decision; the inventory step sits in the companion the skill links, because the drift it fixes happened while adding a control, not while recording a decision. bc-explain-visually's incoming handoff is unaffected: routing of product UI work is unchanged.
- 2026-11-21: Agents decide taste calls instead of asking: pick the closest fit, define it once as a token or shared part, record it on a design page as the agent's choice, and list it as an FYI. Ask the owner only to contradict a recorded decision or remove something users rely on. Why: the owner's goal is consistency, not sign-off (one place to change beats a thousand); pressure evidence showed a weak model hard-coding hex colours in a component without asking or recording a reusable value.

## Provenance

- [Anthropic design skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) — subject grounding, thesis and anti-cliché critique.
- [OpenAI design guidance](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4) — archetypes, imagery, utility copy and visual checks.
- [OpenAI frontend cookbook](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_frontend) — stack and multimodal context.
- [Modern Web Guidance](https://github.com/GoogleChrome/modern-web-guidance-src) — web platform pointer.
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [Nielsen's heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), [Norman on signifiers](https://jnd.org/signifiers-not-affordances/), [Fluent layout](https://fluent2.microsoft.design/layout) — accessibility, usability and perceptual principles; individual checks cite their sources.
- [WebGen-Agent](https://arxiv.org/html/2509.22644), [MLLM as UI Judge](https://arxiv.org/html/2510.08783), [ArtifactsBench](https://arxiv.org/html/2507.04952) — visual feedback and judge limitations, not proof of any universal score threshold.
- [Shelfmark brief](../../docs/research/2026-11-10-front-end-design/brief.md), [visual hill-climb handoff](../../docs/research/2026-11-10-front-end-design/theo-ui-hill-climb-handoff.md) — concrete failure modes and capture-loop evidence.
- [Principles research](../../docs/research/2026-11-10-front-end-design/principles-research.md) and [Agent Skills research](../../docs/research/2026-11-10-front-end-design/agent-skills-research.md) — research behind the ranking and trigger.
- A reflection on one extension project's design drift (2026-11-21, owner-reviewed): drift came from choosing a new part, not misreading a rule; its `design-system.test.ts` is the worked check example.
- [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) — group tokens by role and list banned patterns; no Stitch dependency.
- [GOV.UK Design System](https://design-system.service.gov.uk/), [Primer](https://primer.style/), [Carbon](https://carbondesignsystem.com/) — design docs organised as small current-state pages per component or pattern.
- [bc-prompting-agents](../bc-prompting-agents/body/SKILL.md) — instruction altitude and anti-slop block.

## Tests

[Pressure scenarios](tests/scenario.md) cover the new contract. [Results](tests/results/README.md), 2026-11-11: the skill made the difference in A, C, H and I; B and G held with it but lacked a clean baseline; E and F did not discriminate. Known gap: D (extension popup in its real host) failed in both variants, and three edits made after the last round are untested.

## Deploy targets

Deployed 2026-11-11 by `scripts/deploy-local-skills.py`: relative symlinks for the shared bus `~/.agents/skills/bc-ui-design`, Pi `~/.pi/agent/skills/bc-ui-design`, and Claude Code `~/.claude/skills/bc-ui-design`.
