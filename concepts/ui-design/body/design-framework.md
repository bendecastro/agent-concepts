# Design framework

Use this when adding or restyling a control, or recording a design decision, in a project people use (GUI, TUI or CLI). Design here is everything a user sees or operates: look, interaction, keyboard and mouse, wording, information architecture, states, accessibility and motion. The goal is that short-lived agents build consistently without the owner re-deciding the same things.

## Start from the project's design README

Read the project's `docs/design/README.md` first; it lists the project's design pages and checks. If it is missing, create it from the `docs/design/README.md` template that the `bc-init-agent` scaffold writes, in its own commit. Each project grows its own pages; there is no fixed page list.

## Name the part you reuse

Before adding or restyling any control, name the existing part you are reusing for that kind of control. This is the concrete form of "reuse the existing components" in [existing-app.md](existing-app.md). If there is none, it is a new kind: record it on a page in `docs/design/` in the same commit, and ask the owner when the look or behaviour is a judgement call. Why: past drift came from building a second part beside one that already existed, not from misreading a rule.

## Where a rule lives

If two people could disagree about it, it is prose on a design page, written after the owner decides. If they could only differ by mistake, it is shared code or a design token. If it can be broken unnoticed and found by text search, it is a check. If it shows only on screen (alignment, matching neighbours), it is the screenshot review in [SKILL.md](SKILL.md#screenshot-checklist). Group tokens by role (surface, text, action, status), not by value. Where a component takes a size or variant, prefer a type union (for example `type IconSize = 'sm' | 'md'`) over a check.

## Ask the owner about judgement calls

Bring options before building. By default put pictures in `owner-notes/<item>/` (any untracked notes folder the project uses works): numbered mockups, a README with one line per picture, and the owner replies like `1a 2a ok`. Show the control beside its neighbours, in every supported theme. A text-only question needs no pictures. Working captures and critique rounds stay in `captures/` ([surfaces.md](surfaces.md)); copy only the pictures the owner must choose between into `owner-notes/<item>/`. In a non-interactive run, follow the Report section of [SKILL.md](SKILL.md#report).

## Write path

Log the owner's decision in the project's decision log when it is made. The design-page line lands in the same commit as the code that makes it true, and the plan names that step. Why: a line written at decision time describes behaviour that does not exist yet. A reviewer treats a page line that no longer matches the code as a finding.

## Keep pages small

Pages state current behaviour only: one fact per line, no history. Link decisions by number instead of copying their text. Split a page by question once it grows past about 200 lines, and add each page to the README's Pages list.

## Add a check when a control kind is first named

When a page first names a control kind and its forbidden alternatives, add a text-search check in the project's own test runner; no shared checker tool. Each rule's failure message names the part to use and the design-page line. An exception is a `design-allow <rule>: <reason>` comment on the line. Existing violations go in a per-file baseline that may only fall, so adding the check early costs nothing. List the check under Checks in the README. Worked example: Manicule's `apps/extension/test/design-system.test.ts`.

## Capture scope

Capture every surface the changed part, token or selector reaches, with its neighbours, not only the surface you worked on. Why: a shared selector once changed a surface nobody captured. Capture rules and naming are in [surfaces.md](surfaces.md) and the capture gate in [SKILL.md](SKILL.md#capture-gate).
