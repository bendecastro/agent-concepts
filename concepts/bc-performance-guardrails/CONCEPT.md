---
test_kind: pressure
test_status: pass
tested: 2026-11-25
deployed: yes
---
# Concept: guardrails

## What it is

One method for every guardrail in a project: performance budgets (limits on time, bytes or memory), fitness functions (checks for a structural property) and the ratchet that keeps both from getting worse. Each project keeps a `docs/guardrails/README.md` page listing its targets, budgets and checks; the checks run inside the project's existing full gate. Performance is the first and most detailed part. The lean entry links [measuring.md](body/measuring.md) (runs, noise, ratchet) and [targets.md](body/targets.md) (published user-facing defaults).

## Design decisions (2026-11-25)

- General method rather than performance only, as its own concept; the project page comes from `bc-setup-project`, mirroring the design framework (`bc-design`'s `design-framework.md` and `docs/design/README.md`): read the page first, copy the scaffold text when it is missing, record a limit as the agent's choice the owner may change, land the page line in the same commit as the check (owner decisions, grill 2026-11-25).
- Agents set every limit themselves: a measured ratchet when none exists, published guidelines for user-facing targets. Asking the owner for a number was rejected because guardrails would then not appear without the owner's effort. Owner-chosen limits are never loosened to make a check pass.
- Three check kinds (static, artifact, dynamic), cheapest reliable kind first; the kinds and their split follow the research synthesis, and the glossary already defines them.
- A fixed regression gets its check in the same change even under time pressure; at setup, checks only for stack problems with a named source or past bug, each ratcheted so existing shortfalls do not fail the gate. Why: poteto's practice of turning each found issue into a lint rule, bounded so unsourced checks are not added.
- No shared measuring script or benchmark tool in the scaffold (owner decision). The run count and the one-tenth noise threshold in `measuring.md` are this method's defaults, not a published standard.
- Design-consistency checks stay on the design page; the guardrails page links to it.
- `bc-optimize-code` points here for measuring and noise, and a kept improvement tightens the matching limit.

## Provenance

- [Performance guardrails research](../../docs/research/2026-11-25-performance-guardrails/README.md) (2026-11-25) — vocabulary, check kinds and sources below.
- [poteto, trusting agent work](https://potibo.dev/en/post/2111133080526495985) — "make the easy thing the right thing"; enforce with architecture and automated checks before prose and review.
- [poteto, 60 fps browser game](https://x.noodl3.net/poteto/status/2117043478140276847) (mirror of [the X post](https://x.com/poteto/status/2117043478140276847)) — a lint rule for each found issue and a build-failing download-size budget. It sets no per-step millisecond budget and no frame-rate regression test; no threshold here is attributed to it.
- [Google RAIL](https://web.dev/articles/rail), [Core Web Vitals](https://web.dev/articles/vitals), [web.dev performance budgets](https://web.dev/articles/performance-budgets-101), [AWS latency budgets](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentperf01-bp01.html) — targets and budget decomposition.
- [Building Evolutionary Architectures précis](https://evolutionaryarchitecture.com/precis.html) — fitness functions.
- [CodSpeed thresholds](https://codspeed.io/changelog/2025-10-31-per-benchmark-regression-thresholds), [Spotless ratchet](https://github.com/diffplug/spotless/blob/main/plugin-gradle/README.md#ratchet), [Size Limit](https://github.com/ai/size-limit), [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md#assert) — regression thresholds, ratchet and size budgets.
- [Electron performance](https://www.electronjs.org/docs/latest/tutorial/performance) — blocking I/O in the main process as a sourced setup check.
- [ui-design design framework](../bc-design/body/design-framework.md) — page, write path and agent's-choice model copied here.
- [bc-prompting-agents](../bc-prompting-agents/body/SKILL.md) — rule-plus-why phrasing.

## Tests

[Pressure scenarios](tests/scenario.md): fixing a slowdown under "no time for a check", setting a budget without asking or inventing a number, and an owner-chosen limit blocking a change. Passed 2026-11-25 on the configured model with no tuning: without the skill the agent fixed the slowdown but added no check, and with it the agent added a check; B and C held in both runs ([results](tests/pressure-results-2026-11-25.md)).

## Deploy targets

Deployed 2026-11-25 by `scripts/deploy-local-skills.py`: relative symlinks `~/.agents/skills/bc-performance-guardrails`, `~/.pi/agent/skills/bc-performance-guardrails` and `~/.claude/skills/bc-performance-guardrails`, after the pressure test held.
