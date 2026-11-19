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

The run above is **content-equivalence only**: the overlay text was handed to
the model, so it never decided to read the file.

## Load path with tools (2026-11-19)

The overlay was trimmed to what the owner's always-loaded instructions do not
name (one gate invocation line). Arms read the file through the harness's own
read tool. System file = `body/SKILL.md` + `body/pi.md`; prompt: two worker
results integrated, follow the skill including any files it says to read,
give the exact verification commands and the parallel dispatch, invent no
tools.

- **Pi:** `pi -p --no-session --no-context-files --no-skills --tools read
  --model openai-codex/gpt-6.1-terra --thinking low --append-system-prompt
  <file> --mode json`, n=2 per arm. STRANGER arm: overlay file moved aside
  for the run, then restored.
- **Claude Code:** `claude -p --model sonnet --tools Read --allowedTools Read
  --append-system-prompt <file> --output-format stream-json`, n=1 per arm
  (Terra is not available in Claude Code). Its normal user instructions
  stayed loaded, so its STRANGER arm is "owner machine without the overlay",
  not a true stranger.

**Pass criteria.** OWNER: a read tool call on the overlay path, and the
overlay's gate invocation in the answer. STRANGER: the failed read does not
stop it, and it names no owner tool it was not given elsewhere.

**Result: Pi OWNER 2/2, STRANGER 2/2; Claude Code OWNER 1/1, STRANGER 1/1.**
- Pi owner-1/2: read call on the absolute overlay path; answer gives
  the overlay's gate line verbatim, in the background with a completion wake
  and a parallel reviewer.
- Pi stranger-1/2: read of the overlay returned ENOENT; the agent went on to
  "the project's documented full gate … using its required wrapper" and named
  no owner tool.
- Claude Code owner-1: Read on the overlay path succeeded; the answer uses the
  overlay's gate line.
- Claude Code stranger-1: Read returned "File does not exist"; it continued
  and used the wrapper and runner names from its always-loaded user
  instructions, without the overlay's gate options (that is the intended
  division of labour, not invention).
- `~` expansion: in both harnesses the model expanded `~` itself and passed
  an absolute path to the read tool, so the instruction wording needs no
  change. Not checked in Codex.

Raw outputs were in `/tmp/` (temporary).
