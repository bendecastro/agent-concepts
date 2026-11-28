# bc-qmd and bc-wiki-maintain agree on whether to use qmd query

Why: `bc-qmd/body/SKILL.md` says `qmd query` is "best quality; the default" while `bc-wiki-maintain/body/SKILL.md` says "Never use `qmd query`" for inline reads and backs it with a benchmark (17 of 20 misses for full-sentence queries); agents get opposite advice depending on which skill loaded.
Done when: The two skills give one consistent rule (for example: inline lookups use keyword search with 2-4 terms; `qmd query` only for deliberate deep searches), with the benchmark finding moved or linked into `bc-qmd`.
Stage: now
Blocked by: nothing
Kind: bug
Source: modularity scan 2026-11-27 (run ~/.local/state/bc-swarm/2026-11-27-agents-modularity/memo.md), owner pick 1 (finding F)
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Steps

- [x] Reconcile the rule in both bodies. Done when `rg "qmd query" concepts/*/body` shows no contradiction, lint passes, and bc-qmd's existing pressure scenario still holds.

## Outcome

bc-qmd now owns the rule: 2–4 keywords, `qmd search` first, one `qmd query --no-rerank` rerun on a miss or likely paraphrase, full `qmd query` only when ranking quality matters. bc-wiki-maintain's and the generated vault block's `qmd query` bans are narrowed to inline reads (migration line added for old vaults). The accuracy check covers the figures only (`qmd search` scope). Round 2 paraphrase rerun PASSED 2/2 on Haiku 5.5 low (owner-approved substitute for Terra): search-first answered in 41–44s vs 167–237s for the old body (`concepts/bc-qmd/tests/grep-baseline-results-2026-11-28.md`). bc-wiki-maintain read-path scenario 5 failed in both arms (every run read the whole vault), so it predates this change; filed as its own work item. Moved onto master without 055 by owner choice (2026-11-28).
