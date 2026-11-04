---
test_kind: pressure
test_status: partial
tested: 2026-11-04
deployed: yes
---
# Concept: show-me

Model-invoked visual explanations of how systems, pipelines, modules, and code
paths work. Supplies the smallest useful visual alongside the words it supports,
including inside a comprehensive how-it-works document.

## Design decisions

- **Model-invocable, not always-on.** Drop upstream's user-only invocation flag.
  [Issue #12](https://github.com/humanlayer/skills/issues/12) exposes how that flag
  blocks composition; agents should reach for visuals while writing explanations.
  Narrow triggers and explicit exclusions keep ordinary Q&A and other reports out.
- **Inline is the default.** Adapt `prompting-agents`' loading-is-not-authorization
  block: HTML creation/opening is the costly path, not permission implied by an
  informational question. Explicit artifact requests permit one file, not a deck
  of unrelated views or an unsolicited commit.
- **Examples over rules.** Retain upstream's form menu and shape examples, not a
  mandatory checklist. Adapt prompting-agents' context economy and scope discipline.
- **Current-state, source-grounded docs.** Cite code behind the boxes and choose
  a form the destination renders. Defer placement to codebase-docs and prose to
  plain-language/unslop; architecture reports, lessons, and UI retain their owners.
- **Existing contracts preserved.** The six consumer pointers (plain-language, unslop, codebase-docs, teach, improve-codebase-architecture, frontend-design) only clarify visual
  ownership. Teach's host adapter, state, cadence and after-lesson artifact contract
  are unchanged, so its existing incoming/outgoing relationships are unaffected.

## Provenance

- [HumanLayer snapshot](../../docs/research/raw/humanlayer-show-me/SOURCE.md),
  pinned at `4d69d20f6e9b57b4fcf0d501ccfb1be961f0f329`: show-me skill and
  visual-pr's show-me reference. MIT © 2026 HumanLayer; the full
  [license notice](../../docs/research/raw/humanlayer-show-me/LICENSE) is preserved.
- Dex Horthy, [show-me skill](https://www.humanlayer.com/blog/show-me-skill):
  visual alternatives to walls of prose.
- [Matt Pocock talk notes](../../docs/research/raw/pocock-pr-bottleneck-talk/SOURCE.md):
  visual explanations as an aid to understanding changes.
- `concepts/prompting-agents/body/SKILL.md`: composition, loading is not
  authorization, examples over rules, scope and context economy.

## Tests

`tests/pressure-show-me.md` defines artifact-graded checks. Checks 1, 3, 4, 5 PASS 2026-11-04 (see the file); the pressure
test gate applies before deployment.

## Deploy targets

Deployed 2026-11-04 (owner choice: deploy before the trigger checks) via
`scripts/deploy-local-skills.py`: shared bus (`~/.agents/skills/`), Pi and Claude Code.
Checks 2 and 6 and description-only discovery remain unrun.
