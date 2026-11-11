> Replaced by [`ui-design`](../../../concepts/ui-design/CONCEPT.md) on 2026-11-11; this document describes `frontend-design` at 171e5b1.

# Front-end design skill: Theo's UI hill climb

**Purpose:** Research and handoff for an agent improving a front-end design skill. This is evidence and a set of proposals, not a finished skill or authorization to deploy one.

**Context:** The owner wants agents to make better visual design decisions, inspired by Theo's iterative T3 Code redesign. Start by inspecting the existing `frontend-design` concept (`171e5b1:concepts/frontend-design/CONCEPT.md`) and skill body (`171e5b1:concepts/frontend-design/body/SKILL.md`), rather than assuming a new skill is needed. The companion [Shelfmark brief](brief.md) records local experience with incremental changes and real-browser verification. Reconcile its proposals with this research and ask the owner about material design choices before implementation.

## Evidence and corrections

The strongest accessible evidence is the T3 Code pull requests, not a transcript of the video:

- [Initial UI polish PR #24776](https://github.com/pingdotgg/t3code/pull/24776) describes the designer's complaint about fonts, corner radii, icons and hierarchy; token and primitive changes; before/after images; and three reported council rounds. The PR reports initial scores of 6, 6 and 6.5, rising to 9 from all three reviewers. One score was revised after a 1:1 crop revealed a screenshot-downscaling artifact, not a code defect.
- [Follow-up PR #24837](https://github.com/pingdotgg/t3code/pull/24837) reports five rounds, using fresh screenshots and comparisons against Claude Code and Codex desktop apps. In its final table Opus scored T3 9.0, Muse 7.9, and Sol 9.0. Muse scored Claude Code 8.1, so the PR does **not** show unanimous agreement that T3 beat both references. Scores are the PR author's reported model judgments, not independent user research or an objective measure of quality.
- The follow-up reports quieter sidebars, consistent composer controls, clearer details and settings, and darker light-mode status text. It documents screenshot conditions (macOS, 1280×832, seeded data) and shows dark, light, new-thread and settings captures. This makes comparisons more reproducible, but a screenshot set is not proof of accessibility or behavior.
- Theo's [X post](https://x.com/theo/status/2114280056784921048) is identified in search results with the text “Think I can turn T3 Code's UI into a hill climb for Opus?” X returned 403 when checked, so the thread and surrounding replies were not directly verified. The [video](https://www.youtube.com/watch?v=xq0eB8vxeqk) could not be extracted for direct review. Its details, including publication date, total runtime, number of all rounds, claims about a “jester,” and whether or when a beta shipped, remain unverified here. Do not repeat the earlier conversation's “18 hours,” “30+ rounds,” or unanimous-superiority claims as facts.
- The two PRs describe separate stages with different tables; do not add their round counts and present the result as the full experiment. Both PRs are marked closed in the source metadata; their status alone does not establish shipping.

Checked 2026-11-11. If the distinction matters to the skill, inspect the video, thread, linked commits and current product state directly; do not infer them from a model-generated summary.

## Principles worth testing in a skill

These are recommendations inferred from the evidence, not claims that Theo formulated a universal design system. Adapt them to the product and users; a busy professional tool and an expressive marketing page have different goals.

1. **Hierarchy follows the task.** Make the primary content and action easy to find; reduce competition from labels, metadata and less common controls. Test whether important text remains legible, not just whether it is visually prominent.
2. **Consistency is systematic, not sameness.** Reuse existing components, typography roles, spacing, icon treatment and theme tokens. Give different states and importance levels clear distinctions. When a shared token changes, inspect representative uses across surfaces and themes.
3. **Typography must render as intended.** Check real font availability, weights, line height, truncation, wrapping and platform differences. T3's choice of Inter was a response to its specific font-weight issue, not a universal font recommendation.
4. **Reduce noise without erasing affordances.** Remove redundant dividers and decorations when grouping and alignment carry the structure. Controls still need to look interactive; status and focus must remain apparent.
5. **Use color deliberately.** Reserve stronger color for emphasis and meaningful states where appropriate; avoid both indiscriminate saturation and a flat field where important information disappears. Do not rely on color alone to convey state.
6. **Design for real content and states.** Inspect long names, dense data, empty/loading/error states, disabled and focused controls, light and dark themes where supported, and narrow or resized windows. Examine clipping, wrapping, overflow and alignment.
7. **Respect context and intent.** For an established app, preserve its visual language and reuse its primitives unless redesign is requested. For new work, choose an intentional direction appropriate to the audience and task rather than applying a generic template. The owner makes consequential aesthetic or scope choices.
8. **Accessibility and behavior are constraints, not aesthetic scores.** Use semantic controls, keyboard access, visible focus and accessible names; check contrast and motion preferences as applicable. Screenshot review cannot establish these on its own. WCAG 2.2's [minimum text contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) explains the 4.5:1 normal-text and 3:1 large-text criteria and their exceptions; applicable conformance requirements depend on context.

The PR's 1.75 icon stroke, particular radius scale and font choices are **examples**, not default values to impose across products. PR #24776 and #24837 even describe their radius scales differently; inspect actual code before asserting exact values.

## Proposed visual improvement loop

Use a lightweight version for ordinary UI changes and a larger loop only when the task, available tools, budget and owner authorization support it. The steps below are a design proposal, not a claim that all were used in T3 Code.

1. **Frame:** Identify audience, task, constraints, affected surfaces, design system, intended visual direction and what must not regress. Determine what the owner wants changed and what is out of scope.
2. **Baseline:** Run the actual UI if feasible. Capture representative screens with stable seed data, viewport dimensions, theme, browser/host and revision recorded. Use the real host where sizing or behavior depends on it. Retain the baseline; redact sensitive data.
3. **Critique:** Inspect full-resolution images and, when useful, 1:1 crops. List specific, prioritized issues with locations, evidence, user impact and proposed changes. Distinguish clear defects from subjective preferences and questions for the owner.
4. **Change:** Address a coherent, bounded group of issues. Prefer existing components and shared tokens when their scope is appropriate. Do not silently redesign adjacent surfaces or copy competitors.
5. **Recheck:** Capture comparable after images, inspect them, and record what improved and what regressed. Also exercise interactions, keyboard behavior and accessibility; run relevant code checks. Screenshot-only evaluation cannot substitute for them.
6. **Stop:** Stop when the agreed issues are resolved and checks pass, or when further gains are speculative, the budget is exhausted, or tools/context are unavailable. Report remaining defects and missing evidence rather than claiming visual verification.

If repeat rounds are valuable, keep each capture and critique separate so a reviewer can compare them. Do not make an arbitrary number of rounds or an overall score the sole acceptance criterion. The local [Shelfmark brief](brief.md) proposes a mandatory two-round loop; whether that cost is justified for every visible change is an owner decision.

### Optional scoring and multiple reviewers

For a significant redesign, a fixed rubric can focus discussion: hierarchy, readability/contrast, consistency, task clarity, responsiveness and visual coherence. Describe what each category measures, inspect the same scenarios, record per-category evidence and disagreement, and use before/after comparisons under equivalent conditions. If using reference products, choose genuinely comparable workflows and document differences; they are inspiration, not automatic targets or sources to copy.

Scores are subjective and can drift with prompts, image scaling and model preferences. An increase is a clue, not proof of improvement; repeated optimization against the same judges can overfit their preferences. A model council adds cost and is not necessarily independent or representative of users. Preserve dissent, use distinct reviewers only when available and authorized, and seek human or real-user feedback when decisions warrant it. Never hide accessibility or functional failures behind a high aggregate score.

## Handoff decisions and checks

Before building, the next agent should:

- Read the existing concept, its tests and relationships, this note, and the Shelfmark brief. Identify what is already covered and which failures need a new instruction versus a reference, test or another skill. Follow the repository's concept lifecycle and authoring guidance.
- Ask the owner to resolve consequential choices: extend the current concept or create a complementary skill; the scope and minimum evidence for visual review; when optional independent/cross-model review is worth its cost; and how to handle environments where screenshots cannot be captured. Do not treat delegation or external model use as automatically authorized.
- Design pressure scenarios with observable outcomes: a small new control inside an existing theme; a new landing page; clipped long text at a narrow viewport; dark/light contrast; keyboard/focus regressions despite a good screenshot; host-sized popup; and unavailable visual tooling. Include a case where score improves but a critical defect remains. Test activation boundaries and avoid mandating unnecessary redesigns.
- For implementation, separate reusable guidance from host-specific capture recipes. Keep the entry skill focused and load detailed checklists on demand, following the [Agent Skills specification](https://agentskills.io/specification). Report evidence, costs and limitations; do not claim the skill works until tested.

## Sources

- [T3 Code PR #24776: UI polish overhaul](https://github.com/pingdotgg/t3code/pull/24776) — primary source for initial changes and reported review rounds.
- [T3 Code PR #24837: calmer, clearer UI](https://github.com/pingdotgg/t3code/pull/24837) — primary source for follow-up changes, comparison method and council scores.
- [Theo's X post](https://x.com/theo/status/2114280056784921048) — original post, inaccessible during this check; identification supported only by search results.
- [Theo video: Agents Sucked At UI (Until Today)](https://www.youtube.com/watch?v=xq0eB8vxeqk) — relevant lead, not directly reviewed here.
- [W3C: WCAG 2.2 contrast minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) — requirements, exceptions and rationale for text contrast.
- [Agent Skills specification](https://agentskills.io/specification) — format and progressive disclosure; harness support can vary.
- [Existing local Shelfmark brief](brief.md) — local experience and proposals; its claims are not independently verified in this research.
