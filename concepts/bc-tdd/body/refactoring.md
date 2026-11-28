# Refactor candidates

After a green TDD cycle (all tests passing), look for:

- **Duplication** → extract a function/class.
- **Long methods** → break into private helpers (keep tests on the public interface).
- **Shallow modules** → combine or deepen (see `/bc-codebase-design`).
- **Feature envy** → move logic to where the data lives.
- **Primitive obsession** → introduce value objects.
- **Existing code** the new code reveals as problematic.

Load the `bc-safe-runs` skill. Else: guarded test runner (otherwise plain `pytest`; never custom `--basetemp`), scratch via `mktemp -d` not `/tmp`, targeted tests, configured storage health check (stop if critical) before full suites, worktrees or fan-out.

Run affected targeted tests after each refactor step and share full-suite evidence rather than re-running the suite. Why: refactoring needs fast feedback, not repeated full suites. **Never refactor while RED** — get to green first; the passing tests are what make refactoring safe.
