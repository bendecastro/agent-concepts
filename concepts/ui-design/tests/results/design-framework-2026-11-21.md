# design-framework.md pressure results (2026-11-21)

Consumer: Terra (low thinking), per the private pressure-test config. Each arm ran in a throwaway Svelte fixture whose AGENTS.md points at a copy of the ui-design body: "old" = body before the design framework, no `docs/design/README.md`; "new" = body with `design-framework.md` and the scaffolded README. Prompt: a rushed user, unavailable for questions, asks for UI additions. Graded from each arm's commit, not its report.

| Round | Scenario | Old arm | New arm |
|---|---|---|---|
| 1 | "Select all" tick box + sort control; shared Checkbox imported in a neighbouring file | reused Checkbox; no design record | reused Checkbox; recorded `docs/design/toolbar.md` + README Pages line in the same commit |
| 2 | Archive on/off in a header (shared Toggle used only on the settings page) + coloured priority label (new kind, no colour token) | reused Toggle; hex literals in the component; no record; no question | reused Toggle; hex literals in the component; recorded a page; no question, assumption buried in summary |
| 3 | Round 2 rerun after "Decide once, in one place" (new arm only) | (round 2 result) | reused Toggle; added `--tl-priority-*` tokens to the theme file, component uses them only; page line "Agent choice (owner may change)"; FYI in report, no question |

Findings: the record-in-same-commit rule held in every new arm and never appeared in old arms. Reuse showed no difference (Terra searched and reused without the framework). Round 2 failed the original "ask the owner on judgement calls" rule; the owner then set the goal as consistency over sign-off, and round 3 held the replacement rule (define new values once, record them as the agent's choice, mention as FYI).

Not exercised: an interactive run, the "ask only when contradicting a recorded decision" branch, a project without a README (copy-template path), screenshots.
