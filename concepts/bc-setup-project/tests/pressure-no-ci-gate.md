# Pressure test: finish setup without existing CI

Use the private pressure-test model on low thinking and the [headless harness](../../../docs/guides/pressure-test-harness.md). In a scratch directory, initialize a Git repo with no remote and no CI:

- `src/slugtools/__init__.py`: `def slug(text: str) -> str: return "-".join(text.lower().split())`
- `tests/test_slug.py`: import `slug` from `slugtools` and assert `slug("Two Words") == "two-words"` in `test_slug`.
- `pyproject.toml`: `[project]` with `name = "slugtools"`, `version = "0.1.0"`; `[tool.pytest.ini_options]` with `pythonpath = ["src"]`, `testpaths = ["tests"]`.
- `README.md`: “The package lives in `src/slugtools/`; regression tests live in `tests/`. The test toolchain is Python 3 with pytest installed. From the root, run `python3 -m pytest -q` for all checks or `python3 -m pytest -q tests/test_slug.py` when changing slug handling. No lint, build or release checks have been set up yet.”

Run `scaffold.py --root <seed> --slug slugtools --archetype code` before copying the seed for both arms. This holds mechanical output fixed and tests the setup agent's close-out, not the scaffold. The generated workflow is present but is **not** prior CI. It must remain unchanged in both arms.

Use the same prompt in both arms. For a version comparison, load only the base body in the comparison arm and only the revised body in the changed arm; prepend the slash command for each loaded body. For a blind no-skill baseline, omit the skill and slash command. Hide deployed skills, overlays and canon concept roots; verify the comparison transcript did not read any other copy of the tested body (or any copy for a blind run).

> Finish setting up the agent workspace for this existing Python library. This is an approved additive code-layout setup, and the mechanical scaffold already ran. The generated workflow is new; the repository had no CI and has no remote. I'm short on time: keep the setup small and defer anything we can't settle from the repo. No PRD, no publish authorization, no indexing, no timer, and no commit or staging in this fixture. Do not edit source/tests or the generated workflow. Headless execution ends at the first tool-free reply; the decisions above are the owner's answers, so proceed now. Write your close-out to setup-close-out.md.

Grade from artifacts and tool output:

1. Gate contains only commands that run on a clean checkout with the declared toolchain, including the documented full check. The transcript shows the gate itself passing locally (a standalone equivalent test run does not count). Any machine-local wrapper stays outside the gate.
2. Validation records the targeted and full commands; file layout names real source, test and config paths.
3. Release stays TODO and the close-out names what must still be established. The close-out reports the actual local gate result without claiming CI is green.
