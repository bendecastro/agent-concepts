# Pressure test: Standards review traces data size across changed boundaries

Authored and run 2026-11-19 for the Standards-reviewer question on data crossing a changed boundary (retro 2026-11-19 proposal 1: an income-lab prompt at 430,642 bytes against a 400,000-byte limit, a riprap snapshot at 33.6 MB against a 32 MiB cap, a 31.8 MiB file becoming a 63.5 MiB message).

Consumer: Terra low (`pi -p --no-tools --no-context-files --no-skills --no-session --model openai-codex/gpt-6.1-terra --thinking low --append-system-prompt <file>`), text-only. Arms: without (a one-line "You are a code reviewer" prompt), new body (with skill), and for D only the pre-change body (`HEAD` before this change) to attribute the result to the new sentence. Every prompt opens "You cannot run tools in this reply." Author pressure: "Owner needs this merged …, please approve."

Pass criteria were written before each run. A "size finding" is any finding naming maximum size, amplification/duplication or growth of data crossing the boundary, or behaviour at a limit.

## Scenario A — book import: file → message → IndexedDB + persisted undo history
Popup sends `Array.from(new Uint8Array(buf))` in a runtime message; worker stores the bytes in IndexedDB and pushes them into `library.history`, which is `JSON.stringify`-ed into `chrome.storage.local` on every import. One 3-byte test.
Pass: a size finding on the amplification or the growing history.

- without 1: PASS — "Every import duplicates the book into extension storage … the serialized typed array is substantially larger than the original bytes."
- without 2: PASS — "Full book contents are duplicated into persisted undo history … can exhaust storage quota."
- with 1: PASS — "File data is copied and persisted without a size or growth limit … neither limit nor failure is handled."
- with 2: PASS — "book data is duplicated into persisted undo history … Storage and serialization costs grow."

Verdict: not discriminating; the persisted history makes it obvious to the baseline.

## Scenario B — ledger merge: unbounded LLM prompt + accumulating snapshot, limits stated
Prompt concatenates both ledgers and all prior notes; every merge pushes `{before, after}` into `state.snapshots`, saved in one write. Packet states "llm.complete rejects prompts over 400,000 bytes. store.save fails above 32 MiB."
Pass: size findings on both the prompt and the snapshot growth.

- without 1: PASS — "no handling for the 400,000-byte prompt limit … grows `state.json` until it exceeds 32 MiB."
- without 2: PASS — "Valid merges can exceed the model's prompt limit" and "Snapshot history eventually prevents further saves."
- with 1: PASS — "valid merges can exceed the prompt limit" and "snapshots eventually exceed storage capacity."
- with 2: PASS — same two findings.

Verdict: not discriminating; stating the limits in the packet hands the baseline the answer.

## Scenario D — PDF to offscreen document: amplification only, no limit stated
Panel reads the whole file, `Array.from(new Uint8Array(...))`, sends it via `chrome.runtime.sendMessage`; offscreen document rebuilds a `Uint8Array`. Three green unit tests, Test levels block present. No limit is mentioned anywhere.
Pass: a size finding on the number-array message amplification / missing size handling.

- without 1: FAIL — offscreen-document lifecycle and MIME check only.
- without 2: FAIL — same two findings.
- without 3: FAIL — same two findings.
- old body 1: FAIL — integration evidence gap only.
- old body 2: FAIL — MIME check and integration only.
- with 1: PASS — "Unbounded message amplification … expanded into a JavaScript number array, then serialized into a runtime message … There is no size limit or handled size failure."
- with 2: PASS — "Unbounded message amplification … There is no size limit or handling for oversized files."
- with 3: PASS — "unbounded message amplification … Establish a supported maximum and handle it explicitly."

Verdict: discriminating. without 0/3, old body 0/2, with 3/3. (The with-arm missed the offscreen-lifecycle finding all three without-runs made; it was raised only as an evidence gap. Not caused by this sentence — the old body behaves the same — but noted.)

## Control C — header title trim/fallback, no data movement
Pure `headerTitle` trim + "Untitled" fallback with four example tests.
Pass: no size finding.

- without 1, 2: PASS — "No findings."
- with 1, 2: PASS — no size finding; Standards "No defect identified." (Both raise a Spec property-test finding on the `L2: not required` claim — from the existing Test levels audit, not this sentence.)

## Result
With beats without only where the risk is not handed over (D: 3/3 vs 0/3); where the packet makes growth obvious (A, B) both arms find it. No false size finding in the control. No body tune was made after running.
Transcripts were in `/tmp/bc-swarm/2026-11-19-retro-skill/pt-cr/` (temporary).

## Raw outputs

### A.none.1

````text
**Do not approve yet.** The supplied diff has two blocking issues:

1. **Import reports success before IndexedDB finishes** — `src/background/worker.ts`: `db.put(...)` is not awaited, and the worker replies `{ ok: true }` immediately. A failed write is reported as successful, and the worker may stop before the write completes. Await the write and return an error on failure; the popup should check the response.

2. **Every import duplicates the book into extension storage** — `src/background/worker.ts`: `library.history.push({ name: msg.name, data })` persists the entire file again through `JSON.stringify(library)` and `chrome.storage.local.set`. Book files can exceed storage quota, and the serialized typed array is substantially larger than the original bytes. The storage error is also ignored. Keep book bytes in IndexedDB and persist only references or metadata in history.

The passing test does not cover write failures, realistic file sizes, or whether the popup displays the imported book. The supplied diff also shows no popup library refresh, so that part of issue #212 is not verified.
````

### A.none.2

````text
## Findings

- **[P1] Import reports success before IndexedDB writes finish** — `src/background/worker.ts`: `db.put(...)` is not awaited, and `reply({ ok: true })` runs immediately. A failed or unfinished write is reported as successful; service-worker termination could also interrupt it. Await the write before replying, and propagate errors to the popup.

- **[P1] Full book contents are duplicated into persisted undo history** — `src/background/worker.ts`: `library.history.push({ name: msg.name, data })` followed by `JSON.stringify(library)` serializes every byte into `chrome.storage.local`. EPUBs and especially PDFs can exhaust storage quota or cause substantial serialization and memory overhead; the rejected storage write is also ignored. Keep book bytes in IndexedDB and store only references in history.

- **[P2] The diff does not show the imported book in the popup library** — `src/popup/import.ts`, `src/background/worker.ts`: the new path sends the file and writes it to IndexedDB, but no library refresh or display update is shown. Unless existing code already observes these writes, the issue’s visible-library requirement is unmet.

**Do not approve yet.** The single green test does not cover write failures, realistic file sizes, or the popup display; it also does not establish that the response waits for persistence.
````

### A.new.1

````text
## Spec

- **Important — Import can report success before the book is stored.** In `src/background/worker.ts`, `db.put(...)` is not awaited, and `reply({ ok: true })` runs immediately. A failed or interrupted write can leave no book in IndexedDB despite a successful response. The popup also ignores the response in `src/popup/import.ts`.
- **Untested — Library display.** The supplied diff and test do not show that an imported book appears in the popup library. The existing test checks only a database lookup.
- **Important — Missing test-level evidence.** The packet contains no Test levels block or `Test-levels:` trailers. The example test alone does not establish coverage of the import’s rule-bearing behavior.

## Standards

- **Important — File data is copied and persisted without a size or growth limit.** `src/popup/import.ts` expands the entire file into a JavaScript number array for messaging. `src/background/worker.ts` then stores the bytes both in IndexedDB and in persisted undo history serialized as JSON. Large files and accumulating history can substantially amplify storage and message size; neither limit nor failure is handled.
- **Important — Persistence errors are not surfaced.** Neither `db.put` nor `chrome.storage.local.set` is awaited or checked in `src/background/worker.ts`. The caller cannot distinguish a completed import from a failed write.
- **Untested — Integration and validation.** The reported one passing Vitest test uses a three-byte fixture and does not demonstrate real extension messaging, storage-limit behavior, or failure handling. I could not verify the base ref, full diff, repository standards, or run checks from the supplied excerpt.

**Verdict: Block.** The supplied evidence is insufficient for approval, and the persistence and size-handling findings need resolution.

Merge danger: door = two-way; blast radius = localized; reason = the shown effects are local library writes, though failed imports can affect users’ stored library state.
````

### A.new.2

````text
## Spec

- **Important — persistence can fail after success is reported.** In `src/background/worker.ts`, `db.put(...)` is not awaited, and the popup ignores the reply. The import can appear successful before the book is stored; a rejected write is not propagated to the user.
- **Important — library display is not established.** The supplied diff shows neither a popup file-selection UI nor code that refreshes or displays the imported book. These may exist elsewhere, but the provided evidence does not establish the end-to-end requirement.
- **Important — test-level evidence is missing.** The packet has no Test levels block or commit trailers. It also provides only a three-byte example, with no property test or documented reason for omitting one.

## Standards

- **Important — book data is duplicated into persisted undo history.** `src/background/worker.ts` adds the full `Uint8Array` to `library.history` and serializes the entire library into `chrome.storage.local` on every import. Storage and serialization costs grow with imported files and history; storage-limit or write failures are not handled. This can prevent persistence of library state for larger collections.
- **Important — the test does not establish the extension integration.** `test/import.test.ts` reports one passing test, but the packet does not show how messaging, IndexedDB, or the popup are wired in that test. It does not demonstrate popup display or failure handling.

**Verdict: BLOCK.** The base ref and full diff could not be verified, and the reported test was not independently run; both are **untested** because tools were unavailable for this reply.

Merge danger: door = two-way; blast radius = localized; reason = the shown change affects imported books and library state, with no demonstrated irreversible external action.
````

### B.none.1

````text
**Do not approve yet.** The diff has several specification and reliability gaps:

1. **Merged ledger is not saved** — `src/merge.ts`: The function saves a snapshot and returns `merged`, but never updates the stored ledgers with it. Unless a caller separately persists the return value, the merge is lost. The spec requires saving the merged ledger.

2. **Concurrent merges can lose snapshots** — `src/merge.ts`: Each merge loads state, appends locally, and saves the whole state. Two overlapping calls can load the same state and the later save can overwrite the earlier snapshot. A single-write save does not make the read-modify-write atomic. Use transactional or serialized updates.

3. **Valid large inputs and accumulated history can make merges fail** — `src/merge.ts`: There is no handling for the 400,000-byte prompt limit; either ledger or the accumulated notes can exceed it. Likewise, embedding both input ledgers and the output in every snapshot grows `state.json` until it exceeds 32 MiB, after which merges cannot be saved. The design needs a size-aware reconciliation strategy and snapshot storage that can grow beyond that limit.

4. **The snapshot test may inspect a different store** — `test/merge.test.ts`: It calls `memStore()` separately for the merge and assertion. If that factory returns a fresh store, the assertion does not check the store used by the merge; if it returns a shared store, the test relies on implicit shared state. Retain one instance and assert against it, including the persisted merged ledger.

The reported green test does not cover these cases.
````

### B.none.2

````text
**Do not approve yet.** Based on the supplied diff:

- **`src/merge.ts` — The merged ledger is not saved as the active ledger.** The code saves it only inside a snapshot and returns it. Unless a caller separately persists it, the requested merge is lost as the current ledger. Persist the merged ledger along with its snapshot.

- **`src/merge.ts` — Valid merges can exceed the model’s prompt limit.** Both transaction lists and all prior notes are placed in one unbounded prompt. Once it exceeds 400,000 bytes, `llm.complete` rejects it, so the user cannot merge. The implementation needs a size-aware reconciliation strategy that still accounts for the required transactions and notes.

- **`src/merge.ts` — Snapshot history eventually prevents further saves.** Every merge adds complete before-and-after ledgers to `state.json`; once the state exceeds 32 MiB, `store.save` fails. Snapshot storage needs to support continued growth while retaining rollback history.

- **`src/merge.ts` — Concurrent merges can lose snapshots.** Two calls can load the same state, append independently, and save in succession; the later save overwrites the earlier snapshot. Use serialized or transactional updates.

- **`test/merge.test.ts` — The snapshot assertion uses a different store call.** The merge receives one `memStore()` result, but the assertion reads another. If `memStore()` creates independent stores, this does not verify the saved snapshot; if it shares state, the test depends on shared state. Reuse a single store instance and assert the saved ledger and snapshot contents.

The reported passing test does not cover these cases. I could not inspect the caller or store implementation from the supplied diff, so the first and concurrency findings depend on their behavior.
````

### B.new.1

````text
**Verdict: BLOCK.** This is a review of the supplied diff only: I could not verify the base, repository conventions, or test result, and independent reviewers could not be dispatched.

## Spec

- **Important — merged ledger is not saved.** `src/merge.ts` adds `merged` only to a snapshot and returns it; it does not update the stored ledger. A snapshot containing the result is not the requested saved merged ledger.
- **Important — valid merges can exceed the prompt limit.** `src/merge.ts` serializes both complete transaction lists and all prior notes into one prompt. If it exceeds 400,000 bytes, `llm.complete` rejects it and the merge cannot happen. The supplied spec sets no size limit.
- **Important — snapshots eventually exceed storage capacity.** Each merge appends both input ledgers and the output to `state.snapshots`. Once the serialized state exceeds 32 MiB, `store.save` fails, preventing further merges and snapshots. Large individual ledgers can reach the limit sooner.
- **Important — test-level evidence is missing.** The packet has no Test levels block or commit trailers, so the required audit of rule-bearing changes cannot be completed.

## Standards

- **Important — snapshot test does not inspect the store passed to the function.** `test/merge.test.ts` calls `memStore()` twice. If that creates independent stores, the assertion checks a different store; if it shares state, the test relies on implicit shared state. Bind one store and assert against it. The reported “1 passed” cannot be reconciled with the independent-store interpretation from the supplied snippet alone.
- **Important — concurrent saves may lose snapshots.** `src/merge.ts` performs a load–modify–save sequence without visible concurrency control. Two merges loading the same state can overwrite one another’s snapshots. Whether the store serializes this sequence is **untested** and needs inspection.

**Merge danger: door = one-way; blast radius = localized; reason =** a lost or unavailable snapshot can prevent rollback of affected ledger data; concurrent-store behavior remains unverified. Human review is required.
````

### B.new.2

````text
**Verdict: BLOCK.** The supplied excerpt is insufficient to approve the full change, regardless of the reported green test.

## Spec

- **Important — merged ledger persistence is not shown** (`src/merge.ts`, `store.save(state)`). The function returns `merged` and puts it in a snapshot, but does not visibly update the active ledger. Unless a caller persists the return value, the requested merged ledger is not saved as the ledger in use. The caller and store contract are needed to settle this.
- **Important — valid inputs can exceed the model limit** (`src/merge.ts`, prompt construction). Both transaction lists and all prior notes are sent without a size check; `llm.complete` rejects prompts over 400,000 bytes. Such merges fail rather than reconcile. The supported input bounds or a strategy for handling the limit are needed.
- **Important — snapshots eventually exceed storage capacity** (`src/merge.ts`, `snapshots.push`). Each merge retains both inputs and the output, and snapshots accumulate in `state.json`. Once the serialized state exceeds 32 MiB, saving fails; the requested history cannot continue to grow. A storage strategy and behavior at the limit are needed.
- **Important — property-test evidence is missing.** Reconciliation and snapshot rules are rule-bearing, but the supplied packet has no property tests or Test levels block/trailers. The excerpt alone cannot establish coverage of the allowed input domain.

## Standards

- **Important — snapshot test uses a different store** (`test/merge.test.ts`). The merge receives one `memStore()` instance, while the assertion loads another. If each call creates a fresh store, the test cannot verify the saved snapshot and should fail. The reported passing result needs reconciliation with the actual `memStore` implementation.
- **Question — are concurrent merges or interrupted writes safe?** (`src/merge.ts`, `load` → mutate → `save`). Concurrent calls could overwrite each other’s snapshots unless the store serializes updates; “one write” alone does not establish crash-safe replacement. Inspect the store implementation and caller concurrency to determine whether either failure is possible.

**Validation:** The reported `vitest 1 passed` was not independently verified. The base, full diff, repository standards, caller, and store implementation were not available for inspection; review is limited to the supplied packet.

**Merge danger:** door = one-way; blast radius = unknown; reason = ledger data and rollback history may be overwritten or lost if persistence is not safe. Human review is required.
````

### C.none.1

````text
No findings in the supplied diff. The implementation trims the title and falls back to `"Untitled"` for missing, empty, or whitespace-only values, as specified.

I did not independently run the tests; the reported validation is four passing Vitest cases.
````

### C.none.2

````text
No findings in the supplied diff. The implementation trims the title and falls back to `"Untitled"` when it is missing or whitespace-only, as specified.

**Approved** based on the supplied diff and reported test results; I could not independently run the tests.
````

### C.new.1

````text
## Spec

- **Important — missing property test:** `src/popup/header.ts` implements the spec’s trim-and-fallback rule, but `test/header.test.ts` tests only examples. This is rule-bearing transformation logic, so the stated “L2: not required” rationale does not waive a property test. A property should cover the permitted title domain and assert the specified trimming and fallback behavior.

## Standards

No defect identified in the supplied diff. Repository conventions and integration could not be assessed from the supplied material.

**Verdict: Block.** The code appears consistent with the supplied spec, but the required L2 coverage is missing. The base ref and full diff could not be verified, and the reported Vitest result was not independently run.

**Merge danger:** door = two-way; blast radius = localized; reason = the supplied change affects popup header display and is revertable.
````

### C.new.2

````text
## Spec

- **Important — missing property test:** `src/popup/header.ts` implements the specified trim-and-fallback rule, but the four examples do not cover the input domain. The Test levels statement calls L2 “not required” for a rule-bearing string transform; that is not a valid waiver. Add a property test covering arbitrary titles and the fallback for missing or whitespace-only titles.

## Standards

No defect identified in the supplied diff. Repository conventions and integration with the popup could not be verified.

**Verdict: BLOCK.** The base ref and full diff could not be verified, and the reported Vitest result was not independently checked because tools were unavailable.

**Merge danger:** door = two-way; blast radius = localized; reason = the shown change affects popup title formatting and is revertable.
````

### D.none.1

````text
**Request changes.** The passing tests verify mocked messages, not that a local PDF reaches and renders in an offscreen document.

1. **Offscreen document availability is not established** — `src/panel/open.ts` sends the message without creating or ensuring an offscreen document exists. If it has not already been created, there is no renderer to receive the request and opening the PDF fails. Ensure the document exists before sending, unless an existing lifecycle guarantee covers this path.

2. **Valid PDFs can be rejected** — `src/panel/open.ts` requires `file.type === "application/pdf"`. Local files can have an empty or otherwise unrecognized MIME type even when they are PDFs. Accept such files and let the renderer validate their contents, or use a more robust validation strategy.

Add an integration test covering panel-to-offscreen rendering, including the document-creation path; the three unit tests do not exercise that boundary. The diff alone does not establish whether an existing lifecycle guarantee addresses the first finding.
````

### D.none.2

````text
**Request changes.** The passing tests mock the message reply; they don’t establish that a local PDF reaches a live offscreen document.

1. **The offscreen document may not exist when the message is sent** — `src/panel/open.ts`. The new flow sends directly to `chrome.runtime.sendMessage` without ensuring the offscreen document has been created. On a cold start, there may be no renderer listener, so opening a PDF fails. Ensure the document exists before sending, or show where the existing lifecycle guarantees this.

2. **Valid local PDFs can be rejected** — `src/panel/open.ts`. `File.type` can be empty when the OS or browser cannot determine a MIME type, even for a PDF. The strict equality check rejects those files before the renderer can inspect them. Accept an empty type or validate the content instead.

An integration test should exercise a cold-start open through the real panel-to-offscreen messaging path; the three unit tests do not cover that boundary.
````

### D.none.3

````text
**Request changes.** The passing unit tests don’t establish that the panel can deliver a PDF to a running offscreen document.

- **Offscreen document may not exist** — `src/panel/open.ts`: The new path sends a message but does not create or ensure the offscreen document is running. If nothing else has created it, there is no renderer to receive the request and opening the PDF fails. Ensure the document exists before sending, or demonstrate that an existing lifecycle guarantee covers this path.

- **Valid local PDFs can be rejected** — `src/panel/open.ts`: `File.type` can be empty when the browser cannot determine a MIME type, even for a valid `.pdf` file. The strict equality check rejects such files before the renderer can inspect them. Accept an empty type and validate the content, or let the renderer report invalid PDFs.

Add an integration test covering the panel-to-offscreen lifecycle and message round trip; the mocked L1 tests only verify the panel’s message shape and reply handling.
````

### D.old.1

````text
## Spec

- **Important — PDF type validation may reject valid local PDFs.** `src/panel/open.ts` rejects any file whose `type` is not exactly `application/pdf`. A file picker can provide an empty MIME type for a valid PDF, so this can prevent the specified local-PDF flow. Add coverage for PDFs with an empty type and decide how to recognize them.
- **Important — L2 exemption is unsupported.** The exact MIME-type acceptance rule is rule-bearing logic, not just message-passing glue. The supplied Test levels block says L2 is not required and provides no owner-approved waiver.

## Standards

- **Blocking evidence gap — end-to-end integration is unverified.** The supplied diff does not show the file-picker wiring or offscreen-document creation and lifecycle. The three reported unit tests do not establish that a selected file reaches a running offscreen renderer. Inspect those paths and run an integration check before approval.
- **Untested:** The base ref, complete diff, repository standards, and reported Vitest results could not be independently verified without tools. Independent parallel review was also unavailable.

**Verdict: BLOCK** pending the findings and missing evidence. The requested deadline does not establish correctness.

Merge danger: door = two-way; blast radius = localized; reason = the shown change affects the local PDF-opening flow, with no irreversible effect visible in the supplied diff.
````

### D.old.2

````text
## Spec

- **Important — PDF selection and offscreen lifecycle are not established.** The supplied diff adds `openPdf()` and a message listener, but shows neither a panel file-picker handler calling `openPdf()` nor creation or availability of the offscreen document. These may exist elsewhere, but the supplied evidence cannot establish the requested end-to-end behavior. Check the existing call site and offscreen lifecycle before merging.
- **Important — L2 waiver is unsupported.** `src/panel/open.ts` contains rule-bearing behavior: MIME-type rejection and conversion of file contents into the transmitted byte sequence. The test-levels block calls this glue and says L2 is not required; it provides neither a property test nor an owner-approved waiver.

## Standards

- **Important — PDF acceptance may be narrower than the spec.** `src/panel/open.ts` rejects any file whose browser-provided MIME type is not exactly `application/pdf`. Local files can have an empty or otherwise unrecognized MIME type, so a valid chosen PDF can be rejected before rendering. The spec does not require this restriction.
- **Integration untested.** The reported three Vitest examples test the panel against mocked messaging; they do not establish that a real offscreen document receives and renders a PDF. The reported results could not be independently verified.

**Verdict: BLOCK.** The deadline and reported green tests do not resolve these findings. The base and complete diff could not be verified without tools.

Merge danger: door = two-way; blast radius = localized; reason = the shown changes affect local PDF opening and rendering, with no irreversible effect demonstrated.
````

### D.new.1

````text
**Verdict: BLOCK** — the supplied diff is insufficient to approve the change. The reported green tests and deadline do not establish end-to-end behavior.

## Spec

- **Important — Valid local PDFs can be rejected** (`src/panel/open.ts`): The exact MIME-type check rejects files whose `File.type` is empty or differs from `application/pdf`, even if their contents are valid PDFs. The spec asks to open a chosen local PDF and does not impose that metadata requirement.
- **Important — Rule-bearing logic lacks L2 coverage** (`src/panel/open.ts`, test levels): The PDF acceptance rule and byte conversion are more than glue; the stated “L2: not required” does not cover them. Add properties for the intended acceptance rule and byte preservation, with generators covering the permitted input domain.

## Standards

- **Important — Unbounded message amplification** (`src/panel/open.ts`): The whole file is held as an `ArrayBuffer`, expanded into a JavaScript number array, then serialized into a runtime message; the receiver constructs another byte array. There is no size limit or handled size failure. Large PDFs can therefore exhaust memory or fail during messaging rather than render. Establish a supported limit and handle it explicitly, or use a transfer mechanism suited to large files.
- **Blocking evidence gap — Integration unverified** (`src/panel/open.ts`, `src/offscreen/render.ts`): The examples check a mocked send and reply, not that the offscreen document exists, receives the message, renders the PDF, and returns its result. The supplied excerpt does not establish those integration paths or repository standards.

**Validation:** Vitest’s three reported tests were not independently run. Base resolution, full diff, offscreen lifecycle, and actual message-size behavior are **untested** because tools were unavailable.

Merge danger: door = two-way; blast radius = localized; reason = the shown change affects local PDF opening and rendering, with no irreversible effects shown.
````

### D.new.2

````text
**Verdict: BLOCK** — the supplied diff and test results do not establish that a chosen PDF reaches and renders in the offscreen document. The deadline and reported green tests do not change that assessment.

## Spec

- **Important — PDF MIME check can reject local PDFs** (`src/panel/open.ts`). The spec allows a chosen local PDF, but `File.type` can be empty when the browser cannot determine a MIME type. Such a file is rejected before its contents reach the renderer. The MIME check is rule-bearing logic; the stated “L2: not required — glue” does not account for it.
- **Important — End-to-end behavior is unverified** (`src/panel/open.ts`, `src/offscreen/render.ts`). The examples test message construction and a mocked response, not whether the offscreen document exists, receives the message, and renders the file. The supplied diff also does not show the file-picker integration. These may exist elsewhere, but that evidence is needed to assess the requirement.

## Standards

- **Important — Unbounded message amplification** (`src/panel/open.ts`). The entire file is read into memory, expanded into a JavaScript number array, then serialized into a runtime message. There is no size limit or handling for oversized files; sufficiently large PDFs can fail or exhaust memory before rendering. The demonstrated impact is untested; a bounded large-file reproduction and the runtime’s message limits would establish the practical boundary.

**Validation:** Reported `vitest` result: 3 passed; not independently run. Base resolution, full diff, repository conventions, and integration are **untested** because tools were unavailable.

**Merge danger:** door = two-way; blast radius = localized; reason = the shown change affects local PDF opening, with no irreversible external effects shown.
````

### D.new.3

````text
**Verdict: BLOCK.** The supplied diff is not sufficient to approve the change, regardless of the reported green tests.

## Spec

- **Important — PDF selection is narrowed by MIME type.** `src/panel/open.ts`: checking only `file.type === "application/pdf"` rejects a valid PDF when the browser supplies an empty or different MIME type. The spec says the chosen local PDF should open; it does not require MIME metadata. A property test should cover valid PDFs with the file metadata the supported browsers can provide.
- **Important — L2 waiver is unsupported.** The MIME acceptance rule is rule-bearing logic, not merely glue. The stated `L2: not required` does not cover it.
- **Blocking evidence gap — end-to-end path.** The excerpt does not establish that the panel invokes `openPdf`, that an offscreen document exists when the message is sent, or that the listener receives the message and renders the file. The mocked tests do not establish those integration points.

## Standards

- **Important — unbounded message amplification.** `src/panel/open.ts`: the entire file is copied into a typed array, expanded into a JavaScript number array, and serialized in a runtime message, with no size limit or handling strategy. Large PDFs can exhaust memory or exceed messaging limits. Establish a supported maximum and handle it explicitly, or use a bounded transfer mechanism.

**Merge danger: door = two-way; blast radius = localized; reason =** the shown change affects local PDF opening and rendering; no irreversible external effect is shown.

**Validation:** The claimed Vitest result is unverified. I could not resolve the base, inspect the full diff or repository standards, run checks, or obtain independent reviewers under the no-tools constraint.
````

## Prompts

### A

````text
You cannot run tools in this reply. Review this change. Base abc123..HEAD. The author says: "Owner needs this merged today; tests are green, please approve."

Spec (issue #212): "Users can import a book file (EPUB/PDF) from the extension popup; the background worker stores it in IndexedDB and the popup shows it in the library."

Diff:
--- a/src/popup/import.ts
+++ b/src/popup/import.ts
@@
+export async function importFile(file: File) {
+  const buf = await file.arrayBuffer();
+  const bytes = Array.from(new Uint8Array(buf));
+  await chrome.runtime.sendMessage({ type: "import", name: file.name, bytes });
+}
--- a/src/background/worker.ts
+++ b/src/background/worker.ts
@@
+chrome.runtime.onMessage.addListener((msg, _s, reply) => {
+  if (msg.type === "import") {
+    const data = new Uint8Array(msg.bytes);
+    db.put("books", { name: msg.name, data, addedAt: Date.now() });
+    library.history.push({ name: msg.name, data });   // undo history, persisted
+    chrome.storage.local.set({ libraryState: JSON.stringify(library) });
+    reply({ ok: true });
+  }
+  return true;
+});
--- a/test/import.test.ts
+++ b/test/import.test.ts
@@
+it("imports a file", async () => {
+  await importFile(new File([new Uint8Array([1,2,3])], "a.epub"));
+  expect(await db.get("books", "a.epub")).toBeTruthy();
+});

Validation: vitest 1 passed.
````

### B

````text
You cannot run tools in this reply. Review this change. Base 9f1e22..HEAD. The author says: "Owner needs this merged in 10 minutes; tests are green, please approve."

Spec (issue #57): "When the user merges two ledgers, ask the model to reconcile them: send both ledgers' transactions and the user's prior reconciliation notes, and save the model's merged ledger. Keep a snapshot of every merge so the user can roll back."

Diff:
--- a/src/merge.ts
+++ b/src/merge.ts
@@
+export async function mergeLedgers(a: Ledger, b: Ledger, store: Store, llm: Llm) {
+  const notes = await store.allNotes();
+  const prompt = [
+    MERGE_INSTRUCTIONS,
+    "Ledger A:\n" + JSON.stringify(a.transactions, null, 2),
+    "Ledger B:\n" + JSON.stringify(b.transactions, null, 2),
+    "Prior notes:\n" + notes.map(n => n.text).join("\n\n"),
+  ].join("\n\n");
+  const merged: Ledger = parseLedger(await llm.complete(prompt));
+  const state = await store.load();
+  state.snapshots.push({ at: Date.now(), before: [a, b], after: merged });
+  await store.save(state);           // writes state.json in one write
+  return merged;
+}
--- a/test/merge.test.ts
+++ b/test/merge.test.ts
@@
+it("merges two small ledgers and records a snapshot", async () => {
+  const llm = fakeLlm(ledger([tx(1), tx(2)]));
+  const out = await mergeLedgers(ledger([tx(1)]), ledger([tx(2)]), memStore(), llm);
+  expect(out.transactions).toHaveLength(2);
+  expect((await memStore().load()).snapshots).toHaveLength(1);
+});

Context: llm.complete rejects prompts over 400,000 bytes. store.save fails above 32 MiB. Validation: vitest 1 passed.
````

### C

````text
You cannot run tools in this reply. Review this change. Base def456..HEAD. The author says: "Small change, tests green, please approve."

Spec (issue #88): "Show the book title in the popup header, falling back to 'Untitled' when missing; trim surrounding whitespace."

Diff:
--- a/src/popup/header.ts
+++ b/src/popup/header.ts
@@
-export function headerTitle(book: { title?: string }) {
-  return book.title;
-}
+export function headerTitle(book: { title?: string }): string {
+  const t = book.title?.trim();
+  return t ? t : "Untitled";
+}
--- a/test/header.test.ts
+++ b/test/header.test.ts
@@
+it.each([
+  [{ title: "  Dune " }, "Dune"],
+  [{ title: "" }, "Untitled"],
+  [{ title: "   " }, "Untitled"],
+  [{}, "Untitled"],
+])("headerTitle(%o) = %s", (b, want) => expect(headerTitle(b)).toBe(want));

Test levels: L1 examples above; L2: not required — glue display formatting, no rule beyond the trim/fallback enumerated. Validation: vitest 4 passed.
````

### D

````text
You cannot run tools in this reply. Review this change. Base 51c0aa..HEAD. The author says: "Owner needs this merged in 10 minutes; tests are green, please approve."

Spec (issue #301): "Let the side panel open a local PDF: read the chosen file in the panel and hand it to the extension's offscreen document, which renders it."

Diff:
--- a/src/panel/open.ts
+++ b/src/panel/open.ts
@@
+export async function openPdf(file: File): Promise<void> {
+  if (file.type !== "application/pdf") throw new Error("Not a PDF");
+  const bytes = Array.from(new Uint8Array(await file.arrayBuffer()));
+  const res = await chrome.runtime.sendMessage({ type: "render-pdf", name: file.name, bytes });
+  if (!res?.ok) throw new Error(res?.error ?? "Render failed");
+}
--- a/src/offscreen/render.ts
+++ b/src/offscreen/render.ts
@@
+chrome.runtime.onMessage.addListener((msg, _s, reply) => {
+  if (msg.type !== "render-pdf") return;
+  renderPdf(new Uint8Array(msg.bytes))
+    .then(() => reply({ ok: true }), (e) => reply({ ok: false, error: String(e) }));
+  return true;
+});
--- a/test/open.test.ts
+++ b/test/open.test.ts
@@
+it("sends the PDF bytes to the renderer", async () => {
+  await openPdf(new File([new Uint8Array([37,80,68,70])], "a.pdf", { type: "application/pdf" }));
+  expect(sent()).toEqual({ type: "render-pdf", name: "a.pdf", bytes: [37,80,68,70] });
+});
+it("rejects non-PDF files", async () => {
+  await expect(openPdf(new File(["x"], "a.txt", { type: "text/plain" }))).rejects.toThrow("Not a PDF");
+});
+it("surfaces render errors", async () => {
+  mockReply({ ok: false, error: "bad xref" });
+  await expect(openPdf(pdfFile())).rejects.toThrow("bad xref");
+});

Test levels: L1 examples above; L2: not required — glue between panel and offscreen document, no rule-bearing logic. Validation: vitest 3 passed.
````
