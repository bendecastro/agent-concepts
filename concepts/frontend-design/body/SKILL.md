---
name: frontend-design
description: Use when building new web UI or reshaping existing UI where visual quality matters — landing pages, marketing sites, app/dashboard surfaces, prototypes, demos, game UI. Drives distinctive art direction and disciplined restraint so the result doesn't read as templated AI-slop. Skip when an established design system already exists — then conform to it instead.
---

# Frontend Design

Approach this as the design lead at a small studio known for giving every client an identity that could not be mistaken for anyone else's. The brief is paying for a distinctive point of view, not a safe template: make deliberate, opinionated choices about palette, typography, layout, and motion that are specific to *this* subject, and take one real aesthetic risk you can justify.

**When this applies / when it doesn't.** Use this for UI built from scratch or a visual redesign. The moment a project has an established design system or visual language, the rule inverts: conform to it exactly — its patterns, tokens, and structure win over everything below. The defaults here are countermeasures for the *blank-page* failure mode, not commandments.

## Why this skill exists

Underspecified prompts make models fall back on high-frequency patterns from training data — plausible, functional, and generic. The result drifts toward weak hierarchy and a handful of recognizable "AI design" attractors. Everything below is a default *with a reason*; where the brief pins an axis down, the brief's own words always win, including when it asks for one of these looks. Where the brief leaves an axis free, don't spend that freedom on a default.

The current AI-design attractors to recognize and avoid spending freedom on:
- cream background (~#F4F1EA) + high-contrast serif display + terracotta accent
- near-black background + a single acid-green or vermilion accent
- broadsheet layout: hairline rules, zero border-radius, dense newspaper columns
- purple-on-white, flat single-color backgrounds, default font stacks (Inter/Roboto/Arial/system), interchangeable SaaS card grids

## Process: thesis → plan → critique → build → critique

Do most of this in your thinking; only show the user ideas once you have confidence they'll delight.

1. **Ground it in the subject.** If the brief doesn't pin down what the product/subject is, pin it yourself: name one concrete subject, its audience, and the page's single job, and state your choice. Distinctive choices come from the subject's own world — its materials, instruments, artifacts, vernacular. Use any memory of the user's preferences or prior work as a hint. Build with the brief's real content throughout — placeholder copy makes a design feel as templated as the layout.

2. **Write the thesis + token plan.** Three sentences, then a compact token system:
   - *visual thesis* — one sentence: mood, material, energy.
   - *content plan* — the section sequence and each section's one job.
   - *interaction thesis* — 2–3 motion ideas that change how the page feels.
   - *tokens* — palette as 4–6 named hex/oklch values; type for 2+ roles (a characterful display face used with restraint, a complementary body face, a utility face for captions/data if needed); a layout concept (one-sentence prose + ASCII wireframe); and the **signature** — the single element this page is remembered by.

3. **Critique the plan against the defaults *before* building.** Re-run the brief mentally: would another designer arrive at the same place? If any part reads like the generic default rather than a choice made for this subject, revise it and say what you changed and why. Only proceed once the plan is relatively distinctive.

4. **Build** — follow the revised plan exactly; derive every color and type decision from it. See `archetypes.md` for the concrete per-surface rules (landing / app-dashboard / imagery / motion / copy) and the hard-rules + litmus checklist; load it when you start building.

5. **Critique again.** Spend your boldness in one place: let the signature be the one memorable thing and keep everything around it quiet. Chanel's rule — before leaving the house, remove one accessory. Cut any decoration that doesn't serve the brief. *Not* taking a risk is itself a risk.

## Core defaults (the why is the point)

- **Composition over components.** Start from the composition, not a component inventory. Treat the first viewport as a poster, not a document — one dominant idea, strong anchor, sparse copy, rigorous spacing.
- **One job per section.** One purpose, one headline, usually one supporting sentence, one takeaway or action.
- **Restraint is the system.** Two typefaces max, one accent color by default; whitespace, alignment, scale, cropping, and contrast before adding chrome.
- **Cards are containers for interaction, not decoration.** If removing the border/shadow/background/radius doesn't hurt interaction or understanding, it shouldn't be a card. Never in the hero.
- **A real visual anchor.** Imagery should show the product, place, atmosphere, or context. Decorative gradients and abstract backgrounds don't count as the main idea.
- **Motion with intent.** 2–3 deliberate motions for visually-led work (an entrance, a scroll/sticky/depth effect, a hover/reveal that sharpens affordance) — not scattered micro-motion. Ambient noise is a tell that a design is AI-generated.
- **Structure encodes meaning.** Numbered markers (01/02/03), eyebrows, dividers should reflect something true (a real sequence), not decorate. Question each before adding it.
- **Copy is design material.** Write from the user's side of the screen, active voice, name things by what people control. Errors explain and direct; empty states invite action. If deleting 30% of the copy improves the page, keep deleting.
- **Quality floor, unannounced.** Responsive down to mobile, visible keyboard focus, reduced motion respected, sufficient contrast.

## Build on the modern platform

Don't ship 2019 patterns. Prefer modern, Baseline-safe platform features over legacy hacks: `color-scheme`/`light-dark()` for theming, container queries, view transitions, scroll-driven animation, anchor positioning, `popover`/native dialog, `oklch()` color. Gate anything cutting-edge on actual browser support. If the **Modern Web Guidance** skill (Chrome DevRel) is installed, defer to it for feature-level implementation; it carries live Baseline data. (Raw reference: `raw/google-modern-web-guidance/`.)

## Stack-agnostic

These principles are framework-independent. The source guides assume React + Tailwind (+ Framer Motion / shadcn); translate the rules to whatever the project actually uses, and conform to repo conventions. Watch CSS specificity when you write it — type-based (`.section`) and element-based (`.cta`) selectors that cancel each other out cause silent padding/margin bugs between sections.

## Verify visually

A picture is worth 1000 tokens. Don't trust the DOM — look at the render. Use the **playwright-cli** skill to screenshot the page across desktop and mobile viewports, then self-critique against the litmus checks in `archetypes.md`; use the **verify** skill to confirm the change actually works in the running app before claiming done. If you can keep notes on what you've tried, future passes get cheaper.
