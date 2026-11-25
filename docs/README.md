# Docs

Pages for people working on this workspace. Instructions an agent must follow live in concept
bodies and `AGENTS.md`, not here. Plans and other pending work live in [`../work/`](../work/README.md).

- [guides/harnesses.md](guides/harnesses.md) — which agent harnesses can use the concepts, and how each one is deployed or bootstrapped.
- [guides/bootstrap.md](guides/bootstrap.md) — prompts to paste into a session so a harness without native skill loading reads this workspace.
- [guides/install-packs.md](guides/install-packs.md) — generated `npx skills` commands: every public skill, or one ready-made pack with the skills it needs.
- [guides/pipeline.md](guides/pipeline.md) — how the plan-to-ship skills fit together, from a grilled idea to landed code.
- [guides/pressure-test-harness.md](guides/pressure-test-harness.md) — how to run a pressure test of a concept with Pi: hiding deployed skills, flags, headless pitfalls.
- [examples/](examples/) — templates for the optional private config files under `~/.config/agent-concepts/` (kernel copies, skill copies, pressure-test model, personal-terms denylist). Copy one there and fill it in. The publish policy template stays in [`../policies/`](../policies/publish.example.yaml).
- [status.md](status.md) — generated board of what is untested, undeployed or passing with a known gap. Do not edit it; run `python3 scripts/lint.py --write-status`.
- [research/](research/README.md) — dated investigation folders, plus `research/raw/`, the immutable source inbox.
- `decisions/` — numbered decision records, one per file, for hard-to-reverse choices (none yet).
- [design/](design/README.md) — how the product looks and behaves now, read before changing anything a user sees.
