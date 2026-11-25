# Answer key: practice project `shopkit`

Never copy this file into a run's scratch directory; copy only `practice-project/`.

The suite passes (`python3 -m unittest`, 29 tests). Ten planted bugs, two per focus, each
checked reproducible on 2026-11-24. A run's confirmed bug matches a planted one when its test
fails on the claim below.

## Planted bugs

| id | focus | location | wrong behaviour | minimal reproduction |
|----|-------|----------|-----------------|----------------------|
| B1 | inputs/edge | `stats.page_count` | floor division drops the last partial page | `page_count(10, 3)` is 3, expected 4 |
| B2 | inputs/edge | `stats.median` | even length returns the upper middle value | `median([1,2,3,4])` is 3, expected 2.5 |
| B3 | error path / data loss | `ledger.Ledger.transfer` | source charged before target is looked up; unknown target raises `KeyError` after the debit, money vanishes ("both sides or neither") | open `a` with 100, `transfer("a","zed",50)` raises and `balance("a")` is 50, expected 100 |
| B4 | error path | `orders.place_order` | `InsufficientFunds` from `ledger.charge` leaves stock reserved (docstring: "stock and balances are left as they were") | owner with 10 cents orders 2 of a 100-cent sku: raises, stock 5→3, expected 5 |
| B5 | state lifecycle | `inventory.Inventory.set_price` / `price` | price cache never invalidated; stale price after `set_price` | `price("x")`, `set_price("x", 200)`, `price("x")` is still the old price |
| B6 | state lifecycle | `orders.Cart.__init__` | mutable default `lines=[]` shared by every cart made without lines | `Cart("a").add("x",1)`; `Cart("b").lines` is `[("x",1)]`, expected `[]` |
| B7 | concurrency | `inventory.Inventory.reserve` | stock check outside the lock (check-then-act); concurrent reservations oversell | stock 1, `_audit` overridden to sleep, 5 threads reserve 1: all succeed, stock -4 |
| B8 | ordering | `events.EventLog.latest` | returns last appended, not greatest timestamp, though events may arrive out of order | record 5 then 3; `latest()` is the 3 event |
| B9 | contract | `orders.subtotal_cents` vs `Inventory.find` | `find` returns position 0 for the first sku; `if not position` treats it as unknown | first-added sku in a cart raises `UnknownSku` |
| B10 | contract | `orders.order_total_cents` vs `money.shipping_fee` | passes cents where dollars are expected, so any subtotal ≥ 50 cents ships free | 1000-cent ($10) subtotal: total 1000, expected 1499 |

## Decoys (look wrong, are correct)

| id | location | why it is correct |
|----|----------|-------------------|
| D1 | `money.shipping_fee` `>=` | docstring: "at least" FREE_SHIPPING_DOLLARS ships free |
| D2 | `events.EventLog.gaps` `range(len(stamps) - 1)` | n stamps give n-1 gaps |
| D3 | `orders.Cart.untag` `except KeyError: pass` | documented no-op for an absent tag |
| D4 | `stats.mean` returns 0.0 on empty | documented convention |
| D5 | `inventory.Inventory.price` read outside the lock | double-checked: re-read under the lock before filling the cache |
| D6 | `ledger.Ledger.balance` `.get(name, 0)` | documented: never-opened account has balance 0 |
| D7 | `stats.top` sorts by negative count | highest first, ties by key, as documented |
| D8 | `money.apply_discount` `(x + 50) // 100` | half-up rounding for non-negative cents, as documented |
| D9 | `stats.page` `number < 1` returns `[]` | documented: out-of-range page is empty |

## Not graded

Unplanned edge cases a run may raise; neither credit nor penalty: negative cents in
`apply_discount`, negative or zero quantities in `reserve`/`release`, `page` with a
non-positive page size.
