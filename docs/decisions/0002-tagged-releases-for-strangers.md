# 0002: Tagged releases for people outside the repository

Date: 2026-11-25
Status: accepted

## Context

Agents commit and push to `master` many times a day. Anything that installs from `master` gets work in progress, including mistakes caught only by later review.

## Decision

Install methods for people outside the repository point at tagged releases (`vMAJOR.MINOR.PATCH`). A release goes out only after the fresh-install test passes and the pressure tests of changed discipline skills hold. `CHANGELOG.md` lists each release's changes. The install docs show how to pin a version; updates use each agent's own update command. The owner and contributors keep using `master` through the clone-and-link script.

## Consequences

- Daily pushes do not reach users; a release is a deliberate step.
- Someone has to cut releases; a release that waits too long leaves users on old skills.
- Plugin and package descriptions carry the version and must match the tag.

## Alternatives considered

- Everyone tracks `master`: no release step, but every push reaches users at once.
- A hand-moved `stable` branch: lighter, but no version numbers to pin or compare and no changelog.
