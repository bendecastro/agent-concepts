# Planning gets a map mode for work too big for one session

Why: `bc-plan-to-pipeline` assumes one grill settles every decision before it drafts a PRD and slices. An effort whose decisions need research, a prototype, a task first, or the owner's later thought has no home between sessions: decisions get made in chat and copied into items by hand (the kernel-in-every-install item), and the swarm review-loop rule's "return to planning" has nowhere to land. Matt Pocock's wayfinder skill (`docs/research/raw/ingested/pocock-wayfinder/`) solves this with a map of decision tickets; most of its other parts already exist here.
Done when: On the pressure-test model, a planning session on a vague idea whose grill leaves a question this session cannot settle writes a map item (not a PRD or build steps), and a small idea with nothing left open still goes straight to PRD and slicing, each 3 of 3 with master failing the map case at least once; the GitHub-tracker and change-folder homes are written and checked by reading.
Stage: next
Blocked by: 066-planning-go-ahead-is-not-build
Kind: feature
Source: owner request 2026-11-28 (wayfinder)
Planned: bc-plan-to-pipeline 2026-11-28
Ready for agent: yes
Dependencies: none new

## Requirements

Owner decisions (2026-11-28, in chat): 1a, 2a, 3a, 4b, 5a, 6a, as below.

- **When it is a map (5a).** After the grill (breadth-first for a raw idea), the agent decides by one observable test: is any question still open that this session cannot settle — it needs research the session cannot finish, a prototype to react to, a task done first (access, sign-up, data), or the owner said "not sure yet" / "let me think"? Any such question → map; none → today's path (PRD, slicing). Not a judgment of size. The owner can override either way ("make a map", "just slice it"); the report names the questions that made it a map and how to switch.
- **Where a map lives (1a, 6a).** Same three homes the skill already uses:
  - With a "Where things go" table: a work item with `Kind: map` in the normal folders (dashboard, `order.md`, `Blocked by:` unchanged).
  - With a GitHub tracker: a parent issue labelled `map`; decision steps are child issues, never labelled `ready-for-agent`.
  - Neither: `docs/changes/<slug>/map.md`.
- **Map sections.** Destination (what reaching the end looks like, one or two lines); Decisions so far (one line per resolved decision pointing to where its detail lives — a decision lives in one place); Not yet specified (in-scope questions not yet sharp enough to be a step; graduate to steps as the frontier advances); Out of scope (ruled beyond the destination; never graduates). Steps are decision steps, each typed grilling, research, prototype or task, using the existing skills (`bc-grilling` + `bc-domain-modeling`, `bc-research`, `bc-prototype`); a step is created only when its question can be stated sharply.
- **Working the map (3a).** A "work the map" mode of `bc-plan-to-pipeline` resolves one decision step per session (research steps may run in parallel as subagents), records the answer in the step's home, adds a line to Decisions so far, graduates fog, rules things out of scope. `bc-pipeline-to-done` never builds a map; a map never carries `Ready for agent: yes`. Moving the map to active follows the project's normal rule.
- **When the way is clear (2a).** The map's last step is "slice": run the normal PRD and slicing steps, which create ordinary build items (or issues); the map moves to done with Decisions so far as its Outcome.
- **"Plan, don't do".** Carry wayfinder's line that the pull to just do the work signals the edge of the map, next to 066's go-ahead rule (one home, pointer elsewhere).
- **Credit.** CONCEPT.md provenance cites `docs/research/raw/ingested/pocock-wayfinder/` (MIT); the raw source moves to `ingested/` when done.
- **Test (4b).** Terra low (`openai-codex/gpt-6.1-terra`), master skill vs changed, real Pi 1.6.1 via `scripts/pi_sandbox.py` with pi-multiprovider; blind baseline. If Codex is out of quota, wait for its reset rather than substituting (owner chose Terra).

## Steps

- [ ] **Map mode in the skill (held until the pressure test passes).** Map test, three homes, sections, work-the-map mode, slice-last step, `bc-pipeline-to-done` skipping maps if it needs a line; `relationships.json` edges for any new loads; CONCEPT.md provenance. Done when the skill text covers every Requirement with one home per rule, the GitHub and change-folder homes read correctly to a reviewer, and lint passes. Out of scope: an issue-tracker setup command, wayfinder's one-ticket-claim-by-assignee mechanics beyond the project's existing active rule.
- [ ] **Pressure test, then land.** Blocked by: Map mode in the skill. Two scenarios: a vague idea with an unsettled question (expect a map item with Destination, a typed decision step, no PRD or build steps) and a small settled idea (expect today's PRD and ready item). Done when the results file shows master and changed arms, 3 runs each per scenario on Terra low, graded from artifacts, changed passes both 3/3, master fails the map scenario at least once, and the change is merged. Out of scope: tuning unrelated planning rules.

## Outcome

_To be filled when finished or dropped._
