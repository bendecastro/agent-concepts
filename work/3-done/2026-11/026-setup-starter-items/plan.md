# Seed starter work items when setting up an existing codebase

Why: on an existing codebase `bc-setup-project` creates `docs/design/README.md` and `docs/guardrails/README.md` with empty lists and only names follow-up skills in its close-out, so nothing records the app's existing design, nothing adds the stack checks that `bc-performance-guardrails` § Setup checks says belong "at project setup", and `work/` starts empty on the owner's dashboard.
Done when: setting up an existing codebase proposes, in the init plan, only the starter items its survey shows apply; the accepted ones land in `work/1-planned/` and `work/order.md`; the change has held under a pressure test; requirements in [requirements.md](requirements.md).
Stage: now
Blocked by: nothing
Kind: feature
Source: owner conversation about post-setup onboarding, 2026-11-26
Planned: bc-plan-to-pipeline 2026-11-26
Ready for agent: yes

## Steps

- [x] Starter-item reference and its test: a new `starter-items.md` in `concepts/bc-setup-project/body/` holds the four starter items (design inventory, guardrails setup checks, architecture review, issue triage), each with its applicability signal and its item text per the requirements' table (Kind, `Source: bc-setup-project`, full steps and `Ready for agent: yes` for the first two, `Needs owner:` for the last two); a new test in `concepts/bc-setup-project/tests/` fills each into a fixture work folder and runs `work_index.py --check`. Blocked by: nothing. Stories 2, 4, 5. Done when the test, watched failing first, passes and every step of the two ready items states `Done when` and `Out of scope`. Out of scope: `SKILL.md` wiring and `scaffold.py`.
  - Review: approved by tier-1 2026-11-26
  - Gate: pass ./scripts/gate at eb7d2a0 2026-11-26
  - Landed in `eb7d2a0`.
- [x] Setup proposes and writes starter items: `bc-setup-project`'s `SKILL.md` gathers the signals in its survey, lists proposed starter items with their reason in the init plan for existing codebases only, writes the accepted ones after the scaffold (next number, `--check` placement), names them in the close-out, and never runs an audit during setup; `bc-performance-guardrails` § Setup checks names the starter item; `hands_off` edges in `concepts/relationships.json` regenerated; `CONCEPT.md` decisions, provenance and status frontmatter, `index.md`, `.bc-agent/log.md`. Pressure test (a new `pressure-starter-items.md` in `concepts/bc-setup-project/tests/`) run on the branch before landing (the body deploys by symlink): blind baseline and with-change runs on the pressure-test model over the three fixtures in the requirements. Blocked by: Starter-item reference and its test. Stories 1, 3, 6, 7. Done when the with-change runs propose exactly the applicable items in all three fixtures and run no audit, the baseline does not, results are recorded beside the scenario, and lint has 0 ERROR and the gate passes. Out of scope: re-offering starter items to already set-up projects; new or empty projects.
  - Review: approved by tier-1 2026-11-26
  - Gate: pass ./scripts/gate at bc525c0 2026-11-26
  - Landed in `79a6bb1`.

## Outcome

Setup now offers starter work items for existing codebases: `starter-items.md` holds design inventory, guardrails setup checks (both ready for an agent), architecture review and issue triage (both need the owner). The survey gathers each item's signal, the init plan lists the applicable ones with a reason, and accepted items are filed after the scaffold; setup runs no audit. A scaffold test checks all four items with `work_index.py --check`. Pressure test, one Terra low dry run per arm over three fixtures: the revised body proposed and filed starters in 3/3, the pre-change body in 0/3; neither ran an audit.

Spent: 52m active, 10M tokens, $6.31 (estimated; pi 8 sessions, claude-code 0 sessions, codex 0 sessions; other tools not counted)
