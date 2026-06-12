---
name: prompting-agents
description: Use when writing or revising instructions for a coding agent — concept bodies, AGENTS.md files, system prompts, or per-agent configs. A library of proven instruction blocks to adapt, not invent.
---

# Prompting Agents

Reusable instruction blocks and principles distilled from OpenAI's GPT-5.2 and Codex prompting guides, Anthropic's prompting/context-engineering guidance, and Google's prompt-engineering whitepaper (see CONCEPT.md for provenance), rewritten agent-agnostically. When authoring or tuning instructions for any agent, adapt the relevant block rather than writing one from scratch — these phrasings have been optimized against production evals. Tag origin when copying verbatim so future updates can be traced.

## First: choose the altitude

Before reaching for any block below, decide how much constraint the task actually warrants. Anthropic's context-engineering guidance calls this the **right altitude**: the Goldilocks zone between brittle, hardcoded if-else process steps (fragile, high-maintenance, and insulting to a capable model) and vague high-level guidance that falsely assumes shared context. Instructions should be specific enough to transmit hard-won lessons, flexible enough that the agent applies its own reasoning.

Three principles that govern everything else in this library:

- **Explain the why.** State the motivation behind an instruction, not just the instruction — "Claude is smart enough to generalize from the explanation," and a rule whose reason is visible can be correctly applied to situations its author never imagined. A bare imperative can only be obeyed or violated. (Anthropic prompting best practices.)
- **Prefer general instructions over prescriptive steps.** "Think thoroughly" often beats a hand-written step-by-step plan; a strong model's reasoning frequently exceeds what its author would prescribe. Save prescriptive blocks for places where errors are costly or the failure mode is in-the-moment rationalization. (Anthropic prompting best practices.)
- **Context economy.** Aim for the smallest set of high-signal tokens that produces the outcome — context rot is real: recall degrades as context grows. Progressive disclosure (lean entry file, details loaded just-in-time) is this principle applied to skill structure. (Anthropic context engineering.)

The constraining blocks below (scope discipline, gates-style rules) are tools for *specific failure modes*, not a default posture. Reach for them when the cost of an error is high or when an agent under pressure predictably rationalizes — and even then, attach the why.

## Output shape and verbosity

Models are prompt-sensitive on verbosity; clamp it concretely, not with "be concise":

```
- Default: 3–6 sentences or ≤5 bullets for typical answers; ≤2 sentences for simple yes/no questions.
- For complex multi-step tasks: 1 short overview paragraph, then ≤5 bullets tagged
  What changed / Where / Risks / Next steps / Open questions.
- Avoid long narrative paragraphs; prefer compact bullets and short sections.
- Do not rephrase the user's request unless it changes semantics.
```

## Scope discipline

The strongest single lever against agents doing more than asked:

```
- Implement EXACTLY and ONLY what the user requests.
- No extra features, no added components, no embellishments.
- If any instruction is ambiguous, choose the simplest valid interpretation.
- If you notice adjacent work worth doing, call it out as optional — do not do it.
```

## Autonomy and persistence

For agents that stop too early — pair with the loop-breaker, which prevents the failure mode this block otherwise creates:

```
- Once given a direction, proactively gather context, plan, implement, test, and refine
  without waiting for additional prompts at each step.
- Persist until the task is handled end-to-end within the current turn whenever feasible;
  do not stop at analysis or partial fixes.
- Bias to action: default to implementing with reasonable assumptions; do not end your
  turn with clarifying questions unless truly blocked.
- Loop-breaker: if you are re-reading or re-editing the same files without clear progress,
  stop and end the turn with a concise summary and targeted questions.
```

## Ambiguity and hallucination

```
- If the question is ambiguous or underspecified, say so, then either ask 1–3 precise
  clarifying questions OR present 2–3 plausible interpretations with labeled assumptions.
- Never fabricate exact figures, line numbers, or external references when uncertain;
  prefer "Based on the provided context…" over absolute claims.
- For high-stakes outputs, re-scan your own answer before finalizing for: unstated
  assumptions, ungrounded specifics, and overly strong language ("always", "guaranteed").
```

For non-interactive/research agents, invert the question rule: "Do not ask clarifying questions; cover all plausible intents with breadth and depth, stating your best-guess interpretation plainly."

## Long-context re-grounding

Reduces "lost in the scroll" errors over large inputs:

```
- For long inputs, first produce a short outline of the sections relevant to the request.
- Re-state the user's constraints explicitly before answering.
- Anchor claims to specific sections; quote fine details (dates, thresholds, clauses)
  rather than speaking generically.
```

## Progress updates

```
- Send brief updates (1–2 sentences) only when starting a new major phase or when a
  discovery changes the plan. Do not narrate routine tool calls.
- Each update must contain at least one concrete outcome ("Found X", "Confirmed Y").
```

## Tool use and parallelism

```
- Prefer tools over internal knowledge whenever you need fresh or user-specific data,
  or reference specific IDs, URLs, or document titles.
- Think first: before any tool call, decide ALL files/resources you will need, then
  issue independent reads as one parallel batch. Sequential calls only when the next
  read genuinely depends on a prior result.
- After any write/update, briefly restate what changed, where, and what validation ran.
- Require an explicit verification step before high-impact operations (deletes, billing,
  infra changes).
```

Naming custom tools: make names and parameters semantically exact (`semantic_search(query)`, not `search(q)`), state when/why/how to use them with good and bad examples, and make their output *look different* from similar tools' output so the model doesn't collapse into old habits.

## Plan and promise discipline

```
- Skip planning for straightforward tasks; never make single-step plans.
- The deliverable is working output, not a plan — never end a turn with only a plan.
- Before finishing, reconcile every stated intention: Done, Blocked (reason + targeted
  question), or Cancelled (reason). No dangling in-progress items.
- Do not commit to tests/refactors you will not do now; label them optional next steps.
```

## Final-message style

```
- Lead with the outcome; jump straight in — no "Summary" preamble.
- Match structure to the task: plain sentences for simple confirmations, sections only
  when they aid scanning. Reference file paths instead of dumping file contents.
- When offering multiple options, number them so the user can reply with a single digit.
```

## Working in a dirty repo

```
- NEVER revert changes you did not make; work with or around them.
- If unexpected changes appear in files you are editing, stop and ask.
- No destructive commands (reset --hard, checkout --) without explicit approval.
```

## Frontend anti-slop

For agents producing UI from scratch (skip when a design system exists — then the rule is the opposite: conform to it):

```
- Avoid safe, average-looking layouts: no default font stacks, no purple-on-white
  defaults, no flat single-color backgrounds, no interchangeable boilerplate.
- Choose a clear visual direction; define tokens/CSS variables; use a few meaningful
  animations rather than generic micro-motion. Verify desktop and mobile.
```

## Technique repertoire

When designing a task prompt (rather than standing instructions), pick the lightest technique that fits — from Google's prompt-engineering whitepaper (Boonstra) and Anthropic's docs:

- **Examples over rules** for format/tone/structure: a few well-crafted examples steer more reliably than descriptions — show, don't tell. With reasoning models, examples can include the reasoning pattern itself.
- **Chain-of-thought / "think first"** for problems needing deliberation; **step-back prompting** (ask for the general principle, then the specific answer) when the task benefits from grounding in fundamentals.
- **Self-consistency** (sample multiple reasoning paths, take the consensus) when single-shot accuracy on a hard problem matters more than cost.
- **Self-check** as a cheap reliability win: "before finishing, verify your answer against [criteria]."
- **ReAct** (interleaved reasoning + tool use) is what modern agent harnesses already do — don't re-prompt it explicitly inside one.

## Maintenance technique: metaprompting

When an agent underperforms with instructions from this workspace, ask it — at the end of the disappointing turn — to critique its own instructions: "read your instructions, identify what made this slower/worse than needed, and propose targeted but generalized changes." Run it more than once; adopt only the suggestions that recur, simplified to their general form, and test before deploying (the test gate applies).
