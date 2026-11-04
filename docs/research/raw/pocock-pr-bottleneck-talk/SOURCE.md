# Source: Matt Pocock — "Fixing the PR Bottleneck" (AI Engineer Paris 2026)

- **Video:** [youtube.com/watch?v=LlgiOCmFG_w](https://www.youtube.com/watch?v=LlgiOCmFG_w) (AI Engineer channel, ~22 min; talk given 2026-09-24)
- **Transcript used:** third-party ASR at [usetranscribe.io](https://www.usetranscribe.io/yt/LlgiOCmFG_w/pr-bottleneck-fix); official captions were not obtainable. Supporting: [Conffab live captions + slides](https://agents.conffab.com/aie-paris-26/live/keynotes/sessions/1790260200.md), [AI Engineer talk essay](https://ai.engineer/talks/LlgiOCmFG_w-fixing-pr-bottleneck).
- **Captured:** 2026-11-04. The transcript itself is not redistributed; [`research-notes.md`](research-notes.md) holds a researcher's timestamped condensation with short quotes, claims, and source links.

Immutable evidence snapshot, not a deploy source.

## Ideas taken forward (2026-11-04, owner's choice)

- "Checks can lie": three test failure modes — tautological (re-assert a constant), structure-sensitive (read source text instead of executing), cannot-fail (stubs remove the real failure modes). → `tdd`.
- "Merge danger" on PRs: one-way vs two-way door plus blast radius; always human-review one-way doors. → `code-review`.
- Visual explanation of changes via HumanLayer `show-me`. → new concept; source in [`../humanlayer-show-me/`](../humanlayer-show-me/SOURCE.md).

## Considered, not taken forward yet

- Keep coding standards out of the implementer; a separate reviewer context loads them.
- Reviewer commits fixes rather than comments (local design keeps reviewers read-only; `post-review-patcher` applies fixes).
- `/retro` skill (session/PR → new checks, standards, skill trims); his PR skill and skills v1.3.
