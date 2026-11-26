# Docs and skill references a stranger can follow

Why: `docs/guides/pipeline.md` still describes the old `.bc-agent/` vault layout; setup names `naming-things`, which is not deployed; wiki search needs `$AGENT_CONCEPTS`, set only for a contributor checkout; code projects skip the search indexing and wiki lint setup describes.
Done when: The pipeline guide matches the visible layout; setup either deploys its named skills or states a fallback; wiki search resolves its script without `$AGENT_CONCEPTS`; setup's indexing and lint steps say plainly which archetypes they apply to.
Stage: later
Blocked by: nothing
Kind: docs
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state

## Steps

- [ ] Rewrite the layout parts of the pipeline guide.
- [ ] Resolve the `naming-things` reference (test and deploy, or fallback wording).
- [ ] Script path resolution relative to the installed skill.
- [ ] Clarify indexing and wiki-lint scope in setup; lint green.

## Outcome

