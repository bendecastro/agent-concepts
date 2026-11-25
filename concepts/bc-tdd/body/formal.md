# Level 3 — formal verification

Load this when a change touches a component in a risk class, a component whose project `validation.md` has a `Level 3: on` line, or a spec/proof file. Level 3 means a full machine-checked proof that a stated rule holds for every input, not more testing.

## Tools

Full proof only. Bounded checkers and symbolic test generators (Kani, CrossHair) are not Level 3: they find bugs but leave the rule unproven.

| Code | Tool | Why |
|------|------|-----|
| Python, JS/TS | [Dafny](https://dafny.org/) — prove in Dafny, compile to Python/JS | Neither language has a mature full-proof verifier; Dafny proves the rule and generates the code that runs. |
| Rust | [Verus](https://github.com/verus-lang/verus) | Proves the Rust code itself, so nothing is generated and nothing drifts. |
| Designs: protocols, concurrency, sync | [TLA+](https://lamport.azurewebsites.net/tla/tla.html) with TLC | Design bugs live in interleavings no test schedules; TLC explores every state of a model. Bounded models are allowed here, for designs only. |
| A design rule that must hold in every state for the fixed sizes | [Apalache](https://apalache-mc.org/) inductive invariant, alongside TLC | An inductive invariant is a proof for those sizes, not a search that stops at a depth. |
| Shell | none | Move the rule-bearing logic into a language above. |

## Turning it on

Only the owner turns Level 3 on, per component, by adding a line to the project's `.bc-agent/conventions/validation.md`:

```
Level 3: on — <component path> — <tool> <pinned version> — spec: <spec file> — command: <proof command>
```

You never add, edit or remove this line. Why: a proof costs real effort for the life of the component, and only the owner decides that cost is worth paying.

## Suggesting it

A component is in a **risk class** when it holds one of:

- persisted data that could be lost or corrupted;
- money;
- security or permissions;
- concurrency or sync;
- a core calculation many parts depend on.

Whenever your change touches a component in a risk class, and `validation.md` has neither a `Level 3: on` nor a `Level 3 declined` line for it, add this line to your report:

```
Level 3 candidate: <component> — <risk> — <tool> — <rough effort>
```

Suggest it even when nobody asked, under deadline, and when the owner said to just ship. Suggesting changes nothing in the code and blocks nothing; staying silent hides a choice that belongs to the owner.

When the owner refuses, record it in `validation.md` (writing a refusal the owner gave is allowed; turning Level 3 on is not):

```
Level 3 declined: <component>, <YYYY-MM-DD>, <reason>
```

Do not suggest that component again unless its risk class changes (for example a cache starts persisting user data). Report `L3: declined on <date>` instead.

## Spec file

Before any proof, write a spec file at the path the `Level 3: on` line will name. It holds:

1. **Rules.** Each rule is one plain-English line paired with its formal statement (Dafny `ensures`/lemma, Verus `ensures`/proof fn, TLA+ invariant or property).
2. **Assumptions.** An explicit list of everything taken on trust: every `assume`, axiom, `{:axiom}`, Verus `external_body`/`assume`/`admit`, `{:verify false}`, TLA+ constraint that excludes states, model sizes, and the behavior of unproven code the proof calls.

The owner approves the plain-English rules and the assumptions list. An independent reviewer (`bc-code-review` Spec axis) checks that each formal rule says what its English line says, and that every escape hatch in the proof appears in the approved assumptions.

## Running proofs

Run the recorded `command:` on every change that touches a Level 3 component, and once more in final validation before landing. Use the tool version pinned in the `Level 3: on` line.

If the tool is missing or the proof times out, the result is **untested**, never passed. An untested proof blocks landing changes to that component; changes that do not touch it are unaffected.

## Dafny-generated code

- Commit both the Dafny source and the generated Python/JS; mark each generated file do-not-edit in a header comment.
- Validation regenerates from the current source and fails if the committed output differs.
- Put Level 2 property tests at the boundary where hand-written code calls the generated module.
- Never hand-edit a generated file: change the Dafny source and regenerate.

## Trust boundaries

A proof covers only what it states, under its assumptions. It does not cover: the hand-written code around the proven module (Level 1–2 tests cover it), the Dafny compiler and target runtime, the TLA+ model's fidelity to the real implementation, sizes beyond the fixed model sizes, or anything listed as an assumption. Say which of these a report relies on rather than calling the component "proven correct".
