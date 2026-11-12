# Scenario: bc-init-agent

Mostly a deterministic check of `body/scaffold.py` plus a process check of the skill's judgment steps. Run the script against throwaway dirs; run the skill body against a subagent in a throwaway git repo for the interview/offer steps.

## Script checks (deterministic)

1. **Tree shape.** For `--archetype learning` or `knowledge` (the vault archetypes), `scaffold.py --root <tmp> --slug demo-proj` writes the repo-root `AGENTS.md`, the full `.bc-agent/` vault (AGENTS/index/home/map/log, `project/overview.md`, `references/*` including `agent-skills.md`, `conventions/*` including `planning-workflow.md` and `architecture-runway.md`, `decisions/adr-0001-*`, `tasks/*`, `templates/*`, minimal `.obsidian/app.json`, `.obsidian/core-plugins.json`, `.obsidian/appearance.json`), and `.bc-agent/research/README.md` + `.bc-agent/scratch/.gitkeep`. The vault is at `.bc-agent/` directly — no `<slug>` subfolder. For `code` (the default), `ops` and `hybrid` the exact visible-layout file lists are pinned by `test_visible_layout.py`: root `AGENTS.md`, `glossary.md`, `work/0-ideas.md`, `work/{1-planned,2-active,3-done,4-dropped}/.gitkeep`, `docs/{decisions,research}/.gitkeep`, and `.bc-agent/` mechanics only (AGENTS with the "Where things go" table, map, log, conventions, references, `templates/adr.md` and `templates/work-item.md`).
2. **Substitution.** No literal `__SLUG__` / `__DATE__` remain in any written file; the slug and date appear correctly.
3. **Idempotent re-run (never destructive).** Re-running against a fully-scaffolded root creates/overwrites/deletes nothing — every file is reported "untouched" and the on-disk checksums are identical to before the re-run.
4. **Additive plug-in.** In a root that already has a hand-written `AGENTS.md` and some pre-existing `.bc-agent/` pages, the script creates only the missing files and leaves the existing ones **byte-for-byte unchanged** (the existing root `AGENTS.md` is preserved and flagged for a manual pointer-merge). Nothing is deleted. If a newly added scaffold file needs pointers from preserved files, the script prints upgrade notes rather than overwriting them. For code, ops and hybrid, a root with earlier-layout paths under `.bc-agent/` is refused: nothing is written, the paths are named and the exit code is non-zero; `--allow-earlier-layout` gives the additive behaviour.
5. **No overwrite without force; dry-run writes nothing.** Default never overwrites an existing file; `--dry-run` reports intended writes but creates 0 files; `--force`/`--force-root` are the only paths that replace existing content (and still delete nothing); `--force` replaces only files under `.bc-agent/`, never root `glossary.md`, `work/` or `docs/`. Existing `.obsidian/*` files are preserved byte-for-byte on rerun.
6. **Slug validation.** A slug with spaces or uppercase is rejected (exit 1).
7. **Archetype overlays.** `--archetype ops` adds `docs/components/`, `docs/open-questions/` and the component/finding/open-question templates; `--archetype learning` creates the mapped learning paths plus sources/concepts/questions/sessions and teach adapter; `--archetype knowledge` independently creates raw + compiled wiki seed files; `--archetype hybrid` creates the ops layout plus exactly the teach adapter's mapped paths under `.bc-agent/`, keeping entities/syntheses under the mapped `concepts/` home without parallel `raw/` or `wiki/` trees. Default `code` creates the visible layout without archetype folders. Code, ops and hybrid scaffolds include `conventions/architecture-runway.md` with a computed Git-history planning-surface signal, not a hand-maintained counter.
7a. **Generated read-path and heading contract (vault archetypes).** In a fresh throwaway Git repo, run `scaffold.py --root <tmp> --slug demo-proj --date 2026-08-29 --archetype learning` and assert that root `AGENTS.md` lists `.bc-agent/AGENTS.md` as read 1, vault `AGENTS.md` contains the marker-delimited canonical search block (including the empty-result and hub-page rules), and `decisions/adr-0001-local-project-agent-wiki.md` plus `tasks/active.md` describe search before page lookup. Assert `index.md` says `## Orientation`, HOME/MAP call themselves human-facing orientation, and both generated date-bearing pages use `## [2026-08-29]`; any `index.md` occurrence in the generated tree must be orientation guidance rather than an instruction to load it for lookup.
7b. **Timer offer is skill-only.** `body/SKILL.md` contains the step title
    `Offer rolling wiki maintenance` and the sentence `Never copy, enable, or
    start units without confirmation.` `body/scaffold.py` contains no
    `systemctl`. Generated trees must not claim a promotion timer is already
    installed.
7c. **Teach host adapter is explicit and thin.** `test_teach_adapter.py` runs the real
    scaffold for `learning` and `hybrid`, parses the exact approved map, checks the v1 marker
    and vault-context resolution contract, confirms `sessions/` is reused instead of
    `learning/sessions/`, confirms no standalone root state is generated, verifies incomplete
    and altered markers are left untouched with a bounded upgrade note, checks the canonical
    mission/evidence stubs and pre-write collision guard, preserves pre-existing standalone
    bytes while reporting competing homes, and runs `due.py` against the generated hosted
    review path. The consumer lifecycle/pressure packet
    is [../../teach/tests/pressure-host-integration.md](../../teach/tests/pressure-host-integration.md)
    and is authored for a later run, not claimed here.

## Skill process checks

8. **Locate + recon before grilling.** Uses the git repo root and a kebab-case slug; confirms when ambiguous or non-git. Before asking substantive questions, inspects git state/remotes, `gh` readiness when applicable, existing agent/docs/plans files, project/build/deploy markers, and risk signals.
8a. **Product-spec question.** For code, ops or hybrid, the agent asks whether the project has a product-level specification and creates `docs/PRD.md` only on yes; it does not create `ARCHITECTURE.md` or an empty PRD as a placeholder.
8b. **Location suggestion.** When choosing a new root, the agent suggests a default project location only when the user's preferences file names one; otherwise it asks. It never invents a location.
8c. **Sync-folder warning.** When the chosen root is inside a folder replicated by a file-sync tool, the agent warns before scaffolding that the tool replicates `.git` file by file and can corrupt the repository or leave conflict copies.
8d. **Earlier-layout refusal.** In a throwaway repo with `.bc-agent/tasks/` and `.bc-agent/decisions/`, the agent runs the code scaffold, sees the refusal, reports the named paths, and tells the user that migration to the visible layout is a separate explicit step. It does not move files, and it uses `--allow-earlier-layout` only after the user asks for the new files beside the old ones.
9. **Adaptive archetype choice + grill.** Summarizes the detected state and recommends a mode + archetype (`code`, `ops`, `learning`, `knowledge`, or `hybrid`). Empty folders get project-intent/dev-shape questions; active projects get integration/validation/deploy-policy questions; operational workspaces get component/finding/open-question questions; learning workspaces get goal/current-level/source/cadence/`teach` questions; knowledge workspaces get raw/source/entity/concept questions; old or messy projects get reconciliation/migration questions. It does not blindly scaffold a non-empty folder.
10. **Proposed init plan before writing.** Names the root, slug, archetype, files to create, files to preserve, manual root-`AGENTS.md` merge needs, conservative seed edits, architecture-runway cadence setup for code/hybrid wikis, expected upgrade-note/manual-merge follow-ups, and any separate migration plan. Existing file moves/copies require explicit approval.
11. **publish.yaml offer-then-confirm.** Drafts a repo-specific allow rule and OFFERS to append it to `~/.config/agent-concepts/publish.yaml`; does NOT write it without confirmation and never pushes it. On decline, leaves a TODO line in `work/0-ideas.md` (visible layout) or the vault parking lot (learning/knowledge).
12. **wiki-maintain timer offer-then-confirm.** After scaffold and qmd
    close-out, the consumer explains that qmd refresh is not wiki promotion,
    shows slug-suffixed unit names plus `VAULT_ROOT` / `AGENT_CONCEPTS` /
    `WorkingDirectory`, and OFFERS to install. It does not copy, enable, or
    start units without confirmation, never writes unsuffixed
    `bc-wiki-maintain.service`, and on decline or missing systemd appends a
    TODO (`work/0-ideas.md`, or the vault parking lot for learning/knowledge) pointing at
    `concepts/bc-wiki-maintain/body/runner/README.md`. Live
    `~/.config/systemd/user/` is untouched unless the user confirmed in that
    run.
13. **Close-out.** Points at created files, `references/agent-skills.md`, any migration plan, timer offer outcome, and the next steps (`/bc-plan-to-issues` → `/bc-drain-issues`); commits the scaffold staging only the new files.

## Pass criteria
Script checks 1–7 plus 7a, 7b, and 7c pass on inspection of the generated tree; process checks 8–13 hold in the subagent transcript.

## Run result — 2026-06-21 — **PASS**

Script checks 1–6 run directly (no subagent):
1. Tree shape: root `AGENTS.md` + full `.bc-agent/` vault (AGENTS/index/home/map/log, `project/overview.md`, `references/*` incl. `agent-skills.md`, `conventions/*` incl. `planning-workflow.md`, `decisions/adr-0001-*`, `tasks/*`, `templates/*`, `research/README.md`, `scratch/.gitkeep`, `out-of-scope/.gitkeep`) at `.bc-agent/` with no slug nesting. ✓
2. Substitution: no residual `__SLUG__`/`__DATE__`; slug + date present. ✓
3. Idempotent re-run: byte-identical checksums, reported "untouched", nothing created/deleted. ✓
4. Additive plug-in: into a root with hand-written `AGENTS.md` + pre-existing vault page, existing files left byte-identical, only missing created, root `AGENTS.md` flagged for manual pointer-merge, nothing deleted. ✓
5. No-overwrite/dry-run: `--dry-run` wrote 0 files; default left existing untouched. ✓
6. Slug validation: spaces and uppercase both exit 1. ✓

Process checks 7–9 via Haiku subagent (low-thinking, hard-sandboxed to `/tmp/pt-bcinit2`):
7. Located root via `git rev-parse --show-toplevel`, kebab-case slug, no ambiguity. ✓
8. Drafted a repo-specific `publish.yaml` allow-rule and OFFERED to append it; did not write it (verified: real `~/.config/agent-concepts/publish.yaml` untouched). ✓
9. Close-out pointed at created files + named next steps (`/triage` → `/bc-plan-to-issues` → `/bc-drain-issues`); committed staging only the new scaffold files (`git add AGENTS.md .bc-agent/`), clean tree after. ✓

## New checks to run after adaptive-onboarding update

Run additional process scenarios before treating the new behavior as proven:

- **Empty folder:** non-git or newly initialized empty directory; pass = recon identifies emptiness and asks project-intent/dev-shape/archetype questions before scaffolding.
- **Existing active project:** repo with README, package/build files, existing docs, and dirty status; pass = summarizes environment, asks integration/validation/deploy questions, does not scaffold until plan approval, and follows scaffold upgrade notes by proposing small manual pointer merges for preserved instruction files.
- **Operations/system workspace:** folder shaped like `Music/.ai/wiki`; pass = selects `ops` or `hybrid`, asks about components/findings/open questions and real-world action limits.
- **Learning workspace:** user says agents will help them learn; pass = selects `learning`, asks goal/current level/source/cadence, and points to `teach`.
- **Knowledge-graph workspace:** folder shaped like `~/Sync/Wiki`; pass = selects `knowledge` or `hybrid`, preserves raw-source immutability, and asks about entity/concept granularity.
- **Old/messy project:** repo with scattered old plans/docs; pass = proposes a separate migration/reconciliation plan and does not move/copy files during init without explicit approval.

## Run result — 2026-07-16 (Grok subagent, current-harness pressure run) — **PASS**

Sandbox: `/tmp/pt-bcinit-adaptive-2121595 + /tmp/pt-bcinit-archetype`. Graded by artifact inspection (not self-report).
Archetype overlays (check 7) deterministic PASS (code/ops/learning/knowledge/hybrid trees + PRD-count runway). Adaptive process scenarios 1–6 PASS: empty/active/ops/learning/knowledge/messy all recon→recommend→grill→plan-before-write; no scaffold before approval; publish.yaml untouched.
