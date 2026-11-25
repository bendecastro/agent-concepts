# Research: 60 fps and performance guardrails

## Summary

The supplied poteto post is about trusting agent work, not Electron performance. A separate poteto post does set a 60 fps target for a browser game; it describes lint and a download-size gate, but not a derived timing budget or FPS regression test. The industry term for breaking a user-facing target into smaller time allowances is **latency budget decomposition** (for animation, **frame budgeting**).

## Findings

1. **The supplied post.** The [URL](https://potibo.dev/en/post/2111133080526495985) loads. Its opening asks, “how do you trust your agents' work more?” and its prescription is to “make the easy thing the right thing.” It proposes an inverse pyramid: architecture/types/invariants first; automated checks next; prose for what cannot be enforced; human review last. It groups “lint rules, tests, CI, verification (eg TLA+)” under “static analysis”; the term is used more broadly here than in its technical definition. **Support:** direct text and interpretation. **Confidence:** high.

2. **Likely intended post.** Web search found a [different first-person poteto post](https://x.noodl3.net/poteto/status/2117043478140276847) (mirror; [original X post](https://x.com/poteto/status/2117043478140276847) returned 403). It is about a **browser game**, not Electron. “the bar is 60 fps with 500 enemies on a mid-range phone.” For per-frame/tick code marked `.hot.ts`, “a lint rule bans allocating in it (no object literals, closures, new, etc.)” to curb GC stutter. Separately, “the build fails if the first download goes over budget. it's about 124 KB gzipped right now” (reported size, not the cap). “bots play the game headless to tune each difficulty against target survival rates” describes difficulty tuning, not FPS testing. The author says “every time i found an issue in the code i asked bot to make a lint rule against it”: a way to catch known bad patterns, not proof of frame rate. No per-step millisecond budgets, FPS measurements, timing benchmarks, telemetry, or CI placement are reported. **Support:** direct text and interpretation. **Confidence:** high on the captured text; implementation not independently verified.

3. **Industry vocabulary** (direct support from first-party sources, high confidence unless noted):
   - **Performance budget:** limits on performance-related metrics such as load time, bytes, or requests. [Google web.dev](https://web.dev/articles/performance-budgets-101).
   - **Frame budget / RAIL:** Response, Animation, Idle, Load. At 60 Hz the frame interval is 1000/60 ≈ 16.67 ms. For animation RAIL rounds to ~16 ms and recommends ~10 ms for app work, allowing ~6 ms for browser rendering. A guideline, not a measurement of this game. [Google RAIL](https://web.dev/articles/rail).
   - **Latency budget decomposition:** assign phase ceilings within the end-to-end target; check the split against traces. [AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentperf01-bp01.html). For a frame, allocate the time among work on the critical path and leave slack (researcher inference; no poteto numbers).
   - **Core Web Vitals:** loading (LCP ≤ 2.5 s), interaction (INP ≤ 200 ms), visual stability (CLS ≤ 0.1), evaluated at p75 of page loads by device class. Not FPS. [Google Web Vitals](https://web.dev/articles/vitals).
   - **Benchmark regression testing:** rerun a workload and compare to a reference with a tolerance for variability; [CodSpeed](https://codspeed.io/changelog/2025-10-31-per-benchmark-regression-thresholds) supports per-benchmark thresholds. By contrast, [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md#assert) collects browser audits and can fail on configured absolute budgets.
   - **Architectural fitness function:** “an objective integrity assessment of some architectural characteristic(s),” which can use tests or metrics. [Building Evolutionary Architectures, authors’ précis](https://evolutionaryarchitecture.com/precis.html).
   - **Ratchet / baseline-and-no-regress:** tolerate existing debt while rejecting new deterioration; a numeric ratchet tightens the baseline after verified gains (interpretation). [Spotless](https://github.com/diffplug/spotless/blob/main/plugin-gradle/README.md#ratchet) illustrates a changed-file formatting ratchet, not a numeric timing ratchet.
   - **Bundle budget:** cap delivered artifact bytes, e.g. compressed startup chunks. [Size Limit](https://github.com/ai/size-limit) has byte-only checks and optional headless runtime measurement; don’t conflate them.
   - **Static vs dynamic analysis:** static inspects without executing the program under test; dynamic executes it. [FDA glossary, NBS/IEEE definitions](https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-guides/glossary-computer-system-software-development-terminology-895).

4. **Which checks belong where?** (Researcher synthesis, high confidence.)
   - **Static source/graph:** scope a lint rule to Electron main-process code and reject known sync I/O or sync IPC imports/calls; inspect dependency graphs or lockfiles for forbidden packages, counts, or weight proxies. [Electron](https://www.electronjs.org/docs/latest/tutorial/performance) advises avoiding blocking I/O; [ESLint `no-sync`](https://eslint.org/docs/latest/rules/no-sync) illustrates a naming-based rule, not complete detection.
   - **Artifact-only:** count built bundle or compressed bytes, including bundled dependency contributions. Build/compression tools execute, but the delivered app need not run. More precisely, this is an artifact check, not a source lint or a latency measurement.
   - **Dynamic:** benchmark startup, interaction latency, frame intervals/missed frames and GC pauses; use traces to attribute time and runtime telemetry to see the real device mix. CI can host either kind. An assertion over a saved trace is offline, but its evidence came from executing the app.

## Contradictions and missing evidence

The supplied URL and nearby 60 fps post do not support the Electron attribution. Searches did not verify any other poteto post documenting timing decomposition or FPS regression gates. Automated source-check assessment was inconclusive; RAIL, AWS, and Electron passages were inspected directly.

## Sources and next steps

Kept the two first-person texts and linked primary documentation above. Deprioritized third-party game and interview summaries once first-person material was available. If an Electron-specific write-up is essential, obtain its exact link or transcript before attributing any thresholds or gates.
