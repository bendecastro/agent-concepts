"""work_index.py: the generated pipeline table in a visible-layout project's work/README.md."""
from pathlib import Path
import subprocess
import sys

SCRIPT = Path(__file__).resolve().parents[1] / "body/work_index.py"
README = "# Work\n\nIntro.\n\n<!-- work-index:start -->\n<!-- work-index:end -->\n"
STAGES_AGENTS = "# demo\n\n## Work items\n\nStages: v1, v1.x, stage 1, stage 2, stage 4, unscheduled\n"


def item(stage, why, steps="- [ ] one\n"):
    return f"# Title\n\nWhy: {why}\nDone when: x.\nStage: {stage}\n\n## Steps\n\n{steps}\n## Outcome\n"


def fixture(root, files, agents=STAGES_AGENTS):
    all_files = {"work/README.md": README, "work/0-ideas.md": "# Ideas\n\n- a\n- b\n", **files}
    if agents is not None:
        all_files[".bc-agent/AGENTS.md"] = agents
    for path, text in all_files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text)
    return root


def run(root, *args):
    return subprocess.run([sys.executable, str(SCRIPT), *args, str(root / "work")],
                          capture_output=True, text=True)


def readme(root):
    return (root / "work/README.md").read_bytes().decode()


def rows(root):
    return [line for line in readme(root).splitlines() if line.startswith("| ") and not line.startswith(("| Stage", "| ---"))]


def test_table_is_ordered_by_stages_line_then_number(tmp_path):
    fixture(tmp_path, {
        "work/1-planned/009-ai.md": item("stage 4", "Smart. Second sentence."),
        "work/1-planned/007-unsched.md": item("unscheduled", "Later."),
        "work/1-planned/005-columns/plan.md": item("stage 2", "See [ADR](../x.md) for a | b.", "- [x] a\n- [ ] b\n- [X] c\n"),
        "work/2-active/001-v1/plan.md": item("v1", "Ship it."),
        "work/1-planned/006-mobile.md": item("v1.x", "Phones."),
        "work/1-planned/004-more.md": item("stage 2", "More."),
    })
    result = run(tmp_path)
    assert result.returncode == 0, result.stderr
    assert rows(tmp_path) == [
        "| v1 | [001-v1](2-active/001-v1/plan.md) | active | Ship it. | 0/1 |",
        "| v1.x | [006-mobile](1-planned/006-mobile.md) | planned | Phones. | 0/1 |",
        "| stage 2 | [004-more](1-planned/004-more.md) | planned | More. | 0/1 |",
        "| stage 2 | [005-columns](1-planned/005-columns/plan.md) | planned | See ADR for a \\| b. | 2/3 |",
        "| stage 4 | [009-ai](1-planned/009-ai.md) | planned | Smart. | 0/1 |",
        "| unscheduled | [007-unsched](1-planned/007-unsched.md) | planned | Later. | 0/1 |",
    ]
    assert readme(tmp_path).startswith("# Work\n\nIntro.\n\n<!-- work-index:start -->\n")
    assert "| Stage | Item | Folder | Why | Steps |" in readme(tmp_path)


def test_default_stages_when_agents_has_no_stages_line(tmp_path):
    fixture(tmp_path, {
        "work/1-planned/003-c.md": item("unscheduled", "C."),
        "work/1-planned/002-b.md": item("later", "B."),
        "work/1-planned/001-a.md": item("next", "A."),
        "work/2-active/004-d.md": item("now", "D."),
    }, agents="# demo\n\nNo stages here.\n")
    assert run(tmp_path).returncode == 0
    assert [row.split(" | ")[0] for row in rows(tmp_path)] == ["| now", "| next", "| later", "| unscheduled"]


def test_default_stages_when_agents_file_is_absent(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": item("now", "A.")}, agents=None)
    assert run(tmp_path).returncode == 0
    assert rows(tmp_path)[0].startswith("| now |")


def test_first_why_sentence_keeps_abbreviations_code_and_nested_links(tmp_path):
    fixture(tmp_path, {"work/1-planned/004-x.md": item(
        "v1", "Tags, e.g. work vs. home, i.e. both, and `a. B` use [a link](https://w/a_(b)). Next.")})
    assert run(tmp_path).returncode == 0
    assert "| Tags, e.g. work vs. home, i.e. both, and `a. B` use a link. | 0/1 |" in readme(tmp_path)
    assert "Next." not in readme(tmp_path)


def test_long_why_is_capped_with_ellipsis(tmp_path):
    fixture(tmp_path, {"work/1-planned/004-x.md": item("v1", "a" * 180)})
    assert run(tmp_path).returncode == 0
    assert "| " + "a" * 159 + "… | 0/1 |" in readme(tmp_path)


def test_dash_for_item_with_no_steps(tmp_path):
    fixture(tmp_path, {"work/1-planned/004-x.md": item("v1", "X.", "Not planned yet.")})
    assert run(tmp_path).returncode == 0
    assert "| X. | — |" in readme(tmp_path)


def test_folder_item_without_plan_is_a_clear_error(tmp_path):
    fixture(tmp_path, {"work/1-planned/004-x/other.md": "x"})
    result = run(tmp_path)
    assert result.returncode == 1
    assert result.stderr.strip() == "work-index: 1-planned/004-x/plan.md: missing"


def test_missing_stage_line_is_a_clear_error(tmp_path):
    fixture(tmp_path, {"work/1-planned/004-x.md": "# Title\nWhy: X.\n"})
    result = run(tmp_path)
    assert result.returncode == 1
    assert "1-planned/004-x.md: missing or unknown Stage line" in result.stderr
    assert "v1, v1.x, stage 1" in result.stderr


def test_unknown_stage_is_a_clear_error(tmp_path):
    fixture(tmp_path, {"work/1-planned/004-x.md": item("stage 9", "X.")})
    result = run(tmp_path)
    assert result.returncode == 1
    assert "004-x" in result.stderr and "Stage" in result.stderr
    assert "Traceback" not in result.stderr


def test_counts_ideas_done_month_folders_and_dropped(tmp_path):
    fixture(tmp_path, {
        "work/3-done/003-a.md": "x",
        "work/3-done/2026-11/002-b/plan.md": "x",
        "work/3-done/2026-11/008-c.md": "x",
        "work/3-done/.gitkeep": "",
        "work/4-dropped/010-d.md": "x",
        "work/4-dropped/.gitkeep": "",
    })
    assert run(tmp_path).returncode == 0
    text = readme(tmp_path)
    assert "- [Ideas](0-ideas.md): 2" in text
    assert "- [Done](3-done/): 3" in text
    assert "- [Dropped](4-dropped/): 1" in text


def test_check_fails_while_stale_and_passes_after_writing(tmp_path):
    fixture(tmp_path, {"work/1-planned/004-x.md": item("v1", "X.")})
    stale = run(tmp_path, "--check")
    assert stale.returncode == 1
    assert "out of date" in stale.stderr
    assert readme(tmp_path) == README
    assert run(tmp_path).returncode == 0
    assert run(tmp_path, "--check").returncode == 0


def test_check_tolerates_crlf_and_write_produces_lf(tmp_path):
    fixture(tmp_path, {"work/1-planned/004-x.md": item("v1", "X.")})
    assert run(tmp_path).returncode == 0
    (tmp_path / "work/README.md").write_bytes(readme(tmp_path).replace("\n", "\r\n").encode())
    assert run(tmp_path, "--check").returncode == 0
    (tmp_path / "work/0-ideas.md").write_text("- changed\n")
    assert run(tmp_path).returncode == 0
    assert "\r" not in readme(tmp_path)


def test_crlf_item_is_read(tmp_path):
    fixture(tmp_path, {})
    path = tmp_path / "work/1-planned/004-x.md"
    path.parent.mkdir(parents=True)
    path.write_bytes(item("v1", "X.", "- [x] a\n- [ ] b\n").replace("\n", "\r\n").encode())
    assert run(tmp_path).returncode == 0
    assert "| v1 | [004-x](1-planned/004-x.md) | planned | X. | 1/2 |" in readme(tmp_path)


def test_missing_markers_are_a_clear_error(tmp_path):
    fixture(tmp_path, {"work/README.md": "# Work\n"})
    result = run(tmp_path)
    assert result.returncode == 1
    assert "markers" in result.stderr


def test_second_run_is_byte_identical(tmp_path):
    fixture(tmp_path, {"work/1-planned/004-x.md": item("v1", "X."), "work/1-planned/002-y.md": item("v1", "Y.")})
    assert run(tmp_path).returncode == 0
    first = readme(tmp_path)
    assert run(tmp_path).returncode == 0
    assert readme(tmp_path) == first
    assert "work_index.py" in first


def test_default_work_dir_is_the_project_next_to_bc_agent_scripts(tmp_path):
    fixture(tmp_path, {"work/1-planned/004-x.md": item("v1", "X.")})
    (tmp_path / ".bc-agent/scripts").mkdir()
    copy = tmp_path / ".bc-agent/scripts/work_index.py"
    copy.write_bytes(SCRIPT.read_bytes())
    result = subprocess.run([sys.executable, str(copy)], capture_output=True, text=True, cwd="/")
    assert result.returncode == 0, result.stderr
    assert "[004-x](1-planned/004-x.md)" in readme(tmp_path)


def test_reports_all_invalid_stages(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": item("bad", "A."),
                       "work/2-active/002-b.md": "# No stage\n"})
    result = run(tmp_path, "--check")
    assert result.returncode == 1
    assert "1-planned/001-a.md" in result.stderr
    assert "2-active/002-b.md" in result.stderr


def test_non_utf8_item_is_a_clear_error(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": "placeholder"})
    (tmp_path / "work/1-planned/001-a.md").write_bytes(b"\xff")
    result = run(tmp_path)
    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    assert "utf-8" in result.stderr


def test_handwritten_tail_survives_two_runs_and_check(tmp_path):
    tail = b'\n\n- Open questions: [PRD](../docs/PRD.md)\n'
    fixture(tmp_path, {"work/1-planned/004-x.md": item("v1", "X.")})
    path = tmp_path / "work/README.md"
    path.write_bytes(README.encode() + tail)
    for _ in range(2):
        assert run(tmp_path).returncode == 0
        assert path.read_bytes().endswith(tail)
    assert run(tmp_path, "--check").returncode == 0
    assert path.read_bytes().endswith(tail)
