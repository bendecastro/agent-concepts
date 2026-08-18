# Source: deepseek-ai/deepseek-harness

- **What:** Citation record for the DeepSeek Harness (`dsh`)
  documentation and Agent Notes system. No skill bodies or repo tree
  are stored here.
- **Origin:** https://github.com/deepseek-ai/deepseek-harness
- **Commit read:** `99f6f02fecdb7dff40c3fbc9470f5907c29f74ca`
  (merge of `release/dsh-0.1.0-rc.7`, shallow clone 2026-08-18).
- **License:** MIT (Copyright 2026 DeepSeek). Cited, not redistributed.
- **Why filed:** grilled ingest into `codebase-docs`. The distinctive
  portable ideas were one home per fact, tutorial vs reference,
  current-state writing, and same-change owner updates.
- **Files consulted (not vendored):**
  - `docs/AGENTS.md`
  - `docs/i18n/README.md`
  - `.agents/notes/README.md`
  - `.agents/skills/dsh-doc-standards/SKILL.md`
  - `.agents/skills/dsh-prose-standard/SKILL.md`
  - `.agents/skills/dsh-trim-cot-leakage/SKILL.md`
  - `.agents/skills/dsh-find-simplifications/SKILL.md`
  - `.agents/skills/dsh-archive-agent-notes/SKILL.md`
  - root `AGENTS.md` (`CLAUDE.md` is a symlink to it)
- **Deliberately not adopted:** Agent Notes as a required-every-change
  gate; bilingual `.md` + `.zh.md` + `.i18n.yaml` pairing; type-equiv
  and doc-budget verifiers; VitePress site-sync; stacked-PR / pre-push
  choreography; the full CoT-leakage taxonomy and JSDoc coverage
  matrix. Parked for a later conversation: `code-review` /
  `bc-init-agent` pointers, mandatory alternatives / supersede-don't-rewrite,
  and possible later concepts from `dsh-find-simplifications` and
  `dsh-trim-cot-leakage`.
