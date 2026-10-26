# Cross-provider vs same-family LLM review: correlated errors and bug-finding

**Question:** For a coding-agent workflow (builder writes code; a *fresh* reviewer sees only the diff/spec, no shared conversation), does it matter materially if the reviewer is the same model family/provider as the builder vs a different provider?

**Hypothesis under test:** Errors/blind spots are correlated across LLMs (especially same-family); heterogeneous reviewers find more bugs than same-model reviewers. Cross-provider effect should be weighed against other levers (fresh context, tests/execution, stronger reviewer, multiple independent same-model passes, adversarial prompting).

**Date of this brief:** 2026-10-26.

**Legend:** PEER-REVIEWED | PREPRINT | BLOG-VENDOR | ANECDOTE

**How to read:** Each item states what was *measured*, numbers, setting (task, models, whether code), then **Evidence** vs **Inference**. Items that cut AGAINST the hypothesis are marked **AGAINST** with equal weight.

---

## 1. Correlated errors across LLMs (same-family vs cross-family; capability)

### 1.1 Kim, Garg, Peng, Garg — *Correlated Errors in Large Language Models* (ICML 2025)

- **Source:** Elliot Kim, Avi Garg, Kenny Peng, Nikhil Garg. ICML 2025. [arXiv:2506.07962](https://arxiv.org/abs/2506.07962) · [PMLR](https://proceedings.mlr.press/v267/kim25e.html)
- **Status:** PEER-REVIEWED
- **Measured:** Pairwise agreement *conditional on both models being wrong* (MCQ); residual correlation vs human labels on resume scoring. Regression of error-agreement on provider, architecture, size, accuracy.
- **Numbers:** HELM: pairs agree ~**60%** of the time when both incorrect (chance if wrong answers uniform ≈ **1/3**). Datasets: **349** HuggingFace models × 12,032 MCQs; **71** HELM models × 14,042 MCQs; **20** models × 1,800 resume–JD pairs. Same developer, same base architecture, and similar size all associated with higher error agreement. After conditioning on those, **more accurate pairs still have more correlated errors**. Authors: “larger and more accurate models have highly correlated errors, **even with distinct architectures and providers**.” LLM-as-judge: judges inflate accuracy of weaker models, especially same-provider (red dots in Fig. 2).
- **Setting:** Not code. Leaderboard MCQ + resume screening. Mix of open and closed models through ~2024/early-2025 generations (not Opus 4.7 / GPT-5.5 coding agents).
- **Evidence:** Substantial *absolute* co-failure even across providers; extra correlation for same provider/architecture; correlation **grows with accuracy**.
- **Inference (not in paper):** Switching provider reduces correlation only partially. For frontier coding models, remaining cross-family overlap may still be large.

### 1.2 Goel et al. — *Great Models Think Alike and this Undermines AI Oversight* (ICML 2025)

- **Source:** Shashwat Goel, Joschka Strüber, Ilze Amanda Auzina, Karuna K Chandra, Ponnurangam Kumaraguru, Douwe Kiela, Ameya Prabhu, Matthias Bethge, Jonas Geiping. ICML 2025. [arXiv:2502.04313](https://arxiv.org/abs/2502.04313) · [PMLR](https://proceedings.mlr.press/v267/goel25b.html)
- **Status:** PEER-REVIEWED
- **Measured:** CAPA (κ_p): chance-adjusted probabilistic agreement on mistakes. LLM-as-judge affinity vs CAPA; weak-to-strong training gain vs CAPA; CAPA vs capability.
- **Numbers:**
  - LLM judges: **significant positive correlation** between judgment scores and CAPA **even on across-family pairs** (Fig. 3; all judges p<0.01). Using a different family as judge is **not** enough to remove affinity bias.
  - Weak-to-strong: 12 model pairs, 15 NLP tasks, 180 training runs. Gain vs similarity **r = −0.85**; after controlling for accuracy gap, **partial r = −0.35, p<0.01**. Complementary knowledge (not just elicitation) drives extra gain.
  - Capability trend (Sec. 5): **strong positive correlation** between capability and κ_p (similarity *beyond* chance agreement from accuracy). Trend stronger in instruction-tuned models; alternative architecture (Mamba) “may not be enough.”
- **Setting:** Not code. MMLU-Pro (8,707 items) + HELM/OpenLLM leaderboard + small-model W2S (1–3B teachers, 7–9B students). Pre-2025 frontier mix.
- **Evidence:** Blind spots overlap more as models get stronger. Oversight by a similar-capability model is systematically biased toward models that share mistakes. Diversity of *errors* predicts training/oversight value.
- **Inference:** Cross-provider review should help *more* when the two models’ error patterns differ, not merely when vendor names differ. Stronger frontier pairs may share more mistakes than weaker open-model pairs.

### 1.3 Panickssery, Bowman, Feng — *LLM Evaluators Recognize and Favor Their Own Generations* (ICML 2024)

- **Source:** Arjun Panickssery, Samuel R. Bowman, Shi Feng. ICML 2024. [arXiv:2404.13076](https://arxiv.org/abs/2404.13076)
- **Status:** PEER-REVIEWED
- **Measured:** Self-preference (own summaries scored higher than others’ of equal human quality) and self-recognition (distinguish own text).
- **Numbers:** GPT-3.5, GPT-4, Llama 2 all >50% self-recognition without fine-tune. **GPT-4 73.5%** accurate distinguishing itself from two other LLMs and humans. Linear correlation between self-recognition and self-preference after fine-tunes.
- **Setting:** Summarization (CNN/DailyMail, XSUM). **Not code.** GPT-3.5/4 / Llama 2 era.
- **Evidence:** Same-model *judge* is biased toward own *style/text*, not only toward shared task errors.
- **Inference:** Relevant to “does this model like its own PR?”; weaker evidence for “does it miss the same *bugs*?” Owner’s workflow already uses a fresh session (no authorship memory of the conversation), which removes one self-preference channel but not training-distribution / style preference.

### 1.4 Unverified / weak counter on residual correlation

- **Claim circulating:** After item-response (difficulty) adjustment, residual cross-family co-failure is near zero (*When Do Diverse Models Fail Together?*, future-shock.ai PDF). Fetch of [that PDF](https://www.future-shock.ai/research/when-models-fail-together.pdf) returned essentially empty content in this run, so **numbers are not verified here**. If true, it would be **AGAINST** treating raw 60% co-error as “shared blind spots” rather than “shared hard items.” Kim/Goel already chance-adjust in different ways (wrong-answer agreement vs CAPA); they still find extra-chance overlap.

---

## 2. Multi-agent debate / ensembles: heterogeneous vs homogeneous

### 2.1 Chen, Saha, Bansal — *ReConcile* (ACL 2024)

- **Source:** Justin Chih-Yao Chen, Swarnadeep Saha, Mohit Bansal. ACL 2024. [arXiv:2309.13007](https://arxiv.org/abs/2309.13007)
- **Status:** PEER-REVIEWED
- **Measured:** Round-table among **different families** vs 3-instance same-model debate (temp 1.0), self-consistency, self-refine. Ablation of multi-model component. BERTScore similarity of initial answers.
- **Numbers (100-sample subsets):** ChatGPT + Bard + Claude 2 vs strongest same-model debate: Date understanding **75.3% → 86.7% (+11.4)**; StrategyQA **71.3% → 79.0% (+7.7)**. Ablation: swapping three ChatGPTs for three different models **+6.8%** on StrategyQA (largest component). BERTScore similarity: paraphrases 0.9398; 3× ChatGPT 0.9102; three families **0.8739** (more diverse) with accuracy 72.2 vs **79.0**. MATH: +8% when adding a domain-specific math model (authors’ claim).
- **Setting:** Reasoning (StrategyQA, CSQA, GSM8K, AQuA, date). **Not code.** Models: ChatGPT / Bard / Claude 2 / GPT-4 / Llama-2-70B — **2023-era**. Homogeneous debate sometimes *hurt* (Bard×3, Claude×3).
- **Evidence:** Family diversity beat temperature diversity of one model, at that generation, on reasoning MCQ/short answers.
- **Caveat:** Compute not matched to “one strong model + extra samples.” GPT-4 GSM8K already high; math gains smaller until a specialist is added.

### 2.2 Du, Li, Torralba, Tenenbaum, Mordatch — *Multiagent Debate* (ICML 2024)

- **Source:** Yilun Du et al. ICML 2024. [arXiv:2305.14325](https://arxiv.org/abs/2305.14325) · [PMLR](https://proceedings.mlr.press/v235/du24e.html)
- **Status:** PEER-REVIEWED
- **Measured:** Multiple **instances of the same model** propose, critique, iterate. They note same-class instances still produce diverse answers; they “also investigate” mixed models.
- **Setting:** Math / strategy / factuality. GPT-3.5-class. **Not code.**
- **Evidence:** Homogeneous debate can still beat CoT/reflection *in their protocol*. Does **not** isolate family diversity as the driver.
- **Inference:** Debate gains ≠ proof that *provider* diversity is required.

### 2.3 Wang, Wang, Athiwaratkun, Zhang, Zou — *Mixture-of-Agents* (ICLR 2025 Spotlight)

- **Source:** Junlin Wang et al. ICLR 2025. [arXiv:2406.04692](https://arxiv.org/abs/2406.04692)
- **Status:** PEER-REVIEWED
- **Measured:** Layered aggregation of proposer outputs. For each width n: **single-proposer** (same LLM, T=0.7, n samples) vs **multiple-proposer** (different LLMs).
- **Numbers:** MoA of open models **65.1%** LC win on AlpacaEval 2.0 vs GPT-4o **57.5%** (+7.6). Authors: “using multiple different LLMs consistently yielded better results” than same-model proposers; scores rise monotonically with n. Table 3/4 hold the per-n numbers (image tables; exact per-n LC not extracted as text here).
- **Setting:** Chat preference (AlpacaEval, MT-Bench, FLASK). **Not code.** ~2024 open models + GPT-4o as aggregator in some plots.
- **Evidence:** Heterogeneous proposers > homogeneous sampling at matched width, on preference evals.
- **Caveat:** Preference win-rate ≠ bug recall. Later commentary (search hits) that same-model MoA variants can win in some replications — treat MoA diversity as **directionally supportive, not settled for code**.

### 2.4 Zhang et al. — *Stop Overvaluing Multi-Agent Debate* (2025)

- **Source:** Hangfan Zhang, Zhiyao Cui, Jianhao Chen, et al. [arXiv:2502.08788](https://arxiv.org/abs/2502.08788)
- **Status:** PREPRINT
- **Measured:** 5 MAD methods × 9 benchmarks × 4 foundation models vs CoT and self-consistency.
- **Numbers (abstract):** MAD **often fails to outperform CoT/SC** despite more inference compute. **Model heterogeneity** described as a “universal antidote” that consistently improves current MAD frameworks.
- **Setting:** Standard reasoning/fact benchmarks. **Not code.**
- **Evidence:** **AGAINST** “just add debate.” **FOR** heterogeneity *if* you already run multi-agent. Evaluation-practice paper; HTML body in this run was reference-heavy — treat “universal antidote” as authors’ summary, not a re-checked table.

### 2.5 Huang et al. — *LLMs Cannot Self-Correct Reasoning Yet* (ICLR 2024)

- **Source:** Jie Huang, Xinyun Chen, Swaroop Mishra, et al. (Google DeepMind). ICLR 2024. [arXiv:2310.01798](https://arxiv.org/abs/2310.01798)
- **Status:** PEER-REVIEWED
- **Measured:** *Intrinsic* self-correction: same model revises without external feedback.
- **Numbers:** Qualitative result in abstract: without external feedback, LLMs **struggle to self-correct** reasoning and **sometimes degrade**.
- **Setting:** Reasoning. GPT-3.5/4 era. **Not code.**
- **Evidence:** **AGAINST** same-conversation self-review as a quality lever. **FOR** an independent check *plus an external signal* (tests, spec, oracle). Does not compare same vs different provider.

---

## 3. Code-specific: cross-model review, critics, vendor tools

### 3.1 Greptile — *Models are worse at reviewing their own code* (2026)

- **Source:** Greptile. [Blog](https://www.greptile.com/blog/model-inversion)
- **Status:** BLOG-VENDOR (product motivation for “Model Inversion” routing)
- **Measured:** 500 Claude-authored PRs + 500 Codex-authored PRs; authorship from `Co-authored-by`, `[codex]` titles, `codex/` branches. ~1,500 verified high-severity comments (sentiment, votes, git archaeology). Claude Opus 4.7 and GPT-5.5 `/review`, **3 runs/PR**, recall vs GT with LLM-as-judge. Stylistic comments excluded.
- **Numbers (P0/P1 recall):**
  | Reviewer \ Author | Claude PRs | Codex PRs |
  |---|---|---|
  | Claude Opus 4.7 | **53.7%** same | **60.0%** cross |
  | GPT-5.5 | **62.0%** cross | **50.5%** same |
  Cross-model mean **61.0%** vs same-model mean **52.1%** (**+8.9 pp**). Bug-type mix differs: Claude PRs more “missing behavior” (35.1% vs 24.2%); Codex PRs more “semantic intent” (27.4% vs 21.4%). Reviewer strengths invert across those categories. Process: Opus ~7–8 comments, GPT ~1–2 until prompted to emit more.
- **Setting:** Real PRs, frontier coding agents **Opus 4.7 / GPT-5.5**. **Code.** Reviewer has repo tools (not the owner’s “diff/spec only” constraint).
- **Evidence:** Same-family review worse *in this vendor study* by ~9 pp high-sev recall; complementary checklists.
- **Caveats (important):** Not peer-reviewed; GT and matching use LLM-as-judge (circular with Goel/Kim judge-affinity); authorship labeling noisy; GPT initially under-commented so recall depends on prompting; **reviewer capability is confounded with family** (GPT stronger on Claude PRs, Opus stronger on Codex PRs — could be “other model is complementary” *or* “the other model is simply better at that bug class”). **Inference, not theirs:** 9 pp is a *medium* effect if it replicates, not a 2× effect.

### 3.2 Zhang, Zhang, Xu — *Cross-Model LLM Code Review* (LiveCodeBench; 2026)

- **Source:** Yike Zhang, YueMing Zhang, Hailu Xu. [arXiv:2607.21656](https://arxiv.org/html/2607.21656) (Agentic SE workshop 2026)
- **Status:** PREPRINT
- **Measured:** 116 recent **hard+medium** LiveCodeBench tasks; Claude Opus 4.7 vs Codex GPT-5.5; six conditions: two solos, two cross orderings, two same-model self-reviews. Reviewer sees problem + draft, **cannot run tests**. High reasoning effort. Pass rate of *final program after review* (reviewer rewrites, not just comments).
- **Numbers:**
  - Codex solo **71.6%** → Claude review **89.7%** (p_BH=.001); Codex self-review **84.5%** (p_BH=.022). Cross beats same-model self-review by **+5.2 pp** in this direction.
  - Claude solo **91.4%** → Codex review **82.8%** (p_BH=.046) **regression**; Claude self-review **unchanged at 91.4%**.
- **Setting:** Competitive-programming Python, post-cutoff problems. **Code**, static review. Frontier 2026 models.
- **Evidence:** **Mixed / partly AGAINST naive “always cross-review.”** Useful pairing is **asymmetric**: stronger/better writer should not be overwritten by a weaker reviewer. Cross-model helps when the reviewer is the *better coder* on that distribution. Same-model self-review of Codex still helped (+12.9 pp) without a second family.
- **Inference:** In owner’s workflow, “different provider” is dominated by “is the reviewer at least as strong, and does it *rewrite* or only comment?” This paper’s reviewer *replaces* the solution; a comment-only reviewer would show a different (likely smaller) effect.

### 3.3 Song — *When Does a Second Model Help?* (2026)

- **Source:** Song. [arXiv:2610.01471](https://arxiv.org/html/2610.01471)
- **Status:** PREPRINT (single-author; cites own prior CCR/D-CCR/HCCA preprints)
- **Measured:** 30 artifacts, **150 planted errors**, 10 conditions, **900 sessions**, 3 reviewer models from **2 developers**. Compares same-model fresh-session (CCR) vs cross-model (XMR); two-call unions; lightweight vs top-tier XMR; withholding requirements.
- **Numbers:**
  - Single top-tier XMR **not significantly different in F1** from CCR (does not establish equivalence).
  - Finding overlap Jaccard **41.2%** (partly different errors). Pairwise finding overlap **52.2% within same model vs 37–46% across models** (descriptive).
  - Two review calls: **CCR + XMR matches 56.7%** of planted errors vs **42.7% for two CCR** (Holm-adjusted **p=.006**). Gain vs **two top-tier XMR not significant** — **model difference and reviewer capability not separated**.
  - Lightweight cross-model reviewer **no higher** than same-model review.
  - After excluding one uncertain baseline run: CCR F1 **28.6%** vs same-context **27.1%** (**+1.5 pp, p=0.26, NS**). Earlier CCR paper’s significant result does not hold in the recomputed data.
  - Diachronic second round (same model): **false positives +62%**, no recall gain (from prior D-CCR, recomputed/cited).
- **Setting:** Mixed code + documents with **planted** errors. **Partly code.** Models from two developers (not named in the abstract slice).
- **Evidence:** **FOR** complementary coverage when you *union* same-model + other-model. **AGAINST** “one cross-model pass beats one fresh same-model pass.” **AGAINST** weak other-family reviewer. **AGAINST** extra rounds in the same session. Fresh context alone is a **tiny / NS** F1 bump here.
- **Caveat:** Planted errors ≠ production escaped bugs. Author’s earlier CCR claims are walked back in this paper.

### 3.4 Stephens — *Fresh Eyes Beat a Second Family* (Oct 2026)

- **Source:** Jacob Stephens. Blog + “research paper” PDF. [stephens.page](https://stephens.page/blog/fresh-eyes-beat-a-second-family/)
- **Status:** ANECDOTE / independent preregistered replay (not a venue paper). **Strongest direct analogue to owner’s factory.**
- **Measured:** thirdshift unattended pipeline. **183** replayed reviews, throwaway repos frozen at the reviewed commit, no tests/network/edits. Bars fixed before sessions. Fresh same-model control vs other family. Four checkpoints.
- **Numbers:**
  - **In-Run second opinion (6 escaped timing bugs):** Codex caught **1/6**; fresh Claude caught that same 1. Reverse: Claude on Codex-authored escapes **0/3**. Bar (other family catches ≥2 that fresh same-model misses) **failed**. Timing checklist: 4 catches with vs without, but **different** 4 (trade, not gain).
  - **Plan check:** Codex on Claude plans: 15 stops, **only 5 right** (fails). Fresh Claude: 10 stops, **8 right** (passes). Claude-max on Codex plans: 3 stops, 2 right (passes **at the bar**). Author reads this as **checker strength**, not family.
  - **After whole-feature Spec review (30 Specs):** Codex found real missed bugs in **16/30** (2/25 findings wrong); fresh Claude **19/30** (9/40 wrong). **Mostly different bugs** (Codex-only 13; Claude-only 23). Moving Spec review itself to Codex: 22 vs recorded Claude 23 — **swap does not add**.
  - Original in-session reviews had already **raised 2/6** timing bugs; **authors declined both**. Acting on findings (now: finding must include a test the author runs) judged as important as detection.
- **Setting:** Real agent PRs, **2026** Claude Opus 5.5 / GPT-6.1-class Codex / others. **Code.** Closest to owner’s “fresh reviewer on a factory.”
- **Evidence:** **AGAINST** “second family is what matters.” **FOR** a second *look* (especially after a whole feature) and for **reviewer strength / tests**. Complementary bugs still appear (union of families > either), but a second **fresh same-family** session captured as much as the other family at every preregistered checkpoint.
- **Caveats author owns:** Claude graded Claude; one session per cell (ties inside noise); factory moved to Codex mid-study.

### 3.5 SWE-PRBench — issue detection vs human PR comments (2026)

- **Source:** [arXiv:2603.26130](https://arxiv.org/html/2603.26130)
- **Status:** PREPRINT
- **Measured:** 350 human-annotated PRs; 8 frontier models; LLM-as-judge κ=0.75; configs: diff-only / +file / full context.
- **Numbers:** Models detect only **15–31%** of human-flagged issues (diff-only). **All 8 degrade** as context grows (attention dilution); structured ~2k-token diff+summary **beats** ~2.5k full context with execution/test signatures. Top four models statistically indistinguishable (s̄ 0.147–0.153).
- **Setting:** Human OSS review comments as GT. **Code.** Does **not** compare same vs other family as author.
- **Evidence:** Absolute AI review recall is **low**. Dumping more context (or even “execution context” in the prompt) is **not** a free win. Lever “give the reviewer more files” can **hurt**.

### 3.6 Guo et al. — *Groundability, Not Scale Alone* (2026)

- **Source:** [arXiv:2610.01023](https://arxiv.org/html/2610.01023)
- **Status:** PREPRINT
- **Measured:** When a *weaker* reviewer can audit a strong coding agent. 411 execution-labeled traces; 154 GPT-5.4 SWE-bench Lite/Verified traces (101 defective). Official tests as upper bound; generated tests as deployable cascade.
- **Numbers:** Official execution evidence: after freezing format, **5/6 reviewers improve both rates**; **2 classify every trace correctly**. Reviewer **size is not a consistent predictor**. Generated-test cascade on held-out GPT-5.4: coverage 0.89, risk 0.33, **catch 0.76**, **over-rejection 0.66**. “Producing equally reliable checks without official tests remains the main bottleneck.” 8B reviewer with **patch only** accepted all 9 target omissions.
- **Setting:** SWE-bench traces. **Code.**
- **Evidence:** **Execution/tests dominate model identity.** A weak reviewer with a checkable oracle can beat a strong reviewer staring at a diff. Generated tests still flood false rejects.

### 3.7 Olausson et al. (as summarized by Zhang et al. 2607.21656)

- **Source:** cited as Olausson et al. 2024 on self-repair; HumanEval/APPS; Code Llama, GPT-3.5, GPT-4.
- **Status:** PEER-REVIEWED (original; this brief did not re-fetch the PDF)
- **Measured (per Zhang et al.):** Same-model self-repair modest because feedback on *own* code is weak; **largest gains when a stronger model repairs a weaker model’s drafts**; human debugging >> self-feedback.
- **Setting:** Code generation + repair **with** execution in the original line of work.
- **Evidence:** Aligns with LiveCodeBench 2026: **reviewer strength > family match**.

### 3.8 Vendor / practice notes (weak evidence)

- **CodeRabbit:** describes evaluating multiple models on real PRs for coverage/precision/SNR/latency and using an **ensemble / task-specialized** stack, not a proven same-vs-cross A/B. BLOG-VENDOR. [CodeRabbit blog](https://www.coderabbit.ai/blog/behind-the-curtain-what-it-really-takes-to-bring-a-new-model-online-at-coderabbit)
- **Greptile Model Inversion:** ships cross-routing because of §3.1. BLOG-VENDOR.
- **OpenAI 2026 “cross-model review tooling”** mentioned by Song — not independently fetched here.
- **Anthropic Claude Code issue #72206** (pattern: spawn fresh sub-agent against author-blindness): **ANECDOTE**, argues structural independence of *session*, not provider.
- **SWE-bench LLM critics** (Amazon *code-agent-eval*, arXiv:2501.16655; SWE-Critix; ExecCritic; Agentic Rubrics): execution-free critics exist; none of the abstracts fetched here run a clean same-family vs cross-family critic ablation on SWE-bench.

### 3.9 Not used as evidence

- Zenodo “A Single LLM Is an Incomplete Code Reviewer” (18 artifacts, 154 issues, 8 models): title matches the hypothesis but was **not fully fetched**; n=18 is tiny. Omit pending read.
- “When Do Diverse Models Fail Together?” PDF: fetch failed.

---

## 4. Lever comparison (cross-provider vs the other knobs)

Relative size is **inference**, synthesizing the measurements above. Order is for *owner’s already-fresh, comment-style review*, not for rewriting LiveCodeBench solutions.

| Lever | What the evidence actually shows | Rough size | vs cross-provider |
|---|---|---|---|
| **Tests / execution / groundable checks** | Huang: no-feedback self-correct fails. Groundability: official tests make even weak reviewers work; patch-only 8B misses all planted omissions; generated tests catch ~0.76 but over-reject ~0.66. Stephens: declined findings were the escape, now forced via a failing test. | **Largest** when an oracle exists | Bigger than family swap |
| **Reviewer capability (stronger model)** | LiveCodeBench: Claude reviewing Codex +18.1 pp; Codex reviewing Claude **−8.6 pp**. Song: lightweight XMR useless. Stephens plan check: only max-effort strong checker passes. Olausson: stronger repairer of weaker draft. | **Large, can dominate family** | Usually larger |
| **Second independent pass (union of findings)** | Song: CCR+XMR 56.7% vs 2×CCR 42.7% planted. Stephens Spec: either second look hits >50% of features with *new* real bugs; the two families’ extra bugs barely overlap. ReConcile: diversity of answers. | **Medium**; union > either identity | Similar or larger than family-alone |
| **Fresh context (no builder conversation)** | Owner already does this. Song recomputed CCR vs same-context **+1.5 pp NS**. Huang/Panickssery still motivate not grading in-thread. Stephens: fresh same-model **matched** other family. | **Small–medium** for detection F1; large for avoiding sycophancy | Fresh same-model often ≈ other family |
| **Cross-provider / family** | Kim/Goel: extra same-provider correlation, but **high correlation remains across providers** and **grows with capability**. Greptile: **+8.9 pp** recall (vendor). LiveCodeBench: +5.2 pp only in the good direction; **harm** in the other. Stephens: **no incremental family effect** once fresh. Song: single XMR ≈ CCR. | **Small–medium, unreliable, asymmetric** | This row |
| **Multiple samples of the *same* model (self-consistency)** | ReConcile: 3× ChatGPT debate << 3 families. MoA: same-model proposers < heterogeneous. Song: 2×CCR < CCR+XMR. Du: same-model debate can still help vs CoT. Zhang 2502.08788: MAD often ≈ CoT/SC. | **Small** unless you union complementary detectors | Usually smaller than a *good* other-family pass; can match a *fresh* extra pass |
| **Adversarial / checklist prompting** | Stephens timing checklist: same count, **different bugs**, extra latency. Greptile: fighting GPT `/review` alignment to emit more comments is brittle. | **Small / unstable** | Smaller |
| **More repository context in the prompt** | SWE-PRBench: **monotonic drop** A→C; Type2 contextual detection collapses. | Can be **negative** | Do not spend here first |

**Owner-specific implication:** The workflow already takes the cheap independence lever (fresh reviewer, diff/spec only). The *incremental* question is family. Evidence says:

1. Do not expect a large, reliable lift from “Anthropic reviews OpenAI” as such.
2. Do expect **some complementary misses** (Greptile categories; Song Jaccard 41%; Stephens Spec-only bugs differ). Union of two reviews > one, whether or not the second is another family — but another family is a reasonable way to buy non-overlap.
3. Never put a **weaker** other-family model in a position to *rewrite* a stronger builder’s patch (LiveCodeBench −8.6 pp).
4. Spend first on **runnable checks** and **reviewer strength**, then on a second pass.

---

## 5. Contradictions (equal weight)

1. **Does family matter for code review?** Greptile **yes (~9 pp)**. Stephens **no** (fresh same-model ≥ other family). LiveCodeBench **only if the other model is the better coder**; otherwise **harm**. Song **not for a single pass**; **yes for two-pass union**, and even then capability is not separated.
2. **Are errors more correlated for stronger models?** Kim and Goel **yes** (MCQ/leaderboards). That predicts *shrinking* value of cross-family at the frontier. Greptile still sees a gap at Opus 4.7 / GPT-5.5. Not the same task (MCQ vs PR bugs).
3. **Is most co-failure just item difficulty?** Kim/Goel say leftover agreement after chance/accuracy adjustment is real. An unreproduced IRT paper claims residual ≈ 0. **Unresolved.**
4. **Does debate need heterogeneity?** ReConcile/MoA **yes**. Du **no** (same model enough vs CoT). Zhang 2502.08788: homogeneous MAD often **loses to CoT/SC**; heterogeneity rescues it.
5. **Fresh context:** theoretical/self-preference literature says it should matter a lot; Song’s recomputed CCR is **NS +1.5 pp**. Different tasks (planted mixed artifacts vs summarization/reasoning).

---

## 6. Missing evidence

- No **peer-reviewed**, **repo-level**, **comment-only** study that crosses builder family × reviewer family × fresh vs in-thread × tests vs no tests on the same SWE-bench-like corpus.
- Kim Table 1 **coefficients** (pp of extra agreement for same provider) are figures, not extracted as numbers here.
- MoA Table 3 exact LC win-rate for single- vs multi-proposer at each n.
- Olausson 2024 and Du mixed-model appendix not re-read as PDFs.
- CodeRabbit / Anthropic / OpenAI **internal** same-vs-cross A/Bs: not public.
- Transfer: 2023 ChatGPT/Claude 2 debate numbers **may not transfer** to 2026 reasoning models.
- Owner’s exact setup (fresh, diff/spec, no rewrite, no tests unless provided) is closest to **Song CCR vs XMR** and **Stephens**, not Greptile’s tool-using `/review`.

---

## 7. What the evidence shows vs inference

**Shows (high confidence):**
- LLM errors co-occur far above chance on MCQ leaderboards; same provider/architecture add more correlation; **accuracy still predicts correlation after that** (Kim, ICML 2025).
- Chance-adjusted mistake overlap **rises with capability**; judges favor similar-error models even across families (Goel, ICML 2025).
- Intrinsic self-review without an external signal is weak (Huang, ICLR 2024).
- On code, **reviewer strength and whether review can regress working code** can outweigh family (Zhang et al. LiveCodeBench 2026).
- A second *independent* look finds extra bugs; family is not uniquely required for that (Stephens 2026; Song 2026 two-call results).

**Shows (medium, code):**
- Vendor PR study: ~9 pp high-sev recall for cross vs same at Opus 4.7 / GPT-5.5 (Greptile).
- Planted-error study: one cross pass ≈ one fresh same-model pass; **two mixed passes > two same-model passes** (Song).

**Inference (researcher, not sources):**
- For the owner’s **already-fresh** reviewer, switching provider is **optional insurance**, not the main quality lever. Material when: (a) you **union** findings rather than pick one reviewer; (b) the other model is **at least as strong** and has a **different bug prior** (security vs missing behavior, etc.); (c) you will not let a weaker reviewer rewrite. Not material as a default identity swap. Tests + stronger reviewer + “must attach a failing check” are the higher-ROI moves.

---

## 8. Bottom line (5–10 lines)

Errors *are* correlated across LLMs: on HELM, co-wrong models pick the same wrong MCQ ~60% of the time vs ~33% chance, and **stronger models correlate more even across vendors** (Kim 2025; Goel 2025). Same-family adds extra overlap, but **cross-family is not independence**. For *code review*, the cleanest 2026 tests disagree: Greptile reports **~9 pp** high-sev recall for other-family `/review`; LiveCodeBench shows **+18 pp / −9 pp** depending on who reviews whom (strength and rewrite risk, not family per se); Stephens’s preregistered factory replay finds **fresh same-model ≥ other family** at every checkpoint. Given that the owner already uses a **fresh** reviewer, the incremental cross-provider effect is **small, asymmetric, and smaller than tests, reviewer strength, and a second independent pass**. Use another provider if it is cheap and comparably strong, and **union** comments rather than replace the builder; do not treat “different logo” as the quality strategy. Old GPT-3.5/Claude-2 debate gains (ReConcile +7–11 pp) should not be assumed for 2026 coding agents.

---

## Sources kept

- Kim et al., *Correlated Errors in Large Language Models*, ICML 2025. https://arxiv.org/abs/2506.07962
- Goel et al., *Great Models Think Alike and this Undermines AI Oversight*, ICML 2025. https://arxiv.org/abs/2502.04313
- Panickssery, Bowman, Feng, *LLM Evaluators Recognize and Favor Their Own Generations*, ICML 2024. https://arxiv.org/abs/2404.13076
- Chen, Saha, Bansal, *ReConcile*, ACL 2024. https://arxiv.org/abs/2309.13007
- Du et al., *Improving Factuality and Reasoning through Multiagent Debate*, ICML 2024. https://arxiv.org/abs/2305.14325
- Wang et al., *Mixture-of-Agents*, ICLR 2025. https://arxiv.org/abs/2406.04692
- Zhang et al., *Stop Overvaluing Multi-Agent Debate*, 2025. https://arxiv.org/abs/2502.08788
- Huang et al., *LLMs Cannot Self-Correct Reasoning Yet*, ICLR 2024. https://arxiv.org/abs/2310.01798
- Greptile, *Models are worse at reviewing their own code*, 2026. https://www.greptile.com/blog/model-inversion
- Zhang, Zhang, Xu, *Cross-Model LLM Code Review*, 2026. https://arxiv.org/html/2607.21656
- Song, *When Does a Second Model Help?*, 2026. https://arxiv.org/html/2610.01471
- Stephens, *Fresh Eyes Beat a Second Family*, 2026. https://stephens.page/blog/fresh-eyes-beat-a-second-family/
- SWE-PRBench, 2026. https://arxiv.org/html/2603.26130
- Guo et al., *Groundability, Not Scale Alone*, 2026. https://arxiv.org/html/2610.01023

## Sources deprioritized

- *When Do Diverse Models Fail Together?* (future-shock.ai PDF) — fetch empty; numbers unverified.
- Zenodo multi-family incomplete-reviewer study — not fully read; n=18.
- CodeRabbit vs Greptile SEO comparison pages — no primary data.
- Howardism reprint of Greptile numbers — secondary.
- MindPattern “10 judges ≈ 3.5” — blog, not fetched.
- Amazon code-agent-eval / SWE-Critix / ExecCritic — no same-vs-cross ablation in fetched abstracts.

## Next steps (if more research is needed)

1. Extract Kim Table 1 coefficients and Goel Fig. 6 CAPA-vs-capability slope from PDFs.
2. Read Olausson 2024 self-repair tables (HumanEval/APPS, stronger-repairs-weaker).
3. If deciding a default reviewer identity: A/B on *this* repo’s escaped bugs with frozen bars, copying Stephens’s fresh-same-model control — public papers will not settle the local mix.
