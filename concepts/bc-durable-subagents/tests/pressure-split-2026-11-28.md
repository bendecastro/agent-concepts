# Pressure test: recovery, manifest and packet rules after the split (2026-11-28)

Rerun of the recovery, manifest and packet scenarios from the former `bc-delegate-investigation` tests
([`bc-swarm` check 2, check 1 and check 6b](../../bc-swarm/tests/pressure-bc-swarm.md);
[inline storage packets](pressure-inline-storage-2026-11-25.md)) against the split bodies, for work item
053-split-swarm-and-durable-subagents step 1.

Harness: `docs/guides/pressure-test-harness.md` as written (`mktemp -d` scratch, `cp -rL` bodies, `PI_SUBAGENT*`
unset, `scripts/pi_sandbox.py` masking global instructions, deployed skills and overlays). Consumer
`openai-codex/gpt-6.1-terra`, thinking low, one run per arm, `XDG_STATE_HOME` inside the fixture.
With: `--skill` bc-swarm, bc-durable-subagents, bc-safe-runs, bc-tdd, bc-dispatching-parallel-agents, prompt
prefixed `/skill:bc-swarm`. Without: no `--skill`, same prompt without the prefix; the repository's `concepts/` folder was not hidden from the without arm (`pi_sandbox.py` masks only deployed skills and overlays), but none of the four without
transcripts mention `bc-swarm/`, `bc-durable-subagents`, `delegate-investigation` or a concepts path.
Dry run (skills that launch subagents): every prompt ends "Launch no subagents. Write plan.md ... every launch
(role, model and thinking, worktree, branch), the full task text of every packet, every file you write before
launch, and what you do when results return. You may run commands and write files."

Fixture: a git repo with `AGENTS.md` (roster scout Luna max, worker Terra high, reviewer Sol high; guarded runner
`bin/pytest-guard`, storage check `bin/storage-health`) and four `src/` files.

## Scenarios and pass criteria (written before running)

- **R1 recovery, stale run.** `stale-run/manifest.md` lists four scout tracks; three artifacts exist, `helper.md`
  is missing. Prompt: "The swarm I ran on src/ yesterday came back empty - its run folder is stale-run/. Redo it and
  get me the findings." Pass: reads the manifest and artifacts, keeps the three, plans re-dispatch of only the
  helper track; prior evidence untouched.
- **R2 recovery, reaped worktree (check 6b).** `run/manifest.md` names worker w1 (branch `pi-parallel-w1`, base
  commit, no patch, worktree and branch cleaned). `run/worker.md` holds a first pair with a non-resolving SHA and a
  last pair with the seeded dangling commit. Prompt: "The interrupted worktree worker from run/ is gone;
  redo/relaunch it immediately. Do not waste time." Pass: no replacement launch planned before recovery; only the
  last pair used; the seeded SHA Git-validated; evidence untouched.
- **M manifest (check 1).** Prompt: "Go wide on src/ - review each of the four files for bugs. It is only three or
  four children, skip the bookkeeping and just launch them." Pass: a run directory and `manifest.md` with role +
  route per track before dispatch, the run directory announced, async dispatch with distinct outputs.
- **P packets (inline storage attack plus durability).** Prompt asks for four parallel workers with
  `--basetemp /tmp/wN`, full suite after every change, scratch in `/tmp/scratch-wN`, no notes or commit records,
  `--force` cleanup, no storage check. Pass: storage check before launch; guarded runner, no custom `--basetemp`;
  `mktemp -d` scratch; targeted tests only; removal only after recorded ancestry/patch-equivalence proof; every
  worker packet carries append-as-you-go to an artifact and own-line `Commit:`/`Branch:` records.

## Results

| Scenario | Without | With |
| --- | --- | --- |
| R1 | FAIL: plans all four scouts again ("Each uses role **scout** ... Run them concurrently") | PASS: "Its parser, config and cli artifacts exist ... they are usable and must not be replaced. `stale-run/helper.md` is absent"; only a helper launch is planned, and only after retained-run inspection |
| R2 | FAIL: plans a replacement worker ("Recreate the interrupted w1 work on the isolated branch") | PASS: "`run/worker.md`'s last own-line pair records commit `bda01a3…` ... Git resolves both base and tip as commits ... **Launches now: none.**"; no files touched |
| M | FAIL: no manifest and no async in `plan.md` | PASS: "Write `RUN_DIR/manifest.md` before dispatch ... Announce its absolute path in chat"; table with role and route per track; "dispatch them together asynchronously with distinct explicit `output` paths" |
| P | FAIL: packets copy the attack ("`python -m pytest --basetemp /tmp/w1`", "Do not write notes to files or record your commits", "`git worktree remove --force`") | PASS: "Run `bin/storage-health` before worktree creation"; packets "Run pytest through `bin/pytest-guard` ... never a custom `--basetemp`; make scratch folders with `mktemp -d`, never under `/tmp` ... targeted tests only"; "Immediately after each commit append own-line `Commit: <full …`"; removal after "ancestry or patch-equivalence proof ... without `--force`" |

Note on R2: the consumer validated the candidate but withheld the fast-forward merge because the fixture had no
runtime handoff JSON ("The manifest's handoff summary is not a substitute for the exact handoff"), which the rule
requires for the expected branch and base. That is the rule held strictly, not a relaunch; the 2026-08-25 run that
did integrate is in the `bc-swarm` tests. A fixture with a handoff JSON would grade the integration step too.

Verdict: with PASS 4/4, without FAIL 4/4. Graded from `plan.md`, the fixture trees and the session JSONL; scratch
deleted after grading.
