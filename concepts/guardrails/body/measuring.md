# Measuring and noise

Use this when setting a limit from a measurement, tightening one after an improvement, or deciding whether a change made something worse. `bc-autoresearch-loop` uses the same method to decide whether an improvement is real.

## What to measure

- One number per limit, on a fixed input: median wall time, peak memory, bytes after compression, number of dependencies, frames over budget in a fixed scene. Write down the input and the command so the next agent measures the same thing.
- Static and artifact measures (counts, bytes) usually have no noise: one run is enough, and the allowance can be zero.
- Dynamic measures (time, memory, frames) vary between runs. Measure them on the machine that runs the gate, because a limit measured elsewhere does not hold there.

## How many runs

Run the measurement at least 10 times after one warm-up run you discard. Take the median as today's value. Note the spread: drop the fastest and slowest tenth of the runs (at least one each), then take the slowest minus the fastest of the rest. If the spread is more than about a tenth of the median, the measurement is too noisy for a limit: make the input larger, close other work, or measure something steadier (count operations or allocations instead of time) before setting a limit. Why: a limit inside the noise either fails at random, so people stop trusting it, or is set so loose that real slowdowns pass.

## Setting the limit (ratchet)

Limit = today's median + noise allowance. Use the spread you measured as the allowance, rounded up to a plain number, and never less than zero. Anything worse than the limit fails the check. In the check, take the median of several runs rather than one run, so one slow run does not fail the gate.

This is a ratchet: it accepts what the project already is and stops it getting worse. When an improvement is verified (median clearly better than the limit, across fresh runs), lower the limit to the new median plus the allowance in the same commit.

## Recording

On the guardrails page, the source of a measured limit is the date, the run count, the median and the allowance, for example "agent's choice, measured 2026-11-25: 10 runs, median 412 ms, allowance 30 ms".

## Sources

- Benchmark regression testing compares against a reference with a tolerance for variability; [CodSpeed per-benchmark regression thresholds](https://codspeed.io/changelog/2025-10-31-per-benchmark-regression-thresholds).
- The ratchet (tolerate existing debt, reject new deterioration) is the same idea as [Spotless ratchet](https://github.com/diffplug/spotless/blob/main/plugin-gradle/README.md#ratchet), applied to a number.
- Run counts and the noise threshold above are this method's defaults, not a published standard; record them as the agent's choice.
