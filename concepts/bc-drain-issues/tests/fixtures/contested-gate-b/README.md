# Contested Gate B fixture

Gate B is the model-token A/B that decides whether a drain revision actually costs less.
v2's Gate B used a *clean* fixture: one worker, one rework, no re-review. v3's main levers —
selective re-review and narrowed rework — never engage on such a run, so v3 needs a fixture that
is **contested**: one that plausibly produces material review findings across more than one round.

`make-fixture.py` builds that fixture. Run it once per arm so both arms start byte-identical.

```sh
python3 make-fixture.py            # prints the sandbox root
. <root>/env.sh                    # PATH-first stubs, XDG state, worktree root
```

## What the fixture is

`bc-svc`, a service-control CLI being moved under a `service` subcommand group (issue #102),
shaped after issue #29 — the run that cost ~1.89M child tokens and motivated v2.

| Element | Where it lives | Why |
|---|---|---|
| Old public interface incl. `reload` and `apply-change` | `bc-svc`, `--help`, `tests/test_old_interface.sh` | The Agent Brief's new-command list **omits both**. Recoverable only by inventorying source/help/tests — exactly the audit v2 added. |
| Argument-boundary weakness | `lib/quote.sh` | Latent at base; surfaces once a dispatch layer is added. Mapped to **no** acceptance row, so fixing it is the natural Standards-only rework — the case that exercises selective re-review. |
| Contradictory platform prose | `docs/README.md` vs `primary-docs/systemd.service.5.txt` | README claims restart-on-clean-exit; the primary doc says `Restart=on-failure` excludes exit 0. Repository prose must lose. |
| Known baseline failure | `tests/test_known_flaky.sh` | Must fail at base and still fail at landing. Separates known failures from regressions. |
| Dependency ordering | #103 depends on #102 | #103 must be skipped while #102 is in flight; parent #101 closes only when both children complete. |

`FIXTURE.json` records the base SHA, paths, and the seeded defect list.

## Isolation

`env.sh` puts `stubs/` first on `PATH`. The `git` stub intercepts **only** `push`: claim refs get
real create-once/reject-twice semantics via a lockfile, `HEAD:master` is accepted and discarded,
anything else is refused. `gh` is a full stub over a JSON issue store — list/view/comment/close/
edit-labels all work and mutate nothing real. `publish-check.py` returns 0.

**Residual risk, stated plainly:** the sandbox does not sever general network access, and the
stubs only bind while `env.sh` is sourced and `PATH` is respected. The fixture repo's `origin` is
a local bare path, so even a stub bypass would push to a disposable remote — but the runner must
still verify `commands.log` shows every `push`/`gh`/`publish-check` attempt resolving to
`stubs/`, and must confirm no real repository was touched. Do not run an arm in a shell that has
credentials for a real remote on `PATH` ahead of the stubs.

## Arms

Both arms run the identical fixture, model, and effort; only the canon differs.

- **v2 arm** — canon at commit `745fe01` (pre-v3). Retrieve with
  `git worktree add --detach <dir> 745fe01`, then point the drain at
  `<dir>/agents/concepts/bc-drain-issues/body/`.
- **v3 arm** — current canon at `agents/concepts/bc-drain-issues/body/`.

Verify the arms differ before spending tokens: the v2 `review-contract.md` contains no
`do not re-derive it`; the v3 one does.

## Pass criteria

Inherit every v2 Gate B outcome in `../../pressure-drain.md`, plus:

- the run is genuinely contested — at least two rework rounds occurred, otherwise the fixture
  failed to do its job and the comparison says nothing about v3's main levers;
- an axis holding a standing approval was not re-dispatched when its trigger did not fire;
- every landed diff carries a standing approval from **both** axes bound to its exact hash;
- total v3 child tokens are lower than v2's on this fixture;
- both hidden commands (`reload`, `apply-change`) are preserved;
- restart-policy claims cite `primary-docs/`, not `docs/README.md`;
- `tests/test_known_flaky.sh` still fails at landing and nothing else regressed.

Record the result in `../../results/` following the shape of `2026-07-25-gate-b.md`, and update
`../../pressure-drain.md` plus `../../../CONCEPT.md` with the measured numbers.

If v3 is **not** cheaper, that is a real result and must be recorded as such — the levers were
reasoned from one clean measurement, and a contested run is exactly the evidence that could
overturn them.
