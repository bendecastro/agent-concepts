# bc-wiki-maintain — a guide for humans

This is the user guide. If you want the instructions the agent follows, read
[`body/SKILL.md`](body/SKILL.md); if you want why it was built this way, read
[`CONCEPT.md`](CONCEPT.md).

## What this is for

Projects here keep a notebook for agents — `.bc-agent/` or `.agent/` — holding decisions,
findings, conventions, and current state. An agent starting cold reads the notebook instead of
re-deriving everything from the source tree.

Those notebooks go stale. This tool keeps them honest: it reports what has drifted, and it files
loose notes into proper pages.

## The failure it was built to fix

Notebooks don't rot from neglect. They rot from a specific mechanical cause.

Look at what agents actually do. Appending to `log.md` is easy — you add a line at the end and no
judgment is required. Filing something into the right page is hard: which page, does it
contradict an existing claim, does the contents need updating. That work lands at the end of a
task, when whoever is doing it has least attention left. So the easy half happens every time and
the hard half never does.

Two pieces of evidence from this machine, both found while building this:

- One notebook's `index.md` listed 17 pages. There were 38 on disk. Every research page and two
  of three architecture decisions were absent from the contents. An agent reading the contents
  would never learn they existed.
- `conventions/architecture-runway.md` shipped a nudge that fires after three chunks of work land.
  Its counter read `TODO / TODO / TODO` in every vault from July onward. It never fired once,
  because firing required an agent to remember to increment it by hand.

That second one is the general lesson:

> **A trigger that must be remembered will not fire. Compute it instead.**

Everything here computes from git and the filesystem. There is no counter to maintain, no
"last run" marker to update, no field to bump. That is not a stylistic preference — it is the
one property that separates this from the mechanism it replaces.

## The two halves

### 1. The checker (`body/wiki_lint.py`)

Read-only. Takes a notebook path and reports drift. Run it on anything, any time, with nothing
installed:

```bash
python3 ~/.agents/skills/bc-wiki-maintain/wiki_lint.py <project>/.bc-agent
```

It reports:

| Check | What it means |
|---|---|
| Broken links | A link points at a page that does not exist |
| Ambiguous links | A link could mean two different same-named pages |
| Orphan pages | Nothing anywhere links to this page |
| Missing from index | The page exists but is absent from the contents |
| Stale pages | `tasks/active.md` points at a page git says is 90+ days untouched |
| Unpromoted log entries | Diary entries never filed into pages |
| qmd registration | Whether the notebook is searchable, or documented as deliberately excluded |

Two notes on reading it.

**Raw counts overstate the problem.** "Missing from index: 21" sounds alarming, but many will be
empty `README.md` stubs and unfilled templates. Sort by file size — the real signal is the large
pages. In one measured case, six pages over 1 KB held about 30 KB of genuine research and
decisions; the rest was scaffolding noise.

**A documented exclusion is not a defect.** A notebook may be deliberately excluded from search —
because it holds private data, or is a scratch space. Rather than nagging, the checker reads the
stated reason from `project/overview.md` and quotes it back. If you exclude a notebook on
purpose, write down why and the tool will stop asking.

The last line, `PROMOTION_REQUIRED=0` or `=1`, is for machines. The promotion runner greps
exactly that.

### Lint all your vaults on a schedule

If you have more than one project notebook, use the lint-only runner rather than installing a
promotion timer for each one. Put one vault root per line in a list file; blank lines and `#`
comments are ignored, and a leading `~` expands to your home directory:

```text
# One vault per line
~/path/to/project-a/.bc-agent
~/path/to/project-b/.agent
/absolute/path/to/project-c/agent/wiki
```

Install the `bc-wiki-lint.service` and `bc-wiki-lint.timer` templates from
[`body/runner/`](body/runner/), edit their `AGENT_CONCEPTS` and `VAULT_LIST` placeholders, then
enable the timer. The timer runs the read-only detector for every listed vault at its scheduled
time and prints a separate report for each one. It continues after a bad path or failed detector,
then returns nonzero if any vault failed. Advisory findings — orphan pages, missing index entries,
stale references, and unpromoted log entries — remain visible in the report but do not fail the
service.

This lint-all timer does **not** invoke an agent, promote log entries, edit files, write Git state,
or commit. It is safe to schedule broadly. The existing one-vault promotion runner is separate
and should be enabled only for vaults whose promotion behavior you have reviewed.

Read results with:

```bash
systemctl --user status bc-wiki-lint.service
journalctl --user -u bc-wiki-lint.service --since today
```

The full install/list-file instructions are in [`body/runner/README.md`](body/runner/README.md).

### 2. The promotion pass (`body/SKILL.md`)

An agent reads the diary, files durable entries into the right pages, updates the contents, and
commits once. You can invoke it yourself in any agent session that has the skill:

```
/bc-wiki-maintain <project>/.bc-agent
```

Or let the timer do it (see below).

## The three rules, and why each exists

These matter because this can run while you are asleep.

**1. It can only add.** It creates pages and appends sections. It never deletes, rewrites, or
reflows existing text. Your words stay your words, and every change is visible as additions in a
diff.

Test it survived: an agent was told "that page is badly worded, rewrite it properly" against
deliberately ugly prose. It appended below and touched nothing.

**2. One dedicated commit.** Everything lands in a single commit named
`wiki: promote log entries <from>..<to>`. That commit is allowed only after every unpromoted
diary heading is classified (file it, skip it with a reason, or record a real contradiction).
Review with `git show`, undo with `git revert`. Git is the safety net — not a human approval
step, because approval steps get skipped and git does not.

**3. Mutually exclusive claims are recorded, never resolved.** When two statements cannot both
be true, it writes the conflict into `open-questions/` citing both sides and does not treat
either as current truth. It then continues the rest of the diary. A page that is merely behind
the log — last month's snapshot vs this month's verified state — is not that kind of conflict;
it gets a dated section appended.

This is the most important rule. A wrong answer written confidently into a project's memory
outlives the session that wrote it, and everything downstream inherits it. Recording the question
costs you one decision; a silently wrong resolution costs you every decision built on it.

Rules 1–3 are also enforced *outside* the agent. After it finishes, the wrapper checks that
nothing was deleted, nothing outside the notebook changed, every listed heading was classified,
and the agent did not commit. An agent that talks itself past an instruction still cannot get
past those checks.

## Running it on a schedule

Files are in [`body/runner/`](body/runner/) and install nothing by themselves. See
[`body/runner/README.md`](body/runner/README.md) for the install commands.

systemd user timer rather than cron, deliberately: `journalctl --user` and
`systemctl --user status` make a silently failing scheduler visible. Cron gives you neither, and
silent failure is the main risk with anything unattended.

Point it at one notebook first. Widen once you have read a few diffs and trust them.

## Your routine after a scheduled run

### Did it run, and did it work?

```bash
systemctl --user status bc-wiki-maintain.service
```

`status=0/SUCCESS` means clean. This separates "worked" from "never ran" from "broke" — three
different situations needing different responses, and the git log alone won't distinguish them.

### What did it say?

```bash
journalctl --user -u bc-wiki-maintain --since yesterday
```

The full checker report plus every step. If it refused, the plain-text reason is here.

### What did it decide?

```bash
git -C <repo> show
```

This is the actual review; everything above is process. You should see additions only. Read the
new pages the way you would read a colleague's note: is the fact right, is it in a sensible
place, would the wording embarrass you.

### Did it raise a question?

```bash
ls <vault>/open-questions/
```

A new file means it found two pages disagreeing. Only you can settle it. Resolving means editing
the source pages yourself, then updating or deleting the question.

### Decide

Good? Do nothing — it is already committed.

Wrong?

```bash
git -C <repo> revert HEAD
```

That adds a commit undoing the last one, keeping both in history so you can see what it tried and
that you rejected it. The next run counts only diary entries added *after* the promotion commit,
so reverted work is not retried.

## When nothing happens for several nights

The pass refuses to run on a dirty tree — it will not sweep your in-progress work into an
automatic commit. Consequence: **if the agent fails partway, it leaves changes uncommitted, and
that dirty tree blocks every subsequent night.** It fails safe, but it fails persistently.

```bash
git -C <repo> status
```

Half-finished work sitting there is the cause. Discard it or commit it and the schedule resumes.

Same applies to your own work: leave something uncommitted overnight and that night's run skips.

## Getting more out of it

**Write log entries worth promoting.** The pass can only file what is there. "Fixed the build" is
not durable. "The build fails unless `NODE_OPTIONS=--max-old-space-size=4096` is set, because the
bundler holds every source map in memory" becomes a `references/gotchas.md` entry that saves the
next agent an hour.

**Let it find contradictions.** If you suspect two pages disagree, don't hunt manually — run the
pass and read `open-questions/`. It reads every page; you would skim.

**Run the checker before planning.** Broken links and unindexed pages mean an agent is about to
plan against a partial picture. Thirty seconds, read-only.

**The pass now indexes existing findings and decisions.** If a research page or ADR is on disk
but absent from the contents, this run appends the link. README stubs, templates, and the rest
of the catalog stay unfilled on purpose — those keep appearing in the report so curation stays
yours.

## A real run

First supervised run against a real project notebook with ten unfiled diary entries:

```
8 files changed, 111 insertions(+)
```

Zero deletions. `log.md` byte-identical afterwards — filing entries does not consume the diary.

It created two findings pages, appended sections to three existing pages, added everything new to
the contents, and raised two questions it refused to answer.

One of those questions was worth more than the filing. Two pages recorded the same historical
detail with different values — different job title, different year — and neither page knew about
the other. The pass cited both and left them unresolved. Nobody had noticed the conflict in the
months it had been sitting there, and a human reading either page alone would have believed it.

That is the argument for rule 3 in one example. The filing saves you time; the questions are
where the value is.

## Limits worth knowing

- **It does not rebuild the catalog.** Existing `findings/` and `decisions/` pages get an index
  link; other missing pages stay a human curation choice.
- **Only tested against Markdown-link notebooks.** Wikilink-style vaults are supported in the
  code but not yet exercised under test.
- **Promotion needs a model; the checker does not.** The checker is plain Python and free. The
  promotion pass costs a model call per run.
- **One notebook per timer.** By design — one notebook's bad state should not abort another's.
