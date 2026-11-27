# A stranger installs everything for Pi in one step

Why: In the 039 stranger rerun the test copied the pipeline's three role files into Pi for the stranger; a real stranger must copy them by hand, edit an overlay, install `pi-subagents` from another README section, and install the agent kernel separately (setup then suggested a command that assumes a checkout).
Done when: In a fresh Pi home, `pi install <this package>` plus `pi install npm:pi-subagents` gives the skills, the agent kernel and the three pipeline roles with no copying and no overlay; the README's Pi install is one copy-paste block; when `pi-subagents` is missing the pipeline offers to install it.
Stage: now
Blocked by: nothing
Kind: feature
Source: owner decisions 1a 2b 3a on the 039 stranger walkthrough, 2026-11-27
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Requirements

- The three role profiles (`bc-drain-auditor`, `bc-drain-worker`, `bc-drain-reviewer`) ship inside the package and `pi-subagents` discovers them through the package manifest (`"pi-subagents": {"agents": [...]}`), with tools and authority lines unchanged and no model pinned (children take the session model; the pipeline sets thinking per launch).
- The pipeline (`concepts/bc-pipeline-to-done/body/SKILL.md`) uses those role names by default; the overlay stays an optional override, not a requirement. Its preflight, when the `subagent` tool is missing, asks once to run `pi install npm:pi-subagents` and then tells the user to restart Pi; it never substitutes itself for a job.
- The agent kernel loads from the main Pi package by default (decision 3a): the package's Pi extensions include the kernel extension now in `packages/agent-kernel-pi`; `bc-setup-project` stops suggesting a separate kernel install for Pi.
- README Install: one Pi block with both `pi install` lines; remove the copy-roles step and the separate kernel step for Pi; say in one sentence that the kernel is included and how to turn it off if Pi allows that (check Pi 1.6.1 package filtering; if none exists, say so).
- `scripts/stranger_end_to_end.sh` installs exactly as the README says and stops copying role files.
- Harness docs (`docs/guides/harnesses.md`), `index.md`, CONCEPT.md files and `.bc-agent/log.md` updated; `python3 scripts/lint.py` 0 ERROR; tests that fake only external boundaries.

## Steps

- [x] Ship roles and kernel in the package, wire the pipeline to the bundled role names with the install offer, rewrite the README Pi install, and make the stranger script install per the README. Done when a fresh-HOME `pi install <checkout path>` (no model turn) lists the three roles in `pi-subagents`' agent list and the session system prompt contains the kernel section, and lint passes. Out of scope: other harnesses' installs; the pipeline's report wording (043-plain-pipeline-messages); cutting the release (044-stranger-rerun-and-release).

## Outcome

Implemented 2026-11-27. The three pipeline roles moved to `concepts/bc-pipeline-to-done/body/agents/` (their README became `body/roles.md`, since `pi-subagents` parses every Markdown file in the folder) and ship through `package.json`'s `pi-subagents.agents`; the root manifest also lists `packages/agent-kernel-pi/index.js` under `pi.extensions`, so the kernel loads from the main package and lint keeps checking its one staged copy. The pipeline uses the bundled role names by default (overlay overrides only) and its preflight offers `pi install npm:pi-subagents` once, then asks for a Pi restart. README's Pi install is one block with both `pi install` lines; the kernel is turned off with `pi config` (Pi 1.6.1 has no install-time opt-out; settings package filters `"extensions": []` also work). `bc-setup-project` now points Pi users at the package. The stranger script stops copying roles and installs per the README; its RPC driver no longer passes `-ne`, so sessions load the installed kernel and `pi-subagents` as a stranger's would.

Evidence: fresh HOME (`mktemp -d`, `env -i`), Pi 1.6.1, `pi install <checkout>` + `pi install npm:pi-subagents` (0.90.0). `pi-subagents`' own `discoverAgents` listed `bc-drain-auditor`, `bc-drain-reviewer`, `bc-drain-worker` as `(package)` with no model and no diagnostics; `pi_sandbox.py --check-only` (fake API key, no model turn) captured the system prompt with an `agent-kernel` section containing the canonical `AGENT-KERNEL.md`, and no role file appeared as a skill. Gate A check 6 gained manifest/no-model assertions (watched fail before the manifest change). `python3 scripts/lint.py`: 0 ERROR. Not run: the full stranger script (044-stranger-rerun-and-release) and the bc-setup-project kernel-survey pressure scenario after its wording change.
