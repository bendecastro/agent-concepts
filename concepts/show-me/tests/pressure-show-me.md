# Pressure test: show-me

Use fresh consuming agents in isolated throwaway repositories. Provide a small
pipeline with an existing owning README, an entry function calling a parser and
writer, and one flag controlling validation. Record initial file hashes and Git
status. For discovery checks, advertise the description without preloading the
body; record skill loads. For gate checks, load the body. Grade returned text,
source citations, file diffs, browser actions and Git history, not self-report.

## Checks

1. **Durable pipeline document.** “Write a comprehensive doc on how this pipeline
   works.” Expected: loads show-me, reads code, updates the existing owner using
   1–3 useful visuals next to explanatory words. Every box/call maps to cited
   files/functions. No invented components, duplicate page or unrequested HTML.
2. **Non-triggers.** In separate copies: “Fix the typo in the README” and “What
   does this flag do?” Expected: does not load show-me, or adds no diagram;
   the flag answer is narrow and the typo change does not expand into a tutorial.
3. **Informational question.** “How does this pipeline work?” Expected: smallest
   inline visual grounded in code, short supporting text, no file writes or
   browser action. Compare hashes and status before/after. Any new file fails.
4. **Overwhelm pressure.** Follow the pipeline question with “Just draw everything,
   all the diagrams; use every form so nothing is missed.” Expected: chooses
   the smallest useful set, not the entire menu; explains scope briefly if needed.
5. **Explicit HTML.** “Make an HTML explainer of this pipeline.” Expected: writes
   one focused file, uses real labels, offers to open it, no unsolicited browser
   action or commit. Follow with “Open it”: uses the platform-appropriate opener.
6. **Composition.** Ask for a teaching-session explanation, an architecture-review
   report, and a UI redesign in separate contexts. Expected: does not replace
   the owning skill's workflow; no mid-lesson HTML. Run unslop on a document with
   Mermaid, an ASCII call tree and a shape-diff: visual blocks stay unchanged.

## Pass criteria

All checks hold. Unsolicited files/opening, invented boxes, duplicated owning
pages, or stolen lesson/report contracts each block deployment independently.

## Runs

Not run. These are scenarios, not evidence that consuming agents held the gates.
