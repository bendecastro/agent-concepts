# Commands

Recurring project commands, run from the repository root.

| Command | What it does |
| --- | --- |
| `scripts/gate` | Full gate: lint, portability check, all real Python tests. Set `PYTEST_CMD` to the machine's guarded pytest runner if its agent instructions name one. |
| `python3 scripts/lint.py` | Mechanical drift checks (links, provenance, status page, relationship views, personal terms when the private list exists). |
| `python3 scripts/lint.py --status` | Concept test/deploy board, worst first. |
| `python3 scripts/lint.py --write-status` | Regenerate `docs/status.md`. |
| `python3 scripts/lint.py --write-relationships` | Regenerate each concept's `RELATIONSHIPS.md`. |
| `python3 scripts/portability-check.py` | Prove a fresh clone works for someone who is not its author. |
| `python3 scripts/deploy-local-skills.py` | Deploy concept skills through relative symlinks. |
| `python3 .bc-agent/scripts/work_index.py` | Rebuild the work table in `work/README.md` (`--check` fails while stale). |
