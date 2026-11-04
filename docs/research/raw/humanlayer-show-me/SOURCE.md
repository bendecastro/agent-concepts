# Source: humanlayer/skills — `show-me` (and `visual-pr`'s copy of it)

- **Upstream:** [humanlayer/skills](https://github.com/humanlayer/skills), plugin `show-me` v1.0.1
- **Pinned commit:** [`4d69d20f6e9b57b4fcf0d501ccfb1be961f0f329`](https://github.com/humanlayer/skills/tree/4d69d20f6e9b57b4fcf0d501ccfb1be961f0f329)
- **Snapshot date:** 2026-11-04
- **License:** MIT (© 2026 HumanLayer); the upstream notice is preserved in [`LICENSE`](LICENSE).
- **Author rationale:** Dex Horthy, [show-me blog post](https://www.humanlayer.com/blog/show-me-skill) (2026-08-12) — agent output is "pretty much unreadable" as walls of prose; use visuals for program design (types, signatures, call stacks) and post-hoc diff review. Not snapshotted.
- **Found via:** Matt Pocock's talk "Fixing the PR Bottleneck" (see [`../pocock-pr-bottleneck-talk/`](../pocock-pr-bottleneck-talk/SOURCE.md)), ~18:38.

Immutable evidence snapshot, not a deploy source.

## What was snapshotted

- `plugins/show-me/skills/show-me/SKILL.md` — the skill: smallest useful visual (pseudocode, call tree, component tree, shallow file tree, Mermaid, `diff` of those shapes, whole block, one focused HTML file opened for the user). User-invoked only (`disable-model-invocation: true`).
- `plugins/show-me/skills/show-me/agents/openai.yaml` — `allow_implicit_invocation: false` for Codex.
- `plugins/show-me/.claude-plugin/plugin.json` — version/licence metadata.
- `plugins/visual-pr/skills/visual-pr/SKILL.md` and `references/show-me.md` — HumanLayer's own PR skill copies show-me's shapes rather than invoking it, because user-only invocation blocks composition ([issue #12](https://github.com/humanlayer/skills/issues/12)).

## Snapshot hashes (sha256)

- `LICENSE`: `5f13c18ea00ea5c1384f41745feeca774079164f7f59a92e4ac0899ad217b26f`
- `plugins/show-me/skills/show-me/SKILL.md`: `434a2346cc95e313b0d367d477dda2e23ba642dd2181757415a09500664af100`
- `plugins/show-me/skills/show-me/agents/openai.yaml`: `a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94`
- `plugins/show-me/.claude-plugin/plugin.json`: `3daf5f7ee36d15043e79a336349d04fa7e9ab9906717224d62f4bca7c92058ef`
- `plugins/visual-pr/skills/visual-pr/SKILL.md`: `89df56774d8ec522bd0d0f03cd553dae5d70bff9364749874b5a0c0ae390eec0`
- `plugins/visual-pr/skills/visual-pr/references/show-me.md`: `968f25af5bce778c06826f5bc4540631c3eab3e067be0fe48b48552cc1664a1f`
