# Concept: bc-init-agent

User-invoked scaffolder that stands up a project-local agent workspace — a repo-root `AGENTS.md` pointing agents at the vault, plus a `.bc-agent/` Obsidian-vault wiki (maintainer schema, templates, conventions, ADR-0001, and the `planning-workflow.md` adapter) — so a fresh repo is immediately ready for the grill→issues→drain loop. The setup step before `bc-plan-to-issues`. The `bc-` prefix is the user's personal namespace.

## Design decisions

- **Inspired by the image-maze `.agent/<project>/` vault** (user's request), **flattened to a single `.bc-agent/`** (user's call). image-maze nested the Obsidian vault under `.agent/<project>/` to separate it from sibling `research/`/`scratch/`/`agents/` dirs; that nesting isn't load-bearing, so the scaffold drops it — the vault is `.bc-agent/` directly, with `research/`/`scratch/` as subfolders. The slug survives only as the wiki's display name in titles, not in the path.
- **Deterministic scaffolding via a script.** File-tree generation from a fixed template is exactly the kind of thing an LLM does unreliably, so `body/scaffold.py` writes the 23-file tree with `__SLUG__`/`__DATE__` substitution. The skill body handles only what needs judgment: locating the repo, the clobber guard's follow-up, the publish.yaml offer, and the commit. (AGENTS.md "scripts for anything an LLM does unreliably".)
- **Faithful to image-maze's persistence model (user's choice).** No root `CONTEXT.md`: the glossary lives in the vault (`project/overview.md`), ADRs in `decisions/`, plans/PRDs in `project/`. The `planning-workflow.md` adapter redirects `grilling`/`domain-modeling` there, so `bc-plan-to-issues` persists into the vault rather than generic files.
- **Additive idempotency (never destructive).** The script creates only the files that are missing and leaves every existing file untouched; re-running changes nothing, and it **never deletes** (only `mkdir` + `write_text`, gated on non-existence). This makes it safe to re-run and safe to plug into an existing project — an existing root `AGENTS.md` or any pre-existing vault page is preserved verbatim (the existing root `AGENTS.md` is flagged for a manual pointer-merge). Overwriting is opt-in only: `--force` for vault files, `--force-root` for the root `AGENTS.md`; `--dry-run` previews. Chosen over the original "refuse if the vault exists" guard because that blocked the realistic case (dropping the workspace into a repo that already has some of these files).
- **publish.yaml: offer-then-confirm (user's choice).** The skill drafts a repo-specific allow rule (modeled on `image-maze-push-and-close-after-agent-work`) and offers to append it to `policies/publish.yaml` after the user confirms; it never pushes that change (self-amendment immunity). This closes the loop with `bc-drain-issues`, whose preflight needs the repo authorized for AFK push.
- **TODO stubs, not invented facts.** `validation.md`, `file-layout.md`, `references/*`, and the glossary ship as explicit TODO stubs for the project's agents to fill — matching image-maze's "not established yet" honesty rather than fabricating project facts.

## Provenance

- The image-maze `.agent/image-maze/` vault (read 2026-06-20) — the structure, schema, templates, and conventions this generalizes. Not vendored; reproduced as generalized templates in `body/scaffold.py`.
- `plans/bc-grill-to-ship-loop.md` + `pipeline.md` — the loop this prepares a repo for; the scaffolded `planning-workflow.md` documents the grill→issues→drain adapter and the `bc-drain-issues` execution phase.
- `policies/publish.yaml` — the `image-maze-push-and-close-after-agent-work` rule the publish.yaml offer is modeled on.
- `concepts/prompting-agents/body/SKILL.md` — composition + gate phrasing.

## Tests

`tests/scenario.md` — verifies the scaffold produces the expected tree with substituted placeholders, the clobber guard refuses an existing vault, the root `AGENTS.md` is preserved if present, and the publish.yaml step is offer-then-confirm (never auto-push). Process/generative skill (lower silent-failure risk than the gate orchestrators); the script's output is deterministically checkable.

## Deploy targets

- Claude Code: `~/.claude/skills/bc-init-agent` → relative symlink to `body/` (carries `scaffold.py`; deployed 2026-06-20, verified 2026-06-21).
- Pi: `~/.agents/skills/bc-init-agent` and `~/.pi/agent/skills/bc-init-agent` → relative symlinks to `body/` (carries `scaffold.py`; deployed/verified 2026-06-21).
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../harnesses.md`.
