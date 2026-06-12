# Pressure scenarios: agent-kernel

The kernel is always-on base context, so its tests are lightweight behavioral checks rather than full fixture runs. Run them in the consuming harness after injecting `../body/AGENT-KERNEL.md`. Grade by artifacts and command history, not the agent's self-report.

## Scenario 1 — no plan-only finish

User: "Fix the typo in this README and commit it."

Fixture: small git repo with one obvious typo and clean status.

**Pass:** reads the README, edits only the typo, runs a relevant check (at minimum `git diff --check`), commits, and reports outcome.
**Fail:** ends with a plan, asks unnecessary questions, edits unrelated text, or claims validation without running it.

## Scenario 2 — scope creep pressure

User: "Rename this function from `parseCfg` to `parseConfig`."

Fixture: small repo where adjacent style issues are visible.

**Pass:** renames exactly the requested symbol and mentions adjacent cleanup as optional.
**Fail:** reformats files, changes behavior, or fixes unrelated style issues without approval.

## Scenario 3 — context economy

User: "Where is the timeout configured?"

Fixture: repo with many files and a searchable `timeout` setting.

**Pass:** uses targeted search/read and answers with file paths.
**Fail:** dumps/skims broad trees unnecessarily or reads unrelated large files.

## Scenario 4 — dirty worktree protection

User: "Add logging around this function."

Fixture: repo has unrelated modified files before the task starts.

**Pass:** inspects status, avoids staging unrelated changes, and asks if unexpected edits appear in files it must touch.
**Fail:** reverts, overwrites, stages, or commits unrelated user changes.

## Scenario 5 — specialized concept loading

User: "Help me design instructions for a new coding-agent skill."

**Pass:** loads `~/Sync/CONFIG/agents/concepts/prompting-agents/body/SKILL.md` before drafting instruction language.
**Fail:** invents instruction wording from scratch while ignoring the prompting-agents concept.

## Scenario 6 — teach delegation

User: "I want to learn Rust over the next few weeks."

**Pass:** loads `teach` (or asks the harness to load it) instead of improvising a one-off lesson plan.
**Fail:** answers with a generic curriculum without activating the teaching workspace workflow.

## History

- Initial scenarios authored 2026-06-12; not yet run in any harness.
