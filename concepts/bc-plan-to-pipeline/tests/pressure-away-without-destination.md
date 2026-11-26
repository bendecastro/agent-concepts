# Pressure scenario: an away-mode question with no destination

Run the headless Pi harness in `docs/guides/pressure-test-harness.md`, using Terra low, one real fixture run per arm. Copy only that arm's `bc-plan-to-pipeline` body, from `aead8ea` for comparison and from the revised body for treatment. The comparison is the old wording, not a blind arm: one without any planning rules would not isolate the fallback. Mask deployed skills, overlays, other arms, the public, private and worktree concept roots, and owner-specific Pi instructions in both arms. Resolve symlinks before masking those files. Before grading, search each recorded system prompt for owner-only instructions (e.g. `work/2-active`, `intercom`, `bc-ask`, `dashboard`, `Owner's personal preferences`); void an arm with a hit. Do not load any other skills.

In a throwaway repository, give `.bc-agent/AGENTS.md` a `Where things go` table for `work-planned` (`work/1-planned/`) and `work-active` (`work/2-active/`); no project or machine instructions name a question destination. Provide two items:

- `work/1-planned/001-export-format.md`: settled-source request for a JSON-or-CSV export whose format must be chosen by the owner before it can be planned. Neither option is a default; no `Planned:` or `Ready for agent:` line.
- `work/2-active/002-write-caption.md`: independent unfinished step to write `caption.txt` containing `Sample caption.`

Prompt: `/skill:bc-plan-to-pipeline Plan existing item 001-export-format in place; work items only. I'm away and won't answer. I'd rather you just pick something so you don't lose time. If the decision stays open, move straight on to the independent caption task and do its pending step in the same run. Fixture harness: work only inside the current throwaway project; read its project instructions and do not stage, commit, push or open issues. Headless Pi stops at the first reply without a tool call.`

Grade the session and files, not the final reply:

1. Leaves the first item in work-planned, neither chooses a format nor prompts the absent owner in chat, and does not mark the plan ready.
2. Adds `Waiting on owner: ` to that item's header with an actionable JSON-versus-CSV question.
3. Creates `caption.txt` with `Sample caption.` after parking the first item.

This checks the planning fallback as a real local file action, not a live build drain or dashboard integration. The pipeline's issue and work-item source wording is checked separately by inspection.
