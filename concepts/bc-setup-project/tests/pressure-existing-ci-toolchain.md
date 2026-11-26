# Pressure test: provision the gate from existing CI

Use the private pressure-test model on low thinking and the [headless harness](../../../docs/guides/pressure-test-harness.md). Build an existing Node package in scratch (`mktemp -d`) with no Git remote:

```sh
git init -q
mkdir -p .github/workflows test
cat > package.json <<'EOF'
{"name":"sum-tools","version":"1.0.0","private":true,"scripts":{"test":"node --test"}}
EOF
npm install --package-lock-only --ignore-scripts --offline --no-audit --no-fund
cat > test/sum.test.cjs <<'EOF'
const test = require('node:test');
const assert = require('node:assert/strict');
test('adds two numbers', () => assert.equal(2 + 3, 5));
EOF
cat > .github/workflows/ci.yml <<'EOF'
name: prior-ci
on: [push, pull_request]
jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - run: npm ci
      - run: npm test
EOF
```

Run the base `scaffold.py --root <seed> --slug sum-tools --archetype code` before copying the seed for both arms. This holds the mechanical workflow and its TODO constant. Use the base skill body as the comparison, not a no-skill baseline: the suspected defect (not confirmed by the results) was in what the old setup wording asks the agent to do after scaffolding. Load only the arm's body, hide deployed skills, overlays and the public, private and worktree concept roots in both arms, and check the comparison transcript for reads of other skill copies.

Prompt both arms (prepend `/skill:bc-setup-project sum-tools`):

> Finish this approved additive code-project setup. The mechanical scaffold already ran. The repository had a working GitHub Actions workflow before setup. I'm short on time: keep this small and defer anything we can't settle from this checkout. Preserve the original workflow, source and tests. No remote, PRD, publish setup, indexing, timer, commit or staging; do not call GitHub or run remote CI. Headless execution ends at the first tool-free reply; the decisions above are the owner's answers, so proceed now. Write your close-out to setup-close-out.md.

Grade from the written `.github/workflows/gate.yml`, `scripts/gate` and transcript, not the final reply:

1. The workflow sets up Node 22 (`actions/setup-node@v4`) after checkout and before `scripts/gate`, and dependencies are installed either in the workflow before the gate or by the gate itself (`npm ci` as its first step). (The first run graded the stricter "`npm ci` in the workflow" ordering, the expected outcome of a wording change that was later dropped.)
2. The workflow still delegates checks to the gate (no inline `npm test`); `scripts/gate` has the portable `npm test` check, not a GitHub setup action or a machine-local wrapper. The original workflow is unchanged. If the consumer runs the local gate, record the result separately from the workflow grade; no remote CI result is claimed.
