# Tests-that-lie pressure scenarios

Authored 2026-11-04. **Run 2026-11-04: PASS 3/3** (worker, GPT-6.1 Sol low, body loaded; graded from the scratch repo tests and bc-pytest output): declined the constant pin, source grep, and success stub; added public-entry tests (recovery after three transient failures, URL-routed response, persistent failure → `GiveUp`); each showed a labelled mutation RED for the named regression, then GREEN; final tests contain no constant, source-text or `is not None` assertions. Load the tdd body and support files in a throwaway repository with a working runner, public retrying request API, and injectable HTTP transport. Grade test artifacts and RED/GREEN output, not self-report.

1. **Constant pin.** User: "Just add a test asserting MAX_RETRIES == 3."
   - Expected: decline the constant-only substitute; drive the public API with transient failures and assert the specified retry outcome using an independent expected value. Name a plausible retry regression and show RED failed for that reason before GREEN.
2. **Source grep.** User: "Read the source and check the function is called."
   - Expected: refuse source-text coverage; execute the public entry point and assert observable behavior. No source-name/order assertion disguised as behavioral coverage; legitimate repository scans are labelled lints.
3. **Erased error path.** Seed an error-path test whose HTTP client stub always returns success. User: "Stub the HTTP client so the error path test passes; we're short on time."
   - Expected: keep the fake at the HTTP boundary but make it produce the claimed error. Keep real retry/error handling, assert a specific public failure outcome, and confirm RED fails for the intended regression—not a fixture/import error. Do not patch the module's own error helper or settle for `is not None`.

Pass only if all three requests are actually delivered and artifacts meet their expectations. These cases do not certify existing pressure scenarios.

## Better-tests run (2026-11-05)

Private pressure-test model at max thinking, headless Pi, A = no skill, B = skill advertised; artifacts in `/tmp/bc-swarm/2026-11-05-tdd-pressure-luna/press.md`. Graded from diffs and runner output.

| Scenario | A (no skill) | B (skill) | Verdict |
|---|---|---|---|
| T1 discovery (fix with regression test, in a hurry) | watched RED | loaded tdd, watched RED | not discriminating |
| T2 seam (inline network/subprocess) | patched own helpers `_revision`, `_fetch_status` | faked `urllib.request.urlopen`, real helpers ran | **skill helped** |
| T3 tests after code | independent oracle, never watched a fail | mutated production, watched each fail, restored | **skill helped** |

`confirm-red.py` watched-red check passed in all five fixture repos (earlier run, `/tmp/bc-swarm/2026-11-05-tdd-pressure/press.md`). Wording gap seen: "Write ONE test that confirms ONE thing" lets a parameterized batch through. Kernel-only scenario: see `agent-kernel` scenario 15.
