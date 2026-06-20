# Refactor candidates

After a green TDD cycle (all tests passing), look for:

- **Duplication** → extract a function/class.
- **Long methods** → break into private helpers (keep tests on the public interface).
- **Shallow modules** → combine or deepen (see `/codebase-design`).
- **Feature envy** → move logic to where the data lives.
- **Primitive obsession** → introduce value objects.
- **Existing code** the new code reveals as problematic.

Run the tests after each refactor step. **Never refactor while RED** — get to green first; the passing tests are what make refactoring safe.
