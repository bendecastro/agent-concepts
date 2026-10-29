# Audit and rename existing names

Inventory names across code, config, timers/services, docs/UI and persisted records. Include strings and messages, not just identifiers. Record meaning, job, persisted surfaces and evidence locations. Find collisions: one word with several meanings, one job with several names, one name doing several jobs; flag misleading names using the checklist and cold-read test.

Propose an old → new map with reasons, splits by use and persistence costs. Example: `arch-opt-out-review` used for exemption and final-version verdicts → `review-code-exemption` / `review-final-version`. Why: one overloaded label cannot describe two distinct verdicts. Hand glossary updates, conflicts and ADR decisions to `domain-modeling`.

When carrying out the requested rename:

1. Keep the old → new map in **one module**, its single home; all compatibility readers import it rather than copying mappings.
2. Every reader of persisted records normalizes old names through that map. Never rewrite append-only history.
3. For renamed append-only ledgers, read both the legacy and new file; writers use only the new file. Test that legacy and new records remain visible together.
4. A migration script for live mutable state defaults to dry-run, makes backups before mutation and refuses while work is running. Test all three safeguards.
5. Add a regression test scanning for retired names, including strings and messages. Permit only explicit legacy contexts needed by compatibility, historical records and their tests; unexpected hits fail.
6. Through `domain-modeling`, add a **Retired terms** glossary section stating the permitted legacy contexts in conceptual terms, not implementation paths. Example: `buyer-review` → `propose-improvements`, with the retired spelling permitted only in historical records and compatibility handling. Why: readers need continuity without reviving the old vocabulary.

Verify old-record normalization, dual-ledger reads, new-only writes and the retired-name scan before reporting the rename complete.
