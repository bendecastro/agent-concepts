# 0005: The agent kernel holds only rules for everyone

Date: 2026-11-26
Status: accepted

## Context

Setup is going to offer strangers the agent kernel (work item `030-ship-machine-only-rules`). The kernel grew on the owner's machine and mixes rules any agent user benefits from with the owner's own tastes and tools.

## Decision

The kernel holds only rules that make sense for anyone. The owner's personal rules live in their private preferences, outside this repository; a generic rule whose specifics are personal stays generic in the kernel, with the specifics in the private layer. Work item `034-kernel-for-everyone` audits the current kernel before setup starts offering it.

## Consequences

- Each kernel rule needs a reason that holds for a stranger.
- The owner's setup loads two layers: the kernel and their private preferences.

## Alternatives considered

- Offer the kernel as it is: pushes the owner's preferences onto every stranger.
- Ship two kernels (minimal and full): two copies drift.
