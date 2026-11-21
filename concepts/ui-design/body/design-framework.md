# Design framework

Use this when adding or restyling a control, or recording a design decision, in a project people use (GUI, TUI or CLI). Design here is everything a user sees or operates: look, interaction, keyboard and mouse, wording, information architecture, states, accessibility and motion. The goal is that short-lived agents build consistently without the owner re-deciding the same things.

## Start from the project's design README

Read the project's `docs/design/README.md` first; it lists the project's design pages and checks. If it is missing, copy the `DESIGN_README` text from `bc-init-agent`'s `body/scaffold.py` into `docs/design/README.md` in its own commit; do not run the scaffold just for this. Without `bc-init-agent`, write the sections Current truth vs decision log, Where a rule lives, Before adding or restyling a control, Pages, and Checks. Each project grows its own pages; there is no fixed page list.

## Name the part you reuse

Before adding or restyling any control, name the existing part you are reusing for that kind of control. This is the concrete form of "reuse them" in [existing-app.md](existing-app.md). If there is none, it is a new kind: follow [Decide once, in one place](#decide-once-in-one-place). Why: past drift came from building a second part beside one that already existed, not from misreading a rule.

## Where a rule lives

If two people could disagree about it, it is prose on a design page stating the current choice, whoever made it. If they could only differ by mistake, it is shared code or a design token. If it can be broken unnoticed and found by text search, it is a check. If it shows only on screen (alignment, matching neighbours), it is the screenshot review in [SKILL.md](SKILL.md#screenshot-checklist). Group tokens by role, not by value ([principles.md](principles.md) #17). Where a component takes a size or variant, prefer a type union (for example `type IconSize = 'sm' | 'md'`) over a check.

## Decide once, in one place

When the change needs something the project does not have yet (a colour, size, spacing, icon, wording pattern or new control kind), do not ask. Pick the closest fit to the existing look, define it once (a token in the project's token or theme file, or a shared part), and use it only from there, never as a literal value in the component. Record it on a design page, marked as the agent's choice the owner may change, and list it as one FYI line in the report. Why: the goal is consistency, not sign-off; a choice made in one place is one edit to change, while scattered literals need a thousand.

Ask the owner only when the change would contradict a recorded decision or design-page line, or remove or rename something users already rely on. Then put numbered pictures in `owner-notes/<item>/` (or the project's untracked notes folder) with a README of one line per picture; the owner replies like `1a 2a ok`. Show the control beside its neighbours in every supported theme; a text-only question needs no pictures. Copy only the pictures the owner must choose between into `owner-notes/<item>/`; working captures stay where [surfaces.md](surfaces.md) puts them. In a non-interactive run, follow the Report section of [SKILL.md](SKILL.md#report).

## Write path

Log an owner decision in the project's decision log when it is made. Record an agent choice on its design page. Either way, the design-page line lands in the same commit as the code that makes it true, and the plan names that step. Why: a line written at decision time describes behaviour that does not exist yet. A reviewer treats a page line that no longer matches the code as a finding.

## Keep pages small

Pages state current behaviour only: one fact per line, no history. Link decisions by number instead of copying their text. Split a page by question once it grows past about 200 lines, and add each page to the README's Pages list.

## Add a check when a control kind is first named

When a page first names a control kind and its forbidden alternatives, add a text-search check in the project's own test runner; no shared checker tool. Each rule's failure message names the part to use and the design-page line. An exception is a `design-allow <rule>: <reason>` comment on the line. Existing violations go in a per-file baseline that may only fall, so adding the check early costs nothing. List the check under Checks in the README.

If `~/.config/agent-concepts/overlays/ui-design.md` exists, read it: it may name a worked example of a project check. It never changes behaviour, and the project's own instructions take precedence.

## Capture scope

The capture scope is in the [capture gate](SKILL.md#capture-gate); capture rules and naming are in [surfaces.md](surfaces.md).
