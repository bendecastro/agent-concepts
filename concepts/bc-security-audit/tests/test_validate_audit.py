"""Contract tests for validate_audit; never imports or executes the audit fixture."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "validate_audit", Path(__file__).parents[1] / "body" / "validate_audit.py")
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def unit():
    return dict(id="U1", surface="api#get", boundary="caller -> owner",
                subsystem="docs", attack_class="access control", status="covered",
                evidence=["api.py:10 owner binding reviewed"])


def finding(verdict="confirmed"):
    common = dict(id="F1", title="Owner binding", units=["U1"],
                  trace=["api.py:10 entry -> return"], verdict=verdict)
    branches = {
        "confirmed": dict(principal="A", resource="B's document", outcome="private read",
                          impact="high", severity="high", evidence=["source trace"],
                          remediation="Bind owner before return"),
        "needs_validation": dict(hypothesis="runtime scope mismatch",
                                 blockers=["No approval or sandbox"],
                                 validation_plan=["After approval, compare dummy owners in sandbox"]),
        "rejected": dict(reason="No concrete security outcome"),
    }
    return dict(common, **branches[verdict])


class ValidateAuditTests(unittest.TestCase):
    def test_accepts_all_three_verdicts(self):
        records = []
        for index, verdict in enumerate(audit.BRANCH):
            record = finding(verdict)
            record["id"] = f"F{index}"
            records.append(record)
        self.assertEqual(audit.validate(records, [unit()]), [])

    def test_severity_ceiling_entire_scale(self):
        for impact, impact_rank in audit.SCALE.items():
            for severity, severity_rank in audit.SCALE.items():
                with self.subTest(impact=impact, severity=severity):
                    record = dict(finding(), impact=impact, severity=severity)
                    self.assertEqual(bool(audit.validate([record], [unit()])),
                                     severity_rank > impact_rank)

    def test_nonconfirmed_severity_is_forbidden_even_null(self):
        for verdict in ("needs_validation", "rejected"):
            record = dict(finding(verdict), severity=None)
            self.assertTrue(audit.validate([record], [unit()]))

    def test_required_branch_fields(self):
        for verdict, fields in audit.BRANCH.items():
            for field in fields:
                with self.subTest(verdict=verdict, field=field):
                    record = finding(verdict)
                    del record[field]
                    self.assertTrue(audit.validate([record], [unit()]))

    def test_empty_blockers_plan_and_reason(self):
        for field, value in (("blockers", []), ("validation_plan", [" "])):
            self.assertTrue(audit.validate([dict(finding("needs_validation"), **{field: value})], [unit()]))
        self.assertTrue(audit.validate([dict(finding("rejected"), reason="")], [unit()]))

    def test_exactly_one_verdict(self):
        for verdict in (None, [], ["confirmed", "rejected"], "confirmed/rejected", "other"):
            self.assertTrue(audit.validate([dict(finding(), verdict=verdict)], [unit()]))

    def test_unique_ledger_ids_and_tuples(self):
        duplicate = dict(unit(), surface="other")
        self.assertTrue(audit.validate([], [unit(), duplicate]))
        duplicate = dict(unit(), id="U2")
        self.assertTrue(audit.validate([], [unit(), duplicate]))

    def test_out_of_scope_never_covered(self):
        excluded = dict(unit(), status="out_of_scope", reason="excluded", evidence=[])
        self.assertEqual(audit.validate([], [excluded]), [])
        for change in ({"covered": True}, {"status": ["out_of_scope", "covered"]}):
            self.assertTrue(audit.validate([], [dict(excluded, **change)]))
        self.assertTrue(audit.validate([], [dict(unit(), evidence=[])]))

    def test_references_and_finding_ids(self):
        self.assertTrue(audit.validate([dict(finding(), units=["unknown"])], [unit()]))
        self.assertTrue(audit.validate([finding(), finding()], [unit()]))

    def test_malformed_types_do_not_crash(self):
        for data in (None, {}, "bad", [None], [0]):
            self.assertTrue(audit.validate(data, [unit()]))
            self.assertTrue(audit.validate([], data))
        for field in finding():
            bad = copy.deepcopy(finding())
            bad[field] = {}
            self.assertTrue(audit.validate([bad], [unit()]))
        for field in unit():
            self.assertTrue(audit.validate([], [dict(unit(), **{field: {}})]))

    def test_cli_and_duplicate_json_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(audit.main([directory]), 1)
                (root / "findings.json").write_text("[]")
                (root / "coverage-ledger.json").write_text(json.dumps([unit()]))
                self.assertEqual(audit.main([directory]), 0)
                (root / "findings.json").write_text('[{"verdict":"confirmed","verdict":"rejected"}]')
                self.assertEqual(audit.main([directory]), 1)
                (root / "findings.json").write_text("{broken")
                self.assertEqual(audit.main([directory]), 1)


if __name__ == "__main__":
    unittest.main()
