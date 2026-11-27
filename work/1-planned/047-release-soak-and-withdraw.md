# Releases reach strangers only after a soak, and a bad one can be pulled back

Why: Agents release without asking, the npm install is unpinned and the Pi package loads the kernel into every session, so a bad agent-written release reaches every stranger at once; the only written remedy is "release the next patch".
Done when: A tagged release lands on npm's `next` dist-tag, moves to `latest` only after the stranger end-to-end test passes on that version, and `docs/guides/releasing.md` has a bad-release procedure (deprecate, move `latest` back, release note, CHANGELOG entry) that has been dry-run.
Stage: now
Blocked by: nothing
Kind: release
Source: blind-spot council, owner decisions 2026-11-27 (1a: soak on next, agents keep releasing without asking)
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Requirements

- `release.yml`'s `publish-npm` job publishes with `--tag next`; `latest` moves only by the promotion step.
- Promotion runs after `STRANGER_SOURCE=pack scripts/stranger_end_to_end.sh` (or an npm-installed variant of it) passes for that version. Check first, from docs.npmjs.com, whether `npm dist-tag add` works under trusted publishing (OIDC) without a stored token. If it needs a token or the owner's two-factor approval, stop and ask the owner how promotion should be authorized before building it; do not add a token.
- "Bad release" section in `docs/guides/releasing.md`: `npm deprecate agent-concepts@X "<reason; use Y>"`, move `latest` back to the last good version, a GitHub release note, and a CHANGELOG "Withdrawn" line; decision 0002 and AGENTS.md's Release operation name the soak.
- README: say that `pi install npm:agent-concepts` follows `latest`, and how to try `next`.

## Steps

- [ ] Publish to `next`, promote to `latest` after the stranger test, and document a bad-release procedure. Done when a test version goes to `next` and is promoted (or the owner has chosen the promotion authorization), and the bad-release steps are run once against a throwaway prerelease or reviewed line by line against npm docs. Out of scope: Claude Code and Codex plugin channels.

## Outcome

_To be filled when finished or dropped._
