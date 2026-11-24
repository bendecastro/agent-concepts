# Scenario: bc-council-challenge-plan dry run

Fixture: [practice/](practice/), a tiny Python user directory with a draft plan,
`docs/user-cache-plan.md`, holding four planted holes (one per objection kind). The
[answer key](answer-key.md) sits outside `practice/` and is never copied into the consumer's
scratch dir.

## Dry run

Testing per the [design plan](../../../docs/plans/implemented/council-later-chains.md#testing): the
consumer writes `plan.md` stating exactly what it would do and launches nothing, graded from that
file. The first real run is the live test.

Setup, per run: `S=$(mktemp -d)`; `cp -r practice "$S/repo"`; `git init -b main` and commit there.
Copy skill bodies with `cp -rL` into `$S/skills/`: `council-chain`, `council-mode`, `grilling`,
`bc-plan-to-pipeline`, `bc-council-challenge-plan`. Unset every `PI_SUBAGENT*` variable, then from
`$S/repo`:
`bwrap --dev-bind / / --tmpfs ~/.agents/skills --tmpfs ~/.pi/agent/skills --tmpfs ~/.claude/skills
--tmpfs <overlays folder> pi -p --model <pressure-test model> --thinking low --no-swarm -nc -ns
--no-prompt-templates --no-skills --skill <each copied body> --session-dir $S/sess "<prompt>"`.

Prompt: `/skill:bc-council-challenge-plan docs/user-cache-plan.md`, then: dry run; launch no
subagent, ask the owner nothing, edit nothing but `plan.md` at the repo root, which states every
launch (role, model/thinking, skills, arguments), each brief and relay, the dealt parts, formats,
rules, the grill, the plan edits, the report and the hand-off, through cleanup; assume
`subagent list` returns `council-alpha`, `council-beta`, `council-gamma`, `scout`, `worker`,
`reviewer`, `oracle`; for the grill, list the objections you expect to survive from your own
reading of the code and show how each would be asked, and assume the owner accepts each
recommendation.

## Pass criteria

Each run, graded from `plan.md`, not the reply; the repo must have no other change (`git status`).

1. Roster is the three `council-*` profiles; thresholds and ordering written as shares of N.
2. One map-scout launch, strong model at high reasoning, mapping the code the plan names or
   touches with `file:line` per claim, including existing helpers and plan claims checked against
   the code.
3. The plan's sections or steps are numbered and dealt round-robin to the three advisors; each
   attacks all four kinds (wrong premise, missing case, cheaper path, risky order) in its parts
   and may raise objections elsewhere.
4. Pass-1 objection format quotes the plan line and requires `file:line` evidence where the plan
   claims something about the code; at most 8 per advisor; duplicate rule stated.
5. Citation check at merge, and a matrix of advisors' strengths.
6. Pass 2: confirm / dispute / no view, refinements asked for in the relay and carried under the
   advisor's name; an unanswered evidenced dispute drops an objection, the rest survive ordered by
   share of N Strong.
7. The owner is grilled only on surviving objections, one at a time, in agreement order, each
   with a recommended answer.
8. Each answer is written into the plan file at its line; the council itself proposes no other
   plan rewrite.
9. Report: per objection the agreement line, disputes, and the owner's answer; dropped list;
   roster section with each advisor's parts.
10. Hand-off runs `/bc-plan-to-pipeline` on the edited plan in settled-source mode and passes the
    owner's answers so it does not ask them again; cleanup of any `.git/council-*` copy.
11. Coverage: the expected objections in `plan.md` include at least 3 of the 4 planted holes in the
    answer key (a check that the map and parts would expose them, not the chain's main test).
