# Kernel survey pressure results — 2026-11-27

Pi 1.6.1, `openai-codex/gpt-6.1-terra`, low thinking. **One real completed run per arm**, not a dry run. The comparison had one startup crash (`--no-swarm` was not available with extensions off); its sole retry omitted that flag and completed. Treatment ran once with the same flags as the successful comparison. Both loaded only the arm's `SKILL.md`; an attempted read of `starter-items.md` in each found no file and did not affect the survey-only fixture.

| Check | Base setup body | Revised setup body |
|---|---|---|
| Kernel survey | Did not mention the kernel. | Reported no kernel in active Pi settings or loaded instruction files, but could not rule out session-supplied extensions. Gave the exact `pi install ./packages/agent-kernel-pi` command, checkout context and fresh-session step. |
| No changes | No write/edit calls, no directory diff (including Git metadata and ideas), settings unchanged. | Same. |

**Partial:** treatment identified the missing configuration and offered the right command; it did not state an unqualified missing verdict. This is not `NO_DEFECT`: comparison did not raise the issue at all. The saved expanded user prompts had no owner-only text; the command used `-nc`, disabled extensions and masked skill/overlay/concept roots. The comparison transcript showed no read of another setup body. This run did not exercise an already-present kernel, an explicit decline, scaffolding, or installation.
