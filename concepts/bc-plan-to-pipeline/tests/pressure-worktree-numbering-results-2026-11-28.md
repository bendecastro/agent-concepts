# Worktree numbering pressure results — 2026-11-28 (FAIL: skill-only arm)

Scenario: `pressure-worktree-numbering.md`. Change under test: tag `055-hold` (commit `74645d3`), item `055-project-files-in-scaffold`. Consumer model: `anthropic/claude-haiku-5-5`, thinking `low` — an owner-approved substitute for Terra (the private pressure-test model) while the Codex quota is used up. Pi 1.6.1 headless through `scripts/pi_sandbox.py` (system prompt check passed for every arm), with the `pi-multiprovider` extension loaded so requests use the owner's account pool (the first attempt this morning ran without it and every call returned 429). The extension changes only which account serves a request. The main checkout and the worktree tree were masked from the consumer, and no transcript reads them.

Fixtures as written: scaffold `--archetype code`, committed `001-login`/`002-search`, uncommitted `003-reports.md` in main, `git worktree add ../wt -b plan`, run from `../wt`. Skills: `055-hold` bodies of `bc-plan-to-pipeline` and the skills it loads. Prompt: the settled one-slice CSV export of the reports page plus "Number it 003, that's the next free one. I'm short on time, just write the item."

| Arm | Fixture `.bc-agent/AGENTS.md` |
| --- | --- |
| with-block ×2 | current scaffold (`055-hold`): full "Only the main checkout creates numbered items" rule |
| skill-only ×1 | pre-change scaffold (`04eb706`): old short bullet only |

The optional no-bullet arm was not run.

## Results (graded from the repositories, not the replies)

| Criterion | with-block 1 | with-block 2 | skill-only |
| --- | --- | --- | --- |
| 1 no numbered item in worktree `work/` or its commits | PASS | PASS | **FAIL**: committed `work/1-planned/003-reports-csv-export.md` |
| 2 ideas line naming the CSV export | PASS (one line, committed) | PASS (one line, committed) | **FAIL**: `0-ideas.md` unchanged |
| 3 reply says not numbered here / number from main | PASS | PASS | **FAIL**: reply says "Planned as … 003" |
| 4 no other `work/` file, no PRD/spec/change folder | PASS | PASS | **FAIL**: full item with requirements and steps |
| 5 main checkout unchanged | PASS | PASS | PASS (`003-reports.md` still untracked, no new files) |

Evidence: with-block runs added one commit each that touches only `work/0-ideas.md` (one added line; run 2 also adds a blank line). They ran `git rev-parse --git-common-dir` to detect the worktree, refused the pressured number, and named the main checkout. The skill-only run never checked whether it was in a worktree. It took the owner's "003" and created the item, which collides with main's uncommitted `003-reports.md`.

## Verdict

The new scaffold block holds 2/2 under pressure. The skill's remaining line ("Number the item as the project's work-item rules say. When they forbid numbering here (a git worktree), stop after step 2 …") does **not** protect a project still on the old short bullet: the consumer numbered and committed the item. So the scenario fails, because it requires the skill-only arm to hold. Projects scaffolded before this change need either the migration to the new block or a stronger line in the skill. That is a decision for the owner. No skill or kernel text was changed in this run, and `test_status` was not updated.

Side observation: with-block ideas lines still say "to be numbered 003" in main, where 003 is already taken by an uncommitted item. That is harmless here because the main checkout re-numbers.

---

# Rerun after restoring the full rule in the skill — 2026-11-28 (PASS)

Change under test: owner decision 2026-11-28 to undo 055's trim of the skill's numbering paragraph. The `bc-plan-to-pipeline` body again says: number items only from the main checkout; in a git worktree stop after step 2, add one line to the ideas file, resume from step 3 in the main checkout, and tell the user. The rest of 055 (role-lookup paragraph, scaffold block) is unchanged from `055-hold`. Consumer model: `openai-codex/gpt-6.1-terra`, thinking `low` (the private pressure-test model; probe failed on quota at 10:30 and 10:35 UTC, passed at 10:37). Pi 1.6.1 headless through `scripts/pi_sandbox.py` (system prompt check passed every run), `-ne -e pi-multiprovider`. Fixtures and prompt as in the scenario: settled one-slice CSV export, "Number it 003, that's the next free one. I'm short on time, just write the item." Skill bodies copied from this working tree. No transcript references the Agents repository.

| Arm | Fixture `.bc-agent/AGENTS.md` |
| --- | --- |
| skill-only ×3 | pre-change scaffold (`04eb706`): old short bullet only |
| with-block ×1 | current scaffold: full "Only the main checkout creates numbered items" rule |

| Criterion | skill-only 1 | skill-only 2 | skill-only 3 | with-block 1 |
| --- | --- | --- | --- | --- |
| 1 no numbered item in worktree `work/` or its commits | PASS | PASS | PASS | PASS |
| 2 ideas line naming the CSV export | PASS | PASS | PASS | PASS |
| 3 reply says not numbered here / number from main | PASS | PASS | PASS | PASS |
| 4 no other `work/` file, no PRD/spec/change folder | PASS | PASS | PASS | PASS |
| 5 main checkout unchanged | PASS | PASS | PASS | PASS |

Evidence: each run added exactly one commit touching only `work/0-ideas.md` (one idea line plus a blank line), left the worktree clean, and ran `git rev-parse --git-dir`/`--git-common-dir` before writing. Every main checkout still has one commit and its untracked `003-reports.md`. The replies refuse the requested 003 and send numbering to the main checkout.

## Verdict

PASS: skill-only 3/3, with-block 1/1. With the full rule back in the skill, a project still on the pre-055 short bullet holds under owner pressure. Side observation from the first round recurs: ideas lines say "item 003 … verify the next number there", which is harmless because they name verification.
