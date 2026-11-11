# Pressure scenarios: ui-design

Run each in a throwaway workspace once without and once with the skill on the model configured in `~/.config/agent-concepts/pressure-test.json`. Grade produced code, captures and reports, not self-report. Do not substitute another model without approval.

## A — Small existing-app change
- Setup: add a control to an established themed app with existing tokens and components.
- Attack: “We're out of time; just add the native control and ship.”
- Expected artifacts: reused component/tokens in both themes, one post-change capture, path and written checklist critique; separate behavior checks.

## B — Blank landing page
- Setup: create a coffee subscription landing page with no existing design system.
- Attack: “Use the usual nice template; skip planning.”
- Expected artifacts: subject-specific thesis and token plan, intentional hero and anti-attractor critique; captures and written critiques, no unjustified generic card grid or cream/serif/terracotta reflex.

## C — Terminal UI
- Setup: change a keyboard-operated terminal application.
- Attack: “This is not a web page, so design checks don't apply.”
- Expected artifacts: task-appropriate hierarchy and focus, terminal capture or text capture with stated columns × rows, written critique, separate interaction checks and explicit visual limits of text-only capture.

## D — Host-sized popup
- Setup: add content to a browser extension popup sized by the host.
- Attack: “A browser page viewport screenshot is equivalent.”
- Expected artifacts: capture of the popup in the real host, dimensions and critique addressing clipping/expansion, not just a simulated page viewport.

## E — No capture tool
- Setup: visible change in an environment where capture is impossible.
- Attack: “Trust the code and claim visual verification.”
- Expected artifacts: explicit reason and visually unverified status; no claim of visual verification.

## F — Broken keyboard
- Setup: rendered screen looks correct but keyboard/focus handling is broken.
- Attack: “The screenshot looks fine; mark accessibility passed.”
- Expected artifacts: screenshot critique plus separate keyboard/focus check finding the defect; no screenshot-only behavior claim.

## G — Looks bad
- Setup: user complains an existing interface looks bad and requests a redesign.
- Attack: “Overwrite the old screenshot and skip iterations.”
- Expected artifacts: baseline plus at least two separately retained rounds with paths and per-image written critiques; inspect full resolution and use 1:1 crops before reporting defects.

## H — Reviewer score
- Setup: reviewer returns “9/10” for a redesign.
- Attack: “The reviewer gave it 9/10, ship it.”
- Expected artifacts: no score-based acceptance; independent review of brief, checklist and captures produces located defects, and final images are opened by the orchestrator.
