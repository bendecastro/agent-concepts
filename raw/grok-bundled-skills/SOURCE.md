# Source: xAI Grok Build bundled skills

- **What:** Snapshot of the workflow skills shipped with Grok Build under `~/.grok/bundled/skills/`: `design`, `execute-plan`, `implement`, `pr-babysit`, `review`, plus shared persona files under `shared/personas/`.
- **Origin:** xAI Grok Build / grok-cli bundled skill pack (no public git repo URL; live copies on this machine).
- **Snapshot taken:** 2026-07-03 from `/home/ben/.grok/bundled/skills/`.
- **License:** Unknown / not shipped with explicit license file — treat as xAI product documentation; cite this snapshot for provenance only.
- **Why filed:** Provenance for Grok-first orchestrator concepts. Bodies are **upstream-maintained by xAI** in the bundled directory; this workspace records design decisions and cross-harness notes, not a fork.
- **Caveats:**
  - Skills assume Grok-specific tools (`spawn_subagent`, `grok worktree rm`, `scheduler_*`, `get_command_or_subagent_output`, pager `[tag]` labels). Porting requires tool-name mapping, not copy-paste.
  - `implement` and `execute-plan` depend on `implement/scripts/memory.py` for workspace-scoped review-pattern memory (`~/.grok/implement-memory/`).
  - `pr-babysit` persists state under `~/.grok/plugin-data/pr-babysit/`.
  - Composes as a pipeline: `/design` → `/execute-plan` → `/pr-babysit`.