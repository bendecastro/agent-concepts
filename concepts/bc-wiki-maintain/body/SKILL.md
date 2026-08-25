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
Skipping a heading still requires classifying it; silence is not a skip.

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
  awaiting promotion, and lists each unpromoted heading. Preserve that range for the
  wrapper-owned commit subject. The next dedicated commit treats the whole listed set as
  considered, so every heading must be classified before that commit is allowed.

### 2. Run detection first

Run the bundled detector before reading candidates or editing pages:

```bash
python3 <skill-dir>/wiki_lint.py "<vault-root>"
```

Read the report and act on it. Broken or ambiguous links that affect a candidate must be
resolved by the smallest additive change or reported as a blocker; never hide them with a
rewrite. Missing `findings/` and `decisions/` index entries are fixed by the additive index
update in Gate 1. Distinguish pre-existing findings from defects introduced by this pass. The
detector is read-only; its report is evidence, not a license to skip the safety gates.

### 3. Read the evidence and classify every unpromoted heading

Read the unpromoted `log.md` headings the detector listed, the pages they mention, and the
relevant `index.md` section. Keep `log.md` intact: it is the evidence trail, not a queue to
truncate.

Classify **every** listed heading. A later dedicated commit closes this list whether you filed
one item or twenty; a thin write must not be allowed to swallow the rest.

- `promote` — durable and not already represented accurately; file it
- `skip` — transient status, a transcript, a TODO with no durable claim, or a fact already
  represented accurately; one-line reason required
- `conflict` — mutually exclusive claims (Gate 3); file the question, do not promote either
  side as current truth

Write one JSON object per heading, covering the detector list as a multiset of exact `##`
lines, to `$CLASSIFY_PATH` when that environment variable is set. Otherwise write the same
JSONL to a temp file you report and do not put it in the vault — a new non-Markdown file left
in the vault fails the pass:

```json
{"heading":"## [YYYY-MM-DD] …","verdict":"promote","reason":"…","page":"references/gotchas.md"}
```

`page` is required for `promote` and `conflict`. Do not commit this file; it is a same-pass
gate, not a wiki page. Its verdicts are carried into the promotion commit body, so write each
`reason` for the next reader auditing why a heading was never filed.

For each `promote`, choose the smallest existing page or a new page by meaning:

- verified discovery, scan result, or durable observation → `findings/`;
- a costly or irreversible choice with a real alternative → the next numbered ADR in
  `decisions/` (inspect existing numbering first);
- stable command, path, external reference, or gotcha → `references/`;
- durable workflow rule or operating convention → `conventions/`;
- unresolved uncertainty or mutually exclusive claims → `open-questions/`.

Do not invent frontmatter: the directory supplies the page kind and Git supplies dates
(`git log -1 --format=%cs -- <path>`). Name appended sections after the fact, not after the
maintenance pass.

### 4. Apply the three gates before and during promotion

These gates exist because an unattended promotion has write access. The moment one blocks you
is precisely when a convenient exception is least trustworthy; do not skip one because the
change is small, obvious, or time-sensitive.

#### Gate 1 — Additive-only

Create missing pages and append a dated section to an existing page. Append a new link in the
appropriate curated section of `index.md` when a page is created. Also append a link for an
existing `findings/` or `decisions/` page the detector lists as missing from the index, except
`README.md` and anything under `templates/`. **Never delete, rewrite, or reflow existing
prose.** Do not improve wording while you are in the file, normalize headings, generate the
index, or reorder it. Do not backfill `conventions/`, `references/`, stubs, or other
directories in this pass. This mirrors `scaffold.py`'s additive/idempotent/never-deletes
precedent: the existing record is not yours to rewrite, and an additive diff is inspectable
and reversible.

#### Gate 2 — One dedicated Git commit, which you are probably not the one making

This pass produces exactly one commit, with the subject:

```text
wiki: promote log entries <from>..<to>
```

**Default: do not create it.** Assume the automatic runner invoked you unless a human, in this
conversation, explicitly told you to commit. Under the runner the wrapper checks classification
coverage, stages only the vault files this pass changed, and commits — all after your process
has exited. You will never see that commit. Do not `git add`, do not `git commit`, and do not
wait for `HEAD` to move.

A commit *you* create with that subject permanently closes the entire unpromoted heading list,
because the detector computes the next boundary from the latest such commit. That is the
thin-write failure this gate exists to prevent, entered through the front door. Never use
`git add -A`, amend an unrelated commit, or edit a dirty tree in place.

Only in a direct manual invocation, where a human asked for the commit, do you create it
yourself — after running the same checks the wrapper would, including classification coverage.
Then stage only this pass's verified vault files, commit once with the exact detector-provided
subject and the verdict summary as the body, and confirm with `git show --stat --oneline HEAD`
and a clean `git status --short`.

A separate commit is not noise: Git is the audit trail and the undo path (`git show` and
`git revert`). If every heading is a skip, make no empty commit and report the no-op; the list
stays unpromoted until a later pass files or classifies it into a commit.

#### Gate 3 — Flag mutually exclusive claims; do not halt on staleness

Two different disagreements exist. Only the first is a contradiction.

- **Mutually exclusive claims** cannot both be true: a research spike says an acceptance bar
  was "formally lowered" while the ADR addendum and `tasks/active.md` say it was not. Write
  both citations to `open-questions/` (one resolvable question per page or heading, not a
  batch dump), do not promote either claim as current truth, and classify that heading
  `conflict`. Continue the rest of the pass.
- **Stale page vs newer dated log** is the promotion job: the log has later verified state
  and a project page still describes the earlier snapshot. Append a dated section with the
  newer observation; do not rewrite the old sentence. Optionally note the leftover sentence
  in `open-questions/` if it would mislead a cold reader. Classify `promote`.

A conflict stops that item, not the pass. Do not pick a winner, rewrite either source, or
turn a conflict into an accepted ADR. The scheduled agent must not silently decide that a
spike is outdated or that the newer-looking statement wins.

### 5. Verify the artifact, then hand off

Before the wrapper handoff or direct-manual commit:

1. Inspect `git diff --check` and the diff itself. Confirm existing prose was not rewritten,
   no file was deleted or renamed, and every new page has an index entry. The wrapper also
   rejects any non-additive change to a tracked page, so a rewrite fails the whole run rather
   than landing quietly — find it here, not in the failure log.
2. Re-run `python3 <skill-dir>/wiki_lint.py "<vault-root>"`. Separate pre-existing warnings
   from new defects; do not claim a clean report when it is not clean.
3. Confirm the classification file covers every detector-listed heading
   (`python3 <skill-dir>/wiki_lint.py "<vault-root>" --verify-classify "$CLASSIFY_PATH"`). It
   prints the verdict summary on success and fails when the unpromoted list is unknown; an
   unknown list is a safe stop, not a pass.
4. Check `git status --short`. Leave the index and `HEAD` unchanged, then stop and report:
   the wrapper stages and commits after you exit. Do not try to verify a commit — while you
   are running there is none to see. Committing yourself is the Gate 2 failure.
   In a direct manual invocation only, follow the commit steps in Gate 2 instead.

Report the detector output, the classification verdicts, promoted pages, any open-question
conflict, commit ID, and checks run. The next reader should be able to audit the result from
the commit and the preserved log, not from your self-report.

## Automatic runner contract

A scheduler may invoke this skill headlessly, but it does not relax any gate. A dirty tree,
missing or partial classification, or a mutually exclusive claim that cannot even be filed as
an open question is a safe stop, not a reason to guess. Keep the run scoped to the supplied
vault; do not modify qmd registry policy, other repositories, or the personal wiki from this
skill.
