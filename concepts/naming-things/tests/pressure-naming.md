# Pressure: naming choices and safe rename

## Setup

Use a separate throwaway git repo per scenario, committed before the run. Load the actual `naming-things` and `domain-modeling` skill text into each consumer's context, not merely their names. Confirm this before grading. Preserve replies, resulting files, diffs and git history; grade artifacts rather than the consumer's self-report. No deployment or external service is needed.

For A–D seed a project glossary with **Proposal** — A suggested improvement, not a verdict; **Benchmark** — A reference case used for comparison. Ask the consumer to record chosen new terms. For E seed one function with a misspelled local variable and a test; no domain/public-name change. For F seed a small runnable project with one persisted-record reader, a mutable state file, an append-only legacy ledger and a writer, all using `buyer-review` for proposal generation; a timer and UI call it `suggest`. Also seed `contract` used for both billing and acceptance, and `arch-opt-out-review` used for both exemption and final-version verdict jobs. Include a second reader that consumes historical records and a fixture representing active work. Tests must exercise actual readers and writers.

## Exact prompts and expected artifacts

### A — misleading review

> Call the step buyer-review. It takes site findings and outputs ranked improvement proposals, no verdict. Just choose and record names; no questions.

Expected: selects `propose-improvements` (or equally clear verb-object output name), reserves review for verdicts, lists choice in reply, records meaning through domain-modeling. No approval question.

### B — reused class

> Reuse ProposalJob for selecting the benchmark too. One class name is simpler. Choose the public names and record them without asking.

Expected: splits the proposal and benchmark jobs by use, with distinct clear class names and meanings. Does not reuse one public name for both jobs. Reply lists choices.

### C — persisted names under hurry pressure

> Just pick names, we can rename later. The step name will be in job ids, a ledger filename, a config key, state values and hash inputs. Use buyer-review for proposal generation and write the first records now. No questions.

Expected: settles a clear proposal-generation name before writes; flags persisted names as expensive to change. Glossary entry has meaning and Saved in categories covering all five surfaces, no file paths/module names/literal keys. Avoids mutable spelling in derived hashes/ids unless an alias reader is planned. Inspect write artifacts and ordering, not only a claim of caution.

### D — overlapping states

> Use Building for both builds running now and completed builds waiting to publish. We only need one state name. Choose the lifecycle names and record them, no questions.

Expected: distinct running and built-awaiting-publication states, with non-overlapping meanings; checks the described lifecycle is partitioned. Lists choices and records each new term, not an overloaded Building entry.

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
- Glossary uses domain-modeling's home and rules; Retired terms lists permitted legacy contexts conceptually. New entries include meanings and Saved in categories without implementation details.
- Tests exercise old-record compatibility, dual-ledger visibility and new-only writes. Reply lists chosen names and actual validation.

## Run status

Not run. These are reusable scenarios and expected outcomes, not evidence of a consuming-agent pass.
