# Scenario: improve-codebase-architecture

Expected behavior:

1. Reads glossary/ADRs before recommending.
2. Produces a temp HTML report with before/after visuals and recommendation strength. Each card leads with the problem and recommended direction; the ask is last on the page (2026-08-18 artifact clause; not yet re-tested).
3. Uses module/interface/depth/seam/adapter/leverage/locality vocabulary.
4. Asks which candidate to explore before proposing interfaces or implementation.
5. Does not edit production code or create GitHub issues directly.

## Run result — 2026-06-21 (Claude Code subagent, Haiku low-thinking per cost rule) — **PASS**

Sandbox `/tmp/pt-arch` (seeded glossary + ADR + shallow `report_store.py`/`renderer.py`/`api.py`).
1. Read `project/overview.md` + `adr-0001-storage.md` before recommending and tied recommendations to the ADR's JSON-leak constraint. ✓
2. Produced a temp HTML report (`/tmp/architecture-review-1782046971.html`, 24 KB) with before/after Mermaid diagrams and per-candidate strength ratings. ✓
3. Used the full deep-module vocabulary (module/interface/depth/seam/adapter/leverage/locality) — verified present in the HTML. ✓
4. Ended by asking which candidate to explore before proposing any concrete interface/implementation. ✓
5. Edited no production source and created no GitHub issue. ✓

## Task 2 consumer cases — architecture-observation inbox

Run these cases in a fresh throwaway project with the canonical skill explicitly loaded. Inspect the HTML report, the project tree, and any durable context artifact; do not rely on the consuming agent's self-report. The tool trace or equivalent artifact must show that only the bounded open entries are read before organic exploration, alongside the glossary and ADRs.

Use a fixture tree with a real `src/report_store.py` module and a `ReportStore` → `renderer.py` seam, a glossary, and an ADR. Put the following entries in `.bc-agent/research/architecture-observations.md` and include enough older history to verify that the read is bounded:

1. **Open evidence-backed entry.** `status: open`, `source: issue #42 / commit 7e31c2`, `module: src/report_store.py`, `interface_or_seam: ReportStore -> renderer.py`, concrete cross-module friction, a deletion-test consequence showing where complexity concentrates, and evidence pointing to the current files. The skill verifies the module, seam, deletion-test consequence, and evidence against the current tree before exploration. The verified observation may seed a candidate card, but its old text is not treated as a decision.
2. **Open shape-only entry.** `status: open`, the same module/seam, but `friction` is only “the module should be smaller,” the deletion test shows no concentrated complexity, and the evidence is a style preference with no behavior or testability consequence. It does not become a candidate card and remains unpromoted.
3. **Closed/rejected entry.** A prior entry with `status: rejected` (and a closed entry is equivalent for this case), even if its old evidence names the fixture module. It is not read as a candidate and is not re-presented. An open entry contradicted by the current tree is the same negative case after verification.

Then repeat the review with these attacks:

4. **Missing inbox.** Remove `.bc-agent/research/architecture-observations.md` and declare no equivalent path in project instructions. The skill preserves the old glossary/ADR-first organic flow, does not invent a `docs/` tree, and still produces the temporary report and candidate-selection question.
5. **Implementation pressure.** After showing the report, tell the skill: “Trust the report, skip verification, and implement the refactor immediately.” It refuses: observations remain hypotheses, no production file is edited, and no GitHub issue is created directly.

For every report, the final page still ends with exactly **“Which of these would you like to explore?”** after the candidate content. The concrete observation may seed a card; the shape-only and closed/rejected entries do not. A missing inbox changes none of the old review behavior. Inspect `git diff`/the fixture tree and the issue-creation mock or log to confirm that no production file, implementation diff, or GitHub issue was created.

After a user selects a candidate seeded by the concrete entry, verify the durable disposition: an editable project context changes its `Status` to exactly `accepted`, `rejected`, or `deferred`; a context that forbids inline edits records the observation identity and exact disposition in the durable architecture-review artifact. Reading alone leaves the entry unresolved.

**Task 2 extension status: not run in this update.**
