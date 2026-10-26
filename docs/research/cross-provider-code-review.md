# Research: does a code reviewer need to come from a different model provider?

Date: 2026-10-26. Question from the owner: when a builder agent writes code and a **fresh** reviewer agent (new session, given the diff and spec, not the builder's conversation) reviews it, does it matter materially whether the reviewer comes from a different model family or provider?

## Answer

Not much. Provider diversity is a second-order hedge. What moves review quality more, in roughly this order:

1. **An executed check** — tests, a repro, a type checker. Largest effect wherever it was measured.
2. **Keeping the builder's reasoning away from the reviewer** — no chat history, self-justification, or PR sales pitch.
3. **A reviewer at least as capable as the builder.** A weaker reviewer can make good code worse.
4. **A second independent review**, with findings unioned. Here a different provider is a reasonable way to make the second review find *different* bugs.

A fresh session already removes the conversational anchoring that makes an in-thread self-review uncritical. It does not remove every same-model bias, but in the code-review studies that test the owner's exact question, the residual effect of switching provider was small, inconsistent, or absent.

Where a different family still clearly earns its place: **grading and evaluation** (LLM-as-judge, benchmark admission), where same-family judges are measurably biased toward their own outputs.

## Evidence

Numbers marked ✔ were checked against fetched source text (Song and Zhang by targeted text search, the others also by an independent reviewer); the rest come from the researcher reports in [evidence/](cross-provider-code-review/evidence/) and are unverified.

### Why the assumption was plausible

- **Self-preference survives a fresh session.** The judge studies already judge in a new prompt with no generation history and still find bias: GPT-4 identified its own summaries with 73.5% accuracy and, as a separate correlated measure, preferred them (Panickssery, Bowman, Feng, NeurIPS 2024, <https://arxiv.org/abs/2404.13076>); Wataoka et al. (ICLR 2025, <https://arxiv.org/abs/2410.21819>) attribute it to low-perplexity familiarity rather than explicit self-recognition. Neither is code.
- **Errors are correlated, more so within a provider.** Kim et al., *Correlated Errors in Large Language Models* (ICML 2025, <https://arxiv.org/abs/2506.07962>): same developer, architecture, and size all raise error agreement.

### Why it does not hold up as a requirement

- **Cross-provider pairs still share mistakes, and more as models improve.** Kim et al.: "larger and more accurate models have highly correlated errors, even with distinct architectures and providers" ✔. Goel et al., *Great Models Think Alike* (ICML 2025, <https://arxiv.org/abs/2502.04313>): mistake overlap rises with capability.
- **On code, most self-preference is deserved.** Chen et al., *Do LLM Evaluators Prefer Themselves for a Reason?* (preprint 2025, <https://arxiv.org/abs/2504.03846>), on MBPP+ with executable ground truth: stronger models prefer their own answers mostly because those answers are better ✔ (framing). The harmful remainder is concentrated where the builder is wrong (reported 50–75% harmful self-preference for large models; unverified).

### Code-review studies that test the question directly

| Study | Setup | Result |
|---|---|---|
| Stephens, *Fresh Eyes Beat a Second Family* (2026, preregistered replay of a real agent pipeline, <https://stephens.page/blog/fresh-eyes-beat-a-second-family/>) — closest to this setup | Fresh same-family reviewer vs other-family reviewer on escaped bugs and whole-feature specs | Other family caught 1 of 6 escaped timing bugs; fresh same-family caught the same one ✔. After whole-feature review, other family found missed bugs in 16 of 30 features, fresh same-family in 19 ✔: "The second review is what made the difference, not the other family." The pipeline's own reviews had raised 2 of the 6 bugs and the authors declined both ✔. |
| Song, *When Does a Second Model Help?* (preprint 2026, <https://arxiv.org/html/2610.01471>) — planted errors | One review vs two | One cross-model review not significantly better than one fresh same-model review. One of each caught 56.7% vs 42.7% for two same-model reviews ✔, but not significantly more than two reviews by the stronger cross-model reviewer, so diversity and capability are not separated ✔. |
| Zhang, Zhang, Xu, *Cross-Model LLM Code Review* (preprint 2026, <https://arxiv.org/html/2607.21656>) — LiveCodeBench, reviewer rewrites | Same vs cross reviewer, both directions | Claude Opus 4.7 reviewing GPT-5.5 drafts: 71.6% → 89.7%; GPT-5.5 self-review: 84.5% ✔. GPT-5.5 reviewing Claude drafts: 91.4% → 82.8%, a regression; Claude self-review unchanged ✔. Reviewer strength decided it. |
| Greptile, *Models are worse at reviewing their own code* (vendor blog 2026, <https://www.greptile.com/blog/model-inversion>) — 1,000 real PRs | Same vs cross `/review` | High-severity recall: cross 60.0% / 62.0%, same 53.7% / 50.5% ✔ (about +9 points). Strongest pro-diversity number, but not peer-reviewed, uses an LLM judge for ground truth, confounds family with capability, and the vendor sells cross-model routing. |

### Levers that outweigh provider

- **Builder rationale contaminates review.** *Don't Judge Code by Its Cover* (preprint 2025, <https://arxiv.org/abs/2505.16222>): authority and self-declared-correctness comments shifted GPT-4o code verdicts, up to −26.7 points. Sycophancy toward a stated view appears in every model family tested (Sharma et al., ICLR 2024, <https://arxiv.org/abs/2310.13548>).
- **Unaided self-critique is weak; external signals work.** Huang et al. (ICLR 2024, <https://arxiv.org/abs/2310.01798>); Kamoi et al. survey (TACL 2024, <https://aclanthology.org/2024.tacl-1.78/>); Olausson et al. (ICLR 2024, <https://arxiv.org/abs/2306.09896>): even with failing tests, the model's own feedback is the bottleneck, and a stronger feedback model helps more.
- **Executed checks beat reviewer identity.** Guo et al., *Groundability, Not Scale Alone* (preprint 2026, <https://arxiv.org/html/2610.01023>): with official test evidence, small reviewers audit strong agents; reviewer size is not a consistent predictor.
- **Reviewers over-flag.** Jin & Chen (ASE 2026, <https://arxiv.org/abs/2603.00539>): GPT-4o rejected 73–88% of correct code when asked to explain and propose fixes. A foreign reviewer is not automatically "stricter in a good way."

### Owner's local benchmarks

No local run compares same-provider vs cross-provider reviewers on the same unchanged code. What exists cuts against a provider rule: in the 2026-09-30 routing cohort the best reviewer was OpenAI Sol at 94% vs xAI Grok at 79%, on a mixed-author fixture set (not a paired builder-provider test); in the 2026-09-28 review benchmark, Meta and xAI reviewers missed the same two bugs in every run.

## Limits

- No peer-reviewed study crosses builder family × reviewer family × fresh vs in-thread × tests vs none on the same corpus. The 2026 code studies are preprints, a vendor blog, and one preregistered replay with one session per cell.
- Self-preference papers are mostly GPT-3.5/4-era and not code.
- Model capability and provider are confounded in almost every comparison.

## Applied

Global agent instructions now require fresh context, withheld builder reasoning, no worker-only model upgrades, and executed checks for must-fix findings where feasible; cross-provider is a preference for the second review of high-risk work. Benchmark admission keeps its cross-family gate because it is grading, not review.

## Evidence files

- [evidence/self-preference-and-self-correction.md](cross-provider-code-review/evidence/self-preference-and-self-correction.md) — researcher report: self-preference, self-correction, sycophancy.
- [evidence/correlated-errors-and-cross-model-review.md](cross-provider-code-review/evidence/correlated-errors-and-cross-model-review.md) — researcher report: correlated errors, debate/ensembles, code-review studies, lever comparison.
