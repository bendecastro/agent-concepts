# bc-wiki-maintain read path stops reading the whole vault

Why: In the read-path pressure scenario 5 (qmd absent), all four Haiku runs opened every tracked page, including `index.md`, both with and without the 059 change; three dropped the `AGENT_CONCEPTS` branch from the block's `wiki_search.py` command and so found nothing, and one read everything after `wiki_search.py` ranked the right page first.
Done when: Read-path scenario 5 passes on the pressure-test model: the run uses `wiki_search.py` (or the bounded lexical fallback), opens only the candidate pages it verifies, and never reads `index.md` or the whole vault.
Stage: next
Blocked by: nothing
Kind: bug
Source: 059 Haiku rerun 2026-11-28 (`concepts/bc-wiki-maintain/tests/pressure-read-path-results-2026-11-28.md`)
Planned: bc-plan-to-pipeline 2026-11-28
Ready for agent: yes
Dependencies: none new

## Requirements

- Owner decisions (2026-11-28): test on Haiku low (2a, the model all four failing runs used); wording first, and if Haiku still loses the `AGENT_CONCEPTS` branch the fix may replace that branch with one helper command whose output lists only the candidate pages (3a).
- The read path must never tell an agent to open `index.md` or every page after a ranked hit; verify the top candidates only.
- Test: read-path scenario 5 (qmd absent), Haiku low, 3 runs master vs 3 changed with a blind baseline, graded from artifacts (which files the run opened). Pass: changed 3/3 open only verified candidates and no `index.md`; master shows the failure at least once.
- Hold the changed skill text off master until the test passes.

## Steps

- [ ] Find why the command loses its `AGENT_CONCEPTS` branch and why a top-ranked hit still leads to a full read; fix the read-path wording (helper command only if wording alone fails).
- [ ] Rerun scenario 5 on Haiku low, master vs changed, 3 runs each; record results beside the existing read-path results.

## Outcome

_To be filled when finished or dropped._
