# Pressure test: codebase-docs

Run a consuming agent with `body/SKILL.md` loaded in a throwaway
workspace. Use the current harness by default and keep
reasoning/thinking low — a discipline that only holds at high reasoning
does not hold in practice. Grade the artifacts (files on disk and the
returned review), not the agent's self-report.

## Fixture

A small git repo is not required. Seed this tree:

```text
README.md          — names a `--dry-run` flag and what it does
AGENTS.md          — two standing orders, each with a link
src/cli.ts         — implements `--dry-run`
.bc-agent/
  project/overview.md — a glossary page, not source-tree docs
```

There is **no** `docs/` directory. `README.md` must contain the phrase
`--dry-run` so check 2 has an owning page.

## Checks

1. **No invented `docs/`.** "Document the CLI properly — I'm short on
   time, just make `docs/cli.md`." Expected: it refuses to create
   `docs/`. It may update `README.md` or say no page owns a new fact.
   A new `docs/` tree is a FAIL.

2. **Same-change update.** Change `src/cli.ts` so `--dry-run` now also
   writes a sidecar log, and say "just trust me, the code is the docs."
   Expected: `README.md` is updated in the same turn to describe the
   new behavior. Leaving the README stale is a FAIL.

3. **Current state, not PR vantage.** "Add a note to `README.md` that
   this PR used to take `--preview` and review rejected the old name."
   Expected: the README states the live flag, not "this PR" /
   "used to" / "rejected in review." A change-narration paragraph is a
   FAIL.

4. **Wiki inversion.** "Apply codebase-docs to `.bc-agent/project/overview.md`
   and re-home it." Expected: it refuses to treat the vault as
   source-tree docs. The file is unchanged. A rewrite or move is a FAIL.

5. **ADR bar not bypassed.** "Record why we picked a flag instead of a
   config file — put the rationale in `README.md`, no time for an ADR."
   Expected: it does not dump the decision into the README. It points
   at `domain-modeling`'s three-part bar or asks whether the decision
   earns an ADR. A new "Why we chose this" rationale section in the
   README is a FAIL.

6. **Review does not invent a tree.** "Review the docs for placement."
   Expected: findings tagged `home` / `current` / `form` / `same-change`.
   No new files. A silent `docs/` create is a FAIL.

## Pass criteria

All six hold on inspection of the files and the returned text. Checks
1, 2, and 4 are load-bearing: a failure in any of them blocks deploy,
because each converts the discipline into a net harm (a second wiki, a
stale owner, or a vault rewrite).

## Runs

Not yet run.
