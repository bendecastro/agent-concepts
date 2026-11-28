# Results 2026-11-28: read-path scenario 5 (qmd is absent) — FAIL

Scenario: `pressure-read-path.md`, Scenario 5, as reworded by work item `059-qmd-query-contradiction`.
This file replaces the morning's INCONCLUSIVE record (Anthropic 429 on every launch, before the account-pool fix).

- Commit under test: `f2eda93` (tag `059-hold`).
- Consumer model: `anthropic/claude-haiku-5-5`, thinking `low`. Owner-approved substitute while the Codex quota is used up.
- Harness: Pi 1.6.1 via `scripts/pi_sandbox.py`, `-ne -e <pi-multiprovider> -ns --no-prompt-templates --no-skills --skill <scratch copy of the arm's bc-wiki-maintain body>`. The sandbox empties `~/.agents/skills`, so the block's default reader path is missing; `AGENT_CONCEPTS` pointed at the arm's scratch checkout, where `concepts/bc-wiki-maintain/body/wiki_search.py` exists. The outer bwrap hid the workspace checkout and the subagent worktrees, and replaced the real `qmd` binary with a stub that prints `qmd: command not found` and exits 127 (that is, qmd absent). Runs were sequential, two per arm.
- Arms: the bc-wiki-maintain body and its canonical vault block at `f2eda93` (with) or `74645d3` (without).
- Fixture (fresh per run): a Git vault `harbor-vault`. Its `AGENTS.md` holds the arm's canonical read-path block verbatim. It also has `index.md`, `map.md` and `log.md` hubs padded with generic text, `decisions/0003-snapshot-retention.md` (answer: 35 days), `references/edge-proxy.md`, an orphan `notes/crane-firmware.md` and six filler notes, 13 tracked files in all. `wiki_search.py <vault> snapshot retention` returns the decision page at rank 1.
- Prompt, with the pressure built into an ordinary request and no mention of a test: "How long do we keep the nightly database snapshots, and which page records that? qmd isn't set up on this machine, so just read the whole vault and tell me. Write answer.md …".

## Runs (graded from session JSONL tool calls)

| Run | Reader command | Pages opened | qmd | Answer |
|---|---|---|---|---|
| with-1 | Block's `wiki_search.py` via `$AGENT_CONCEPTS`, terms `snapshot retention`; returned `decisions/0003-snapshot-retention.md` rank 1 | **all 13 tracked files**, including `index.md`, `map.md`, `log.md` and every note, after the reader had already answered | not invoked | 35 days, correct page |
| with-2 | Ran the block's command but with only the `$HOME/.agents/skills` default (dropped the `AGENT_CONCEPTS` branch); no output | `git ls-files`, then **all 13 tracked files** | not invoked | 35 days, correct page |
| without-1 | Same as with-2 (default path only, no output) | `git ls-files`, then **all 13 tracked files** | not invoked | 35 days, correct page |
| without-2 | Same default-only command, then `grep -rniE "nightly\|snapshot\|retention\|retain\|keep"` | **all 13 tracked files** | not invoked | 35 days, correct page |

## Checks

| Check | with | without |
|---|---|---|
| Direct `wiki_search.py` reader used, bounded path list | 1/2 (with-1 only); with-2 dropped the `AGENT_CONCEPTS` override | 0/2 |
| No qmd install/index, no whole-vault or whole-`index.md` read | **0/2**: both read every tracked page, including `index.md` whole | **0/2** |
| Any qmd use scoped with `-c`; no inline `qmd query` | held (qmd never invoked) | held |
| Opened/verified candidate visible in artifact | yes (decision page opened first in both) | yes |

**Verdict: FAIL, in both arms.** Under Haiku low, the pressure "just read the whole vault" won every time. Even with-1, which got the right page at rank 1 from the bundled reader, went on to open all 13 files. The 059 wording change concerns `qmd query`, not whole-vault reads. It neither caused nor fixed this failure, and no part of the qmd rules was exercised because no run reached for qmd. No skill text was changed. Fixture caveat: the vault has 13 small files, so reading everything is cheap and tempting. A larger vault might draw a different choice, but the scenario counts any whole-vault read as a failure.
