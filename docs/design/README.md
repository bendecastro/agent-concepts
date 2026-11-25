# Design

This folder says how this product looks and behaves **now**. Agents and people
read it before adding or changing anything a user sees or operates. The
generic method behind it is `design-framework.md` in the `ui-design` skill.

<!-- Optional: if the project has a page for its screenshot and review conventions, link it here. -->

## Current truth vs decision log

- These pages state current behaviour only: one fact per line, no history.
- Why something is so lives in the project's decision log. Link the decision
  number; do not copy its text.
- A page line becomes true in the same commit as the code that makes it true.
  A decision may be logged earlier, when it is made.

## Where a rule lives

| If two people could... | It belongs in |
|---|---|
| disagree about it (taste, wording, trade-off) | a page here, stating the current choice, whoever made it |
| only differ by mistake (a value, a look, a part) | shared code or a design token |
| break it without noticing, and it can be found by text search | a check in the project's test suites, with a message naming the part and the page line |
| only see it on screen (alignment, matching neighbours) | the screenshot review |

## Before adding or restyling a control

Name the existing part you are reusing for that kind of control. If the
change needs something new (a colour, size, icon, wording or control kind),
pick the closest fit to the existing look, define it once as a token or shared
part, use it only from there, and record it on a page here in the same commit,
marked as the agent's choice the owner may change. Ask the owner only to
contradict a recorded decision, to remove something users rely on,
or any case listed under **Stricter ask-cases**; never for taste calls.

## Stricter ask-cases

<!-- Optional: one line per extra case where this project wants the owner asked. -->

## Pages

<!-- Add one line per page as the project grows: `page.md`: the question it answers. -->

(none yet)

## Checks

<!-- List each design check: file, what it rejects, and how exceptions are marked. -->

(none yet)
