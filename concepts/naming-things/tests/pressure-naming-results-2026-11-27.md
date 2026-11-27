# Naming Things pressure result — 2026-11-27

**FAIL; deployment stays off.** Decisive [case G](pressure-naming.md): three blind baseline and three with-skill runs on `openai-codex/gpt-6.1-terra`, thinking low. These were real tool-using sessions in throwaway fixtures, not planning dry runs. All six sessions finished; none held all three checks. Cases A–F were not run.

Both arms started with byte-identical prompts and glossaries. Deployed skills, overlays and the public/private concept roots (including the test checkout) were hidden in both arms. Pi's always-loaded instructions and their resolved targets were masked; context discovery and extensions were off. The captured system messages and complete session logs had no owner-only text matches and no unexpected skill reads. The blind sessions read neither skill; each treatment session read both the supplied naming body and its glossary dependency before writing artifacts.

| Run | Clear name | Stable ID and hash input | Glossary persistence | Overall |
| --- | --- | --- | --- | --- |
| Baseline 1 | Fail | Fail | Fail | Fail |
| Baseline 2 | Fail | Fail | Fail | Fail |
| Baseline 3 | Fail | Fail | Fail | Fail |
| With skill 1 | Fail | Fail | Pass | Fail |
| With skill 2 | Fail | Fail | Pass | Fail |
| With skill 3 | Fail | Fail | Pass | Fail |

- **Names:** All six manifests and modules retained `harbor-review` (or its corresponding Python/title spelling) on every public naming surface for a step that drafts, not reviews. Its provider is irrelevant to the function. All six named Python entry points were callable and returned a draft matching the ledger record.
- **Persistence:** All six embedded the requested spelling in both `job_id` and `hash_input` in the first write, without an alias reader. In each fixture, the ledger had the same ID as the manifest.
- **Glossary:** No run redefined **Review**. The baseline runs omitted `Saved in` and rename-cost markers. The three treatment runs added both without implementation paths. With-skill runs 1 and 3 recorded the separately named state as a separate `state value` entry; run 2 included it under the step term.
- **Approval:** No run paused for naming approval (the body says not to).
- **Flagging:** every with-skill reply named the clash between `harbor-review` and the glossary's verdict meaning of Review (3/3); no baseline reply mentioned it (0/3). Only with-skill run 1 proposed a replacement (`draft-reply`); runs 2 and 3 only noted the clash. Run 1 also warned that the spelling was now in the job ID and hash input.

The skill changed what the agent noticed but not what it did: with it, the agent saw the clash every time, then still used the name the user dictated and persisted it into IDs and hashes.

**Body gap (cause, for a later fix).** `body/SKILL.md` line 8 says to "choose names" from an "advisory checklist", and its rules say to reserve `review` for a verdict and to keep mutable names out of derived IDs and hashes. It never says what to do when the user explicitly dictates a name that breaks those rules, or explicitly asks for the spelling in IDs and hashes. Faced with that conflict, the model treated the user's instruction as overriding the advisory checklist. A fix should add one rule for that case: say which outcome is wanted (use the clearer name and report the change, or keep the dictated name only after stating the clash and the proposed name before the first persisted write) and how that squares with "do not pause to ask for naming approval". Then rerun case G on both arms. Whether the fixture should instead accept flag-and-propose as a hold depends on that choice, so check 1 stays as written until the body states it.

The skill body was not changed and no deployment ran.
