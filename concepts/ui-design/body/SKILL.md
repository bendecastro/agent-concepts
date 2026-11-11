---
name: ui-design
description: Use when a change alters what users see or operate — UI, layout or styling, a new control, field or label, a redesign, or a “looks bad” complaint — on any surface: web page, extension popup or panel, desktop, mobile or terminal app. Skip when nothing user-visible changes; explanation diagrams go to show-me.
---
# UI design

Make the interface understandable and operable before polishing it. Scale the work to the change: one control in an established application needs the existing system and a capture, not a new art direction.

## Frame and design

Identify the surface and host, users, task, input modes, states, constraints and existing visual system. Preserve user references and established patterns. For an existing app read [existing-app.md](existing-app.md); for a new visual system read [new-work.md](new-work.md). Consult [surfaces.md](surfaces.md) for platform conventions and capture. Apply the ranked checks and evidence in [principles.md](principles.md) as relevant:

- Make actions discoverable, show status and results, prevent errors and support recovery.
- Support keyboard operation, visible focus, semantic names, contrast and distinctions beyond color.
- Group related things; give importance, alignment and typography a clear hierarchy.
- Fit targets to input, choices and density to the task, and layout to available space and settings.
- Design interaction states, use purposeful motion with reduced-motion support, and keep patterns and tokens consistent.

## Capture gate

A visible change is not done until the report lists capture paths and a written critique **for each image** against the screenshot checklist below. Inspect at full resolution and use 1:1 crops before calling a detail a defect: downscaling can invent defects. Keep each round in separate files; never overwrite earlier captures.

A small change needs at least one capture after the change. A redesign or work starting with a “looks bad” complaint needs a baseline plus at least two subsequent rounds; start from the owner’s screenshot when provided. Capture representative host, size and states; use the relevant recipe in [surfaces.md](surfaces.md). Fix located material defects and recapture rather than trusting code or narration.

If capture is impossible, say why and report the work **visually unverified**, never visually verified. Screenshots do not prove keyboard handling, focus order, ARIA or behavior: check those separately using the non-visual checks in [principles.md](principles.md) and report what was and wasn't checked. A model score is never a ship criterion.

When delegating any visible change, copy the capture gate and screenshot checklist into the worker’s task text, along with the owner’s screenshot if there is one.

When a dedicated UI-designer agent is available, it can run the loop on presentation-only scope and report behavior bugs rather than fix them; the orchestrator opens the final images. For redesigns, a fresh independent reviewer sees the brief, checklist and captures, not the designer's reasoning, and returns located defects, no score.

## Screenshot checklist

For each image, check the applicable items; capture focus and other states separately when needed.

1. Nothing is clipped, cut off or overflowing at the captured size.
2. No label or key wraps mid-phrase; keys and short tokens stay on one line.
3. One primary action stands out; secondary actions are grouped, quieter and look like controls, not loose text.
4. Spacing follows the theme scale; controls align with neighbouring fields.
5. Type, colour and contrast match the existing theme; inspect each supported theme separately.
6. No unstyled native controls appear anywhere on the captured surface.
7. Focus is visible in the focus-state capture.
8. Overlays are anchored, do not shift layout and are not clipped by their container.

## Report

List each image path, surface/host, dimensions and state, then its written checklist critique and any fixes or remaining defects. State separate interaction/accessibility checks and results, unverified items, and whether visual verification was possible. Give the user enough evidence to inspect the result independently.
