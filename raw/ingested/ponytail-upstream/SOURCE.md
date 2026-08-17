# Source: DietrichGebert/ponytail

- **Upstream:** [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)
- **Pinned commit:** [`2ed6c52c9d7e5e56942508591085fd45dea277d3`](https://github.com/DietrichGebert/ponytail/tree/2ed6c52c9d7e5e56942508591085fd45dea277d3) (2026-08-07)
- **Snapshot date:** 2026-08-17
- **License:** MIT; the upstream notice is preserved in [`LICENSE`](LICENSE).

Immutable evidence snapshot, not a deploy source. Ingested → [`concepts/minimal-solution-ladder`](../../../concepts/minimal-solution-ladder/CONCEPT.md).

## What was snapshotted, and what was not

The upstream repository is roughly 95% distribution machinery: plugin manifests for ~20 harnesses, lifecycle hooks, an MCP server, a statusline, a Pi extension, and a promptfoo benchmark suite. None of that is evidence for the *instruction* being adapted, and this workspace deploys skills by symlink, so it was deliberately not captured.

Snapshotted:

- `LICENSE`, `README.md` — licence and the claims/positioning being cited.
- `AGENTS.md` — upstream's own condensed always-on rule file; the closest upstream analogue to a kernel delta, and useful evidence for the persistence design decision.
- `skills/ponytail/SKILL.md` — the primary body the concept adapts.
- `skills/ponytail-{audit,debt,gain,review,help}/SKILL.md` — the five companion skills, kept so the decision *not* to adapt them stays auditable.
- `benchmark-2026-06-18-agentic.md` — upstream's agentic benchmark writeup (copied from `benchmarks/results/`), the source of the headline effect sizes and of the retraction of the earlier single-shot figures.

## Snapshot hashes

- `LICENSE`: `fb1bc6909ac3ef82d5c22106e32ef682b0cff66788fa915fb9b53b15c9d2f3ab`
- `README.md`: `03432a62c4f08b4312f7f85fd7349d6510c765e3bc94608df0b28e9f752e9a15`
- `AGENTS.md`: `b57f736a83ddab7111d752008c3e131a157e646a6b47c9eb223f076c494685a8`
- `benchmark-2026-06-18-agentic.md`: `fe274964a4f2b9801e67ba956eef3a029c472aa5693b7e0643c83bd406f9ee6f`
- `skills/ponytail/SKILL.md`: `1316a2f3f95741d2300b116fe0c2d81ce4a9568656ed0a62643f54aaf09957f2`
- `skills/ponytail-audit/SKILL.md`: `5560b8e383dbe2ddfddc873a1e2bf2e586e23e0cd7d995537482b2315331f6d1`
- `skills/ponytail-debt/SKILL.md`: `c84fba75f0ca12bfe83f9a78ea02fd125c5dd3f1fbb18124105a489937f284e6`
- `skills/ponytail-gain/SKILL.md`: `24e01d1c9715cb136ba1c4f1e52a95940c0193558b876828e537736480d6408b`
- `skills/ponytail-help/SKILL.md`: `2264d1615117b02b0fd5a69ec84cd2757006471a78e4d6c22eed6d581c1d37a4`
- `skills/ponytail-review/SKILL.md`: `40df33b58fc6ef889b93585733feb9566b76e9586efa7f376785c1e995197ac0`
