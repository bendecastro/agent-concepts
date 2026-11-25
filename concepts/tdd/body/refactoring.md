# Refactor candidates

After a green TDD cycle (all tests passing), look for:

- **Duplication** → extract a function/class.
- **Long methods** → break into private helpers (keep tests on the public interface).
- **Shallow modules** → combine or deepen (see `/codebase-design`).
- **Feature envy** → move logic to where the data lives.
- **Primitive obsession** → introduce value objects.
- **Existing code** the new code reveals as problematic.

Run affected targeted tests after each refactor step; run pytest through the guarded test runner the project's or machine's instructions name (never with a custom `--basetemp`), and share full-suite evidence rather than re-running the suite. The `agent-kernel` concept's Storage safety section holds the full rule, when loaded. Why: refactoring needs fast feedback, not repeated full suites. **Never refactor while RED** — get to green first; the passing tests are what make refactoring safe.
