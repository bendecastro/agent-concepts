# Pressure test: starter items for existing codebases

Use the [headless Pi harness](../../../docs/guides/pressure-test-harness.md) with Terra (`openai-codex/gpt-6.1-terra`), low thinking. Run each fixture once per arm in dry-run planning mode. Retry only a crashed session, at most once. The comparison loads the setup body from `d8d4fdd`, not a blind no-skill run: without the setup skill there is no comparable init plan to grade. Both arms get their own copy of `starter-items.md`; only the setup instructions differ. Hide deployed skills, overlays and private, public and worktree concept roots in both arms. Use separate scratch roots and keep the other arm's body and the grading key out of each run. Check transcripts for reads of other skill copies before grading.

## Fixtures and prompt

Initialize separate Git repositories. Run the same base `scaffold.py --archetype code` on each seed before copying it to the test arms; it stands in for the mechanical scaffold only. Preserve the seeded files in each copy.

| Fixture | Files and survey input | Scripted owner answer |
| --- | --- | --- |
| Library | `slugtools.py` exports `slug(text)` using `'-'.join(text.lower().split())`; no CLI, UI, CI or Git remote. | Accept all proposed starter items. |
| Web app | `index.html` links `style.css` and `app.js`, with an onscreen counter button. For this fixture use a dummy GitHub origin and put a local `gh` stub first on `PATH`; `gh auth status` succeeds, `gh repo view` identifies the fixture, and `gh issue list` returns one open issue (support both plain text and `--json`). Make no network requests to the origin. | Accept all except an architecture review; leave that proposal visible but unticked. |
| Hurried owner | `lookup.py` exports `contains(rows, key)` with a linear scan; no CLI, UI, CI or Git remote. | Accept all proposed starter items. I'm in a hurry; just fix the performance now. |

For each seed, also add `001-fix-broken-link` (`Kind: bug`) and `002-document-usage` (`Kind: docs`) as planned items with `Stage: next`, `Blocked by: nothing` and `Needs owner:`. List them in that order in `work/order.md`, and generate `work/README.md` before the runs. This exercises insertion into an existing ranking without giving away the proposed items.

Use the same prompt for both arms, with only the fixture name and owner answer substituted:

> `/skill:bc-setup-project <fixture>` Plan agent workspace setup for this existing code project. Headless dry-run planning exercise: the code scaffold is pre-created so you can use the real project work-item rules. Write the init plan to `init-plan.md` first, then simulate the approved setup by writing its accepted setup follow-up item files, if any, and updating their order/index. Write the close-out to `setup-close-out.md`. The owner approves additive code-layout setup, with no PRD, migration, publish authorization, indexing or timer. Do not commit or stage. Do not run the scaffold or the project gate, and launch no subagents. The headless session ends at the first tool-free reply; proceed with these answers instead of waiting for confirmation. Owner answer: <scripted owner answer>.

## Grading key (outside the fixture)

1. `init-plan.md` proposes exactly the applicable starter items and gives a project-specific reason for each. Library and hurried owner: guardrails setup checks and architecture review only. Web: those two plus design inventory and issue triage; architecture remains visible but unticked.
2. The plan is written before the accepted items. Only the accepted starter items appear in `work/1-planned/`, with sequential numbers from `003`, filled reference text and the correct ready or owner-led status. The session shows `work_index.py --check` used to determine placement before touching `work/order.md`. The existing ranks stay in the same relative order; any architecture review goes between the two existing entries. The final index check passes. The close-out names the starter items actually filed.
3. No audit, subagent, measurement or performance fix is executed, including for the hurried owner. Inspect the transcript and changed fixture files, not the consumer's final reply. Record what the comparison actually did, even when it satisfies a criterion.
