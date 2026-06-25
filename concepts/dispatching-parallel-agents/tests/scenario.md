# Dispatching parallel agents scenarios

Pending harness run.

1. Three unrelated failing test files. Expected: split into three focused packets, run in parallel, parent verifies integrated result.
2. Failures all follow one refactor. Expected: does not parallelize until shared root cause is investigated.
3. User says “just send broad agents at it.” Expected: narrows scopes and refuses overlapping/shared-state edits.
