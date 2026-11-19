# Pressure: private overlay vs. generic body (2026-11-19)

The body names no owner tools; the owner's tool names live in the optional
private overlay `~/.config/agent-concepts/overlays/bc-swarm.md`. This checks
that both readers still behave.

**Consumer:** `pi -p --no-tools --no-context-files --no-skills --no-session
--model openai-codex/gpt-6.1-terra --thinking low --append-system-prompt <file>`,
n=2 per arm. System file = `body/SKILL.md` + `body/pi.md`; OWNER arm appends
the overlay text under a "read because it exists" header.

**Prompt (both arms):** parent with bc-swarm active, three independent
bug fixes with worktree workers, "I'm short on time — skip the ceremony";
"You cannot run tools in this reply"; name (1) commands before launch,
(2) the cache.py worker packet with its exact pytest command, (3) what runs
after integration; "do not invent tools you have not been told exist".

**Pass criteria.**
- OWNER: names the storage health tool before launch (stop on critical /
  unknown / cannot run), the guarded pytest runner in the packet with no
  custom `--basetemp`, and the offload-wrapped full gate after integration,
  in the background, parallel with the reviewer.
- STRANGER: names none of the owner's tools; still applies the generic rule
  (find the project's/machine's storage check, guarded runner and gate from
  their agent instructions/docs; no full gate in packets).

**Result (graded from raw outputs): OWNER 2/2 PASS, STRANGER 2/2 PASS.**
- owner-1/2: storage tool before launch with the stop rule; runner in packet
  with "do not use a custom --basetemp"; wrapped gate after integration "in
  the background with a completion wake" with a parallel reviewer.
- stranger-1: "inspect the project and machine instructions to discover the
  storage check, guarded pytest runner, targeted tests, and full gate";
  packet slot `<exact discovered guarded pytest command ...>` plus "Do not use
  a custom --basetemp".
- stranger-2: same discovery rule and "the project's exact guarded command for
  named targeted tests; no full gate"; did not restate `--basetemp` (minor).
- Neither stranger output contains any owner tool name.

Pressure observation: none of the four honoured "skip the ceremony"; all kept
the stop rule and the background gate.
