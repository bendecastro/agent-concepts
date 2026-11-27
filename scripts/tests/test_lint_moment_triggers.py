"""Named moments in deployed bodies require a directed trigger in the graph."""

import json
from pathlib import Path
import sys

from hypothesis import HealthCheck, given, settings, strategies as st
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import lint


SETUP = "bc-setup-project"
TARGET = "fixture-check"


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    monkeypatch.setattr(lint, "ROOT", tmp_path)

    def concept(name, body, deployed="2026-11-27", filename="SKILL.md"):
        directory = tmp_path / "concepts" / name
        path = directory / "body" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        (directory / "CONCEPT.md").write_text(f"---\ndeployed: {deployed}\n---\n", encoding="utf-8")
        path.write_text(body, encoding="utf-8")

    def check(edges=()):
        (tmp_path / lint.relationships.GRAPH_PATH).write_text(
            json.dumps({"schema": 1, "edges": list(edges)}), encoding="utf-8"
        )
        parsed, errors = lint.relationships.load_graph(tmp_path)
        assert not errors
        lint.relationships.write_views(tmp_path, parsed)
        issues = []
        lint.lint_relationships(issues)
        return issues

    concept(SETUP, f"Offer {TARGET}.\n")
    concept(TARGET, f"From {SETUP}.\nRun at project setup.\n")
    return concept, check


def test_warns_without_trigger(workspace):
    _, check = workspace
    issues = check()
    assert [issue.severity for issue in issues] == ["WARN"]
    message = issues[0].message
    assert f"concepts/{TARGET}/body/SKILL.md:2:" in message
    assert "at project setup" in message
    assert SETUP in message


def edge(source, target, relation, required=False):
    return {"from": source, "to": target, "relation": relation, "required": required,
            "source": f"concepts/{source}/body/SKILL.md", "reason": "Fixture edge."}


@pytest.mark.parametrize("relation", ["hands_off", "loads"])
def test_accepts_matching_trigger_edge(workspace, relation):
    _, check = workspace
    assert check([edge(SETUP, TARGET, relation)]) == []


def test_allow_comment_applies_only_to_its_line(workspace):
    concept, check = workspace
    concept(TARGET, "During setup, run this. <!-- trigger-allow: owner runs it manually -->\n"
                    "Run at project setup, too.\n")
    issues = check()
    assert [issue.severity for issue in issues] == ["WARN"]
    assert f"concepts/{TARGET}/body/SKILL.md:2:" in issues[0].message


@pytest.mark.parametrize("suffix", [" trigger-allow: manual", " <!-- trigger-allow: -->"])
def test_allow_requires_html_comment_with_reason(workspace, suffix):
    concept, check = workspace
    concept(TARGET, f"Run during setup.{suffix}\n")
    assert [issue.severity for issue in check()] == ["WARN"]


def test_exempts_moment_owners_own_body(workspace):
    concept, check = workspace
    concept(SETUP, "At project setup, do this.\n")
    concept(TARGET, "Nothing to check.\n")
    assert check() == []


def test_ignores_undeployed_body(workspace):
    concept, check = workspace
    concept(TARGET, "At project setup, do this.\n", deployed="no")
    assert check() == []


@pytest.mark.parametrize(("phrase", "owner"), [
    ("BEFORE PLANNING", "bc-plan-to-pipeline"),
    ("When planning", "bc-plan-to-pipeline"),
    ("during a drain", "bc-pipeline-to-done"),
    ("while draining", "bc-pipeline-to-done"),
])
def test_checks_nested_bodies_and_reports_the_phrase_as_written(workspace, phrase, owner):
    concept, check = workspace
    concept(TARGET, "Nothing to check.\n")
    concept(TARGET, f"# Reference\n\nRun {phrase}.\n", filename="refs/notes.md")
    issues = check()
    assert [issue.severity for issue in issues] == ["WARN"]
    assert f"concepts/{TARGET}/body/refs/notes.md:3:" in issues[0].message
    assert phrase in issues[0].message
    assert owner in issues[0].message


# `check` rewrites the graph and its views on every example; the bodies are fixed.
@settings(database=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(relation=st.sampled_from(["loads", "hands_off", "adapts", "depends_on_contract"]),
       required=st.booleans(), reversed_edge=st.booleans())
def test_only_a_forward_load_or_handoff_satisfies_the_moment(workspace, relation, required, reversed_edge):
    _, check = workspace
    source, target = (TARGET, SETUP) if reversed_edge else (SETUP, TARGET)
    issues = check([edge(source, target, relation, required)])
    linked = not reversed_edge and relation in {"hands_off", "loads"}
    assert [issue.severity for issue in issues] == ([] if linked else ["WARN"])
