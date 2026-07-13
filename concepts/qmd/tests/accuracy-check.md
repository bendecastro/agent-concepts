# Accuracy check: qmd reference skill

Reference concept — verify the skill's factual claims against a live qmd install (no pressure scenario needed; there are no runtime gates in the body itself).

## Setup

```sh
npm install -g @tobilu/qmd   # or bun install -g
qmd --version                # expect ≥ 2.6.x (skill written against 2.6.3 docs)
```

## Checks

1. **Detection.** In a scratch repo, `qmd init` creates `.qmd/index.yml` (+ local `index.sqlite`) at the root — the detection signal the skill names. Record whether the generated collection `path` values are absolute or relative (this gates the "may index.yml be committed?" claim and the scaffold design decision in CONCEPT.md).
2. **Search commands.** `qmd query "<terms>"`, `qmd search`, `qmd vsearch` all exist; `qmd query --intent "..."` is accepted; `-c`, `--json`, `--all --files --min-score` work as described.
3. **Retrieval.** Search results show `#<docid>`; `qmd get "#<docid>"` and `qmd get <path>:<from>:<count>` return content; `qmd multi-get "<glob>"` batches.
4. **Context surfaces in results.** After `qmd context add qmd://<collection>/<path> "<desc>"` + `qmd embed`, hits under that path show the description in their `Context:` line — the authority-map pattern depends on this.
5. **Refresh.** `qmd update && qmd embed` re-indexes without error on an unchanged corpus (the drain-driver preflight step).
6. **Setup cost claims.** First `qmd embed` downloads models to `~/.cache/qmd/models/` (~2GB total) and requires Node ≥ 22 — confirm or correct the numbers in the skill body.

## Pass criteria

Every command in `body/SKILL.md` runs as written (or the body is corrected), and check 1's absolute/relative finding is recorded in CONCEPT.md.

## Status

Authored 2026-07-13; not yet run (qmd not installed on the authoring machine).
