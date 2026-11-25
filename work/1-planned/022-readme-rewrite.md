# Rewrite the README as a plain reference

Why: the README opens with a pitch, overstates what lint and tests prove, and gives a stranger no map of the repository.
Done when: `README.md` says what the repo is, how to install it, where things are, the loop, the hard rules, authorization and credits, with every claim matching the code and using the glossary's terms.
Stage: next
Blocked by: 005-glossary
Kind: docs
Source: owner review of the README, 2026-11-25
Planned: owner chose a plain-reference rewrite after the glossary, 2026-11-25

## Steps

- [ ] Order for a stranger: what it is, prerequisites and supported harnesses (including Muse), install, repository map (`index.md`, `docs/README.md`, `docs/status.md`, `work/`, `scripts/gate`, CI, `.bc-agent/`, `glossary.md`), then the loop.
- [ ] Qualify claims: lint checks each concept's recorded test status, not that every rule was attacked; the wiki-search benchmark's token counts are bytes ÷ 4 estimates on one 20-question set.
- [ ] Describe the hard rules as `AGENTS.md` states them (canon covers derived outputs too; immutability covers all of `docs/research/raw/`), with the names item 004 settles.
- [ ] Cut promotional phrasing ("while you sleep", "makes you discover the loophole"); keep authorization, private concepts and provenance, shortened.
- [ ] Fact-check every remaining claim against the code (the 2026-11-25 scout check was partial), lint and gate green.

## Outcome

