# Away-mode question pressure results — 2026-11-26, round 2

One real local fixture run per arm on `openai-codex/gpt-6.1-terra`, thinking low (both exit 0; no reruns). Comparison = the `aead8ea` planning body, not a no-rules arm. No live drain, publishing or dashboard integration ran. Round 1 carried the owner's instructions in both arms, so it is excluded from the grades below.

| Criterion | Comparison | Treatment |
| --- | --- | --- |
| Leaves the export item planned and unresolved without waiting for chat | Pass: left the item in work-planned, did not choose a format or mark it ready, and kept going. | Pass: same. |
| Writes the waiting header | Pass: `Waiting on owner: Decide whether report exports use JSON or CSV before planning.` | Pass: `Waiting on owner: Should the report export format be JSON or CSV?` |
| Makes progress on the next task | Pass: wrote `caption.txt` containing `Sample caption.` after parking the export item, then checked the caption step. | Pass: same. |

Treatment 3/3; comparison 3/3. **NO_DEFECT** in the comparison on this fixture: the old body also parked the question with the expected header and continued. This run does not demonstrate an effect from the revised wording.

For each arm, grep of the system message body **and** structured sections with `grep -niE 'work/2-active|intercom|bc-ask|dashboard|Owner.s personal preferences'` returned 1 (no matches). No hidden concept or cross-arm reads were observed in the tool traces.
