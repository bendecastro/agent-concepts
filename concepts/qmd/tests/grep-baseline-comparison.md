# Test: qmd vs grep baseline (A/B, cold agents)

Status: Run 2026-07-14 on Arch (qmd 2.5.3, 5 global collections, ~1,055 docs). PASS — results canonized in the skill's "when to reach for it" guidance.

## Setup

Two fresh general-purpose subagents, identical question, ground truth verified beforehand (`music` corpus: `findings/sticker-db-syncthing-fork.md` + `decisions/single-writer-sticker-sync.md`). Condition A: qmd required, grep forbidden. Condition B: grep/read only, qmd forbidden, given the five corpus roots explicitly.

## Round 1 — keyword-friendly question ("play counts diverged between desktop and beelink")

| | grep agent | qmd agent |
|---|---|---|
| Wall time | 36s | 45s |
| Tokens | 25,031 | 24,597 |
| Tool calls | 4 | 4 |
| Correct | yes | yes |

**Tie.** When the question's words literally appear in the corpus, grep matches qmd on every axis. The qmd agent chose the fast `search` tier on its own from the skill text — cold-agent validation that the latency-tier guidance works.

## Round 2 — paraphrase question, zero keyword overlap ("stop two machines doing duplicate work on the same ticket")

- grep, five natural phrasings, all corpora: **0 hits**. Failure mode is silent — an agent reports "nothing recorded" and re-decides settled questions, or burns unbounded tokens brute-reading directories.
- `qmd query --no-rerank`, first attempt, 20.7s: ground truth (`bc-drain-issues` claim-branch/worktree section) at rank 3, plus `dispatching-parallel-agents` at rank 4. `Context:` authority labels present on all hits.

## Conclusions (encoded in body/SKILL.md)

1. Known keyword → grep; qmd adds nothing. The skill's "grep is still fine" caveat is load-bearing, not politeness.
2. Concept/decision recall ("have I thought about this before?") → qmd finds what grep cannot find at all; its value is preventing false "no prior art", not saving tokens on successful searches.
3. Measured tiers reconfirmed: `search` 0.47s, `--no-rerank` 20.7s.
