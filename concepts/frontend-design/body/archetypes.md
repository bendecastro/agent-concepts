# Archetypes & checklist

Load this when you start building. These are the concrete per-surface rules behind the defaults in `SKILL.md`. They are defaults that counter known failure modes — break one only deliberately, and only when the brief or an existing design system calls for it.

## Landing pages & marketing surfaces

Default section sequence (a narrative, not a dashboard):
1. **Hero** — brand/product, promise, CTA, and one dominant visual
2. **Support** — one concrete feature, offer, or proof point
3. **Detail** — atmosphere, workflow, product depth, or story
4. **Social proof** — credibility (optional)
5. **Final CTA** — convert, start, visit, contact

Hero rules:
- One composition only. Full-bleed image or dominant visual plane — edge-to-edge, no inherited page gutters or shared max-width; constrain only the inner text/action column.
- Brand first, headline second, body third, CTA fourth. No headline should overpower the brand on a branded page.
- Hero budget: usually only brand + one headline + one short supporting sentence + one CTA group + one dominant image. Keep stats, schedules, event listings, address blocks, promos, "this week" callouts, and metadata rows *out* of the first viewport.
- No detached labels, floating badges, promo stickers, info chips, or callout boxes on top of hero media.
- Headlines ~2–3 lines on desktop, one glance on mobile. Text column narrow, anchored to a calm tonal area of the image, strong contrast, clear tap targets.
- **Viewport budget:** a sticky/fixed header counts against the hero — header + hero must fit the initial viewport at common desktop and mobile sizes. With `100vh`/`100svh` heroes, subtract chrome (`calc(100svh - header-height)`) or overlay the header instead of stacking it in flow.
- Tests: if the first viewport still works after removing the image, the image is too weak. If the brand disappears once you hide the nav, the hierarchy is too weak.

## Apps, dashboards & product surfaces

Default to **Linear-style restraint**: calm surface hierarchy, strong typography and spacing, few colors, dense-but-readable information, minimal chrome, cards only when the card *is* the interaction.

Organize around: primary workspace · navigation · secondary context/inspector · one clear accent for action or state.

Avoid: dashboard-card mosaics, thick borders on every region, decorative gradients behind routine UI, multiple competing accents, ornamental icons that don't aid scanning. If a panel becomes plain layout without losing meaning, drop the card treatment.

**Utility copy** (dashboards/admin/operational tools): orientation, status, and action over promise/mood/brand voice. Start with the working surface (KPIs, charts, filters, tables, status) — no hero section unless explicitly asked. Headings say what the area is or what you can do there ("Selected KPIs", "Plan status", "Last sync"). One sentence on scope/behavior/freshness/decision-value. Litmus: scanning only headings, labels, and numbers, can an operator understand the page immediately? If a sentence could appear in a homepage hero or ad, rewrite it until it sounds like product UI.

## Imagery

Imagery must do narrative work — the first viewport needs a *real* anchor; decorative texture isn't enough.
- At least one strong, real-looking image for brands, venues, editorial, lifestyle products. Prefer in-situ photography over abstract gradients or fake 3D.
- Crop to a stable tonal area for text. Avoid images with embedded signage/logos/typographic clutter fighting the UI, or built-in UI frames/splits/cards/panels.
- Multiple moments → multiple images, not one collage.
- If you generate imagery: build a mood board / several options first, describe the attributes you want (style, palette, composition, mood), then select. Default to any uploaded/pre-generated images; don't hotlink web images unless asked.

## Motion

Use motion to create presence and hierarchy, not noise. Ship 2–3 intentional motions for visually-led work: one hero entrance sequence; one scroll-linked, sticky, or depth effect; one hover/reveal/layout transition that sharpens affordance. Motion must be noticeable in a quick recording, smooth on mobile, fast, restrained, consistent across the page — and removed if it's only ornamental. (Framer Motion when the stack has it: section reveals, shared-layout transitions, scroll-linked opacity/translate/scale, sticky storytelling, presence effects.)

## Copy

Product language, not design commentary. Let the headline carry meaning; supporting copy is usually one short sentence. Cut repetition between sections. Never leak prompt language or design commentary into the UI. Each section does exactly one job: explain, prove, deepen, or convert.

## Hard rules (defaults — break only deliberately)

- No cards by default; no hero cards.
- No boxed/center-column hero when the brief calls for full bleed.
- No more than one dominant idea per section.
- No section needing many tiny UI devices to explain itself.
- No headline overpowering the brand on branded pages.
- No filler copy.
- No split-screen hero unless text sits on a calm, unified side.
- No more than two typefaces without a clear reason.
- No more than one accent color unless the product already has a strong system.
- No purple bias, no dark-mode bias — choose a direction and define CSS variables.

## Reject these failures

Generic SaaS card grid as first impression · beautiful image with weak brand presence · strong headline with no clear action · busy imagery behind text · sections repeating the same mood statement · carousel with no narrative purpose · app UI made of stacked cards instead of layout.

## Litmus checks (run against the render, not the DOM)

- Is the brand/product unmistakable in the first screen?
- Is there one strong visual anchor?
- Can the page be understood by scanning headlines only?
- Does each section have one job?
- Are cards actually necessary?
- Does motion improve hierarchy or atmosphere?
- Would the design still feel premium if all decorative shadows were removed?
