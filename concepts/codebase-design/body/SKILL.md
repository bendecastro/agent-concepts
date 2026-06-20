---
name: codebase-design
description: Shared vocabulary for designing deep modules. Use when designing or improving a module's interface, finding deepening opportunities, deciding where a seam goes, making code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.
---

# Codebase Design

## Glossary

Use these terms exactly — don't substitute "component," "service," "API," or "boundary." Consistent language is the whole point.

- **Module** — anything with an interface and an implementation. Deliberately scale-agnostic: a function, class, package, or tier-spanning slice. *Avoid:* unit, component, service.
- **Interface** — everything a caller must know to use the module correctly: the type signature, but also invariants, ordering constraints, error modes, required configuration, and performance characteristics. *Avoid:* API, signature (too narrow — they refer only to the type-level surface).
- **Implementation** — what's inside a module, its body of code. Distinct from **Adapter**.
- **Depth** — leverage at the interface: how much behaviour a caller (or test) can exercise per unit of interface they have to learn. **Deep** = a lot of behaviour behind a small interface; **shallow** = the interface is nearly as complex as the implementation.
- **Seam** *(Michael Feathers)* — a place where you can alter behaviour without editing in that place; the *location* at which a module's interface lives. Where to put the seam is its own design decision, distinct from what goes behind it. *Avoid:* boundary (overloaded with DDD's bounded context).
- **Adapter** — a concrete thing that satisfies an interface at a seam. Describes *role* (what slot it fills), not substance (what's inside).
- **Leverage** — what callers get from depth: more capability per unit of interface learned. **Locality** — what maintainers get from depth: change, bugs, and verification concentrate in one place.

## Deep vs shallow

A **deep module** = small interface + lots of implementation. A **shallow module** = large interface + thin implementation (avoid — it's nearly a pass-through). When designing an interface, ask: Can I reduce the number of methods? Simplify the parameters? Hide more complexity inside?

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can be internally composed of small, mockable, swappable parts — they just aren't part of the interface. A module can have **internal seams** (private, used by its own tests) as well as the **external seam** at its interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape.
- **One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce a seam unless something actually varies across it.

## Designing for testability

Good interfaces make testing natural:
1. **Accept dependencies, don't create them** — `processOrder(order, paymentGateway)`, not a function that `new`s a `StripeGateway()` inside.
2. **Return results, don't produce side effects** — `calculateDiscount(cart): Discount`, not `applyDiscount(cart): void` that mutates `cart.total`.
3. **Small surface area** — fewer methods = fewer tests; fewer params = simpler setup.

## Rejected framings

- **Depth as ratio of implementation-lines to interface-lines** (Ousterhout): rewards padding the implementation. Use depth-as-leverage instead.
- **"Interface" as the TypeScript `interface` keyword or a class's public methods**: too narrow — interface here includes every fact a caller must know.
- **"Boundary"**: overloaded with DDD's bounded context. Say **seam** or **interface**.
