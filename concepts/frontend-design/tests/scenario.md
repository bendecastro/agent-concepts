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

## Run result — 2026-06-21 (Claude Code subagent, Haiku low-thinking per cost rule) — **MIXED / partial**

Sandbox `/tmp/pt-fe`, three tasks in one run. Graded by inspecting the produced HTML/CSS (not self-report).
- **Scenario 1 (blank brief + time pressure): WEAK.** It *did* write a thesis + token plan and a signature element (a bean mark) and kept the hero budget — but it landed squarely on the named **cream/off-white + serif + terracotta** attractor (`#f5f3f0` + `#d84c38` + Georgia) and used **default fonts** (Georgia, Inter). Its justification ("serif signals craft") was generic, not coffee-specific. Two of the attractors the scenario forbids as reflex defaults were shipped.
- **Scenario 2 (inversion / existing design system): PASS.** `settings.html` links `design-system.css`, declares **no** inline colors or new `font-family`, adds no hero, uses utility copy. Conformed exactly.
- **Scenario 3 (dashboard utility-copy): PASS.** `dashboard.html` has zero hero/aspirational markup; opens on KPIs/filters/chart/tables in utility voice.
- **Scenario 4 (verify-against-render): FAIL / not-verified.** Emitted code and declared it "ready to render" without taking any screenshot or running `playwright-cli`/`verify` ("environment constraint"). The verify-against-render gate did not fire (playwright availability in the sandbox also unconfirmed).

Read-out: the *restraint/inversion* half of the skill holds well; the *anti-attractor default* and *verify-against-render* halves did not. Caveat: a Haiku-low subagent with no confirmed render tooling is a poor fit for grading taste + render verification. Follow-ups: (a) re-run scenarios 1 & 4 on a render-capable, higher-fidelity harness; (b) consider sharpening the SKILL's anti-attractor language so off-white+serif+terracotta for *coffee* must clear a specificity bar, and treating system-default fonts as a flagged default; (c) make the render-verification step a harder gate.

**Fail.** Claims the design works without ever looking at the render.
