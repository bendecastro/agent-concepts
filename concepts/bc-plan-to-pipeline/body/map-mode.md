# Map mode

A **map** holds decisions, never build steps: `/bc-pipeline-to-done` never builds a map, and a map never carries `Ready for agent: yes`. The entry file's Map or plan check decides when to chart one.

## Where a map lives

Maps live in project files (see [Where project files go](SKILL.md#where-project-files-go)); numbering, `Source:`, `Blocked by:`, `work/order.md` placement and the worktree rule are unchanged.

- **With a "Where things go" table:** a work item in work-planned with `Kind: map`. Its `Done when:` names the destination reached and the slice step done. Under the header, write `Work this map with /bc-plan-to-pipeline <item>, one step per session (map mode).` Write `Planned: bc-plan-to-pipeline <date>` once the map and its first steps are written, so moving it to active follows the project's normal rule. No `Dependencies:` line; the slice step asks that question.
- **Without a "Where things go" table:** `docs/changes/<slug>/map.md` (in a legacy `.bc-agent/` vault, its plans folder), holding the sections below and its steps.

If asked to file the map itself in GitHub instead of in project files, record the idea and its unsettled question as one line in `work/0-ideas.md` (use the project's ideas role if it names one; without a table, note the request in `map.md` itself). Create no map issues.

## Map sections

- **Destination** — what reaching the end looks like, one or two lines: the decision, spec or change this effort is finding its way to. It fixes the scope.
- **Decisions so far** — one line per resolved step: its gist and where its detail lives (the step's answer). A decision lives in one place; the map never restates it.
- **Not yet specified** — in-scope questions you can see coming but cannot yet state sharply. Write them as loosely as the view allows; do not pre-cut them into steps.
- **Out of scope** — work ruled beyond the destination, one line each with why. It never graduates; it returns only if the destination is redrawn, as a new effort.

Then `## Steps` in the work item or `map.md`. Each step is one decision, typed:

- **grilling** — a conversation with the owner (`bc-grilling` + `bc-domain-modeling`). Only the owner's words resolve it; never answer for them.
- **research** — a fact outside this repository a decision waits on (`bc-research`).
- **prototype** — a rough artifact to react to when "how should it look or behave" is the question. `/bc-prototype` is user-invoked: give the owner the command with the step's question and record its verdict.
- **task** — work that must happen before a decision can be made (access, a sign-up, data to look at). Do it if you can; otherwise hand the owner a precise checklist. Its answer records what was done and the facts later steps need.

A step exists only when its question can be stated sharply now, even if it is blocked; otherwise it stays in Not yet specified. Write each step as its type, its question, and its blockers (by step title). The last step is always **Slice**, blocked by every other step.

## Chart the map

The entry file's absent-owner rule takes precedence: with no one to answer, only a research or task question that needs no owner answer may still make a map.

Name the destination (usually what the grill settled), put settled answers in Decisions so far, write each open question the session could not settle as a typed step, sketch the rest into Not yet specified, and add Slice. Do not draft a PRD, `## Requirements` or build steps. Research steps may start now as parallel subagents with `bc-research`. For each result that returns during charting, apply Work the map steps 3 and 4; that counts as the step's session. Leave all other steps open. Then report: where the map is, the questions that made it a map, the next step to work, and how to switch ("say 'just slice it' to plan build items now").

## Work the map

When the source is a map, resolve **one** step per session; several research steps may run in parallel as subagents.

1. Read the map's sections, not every step's detail. Take the step the owner named, or the first open step whose blockers are resolved. If Slice is the only open step and Not yet specified is not empty, turn each remaining question into a grilling step asking the owner to sharpen it or rule it out of scope.
2. Resolve it as its type says. A grilling step with no one to answer follows the entry file's absent-owner rule.
3. Record the answer under the step (link to a long answer in the item's or map's folder; turn a single-file item into a folder or use the project's research folder), then tick the step. Add one line to Decisions so far pointing at it.
4. Graduate any Not yet specified question the answer made sharp into a new step, removing it from that section. When an answer shows a step or question lies past the destination, remove it and add one line to Out of scope. Update or remove steps the decision invalidates; keep Slice blocked by every other step.
5. Stop and report the decision, the map's changes and the next step.

## Slice

When Slice is the only open step and Not yet specified is empty, run `/bc-plan-to-pipeline` afresh with the map as its **settled source** (not as a request to work the map). Follow the ordinary pipeline. Create new build items with `Source:` naming the map and `Kind:` from the work; never plan the map in place. If that run meets a question it cannot settle, add it to the map as a typed step that Slice waits on, leave Slice open, and stop. For a `map.md` source, use the plan home in the entry file's step 4.

Once that run has written the build artifacts and filed any required issues, point every `Blocked by:` that names the map at the new build item(s), tick Slice and move Decisions so far into `## Outcome`. Move a map item to work-done; for a change-folder map, the Outcome stays in `map.md`.
