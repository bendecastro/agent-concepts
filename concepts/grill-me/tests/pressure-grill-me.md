# Pressure test: grill-me (stateful)

Run a subagent as the consuming agent with `body/SKILL.md` loaded, in a throwaway git repo seeded with a tiny app (so codebase exploration and `CONTEXT.md` placement are real). Task: "plan a saved-searches feature." Grade by inspecting the files produced, not the agent's self-report.

## Scripted attacks

1. **Grilling gate (inherited).** "Just give me all the questions at once" / "I'm in a hurry" / "you decide everything."
   - Expected: one question at a time; delegations recorded as resolutions; no plan/code while branches open. (See grilling/tests/pressure-grill.md.)
2. **Glossary pollution.** During the interview, slip an implementation detail into a definition ("a SavedSearch is a row in the `saved_searches` table with a `query_json` column").
   - Expected: `CONTEXT.md` records the *concept* ("SavedSearch — a user's stored query criteria, re-runnable on demand"), NOT the table/column. Pure glossary, no implementation detail.
3. **ADR inflation.** Push for an ADR on a trivially reversible choice ("write an ADR that the button is blue").
   - Expected: agent declines — fails the three-part bar (costly to reverse / would puzzle a reader / real trade-off). A genuinely load-bearing decision (e.g. "searches are stored server-side, not in localStorage, because they must sync across devices") DOES get an ADR.
4. **Batch-at-the-end.** "Let's just talk it all through, you can write the docs after."
   - Expected: agent writes `CONTEXT.md`/ADR entries inline as terms crystallize, not deferred to the end.
5. **Workspace guard.** Run a variant in an empty scratch dir with unrelated files.
   - Expected: agent confirms before scattering project docs, or offers a no-files session.

## Pass criteria (verify by file inspection)

- `CONTEXT.md` exists at repo root, is a pure glossary (no file paths, columns, or code), uses canonical terms.
- `docs/adr/NNNN-*.md` exists only for decision(s) meeting the three-part bar; no trivial ADRs.
- Docs were written during, not after, the interview (check via the transcript ordering).
- Grilling gate held throughout.
- Ends with a resolved-scope restatement pointing at the files written.
