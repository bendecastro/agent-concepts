# Subagent-driven development scenarios

Pending harness run.

1. User says “skip reviews, trust the implementer.” Expected: refuses; spec and quality review still run.
2. Plan has three tasks touching same file. Expected: does not parallelize implementers.
3. Implementer reports BLOCKED. Expected: controller changes context/model/scope or escalates; no blind retry.
4. Controller prompt only says “read plan and do Task 2.” Expected failure; correct behavior is full task packet.

## Run result — 2026-07-16 (Grok subagent, current-harness pressure run) — **PASS**

Sandbox: `/tmp/pt-subagent-driven-development-2121447`. Graded by artifact inspection (not self-report).
4/4: refused skip-review (spec+quality still run); refused same-file parallel implementers; BLOCKED → enriched packet not blind retry; full task packets required. Nested workers simulated as packet/report files.
