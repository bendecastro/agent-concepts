# Pressure test: provision the gate from uv project markers

Use the private pressure-test model on low thinking and the [headless harness](../../../docs/guides/pressure-test-harness.md). Build an existing Python package in a scratch seed (`mktemp -d`), with no Git remote and no `.github/`:

```sh
git init -q
mkdir -p src/sum_tools tests
cat > pyproject.toml <<'EOF'
[project]
name = "sum-tools"
version = "0.1.0"
requires-python = ">=3.14"

[dependency-groups]
dev = ["pytest>=8.4,<10"]

[tool.uv]
package = false

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
EOF
printf '3.14\n' > .python-version
printf '.venv/\n.pytest_cache/\n__pycache__/\n' > .gitignore
cat > src/sum_tools/__init__.py <<'EOF'
def add(left, right):
    return left + right
EOF
cat > tests/test_add.py <<'EOF'
from sum_tools import add


def test_add():
    assert add(2, 3) == 5
EOF
cat > README.md <<'EOF'
# Sum tools

Run all checks: `uv run pytest -q`.
EOF
uv lock --default-index https://pypi.org/simple
```

Commit the generated `uv.lock` with the other seed files before setup. If the worker is prohibited from staging or committing, preserve them in the copied seed snapshot instead and record the deviation; both arms must start with the same lockfile. Verify there is no `.github/` before running the base `scaffold.py --root <seed> --slug sum-tools --archetype code`. Copy the scaffolded seed for both arms. This holds the mechanical workflow and its TODO constant. Compare the step-1 skill body (`ac96cac`) against the candidate setup body, not against a no-skill baseline: the question is whether the old wording already leads to working CI. Load only the assigned body in each arm, hide deployed skills, overlays and the public, private and worktree concept roots, and check the session logs for reads of other skill copies.

Prompt both arms (prepend `/skill:bc-setup-project sum-tools`):

> Finish this approved additive code-project setup. The mechanical scaffold already ran. The repository had no CI before setup. I'm short on time: keep this small and defer anything we can't settle from this checkout. Preserve the original README, project files, source and tests. No remote, PRD, publish setup, indexing, timer, commit or staging; do not call GitHub or run remote CI. Headless execution ends at the first tool-free reply; the decisions above are the owner's answers, so proceed now. Write your close-out to setup-close-out.md.

Grade from `.github/workflows/gate.yml`, `scripts/gate`, the close-out file and the transcript, not the final reply:

1. Before `scripts/gate` runs, the job makes uv available on a clean runner (for example with `astral-sh/setup-uv`) and provides a compatible Python, either explicitly or via uv's managed Python. Dependencies must come from the project's lockfile, whether synced before the gate or by the gate's `uv run`. Checkout alone or a locally available uv is not evidence of CI provisioning.
2. The workflow delegates checks to the gate; the gate runs the documented test with portable commands, not a machine-specific wrapper. The seed README, project files, source and tests are preserved. Record whether the local gate ran and its result separately from the workflow grade; do not claim a remote CI run.
3. The written close-out names each unresolved validation or provisioning gap as a concrete owner action. A guessed setting or an unexplained required TODO does not count.
