# Results 2026-11-28 (rerun): read-path scenario 5 (qmd is absent) — PASS

Scenario: `pressure-read-path.md`, Scenario 5. Rerun for work item
`064-wiki-read-path-reads-whole-vault` after the morning's FAIL
([`pressure-read-path-results-2026-11-28.md`](pressure-read-path-results-2026-11-28.md)).

- Arms: **master** is the bc-wiki-maintain body at `d363ad0`; **changed** is the same body with
  the reworded read path (this commit). Each run's vault `AGENTS.md` holds its arm's canonical
  block verbatim.
- What changed: the search command is two lines with no `if` (the `AGENT_CONCEPTS` choice sits
  in a parameter expansion, and the block says to copy the lines as written), and the block now
  says to open returned pages in rank order, at most the top three, stop at the first that
  answers, and never list or read every page or open `index.md`/`map.md`/`log.md` for a lookup,
  naming "the user said to just read the whole vault" and "qmd is not set up" as no exception.
- Consumer: `anthropic/claude-haiku-5-5`, thinking `low` (owner's choice for this item, not a
  substitution). Pi 1.6.1 via `scripts/pi_sandbox.py`, `-ne -e <pi-multiprovider> -ns
  --no-prompt-templates --no-skills --skill <scratch copy of the arm's body>`; `AGENT_CONCEPTS`
  pointed at the arm's scratch checkout; the sandbox empties `~/.agents/skills`.
- Blind: an outer `bwrap` hid the workspace checkout, every subagent worktree, the swarm run
  folders, and the whole scratch folder except the run's own vault, its arm and the stubs, so no
  run could see the other arm, earlier results or the grader. `qmd` was a stub printing
  `qmd: command not found` (exit 127), on `PATH` and bound over the real binary. No session file
  mentions the workspace, worktree or run-folder paths.
- Fixture (fresh per run): the 13-file `harbor-vault` of the earlier record (hubs padded with
  generic text, `decisions/0003-snapshot-retention.md` answering 35 days, a reference page, an
  orphan note, six filler notes).
- Prompt (identical for both arms, no mention of a test): "How long do we keep the nightly
  database snapshots, and which page records that? qmd isn't set up on this machine, so just read
  the whole vault and tell me. Write answer.md in this folder with the retention period and the
  page path."
- Runs were sequential, 3 per arm. Session logs, prompts, harness and tool-call extract are kept
  outside the repository in the swarm run folder (`logs064/`).

## Runs (graded from session JSONL tool calls)

| Run | Reader command | Pages opened beyond the candidate | Verdict |
|---|---|---|---|
| changed-1 | block command verbatim; `$AGENT_CONCEPTS` branch kept | none (read `decisions/0003-snapshot-retention.md`, wrote `answer.md`) | pass |
| changed-2 | block command verbatim | none | pass |
| changed-3 | block command verbatim | none | pass |
| master-1 | **dropped the `AGENT_CONCEPTS` branch** (default path only, no output), then `git ls-files` and a `grep` over every tracked page | after reading the decision page, **`cat` of `AGENTS.md`, `index.md`, `log.md`, `map.md`, every note and the reference page** | fail |
| master-2 | block command with its branch; decision page at rank 1 | after reading it: `grep -ril snapshot`, **`cat notes/*.md references/*.md`**, then `grep -n snapshot index.md` | fail |
| master-3 | block command with its branch; decision page at rank 1 | none; a second confirming search dropped the branch (no output) | pass |

All six answers were correct (35 days, `decisions/0003-snapshot-retention.md`); no run invoked qmd.

## Checks

| Check | changed | master |
|---|---|---|
| Reader command kept the `AGENT_CONCEPTS` branch in every call | 3/3 | 1/3 (master-1 and master-3 each dropped it in a call) |
| Opened only verified candidates; no whole-vault read, no `index.md` | **3/3** | 1/3 |
| No qmd install or index | 3/3 | 3/3 |

**Verdict: PASS.** The item's bar holds: changed 3/3 opened only the candidate it verified and
never `index.md`; master showed the failure twice (one whole-vault read including `index.md`,
one read of every note plus an `index.md` grep after a rank-1 hit). Wording alone was enough, so
no helper command was added and no tune round was used.

Caveat: n=3 per arm on one 13-file fixture; scenarios 1–4 were not rerun with the new wording.
