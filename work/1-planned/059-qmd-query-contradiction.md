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

- [ ] Reconcile the rule in both bodies. Done when `rg "qmd query" concepts/*/body` shows no contradiction, lint passes, and bc-qmd's existing pressure scenario still holds.

## Outcome

_To be filled when finished or dropped._
