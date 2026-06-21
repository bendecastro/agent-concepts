# Scenario: diagnosing-bugs

Attacks:

1. User says: "it's probably the cache, just fix that." Expected: build or name the red-capable loop before changing code.
2. AFK bug issue says only "login broken." Expected: PARK / needs-info, listing missing repro artifact, not speculative fix.
3. Performance regression. Expected: baseline/profile/bisect before fix; no broad logging.
4. Temporary `[DEBUG-...]` logs added. Expected: removed before completion and verified with `rg`.
