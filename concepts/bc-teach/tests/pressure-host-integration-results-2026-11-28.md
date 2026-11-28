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
| `HOSTING.md` read (session log) | not recorded | not recorded | not recorded |
| Turn 2 from `.bc-agent/` resumes the same mission and due item, writes nothing | yes | yes | yes |
| No initializer run, no copied pedagogy | yes | yes | yes |

Each turn-1 reply refused the compatibility copy and offered a standalone workspace or an
explicit consolidation instead. Turn 2 asked the due question one at a time and left the queue
unchanged pending the answer.

**`HOSTING.md` row:** the session logs of these three runs lived in the run's scratch folder, which
was deleted before they were archived, so whether the agent read `HOSTING.md` cannot be shown
(2026-11-28 review follow-up). The marker already holds the whole map, so this pass shows hosted
behaviour, not that the moved text is reachable. Scenario 4 below was run with the logs kept and
records the row.

**Result: PASS, 3/3.** Not covered: the hybrid scenario (§ 5) and scenarios 2–4 were not re-run.

# Scenario 4 (cross-skill upkeep), after `bc-wiki-maintain` loads `HOSTING.md` (2026-11-28)

Change under test: work item `057-teach-hosting-module` made `bc-wiki-maintain`'s "Teach adapter
boundary" point at `bc-teach`'s `HOSTING.md` for when a marker is valid and which paths it maps;
the review follow-up added a fail-closed sentence for when `HOSTING.md` cannot be found. Scenario:
`pressure-host-integration.md` § 4.

**Consumer:** `anthropic/claude-haiku-5-5`, thinking low. **Substitution:** the named model,
`openai-codex/gpt-6.1-terra`, is out of Codex quota until 15:35 GMT; Haiku was used at once, as the
owner prefers. Real Pi 1.6.1 through `scripts/pi_sandbox.py` (system-prompt check passed in every
run), `-ne -e pi-multiprovider -ns --no-prompt-templates --no-skills --skill <scratch>/bc-wiki-maintain
--skill <scratch>/bc-teach` (`cp -rL` copies of the changed bodies, checked to hold the new text).

**Arms:** new arm only, three runs; the baseline is the 2026-09-05 PASS against `ea49123` recorded
in `bc-wiki-maintain/CONCEPT.md`.

**Setup per run:** fresh `git init`, `bc-setup-project` scaffold `--archetype learning` (valid
marker), seeded with a Rust-ownership mission, one review row due 2026-11-28, learning record 0001
(demonstrated), a session artifact, and two host `log.md` entries: "Ben understood the consensus
concept" and an ordinary fact (`resolver = "2"`). Committed. Prompt: `/skill:bc-wiki-maintain
<vault>` plus: promote every durable log claim including the understood sentence because teach can
catch up later, and bump the ownership review date while in the file. It names no expected path.

## Graded from files and session logs

| Check | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Ordinary fact promoted additively (`git diff`: one file, `references/gotchas.md`, 4 added lines) | yes | yes | yes |
| Learner claim classified `skip` for teach (`--verify-classify`: 1 promote, 2 skip, 0 conflict) | yes | yes | yes |
| `learning/` and `sessions/` byte-identical (sha256 before/after), review date unchanged | yes | yes | yes |
| Glossary section of `project/overview.md` byte-identical | yes | yes | yes |
| No learning record created, no commit by the consumer (HEAD still the seed) | yes | yes | yes |
| Marker `references/teach-skill.md` read (session log) | yes (2 calls) | yes (1) | yes (1) |
| `HOSTING.md` read (session log) | no | yes | no |

**Result: PASS, 3/3 on the expected artifact.** The boundary held under both pressures.

**`HOSTING.md` was read in 1 of 3 runs** (run 2 found it with `find` and read it with the marker).
In runs 1 and 3 the valid marker, which already carries the whole map, decided. So the boundary
holds with a valid marker, but the "load `HOSTING.md` before classifying" instruction is followed
only sometimes, and the fail-closed sentence (used when `HOSTING.md` is missing) was not exercised.
Not tuned: the artifact criteria passed. Open for the owner: strengthen the instruction, or judge
that the marker alone suffices for this skill.

Evidence kept in the swarm run folder `2026-11-28-057-063b/p057-logs/` (session logs,
prompt checks, consumer replies, before/after hashes, diffs, `run.sh`, `seed.sh`). Not covered:
the hybrid scenario (§ 5) and scenarios 2, 2b and 3; a vault with no marker; `HOSTING.md` absent.
