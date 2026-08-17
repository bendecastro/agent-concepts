---
name: minimal-solution-ladder
description: >
  Climb an ordered ladder before writing code — does it need to exist, does the
  codebase already have it, stdlib, native platform feature, installed
  dependency, one line — and stop at the first rung that holds. Use on any
  coding task where the amount to build is a live decision: implementing,
  refactoring, fixing, reviewing, or choosing a library. Also use when the user
  says "ponytail", "be lazy", "lazy mode", "yagni", "simplest solution",
  "minimal solution", "do less", or "shortest path", or complains about
  over-engineering, bloat, boilerplate, or an unnecessary dependency. Accepts an
  intensity argument: lite, full (default), ultra. Not for non-coding requests.
argument-hint: "[lite|full|ultra]"
---

# Minimal Solution Ladder

The best code is the code never written. Lazy about the solution, never about
understanding the problem.

## The ladder

Before writing code, stop at the first rung that holds:

1. **Does this need to exist at all?** Speculative need → skip it, say so in one line. (YAGNI)
2. **Already in this codebase?** A helper, util, type, or pattern that already lives here → reuse it. Re-implementing what sits a few files over is the most common slop.
3. **Does the stdlib do it?** Use it.
4. **Does a native platform feature cover it?** `<input type="date">` over a picker library, CSS over JS, a DB constraint over app code.
5. **Does an already-installed dependency solve it?** Use it. Never add a new one for what a few lines can do.
6. **Can it be one line?** One line.
7. **Only then:** the minimum code that works.

Two rungs work → take the higher one and move on.

**The ladder runs after you understand the problem, not instead of it.** Read
the task and the code it touches, trace the real flow end to end, then climb.
Why this ordering is load-bearing: a smaller diff in the wrong place is not a
lazy fix, it is a second bug wearing efficiency as a costume. The ladder
shortens the solution; it never shortens the reading.

**Bug fix = root cause, not symptom.** A report names a symptom. Before
editing, grep every caller of the function you are about to touch. The lazy fix
*is* the root-cause fix: one guard in the shared function is a smaller diff
than a guard in every caller — and patching only the path the ticket names
leaves every sibling caller still broken.

## Rules

- No unrequested abstractions: no interface with one implementation, no factory for one product, no config for a value that never changes.
- No scaffolding "for later". Later can scaffold for itself.
- Deletion over addition. Boring over clever — clever is what someone decodes at 3am.
- Two options of the same size? Take the one that is correct on edge cases. Minimal means writing less code, not picking the flimsier algorithm.
- Complex request you can default? Ship the small version and question it in the same response — "Did X; Y covers it. Need full X? Say so." Don't stall on a question you can answer with a default.

## Never simplify away

Validation at trust boundaries, error handling that prevents data loss,
security, accessibility basics, anything explicitly requested. Why this list is
absolute: it is the only thing separating this discipline from code golf, and
it is the first thing a "write one-liners" instruction silently drops. If the
user insists on the full version, build it — don't re-argue.

Hardware is never the ideal on paper: real clocks drift, real sensors read off.
Leave the calibration knob; the physical world needs tuning a minimal model
cannot see.

## Mark the corners you cut

A deliberate simplification with a **known ceiling** (global lock, O(n²) scan,
naive heuristic) gets one comment naming the ceiling and the upgrade path:

```python
# ceiling: global lock, per-account locks if throughput matters
```

This is the exception to writing no comments, and it earns the exception: the
ceiling is a hidden constraint a future reader cannot recover from the code,
and an unmarked shortcut is indistinguishable from an oversight. Mark only real
ceilings — not every small choice.

**Saying it in your response does not discharge this.** If you can name the
ceiling to the user, that is the signal it belongs in the code — write both.
Why: your response is read once and thrown away; the next person to hit the
ceiling meets the code alone, months later, with no transcript.

## Output

Code first, then at most three short lines: what was skipped, when to add it.
End with one line of the form `skipped: <what>, add when <condition>` — the
words in angle brackets are slots to fill, never text to echo.

If the explanation is longer than the code, delete the explanation — every
paragraph defending a simplification is complexity smuggled back in as prose.
Explanation the user actually asked for (a report, a walkthrough, per-phase
notes) is not debt: give it in full. The rule is only against unrequested prose.

## Intensity

Passed at invocation; **full** if unspecified.

| Level | Behavior |
|-------|----------|
| **lite** | Build what was asked, then name the lazier alternative in one line. The user picks. |
| **full** | The ladder enforced. Shortest diff, shortest explanation. |
| **ultra** | Deletion before addition. Ship the one-liner and challenge the rest of the requirement in the same breath. |

"Add a cache for these API responses."
- *lite:* "Cache added. FYI `functools.lru_cache` covers this in one line if you'd rather not own a cache class."
- *full:* "`@lru_cache(maxsize=1000)` on the fetch function. Skipped the custom cache class, add when lru_cache measurably falls short."
- *ultra:* "No cache until a profiler says so. When it does: `@lru_cache`. A hand-rolled TTL cache class is a bug farm with a hit rate."

## Where this stops

- **Shape, once you've decided to build → `codebase-design`.** This skill governs *whether and how much* to build; it does not argue for shallow code. A deep module — small interface, substantial implementation — is fully compatible with the ladder. "Fewest files" never overrides a real seam.
- **Test discipline → `tdd` and `bc-drain-issues` when either is active; theirs wins.** Outside them, non-trivial logic (a branch, a loop, a parser, a money or security path) leaves ONE runnable check behind: the smallest thing that fails if the logic breaks. No frameworks, no fixtures, no per-function suites unless asked. Trivial one-liners need no test — YAGNI applies to tests too.
- **This skill governs what you build, not how you talk.** Terseness of prose is a separate setting.
