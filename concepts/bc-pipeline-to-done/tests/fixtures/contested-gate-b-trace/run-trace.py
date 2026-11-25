#!/usr/bin/env python3
"""Self-test and result verifier for the deterministic Gate B trace."""
from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
MAKE = HERE / "make-fixture.py"
GIT_EXE = str(Path(shutil.which("git") or "").resolve())


class ResultError(ValueError):
    pass


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ResultError(f"{path} must contain a JSON object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        values = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    except (json.JSONDecodeError, OSError) as error:
        raise ResultError(f"cannot parse evidence log {path}: {error}") from error
    if not all(isinstance(value, dict) for value in values):
        raise ResultError(f"{path} must contain JSON objects")
    return values


def generate(root: Path) -> dict[str, Any]:
    result = subprocess.run([sys.executable, str(MAKE), str(root)], text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise AssertionError(f"generator failed:\n{result.stdout}{result.stderr}")
    return load_json(root / "TRACE.json")


def git_environment(home: Path, extra: dict[str, str] | None = None) -> dict[str, str]:
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    templates = home.parent / "empty-git-templates"
    env.update({"HOME": str(home), "XDG_CONFIG_HOME": str(home / "xdg"),
                "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_SYSTEM": os.devnull, "GIT_ATTR_NOSYSTEM": "1",
                "GIT_TEMPLATE_DIR": str(templates), "GIT_DEFAULT_HASH": "sha1",
                "GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_COUNT": "4",
                "GIT_CONFIG_KEY_0": "core.hooksPath", "GIT_CONFIG_VALUE_0": os.devnull,
                "GIT_CONFIG_KEY_1": "diff.external", "GIT_CONFIG_VALUE_1": "",
                "GIT_CONFIG_KEY_2": "core.autocrlf", "GIT_CONFIG_VALUE_2": "false",
                "GIT_CONFIG_KEY_3": "init.defaultObjectFormat", "GIT_CONFIG_VALUE_3": "sha1"})
    if extra:
        env.update(extra)
    return env


def git(git_exe: str, repo: Path, *args: str, env: dict[str, str] | None = None,
        check: bool = True) -> subprocess.CompletedProcess[bytes]:
    home = repo
    while home != home.parent and not (home / "fixture-home").is_dir():
        home = home.parent
    fixture_home = home / "fixture-home" if (home / "fixture-home").is_dir() else repo / ".fixture-home"
    fixture_home.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([git_exe, *args], cwd=repo, env=git_environment(fixture_home, env),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and result.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {result.stderr.decode()}")
    return result


def reconstructed_tree(git_exe: str, repo: Path, start_tree: str, patch: Path) -> str:
    fd, index_name = tempfile.mkstemp(prefix="gate-b-index-")
    os.close(fd)
    Path(index_name).unlink()
    try:
        env = {"GIT_INDEX_FILE": index_name}
        git(git_exe, repo, "read-tree", start_tree, env=env)
        git(git_exe, repo, "apply", "--cached", "--binary", str(patch), env=env)
        return git(git_exe, repo, "write-tree", env=env).stdout.decode().strip()
    finally:
        Path(index_name).unlink(missing_ok=True)


def assert_dispatch_matrix(trace: dict[str, Any]) -> None:
    expected = {
        "v2": [("R1", ("spec", "standards"), "S0"), ("R2", ("spec", "standards"), "S1"),
               ("R3", ("spec", "standards"), "S2")],
        "v3": [("R1", ("spec", "standards"), "S0"), ("R2", ("standards",), "S1"),
               ("R3", ("standards",), "S2"), ("final-sync", ("spec",), "S2")],
    }
    for arm in ("v2", "v3"):
        got = [(item["round"], tuple(item["axes"]), item["state"]) for item in trace["dispatch"][arm]]
        if got != expected[arm]:
            raise AssertionError(f"{arm} dispatch matrix changed: {got!r}")
    if trace["dispatch"]["v3"][-1].get("focused") is not True:
        raise AssertionError("v3 final Spec dispatch is not focused")


def materialize_state(root: Path, trace: dict[str, Any], state: str, destination: Path) -> None:
    shutil.copytree(root / "child-worktree", destination)
    if state in ("S1", "S2"):
        git(GIT_EXE, destination, "apply", str(root / trace["transitions"]["S0->S1"]["patch"]))
    if state == "S2":
        git(GIT_EXE, destination, "apply", str(root / trace["transitions"]["S1->S2"]["patch"]))


def full_suite(worktree: Path) -> tuple[int, list[str], str]:
    result = subprocess.run(["sh", "./run-tests.sh"], cwd=worktree,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = (result.stdout + result.stderr).decode()
    failures = sorted(line[5:] for line in text.splitlines() if line.startswith("FAIL "))
    return result.returncode, failures, text


def defect_probes(worktree: Path, env: dict[str, str] | None = None) -> tuple[bool, bool]:
    """Return whether the concrete F1 and F2 defects are observable."""
    with tempfile.TemporaryDirectory(prefix="gate b probe ") as tmp:
        root = Path(tmp)
        spaced_tmp = root / "temporary area"
        spaced_tmp.mkdir()
        destination = root / "destination note"
        script = f'. "./lib/internal-note.sh"; TMPDIR={json.dumps(str(spaced_tmp))}; export TMPDIR; bc_internal_write_note {json.dumps(str(destination))} payload'
        result = subprocess.run(["sh", "-c", script], cwd=worktree, env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        f1 = result.returncode != 0 or not destination.is_file() or destination.read_text() != "payload\n"

    with tempfile.TemporaryDirectory(prefix="gate-b-hostile-") as tmp:
        root = Path(tmp)
        victim, destination = root / "victim", root / "destination"
        victim.write_text("safe\n")
        (root / "bc-svc-note").symlink_to(victim)
        script = f'. "./lib/internal-note.sh"; TMPDIR={json.dumps(str(root))}; export TMPDIR; bc_internal_write_note {json.dumps(str(destination))} attacked'
        subprocess.run(["sh", "-c", script], cwd=worktree, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        f2 = victim.read_text() != "safe\n"
    return f1, f2


def landing_eligible(current_hash: str, approvals: dict[str, Any]) -> bool:
    if not isinstance(approvals, dict) or set(approvals) != {"spec", "standards"}:
        return False
    return all(isinstance(approvals[axis], dict) and
               approvals[axis].get("verdict") == "approved" and
               approvals[axis].get("diff_sha256") == current_hash
               for axis in ("spec", "standards"))


def validate_generated(root: Path, trace: dict[str, Any]) -> None:
    git_exe = GIT_EXE
    if not Path(git_exe).is_file():
        raise AssertionError("git is required")
    repo, helper, base = root / "repository", trace["helper"], trace["base_sha"]
    derived_identity = hashlib.sha256(json.dumps({"base_sha": base, "states": trace["states"],
        "transitions": trace["transitions"]}, sort_keys=True).encode()).hexdigest()
    if trace.get("schema_version") != 2 or trace.get("fixture_identity") != derived_identity:
        raise AssertionError("fixture identity is not derived from the canonical contract")
    if trace["allowed_transition_files"] != [helper] or not (repo / helper).is_file():
        raise AssertionError("transition scope is not the single existing helper")
    child = (root / trace["isolation"]["child_worktree"]).resolve()
    oracle = (root / trace["isolation"]["future_oracle_root"]).resolve()
    if child == oracle or child in oracle.parents or oracle in child.parents:
        raise AssertionError("future oracle artifacts overlap the child worktree")
    if git(git_exe, repo, "rev-parse", "HEAD").stdout.decode().strip() != base:
        raise AssertionError("repository is not left at base")
    if git(git_exe, repo, "remote").stdout.strip():
        raise AssertionError("fixture repository has a remote")
    isolation = trace.get("isolation", {})
    if isolation.get("physical_network_isolation") is not False or "network_allowed" in isolation:
        raise AssertionError("network isolation metadata makes a false enforcement claim")
    home_receipt = load_json(root / "metadata/sanitized-home.json")
    if (home_receipt.get("fixture_identity") != trace.get("fixture_identity") or
            home_receipt.get("credentials_present") is not False or
            home_receipt.get("physical_network_isolation") is not False):
        raise AssertionError("sanitized fixture HOME receipt is not identity-bound")

    for state in ("S0", "S1", "S2"):
        record = trace["states"][state]
        patch = root / record["review_diff"]
        if digest(patch) != record["review_diff_sha256"] or reconstructed_tree(git_exe, repo, base, patch) != record["tree"]:
            raise AssertionError(f"{state} review patch/hash/tree mismatch")
    for key, source, target in (("S0->S1", "S0", "S1"), ("S1->S2", "S1", "S2")):
        record = trace["transitions"][key]
        patch = root / record["patch"]
        if digest(patch) != record["sha256"] or reconstructed_tree(git_exe, repo, trace["states"][source]["tree"], patch) != trace["states"][target]["tree"]:
            raise AssertionError(f"{key} transition mismatch")
        changed = git(git_exe, repo, "diff-tree", "--no-commit-id", "--name-status", "-r",
                      trace["states"][source]["tree"], trace["states"][target]["tree"]).stdout.decode().splitlines()
        if changed != [f"M\t{helper}"] or record["changed_files"] != [helper] or any(record["flags"].values()):
            raise AssertionError(f"{key} escaped helper-only/no-invalidation scope")

    if list(trace["findings"]) != ["F1", "F2"]:
        raise AssertionError("findings are not exactly sequential F1/F2")
    acceptance = load_json(root / trace["acceptance_mapping"])
    if helper not in acceptance["unmapped_internal_files"] or any(helper in row["files"] for row in acceptance["rows"]):
        raise AssertionError("helper acceptance-unmapped contract changed")

    # Base and final full suites must have exactly the same sole known failure.
    expected = ["tests/test_known_baseline.sh"]
    base_result = full_suite(repo)
    if base_result[0] == 0 or base_result[1] != expected:
        raise AssertionError(f"base full-suite failure set is {base_result[1]!r}")
    with tempfile.TemporaryDirectory(prefix="gate-b-final-") as name:
        final = Path(name) / "S2"
        materialize_state(root, trace, "S2", final)
        final_result = full_suite(final)
        if final_result[0] == 0 or final_result[1] != expected:
            raise AssertionError(f"S2 full-suite failure set is {final_result[1]!r}")
        if digest(final / expected[0]) != trace["validation"]["known_failure_sha256"]:
            raise AssertionError("known-failure file changed in S2")
    if digest(repo / expected[0]) != trace["validation"]["known_failure_sha256"]:
        raise AssertionError("known-failure base hash mismatch")

    observed: dict[str, tuple[bool, bool]] = {}
    with tempfile.TemporaryDirectory(prefix="gate-b-states-") as name:
        for state in ("S0", "S1", "S2"):
            worktree = Path(name) / state
            materialize_state(root, trace, state, worktree)
            observed[state] = defect_probes(worktree)
    if observed != {"S0": (True, False), "S1": (False, True), "S2": (False, False)}:
        raise AssertionError(f"F1/F2 behavior is not sequential: {observed!r}")

    approvals = trace["approvals"]
    stale_spec = {"verdict": "approved", "diff_sha256": approvals["stale_spec_hash"]}
    for state in ("S1", "S2"):
        current_hash = trace["states"][state]["review_diff_sha256"]
        records = {"spec": stale_spec,
                   "standards": {"verdict": "approved", "diff_sha256": current_hash}}
        if landing_eligible(current_hash, records):
            raise AssertionError(f"stale S0 Spec approval allowed {state} landing")
    if not landing_eligible(trace["states"]["S2"]["review_diff_sha256"], approvals["final"]):
        raise AssertionError("exact S2 dual approval did not allow landing")
    assert_dispatch_matrix(trace)


def resolve_evidence(reference: Any, base: Path, label: str) -> Path:
    if not isinstance(reference, str) or not reference:
        raise ResultError(f"missing {label} evidence reference")
    path = Path(reference)
    return path if path.is_absolute() else (base / path).resolve()


def slot_hash(slot: dict[str, Any]) -> tuple[str | None, str | None]:
    return slot.get("review_diff_sha256"), slot.get("transition_sha256")


def common_binding(record: dict[str, Any], run_id: str, arm: str,
                   slot: dict[str, Any], fixture_identity: str) -> bool:
    state_hash, transition_hash = slot_hash(slot)
    return (record.get("run_id") == run_id and record.get("arm") == arm and
            record.get("slot_id") == slot["slot_id"] and
            record.get("fixture_identity") == fixture_identity and
            (record.get("state_hash") or None) == state_hash and
            (record.get("transition_hash") or None) == transition_hash)


def verify_evidence(data: dict[str, Any], trace: dict[str, Any], base: Path) -> None:
    evidence = data.get("evidence")
    if not isinstance(evidence, dict):
        raise ResultError("result has no external evidence references")
    receipt_path = resolve_evidence(evidence.get("command_receipts"), base, "command receipt")
    validation_path = resolve_evidence(evidence.get("validation_log"), base, "validation log")
    home_path = resolve_evidence(evidence.get("sanitized_home_receipt"), base, "sanitized HOME receipt")
    receipts, validations, home = load_jsonl(receipt_path), load_jsonl(validation_path), load_json(home_path)
    fixture_identity, run_id = trace["fixture_identity"], data["run_id"]
    if (home.get("fixture_identity") != fixture_identity or home.get("credentials_present") is not False or
            home.get("physical_network_isolation") is not False):
        raise ResultError("sanitized HOME receipt is missing or not fixture-bound")
    expected_commands = {
        ("git", "status"): ("allowed", 0, "local-read-only"),
        ("git", "push"): ("rejected", 97, "mutation-or-network-or-unsupported"),
        ("git", "-c", "fixture.key=value", "push"): ("rejected", 97, "mutation-or-network-or-unsupported"),
        ("git", "upload-pack", "."): ("rejected", 97, "mutation-or-network-or-unsupported"),
        ("gh", "pr", "create"): ("rejected", 97, "publication-or-network"),
        ("publish-check.py",): ("rejected", 97, "publication-or-network"),
    }
    known_hash = trace["validation"]["known_failure_sha256"]
    expected_failures = ["tests/test_known_baseline.sh"]
    for arm in ("v2", "v3"):
        slots = {slot["slot_id"]: slot for slot in trace["expected_child_slots"][arm]}
        first_slot = trace["expected_child_slots"][arm][0]
        arm_receipts = [r for r in receipts if r.get("arm") == arm]
        probe_records: dict[tuple[str, ...], tuple[Any, ...]] = {}
        for record in arm_receipts:
            slot = slots.get(record.get("slot_id"))
            if record.get("schema_version") != 2 or slot is None or not common_binding(record, run_id, arm, slot, fixture_identity):
                raise ResultError(f"{arm} has an unbound command receipt")
            status, exit_code, classification = (record.get("status"), record.get("exit_code"),
                                                  record.get("classification"))
            if classification == "local-read-only":
                if status not in {"allowed", "allowed-failed"} or type(exit_code) is not int:
                    raise ResultError(f"{arm} has an invalid read-only stub record")
            elif classification in {"mutation-or-network-or-unsupported", "publication-or-network"}:
                if status != "rejected" or exit_code != 97:
                    raise ResultError(f"{arm} contains a successful mutation/network/publication record")
            else:
                raise ResultError(f"{arm} contains an unknown stub classification")
            if common_binding(record, run_id, arm, first_slot, fixture_identity):
                probe_records[tuple(record.get("command", []))] = (status, exit_code, classification)
        if any(probe_records.get(command) != expected for command, expected in expected_commands.items()):
            raise ResultError(f"{arm} controlled stub probes are incomplete")
        arm_logs = [r for r in validations if r.get("arm") == arm]
        if len(arm_logs) != 2:
            raise ResultError(f"{arm} validation log must contain exactly baseline and final full suites")
        by_phase = {r.get("phase"): r for r in arm_logs}
        if set(by_phase) != {"baseline", "final"}:
            raise ResultError(f"{arm} validation phases are wrong")
        final_slot = next(slot for slot in reversed(trace["expected_child_slots"][arm])
                          if slot["phase"] == "review" and slot["state"] == "S2")
        for phase, slot in (("baseline", first_slot), ("final", final_slot)):
            record = by_phase[phase]
            if (record.get("schema_version") != 2 or not common_binding(record, run_id, arm, slot, fixture_identity) or
                    record.get("command") != ["./run-tests.sh"] or record.get("exit_code") != 1 or
                    record.get("failures") != expected_failures or record.get("known_failure_sha256") != known_hash):
                raise ResultError(f"{arm} {phase} full-suite evidence is wrong or unbound")


def status_child(reference: dict[str, Any], base: Path, child_worktree: Path,
                 expected: dict[str, Any], controls: dict[str, Any]) -> tuple[str, int, float]:
    path = resolve_evidence(reference.get("status_artifact"), base, "Pi status artifact")
    try:
        path.relative_to(child_worktree)
    except ValueError:
        pass
    else:
        raise ResultError("Pi status artifact is inside measured child worktree")
    if path.name != "status.json":
        raise ResultError("Pi lifecycle artifact must be named status.json")
    artifact = load_json(path)
    index = reference.get("child_index")
    steps = artifact.get("steps")
    if type(index) is not int or index < 0 or not isinstance(steps, list) or index >= len(steps):
        raise ResultError("invalid Pi child index")
    step = steps[index]
    run_id, session_file = artifact.get("runId"), step.get("sessionFile")
    model = step.get("model")
    if model not in (controls["model"], f'{controls["model"]}:{controls["effort"]}'):
        raise ResultError("Pi artifact model mismatch")
    tokens, cost = step.get("tokens"), step.get("totalCost")
    if (artifact.get("lifecycleArtifactVersion") != 3 or artifact.get("state") != "completed" or
            step.get("status") != "completed" or step.get("thinking") != controls["effort"] or
            not isinstance(run_id, str) or not run_id or not isinstance(session_file, str) or not session_file or
            not isinstance(tokens, dict) or any(type(tokens.get(k)) is not int or tokens[k] < 0 for k in ("input", "output", "total")) or
            tokens["total"] <= 0 or tokens["total"] < tokens["input"] + tokens["output"] or
            not isinstance(cost, dict) or type(cost.get("costUsd")) not in (int, float) or cost["costUsd"] < 0):
        raise ResultError("Pi status artifact lacks completed session/token/cost evidence")
    if reference.get("slot_id") != expected["slot_id"]:
        raise ResultError("Pi child artifact reference is misbound to slot")
    return f"{run_id}:{index}:{session_file}", tokens["total"], float(cost["costUsd"])


def external_artifact(reference: dict[str, Any], field: str, base: Path,
                      child_worktree: Path, label: str) -> Path:
    path = resolve_evidence(reference.get(field), base, label)
    try:
        path.relative_to(child_worktree)
    except ValueError:
        return path
    raise ResultError(f"{label} is inside measured child worktree")


def verify_reviewer_outcome(path: Path, slot: dict[str, Any], trace: dict[str, Any]) -> None:
    outcome = load_json(path)
    if set(outcome) != {"verdict", "findings"} or outcome.get("verdict") not in {"approved", "changes_requested"}:
        raise ResultError("reviewer outcome does not match the strict review schema")
    findings = outcome.get("findings")
    if not isinstance(findings, list):
        raise ResultError("reviewer findings must be a list")
    for finding in findings:
        if (not isinstance(finding, dict) or set(finding) != {"severity", "requirement", "location", "evidence"} or
                finding.get("severity") not in {"Critical", "Important"} or
                any(not isinstance(finding.get(key), str) or not finding[key].strip()
                    for key in ("requirement", "location", "evidence"))):
            raise ResultError("reviewer finding does not match the strict review schema")
    expected = slot["outcome"]
    if expected["verdict"] == "approved":
        if outcome != {"verdict": "approved", "findings": []}:
            raise ResultError(f"{slot['slot_id']} did not produce the expected approval")
        return
    finding_id = expected.get("finding_id")
    authoritative = trace["findings"].get(finding_id, {})
    expected_file = str(authoritative.get("location", "")).split(":", 1)[0]
    matched = any(finding["location"].split(":", 1)[0] == expected_file for finding in findings)
    if outcome["verdict"] != "changes_requested" or not matched:
        raise ResultError(f"{slot['slot_id']} did not identify authoritative {finding_id}")


def checkout_tree(repo: Path, tree: str, destination: Path) -> None:
    destination.mkdir(parents=True)
    archive = git(GIT_EXE, repo, "archive", "--format=tar", tree).stdout
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as stream:
        # The archive is produced from this verifier-generated Git tree; no
        # caller-controlled tar headers are accepted independently of the patch.
        stream.extractall(destination)


def verify_reworker_outcome(path: Path, slot: dict[str, Any], trace: dict[str, Any],
                            fixture_root: Path) -> None:
    if not path.is_file() or not path.read_bytes():
        raise ResultError("reworker outcome patch is missing or empty")
    source = slot["state"]
    target = slot["outcome"]["target_state"]
    source_tree = trace["states"][source]["tree"]
    repo = fixture_root / "repository"
    try:
        result_tree = reconstructed_tree(GIT_EXE, repo, source_tree, path)
    except (AssertionError, OSError, subprocess.SubprocessError) as error:
        raise ResultError(f"reworker outcome patch does not apply to {source}: {error}") from error
    changed = git(GIT_EXE, repo, "diff-tree", "--no-commit-id", "--name-status", "-r",
                  source_tree, result_tree).stdout.decode().splitlines()
    helper = trace["helper"]
    if changed != [f"M\t{helper}"]:
        raise ResultError("reworker outcome changed files outside the existing helper allowlist")
    source_entry = git(GIT_EXE, repo, "ls-tree", source_tree, "--", helper).stdout.decode().split(maxsplit=2)[:2]
    result_entry = git(GIT_EXE, repo, "ls-tree", result_tree, "--", helper).stdout.decode().split(maxsplit=2)[:2]
    if source_entry != result_entry or source_entry not in (["100644", "blob"], ["100755", "blob"]):
        raise ResultError("reworker outcome changed the helper's file type or executable mode")
    with tempfile.TemporaryDirectory(prefix="gate-b-worker-outcome-") as name:
        worktree = Path(name) / "tree"
        checkout_tree(repo, result_tree, worktree)
        fixture_home = fixture_root / "fixture-home"
        probe_env = {
            "PATH": str(fixture_root / "stubs") + os.pathsep + os.defpath,
            "HOME": str(fixture_home), "XDG_CONFIG_HOME": str(fixture_home / "xdg"),
            "LANG": "C", "LC_ALL": "C", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_ATTR_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0",
            "GATE_B_RECEIPT_LOG": os.devnull,
        }
        observed = defect_probes(worktree, env=probe_env)
    expected = {"S1": (False, True), "S2": (False, False)}[target]
    if observed != expected:
        raise ResultError(f"reworker outcome does not produce target {target} behavior: {observed!r}")


def verify_outcome(reference: dict[str, Any], slot: dict[str, Any], trace: dict[str, Any],
                   evidence_base: Path, child_worktree: Path, fixture_root: Path) -> None:
    path = external_artifact(reference, "outcome_artifact", evidence_base, child_worktree,
                             "model outcome artifact")
    if slot["phase"] == "review":
        verify_reviewer_outcome(path, slot, trace)
    else:
        verify_reworker_outcome(path, slot, trace, fixture_root)


def verify_result(data: dict[str, Any], trace: dict[str, Any], evidence_base: Path,
                  fixture_root: Path) -> None:
    if (data.get("schema_version") != 2 or data.get("fixture_base_sha") != trace["base_sha"] or
            data.get("fixture_identity") != trace["fixture_identity"] or
            not isinstance(data.get("run_id"), str) or not data["run_id"]):
        raise ResultError("wrong result schema, fixture identity, or run id")
    if "trace_path" in data:
        raise ResultError("result-selected trace paths are forbidden")
    controls = data.get("controls")
    if not isinstance(controls, dict) or controls != {"model": trace["controls"]["model"], "effort": trace["controls"]["effort"]}:
        raise ResultError("wrong model or effort control")
    arms = data.get("arms")
    if not isinstance(arms, dict) or set(arms) != {"v2", "v3"}:
        raise ResultError("result must contain exactly v2 and v3 arms")
    verify_evidence(data, trace, evidence_base)
    seen_sessions: set[str] = set()
    totals: dict[str, int] = {}
    final_hash = trace["states"]["S2"]["review_diff_sha256"]
    child_worktree = (fixture_root / trace["isolation"]["child_worktree"]).resolve()
    for arm in ("v2", "v3"):
        record = arms[arm]
        if not isinstance(record, dict) or record.get("dispatch") != trace["dispatch"][arm]:
            raise ResultError(f"{arm} dispatch sequence is wrong")
        sessions = record.get("sessions")
        if not isinstance(sessions, list):
            raise ResultError(f"{arm} sessions are missing")
        expected_slots = {slot["slot_id"]: slot for slot in trace["expected_child_slots"][arm]}
        actual_slots: dict[str, dict[str, Any]] = {}
        calculated = 0
        for reference in sessions:
            if not isinstance(reference, dict) or set(reference) != {"slot_id", "status_artifact", "child_index", "outcome_artifact"}:
                raise ResultError("session envelope must contain only status/outcome artifact references, child index, and slot")
            slot_id = reference["slot_id"]
            if slot_id not in expected_slots or slot_id in actual_slots:
                raise ResultError(f"{arm} has extra or duplicate child slot")
            slot = expected_slots[slot_id]
            identity, tokens, _cost = status_child(reference, evidence_base, child_worktree,
                                                   slot, controls)
            verify_outcome(reference, slot, trace, evidence_base, child_worktree, fixture_root)
            if identity in seen_sessions:
                raise ResultError("globally duplicate Pi child session")
            seen_sessions.add(identity); calculated += tokens
            actual_slots[slot_id] = slot
        if set(actual_slots) != set(expected_slots):
            raise ResultError(f"{arm} is missing child slots")
        slots = list(actual_slots.values())
        derived_reworks = [s["outcome"]["resolves"] for s in slots if s["phase"] == "rework"]
        if record.get("reworks") != derived_reworks or derived_reworks != ["F1", "F2"]:
            raise ResultError(f"{arm} rework summary is not slot-derived")
        final_reviews = {s["axis"]: {"verdict": s["outcome"]["verdict"], "diff_sha256": s["review_diff_sha256"]}
                         for s in slots if s["phase"] == "review" and s["state"] == "S2" and s["outcome"]["verdict"] == "approved"}
        if not landing_eligible(final_hash, final_reviews) or record.get("final_approvals") != final_reviews:
            raise ResultError(f"{arm} final approvals are not exact S2 approvals")
        if "fidelity" in record:
            raise ResultError(f"{arm} contains a caller-supplied fidelity assertion")
        if record.get("full_suite_invocations") != trace["validation"]["expected_full_suite_invocations"]:
            raise ResultError(f"{arm} full-suite count summary disagrees with evidence")
        if "total_tokens" in record or any("usage" in ref for ref in sessions):
            raise ResultError("result envelope contains forbidden usage numbers or labels")
        totals[arm] = calculated
    if totals["v2"] > trace["controls"]["v2_token_ceiling"] or totals["v3"] >= totals["v2"]:
        raise ResultError("artifact-derived token ceiling/win failed")


def binding_fields(run_id: str, arm: str, slot: dict[str, Any], trace: dict[str, Any]) -> dict[str, Any]:
    state_hash, transition_hash = slot_hash(slot)
    return {"run_id": run_id, "arm": arm, "slot_id": slot["slot_id"],
            "fixture_identity": trace["fixture_identity"], "state_hash": state_hash,
            "transition_hash": transition_hash}


def write_self_test_evidence(root: Path, trace: dict[str, Any], run_id: str) -> None:
    receipt = root / trace["isolation"]["command_receipt"]
    env = os.environ.copy()
    env["PATH"] = str(root / "stubs") + os.pathsep + env["PATH"]
    env["GATE_B_RECEIPT_LOG"] = str(receipt)
    env["GATE_B_FIXTURE_IDENTITY"] = trace["fixture_identity"]
    env["GATE_B_RUN_ID"] = run_id
    commands = (["git", "status"], ["git", "push"], ["git", "-c", "fixture.key=value", "push"],
                ["git", "upload-pack", "."], ["gh", "pr", "create"], ["publish-check.py"])
    for arm in ("v2", "v3"):
        slot = trace["expected_child_slots"][arm][0]
        env.update({"GATE_B_ARM": arm, "GATE_B_SLOT_ID": slot["slot_id"],
                    "GATE_B_STATE_HASH": str(slot.get("review_diff_sha256") or ""),
                    "GATE_B_TRANSITION_HASH": str(slot.get("transition_sha256") or "")})
        for command in commands:
            result = subprocess.run(command, cwd=root / "child-worktree", env=env,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            expected = 0 if command == ["git", "status"] else 97
            if result.returncode != expected:
                raise AssertionError(f"stub returned {result.returncode}, expected {expected}: {command!r}")
    log = root / trace["isolation"]["validation_log"]
    records = []
    for arm in ("v2", "v3"):
        base_result = full_suite(root / "repository")
        with tempfile.TemporaryDirectory(prefix="gate-b-evidence-") as name:
            final = Path(name) / "S2"; materialize_state(root, trace, "S2", final)
            final_result = full_suite(final)
        first = trace["expected_child_slots"][arm][0]
        final_slot = next(slot for slot in reversed(trace["expected_child_slots"][arm])
                          if slot["phase"] == "review" and slot["state"] == "S2")
        for phase, result, slot in (("baseline", base_result, first), ("final", final_result, final_slot)):
            record = {"schema_version": 2, "phase": phase, "command": ["./run-tests.sh"],
                      "exit_code": result[0], "failures": result[1],
                      "known_failure_sha256": trace["validation"]["known_failure_sha256"]}
            record.update(binding_fields(run_id, arm, slot, trace)); records.append(record)
    log.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records))


def canned_result(root: Path, trace: dict[str, Any], run_id: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema_version": 2, "fixture_base_sha": trace["base_sha"],
        "fixture_identity": trace["fixture_identity"], "run_id": run_id,
        "controls": {"model": trace["controls"]["model"], "effort": trace["controls"]["effort"]},
        "evidence": {"command_receipts": str(root / trace["isolation"]["command_receipt"]),
                     "validation_log": str(root / trace["isolation"]["validation_log"]),
                     "sanitized_home_receipt": str(root / "metadata/sanitized-home.json")},
        "arms": {},
    }
    artifact_dir = root / "test-only-status-artifacts"; artifact_dir.mkdir()
    outcome_dir = root / "test-only-outcome-artifacts"; outcome_dir.mkdir()
    for arm, total in (("v2", 200000), ("v3", 150000)):
        slots = trace["expected_child_slots"][arm]; per, remainder = divmod(total, len(slots)); sessions = []
        for index, slot in enumerate(slots):
            tokens = per + (1 if index < remainder else 0)
            artifact = {"lifecycleArtifactVersion": 3, "runId": f"test-only-{arm}-{index}",
                        "state": "completed", "testOnly": True, "steps": [{
                            "status": "completed", "sessionFile": str(artifact_dir / f"session-{arm}-{index}.jsonl"),
                            "model": f'{trace["controls"]["model"]}:{trace["controls"]["effort"]}',
                            "thinking": trace["controls"]["effort"],
                            "tokens": {"input": tokens - 100, "output": 100, "total": tokens},
                            "totalCost": {"inputTokens": tokens - 100, "outputTokens": 100, "costUsd": 1.0}}]}
            artifact_path = artifact_dir / f"{arm}-{index}" / "status.json"; artifact_path.parent.mkdir()
            canonical = json.dumps(artifact, indent=2, sort_keys=True) + "\n"; artifact_path.write_text(canonical)
            if slot["phase"] == "review":
                expected = slot["outcome"]
                if expected["verdict"] == "approved":
                    outcome: object = {"verdict": "approved", "findings": []}
                else:
                    finding = trace["findings"][expected["finding_id"]]
                    outcome = {"verdict": "changes_requested", "findings": [{
                        "severity": "Important", "requirement": finding["finding"],
                        "location": finding["location"], "evidence": "test-only authoritative finding evidence"}]}
                outcome_path = outcome_dir / f"{arm}-{index}-review.json"
                outcome_path.write_text(json.dumps(outcome, indent=2, sort_keys=True) + "\n")
            else:
                target = slot["outcome"]["target_state"]
                outcome_path = outcome_dir / f"{arm}-{index}-rework.patch"
                shutil.copyfile(root / trace["transitions"][f'{slot["state"]}->{target}']["patch"], outcome_path)
            sessions.append({"slot_id": slot["slot_id"], "status_artifact": str(artifact_path),
                             "child_index": 0, "outcome_artifact": str(outcome_path)})
        final_approvals = {slot["axis"]: {"verdict": "approved", "diff_sha256": slot["review_diff_sha256"]}
                           for slot in slots if slot["phase"] == "review" and slot["state"] == "S2" and slot["outcome"]["verdict"] == "approved"}
        result["arms"][arm] = {"dispatch": trace["dispatch"][arm], "sessions": sessions,
                               "reworks": ["F1", "F2"],
                               "full_suite_invocations": trace["validation"]["expected_full_suite_invocations"],
                               "final_approvals": final_approvals}
    return result


def hostile_environment_regression(parent: Path) -> None:
    victim = parent / "victim"; victim.mkdir()
    git(GIT_EXE, victim, "init", "-q", "-b", "main")
    (victim / "victim.txt").write_text("untouched\n")
    git(GIT_EXE, victim, "add", "victim.txt")
    identity = {"GIT_AUTHOR_NAME": "Victim", "GIT_AUTHOR_EMAIL": "victim@example.invalid",
                "GIT_COMMITTER_NAME": "Victim", "GIT_COMMITTER_EMAIL": "victim@example.invalid",
                "GIT_AUTHOR_DATE": "2001-01-01T00:00:00+0000", "GIT_COMMITTER_DATE": "2001-01-01T00:00:00+0000"}
    git(GIT_EXE, victim, "commit", "-q", "-m", "victim", env=identity)
    before = (git(GIT_EXE, victim, "rev-parse", "HEAD").stdout,
              digest(victim / ".git/index"), (victim / "victim.txt").read_bytes())
    hostile_home = parent / "hostile-home"; hostile_home.mkdir()
    (hostile_home / ".gitconfig").write_text("[core]\n\tautocrlf = true\n[alias]\n\tstatus = reset --hard\n[diff]\n\texternal = false\n")
    templates = parent / "hostile-templates" / "hooks"; templates.mkdir(parents=True)
    hook_marker = parent / "hostile-hook-ran"
    hook = templates / "post-commit"
    hook.write_text(f"#!/bin/sh\necho hit >> {json.dumps(str(hook_marker))}\n"); hook.chmod(0o755)
    hostile = {"GIT_DIR": str(victim / ".git"), "GIT_WORK_TREE": str(victim),
               "GIT_INDEX_FILE": str(victim / ".git/index"), "GIT_DEFAULT_HASH": "sha256",
               "GIT_CONFIG_GLOBAL": str(hostile_home / ".gitconfig"),
               "GIT_TEMPLATE_DIR": str(parent / "hostile-templates"), "GIT_EXTERNAL_DIFF": "false",
               "HOME": str(hostile_home)}
    old = {key: os.environ.get(key) for key in hostile}; os.environ.update(hostile)
    fixture = parent / "hostile-generated"
    try:
        trace = generate(fixture)
    finally:
        for key, value in old.items():
            if value is None: os.environ.pop(key, None)
            else: os.environ[key] = value
    after = (git(GIT_EXE, victim, "rev-parse", "HEAD").stdout,
             digest(victim / ".git/index"), (victim / "victim.txt").read_bytes())
    author = git(GIT_EXE, fixture / "repository", "show", "-s", "--format=%an <%ae>", "HEAD").stdout.decode().strip()
    if (before != after or hook_marker.exists() or
            author != "Gate B Trace Fixture <gate-b-trace@example.invalid>"):
        raise AssertionError("hostile Git environment changed victim, ran a hook, or changed fixture identity")


def self_test(explicit_matrix: bool) -> None:
    with tempfile.TemporaryDirectory(prefix="gate-b-trace-selftest-a-") as a_name, \
         tempfile.TemporaryDirectory(prefix="gate-b-trace-selftest-b-") as b_name:
        first, second = Path(a_name), Path(b_name)
        trace_a, trace_b = generate(first), generate(second)
        validate_generated(first, trace_a)
        validate_generated(second, trace_b)
        identity = lambda trace: {"base": trace["base_sha"],
            "trees": {k: v["tree"] for k, v in trace["states"].items()},
            "reviews": {k: v["review_diff_sha256"] for k, v in trace["states"].items()},
            "transitions": {k: v["sha256"] for k, v in trace["transitions"].items()}}
        if identity(trace_a) != identity(trace_b):
            raise AssertionError("independent fixture generations are not deterministic")
        if explicit_matrix:
            assert_dispatch_matrix(trace_a)
        run_id = "verifier-issued-test-run"
        write_self_test_evidence(first, trace_a, run_id)
        good = canned_result(first, trace_a, run_id)
        verify_result(good, trace_a, first, first)

        negative_dir = first / "test-only-negative-outcomes"; negative_dir.mkdir()
        malformed_review = negative_dir / "malformed-review.json"
        malformed_review.write_text('{"verdict":"changes_requested","findings":[],"extra":true}\n')
        wrong_review = negative_dir / "wrong-review.json"
        wrong_review.write_text(json.dumps({"verdict": "approved", "findings": []}) + "\n")
        wrong_location = negative_dir / "wrong-location.json"
        wrong_location.write_text(json.dumps({"verdict": "changes_requested", "findings": [{
            "severity": "Important", "requirement": "wrong location", "location": "README.md:1",
            "evidence": "non-empty"}]}) + "\n")
        with tempfile.TemporaryDirectory(prefix="gate-b-negative-patches-") as name:
            source = Path(name) / "S0"; materialize_state(first, trace_a, "S0", source)
            (source / "bc-svc").write_text((source / "bc-svc").read_text() + "\n# out of scope\n")
            out_of_scope = negative_dir / "out-of-scope.patch"
            out_of_scope.write_bytes(git(GIT_EXE, source, "diff", "--binary", "--full-index", "--no-ext-diff",
                                         trace_a["states"]["S0"]["tree"]).stdout)
        with tempfile.TemporaryDirectory(prefix="gate-b-negative-patches-") as name:
            source = Path(name) / "S0"; materialize_state(first, trace_a, "S0", source)
            helper = source / trace_a["helper"]
            helper.write_text(helper.read_text() + "# does not fix F1\n")
            wrong_behavior = negative_dir / "wrong-behavior.patch"
            wrong_behavior.write_bytes(git(GIT_EXE, source, "diff", "--binary", "--full-index", "--no-ext-diff",
                                           trace_a["states"]["S0"]["tree"]).stdout)
        first_review = next(i for i, slot in enumerate(trace_a["expected_child_slots"]["v2"])
                            if slot["phase"] == "review" and slot["outcome"]["verdict"] == "changes_requested")
        first_rework = next(i for i, slot in enumerate(trace_a["expected_child_slots"]["v2"])
                            if slot["phase"] == "rework")
        mutations = [
            ("missing slot", lambda x: x["arms"]["v2"]["sessions"].pop()),
            ("extra slot", lambda x: x["arms"]["v2"]["sessions"].append({"slot_id": "extra"})),
            ("duplicate slot", lambda x: x["arms"]["v2"]["sessions"][1].update(slot_id=x["arms"]["v2"]["sessions"][0]["slot_id"])),
            ("duplicate artifact session", lambda x: x["arms"]["v3"]["sessions"][0].update(status_artifact=x["arms"]["v2"]["sessions"][0]["status_artifact"])),
            ("missing outcome", lambda x: x["arms"]["v2"]["sessions"][0].pop("outcome_artifact")),
            ("wrong reviewer outcome", lambda x: x["arms"]["v2"]["sessions"][first_review].update(outcome_artifact=str(wrong_review))),
            ("malformed reviewer schema", lambda x: x["arms"]["v2"]["sessions"][first_review].update(outcome_artifact=str(malformed_review))),
            ("wrong reviewer location", lambda x: x["arms"]["v2"]["sessions"][first_review].update(outcome_artifact=str(wrong_location))),
            ("out-of-scope reworker patch", lambda x: x["arms"]["v2"]["sessions"][first_rework].update(outcome_artifact=str(out_of_scope))),
            ("behaviorally wrong reworker patch", lambda x: x["arms"]["v2"]["sessions"][first_rework].update(outcome_artifact=str(wrong_behavior))),
            ("envelope usage", lambda x: x["arms"]["v2"]["sessions"][0].update(usage={"total": 1})),
            ("caller fidelity", lambda x: x["arms"]["v2"].update(fidelity={"state_hashes": True})),
            ("summary lie", lambda x: x["arms"]["v2"].update(reworks=["F1"])),
            ("wrong receipt", lambda x: x["evidence"].update(command_receipts="missing.jsonl")),
            ("wrong final approval", lambda x: x["arms"]["v3"]["final_approvals"]["spec"].update(diff_sha256="0" * 64)),
            ("result-selected trace", lambda x: x.update(trace_path="attacker.json")),
        ]
        for label, mutate in mutations:
            bad = copy.deepcopy(good)
            mutate(bad)
            try:
                verify_result(bad, trace_a, first, first)
            except ResultError:
                pass
            else:
                raise AssertionError(f"result verifier accepted {label}")

        hostile_environment_regression(first)
        print("PASS hostile Git routing/config/hash/template inputs leave victim HEAD/index/worktree unchanged")
        print("PASS base and S2 full suites have exactly tests/test_known_baseline.sh")
        print("PASS known-failure hash unchanged and F1/F2 probes are S0-only/S1-only/neither")
        print("PASS independent roots have identical state/tree/review/transition hashes")
        print("PASS Pi status artifacts derive child identity/tokens/cost; envelope-only usage rejected")
        print("PASS reviewer JSON and reworker patches derive model fidelity; caller assertions rejected")
        print("PASS canonical contract ignores/rejects result-selected modified trace paths")
        print("PASS fail-closed Git/gh/publication stub receipts and bound validation logs")
        print("PASS stale S0 approvals block S1/S2; exact dual S2 approval lands")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--assert-dispatch-matrix", action="store_true")
    parser.add_argument("--verify-result", metavar="JSON")
    args = parser.parse_args()
    if args.assert_dispatch_matrix and not args.self_test:
        parser.error("--assert-dispatch-matrix requires --self-test")
    if args.self_test == bool(args.verify_result):
        parser.error("choose exactly one of --self-test or --verify-result")
    try:
        if args.self_test:
            self_test(args.assert_dispatch_matrix)
        else:
            result_path = Path(args.verify_result).resolve()
            data = load_json(result_path)
            # The verifier, never the untrusted result, selects and validates the
            # canonical contract used for every identity/slot/evidence check.
            with tempfile.TemporaryDirectory(prefix="gate-b-trace-verify-") as name:
                fixture_root = Path(name)
                trace = generate(fixture_root)
                validate_generated(fixture_root, trace)
                verify_result(data, trace, result_path.parent, fixture_root)
            print("PASS real Gate B result envelope against verifier-generated contract")
    except (AssertionError, ResultError, json.JSONDecodeError, OSError, subprocess.SubprocessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
