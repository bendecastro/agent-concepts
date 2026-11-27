# 0002: Tagged releases for people outside the repository

Date: 2026-11-25
Status: accepted

## Context

Agents commit and push to `master` many times a day. Anything that installs from `master` gets work in progress, including mistakes caught only by later review.

## Decision

Install methods for people outside the repository point at tagged releases (`vMAJOR.MINOR.PATCH`). A release goes out only after the fresh-install test passes and the pressure tests of changed discipline skills hold. `CHANGELOG.md` lists each release's changes. The install docs show how to pin a version; updates use each agent's own update command. The owner and contributors keep using `master` through the clone-and-link script.

Amended 2026-11-27: the Pi package is also published to npm as `agent-concepts` for each tag, and the README's Pi install is the unpinned `pi install npm:agent-concepts`, which `pi update` moves to each new release. Git tags remain for pinning (Pi skips pinned packages on update), and the other install methods still name the tag. Why: a tag-pinned Pi install never updated, so strangers stayed on their first release.

Amended 2026-11-27: each tag publishes to npm's `next` dist-tag; `latest`, which the unpinned install follows, moves to it only after the stranger end-to-end test passes on the published version, and a bad release is withdrawn by moving `latest` back and deprecating it (steps in `docs/guides/releasing.md`). Why: agents release without asking and the Pi package loads the agent kernel into every session, so without a soak one bad release would reach every stranger at once.

## Consequences

- Daily pushes do not reach users; a release is a deliberate step.
- Someone has to cut releases; a release that waits too long leaves users on old skills.
- Plugin and package descriptions carry the version and must match the tag.
- npm holds a copy of each release; a published version cannot be replaced, so a broken one is withdrawn (`latest` moved back, the version deprecated) and fixed by the next patch release.
- A release reaches npm users only after the soak: someone has to run the stranger test and promote it, or it stays on `next`.

## Alternatives considered

- Everyone tracks `master`: no release step, but every push reaches users at once.
- A hand-moved `stable` branch: lighter, but no version numbers to pin or compare and no changelog.
