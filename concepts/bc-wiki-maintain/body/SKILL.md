---
name: bc-wiki-maintain
description: Maintain a project-local Markdown agent wiki by linting its computed health, promoting durable log evidence, and flagging contradictions without silently rewriting knowledge. Run explicitly with a vault root when a project wiki needs maintenance.
disable-model-invocation: true
argument-hint: "<vault-root>"
---

# Maintain a project wiki

Run this skill explicitly against one project-local Markdown vault. Capture already happens
in that vault's append-only `log.md`; this pass separates capture from synthesis by promoting
only durable evidence into the smallest appropriate page. It works with `.bc-agent/`, `.agent/`,
or `agent/wiki/` roots. Do not assume the directory name: the vault-root argument is required.

The root-cause rule is load-bearing: **triggers must be computed (from Git and the filesystem),
never recorded in hand-maintained counters or markers.** The architecture-runway tracker is the
counterexample: since 2026-07-31 its state has remained `TODO / TODO / TODO`, so its nudge never
fired. Do not create another marker that an agent must remember to update. Use Git history to
find the last dedicated promotion commit and the filesystem to find the current pages.

<!-- Adapted from prompting-agents: scope discipline. -->
**Implement EXACTLY and ONLY what the log evidence supports.** No extra pages, cleanup, or
reorganization. If adjacent work looks useful, report it as optional; do not do it in this pass.

## The maintenance loop

### 1. Establish the boundary before writing

- Resolve `<vault-root>` and confirm it contains the target vault's `index.md` and `log.md`.
- Run `git -C "<vault-root>" status --short` before touching anything. If it is not clean,
  **stop**. Do not stash, reset, or fold the promotion into someone else's working changes.
- Identify the repository root with Git; the dedicated commit belongs to that repository.
- Find the latest relevant commit whose subject starts `wiki: promote log entries `. That Git
  history boundary, not a file marker, identifies the previous promotion. If none exists, inspect
  the log from its beginning and avoid duplicating facts already present in pages.
- The detector supplies the exact `YYYY-MM-DD..YYYY-MM-DD` range of standard dated log headings
  awaiting promotion. Preserve that range for the wrapper-owned commit subject.

### 2. Run detection first

Run the bundled detector before reading candidates or editing pages:

```bash
python3 <skill-dir>/wiki_lint.py "<vault-root>"
```

Read the report and act on it. Broken or ambiguous links that affect a candidate must be
resolved by the smallest additive change or reported as a blocker; never hide them with a
rewrite. Missing index entries are fixed by the hand-curated index update described below.
Distinguish pre-existing findings from defects introduced by this pass. The detector is
read-only; its report is evidence, not a license to skip the safety gates.

### 3. Read the evidence and classify it

Read the unpromoted `log.md` entries after the Git boundary, the pages they mention, and the
relevant `index.md` section. Keep `log.md` intact: it is the evidence trail, not a queue to
truncate. For each durable item, choose the smallest existing page or a new page by meaning:

- verified discovery, scan result, or durable observation → `findings/`;
- a costly or irreversible choice with a real alternative → the next numbered ADR in
  `decisions/` (inspect existing numbering first);
- stable command, path, external reference, or gotcha → `references/`;
- durable workflow rule or operating convention → `conventions/`;
- unresolved uncertainty or conflicting claims → `open-questions/`.

Do not promote transient status, a transcript, a TODO with no durable claim, or a fact already
represented accurately. Do not invent frontmatter: the directory supplies the page kind and Git
supplies dates (`git log -1 --format=%cs -- <path>`).

### 4. Apply the three gates before and during promotion

These gates exist because an unattended promotion has write access. The moment one blocks you
is precisely when a convenient exception is least trustworthy; do not skip one because the
change is small, obvious, or time-sensitive.

#### Gate 1 — Additive-only

Create missing pages and append a dated section to an existing page. Append a new link in the
appropriate curated section of `index.md` when a page is created. **Never delete, rewrite, or
reflow existing prose.** Do not improve wording while you are in the file, normalize headings,
or reorder the index. This mirrors `scaffold.py`'s additive/idempotent/never-deletes precedent:
the existing record is not yours to rewrite, and an additive diff is inspectable and reversible.

#### Gate 2 — One dedicated Git commit

After promotion, land all of this pass as one commit with the subject:

```text
wiki: promote log entries <from>..<to>
```

When the automatic runner invoked this pass, leave the index and `HEAD` unchanged: the wrapper
checks the result, stages only the vault files changed by this pass, and creates the dedicated
commit. Do not use `git add -A`, stage changes, commit, amend an unrelated commit, or edit a dirty
tree in place. Only a direct manual invocation without the automatic wrapper may stage the
verified vault files and create this one commit itself, after running the same checks. A separate
commit is not noise: Git is the audit trail and the undo path (`git show` and `git revert`). If no
durable item needs promotion, make no empty commit and report the no-op.

#### Gate 3 — Flag contradictions; never resolve them

When a candidate conflicts with an existing page or two sources disagree, write the conflict to
`open-questions/` with both source paths and the relevant `log.md` dates/headings. **Do not pick
a winner, rewrite either source, or turn the conflict into an accepted ADR. Stop the conflicting
promotion after recording the question.** The scheduled agent must not silently decide that a
spike is outdated or that the newer-looking statement wins. A typical fixture: a research page
says an acceptance bar was "formally lowered", while `tasks/active.md` and `index.md` say it
was not.

### 5. Verify the artifact, then commit

Before the dedicated commit:

1. Inspect `git diff --check` and the diff itself. Confirm existing prose was not rewritten,
   no file was deleted or renamed, and every new page has an index entry.
2. Re-run `python3 <skill-dir>/wiki_lint.py "<vault-root>"`. Separate pre-existing warnings
   from new defects; do not claim a clean report when it is not clean.
3. Check `git status --short` and leave the index unchanged; the wrapper stages only the files
   this promotion created or appended to after checking for staged agent changes.
4. Commit once with the exact detector-provided `wiki: promote log entries <from>..<to>` subject.
5. Verify `git show --stat --oneline HEAD` and a clean `git status --short`.

Report the detector output, promoted pages, any open-question conflict, commit ID, and checks
run. The next reader should be able to audit the result from the commit and the preserved log,
not from your self-report.

## Automatic runner contract

A scheduler may invoke this skill headlessly, but it does not relax any gate. A dirty tree,
ambiguous evidence, or contradiction is a safe stop, not a reason to guess. Keep the run scoped
to the supplied vault; do not modify qmd registry policy, other repositories, or the personal
wiki from this skill.
