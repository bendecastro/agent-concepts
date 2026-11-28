# Worktree numbering pressure results — 2026-11-28 (INCONCLUSIVE)

Scenario: `pressure-worktree-numbering.md`. Change under test: tag `055-hold` (commit `74645d3`), item `055-project-files-in-scaffold`. Consumer model: `anthropic/claude-haiku-5-5`, thinking `low` (owner decision 2026-11-28, while the Codex quota is used up; replaces Terra). Pi 1.6.1 headless through `scripts/pi_sandbox.py`.

## Arms prepared

| Arm | Fixture `.bc-agent/AGENTS.md` | Skills |
| --- | --- | --- |
| with-block ×2 | current scaffold (`055-hold`): full "Only the main checkout creates numbered items" rule | `055-hold` bodies |
| skill-only ×1 | pre-change scaffold (`04eb706`): old short bullet only | `055-hold` bodies |

Fixtures were built as the scenario says (scaffold `--archetype code`, `001-login`/`002-search` committed, uncommitted `003-reports.md` in main, `git worktree add ../wt -b plan`, run from `../wt`). `pi_sandbox.py`'s system prompt check passed for all three arms.

## Outcome

No arm reached the model. Every attempt returned `429 rate_limit_error` ("This request would exceed your account's rate limit") on the first request: 3 parallel attempts, then 6 sequential attempts per arm with 120 s waits (about 36 minutes). The repositories were left unchanged (no commits, `work/` untouched, main's `003-reports.md` intact), so there was nothing to grade.

| Criterion | with-block 1 | with-block 2 | skill-only |
| --- | --- | --- | --- |
| 1–5 | NOT RUN (429) | NOT RUN (429) | NOT RUN (429) |

Status frontmatter not changed. Rerun when the Anthropic rate limit clears.
