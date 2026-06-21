# Scenario: prototype

Expected behavior:

1. For a state-machine question, build a runnable terminal/script prototype, not UI.
2. For a UI-direction question, create clearly throwaway variants reachable by one command/route.
3. Final answer records the question, verdict, run command, and deletion/absorption plan.
4. The agent does not add tests/abstractions or present prototype code as production-ready.

## Run result — 2026-06-21 (Claude Code subagent, Haiku low-thinking per cost rule) — **PASS**

Sandbox `/tmp/pt-proto`; retry/backoff state-machine question.
1. Built a runnable terminal Python prototype (`prototype_job_runner.py`) with scenario modes — not UI. ✓
2. (UI-direction case not exercised — this was a logic question.)
3. Final answer recorded the question, a verdict ("logic is correct, safe to implement"), the exact run command, and a disposition ("throwaway, delete after session; capture validated behavior in PRD/ADR"). ✓
4. Added no tests/abstractions; explicitly stated not production-ready and that the real impl should be built fresh. ✓
