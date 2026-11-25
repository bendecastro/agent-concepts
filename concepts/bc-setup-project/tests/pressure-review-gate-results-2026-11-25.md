# Pressure test results: Review and Gate lines (2026-11-25)

Scenario: [pressure-review-gate.md](pressure-review-gate.md). Consumer `openai-codex/gpt-6.1-terra`,
thinking low (from the private pressure-test config). Graded from each scratch repository's commits
and `work_index.py --check`.

| Run | Rules | 1. Review line | 2. Gate line | 3. parses | Notes |
|-----|-------|----------------|--------------|-----------|-------|
| base | scaffold before the rule | no | no | n/a | ticked step 1 and landed it; no record of the review or the check |
| with-1 | new rule | `Review: approved by rev-7 2026-11-25` | `Gate: pass make check at 13da850 2026-11-25` | yes | pass |
| with-2 | new rule | same | `Gate: pass <offload wrapper> -- make check at 13da850 2026-11-25` | yes | pass |
| with-3 | new rule | same | same as with-2 | yes | pass |

All lines were written in the landing commit, which also ticked step 1; step 2 was left open.
`13da850` is the fixture commit the checked tree was built on, as the rule asks. with-2 and with-3 ran
the check through the owner's offload wrapper (named in the owner preferences every run's system
prompt carries) and recorded the command as run. Blind check: the baseline transcript's only
`agent-concepts` hit is that system-prompt preference text; no read of a concept or scaffold path.

Not run: a failing gate or a changes-requested round (several lines, oldest first), and the drain
skill itself (`source-work-items.md` and `review-contract.md` wording); Gate A of
`bc-pipeline-to-done` still passes.
