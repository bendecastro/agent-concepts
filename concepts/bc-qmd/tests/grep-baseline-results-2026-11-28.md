# Results 2026-11-28: Round 2 rerun (paraphrase question) — PASS

Plan: `grep-baseline-comparison.md`, section "Plan 2026-11-28: re-run Round 2 against the reworded body".
This file replaces the morning's INCONCLUSIVE record (every launch then got Anthropic 429 because the consumers ran without the account-pool extension).

- Commit under test: `f2eda93` (tag `059-hold`, work item `059-qmd-query-contradiction`).
- Consumer model: `anthropic/claude-haiku-5-5`, thinking `low`. Owner-approved substitute while the Codex quota is used up; the plan named `openai-codex/gpt-6.1-terra`.
- Harness: Pi 1.6.1 via `scripts/pi_sandbox.py`, `-ne -e <pi-multiprovider> -ns --no-prompt-templates --no-skills --skill <scratch copy of the arm's bc-qmd body>`. The multiprovider extension only picks which Claude account serves the request. The outer bwrap mounted tmpfs over the workspace checkout and the subagent worktrees, so neither arm could read either body version from the repository. Scratch Git project with a one-paragraph `AGENTS.md`. Runs were sequential.
- Arms: **with change** = `bc-qmd/body/SKILL.md` at `f2eda93`. **Without change** = the same body at `74645d3`, which says `qmd query` is "the default". Both arms got the same prompt, which did not name the change: `/skill:bc-qmd`, the Round 2 question ("how to stop two machines doing duplicate work on the same ticket"), qmd required, no grep/rg/find, and write `answer.md` with the answer, sources and every command.
- Blinding shim: `grep-baseline-comparison.md` is itself indexed in the `agents` collection and quotes both the question and the ground truth. The first with-change run found it (`qmd search "duplicate"`), ran `qmd get` on it, and read the ground truth. That run is excluded below. After it, a `qmd` wrapper on `PATH` dropped every `bc-qmd/tests/` hit from results, refused `qmd get` on those paths, and logged each call with wall time. All other output was passed through unchanged. Ranks below are after that filter. No `qmd update`/`embed` was run.

## Preconditions (read-only)

`qmd status`: 1,892 files, 15 collections including `agents`. `qmd search "claim branch worktree" -c agents --format files -n 3` returned `bc-pipeline-to-done/body/SKILL.md` at rank 2 (0.90).

## Runs (graded from session JSONL tool calls and the shim log)

| Run | First qmd command | Follow-ups | Full `qmd query`? | Answer / source | Wall |
|---|---|---|---|---|---|
| with-1 (excluded: read the test file) | `search "duplicate work ticket lock"` | 6× `search`, `get` of the test file, 1× `query --no-rerank` | no | claim branch; `docs/guides/pipeline.md` + `bc-pipeline-to-done` body | 69s |
| with-2 | `search "duplicate ticket machines lock"` (0.2s) | `search` ×4 (`duplicate work`, `two machines ticket`, `lock claim`, `claim machine`), then `query --no-rerank "claim ticket"` (15.2s), `search "claim ref protocol"`, `get bc-pipeline-to-done/body/SKILL.md` | no | no-force `bc-drain-claims/issue-<n>` claim ref from `bc-pipeline-to-done/body/SKILL.md` (its `source-issues.md` was rank 3 of the `--no-rerank` run) | 41s |
| with-3 | `search "duplicate work ticket machines"` (0.3s) | `query --no-rerank "ticket claim lock machines"` launched in parallel with a `search`, failed at once (qmd SQLite `trigger documents_ai already exists`, a concurrent-start race), `search` ×4, then `query --no-rerank "ticket claim machines"` (20.3s; `docs/guides/pipeline.md:85` Claim bullet at rank 5), `get pipeline.md:83:6` | no | no-force `bc-drain-claims/issue-<n>`/`item-<slug>` claim branch; `docs/guides/pipeline.md` (the `/bc-pipeline-to-done` claim section) + glossary "claim" | 44s |
| without-1 | `search "two machines duplicate work same ticket lock claim"` (sentence-length) | **full `qmd query` with the whole sentence + `--intent`** (149.4s), `search`, `get pipeline.md:83:6` | **yes** | claim branch; `docs/guides/pipeline.md:85` | 167s |
| without-2 | **full `qmd query "stop two machines doing duplicate work on the same ticket" --intent …`** as its first search (killed by its 180s tool timeout) | `search` ×5 (some sentence-length), `get` ×2 | **yes** | claim ref; `bc-pipeline-to-done/tests/pressure-drain.md` + `README.md` (says it did not open the skill body) | 237s |

## Checks (with-change arm, clean runs with-2 and with-3)

| Check | Result |
|---|---|
| 1. First command and follow-ups recorded, with wall time | Done (table above, from the shim log). |
| 2. Ground truth reached, and rank | Both reached the claim mechanism. with-2 opened and cited `bc-pipeline-to-done/body/SKILL.md`, after its `source-issues.md` came up at rank 3 in `--no-rerank`. with-3 cited `docs/guides/pipeline.md`'s Claim bullet, the human guide to the same `/bc-pipeline-to-done` claim (rank 5 in `--no-rerank`), and did not open the skill body. |
| 3. PASS: `search` first, `query --no-rerank` after the miss, ground truth reported | **Held 2/2.** Both started with short-keyword `qmd search`, got off-topic hits, reran as `qmd query --no-rerank` with short terms, and reported the claim mechanism. Neither ran full `qmd query`, concluded "no prior art", or accepted an unrelated `search` hit. |
| FAIL conditions | None hit in the with arm. Both without-arm runs hit "picks full `query` for an exploratory lookup", which took 149s in one and timed out at 180s in the other. |

**Verdict: PASS.** Against the old body, the change moves the cold agent off full `qmd query`: with-change runs took 41–44s and the without-change runs 167–237s.

Caveats: n=2 per arm, on Haiku rather than Terra. The with arm ran more than one `search` reformulation before the `--no-rerank` rerun rather than exactly one miss then one rerun; the plan does not count that as a failure. One with run fired `--no-rerank` early, in parallel, and it crashed on a qmd SQLite race, so the one `--no-rerank` that ran came after the misses. with-3's source is the guide page, not the skill body named as ground truth in 2026-07-14.
