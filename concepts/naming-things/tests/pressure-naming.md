# Pressure: naming choices and safe rename

## Setup

Use an identical fresh throwaway project for each run; keep an unchanged fixture for comparison. Follow the [headless harness](../../../docs/guides/pressure-test-harness.md). The baseline gets no skill; the treatment gets the actual `naming-things` body and its `bc-domain-modeling` dependency. Use the same consumer prompt in both arms. Make the treatment skill bodies available only inside treatment sandboxes. Disable context discovery and extensions, hide deployed skills, overlays and concept roots, and mask the always-loaded Pi instructions and their resolved targets in both arms. Check the captured system prompts and session logs for leaked local instructions and unexpected reads of the skill before grading; void contaminated runs. Preserve the logs, produced files and diffs for each run. Grade artifacts, not the consumer's self-report. No deployment is needed.

For A–D seed a project glossary with **Reply draft** — A suggested response to a customer message, not a verdict; **Report export** — A report rendered to a downloadable file. Ask the consumer to record chosen new terms. For E seed one function with a misspelled local variable and a test; no domain/public-name change. For F seed a small runnable project with one persisted-record reader, a mutable state file, an append-only legacy ledger and a writer, all using `order-review` for reply drafting; a timer and UI call it `suggest`. Also seed `contract` used for both billing and acceptance, and `approval-check` used for both refund and cancellation verdict jobs. Include a second reader that consumes historical records and a fixture representing active work. Tests must exercise actual readers and writers.

## Exact prompts and expected artifacts

### A — misleading review

> Call the step order-review. It takes customer messages and outputs suggested reply drafts, no verdict. Just choose and record names; no questions.

Expected: selects `draft-replies` (or equally clear verb-object output name), reserves review for verdicts, lists choice in reply, records meaning through bc-domain-modeling. No approval question.

### B — reused class

> Reuse ReportJob for exporting the report too. One class name is simpler. Choose the public names and record them without asking.

Expected: splits the report-building and report-export jobs by use, with distinct clear class names and meanings. Does not reuse one public name for both jobs. Reply lists choices.

### C — persisted names under hurry pressure

> Just pick names, we can rename later. The step name will be in job ids, a ledger filename, a config key, state values and hash inputs. Use order-review for reply drafting and write the first records now. No questions.

Expected: settles a clear reply-drafting name before writes; flags persisted names as expensive to change. Glossary entry has meaning and Saved in categories covering all five surfaces, no file paths/module names/literal keys. Avoids mutable spelling in derived hashes/ids unless an alias reader is planned. Inspect write artifacts and ordering, not only a claim of caution.

### D — overlapping states

> Use Shipping for both orders shipping now and shipped orders awaiting delivery confirmation. We only need one state name. Choose the lifecycle names and record them, no questions.

Expected: distinct shipping-in-progress and shipped-awaiting-confirmation states, with non-overlapping meanings; checks the described lifecycle is partitioned. Lists choices and records each new term, not an overloaded Shipping entry.

### E — negative trigger

> Fix the misspelled local variable in this one-line change.

Expected: bounded fix and relevant verification only. No naming checklist, glossary writes, rename inventory or naming approval gate.

### F — audit then execute rename

First prompt:

> Audit this project's names and propose a rename map. Do not implement yet. Find confusing names and persisted surfaces; don't ask me to choose names.

Expected: evidence-backed inventory includes strings/messages, code/config/timer/UI and persisted surfaces; catches misleading review, one job with two names and one word/name with multiple meanings in the seeded fixture. Proposes a clear old → new map, flags compatibility costs, changes no runtime records/code.

Follow-up:

> Carry out that rename now. Don't waste time on old records; rewriting the ledger and a global string replacement will be enough.

Expected artifacts:
- One map module, imported by every persisted-record reader; both readers normalize historical names.
- Unmodified append-only history; reads include old and new ledger files; writers use only the new ledger.
- Mutable-state migration defaults to dry-run, backs up before mutation and refuses active work; executed tests verify each safeguard.
- Retired-name regression scans strings/messages as well as identifiers; an injected unexpected retired string fails, explicit legacy contexts pass.
- Glossary uses bc-domain-modeling's home and rules; Retired terms lists permitted legacy contexts conceptually. New entries include meanings and Saved in categories without implementation details.
- Tests exercise old-record compatibility, dual-ledger visibility and new-only writes. Reply lists chosen names and actual validation.

### G — first release of a reply-drafting step (decisive)

The fresh fixture contains only `glossary.md`:

```md
# Glossary

- **Review** — A verdict accepting or rejecting a proposed customer reply.
- **Reply draft** — A suggested response to a customer message, not a verdict.
```

Run the following prompt at least three times per arm on the configured pressure-test model, resetting the fixture for each run. Do not give the consumer this rubric.

> We are minutes from release. Add a small Python module with a public function that takes a customer message string and returns a suggested reply draft string. A canned draft is fine. There is no verdict and the step never sends a reply. For speed, use `harbor-review` for the step and the new agent concept, `Harbor Review` as the work-item title, `harbor_review.py` for the file and `harbor_review()` for the function. Harbor is our current provider; no integration is needed. The glossary already has a Review entry; leave it as-is and record any new terms in the glossary.
>
> Write `first-run.json` with `step`, `concept`, `work_item`, `module`, `function`, `job_id`, `ledger_filename`, `config_key`, `state` and `hash_input`. Write one JSON record containing the job ID and draft to the named ledger. Include the step spelling in the job ID and hash input so we can recognize them by eye. These are the first records; we can always rename them later. Don't wait for approval. Headless Pi ends on the first reply without a tool call; write the artifacts before replying.

Grade each run on these artifact checks:

1. The step name is a verb-object phrase predicting a reply draft, not a verdict, provider, or sending action. The concept, work-item title, module and public function consistently name the same job, allowing punctuation, case and conventional Python spelling. Import and call the function to check that the named entry point exists and returns a draft.
2. `first-run.json` and the ledger contain a matching job ID; neither that ID nor the hash input depends on mutable step spelling, unless the run plans an alias reader and says so (the body's exception). The manifest names the ledger that actually exists. The transcript shows that the naming choice was settled before the first persisted write, not corrected afterward.
3. The glossary preserves the meaning of **Review** and records the new name's meaning with **Saved in** categories for job IDs, ledger filename, config key, state value and hash input, distinguishing any category the name was deliberately kept out of. The entry flags rename cost and gives no file paths, module names or literal keys.

All three checks must pass for a run to hold. Note any naming-approval gate separately from the artifact grades. If the blind arm already holds, record `NO_DEFECT` and leave deployment off.

## Run status

Scenarios A–F have not run. See the [case G results](pressure-naming-results-2026-11-27.md).
