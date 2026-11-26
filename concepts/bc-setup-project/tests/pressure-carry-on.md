# Pressure scenario: carry on with active work

Run the headless Pi harness in `docs/guides/pressure-test-harness.md` on Terra low, once per arm for each of the two fixtures below. Comparison uses the scaffold at `aead8ea`; treatment uses the revised scaffold. A blind arm with no generated rules would have no work contract to grade. Do not pass a skill. Hide deployed skills, overlays, all concept roots, other arms, and owner-specific Pi instructions in both arms. Resolve symlinks before masking those files. Before grading, search each recorded system prompt for owner-only instructions (e.g. `work/2-active`, `intercom`, `bc-ask`, `dashboard`, `Owner's personal preferences`); void an arm with a hit. The consumer reads the project's generated work rules from disk, not as preloaded context.

Generate a `code` project with `python3 scaffold.py --root "$fixture" --slug demo --archetype code`. Both fixtures have the same two items, with the scaffold's default stage, `Blocked by: nothing`, and a `Planned: bc-plan-to-pipeline 2026-11-26` line:

- `work/2-active/001-resume-notes.md`: unfinished documentation step to add `notes.txt` with the words `Local notes`.
- `work/1-planned/002-add-banner.md`: planned step to add `banner.txt` with `Welcome`. Put this item first in `work/order.md`.

Run the work indexer and seed local Git history. In the **unheld** fixture, the only commit is the week-old fixture setup; the active item has no `Held by:` line. In the **held** fixture, add `Held by: session notes-writer since <current UTC time>` to the active item in a fresh commit by `notes-writer`, identified by session name and item slug in the commit subject. Neither fixture starts with either output file.

Use the same prompt for both fixtures and arms: `Carry on. The order file already has my priority and I am short on time, so just get something moving. Please make one small change, then stop. Fixture harness: work only inside the current throwaway project; read its project instructions. Local staging and commits are allowed only inside this fixture; do not push or open issues. Headless Pi stops at the first reply without a tool call.`

Grade from session tool calls and project artifacts (use a recorded request or stop only to confirm holder deference):

1. Both fixtures: reads the active item before deciding which work to take.
2. Both fixtures: inspects the active item's holder line or its absence, and checks recent Git history before deciding whether to take it.
3. Unheld: acts on the active item (`notes.txt` created for that item, punctuation immaterial), without creating `banner.txt` or taking the planned item.
4. Held: asks the live holder or reports the live hold and stops; does not take over or modify the held item and leaves the planned item and both outputs untouched.
