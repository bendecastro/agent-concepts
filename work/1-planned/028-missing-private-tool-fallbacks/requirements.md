# Requirements: fallbacks when a machine-only tool is missing

## Problem Statement

The skills were written on one machine that supplies a publish-policy checker, a guarded pytest runner, a storage health check and configured Pi worker roles. A stranger has none. `bc-pipeline-to-done` preflight says "A denial, or no check, aborts unless the user pre-agreed to commit-only-local mode", and the bundled `scripts/publish-check.py` sits outside every skill body, so plugin and package installs never receive it.

## Solution

1. **Publish check ships with the pipeline.** The checker becomes part of `bc-pipeline-to-done`'s body (moved there, with `scripts/publish-check.py` kept as a thin entry point so existing callers keep working). Preflight runs the overlay-named checker when one exists, else the bundled one.
2. **No policy file, owner present:** preflight asks once, "May this run push to <remote> <target branch>?" A yes is current user authorization for this run only and is recorded in the run manifest; it never writes or edits the policy file. No policy file and owner away: commit locally only, as today (deny by default).
3. **Other machine tools:** every "the machine's ... if one exists" reference in deployed bodies states its fallback: plain `pytest` with `tmp_path` and the temp-file rules when no guarded runner exists; skip the storage check with one report line when none exists; a clear stop naming what to configure when a required capability (Pi subagents and the pipeline's worker roles) is missing.
4. **README install prerequisites** list what the pipeline needs (pi-subagents, its worker roles from the examples folder, `gh` for issue sources) and the optional machine tools with their fallbacks.

## User Stories

1. As a stranger, I can start `/bc-pipeline-to-done` without a publish policy and decide pushing for this run.
2. As a stranger away from the keyboard, my unattended run commits locally and never pushes without a policy.
3. As a stranger, each instruction that names a machine tool tells me what happens when I do not have it.
4. As a stranger, the README tells me what to install before using the pipeline.

## Implementation Decisions

- Deny by default is unchanged; the per-run answer is never persisted as policy (self-amendment immunity unchanged).
- The inventory of references is made by grep over `concepts/*/body/` for "machine's", "if one exists", "overlay names" and the private tool names in the optional personal-terms list; each hit is classified has-fallback / needs-fallback / needs-stop.

## Testing Decisions

- The bundled checker keeps the existing `scripts/tests/` coverage, run against the moved code.
- Pressure scenario (pressure-test model, blind baseline) with no policy file: owner present (agent asks once and records the answer) and owner away (agent commits only, does not push).

## Out of Scope

- Writing or editing anyone's publish policy; shipping a storage health tool or guarded runner.
