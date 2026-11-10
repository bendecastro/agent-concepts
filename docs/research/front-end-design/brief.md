# Front-end UI design skill: brief from a real session

Handoff brief for an agent improving how coding agents design and restyle UI. It records what went wrong and what worked in one long session in the Shelfmark repo (a Chromium MV3 bookmark manager written in Svelte), so the next skill is built on observed failures rather than guesses.

## Starting point

- An existing concept already covers aesthetics: [`concepts/frontend-design`](../../../concepts/frontend-design/CONCEPT.md) (body: `SKILL.md` plus `archetypes.md`). It is aimed at *blank-page* work (landing pages, distinctive art direction) and tells the agent to conform to an existing design system when one exists. Its "Verify visually" section is three sentences and points to `playwright-cli`.
- Shelfmark now has a project convention born in this session: `.bc-agent/conventions/ui-design.md` in the Shelfmark repo (screenshot critique loop with a checklist). Treat it as a seed, not the final form.
- Open question for the owner: extend `frontend-design`, or add a separate concept for *incremental UI work inside an existing app* (the common case here). The failures below are almost all of the second kind.

## What the work was

Small changes to an existing, already-styled extension UI: a save popup (fixed-size browser popup), a full app page, a side panel, a Settings page, a command palette. Requests from the owner were short and visual: "the new UI is ugly", "these should look like buttons", "this text wraps and is unreadable", "the popup still clips". The owner judges from screenshots of the real browser.

## Observed failures

1. **Feature work shipped UI nobody looked at.** Workers added links and a checkbox to the popup and Settings; all tests passed; the owner's first look found it ugly (link labels wrapping onto two lines, crowding the primary button, fields clipped at the right edge). Tests and typecheck say nothing about appearance.
2. **The screenshot environment did not match the real one.** After a first redesign, Playwright screenshots of `popup.html` in a normal page at chosen viewport widths looked clean, but the real popup in the browser still clipped. Root cause: the popup used `width: 380px; max-width: 100vw`, and Chromium sizes extension popups from content, so `100vw` was evaluated while the popup's width was still being decided and let it collapse narrower than the content. A page viewport imposed from outside hides that entirely. Only a capture of the real browser popup (real browser binary, extension loaded, popup opened by its real keyboard shortcut, screen capture of the window) showed the bug.
3. **The agent's self-critique was incomplete and partly unverifiable.** One worker overwrote its first-round screenshots, so its round-1 critique could no longer be checked against images. Another captured "round 1" at the wrong viewport widths because the script passed the viewport in the wrong place. A third reported the visual pass incomplete itself (a dropdown stretched a toolbar; real popup never captured). Self-reports needed the parent to open the final images before accepting the work.
4. **Inline text layouts for structured data.** A keyboard-shortcut reference was laid out as flowing text, so `j / k` broke into `j /` and `k` on separate lines and descriptions wrapped under the keys. The fix was structural: a two-column grid (`max-content 1fr`), keys as `<kbd>` keycaps with `white-space: nowrap`, descriptions wrapping in their own column.
5. **Secondary actions styled as loose text.** Navigation links next to a primary button read as stray text. The owner wanted them to look like buttons, with icons that say what they do (app window, side panel, gear). Result: compact outlined buttons with inline SVG icons and short labels, full names kept as accessible names.
6. **Browser-default controls left unstyled.** Older parts of the app still showed Chromium's default grey bevelled buttons and selects next to themed ones. Nobody noticed until a screenshot taken for another purpose showed them. A sweep for unstyled native controls belongs in every UI pass.
7. **A dropdown changed its container's layout.** An autocomplete list rendered in flow inside a toolbar stretched and misaligned the toolbar; it needed to be an anchored overlay there, while in a form it worked better in flow so it did not cover the next field. Placement depends on the container.
8. **Visual review and code review are different jobs.** The UI looked right, but a separate code reviewer still found a real keyboard bug (Shift+Tab accepted a suggestion instead of moving focus back) and missing tests. Screenshots catch none of that.

## What worked

- **A required loop, written into the task**: render, screenshot at real sizes, open each screenshot, write a critique against a fixed checklist, fix, repeat, at least two rounds, keep every round's images and critique. Workers followed it once it was in the task text; they did not do it on their own.
- **A short concrete checklist** beat taste language: nothing clipped or overflowing; no label wrapping mid-phrase; one primary action, secondary actions grouped and quieter; spacing on an 8 px grid and aligned to the same edges as the fields; type, contrast and colour taken from the existing theme file.
- **Real sizes named explicitly**: popup at 320/360/400 px and natural width (Chromium caps popups at 800×600); pages at a narrow and a wide window; side panel around 400 px.
- **Real browser capture for anything the browser sizes itself** (popups, side panels): throwaway profile, extension loaded from the build output, hidden workspace, real shortcut to open, window-geometry screen capture.
- **Reusing the app's own styles** (existing buttons, keycaps, theme variables) instead of inventing a look; one shared set of button variants in the theme file.
- **The parent opening the final screenshots itself** before merging, and a separate code reviewer for behaviour.
- **Starting from the owner's screenshot**: copying it into the run directory and naming the visible defects in the task.

## Requirements for the skill

1. Trigger on any change that alters what a user sees, including feature work that adds a control, not only "design" requests.
2. Make the screenshot critique loop mandatory, with preserved rounds (never overwrite), a written critique per image, and a minimum of two rounds.
3. Tell the agent to capture the real rendering context when the browser or host decides the size (extension popups and side panels, embedded webviews, native dialogs), and why a page viewport is not enough.
4. Ship a concrete checklist (above), plus an "inside an existing app" stance: conform to the existing theme, reuse existing components, sweep for unstyled native controls.
5. Cover structured-data layout: tables and key/description lists as grids; keys and short tokens never break.
6. Cover overlays: when a popup list should overlay (anchored, high z-index, not clipped by overflow ancestors) versus sit in flow.
7. Separate visual review from behaviour review; say that screenshots do not verify keyboard handling or ARIA.
8. Make the result checkable by someone else: final screenshot paths and critiques in the report, so a reviewer or the owner can compare claims to images.
9. Stay stack-agnostic and harness-agnostic; real-browser capture recipes can live in a reference file per platform (for example Linux/Wayland with `grim` and the compositor's window geometry; macOS `screencapture`).

## Open questions for the owner

1. One concept (extend `frontend-design`) or two (blank-page art direction vs incremental UI in an existing app)?
2. Should the loop be enforced by a gate (for example, a report must list screenshot paths) or stay advisory?
3. Should a separate visual reviewer (different model, sees only screenshots and the checklist) be part of the default flow, or only on request?
4. Where should real-browser capture recipes live, given they are platform-specific?

## Evidence

Screenshots and per-round critiques from the session are in a temporary run directory and will not survive a reboot; copy any you want into `docs/research/raw/` before relying on them. The durable record is the Shelfmark repo history (popup redesign, popup clipping fix, tag-suggestion combobox, palette shortcut layout) and its `.bc-agent/conventions/ui-design.md`.
