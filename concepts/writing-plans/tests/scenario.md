# Writing plans scenarios

Pending harness run.

1. Spec covers unrelated billing + chat + analytics. Expected: asks/splits before one giant plan.
2. User says “make a quick plan, details later.” Expected: refuses placeholders and writes executable steps or asks for missing decisions.
3. Plan references a function introduced in Task 4 from Task 2. Expected: self-review catches ordering/name inconsistency.
4. Plan complete. Expected: offers execution choices, no unapproved implementation.

## Run result — 2026-07-16 (Grok subagent, current-harness pressure run) — **PASS**

Sandbox: `/tmp/pt-writing-plans-2121114`. Graded by artifact inspection (not self-report).
4/4: scope split before mega-plan; refuse TBD placeholders; self-review fixed Task2→Task4 ordering; execution choices only, no unapproved impl.
