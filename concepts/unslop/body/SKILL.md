---
name: unslop
description: >
  Remove the tells that make human-facing text read as machine-generated,
  and put specifics back in their place. Use for docs, READMEs,
  announcements, emails, blog and marketing copy, research writeups, and
  shipped artifacts like commit messages and PR bodies. Triggers: unslop,
  AI slop, sounds like AI, reads like ChatGPT, de-AI this, AI tells, make
  it sound human, remove the AI voice. Not for chat replies, code, or
  agent-facing instructions.
---

# Unslop

## What is actually wrong

LLM prose regresses to the mean. Specific, unusual, checkable facts get
replaced by generic, positive, statistically common ones: "inventor of
the first train-coupling device" becomes "a revolutionary titan of
industry". Every tell below is a symptom of that one movement, not the
disease.

**A pass that removes tells without adding specifics has failed.** It has
made vague content harder to detect, which is worse than leaving it
obviously vague. Why: the reader's real complaint is that the text
circles a point without landing on it. Deleting "vibrant" does not make
the sentence say anything.

So the test for every edit: does the sentence now carry a fact, a number,
a name, a mechanism, or an instruction that it did not carry before? If
you cannot restate it as one of those, cut the sentence instead of
polishing it.

## When this applies

Human-facing text that ships: docs, READMEs, announcements, emails, blog
and marketing copy, SEO pages, research writeups, changelogs, commit
messages, PR and issue bodies.

**Not chat replies** (`agent-kernel` § Final response carries a thin always-on
clause for those, because a model-invoked skill cannot fire on every turn),
**not code**, and **not agent-facing instructions** — skill bodies,
`AGENTS.md`, kernels, gates. Agent instructions go to `prompting-agents`.
Why: those documents deliberately use bold lead-ins, parallel structure, and repeated
why-clauses, and every one of those reads as a tell. Unslopping them
strips the reasons a capable agent needs and leaves bare imperatives.
See **Never**, below: this one holds even when the user insists.

Leave code, commands, logs, diffs, and quoted file contents untouched.

## Modes

**Your own draft: fix it silently before shipping.** No report, no
permission request. Editing your own unshipped text is not a change to
anything the user owns.

**Text you did not write: report first, rewrite only when asked.** Why:
someone's prose is their voice, and an unsolicited rewrite is a meaning
change they never authorized. Report as a short list of located tells,
worst first.

## No single tell is evidence

One "landscape", one em dash, one triad proves nothing — humans write all
of them, and the models learned them from humans. What reads as machine
authorship is **accumulation**: the same handful of moves repeating across
paragraphs. Before calling text sloppy, name at least two co-occurring
patterns from different sections below.

Humans are near chance at this judgment. Heavy LLM users reach roughly
90%, which still means one false call in ten.

## Constructions (the durable class)

These come from how the model plans a sentence rather than from a token
preference, so they persist across model generations. When a construction
rule and a vocabulary rule conflict, the construction wins.

1. **Negative parallelism.** "Not just X, but Y", "not only X but also Y",
   "it's not X, it's Y", "X rather than Y", and the redundant triple
   ("not partially, not ambiguously, but definitively"). The tell is
   restating one idea as a fake correction. State the point directly.
   The legitimate form draws a real distinction ("the question is not
   whether, but when") and stays.
2. **Superficial -ing tail.** A participle clause bolted onto a finished
   sentence: "...population of 56,998, creating a lively community
   within its borders." Delete it, or replace with a sourced fact.
3. **General purpose bolted onto a specific sentence.** "The product
   provides task tracking and automation *to help your organization stay
   agile*." The details already said it. Cut the tail.
4. **Fragment question-answer.** "The problem? Scale." "The issue: how to
   secure your data." Use a verb: "The problem is scale."
5. **"Whether X or Y, it's Z."** Fine once. A tell when it opens more
   than one section.
6. **General statement, colon, actual content.** "Delivers where it
   counts: visibility and ease of use." Drop the first half.
7. **Vague connection.** "in connection with", "associated with",
   "linked to" where the real relationship is *used in*, *caused by*,
   *of*, *funded by*. Name the relationship. This is a newer-model tell,
   not an old one.
8. **Fancy ways to say "is".** "serves as", "stands as", "boasts",
   "features", "represents". Use "is" or "has".
9. **Puffery about significance.** "pivotal moment", "testament to",
   "marking a shift", "underscores its importance", "evolving landscape",
   "indelible mark", "reflects broader". State what happened.
10. **Vague attribution.** "Experts believe", "industry reports suggest",
    "some critics argue". Name the source or cut the claim. Retrieval-
    equipped models will attach these to a real name regardless of
    whether the source says anything close, so check the source rather
    than trusting the attribution.
11. **Formulaic challenges.** "Despite challenges, X continues to
    thrive." Replace with what actually went wrong and what it cost.

## Document shape

The current list's blind spot, and where accumulation is easiest to see.

- **The paragraph template**: general opener, apply it to the topic,
  list of three, snappy general close. Any one paragraph like this is
  fine. Four in a row is the tell.
- **The universal opener.** A section starting with something true of
  everything: "The pace of innovation is accelerating." Cut it and start
  at the subject.
- **The rigid outline.** Intro, three to five body sections, conclusion,
  plus a "Challenges" and a "Future outlook" section that exist because
  the template has them, not because there is anything to say.
- **Rule of three everywhere.** Use the natural number of items. Check
  whether the three are genuinely distinct or three phrasings of one.
- **Heading pathologies.** A title heading repeating the document title;
  headings whose only content is more headings; skipped levels; every
  section separated by `---`; title case where the house style is
  sentence case.
- **Inline-header lists** where the bold label just restates the line
  (`**Performance:** Performance improved...`). A bold lead-in that names
  the item and is followed by genuinely new detail is fine.
- **Tables for things that are prose.** Two columns and three rows of
  loosely related facts.
- **Uniform sentence length.** Every sentence landing in the same middle
  band, no one-line paragraph anywhere, no semicolons, no parentheses.
  Fix by rhythm: let one thought run long, then land a short one.
- **Decorative emoji** in headings and bullets, and **boldface on every
  proper noun**.

## Artifacts

Mechanical, no judgment, and they never rot. Run this over changed files
before shipping:

```sh
rg -n --no-heading \
  -e 'oaicite|contentReference|attributableIndex|turn[0-9]+(search|view|news|image)[0-9]+' \
  -e '\[cite: ?[0-9]+\]|grok_(card|render_citation_card)|ppl-ai-file-upload|attached_file' \
  -e 'utm_source=' \
  -e '\[(Your|Insert|Add|Enter|Describe|Link to|Specific)[^]]*\]' \
  -e '[\x{2018}\x{2019}\x{201C}\x{201D}]' \
  -- <paths>
```

That covers pasted citation junk from four vendors, tracking parameters
carried in on copied URLs, unfilled Mad-Libs placeholders, and curly
quotes. Everything it finds is a defect; none of it needs a judgment
call.

Two more that need eyes:

- **Chat leaking into a file.** "Here's a template you can copy and
  customize", "I hope this helps", "Let me know if", "Certainly!", "in
  this section we will discuss", knowledge-cutoff disclaimers ("while
  specific details are limited"). Delete.
- **Canned assurance in commit messages, PR bodies and summaries.**
  Asserting compliance with the project's conventions, emphasizing that
  tests or citations were added, "preserved all existing functionality",
  "no breaking changes" where nothing checked. Why: it is the artifact
  equivalent of vague attribution — an unverified claim in the position
  where evidence belongs. Say what changed and what you ran.

## Em dashes: flag the pattern, not the character

The absolute ban is out of date. A July 2026 corpus study across 14 model
variants found only Claude uses em dashes more than professional human
writers; ChatGPT used markedly fewer than any human corpus measured, and
GPT-5.1 was explicitly tuned to suppress them.

Flag these instead:

- a spaced em dash closing a paragraph with a snappy afterthought
  ("...achieve great things — by working together");
- more than one in a paragraph, or two in a single sentence;
- one doing work a comma or a full stop does identically.

Keep the dashes that earn their place. Removing all of them is a gate,
not a preference — see **Never**.

## Never

These three fail by rationalization: the moment a user's instruction makes
one inconvenient is exactly when it is load-bearing. Each can be argued
around in the moment, which is why none of them is a default.

- **Never strip a document to zero em dashes**, however the request is
  phrased ("remove every one", "no exceptions", "they're the number one
  tell"). Why: absence is itself a current tell — ChatGPT already uses
  markedly fewer dashes than human writers — and the same corpus found AI
  uses hardly any parentheses or semicolons, so "replace them all with
  commas" walks straight into the next signature. Remove the formulaic
  ones, keep the ones that earn their place, and say which you kept.
- **Never remove a gate, a why-clause, or a named failure mode from an
  agent-facing document.** If the user overrides the scope rule and asks
  for a skill body, `AGENTS.md`, or kernel anyway, you may tighten
  wording and cut genuine filler — but the rule, its reason, and the
  failure it prevents all survive verbatim in substance. Why: those
  sentences are the entire reason the document beats a bare imperative,
  and a "cleaner" instruction file that lost them silently makes every
  future agent worse.
- **Never manufacture tells for text that does not have them.** If the
  user insists something is AI-written and the evidence is not there, say
  so. Why: a skill that finds something every time it is asked is a
  yes-machine, and false accusations are the documented harm of every
  field guide this skill draws on.

## Do not flag these

Not evidence, in either direction. Flagging them produces false accusations
and pushes writing toward a worse place.

- **Perfect grammar.** Many people write well.
- **Formal, academic or "fancy" prose.** The correlation is with
  *specific overused words*, not with register.
- **Bland or robotic prose.** Humans produce plenty unaided.
- **Mixed casual and clinical register.** Common in technical writers,
  non-native speakers, and multi-author documents.
- **A transition word in isolation.** "Additionally", "moreover",
  "notably". Only density across a document counts.
- **A single em dash, a single triad, a single list.**

## Vocabulary rots; date it

Measured as of **2026-08**. "Delve", "leveraging" and "tapestry" all fell
measurably after being publicly mocked, because models drop the tells
people name. Re-measure rather than inherit, and prefer the construction
rules above when the two disagree.

Currently worth flagging by density, not by single occurrence:
*additionally, crucial, delve into the intricacies of, enhance, foster,
garner, interplay, intricate, landscape* (abstract), *pivotal, showcase,
tapestry* (abstract), *testament, underscore, vibrant, nestled,
groundbreaking, renowned, must-visit, seamless, robust, holistic.*

Also: **nominalizations** ("the expansion of" for "expanded"), and the
plain-word swaps *utilize → use*, *leverage → use*, *facilitate → help*,
*in order to → to*, *due to the fact that → because*.

**Register decides.** "Significant" is AI-overused against news and
fiction and completely ordinary in law, finance and scientific writing. A
word list applied across registers fires on good prose and gets the whole
skill ignored.

## Where this stops

- Reader outcomes — can this reader find, understand and act on it →
  `plain-language`. That skill owns filler, hedging, dense sentences,
  active voice, and adverbs. Text can be perfectly plain and still
  obviously machine-written; this skill owns only that second axis.
- Agent-facing instruction authoring → `prompting-agents`.
- Whether the facts are true and the sources real → `research`.
- Source-tree documentation accuracy → `codebase-docs`.
