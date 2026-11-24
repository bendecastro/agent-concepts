---
test_kind: pressure
test_status: pass # dry run 2/2 on Terra low: plan.md met all 11 criteria, 4/4 planted holes
tested: 2026-11-24
deployed: yes
---
# Concept: bc-council-challenge-plan

Challenges a plan or PRD through the advisor council (`council-chain` + `council-mode`) before it is sliced: one scout maps the code the plan names or touches, every advisor attacks the plan sections dealt to it for wrong premises, missing cases, cheaper paths and risky order, advisors attack each other's objections, the owner is grilled (`grilling`) only on the surviving ones, the answers are written into the plan, and `bc-plan-to-pipeline` then slices it in settled-source mode.

## Design decisions

All from the owner-approved [later council chains plan](../../docs/plans/implemented/council-later-chains.md); numbers are that plan's decisions.

- **Thin chain.** Loads `council-chain`, `council-mode`, `grilling` and `bc-plan-to-pipeline` and defines only what `council-chain`'s "What a chain must define" list leaves open. The parent is the plan itself; its pre-reading is reading the plan and numbering its parts. `bc-plan-to-pipeline`'s modes are referenced by name, never copied, so its own edits stay in one home.
- **Map is the plan's code context.** The scout maps what the plan names or would touch, with existing helpers and each plan claim marked as matching, contradicting or unverifiable. Why: wrong premises and cheaper paths are found in the code, not the plan.
- **Objections, four kinds (decision 5).** Each quotes the plan line it attacks and cites `file:line` where the plan claims something about the code. Pass 2 attacks and refines them.
- **The council never rewrites the plan (decision 5).** Only the owner's answers go in, at the line they settle. Why: the plan is the owner's decision record.
- **Grill only survivors, one at a time, in agreement order (decision 5).** An unanswered evidenced dispute drops an objection; the rest are ordered by share of N rating them Strong. Open disputes go to the owner with both sides' evidence, per `council-chain`.
- **Hand-off (decision 6).** Standalone `/bc-council-challenge-plan <plan>`; after the answers are written it runs `/bc-plan-to-pipeline` in settled-source mode with the answers passed as settled. Why: the owner is never asked twice.
- **Focus by sections (decision 7).** Plan sections or steps dealt round-robin; each advisor attacks every kind in its parts and may raise objections anywhere. Why: every part gets a dedicated reader.
- **At most 8 objections per advisor; duplicates are the same quoted line with the same claim.** Copied from `bc-council-find-bugs` for consistency; same line with a different claim is a disagreement, mirroring `council-chain`.
- **Run through without stopping.** Copied from `bc-council-find-bugs`' pressure-test lesson: on a weak consumer a long chain otherwise stops after the map.

## Provenance

- [Later council chains plan](../../docs/plans/implemented/council-later-chains.md), decisions 5–7 and its Testing section.
- Composes [council-chain](../council-chain/CONCEPT.md), [council-mode](../council-mode/CONCEPT.md), [grilling](../grilling/CONCEPT.md) and [bc-plan-to-pipeline](../bc-plan-to-pipeline/CONCEPT.md); shape copied from [bc-council-find-bugs](../bc-council-find-bugs/CONCEPT.md).

## Tests

[tests/scenario.md](tests/scenario.md) dry-runs the chain on a practice code tree whose draft plan holds one planted hole per objection kind ([answer key](tests/answer-key.md)). [Results 2026-11-24](tests/results-2026-11-24.md): 2/2 pass. The first real run with the real council is the live test.

## Deploy targets

Not deployed. When deployed: the shared skill bus via `scripts/deploy-local-skills.py`.
