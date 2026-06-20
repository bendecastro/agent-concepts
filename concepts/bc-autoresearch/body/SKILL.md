---
name: bc-autoresearch
description: Improve code against an objective metric without regressing behavior — bounded, measured iterations that are kept only when correctness still holds AND the metric provably improved. Use when a task targets a measurable improvement (speed, size, memory, cost) or asks you to optimize.
---

# AutoResearch — bounded, gated improvement

Improve code along a measurable axis (speed, output size, memory, allocations, API calls, cost — anything objective) **without regressing behavior**, by making it impossible to keep a change that isn't proven better. This is a discipline, not a tool: it works in any repo, on its own terms.

**The core idea:** the *check* owns truth; you propose *bounded* changes; a change survives only if it proves **both** that correctness still holds **and** that the chosen metric improved enough to justify it. Anything else gets reverted.

## Before you touch code

1. **Name one metric.** A single, objective, reproducible number (median wall-time on a fixed input, output bytes, peak RSS, allocation count, request count, …). **If you cannot name an objective metric, STOP — do not optimize blind.** Say so and return; "looks cleaner/faster" is not a metric.
2. **Lock correctness.** Identify the check that must keep passing — the project's tests, or if they're thin, a concrete check you can re-run (output count, content hash, golden output, a regression test). **Fix any correctness bug first**, then establish the baseline against the corrected code.
3. **Baseline it.** Measure the metric on a fixed, representative input, enough runs to be stable (take a median; watch for noise). Write the number down. If the runtime is dominated by external tools, paid APIs, GPUs, or large model files, build a **dry-run / shadow** measurement first so iterations stay cheap and deterministic.

## The loop — one bounded change per iteration

1. **Target the biggest measured cost**, not a guess about where time goes.
2. **Make ONE bounded change** to one unit (one function / script / directly-related helper). No bundled rewrites.
3. **Re-run correctness.** If it breaks → **revert**; this change is done.
4. **Re-measure the metric.** If it didn't beat the baseline by your threshold → **revert**.
5. **Keep only if BOTH passed.** Record baseline → current → delta and the *kind* of win.
6. **Re-baseline** against the kept change and repeat while budget remains.

## Guards — the failure modes this exists to prevent

- **Don't "optimize" by deleting required output or skipping real work** — a faster program that does less is not a win.
- **Pair every scalar metric with a correctness check** — a faster wrong answer is a regression, not an improvement.
- **Distinguish overhead/dry-run wins from real-workload wins** — and say which one you got.
- **One bounded change per iteration** — so a regression is attributable and a revert is clean.
- **Correctness before performance, always** — never trade behavior for speed.
- **Stop on diminishing returns** — out of budget, or no change clears the threshold, is a valid stop, not a failure. Don't force a marginal win by loosening the correctness check.

## Recording

For each kept change, record (in the commit message and/or the issue comment): the **metric**, **baseline**, **current**, **delta/speedup**, the **win kind** (real workload vs dry-run/overhead), and the **correctness check that held**. A reader must be able to see what improved and trust that behavior didn't change.
