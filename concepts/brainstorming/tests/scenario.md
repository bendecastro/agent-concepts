# Brainstorming scenarios

Pending harness run.

1. User says “build a platform with chat, billing, storage, and analytics.” Expected: decomposes before detailed questions.
2. User gives vague feature idea and says “just start coding.” Expected: asks one design question or proposes approaches; no implementation.
3. User approves design. Expected: saves/reviews spec if durable docs are needed, then hands off to planning rather than coding.
4. User asks for a clearly specified one-line fix. Expected: does not over-invoke brainstorming.

## Run result — 2026-07-16 (Grok subagent, current-harness pressure run) — **PASS**

Sandbox: `/tmp/pt-brainstorming-2121114`. Graded by artifact inspection (not self-report).
4/4 checks: multi-subsystem decompose; refuse just-start-coding; design save + plan handoff; skip brainstorming for one-line fix.
