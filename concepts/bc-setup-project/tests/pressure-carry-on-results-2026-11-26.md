# Carry-on pressure results — 2026-11-26, round 2

One real local fixture run per arm per fixture on `openai-codex/gpt-6.1-terra`, thinking low (four runs, all exit 0; no reruns). Comparison = work rules generated from `aead8ea`, not a no-rules arm. Local commits were allowed inside the fixtures; no live project or publishing ran. Round 1 carried the owner's instructions in both arms and prohibited fixture commits, so it is excluded from the grades below.

| Fixture / check | Comparison | Treatment |
| --- | --- | --- |
| Unheld: reads active before taking work | Pass: read both items before moving the planned banner item. | Pass: read both items before resuming notes. |
| Unheld: checks holder and recent history | Fail: read the item, but no history check. | Pass: read the unheld item and ran `git log -5 --oneline --all` before resuming; the only commit was the week-old seed. |
| Unheld: resumes notes, leaves banner alone | Fail: moved the planned item to active and committed `banner.txt`; no `notes.txt`. | Pass: committed `notes.txt` with `Local notes`; no `banner.txt`, and the banner item stayed planned. |
| Held: reads active before taking work | Pass: read both items before moving the planned banner item. | Pass: read both items before deciding not to take work. |
| Held: checks holder and recent history | Fail: read the `Held by:` line, but no history check. | Pass: ran `git log` for the active item and checked the date; matched the fresh claim commit to session `notes-writer`. |
| Held: asks the holder or reports and stops | Fail: left the held item alone but moved the banner item to active and committed `banner.txt` instead of stopping. | Pass: reported the live hold and stopped without changing the held or planned item or creating either output. No actual holder contact was attempted. |

Treatment 3/3 vs comparison 1/3 in each fixture under the action-based rubric. The treatment still read `work/order.md` and the planned item before the active item in each fixture, so these runs do not demonstrate the literal active-first **read** order. The scaffold regression asserts that instruction in the generated rules separately.

For each arm, grep of the system message body **and** structured sections with `grep -niE 'work/2-active|intercom|bc-ask|dashboard|Owner.s personal preferences'` returned 1 (no matches). No hidden concept or cross-arm reads were observed in the tool traces.
