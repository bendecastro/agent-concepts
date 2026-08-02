# Portability — make the workspace installable by anyone

Date: 2026-08-02
Status: implemented and passing `scripts/portability-check.py` (2026-08-02)

## Problem

The workspace was published as [agent-concepts](https://github.com/bendecastro/agent-concepts)
on 2026-08-02. It is readable but not *usable*: it assumes one particular machine and one
particular person.

The sharpest failure is that the repo's own validation gate rejects its own users.
`scripts/lint.py` asserts that `~/.config/agent-concepts/publish.yaml` contains the literal strings
`~/Sync/CONFIG`, `https://github.com/bendecastro/CONFIG.git`, `~/Sync/Music` and six more like
them. Anyone who edits the policy to describe *their* repos fails lint. The check mistook the
author's data for the invariant it was meant to protect.

Beyond that:

- `~/.config/agent-concepts/publish.yaml` is one person's authorization rules for five private repos, shipped as
  if it were canon.
- 85 references outside `log.md` point at `~/Sync/CONFIG/...`, including the copy-paste bootstrap
  prompts in `harnesses.md` that a new user is told to run.
- Five concepts are environment-coupled (`qmd`, `omarchy`, `herdr`, `notebooklm`, `last30days`)
  with nothing marking them as such.
- `index.md` embeds deploy status inside each description, so a stranger reads about someone
  else's machines while trying to learn what a concept does.

The deploy mechanism itself is *already* portable: `deploy-local-skills.py` derives its source
from `__file__` and its targets from `Path.home()`, and supports `--dry-run`, `--force` and
`--harness`. Only its docstring is stale. The gap is configuration and documentation, not
machinery.

## Goals

- A stranger can clone, deploy, and use the general-purpose concepts without editing anything.
- The author can adopt this repo as canon and work in it publicly without leaking private
  configuration.
- Environment requirements are visible before install, not discovered at runtime.
- Portability is *demonstrated by a test*, not asserted in prose.

## Non-goals

- No install shell script. The Python entry point already works and a wrapper would rot.
- No requirement auto-detection. Concepts self-gate through their descriptions; building
  detection is speculative until someone complains.
- No `requires:` key in `SKILL.md` frontmatter. No harness reads it, so it would imply
  enforcement that does not exist.

## Resolved design

Settled by grilling, 2026-08-02.

1. **This is a library, not a template.** People install it and pull updates; they do not fork
   and own it. The decisive reason is that the author intends to make this his canon and keep
   working in it *in public* — so the private layer must be outside the repo, or something
   private eventually gets committed.
2. **The personal layer lives at `~/.config/agent-concepts/`.** XDG standard, outside the repo,
   survives re-cloning. The author syncs it by symlinking into `~/Sync/CONFIG/.config/`, exactly
   as `~/.config/opencode` already is — no new mechanism.
3. **Only the publish policy moves out.** `log.md` and `index.md` stay: they are the workspace's
   evidence, and removing them would gut the reason the repo is worth reading. Environment-coupled
   concepts are *labelled*, never removed.
4. **The repo ships `policies/publish.example.yaml`.** `publish-check.py` resolves the XDG path
   only, with **no in-repo fallback** — a fallback would re-create the hazard being removed. An
   absent policy already means "no rule can match, ask the user", which is the correct default for
   someone who has not opted in.
5. **Install stays `git clone` + `deploy-local-skills.py`**, deploying everything by default with
   a `--skip` flag.
6. **Lint validates structural invariants only** — `version: 1`, `default: deny`, the
   self-amendment-immunity clause, the constraint keys — and names no repository.
7. **Catalog entries keep a one-line description**, with `Requires: … · Status: …` on an indented
   sub-bullet, omitted where there is nothing to say.
8. **Docs use an `<agent-concepts>/` placeholder.** Not an environment variable: these strings are
   pasted into a chat window, where `$AGENT_CONCEPTS` would not expand. `log.md` is left alone; its
   paths were accurate when written.

## Steps

1. **Policy extraction** — add `policies/publish.example.yaml`; make `publish-check.py` resolve
   `~/.config/agent-concepts/publish.yaml` only; rewrite `policies/README.md` to describe the
   model rather than list the author's repos; move the real policy to the XDG path.
2. **Lint** — delete the nine repo-specific assertions; validate the example structurally; add
   `CONCEPT.md` link walking.
3. **Catalog** — split status out of all 36 descriptions; add `Requires:` where applicable.
4. **Concept labelling** — record requirements in `CONCEPT.md` for `qmd`, `omarchy`, `herdr`,
   `notebooklm`, `last30days`.
5. **Deploy script** — fix the stale docstring; add `--skip`.
6. **Docs** — `<agent-concepts>` placeholder through `harnesses.md` and `bootstrap.md`; install
   section in `README.md`; `AGENTS.md` documenting the personal-layer seam.
7. **Portability smoke test** — clone to a scratch directory under a fake `HOME`, run
   `deploy --dry-run` and `lint`, and assert both pass with no reference to the author's tree.

## Verification

Step 7 is the gate. The workspace's own test discipline holds that a change does not ship until
someone has watched it hold under conditions that could falsify it, and portability cannot be
established by reading the diff — the author's machine will satisfy assumptions a stranger's will
not. The smoke test is what converts "portable" from a claim into a result.

**Result 2026-08-02: passing.** All seven steps are implemented and
`scripts/portability-check.py` reports PORTABLE.

The check is not inert — it failed twice on real defects before passing. Its first run
caught 49 author-path references (it exports `HEAD`, so it was correctly reporting that
the fixes were still uncommitted); the second caught three more, two of which turned out
to be legitimate provenance attribution rather than defects, which narrowed the pattern.

Three guards have only ever been observed passing: the symlink-target check, the
relative-link check, and the policy-denial check. They are unproven in the sense that
matters here — nobody has watched them fire.
