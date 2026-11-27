# Results: setup with installed wiki tools only

[Scenario and rubric](pressure-installed-wiki-tools.md). One real consumer run per arm on `openai-codex/gpt-6.1-terra`, low, base bodies at `ec5f728` versus revised bodies. This was not a dry run of the CLI actions: both consumers ran registration-entry generation, lint and search. Neither changed the real qmd registry or installed a timer; those actions were not in the run. Both Pi processes returned 2 but the sessions record normal `stop` completion and all four requested artifacts; no crash, no retry.

| Criterion | Base | Revised |
| --- | --- | --- |
| Correct archetype scope | Fail: `scope.md` skips indexing for code, ops and hybrid because of the introductory scope sentence. | Pass: `scope.md` applies default indexing and lint to all five and offers promotion only for learning and knowledge. |
| Real registration YAML | Pass: installed detector exited 0, prints `compass` and `compass-project`, rooted in mechanics and repo respectively. | Pass: same. |
| Real lint report | Pass: installed detector exited 0 and reported visible layout and no promotion. | Pass: same. |
| Installed search and verification | Pass: inferred a local script path, then widened the search boundary from `.bc-agent/` to the project root; result was `docs/research/calibration.md` and the consumer opened it. | Pass: used the installed script, also widened to the project root and opened the matching file. |

No alternate copy of either tested skill was read. A revised-arm probe for a private skill failed against the masked root. Both fixture trees remained unchanged apart from Git's index stat-cache refresh. The pressure run distinguishes archetype wording (3/4 base, 4/4 revised), not the search repair: the old consumer worked around the literal checkout-dependent command, which the deterministic installed-layout regression catches directly.
