# Concept: bc-init-agent

User-invoked scaffolder that stands up a project-local agent workspace — a repo-root `AGENTS.md` pointing agents at the vault, plus a `.agent/<slug>/` Obsidian-vault wiki (maintainer schema, templates, conventions, ADR-0001, and the `planning-workflow.md` adapter) — so a fresh repo is immediately ready for the grill→issues→drain loop. The setup step before `bc-grill-to-issues`. The `bc-` prefix is the user's personal namespace.

## Design decisions

- **Inspired by the image-maze `.agent/<project>/` vault** (user's request). The structure, schema, and conventions are generalized from that repo's wiki, which the user already works in; `bc-init-agent` reproduces it for any project so the loop has a consistent home.
- **Deterministic scaffolding via a script.** File-tree generation from a fixed template is exactly the kind of thing an LLM does unreliably, so `body/scaffold.py` writes the 23-file tree with `__SLUG__`/`__DATE__` substitution. The skill body handles only what needs judgment: locating the repo, the clobber guard's follow-up, the publish.yaml offer, and the commit. (AGENTS.md "scripts for anything an LLM does unreliably".)
- **Faithful to image-maze's persistence model (user's choice).** No root `CONTEXT.md`: the glossary lives in the vault (`project/overview.md`), ADRs in `decisions/`, plans/PRDs in `project/`. The `planning-workflow.md` adapter redirects `grilling`/`domain-modeling` there, so `bc-grill-to-issues` persists into the vault rather than generic files.
- **Clobber guard.** The script refuses (exit 2) if `.agent/<slug>/` exists, and only writes the root `AGENTS.md` if absent — a live vault or a hand-written root AGENTS.md is never overwritten. Standing up a workspace must be safe to re-attempt.
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

- Claude Code: `~/.claude/skills/bc-init-agent` → relative symlink to `body/` (carries `scaffold.py`). Deploy after the scenario check.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../harnesses.md`.
