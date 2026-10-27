# Refactor candidates

After a green TDD cycle (all tests passing), look for:

- **Duplication** → extract a function/class.
- **Long methods** → break into private helpers (keep tests on the public interface).
- **Shallow modules** → combine or deepen (see `/codebase-design`).
- **Feature envy** → move logic to where the data lives.
- **Primitive obsession** → introduce value objects.
- **Existing code** the new code reveals as problematic.

Run affected targeted tests after each refactor step; use guarded pytest and share full-suite evidence per [kernel Storage safety](../../agent-kernel/body/AGENT-KERNEL.md#storage-safety). Why: refactoring needs fast feedback, not repeated full suites. **Never refactor while RED** — get to green first; the passing tests are what make refactoring safe.
