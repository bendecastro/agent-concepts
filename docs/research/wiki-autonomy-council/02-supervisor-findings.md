# Supervisor findings — verified independently of the advisors

These were checked by the parent session against the machine, not taken from an
advisor report. Two correct an evidence artifact; one is new material the
advisors were not given in Pass 1.

## V1 — `map.md` contributes zero edges to the link graph (verified)

Opus reported this; I verified it directly rather than relay it.

`scaffold.py` writes `map.md` in every vault with its targets as inline code:

```
- `project/overview.md`
- `references/commands.md`
```

`wiki_lint.py:22-42` `without_code()` replaces every inline-code span with
spaces before `links()` (`:71-79`) ever runs. So those targets are invisible to
the parser. `map.md` therefore contributes **no** inbound links, and the lint has
never validated a single entry in it.

Consequence: the vault ships a "context picker" page that is (a) not counted when
computing orphans, (b) never checked for broken targets, and (c) drifts silently.
image-maze's lists architecture-runway rounds 4-7 while 8 and 9 exist on disk.

This matters more than it first looks. `map.md` is the closest thing the current
scaffold has to a cheap read path, and it is both unmaintained and unvalidated.

## V2 — the scout undercounted the installed timers

`vault-reality.md` reports "five timers and five oneshot services". The machine
has **seven of each**. The two it missed are not bc-wiki-maintain units:

```
wiki-health-check.timer            daily 09:00
wiki-semantic-consolidation.timer  daily 09:30
```

Both enabled and active. They point at `~/Sync/Wiki`, not at a project vault.
Recorded because the artifact is otherwise accurate and will be reused.

## V3 — a working autonomous wiki maintainer already runs on this machine

This is the most consequential finding of the run, and no advisor saw it in
Pass 1 because I scoped them to the project-vault concepts.

`~/Sync/Wiki` is the user's personal wiki: 383 Markdown pages, 1.8 MB. It is
maintained by two daily systemd user units:

- `wiki_daily_health_check.py` — deterministic lint, commits.
- `wiki_semantic_consolidation.py` (5,983 bytes) — delegates semantic judgment
  to Pi under a PID lock, writes a dated report to
  `wiki/_meta/semantic-consolidation-YYYY-MM-DD.md`, and commits.

It works. `git log` shows a `Semantic wiki consolidation <date>` and a
`Daily wiki health check <date>` commit pair every day from 2026-08-19 to
2026-08-26, and earlier from 2026-06-18 to 2026-06-30.

Its 2026-08-24 report ends with the state the project vaults do not have:

> Lint after edits: 379 pages, 0 broken links, 0 ambiguous links, 0 orphans,
> 0 missing index entries.

### Why this reframes the council question

1. **The design target is already met somewhere.** 0 orphans and 0 missing index
   entries on 379 pages, maintained daily and unattended. The project vaults sit
   at 7-21 orphans each. The question shifts from "what should we invent" toward
   "what does this system do that `bc-wiki-maintain` does not".

2. **It validates the frontmatter decision by counterexample.** The personal wiki
   *does* carry `updated:` frontmatter. The 2026-08-24 pass had to repair five
   pages whose `updated:` was "objectively wrong" against `git log`. That is
   `CONCEPT.md`'s recorded rationale — "a second `updated` field would be
   hand-maintained state that can drift" — observed drifting in the neighbouring
   system, and consuming daily LLM effort to correct. Strong evidence to keep
   using Git dates in project vaults.

3. **`_meta/` already has a precedent.** Both advisors who proposed a generated
   catalog chose `_meta/`. The personal wiki already writes dated reports there,
   and `wiki_lint.py:206` `maintenance_report()` already excludes `_meta`
   lint/health/semantic pages from orphan and index findings. The seam exists.

4. **Unattended LLM maintenance fails silently, and that is the real risk.**
   Two recorded failures:
   - A stranded PID lock "silently skipped every scheduled run for seven weeks"
     (the script's own docstring). Visible in the gap between 2026-06-30 and
     2026-08-19.
   - Today, 2026-08-26: Pi returned `Request timed out.` after 24 minutes. The
     wrapper caught it, wrote `status: needs-review`, and did not pretend to
     succeed.

   The second is the model to copy: the wrapper turned a model failure into a
   dated, committed, reviewable artifact. The first is the failure mode to design
   against — not a crash, but months of silence that looks identical to success.
   Any "seamless and automatic" design needs an answer to *how the user finds out
   it stopped working*. Neither the current `bc-wiki-maintain` runner nor any
   Pass 1 advisor proposal has one.

## Scope note

`bc-wiki-maintain`'s body explicitly forbids the skill from touching the personal
wiki, and nothing here proposes changing that. `~/Sync/Wiki` is cited only as
prior art running on the same machine.
