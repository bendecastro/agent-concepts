# Map mode

A **map** plans an effort whose decisions cannot all be settled in one session. It holds decisions, never build steps: `/bc-pipeline-to-done` never builds a map, and a map never carries `Ready for agent: yes`. The entry file's map test (step 1) decides when to chart one; its go-ahead rule (step 2) applies here too.

## Where a map lives

The same three homes as a plan (see the entry file's mode choice and [Where project files go](SKILL.md#where-project-files-go)); numbering, `Source:`, `Kind:`, `Blocked by:`, `work/order.md` placement and the worktree rule are unchanged.

- **With a "Where things go" table:** a work item in work-planned with `Kind: map`. Its `Done when:` names the destination reached and the slice step done. Under the header, write `Work this map with /bc-plan-to-pipeline <item>, one step per session (map mode).` Write `Planned: bc-plan-to-pipeline <date>` once the map and its first steps are written, so moving it to active follows the project's normal rule. No `Dependencies:` line; the slice step asks that question.
- **With a GitHub tracker:** a parent issue titled `Map: <effort>`, labelled `map`, whose body holds the sections below. Each step is a child issue with `## Parent #<map>` in its body, a label naming its type (`map-grilling`, `map-research`, `map-prototype`, `map-task`, or `map-slice` for Slice) and `Blocked by #NN` lines for its blockers. Create missing labels first (`gh label create <label>`), then create the issues and add blocker lines with the real numbers. Never label a map or its steps `ready-for-agent`. With both a table and a tracker, the work item points to the map issue with `Issue: #<map>`; the map sections and steps live only in the issues, with no `## Steps` in the item.
- **Neither:** `docs/changes/<slug>/map.md`, holding the sections below and its steps.

## Map sections

- **Destination** — what reaching the end looks like, one or two lines: the decision, spec or change this effort is finding its way to. It fixes the scope.
- **Decisions so far** — one line per resolved step: its gist and where its detail lives (the step's answer). A decision lives in one place; the map never restates it.
- **Not yet specified** — in-scope questions you can see coming but cannot yet state sharply. Write them as loosely as the view allows; do not pre-cut them into steps.
- **Out of scope** — work ruled beyond the destination, one line each with why. It never graduates; it returns only if the destination is redrawn, as a new effort.

Then the **steps**: child issues with a tracker, otherwise `## Steps` in a work item or `map.md`. Each step is one decision, typed:

- **grilling** — a conversation with the owner (`bc-grilling` + `bc-domain-modeling`). Only the owner's words resolve it; never answer for them.
- **research** — a fact outside this repository a decision waits on (`bc-research`).
- **prototype** — a rough artifact to react to when "how should it look or behave" is the question. `/bc-prototype` is user-invoked: give the owner the command with the step's question and record its verdict.
- **task** — work that must happen before a decision can be made (access, a sign-up, data to look at). Do it if you can; otherwise hand the owner a precise checklist. Its answer records what was done and the facts later steps need.

A step exists only when its question can be stated sharply now, even if it is blocked; otherwise it stays in Not yet specified. Write each step as its type, its question, and its blockers (by step title). The last step is always **Slice**, blocked by every other step.

## Chart the map

The entry file's absent-owner rule takes precedence: with no one to answer, only a research or task question that needs no owner answer may still make a map. From an existing work item, chart in place: replace its `Kind:` with `Kind: map`, keeping the original kind's work for Slice.

Name the destination (usually what the grill settled), put settled answers in Decisions so far, write each open question the session could not settle as a typed step, sketch the rest into Not yet specified, and add Slice. Do not draft a PRD, `## Requirements` or build steps. Research steps may start now as parallel subagents with `bc-research`. If one returns during charting, record its answer as in Work the map step 3; that counts as the step's session. Leave all other steps open. Then report: where the map is, the questions that made it a map, the next step to work, and how to switch ("say 'just slice it' to plan build items now").

## Work the map

When the source is a map, resolve **one** step per session; several research steps may run in parallel as subagents.

1. Read the map's sections, not every step's detail. Take the step the owner named, or the first open step whose blockers are resolved.
2. Resolve it as its type says. A grilling step with no one to answer follows the entry file's absent-owner rule.
3. Record the answer in the step's home: under the step in a work item or `map.md` (link to a long answer in the item's or map's folder; turn a single-file item into a folder or use the project's research folder), or as a closing comment on its issue, then tick the step or close the issue. Add one line to Decisions so far pointing at it.
4. Graduate any Not yet specified question the answer made sharp into a new step, removing it from that section. When an answer shows a step or question lies past the destination, remove or close it and add one line to Out of scope. Update or remove steps the decision invalidates.
5. Stop and report the decision, the map's changes and the next step.

## Slice

When Slice is the only open step and Not yet specified is empty, run the entry file's steps 2 and 4–9 with the map as a settled source (see step 2's edge-of-the-map line; Slice still needs every other step resolved). The map is not the item to plan in place: create new build items (or slice issues), numbered as usual with `Source:` naming the map and `Kind:` from the work. Never add requirements or build steps to the map. With neither a table nor a tracker, write `prd.md` and `tasks.md` alongside `map.md`.

Once the build plan is published, tick Slice (or close its issue) and move Decisions so far into `## Outcome` in the map's home, including in `map.md`. Move the map item to work-done or close the map issue, as applicable. If both exist, the item's Outcome points to the issue's Outcome.
