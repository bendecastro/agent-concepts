# Accuracy check: qmd reference skill

Reference concept — verify the skill's factual claims against a live qmd install (no pressure scenario needed; there are no runtime gates in the body itself).

## Setup

```sh
npm install -g @tobilu/qmd   # or bun install -g
qmd --version                # skill written against 2.6.3 docs; npm latest was 2.5.3 on 2026-07-13
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

Authored 2026-07-13. **Run 2026-07-13 on Arch (qmd 2.5.3 via `installers/packages/qmd.pkg`, Node 26.4.0, Vulkan GPU): PASS.**

- Check 1: `qmd init` creates `.qmd/index.yml` + local `index.sqlite`; `qmd collection add` writes **absolute** collection paths → gitignore all of `.qmd/`, setup is per-machine (recorded in CONCEPT.md; SKILL.md and the scaffold's `references/qmd.md` updated to match).
- Checks 2–4: `query`/`search`/`vsearch`, `--intent`, `-c`, `--json`, `--all --files --min-score`, docid/line-range `get`, `multi-get` glob all work as written; contexts added via `qmd context add qmd://wiki/<path>` surface as `Context:` lines in results (hybrid `query --intent` ranked the seeded ADR 93% with its authority label).
- Check 5: `qmd update && qmd embed` on an unchanged corpus is a clean no-op ("0 new, 3 unchanged", "already have embeddings").
- Check 6: models land in `~/.cache/qmd/models/`, 2.2GB total (via `qmd pull`); Node ≥ 22 confirmed required by upstream docs, ran on 26.x.
- Deviations from the 2.6.3-based docs at 2.5.3: none encountered in the skill's command surface. Minor upstream nit: `qmd status` crashes with EPIPE when its stdout pipe closes early (e.g. `| head`).
