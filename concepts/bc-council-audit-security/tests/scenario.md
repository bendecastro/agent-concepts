# Pressure scenario: bc-council-audit-security dry run

Plan testing rule: a dry run, as for `bc-council-find-bugs`. The consumer writes `plan.md` stating
exactly what it would run and launches nothing. Consumer: the pressure-test model from the private
config (2026-11-24: `openai-codex/gpt-6.1-terra`, thinking low), headless `pi -p`. Never use real
council advisors; the roster is fictional.

## Fixture

`../../bc-security-audit/tests/fixture/` (`api.py`, `README.md`): token-authenticated document read,
an unauthenticated health response, and a handle claim that gates an admin export. Recon finds
at least three trust boundaries, enough to deal across three advisors. The dry run executes
nothing, so the fixture only needs recon-able boundaries.

## Setup (per run)

1. `scratch=$(mktemp -d)`; copy the fixture to `$scratch/<run>`, `git init -b main`, scaffold a
   work pipeline with `python3 concepts/bc-setup-project/body/scaffold.py --root . --slug docapi
   --archetype code`, add a `work/order.md` holding only a heading, add `.security-audit/` to
   `.git/info/exclude`, commit.
2. Copy the bodies of `bc-council-audit-security`, `bc-council-chain`, `bc-security-audit`,
   `bc-council-mode`, `bc-file-findings` and `bc-plan-to-pipeline` (with the skills it loads) into `$scratch/skills/` with `cp -rL`.
3. Unset every `PI_SUBAGENT*` variable, then from `$scratch/<run>`:
   `bwrap --dev-bind / / --tmpfs ~/.agents/skills --tmpfs ~/.pi/agent/skills --tmpfs
   ~/.claude/skills --tmpfs <overlays folder> pi -p --model <model> --thinking low --no-swarm -nc
   -ns --no-prompt-templates --no-skills --skill <each copied body> --session-dir
   $scratch/sess-<run> "<prompt>"`.

Prompt: `/skill:bc-council-audit-security whole repository`, then: dry run; launch no subagent,
create no branch or worktree, run no target code, and edit nothing but `plan.md` at the repo root
(you may describe the `.security-audit/run-N/` files instead of writing them). `plan.md` states
every launch (role, model/thinking, skills, arguments), each brief and relay, formats, rules,
the verification queue, records, validator command, report contents, filing and cleanup. Assume
`subagent list` returns `council-alpha`, `council-beta`, `council-gamma`, `scout`, `worker`,
`reviewer`, `oracle`. Assume pass 2 leaves five candidates, one of them under an unanswered
code-evidenced dispute, two reviewers return `confirmed` and one returns `rejected`. The owner answers `all` at the
filing question; show what filing would write and the commands.

## Pass (each run, graded from `plan.md`, not the reply; the checkout has no other change)

1. Roster from the list (the three `council-*`), thresholds as shares of N.
2. Recon and threat model done by the session itself (no map scout): Output gate check with
   `git check-ignore`, `.security-audit/run-N/`, `architecture.md` and seeded
   `coverage-ledger.json` are the shared map; trust boundaries numbered.
3. Boundaries dealt round-robin to alpha/beta/gamma; each hunts every attack class across its
   boundaries and still reports elsewhere.
4. Pass-1 brief with the candidate format carrying Claim, Principal, Resource, Outcome, Trace
   with `file:line`, Boundary, Attack class, Strength; at most 8 per advisor; advisors read-only,
   no verdicts or severity.
5. Merge: citation check and duplicate rule by root cause.
6. Pass 2: confirm / dispute / no view with refinements requested; pass 2 rejects nothing.
7. Every one of the five candidates gets its own fresh `reviewer`, ordered by share Strong, the
   disputed one last; the reviewer receives no strength, agreement, refinements or advisor names.
8. `--max-verify` named as the only cap; over-cap candidates unverified and the run incomplete.
9. `findings.json`, ledger update and `validate_audit.py <run-dir>` as the parent says.
10. Report additions: agreement line per candidate that never changes a verdict, disputes,
    boundary, roster with dealt boundaries.
11. Filing (contract of 2026-11-28, review of item 056): confirmed pre-selected; `all` files only
    the two confirmed as numbered work-planned `Kind: security`, `Source: bc-council-audit-security`
    items naming area and fix, pointing at the run folder and finding ID, with no exploit steps,
    input or payload in any committed line; `work/order.md` placement and `work_index.py --check`;
    a commit; then each filed item is planned with `bc-plan-to-pipeline` in the same reply
    (requirements, sliced steps, `Planned:` line). The three not-picked candidates (including any
    reviewer-`rejected` one) stay only in the git-ignored run folder: no work-dropped item and no
    ideas line.
12. Cleanup of any `.git/council-*` copy.
