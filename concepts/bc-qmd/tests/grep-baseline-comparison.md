# Test: qmd vs grep baseline (A/B, cold agents)

Status: Run 2026-07-14 on Arch (qmd 2.5.3, 5 global collections, ~1,055 docs). PASS — results canonized in the skill's "when to reach for it" guidance.

## Setup

Two fresh general-purpose subagents, identical question, ground truth verified beforehand (`music` corpus: `findings/sticker-db-syncthing-fork.md` + `decisions/single-writer-sticker-sync.md`). Condition A: qmd required, grep forbidden. Condition B: grep/read only, qmd forbidden, given the five corpus roots explicitly.

## Round 1 — keyword-friendly question ("play counts diverged between desktop and <second-machine>")

| | grep agent | qmd agent |
|---|---|---|
| Wall time | 36s | 45s |
| Tokens | 25,031 | 24,597 |
| Tool calls | 4 | 4 |
| Correct | yes | yes |

**Tie.** When the question's words literally appear in the corpus, grep matches qmd on every axis. The qmd agent chose the fast `search` tier on its own from the skill text — cold-agent validation that the latency-tier guidance works.

## Round 2 — paraphrase question, zero keyword overlap ("stop two machines doing duplicate work on the same ticket")

- grep, five natural phrasings, all corpora: **0 hits**. Failure mode is silent — an agent reports "nothing recorded" and re-decides settled questions, or burns unbounded tokens brute-reading directories.
- `qmd query --no-rerank`, first attempt, 20.7s: ground truth (`bc-pipeline-to-done` claim-branch/worktree section) at rank 3, plus `bc-dispatching-parallel-agents` at rank 4. `Context:` authority labels present on all hits.

## Conclusions (encoded in body/SKILL.md)

1. Known keyword → grep; qmd adds nothing. The skill's "grep is still fine" caveat is load-bearing, not politeness.
2. Concept/decision recall ("have I thought about this before?") → qmd finds what grep cannot find at all; its value is preventing false "no prior art", not saving tokens on successful searches.
3. Measured tiers reconfirmed: `search` 0.47s, `--no-rerank` 20.7s.

## Plan 2026-11-28: re-run Round 2 against the reworded body (not yet run on a model)

The body now says: short keywords always, `qmd search` first, one `qmd query --no-rerank` rerun on a miss or a likely paraphrase, full `qmd query` only when ranking quality matters. The Round 2 result above predates it and does not show that a cold agent reaches ground truth under it.

Baseline measured 2026-11-28 (qmd, `music` collection present, plain BM25, no model): `qmd search "stop two machines doing duplicate work on the same ticket" -c music --format files -n 10` returned **no results** (2.7s). Unscoped, the same query returned one unrelated hit (`agents` collection, `work/3-done/2026-11/024-skill-delivery/evidence/2026-11-25-repo-scout.md`, score 90%, 3.6s), not the ground truth. Note the original Round 2 ground truth was in the `bc-pipeline-to-done` / `bc-dispatching-parallel-agents` bodies and the `music` collection holds the music corpus, so this checks the BM25 inference only; the model run must use the collections Round 2 used.

Run when quota returns (openai-codex/gpt-6.1-terra, thinking low), one cold agent given only the new `bc-qmd` body and the Round 2 question, grep forbidden:

1. Record the first command it picks and every follow-up, with wall time.
2. Record whether it reaches the ground truth (`bc-pipeline-to-done` claim-branch/worktree section) and at which rank.
3. PASS: it starts with `qmd search`, reruns as `qmd query --no-rerank` after the miss, and reports the ground truth. FAIL: it concludes "no prior art" after `search` alone, accepts an unrelated `search` hit (such as the 90% `agents` hit recorded above) as the answer, or picks full `query` for an exploratory lookup. If `search` itself returns the ground truth, record it as INCONCLUSIVE for the fallback (the rule was not exercised) and rerun with the question unchanged on the same collections as Round 2.
4. Only then tick the work item step and update `CONCEPT.md`'s "has not been re-run" note.
