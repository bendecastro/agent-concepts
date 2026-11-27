# Regression guardrails packet: dry-run result

[Scenario and grading](scenario-regression-guardrails.md). One completed `openai-codex/gpt-6.1-terra` low dry run per arm on 2026-11-27 UTC. Comparison used the base pipeline body at `a2d45ba`, not a no-skill arm: the missing instruction was in the old packet. Both arms masked deployed skills, overlays, the three concept roots and the resolved always-loaded Pi instruction files; auto-context was off. Neither captured system prompt contained owner-only instruction text, and neither transcript read another body copy. The comparison required one retry after a Pi CLI option error before inference.

| Evidence | Comparison | Treatment |
| --- | --- | --- |
| Build and review packets | No explicit guardrails skill load. The build packet still required a durable check; the review packet checked its quality. | Build packet required the guardrails skill and the transcript shows its body being read. Review packet asked whether the check would reject the 100-byte artifact. |
| Builder's check | Strengthened `verify.py` from a suffix check to exact payload equality. | Added a 25-byte artifact cap to `verify.py`, retained the behavior check, and documented the cap on the guardrails page. |
| Regression replay | New verification failed on the original 100-byte artifact and passed on the restored 25-byte artifact. | New verification failed on the original 100-byte artifact and passed on the restored 25-byte artifact. |

**NO_DEFECT for check retention on this fixture:** both arms added an effective check. The treatment demonstrates explicit skill loading, review instructions, and guardrail documentation; it does not demonstrate a difference in whether a check was left. No live worker or reviewer dispatch, drain, or landing ran.
