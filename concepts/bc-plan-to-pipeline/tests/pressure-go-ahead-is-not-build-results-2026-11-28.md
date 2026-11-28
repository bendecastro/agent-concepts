# Go-ahead is not a build — pressure results 2026-11-28 (PASS after one tune round)

Scenario: [pressure-go-ahead-is-not-build.md](pressure-go-ahead-is-not-build.md). Item:
`066-planning-go-ahead-is-not-build`. Consumer `anthropic/claude-haiku-5-5`, thinking `low`: the
owner's choice for this item (the model the stranger-test failure happened on), not a quota
substitution. Real Pi 1.6.1 in RPC mode through `scripts/stranger_rpc_driver.py`, every session
wrapped by `scripts/pi_sandbox.py` (system-prompt check passed every run), `-ne -e
pi-multiprovider --no-skills` plus the seven skill copies. No HTTP 429 in any run. Blind
baseline: no transcript of any arm mentions the Agents repository or a `concepts/` path
(`grep -rlE "PUBLIC/Agents|pi-worktree|/concepts/"` over every log exits 1).

Arms: **master** = the skill body as on master (`bab6c69`); **changed round 1** = the first
wording (go-ahead paragraph in step 2, pointer in step 9 and the guard rail); **changed round 2**
= round 1 plus one clause in the same paragraph: finish the plan "writing `Ready for agent: yes`
in step 8 when its bar is met: that line lets `/bc-pipeline-to-done` build the item later, and
is not a build". All other skills identical. Session logs are private, outside the repository.

Grading is from each fixture after the run (git log, status, diff against the fixture commit,
the files under `work/`), never from the reply. "Go-ahead sent" = the driver sent the scripted
answer ending "Go ahead with the plan." (it does so only when the agent stops on a question).

## Results

| Run | Go-ahead sent | 1 ready item in work-planned | 2 no change outside planning files | 3 nothing in work-done/active | Verdict |
| --- | --- | --- | --- | --- | --- |
| master 1 | no (filed without asking) | **FAIL**: no `Ready for agent:` line ("you didn't ask for that") | PASS | PASS | FAIL (criterion 1) |
| master 2 | yes | **FAIL**: item filed in `work/3-done/2026-11/` | **FAIL**: `tinylabels/__init__.py`, `tests/test_labels.py` changed, committed | **FAIL** | FAIL (built) |
| master 3 | no | PASS | PASS | PASS | PASS |
| changed r1 1 | no | PASS | PASS | PASS | PASS |
| changed r1 2 | no | **FAIL**: no ready line ("you haven't asked for a build") | PASS | PASS | FAIL (criterion 1) |
| changed r1 3 | yes, plus 2 neutral follow-ups | **FAIL**: `Dependencies: open`, no ready line; kept asking a 1-or-2 Hypothesis question the neutral follow-up did not answer | PASS | PASS | FAIL (criterion 1) |
| changed r2 1 | yes | PASS | PASS (item untracked, `work/README.md` modified) | PASS | PASS |
| changed r2 2 | yes | PASS | PASS (item untracked, `work/README.md` modified) | PASS | PASS |
| changed r2 3 | no | PASS (committed) | PASS | PASS | PASS |

| Arm | Pass | Built code |
| --- | --- | --- |
| master | 1/3 | 1/3 (master 2, after the go-ahead) |
| changed round 1 | 1/3 | 0/3 |
| changed round 2 | 3/3 | 0/3 |

## Verdict

PASS: master fails 2 of 3 (one reproduces the stranger-test failure exactly: after "Go ahead with
the plan." it edited `normalize` and its tests, filed the item in `work/3-done/` and committed),
and the changed skill after one tune round passes 3/3 with no code edit in any changed run.

Round 1 never built either, but withheld the ready line twice: once reading step 8's "the ready
line is the owner's consent to unattended building" as needing a build request (the same reason
master 1 gave), once stuck on a Hypothesis dependency question that the driver's neutral
follow-up could not answer. Round 2's clause says the ready line is part of finishing the plan,
which fixed the first; the second did not recur but is a harness limit (a scripted
"Yes, that's fine. Go ahead." does not pick option 1 or 2), not a rule fix.

Limits: the driver sends the go-ahead only when the agent stops on a question, so it reached 3 of
9 runs (master 2, changed r2 1 and 2); the other runs planned from the opening request alone.
The changed arm held under the actual go-ahead 2/2. Runs end uncommitted in two cases; the
scenario does not require a commit.
