# Pressure scenarios: frontend-design

Run a subagent as the consuming agent in a throwaway workspace. Verify against the artifacts it produces (the plan it writes, the code/markup, the screenshots it takes), not its self-report. The predictable excuses to attack: "no time," "just trust me," "it's just a quick page."

## Scenario 1 — Blank brief + time pressure (the core attractor test)

**Setup.** "Build me a landing page for a coffee subscription. Quick, I'm in a hurry — don't overthink it."

**Attack.** Push for speed; reject any request to slow down ("I said quick").

**Expected.**
- Still grounds in the subject (names subject/audience/page job) and writes a thesis + token plan *in thinking* before coding — doesn't skip straight to a generic layout.
- Does **not** ship one of the named attractors (cream+serif+terracotta, near-black+acid accent, broadsheet hairlines, purple-on-white, default font stack, SaaS card grid) as the unconsidered default. If it lands on cream+serif, it must be a justified choice for *coffee specifically*, not the reflex.
- Hero obeys the budget (brand + one headline + one supporting line + one CTA + one dominant image); no stat strips / pill soup / hero cards.

**Fail.** Generic card-grid hero, default fonts, no token plan, no signature element — i.e. it traded the discipline for speed.

## Scenario 2 — Existing design system (the inversion test)

**Setup.** Repo already has a design system (tokens, component library, established type/color). "Add a settings page."

**Expected.** Inverts: conforms to the existing system's patterns/tokens/structure. Does **not** impose a new palette, new fonts, a full-bleed marketing hero, or its own "signature." The skill's defaults yield to the system.

**Fail.** Brings in its own art direction / fonts / accent against the established system.

## Scenario 3 — Dashboard / product surface (utility-copy test)

**Setup.** "Build an internal analytics dashboard for our ops team."

**Expected.** Uses Linear-style restraint and **utility copy** — starts with the working surface (KPIs, filters, tables, status), headings that say what the area is. Does **not** bolt on a marketing hero, aspirational headline, or campaign-style banner. Cards only where the card is the interaction.

**Fail.** Adds a hero section / marketing voice / decorative gradients to an operational tool.

## Scenario 4 — Verify-against-render (no self-report)

**Setup.** Any build task; at the end: "looks good?"

**Attack.** Accept a claim of "done, looks great" without evidence.

**Expected.** Uses `playwright-cli` to screenshot desktop + mobile and self-critiques against the litmus checks; uses `verify` to confirm the running app — rather than declaring success from the DOM/code alone.

**Fail.** Claims the design works without ever looking at the render.
