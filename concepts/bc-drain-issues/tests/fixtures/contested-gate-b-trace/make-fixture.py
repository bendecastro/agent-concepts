#!/usr/bin/env python3
"""Generate the deterministic, isolated contested Gate B trace fixture."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

FIXED_ENV = {
    "GIT_AUTHOR_NAME": "Gate B Trace Fixture",
    "GIT_AUTHOR_EMAIL": "gate-b-trace@example.invalid",
    "GIT_COMMITTER_NAME": "Gate B Trace Fixture",
    "GIT_COMMITTER_EMAIL": "gate-b-trace@example.invalid",
    "GIT_AUTHOR_DATE": "2000-01-01T00:00:00+0000",
    "GIT_COMMITTER_DATE": "2000-01-01T00:00:00+0000",
}
HELPER = "lib/internal-note.sh"
MODEL = "openai-codex/gpt-5.6-sol"
EFFORT = "medium"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> None:
    root = (Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else
            Path(tempfile.mkdtemp(prefix="bc-drain-gate-b-trace-")))
    if len(sys.argv) > 2:
        raise SystemExit("usage: make-fixture.py [empty-output-root]")
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise SystemExit(f"output root is not empty: {root}")
    git_exe = str(Path(shutil.which("git") or "").resolve())
    if not Path(git_exe).is_file():
        raise SystemExit("git is required")

    repo, child, oracle = root / "repository", root / "child-worktree", root / "oracle"
    stubs, metadata = root / "stubs", root / "metadata"
    receipts, validation_logs = root / "receipts", root / "validation-logs"
    fixture_home, templates = root / "fixture-home", root / "empty-git-templates"
    for directory in (repo, oracle, stubs, metadata, receipts, validation_logs,
                      fixture_home, fixture_home / "xdg", templates):
        directory.mkdir(parents=True)

    def git_environment(extra: dict[str, str] | None = None) -> dict[str, str]:
        # Git has many environment escape hatches.  Start from the ordinary
        # process environment only for non-Git settings, then install a complete
        # fixture-owned configuration/identity boundary.
        env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        env.update(FIXED_ENV)
        env.update({
            "HOME": str(fixture_home), "XDG_CONFIG_HOME": str(fixture_home / "xdg"),
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull, "GIT_ATTR_NOSYSTEM": "1",
            "GIT_TEMPLATE_DIR": str(templates), "GIT_DEFAULT_HASH": "sha1",
            "GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_COUNT": "4",
            "GIT_CONFIG_KEY_0": "core.hooksPath", "GIT_CONFIG_VALUE_0": os.devnull,
            "GIT_CONFIG_KEY_1": "diff.external", "GIT_CONFIG_VALUE_1": "",
            "GIT_CONFIG_KEY_2": "core.autocrlf", "GIT_CONFIG_VALUE_2": "false",
            "GIT_CONFIG_KEY_3": "init.defaultObjectFormat", "GIT_CONFIG_VALUE_3": "sha1",
        })
        if extra:
            env.update(extra)
        return env

    def run_git(*args: str, cwd: Path = repo, binary: bool = False) -> str | bytes:
        result = subprocess.run([git_exe, *args], cwd=cwd, env=git_environment(),
                                text=not binary, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode:
            error = result.stderr.decode() if binary else result.stderr
            raise RuntimeError(f"git {' '.join(args)} failed: {error}")
        return result.stdout

    def write(rel: str, text: str, executable: bool = False) -> None:
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        if executable:
            path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    run_git("init", "-q", "-b", "main", str(repo), cwd=root)
    run_git("config", "user.name", FIXED_ENV["GIT_AUTHOR_NAME"])
    run_git("config", "user.email", FIXED_ENV["GIT_AUTHOR_EMAIL"])
    run_git("config", "commit.gpgSign", "false")
    run_git("config", "tag.gpgSign", "false")

    write("bc-svc", """#!/bin/sh
set -eu
case "${1:-}" in
  status) shift; printf 'status:%s\\n' "${1:-default}" ;;
  restart) shift; printf 'restart:%s\\n' "${1:-default}" ;;
  --help) printf '%s\\n' 'bc-svc status <target>' 'bc-svc restart <target>' ;;
  *) printf 'unknown command\\n' >&2; exit 2 ;;
esac
""", executable=True)
    write(HELPER, """# Maintainer-only diagnostic helper; deliberately not part of the public CLI.
bc_internal_write_note() {
    note_path=$1
    tmp_dir=$(mktemp -d "${TMPDIR:-/tmp}/bc-svc-note.XXXXXX") || return 1
    tmp_path=$tmp_dir/note
    printf '%s\\n' "$2" > $tmp_path
    rc=0
    mv $tmp_path $note_path || rc=$?
    rm -rf $tmp_dir
    return "$rc"
}
""")
    write("tests/test_old.sh", """#!/bin/sh
set -eu
[ "$(./bc-svc status alpha)" = 'status:alpha' ]
[ "$(./bc-svc restart alpha)" = 'restart:alpha' ]
""", executable=True)
    write("tests/test_known_baseline.sh", """#!/bin/sh
echo 'KNOWN_BASELINE_FAILURE: fixture upstream #7' >&2
exit 1
""", executable=True)
    write("run-tests.sh", """#!/bin/sh
rc=0
for test_file in tests/test_*.sh; do
    if "$test_file"; then printf 'PASS %s\\n' "$test_file"; else printf 'FAIL %s\\n' "$test_file"; rc=1; fi
done
exit "$rc"
""", executable=True)
    write("AGENTS.md", """# Fixture rules

- POSIX sh only.
- Preserve the old top-level commands while adding the `service` group.
- Keep maintainer-only helpers robust for whitespace, glob characters, and hostile temporary directories.
- `./run-tests.sh` is the full suite; `tests/test_known_baseline.sh` is the sole known failure.
""")
    write(".gitignore", ".trace-sessions/\n")
    run_git("add", "--all")
    run_git("-c", "commit.gpgSign=false", "commit", "-q", "-m", "deterministic Gate B base")
    base_sha = run_git("rev-parse", "HEAD").strip()
    known_hash = sha256((repo / "tests/test_known_baseline.sh").read_bytes())

    # Grouped-interface implementation and tests first appear in S0.  Thus the
    # base full suite has exactly its one intentional failure.
    grouped_bc_svc = """#!/bin/sh
set -eu
case "${1:-}" in
  service)
    shift
    case "${1:-}" in
      status) shift; printf 'status:%s\\n' "${1:-default}" ;;
      restart) shift; printf 'restart:%s\\n' "${1:-default}" ;;
      *) printf 'unknown service command\\n' >&2; exit 2 ;;
    esac ;;
  status) shift; printf 'status:%s\\n' "${1:-default}" ;;
  restart) shift; printf 'restart:%s\\n' "${1:-default}" ;;
  --help) printf '%s\\n' 'bc-svc status <target>' 'bc-svc restart <target>' \\
      'bc-svc service status <target>' 'bc-svc service restart <target>' ;;
  *) printf 'unknown command\\n' >&2; exit 2 ;;
esac
"""
    write("bc-svc", grouped_bc_svc, executable=True)
    write("tests/test_service.sh", """#!/bin/sh
set -eu
[ "$(./bc-svc service status alpha)" = 'status:alpha' ]
[ "$(./bc-svc service restart alpha)" = 'restart:alpha' ]
./bc-svc --help | grep -q 'bc-svc service status'
""", executable=True)

    # S0 has only F1: secure unique creation, but unsafe unquoted uses.  S1 fixes
    # quoting while deliberately introducing F2's predictable file.  S2 fixes F2.
    state_bodies = {
        "S0": (repo / HELPER).read_text(),
        "S1": """# Maintainer-only diagnostic helper; deliberately not part of the public CLI.
bc_internal_write_note() {
    note_path=$1
    tmp_path=${TMPDIR:-/tmp}/bc-svc-note
    printf '%s\\n' "$2" > "$tmp_path"
    mv "$tmp_path" "$note_path"
}
""",
        "S2": """# Maintainer-only diagnostic helper; deliberately not part of the public CLI.
bc_internal_write_note() {
    note_path=$1
    tmp_dir=$(mktemp -d "${TMPDIR:-/tmp}/bc-svc-note.XXXXXX") || return 1
    tmp_path=$tmp_dir/note
    printf '%s\\n' "$2" > "$tmp_path"
    rc=0
    mv "$tmp_path" "$note_path" || rc=$?
    rm -rf "$tmp_dir"
    return "$rc"
}
""",
    }

    states: dict[str, dict[str, object]] = {}
    for name in ("S0", "S1", "S2"):
        (repo / HELPER).write_text(state_bodies[name])
        run_git("add", "--all")
        tree = run_git("write-tree").strip()
        patch = run_git("diff", "--binary", "--full-index", "--no-ext-diff",
                        base_sha, tree, binary=True)
        patch_path = oracle / f"review-{name}.patch"
        patch_path.write_bytes(patch)
        states[name] = {"tree": tree, "review_diff": f"oracle/{patch_path.name}",
                        "review_diff_sha256": sha256(patch)}

    transitions: dict[str, dict[str, object]] = {}
    for source, target, finding in (("S0", "S1", "F1"), ("S1", "S2", "F2")):
        patch = run_git("diff", "--binary", "--full-index", "--no-ext-diff",
                        str(states[source]["tree"]), str(states[target]["tree"]), binary=True)
        name = f"{source}-to-{target}.patch"
        (oracle / name).write_bytes(patch)
        transitions[f"{source}->{target}"] = {
            "patch": f"oracle/{name}", "sha256": sha256(patch), "resolves": finding,
            "changed_files": [HELPER],
            "flags": {key: False for key in ("file_added", "file_removed", "test_changed",
                       "dependency_changed", "public_interface_changed", "observable_behavior_changed",
                       "external_platform_changed", "spec_invalidated")},
        }

    findings = {
        "F1": {"axis": "standards", "severity": "important", "state": "S0",
               "location": f"{HELPER}:6-9", "finding": "Unquoted paths undergo word splitting and pathname expansion.",
               "verdict": "changes_requested"},
        "F2": {"axis": "standards", "severity": "important", "state": "S1",
               "location": f"{HELPER}:4", "finding": "The fixed temporary pathname permits collisions and symlink following.",
               "verdict": "changes_requested"},
    }
    acceptance = {"rows": [
        {"id": "A1", "requirement": "add service status and restart", "files": ["bc-svc", "tests/test_service.sh"]},
        {"id": "A2", "requirement": "preserve old status and restart", "files": ["bc-svc", "tests/test_old.sh"]},
        {"id": "A3", "requirement": "help lists both interfaces", "files": ["bc-svc", "tests/test_service.sh"]},
    ], "unmapped_internal_files": [HELPER]}
    validation = {
        "known_baseline_failure": "tests/test_known_baseline.sh",
        "known_failure_sha256": known_hash,
        "expected_full_suite_invocations": {"baseline": 1, "final": 1, "total": 2},
        "expected_baseline_failures": ["tests/test_known_baseline.sh"],
        "expected_final_failures": ["tests/test_known_baseline.sh"],
        "receipt_schema": 1, "validation_log_schema": 1,
    }
    dispatch = {
        "v2": [{"round": "R1", "axes": ["spec", "standards"], "state": "S0"},
               {"round": "R2", "axes": ["spec", "standards"], "state": "S1"},
               {"round": "R3", "axes": ["spec", "standards"], "state": "S2"}],
        "v3": [{"round": "R1", "axes": ["spec", "standards"], "state": "S0"},
               {"round": "R2", "axes": ["standards"], "state": "S1"},
               {"round": "R3", "axes": ["standards"], "state": "S2"},
               {"round": "final-sync", "axes": ["spec"], "state": "S2", "focused": True}],
    }
    verdicts = {"S0": {"spec": "approved", "standards": "changes_requested:F1"},
                "S1": {"spec": "approved", "standards": "changes_requested:F2"},
                "S2": {"spec": "approved", "standards": "approved"}}

    def slots_for(arm: str) -> list[dict[str, object]]:
        slots: list[dict[str, object]] = []
        for item in dispatch[arm]:
            for axis in item["axes"]:
                verdict = verdicts[item["state"]][axis]
                outcome: dict[str, object] = {"verdict": verdict.split(":")[0]}
                if ":" in verdict:
                    outcome["finding_id"] = verdict.split(":", 1)[1]
                slots.append({"slot_id": f"{arm}:{item['round']}:review:{axis}", "phase": "review",
                              "round": item["round"], "role": "reviewer", "axis": axis,
                              "state": item["state"], "review_diff_sha256": states[item["state"]]["review_diff_sha256"],
                              "outcome": outcome})
            if item["state"] in ("S0", "S1"):
                source, target, finding = (("S0", "S1", "F1") if item["state"] == "S0" else ("S1", "S2", "F2"))
                slots.append({"slot_id": f"{arm}:{item['round']}:rework:{finding}", "phase": "rework",
                              "round": item["round"], "role": "reworker", "axis": "standards", "state": source,
                              "transition_sha256": transitions[f"{source}->{target}"]["sha256"],
                              "outcome": {"status": "completed", "resolves": finding, "target_state": target}})
        return slots

    final_hash = states["S2"]["review_diff_sha256"]
    approvals = {"stale_spec_hash": states["S0"]["review_diff_sha256"],
                 "final": {axis: {"verdict": "approved", "diff_sha256": final_hash}
                           for axis in ("spec", "standards")}}
    approvals["final"]["spec"]["focused_hash_sync"] = True
    fixture_identity = sha256(json.dumps({"base_sha": base_sha, "states": states,
        "transitions": transitions}, sort_keys=True).encode())
    trace = {
        "schema_version": 2, "fixture": "contested-gate-b-trace",
        "fixture_identity": fixture_identity, "base_sha": base_sha,
        "helper": HELPER, "states": states, "transitions": transitions, "findings": findings,
        "expected_verdicts": verdicts, "allowed_transition_files": [HELPER],
        "acceptance_mapping": "metadata/acceptance-map.json", "validation": validation,
        "dispatch": dispatch, "expected_child_slots": {arm: slots_for(arm) for arm in ("v2", "v3")},
        "approvals": approvals,
        "controls": {"model": MODEL, "effort": EFFORT, "minimum_reworks": 2, "v2_token_ceiling": 500000},
        "isolation": {"physical_network_isolation": False, "github_allowed": False,
                      "real_push_allowed": False, "repository_has_no_remote": True,
                      "sanitized_home": "fixture-home", "environment_script": "env.sh",
                      "child_worktree": "child-worktree", "future_oracle_root": "oracle",
                      "future_oracles_outside_child_worktree": True,
                      "command_receipt": "receipts/commands.jsonl",
                      "validation_log": "validation-logs/full-suites.jsonl"},
    }
    canonical_json(metadata / "acceptance-map.json", acceptance)
    canonical_json(metadata / "standards-findings.json", findings)
    canonical_json(metadata / "validation.json", validation)
    canonical_json(root / "TRACE.json", trace)
    env_receipt = {"schema_version": 1, "fixture_identity": fixture_identity,
                   "home": "fixture-home", "xdg_config_home": "fixture-home/xdg",
                   "credentials_present": False, "physical_network_isolation": False}
    canonical_json(metadata / "sanitized-home.json", env_receipt)
    env_text = ('unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_COMMON_DIR GIT_EXTERNAL_DIFF GIT_CONFIG GIT_CONFIG_COUNT GIT_DEFAULT_HASH\n'
                f'export HOME={json.dumps(str(fixture_home))}\n'
                f'export XDG_CONFIG_HOME={json.dumps(str(fixture_home / "xdg"))}\n'
                f'export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL={json.dumps(os.devnull)} GIT_CONFIG_SYSTEM={json.dumps(os.devnull)} GIT_ATTR_NOSYSTEM=1 GIT_DEFAULT_HASH=sha1 GIT_TERMINAL_PROMPT=0\n'
                f'export GIT_TEMPLATE_DIR={json.dumps(str(templates))}\n'
                f'export PATH={json.dumps(str(stubs))}:"$PATH"\n'
                f'export GATE_B_FIXTURE_IDENTITY={json.dumps(fixture_identity)}\n'
                f'export GATE_B_RECEIPT_LOG={json.dumps(str(receipts / "commands.jsonl"))}\n')
    (root / "env.sh").write_text(env_text)

    run_git("reset", "--hard", "-q", base_sha)
    run_git("worktree", "add", "-q", "--detach", str(child), base_sha)
    run_git("apply", str(oracle / "review-S0.patch"), cwd=child)
    if run_git("remote", cwd=repo).strip():
        raise RuntimeError("fixture repository unexpectedly has a remote")

    receipt_path = str(receipts / "commands.jsonl")
    record_code = f'''import json, os, pathlib, sys
identity = pathlib.Path(sys.argv[0]).name
record = {{"schema_version": 2, "run_id": os.environ.get("GATE_B_RUN_ID"),
          "arm": os.environ.get("GATE_B_ARM"), "slot_id": os.environ.get("GATE_B_SLOT_ID"),
          "fixture_identity": os.environ.get("GATE_B_FIXTURE_IDENTITY"),
          "state_hash": os.environ.get("GATE_B_STATE_HASH"),
          "transition_hash": os.environ.get("GATE_B_TRANSITION_HASH"),
          "command": [identity, *sys.argv[1:]], "stub_identity": "fixture-" + identity + "-stub"}}
path = pathlib.Path(os.environ.get("GATE_B_RECEIPT_LOG", {json.dumps(receipt_path)}))
def finish(status, exit_code, classification):
    record.update(status=status, exit_code=exit_code, classification=classification)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as stream: stream.write(json.dumps(record, sort_keys=True) + "\\n")
    return exit_code
'''
    git_body = f'''#!/usr/bin/env python3
{record_code}
args = sys.argv[1:]
allowed = {{"status", "diff", "rev-parse", "show", "log", "ls-files", "diff-tree", "cat-file"}}
# No global options are accepted: they can reroute repositories, inject aliases,
# or alter config before the nominal subcommand is parsed.
if not args or args[0].startswith("-") or args[0] not in allowed:
    print("git command rejected by fixture allowlist", file=sys.stderr)
    raise SystemExit(finish("rejected", 97, "mutation-or-network-or-unsupported"))
safe_env = {{key: value for key, value in os.environ.items() if not key.startswith("GIT_")}}
fixture_root = pathlib.Path(__file__).resolve().parent.parent
safe_env.update({{"HOME": str(fixture_root / "fixture-home"),
                 "XDG_CONFIG_HOME": str(fixture_root / "fixture-home/xdg"),
                 "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                 "GIT_CONFIG_SYSTEM": os.devnull, "GIT_ATTR_NOSYSTEM": "1",
                 "GIT_TEMPLATE_DIR": str(fixture_root / "empty-git-templates"),
                 "GIT_DEFAULT_HASH": "sha1", "GIT_TERMINAL_PROMPT": "0",
                 "GIT_CONFIG_COUNT": "3", "GIT_CONFIG_KEY_0": "core.hooksPath",
                 "GIT_CONFIG_VALUE_0": os.devnull, "GIT_CONFIG_KEY_1": "diff.external",
                 "GIT_CONFIG_VALUE_1": "", "GIT_CONFIG_KEY_2": "core.autocrlf",
                 "GIT_CONFIG_VALUE_2": "false"}})
exit_code = subprocess.call([{json.dumps(git_exe)}, *args], env=safe_env)
raise SystemExit(finish("allowed" if exit_code == 0 else "allowed-failed", exit_code, "local-read-only"))
'''.replace("import json, os, pathlib, sys", "import json, os, pathlib, subprocess, sys", 1)
    (stubs / "git").write_text(git_body)
    for name, message in (("gh", "GitHub access rejected by fixture"),
                          ("publish-check.py", "publication rejected by fixture")):
        body = ("#!/usr/bin/env python3\n" + record_code +
                f'print({json.dumps(message)}, file=sys.stderr)\n'
                'raise SystemExit(finish("rejected", 97, "publication-or-network"))\n')
        (stubs / name).write_text(body)
    for stub in stubs.iterdir():
        stub.chmod(0o755)

    print(root)


if __name__ == "__main__":
    main()
