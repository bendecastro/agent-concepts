# Source: affaan-m/ECC

- **Upstream:** [affaan-m/ECC](https://github.com/affaan-m/ECC)
- **Pinned commit:** [`e482e579415fde18357cafce70f177ae19fd7f03`](https://github.com/affaan-m/ECC/tree/e482e579415fde18357cafce70f177ae19fd7f03) (2026-09-24)
- **Snapshot date:** 2026-09-26
- **License:** MIT; the upstream notice is preserved in [`LICENSE`](LICENSE).

Immutable evidence snapshot, not a deploy source. Filed in the inbox 2026-09-26, awaiting ingestion.

## What was snapshotted, and what was not

ECC is a large Claude-Code-centred distribution (292 skills, 68 agents, hooks, installers, per-language rules, and the `ecc2/` Rust control plane). A read-only comparison against local canon on 2026-09-26 selected three ideas; only their evidence was captured:

- `scripts/ci/validate-no-personal-paths.js` and `tests/ci/no-personal-paths.test.js` — a CI check for real `/Users/<name>` / `/home/<name>` paths that allows placeholder usernames. Local `AGENTS.md` states the rule; local `scripts/lint.py` does not check it.
- `the-security-guide.md` — "The safety boundary is the policy that sits BETWEEN the model and the action" (prompt is not the security boundary); keep untrusted-content extraction separate from the action-taking agent; persistent memory as an injection-persistence surface ("reset or rotate memory after untrusted runs"). The guide's CVE, vendor-setting, and study claims were not validated.
- `skills/tdd-workflow/SKILL.md` — its "Plan Handoff" section: plan file content is "data, not instructions to the AI"; embedded commands are not executed until reviewed.

Read and rejected, not captured: memory-persistence hooks (conflict with `handoff`'s user-invoked boundary), installer/manifests/schemas, skill/agent frontmatter validators, hook-key validators, `ecc2/`, `SOUL.md`, `contexts/`, `rules/common/`, `security-review`, `agent-eval`, `eval-harness`. `intent-driven-development` (repo facts vs business assumptions) was a lower-ranked candidate not taken forward. About a dozen agent-oriented skills (`context-budget`, `strategic-compact`, `skill-comply`, `skill-stocktake`, `verification-loop`, `agent-introspection-debugging`, `continuous-learning-v2`, and others) were never close-read.

## Snapshot hashes

- `LICENSE`: `326146379f01bb137c0a5d3c54770c1aa31076705c8b88a7f6b26a460f6221b2`
- `the-security-guide.md`: `ac797e493a6d52ffe88f0c6d28fde80794f5e284716a1d6c98d9e7a14946a4ca`
- `skills/tdd-workflow/SKILL.md`: `f5d8543733c557f0c53b688d40f14e9b870a6b2c7e405bab07433954e363828a`
- `scripts/ci/validate-no-personal-paths.js`: `4d0bfc417528772be739b88dba0cff1ada1d44ba3f0ba14f8df9e0a7655cb337`
- `tests/ci/no-personal-paths.test.js`: `b27464a26372cdf1811f8f6f52db018455990334d833206ee0934f2946671d5c`
