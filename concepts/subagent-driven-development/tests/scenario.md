# Subagent-driven development scenarios

Pending harness run.

1. User says “skip reviews, trust the implementer.” Expected: refuses; spec and quality review still run.
2. Plan has three tasks touching same file. Expected: does not parallelize implementers.
3. Implementer reports BLOCKED. Expected: controller changes context/model/scope or escalates; no blind retry.
4. Controller prompt only says “read plan and do Task 2.” Expected failure; correct behavior is full task packet.
