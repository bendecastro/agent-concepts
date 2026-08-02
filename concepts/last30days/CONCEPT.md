# last30days

Reference skill for `/last30days`: an agent-led recent-research workflow that searches and synthesizes what people are saying about a topic across social/community/market sources such as Reddit, X, YouTube, TikTok, Hacker News, Polymarket, GitHub, and web search. Its core value is recency plus engagement-weighted evidence, not generic web summarization.

## Requirements

The upstream `last30days` plugin, installed through its own channel (`npx skills add`
or the Claude Code plugin marketplace). The skill is coupled to a Python engine that
ships with it; the Markdown alone does nothing.

## Design decision: no vendored body (upstream-maintained)

This concept has **no local runtime skill body**, on purpose. The upstream skill is a large Agent Skills package whose `SKILL.md` is tightly coupled to Python engine scripts, assets, fixtures, and install/update mechanics.

- **Canonical body:** the installed upstream package/plugin, not `concepts/last30days/body/`.
- **Install/update path:** use upstream's supported install channel, currently either Claude Code plugin marketplace (`/plugin marketplace add mvanhorn/last30days-skill` then `/plugin install last30days`) or Agent Skills (`npx skills add mvanhorn/last30days-skill -g`). Re-run/update through that channel when upstream changes.
- **Canon gate note:** do not hand-edit an installed copy or transplant only `SKILL.md` into this workspace. The instruction contract invokes bundled scripts and assumes the full upstream package layout.
- **Deployment status here:** not deployed from this workspace. If the user wants `/last30days` available in a harness, install the upstream package/plugin rather than symlinking this concept.

## Provenance

- [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) — immutable snapshot of upstream `SKILL.md` v3.3.2 at commit `122158415ae421da83e739f2668032f6bc78d39c`, with source metadata. Reference only; never deploy from it.
- Upstream: https://github.com/mvanhorn/last30days-skill (MIT).

## Tests

Reference concept with no runtime gates of ours; per the test gate only an accuracy check applies. The local check verifies the snapshot metadata and the deliberate no-vendored-body decision. Runtime correctness belongs upstream and should be validated by the upstream test suite/package when changing that project.
