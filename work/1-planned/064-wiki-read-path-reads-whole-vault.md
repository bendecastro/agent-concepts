# bc-wiki-maintain read path stops reading the whole vault

Why: In the read-path pressure scenario 5 (qmd absent), all four Haiku runs opened every tracked page, including `index.md`, both with and without the 059 change; three dropped the `AGENT_CONCEPTS` branch from the block's `wiki_search.py` command and so found nothing, and one read everything after `wiki_search.py` ranked the right page first.
Done when: Read-path scenario 5 passes on the pressure-test model: the run uses `wiki_search.py` (or the bounded lexical fallback), opens only the candidate pages it verifies, and never reads `index.md` or the whole vault.
Stage: next
Blocked by: nothing
Kind: bug
Source: 059 Haiku rerun 2026-11-28 (`concepts/bc-wiki-maintain/tests/pressure-read-path-results-2026-11-28.md`)

## Steps

- [ ] Find why the command loses its `AGENT_CONCEPTS` branch and why a top-ranked hit still leads to a full read, then fix the read-path wording; rerun scenario 5 old vs new.

## Outcome

_To be filled when finished or dropped._
