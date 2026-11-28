---
test_kind: pressure
test_status: pass # 2026-11-28 find-bugs filing scenario C2 on Haiku low (Terra out of quota): tuned module 3/3, inline master text 3/3; first wording 1/3 (tests/pressure-file-findings-results-2026-11-28.md)
tested: 2026-11-28
deployed: no
---
# Concept: bc-file-findings

Model-invoked module holding how a review's findings become project work once the owner has picked: wait for the pick (an answer already in the invoking message is the pick); chosen → numbered work-planned item from the project's template with the caller's `Kind:`/`Source:`; rejected → numbered work-dropped item whose `## Outcome` gives the owner's reason; everything else → one ideas line each; number only from the main checkout (from a worktree, ideas lines stating the choice); order placement and `work_index.py --check`; commit; then `bc-plan-to-pipeline` from a settled source on each filed item in the same reply, leaving them planned. Without a project work pipeline it files nothing and says so.

## Design decisions

- **Extracted from `bc-find-bugs` §5 (2026-11-28, item 056-file-findings-module).** `bc-find-bugs`, `bc-improve-codebase-architecture` and `bc-council-audit-security` each restated the filing rules, and only `bc-find-bugs` held the tested parts (an answer in the invoking message is the answer; plan every filed item). The module carries the `bc-find-bugs` wording, generalised from "confirmed bug" to "chosen finding".
- **The caller supplies Kind, Source and contents.** What an item must carry (reproduction test, report folder, no exploit steps) is evidence only the caller knows, so it stays in the caller's filing section; the module owns only the homes, numbering, placement and handoff.
- **Four numbered steps, finished only when every filed item has a `Planned:` line (2026-11-28 tune).** As first written, the planning handoff closed the section as a paragraph and two of three Haiku runs stopped after the filing commit; numbered steps with that finish line held 3/3.
- **Callers keep a one-line fallback,** as `bc-safe-runs`' callers do, so a stranger who installed one skill without the module still files correctly. A change to the module's rules must update those fallbacks.
- **`bc-council-audit-security` gains rejected/ideas homes and the planning handoff** by loading the module; before, it filed only picked findings and did not plan them. This is the uniformity the item asked for.
- **Would-be callers load it conditionally:** `bc-self-improve` when a picked proposal becomes later project work, `bc-prototype` when its verdict becomes project work, `bc-council-challenge-plan` when the owner accepts an objection but wants it handled outside the plan. Their wording at each site is this change's choice; the item named them as callers but did not say where.

## Provenance

- [bc-find-bugs §5](../bc-find-bugs/body/SKILL.md) as of 518f99b — source text, tested 2026-11-24 ([results](../bc-plan-to-pipeline/tests/pressure-plan-every-item-results-2026-11-24.md), scenario C2).
- [bc-improve-codebase-architecture §4](../bc-improve-codebase-architecture/body/SKILL.md) — the chosen/rejected/everything-else homes and the rejected-with-reason rationale.
- [bc-council-audit-security](../bc-council-audit-security/body/SKILL.md) — pre-selected `all` and the no-pipeline fallback.
- [Work item 056-file-findings-module](../../work/2-active/056-file-findings-module.md), from the modularity scan of 2026-11-27 (owner pick 1, candidate C).
- [bc-setup-project](../bc-setup-project/CONCEPT.md) — the Where things go roles, work-item rules and `work_index.py` it relies on.

## Tests

[`tests/pressure-file-findings.md`](tests/pressure-file-findings.md) reruns scenario C2 of `bc-plan-to-pipeline/tests/pressure-plan-every-item.md` (find-bugs filing with `all` plus "short on time" and "just start it") with the fixture built by [`tests/make-fixture.sh`](tests/make-fixture.sh). Results: [`tests/pressure-file-findings-results-2026-11-28.md`](tests/pressure-file-findings-results-2026-11-28.md).

## Deploy targets

Not deployed. When deployed: the shared skill bus via `scripts/deploy-local-skills.py`, and the npm package and plugin manifests like its callers.
