#!/usr/bin/env python3
"""Check audit record consistency, not the truth of the underlying evidence."""
import argparse
import json
from pathlib import Path
import sys

SCALE = {name: rank for rank, name in enumerate(
    ("informational", "low", "medium", "high", "critical"))}
STATUSES = {"planned", "candidate", "covered", "blocked", "deferred", "out_of_scope"}
DIMENSIONS = ("surface", "boundary", "subsystem", "attack_class")
COMMON = {"id", "title", "units", "verdict", "trace"}
BRANCH = {
    "confirmed": {"principal", "resource", "outcome", "impact", "severity",
                  "evidence", "remediation"},
    "needs_validation": {"hypothesis", "blockers", "validation_plan"},
    "rejected": {"reason"},
}


def text(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value):
    return isinstance(value, list) and bool(value) and all(map(text, value))


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=unique_object)


def validate(findings, ledger):
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    if not isinstance(findings, list) or not isinstance(ledger, list):
        return ["findings.json and coverage-ledger.json must each contain an array"]
    unit_ids, tuples = set(), set()
    for index, unit in enumerate(ledger):
        label = f"ledger[{index}]"
        if not isinstance(unit, dict):
            errors.append(f"{label}: expected object")
            continue
        required = {"id", "status", "evidence", *DIMENSIONS}
        require(required <= unit.keys(), f"{label}: missing required fields")
        require(not (unit.keys() - required - {"reason"}),
                f"{label}: unknown fields (use one status, no covered flag)")
        uid = unit.get("id")
        require(text(uid), f"{label}: id must be a nonempty string")
        if text(uid):
            require(uid not in unit_ids, f"{label}: duplicate ledger id {uid}")
            unit_ids.add(uid)
        values = tuple(unit.get(key) for key in DIMENSIONS)
        require(all(map(text, values)), f"{label}: dimensions must be nonempty strings")
        if all(map(text, values)):
            require(values not in tuples, f"{label}: duplicate coverage tuple")
            tuples.add(values)
        status = unit.get("status")
        require(isinstance(status, str) and status in STATUSES,
                f"{label}: status must be exactly one of {sorted(STATUSES)}")
        evidence = unit.get("evidence")
        require(isinstance(evidence, list) and all(map(text, evidence)),
                f"{label}: evidence must be an array of nonempty strings")
        if status == "covered":
            require(strings(evidence), f"{label}: covered requires evidence")
        if status in ("blocked", "deferred", "out_of_scope"):
            require(text(unit.get("reason")), f"{label}: {status} requires reason")

    finding_ids = set()
    for index, finding in enumerate(findings):
        label = f"findings[{index}]"
        if not isinstance(finding, dict):
            errors.append(f"{label}: expected object")
            continue
        fid = finding.get("id")
        require(text(fid), f"{label}: id must be a nonempty string")
        if text(fid):
            require(fid not in finding_ids, f"{label}: duplicate finding id {fid}")
            finding_ids.add(fid)
        for field in ("title",):
            require(text(finding.get(field)), f"{label}: {field} must be nonempty")
        for field in ("units", "trace"):
            require(strings(finding.get(field)), f"{label}: {field} must be a nonempty string array")
        if strings(finding.get("units")):
            for uid in finding["units"]:
                require(uid in unit_ids, f"{label}: unknown ledger unit {uid}")
        verdict = finding.get("verdict")
        if not isinstance(verdict, str) or verdict not in BRANCH:
            errors.append(f"{label}: verdict must be exactly one of {sorted(BRANCH)}")
            continue
        allowed = COMMON | BRANCH[verdict]
        require(not (finding.keys() - allowed), f"{label}: fields not allowed for {verdict}")
        require(allowed <= finding.keys(), f"{label}: missing fields for {verdict}")
        if verdict != "confirmed":
            require("severity" not in finding, f"{label}: severity only allowed on confirmed")
        if verdict == "confirmed":
            for field in ("principal", "resource", "outcome", "remediation"):
                require(text(finding.get(field)), f"{label}: {field} must be nonempty")
            require(strings(finding.get("evidence")), f"{label}: confirmed requires evidence")
            impact, severity = finding.get("impact"), finding.get("severity")
            valid_impact = isinstance(impact, str) and impact in SCALE
            valid_severity = isinstance(severity, str) and severity in SCALE
            require(valid_impact, f"{label}: impact must be one of {list(SCALE)}")
            require(valid_severity, f"{label}: severity must be one of {list(SCALE)}")
            if valid_impact and valid_severity:
                require(SCALE[severity] <= SCALE[impact],
                        f"{label}: severity exceeds demonstrated impact")
        elif verdict == "needs_validation":
            require(text(finding.get("hypothesis")), f"{label}: hypothesis must be nonempty")
            require(strings(finding.get("blockers")), f"{label}: needs_validation requires blockers")
            require(strings(finding.get("validation_plan")),
                    f"{label}: needs_validation requires validation_plan")
        else:
            require(text(finding.get("reason")), f"{label}: rejected requires reason")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args(argv)
    try:
        errors = validate(load(args.run_dir / "findings.json"),
                          load(args.run_dir / "coverage-ledger.json"))
    except (OSError, ValueError, RecursionError) as exc:
        print(f"audit validation: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Audit records valid (consistency only; not evidence verification).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
