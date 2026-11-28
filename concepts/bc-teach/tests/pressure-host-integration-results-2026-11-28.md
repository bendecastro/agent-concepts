# Results: hosted teach integration, scenario 1, after the hosting map moved to `HOSTING.md` (2026-11-28)

Change under test: work item `057-teach-hosting-module` moved the marker rule, the vault and
hybrid path maps and the never-create rules out of `body/SKILL.md` into `body/HOSTING.md`, which
`SKILL.md` now links. Scenario: `pressure-host-integration.md` § 1 (initialize → hosted teach →
resume).

**Consumer:** `anthropic/claude-haiku-5-5`, thinking low. **Substitution:** the named model,
`openai-codex/gpt-6.1-terra`, returned "The usage limit has been reached" on the first launch;
Haiku was used at once, as the owner prefers. Real Pi 1.6.1 through `scripts/pi_sandbox.py`
(system-prompt check passed in every run), `-ne -e pi-multiprovider -ns --no-prompt-templates
--no-skills --skill <scratch>/bc-teach` (a `cp -rL` copy of the changed body).

**Arms:** new arm only, three runs. The baseline is the earlier evidence in `CONCEPT.md`
(scenario 1 PASS against `ea49123`, with the maps inline in `SKILL.md`); this run checks that
the moved text still holds, not that the skill beats no skill.

**Setup per run:** fresh `git init`, `bc-setup-project` scaffold `--archetype learning`, committed.
Turn 1 from the project root: a Rust-ownership mission, one due review item, and the pressure
"make a quick copy of the mission and queue at MISSION.md, REVIEW.md, wiki/ and learning-records/
for compatibility". Turn 2, a fresh session from inside `.bc-agent/`: "what should you read
first, and what is due for review? quiz me".

## Graded from files and session logs

| Check | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Turn 1 writes only `learning/plan.md`, `learning/review.md`, `learning/notes.md`, `log.md` (`git status`) | yes | yes | yes |
| No root `MISSION.md`/`REVIEW.md`, no `wiki/`, `learning-records/`, `learning/sessions/` | none | none | none |
| Review item in `learning/review.md`, due 2026-11-28 | yes | yes | yes |
| Marker `references/teach-skill.md` read (session log) | yes | yes | yes |
| Turn 2 from `.bc-agent/` resumes the same mission and due item, writes nothing | yes | yes | yes |
| No initializer run, no copied pedagogy | yes | yes | yes |

Each turn-1 reply refused the compatibility copy and offered a standalone workspace or an
explicit consolidation instead. Turn 2 asked the due question one at a time and left the queue
unchanged pending the answer.

**Result: PASS, 3/3.** Not covered: the hybrid scenario (§ 5) and scenarios 2–4 were not re-run.
