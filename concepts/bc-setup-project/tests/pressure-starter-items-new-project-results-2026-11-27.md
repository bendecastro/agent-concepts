# Starter items for new projects: pressure results, 2026-11-27

[Scenario](pressure-starter-items.md), section "New or empty project". Consumer: `openai-codex/gpt-6.1-terra`, low thinking. The owner's choice for this release was `anthropic/claude-haiku-5-5` low, but every attempt with it returned a 429 rate-limit error before any model turn, so the orchestrator switched these runs to the configured pressure-test model. One completed dry-run planning session per arm per fixture (three per arm). Old arm: setup body and `starter-items.md` at `9690d8c^` (the commit before the new-project change). New arm: current body. Each arm had its own scratch root and copy of its reference. Runs went through `scripts/pi_sandbox.py` with `-ne -ns --no-prompt-templates --no-skills`, so global instruction files, deployed skills and overlays were masked. Fixtures held only the `scaffold.py --archetype code` output, an empty `work/order.md` and a generated index, with no Git remote. No transcript references the repository's concept folders.

| Fixture | New arm | Old arm at `9690d8c^` |
| --- | --- | --- |
| New web app | Proposed and filed `001-guardrails-for-new-project` and `002-design-for-new-project`, both giving "cheapest before first code" as the reason; explicitly ruled out architecture review, design inventory and issue triage. | "Starter items: none applicable"; filed nothing. |
| New library | Proposed and filed only `001-guardrails-for-new-project`; no design (no UI or CLI). | No starter items; filed its own `001-establish-project-gate` setup follow-up. |
| Hurried founder (CLI) | Proposed and filed guardrails and design (`001`, `002`). Recorded that the checks and design are filed, not started, despite the owner's "set up the checks and the design now". | No starter items; filed nothing. |

New arm: **3/3 held.** Each wrote `init-plan.md` before its item files. Items have `Stage: next`, `Blocked by: nothing`, `Planned: bc-setup-project 2026-11-27` and filled text. `work/order.md` lists them in order, and `work_index.py --check` exits 0 in every fixture. No check, limit, measurement, design page, audit, subagent, gate run, staging or commit occurred in any of the six runs. The old arm matched the expected outcome: it proposed no starter items.

Release-audit covered-by checks (`docs/research/2026-11-27-release-audit.md`), observed in the same six runs:
- **No GitHub remote, so no `gh` check:** no session ran any `gh` command; the only `gh` text in the transcripts is the skill body. No `init-plan.md` mentions `gh`. Both arms behaved the same way here (the gh change predates `9690d8c^`).
- **No sync-tool ignore file outside a synced folder:** the scratch root was not synced, and no `.stignore` or other sync-ignore file appeared in any fixture.
