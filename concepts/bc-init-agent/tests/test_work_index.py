"""work_index.py: the generated pipeline table in a visible-layout project's work/README.md."""
from pathlib import Path
import subprocess
import sys

SCRIPT = Path(__file__).resolve().parents[1] / "body/work_index.py"
README = "# Work\n\nIntro.\n\n<!-- work-index:start -->\n<!-- work-index:end -->\n"
STAGES_AGENTS = "# demo\n\n## Work items\n\nStages: v1, v1.x, stage 1, stage 2, stage 4, unscheduled\n"


def item(stage, why, steps="- [ ] one\n", blocked_by="nothing", kind=None):
    blocked = "" if blocked_by is None else f"Blocked by: {blocked_by}\n"
    stage_line = "" if stage is None else f"Stage: {stage}\n"
    kind_line = "" if kind is None else f"Kind: {kind}\n"
    return f"# Title\n\nWhy: {why}\nDone when: x.\n{stage_line}{kind_line}{blocked}\n## Steps\n\n{steps}\n## Outcome\n"


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
    return [line for line in readme(root).splitlines() if line.startswith("| ") and not line.startswith(("| #", "| ---"))]


def names(root):
    return [row.split("[", 1)[1].split("]", 1)[0] for row in rows(root)]


def test_unblocked_items_are_ordered_active_then_by_stages_line_then_number(tmp_path):
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
        "| 1 | [001-v1](2-active/001-v1/plan.md) | active | — | — | Ship it. | 0/1 |",
        "| 2 | [006-mobile](1-planned/006-mobile.md) | planned | — | — | Phones. | 0/1 |",
        "| 3 | [004-more](1-planned/004-more.md) | planned | — | — | More. | 0/1 |",
        "| 4 | [005-columns](1-planned/005-columns/plan.md) | planned | — | — | See ADR for a \\| b. | 2/3 |",
        "| 5 | [009-ai](1-planned/009-ai.md) | planned | — | — | Smart. | 0/1 |",
        "| 6 | [007-unsched](1-planned/007-unsched.md) | planned | — | — | Later. | 0/1 |",
    ]
    assert readme(tmp_path).startswith("# Work\n\nIntro.\n\n<!-- work-index:start -->\n")
    assert "| # | Item | Folder | Waits on | Unblocks | Why | Steps |" in readme(tmp_path)


def test_default_stages_when_agents_has_no_stages_line(tmp_path):
    fixture(tmp_path, {
        "work/1-planned/003-c.md": item("unscheduled", "C."),
        "work/1-planned/002-b.md": item("later", "B."),
        "work/1-planned/001-a.md": item("next", "A."),
        "work/2-active/004-d.md": item("now", "D."),
    }, agents="# demo\n\nNo stages here.\n")
    assert run(tmp_path).returncode == 0
    assert names(tmp_path) == ["004-d", "001-a", "002-b", "003-c"]


def test_default_stages_when_agents_file_is_absent(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": item("now", "A.")}, agents=None)
    assert run(tmp_path).returncode == 0
    assert names(tmp_path) == ["001-a"]


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


def test_item_without_stage_line_sorts_after_every_stage(tmp_path):
    fixture(tmp_path, {
        "work/1-planned/001-nostage.md": item(None, "No stage."),
        "work/1-planned/002-unsched.md": item("unscheduled", "Later."),
        "work/1-planned/003-v1.md": item("v1", "Soon."),
    })
    result = run(tmp_path)
    assert result.returncode == 0, result.stderr
    assert names(tmp_path) == ["003-v1", "002-unsched", "001-nostage"]


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
    assert "| 1 | [004-x](1-planned/004-x.md) | planned | — | — | X. | 1/2 |" in readme(tmp_path)


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


def test_missing_blocked_by_line_is_a_clear_error(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": item("v1", "A.", blocked_by=None)})
    result = run(tmp_path)
    assert result.returncode == 1
    assert "1-planned/001-a.md: missing Blocked by line" in result.stderr


def test_blocked_by_unknown_item_is_an_error(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": item("v1", "A.", blocked_by="099-ghost")})
    result = run(tmp_path)
    assert result.returncode == 1
    assert "1-planned/001-a.md: Blocked by names unknown item 099-ghost" in result.stderr


def test_blocked_by_dropped_item_is_an_error(tmp_path):
    fixture(tmp_path, {"work/4-dropped/002-gone.md": "x",
                       "work/1-planned/001-a.md": item("v1", "A.", blocked_by="002-gone")})
    result = run(tmp_path)
    assert result.returncode == 1
    assert "Blocked by names dropped item 002-gone" in result.stderr


def test_blocked_by_itself_is_an_error(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": item("v1", "A.", blocked_by="001-a")})
    result = run(tmp_path)
    assert result.returncode == 1
    assert "names the item itself" in result.stderr


def test_blocked_by_cycle_is_an_error(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": item("v1", "A.", blocked_by="002-b"),
                       "work/1-planned/002-b/plan.md": item("v1", "B.", blocked_by="001-a")})
    result = run(tmp_path)
    assert result.returncode == 1
    assert "dependency cycle: 001-a -> 002-b -> 001-a" in result.stderr


def test_done_blocker_is_satisfied(tmp_path):
    fixture(tmp_path, {"work/3-done/2026-01/005-old/plan.md": "x",
                       "work/1-planned/001-a.md": item("v1", "A.", blocked_by="005-old")})
    assert run(tmp_path).returncode == 0
    assert "| 1 | [001-a](1-planned/001-a.md) | planned | — | — | A. | 0/1 |" in readme(tmp_path)


def test_items_that_unblock_most_come_first(tmp_path):
    fixture(tmp_path, {
        "work/1-planned/001-few.md": item("v1", "F."),
        "work/1-planned/002-many.md": item("v1", "M."),
        "work/1-planned/003-x.md": item("v1", "X.", blocked_by="002-many"),
        "work/1-planned/004-y.md": item("v1", "Y.", blocked_by="003-x"),
        "work/1-planned/005-z.md": item("v1", "Z.", blocked_by="001-few"),
    })
    assert run(tmp_path).returncode == 0
    assert names(tmp_path) == ["002-many", "001-few", "003-x", "004-y", "005-z"]


def test_blocked_item_follows_its_blocker_despite_an_earlier_stage(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-late.md": item("unscheduled", "L."),
                       "work/1-planned/002-early.md": item("v1", "E.", blocked_by="001-late")})
    assert run(tmp_path).returncode == 0
    assert names(tmp_path) == ["001-late", "002-early"]


def test_waits_on_and_unblocks_columns(tmp_path):
    fixture(tmp_path, {
        "work/1-planned/001-a.md": item("v1", "A."),
        "work/1-planned/002-b.md": item("v1", "B.", blocked_by="001-a"),
        "work/1-planned/003-c/plan.md": item("v1", "C.", blocked_by="001-a, 002-b"),
    })
    assert run(tmp_path).returncode == 0
    assert rows(tmp_path) == [
        "| 1 | [001-a](1-planned/001-a.md) | planned | — | 002-b, 003-c | A. | 0/1 |",
        "| 2 | [002-b](1-planned/002-b.md) | planned | [001-a](1-planned/001-a.md) | 003-c | B. | 0/1 |",
        "| 3 | [003-c](1-planned/003-c/plan.md) | planned | [001-a](1-planned/001-a.md), [002-b](1-planned/002-b.md) | — | C. | 0/1 |",
    ]


ORDER_HEADER = "# Order\n\nThe owner's ranking of open work items, top first.\n\n"


def test_owner_order_ranks_items_without_dependencies(tmp_path):
    fixture(tmp_path, {
        "work/1-planned/001-a.md": item("v1", "A."),
        "work/1-planned/002-b.md": item("v1", "B."),
        "work/1-planned/003-c.md": item("unscheduled", "C."),
        "work/1-planned/004-d.md": item("v1", "D."),
        "work/order.md": ORDER_HEADER + "1. 003-c\n2. 002-b\n",
    })
    assert run(tmp_path).returncode == 0
    assert names(tmp_path) == ["003-c", "002-b", "001-a", "004-d"]


def test_active_items_precede_owner_order(tmp_path):
    fixture(tmp_path, {
        "work/1-planned/001-a.md": item("v1", "A."),
        "work/2-active/002-b.md": item("v1", "B."),
        "work/order.md": "1. 001-a\n2. 002-b\n",
    })
    assert run(tmp_path).returncode == 0
    assert names(tmp_path) == ["002-b", "001-a"]


def test_blockers_override_owner_order(tmp_path):
    fixture(tmp_path, {
        "work/1-planned/001-a.md": item("v1", "A."),
        "work/1-planned/002-b.md": item("v1", "B.", blocked_by="001-a"),
        "work/1-planned/003-c.md": item("v1", "C."),
        "work/order.md": "1. 002-b\n2. 003-c\n",
    })
    assert run(tmp_path).returncode == 0
    assert names(tmp_path) == ["003-c", "001-a", "002-b"]


def test_owner_order_ignores_closed_items_and_other_lines(tmp_path):
    fixture(tmp_path, {
        "work/3-done/2026-11/005-old.md": "x",
        "work/4-dropped/006-gone.md": "x",
        "work/1-planned/001-a.md": item("v1", "A."),
        "work/1-planned/002-b.md": item("v1", "B."),
        "work/order.md": ORDER_HEADER + "1. 005-old\n2. 006-gone\n- 001-a\n3. 002-b\n",
    })
    result = run(tmp_path)
    assert result.returncode == 0, result.stderr
    assert names(tmp_path) == ["002-b", "001-a"]


def test_owner_order_unknown_name_is_an_error(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": item("v1", "A."),
                       "work/order.md": "1. 099-ghost\n"})
    result = run(tmp_path)
    assert result.returncode == 1
    assert "order.md: names unknown item 099-ghost" in result.stderr


def test_owner_order_duplicate_name_is_an_error(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": item("v1", "A."),
                       "work/order.md": "1. 001-a\n2. 001-a\n"})
    result = run(tmp_path)
    assert result.returncode == 1
    assert "order.md: names 001-a more than once" in result.stderr


def test_repeated_closed_names_are_ignored(tmp_path):
    fixture(tmp_path, {"work/3-done/005-old.md": "x", "work/4-dropped/006-gone.md": "x",
                       "work/order.md": "1. 005-old\n2. 005-old\n3. 006-gone\n4. 006-gone\n"})
    result = run(tmp_path)
    assert result.returncode == 0, result.stderr


def test_owner_rank_precedes_readiness(tmp_path):
    fixture(tmp_path, {"work/2-active/001-a.md": item("v1", "A."),
                       "work/1-planned/002-b.md": item("v1", "B.", blocked_by="001-a"),
                       "work/1-planned/003-c.md": item("v1", "C."),
                       "work/order.md": "1. 002-b\n"})
    assert run(tmp_path).returncode == 0
    assert names(tmp_path) == ["001-a", "002-b", "003-c"]


def test_transitive_blockers_override_owner_rank(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": item("v1", "A."),
                       "work/1-planned/002-b.md": item("v1", "B.", blocked_by="001-a"),
                       "work/1-planned/003-c.md": item("v1", "C.", blocked_by="002-b"),
                       "work/order.md": "1. 003-c\n"})
    assert run(tmp_path).returncode == 0
    assert names(tmp_path) == ["001-a", "002-b", "003-c"]


def test_closed_name_repetition_property():
    from hypothesis import given, settings, strategies as st
    from tempfile import TemporaryDirectory

    @settings(deadline=None)
    @given(st.sampled_from(["3-done", "4-dropped"]), st.integers(min_value=2, max_value=20))
    def check(folder, count):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root, {f"work/{folder}/005-old.md": "x",
                           "work/order.md": "".join(f"{i}. 005-old\n" for i in range(1, count + 1))})
            result = run(root)
            assert result.returncode == 0, result.stderr
    check()


def owner_order_case(draw):
    from hypothesis import strategies as st
    count = draw(st.integers(min_value=1, max_value=7))
    item_names = [f"{n:03d}-i{n}" for n in range(1, count + 1)]
    with_blockers = draw(st.booleans())
    blockers = {n: (sorted(draw(st.sets(st.sampled_from(item_names[:k]), max_size=3))) if with_blockers and k else [])
                for k, n in enumerate(item_names)}
    folders = {n: draw(st.sampled_from(["1-planned", "2-active"])) for n in item_names}
    listed = draw(st.permutations(item_names))[:draw(st.integers(min_value=0, max_value=count))]
    return item_names, blockers, folders, listed


def transitive_blockers(blockers, name):
    found, stack = set(), list(blockers[name])
    while stack:
        b = stack.pop()
        if b not in found:
            found.add(b)
            stack.extend(blockers[b])
    return found


def test_owner_order_property():
    from hypothesis import given, settings, strategies as st
    from tempfile import TemporaryDirectory

    @settings(deadline=None, max_examples=60)
    @given(st.composite(owner_order_case)())
    def check(case):
        item_names, blockers, folders, listed = case
        with TemporaryDirectory() as directory:
            root = Path(directory)
            files = {f"work/{folders[n]}/{n}.md": item("v1", "W.", blocked_by=", ".join(blockers[n]) or "nothing")
                     for n in item_names}
            files["work/order.md"] = ORDER_HEADER + "".join(f"{k}. {n}\n" for k, n in enumerate(listed, 1))
            fixture(root, files)
            result = run(root)
            assert result.returncode == 0, result.stderr
            placed = names(root)
        assert sorted(placed) == item_names
        position = {n: k for k, n in enumerate(placed)}
        for n in item_names:
            assert all(position[b] < position[n] for b in blockers[n]), (n, placed)
        active = [n for n in item_names if folders[n] == "2-active"]
        feeds_active = set().union(*(transitive_blockers(blockers, a) for a in active))
        for a in active:
            for p in item_names:
                if folders[p] == "1-planned" and p not in feeds_active:
                    assert position[a] < position[p], (a, p, placed)
            if not blockers[a]:
                assert all(position[a] < position[p] for p in item_names if folders[p] == "1-planned"), (a, placed)
        if not any(blockers.values()):
            planned = [n for n in placed if folders[n] == "1-planned"]
            ranked = [n for n in listed if folders[n] == "1-planned"]
            assert planned[:len(ranked)] == ranked, (listed, placed)
    check()


def test_blockers_of_active_items_precede_other_planned_items(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-p1.md": item("v1", "P1."),
                       "work/1-planned/002-p2.md": item("v1", "P2."),
                       "work/1-planned/003-q.md": item("v1", "Q."),
                       "work/2-active/004-a1.md": item("v1", "A1.", blocked_by="001-p1"),
                       "work/2-active/005-a2.md": item("v1", "A2.", blocked_by="002-p2"),
                       "work/order.md": "1. 003-q\n"})
    assert run(tmp_path).returncode == 0
    assert names(tmp_path).index("003-q") > max(names(tmp_path).index(n) for n in ("001-p1", "002-p2"))


def test_blockers_of_active_items_lead_without_an_order_file(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-unrelated.md": item("v1", "U."),
                       "work/1-planned/002-blocker.md": item("v1", "B."),
                       "work/2-active/003-active.md": item("v1", "A.", blocked_by="002-blocker"),
                       "work/1-planned/004-later.md": item("v1", "L.", blocked_by="001-unrelated")})
    assert run(tmp_path).returncode == 0
    assert names(tmp_path) == ["002-blocker", "003-active", "001-unrelated", "004-later"]


def test_ready_active_item_precedes_ranked_blocker_of_another_active_item(tmp_path):
    fixture(tmp_path, {"work/2-active/001-ready.md": item("v1", "R."),
                       "work/2-active/002-waiting.md": item("v1", "W.", blocked_by="003-blocker"),
                       "work/1-planned/003-blocker.md": item("v1", "B."),
                       "work/order.md": "1. 003-blocker\n2. 002-waiting\n3. 001-ready\n"})
    assert run(tmp_path).returncode == 0
    assert names(tmp_path) == ["001-ready", "003-blocker", "002-waiting"]


def test_owner_order_skips_items_in_dropped_month_folders(tmp_path):
    fixture(tmp_path, {"work/4-dropped/2026-11/005-old.md": "x",
                       "work/1-planned/001-a.md": item("v1", "A."),
                       "work/order.md": "1. 005-old\n2. 001-a\n"})
    result = run(tmp_path)
    assert result.returncode == 0, result.stderr
    assert names(tmp_path) == ["001-a"]
    assert "- [Dropped](4-dropped/): 1" in readme(tmp_path)


def test_open_item_wins_over_closed_item_with_the_same_name(tmp_path):
    fixture(tmp_path, {"work/4-dropped/2026-11/002-b.md": "x",
                       "work/1-planned/001-a.md": item("v1", "A."),
                       "work/1-planned/002-b.md": item("v1", "B."),
                       "work/order.md": "1. 002-b\n2. 002-b\n"})
    result = run(tmp_path)
    assert result.returncode == 1
    assert "order.md: names 002-b more than once" in result.stderr


def test_owner_order_digits_are_ascii_only(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": item("v1", "A."),
                       "work/1-planned/002-b.md": item("v1", "B."),
                       "work/order.md": "\u0661. 002-b\n"})
    assert run(tmp_path).returncode == 0
    assert names(tmp_path) == ["001-a", "002-b"]


def test_owner_order_trailing_nbsp_is_part_of_the_name(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": item("v1", "A."),
                       "work/1-planned/002-b.md": item("v1", "B."),
                       "work/order.md": "1. 002-b\u00a0\n"})
    result = run(tmp_path)
    assert result.returncode == 1
    assert "order.md: names unknown item 002-b\u00a0" in result.stderr


def test_owner_order_cr_only_file_is_read(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": item("v1", "A."),
                       "work/1-planned/002-b.md": item("v1", "B.")})
    (tmp_path / "work/order.md").write_bytes(b"1. 002-b\r2. 001-a\r")
    result = run(tmp_path)
    assert result.returncode == 0, result.stderr
    assert names(tmp_path) == ["002-b", "001-a"]


def test_owner_order_lines_split_only_on_cr_and_lf(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": item("v1", "A."),
                       "work/1-planned/002-b.md": item("v1", "B."),
                       "work/order.md": "1. 002-b\u20282. 001-a\n"})
    result = run(tmp_path)
    assert result.returncode == 0, result.stderr
    assert names(tmp_path) == ["001-a", "002-b"]


def test_ranked_leaf_precedes_unranked_item_that_unblocks_more(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-hub.md": item("v1", "H."),
                       "work/1-planned/002-x.md": item("v1", "X.", blocked_by="001-hub"),
                       "work/1-planned/003-y.md": item("v1", "Y.", blocked_by="001-hub"),
                       "work/1-planned/004-leaf.md": item("v1", "L."),
                       "work/order.md": "1. 004-leaf\n"})
    assert run(tmp_path).returncode == 0
    assert names(tmp_path)[0] == "004-leaf"


def test_item_errors_and_order_errors_are_reported_together(tmp_path):
    fixture(tmp_path, {"work/1-planned/001-a.md": item("bogus", "A."),
                       "work/order.md": "1. 099-ghost\n"})
    result = run(tmp_path)
    assert result.returncode == 1
    assert "001-a.md: unknown Stage line" in result.stderr
    assert "order.md: names unknown item 099-ghost" in result.stderr


def test_check_fails_while_order_file_omits_an_open_item(tmp_path):
    fixture(tmp_path, {
        "work/1-planned/001-a.md": item("v1", "A."),
        "work/1-planned/002-b.md": item("v1", "B.", blocked_by="003-new"),
        "work/1-planned/003-new.md": item("v1", "New."),
        "work/1-planned/004-solo.md": item("v1", "Solo."),
        "work/order.md": ORDER_HEADER + "1. 001-a\n2. 002-b\n",
    })
    assert run(tmp_path).returncode == 0
    result = run(tmp_path, "--check")
    assert result.returncode == 1
    assert "order.md does not list 003-new; add it directly above 002-b" in result.stderr
    assert "order.md does not list 004-solo; add it at the bottom" in result.stderr


def test_check_fails_while_an_item_is_listed_above_an_item_it_waits_on(tmp_path):
    fixture(tmp_path, {
        "work/1-planned/001-a.md": item("v1", "A."),
        "work/1-planned/002-b.md": item("v1", "B.", blocked_by="001-a"),
        "work/order.md": ORDER_HEADER + "1. 002-b\n2. 001-a\n",
    })
    assert run(tmp_path).returncode == 0
    result = run(tmp_path, "--check")
    assert result.returncode == 1
    assert "order.md lists 002-b above 001-a, which it waits on" in result.stderr
    assert "check with the owner" in result.stderr


def test_check_passes_a_complete_order_that_respects_blockers(tmp_path):
    fixture(tmp_path, {
        "work/1-planned/001-a.md": item("v1", "A."),
        "work/1-planned/002-b.md": item("v1", "B.", blocked_by="001-a"),
        "work/1-planned/003-c.md": item("v1", "C."),
        "work/order.md": ORDER_HEADER + "1. 003-c\n2. 001-a\n3. 002-b\n",
    })
    assert run(tmp_path).returncode == 0
    assert run(tmp_path, "--check").returncode == 0


def top_kind_case(tmp_path, order, agents=STAGES_AGENTS, **new):
    files = {
        "work/1-planned/001-sec.md": item("v1", "Sec.", kind="security"),
        "work/1-planned/002-feat.md": item("v1", "Feat.", kind="feature"),
        "work/1-planned/003-plain.md": item("v1", "Plain."),
        "work/order.md": ORDER_HEADER + order,
    }
    files.update({f"work/1-planned/{name.replace('_', '-')}.md": text for name, text in new.items()})
    fixture(tmp_path, files, agents=agents)
    assert run(tmp_path).returncode == 0
    result = run(tmp_path, "--check")
    assert result.returncode == 1
    return result.stderr


def test_new_default_top_kind_item_goes_directly_below_the_top_group(tmp_path):
    stderr = top_kind_case(tmp_path, "1. 001-sec\n2. 002-feat\n3. 003-plain\n",
                           **{"009_bug": item("v1", "Bug.", kind="bug")})
    assert "order.md does not list 009-bug; add it directly below 001-sec" in stderr


def test_new_top_kind_item_goes_at_the_top_when_the_top_item_is_not_a_top_kind(tmp_path):
    stderr = top_kind_case(tmp_path, "1. 002-feat\n2. 001-sec\n3. 003-plain\n",
                           **{"009_build": item("v1", "Build.", kind="build")})
    assert "order.md does not list 009-build; add it at the top" in stderr


def test_several_new_top_kind_items_go_oldest_first(tmp_path):
    stderr = top_kind_case(tmp_path, "1. 001-sec\n2. 002-feat\n3. 003-plain\n",
                           **{"008_arch": item("v1", "Arch.", kind="architecture"),
                              "009_bug": item("v1", "Bug.", kind="bug")})
    assert "order.md does not list 008-arch; add it directly below 001-sec" in stderr
    assert "order.md does not list 009-bug; add it directly below 008-arch" in stderr


def test_top_kinds_line_replaces_the_defaults(tmp_path):
    agents = STAGES_AGENTS + "Top kinds: feature, docs\n"
    stderr = top_kind_case(tmp_path, "1. 002-feat\n2. 001-sec\n3. 003-plain\n", agents=agents,
                           **{"008_docs": item("v1", "Docs.", kind="docs"),
                              "009_bug": item("v1", "Bug.", kind="bug")})
    assert "order.md does not list 008-docs; add it directly below 002-feat" in stderr
    assert "order.md does not list 009-bug; add it at the bottom" in stderr


def test_top_kinds_none_disables_top_placement(tmp_path):
    agents = STAGES_AGENTS + "Top kinds: none\n"
    stderr = top_kind_case(tmp_path, "1. 001-sec\n2. 002-feat\n3. 003-plain\n", agents=agents,
                           **{"009_bug": item("v1", "Bug.", kind="bug")})
    assert "order.md does not list 009-bug; add it at the bottom" in stderr


def test_new_top_kind_item_stays_below_its_blocker(tmp_path):
    stderr = top_kind_case(tmp_path, "1. 001-sec\n2. 002-feat\n3. 003-plain\n",
                           **{"009_bug": item("v1", "Bug.", kind="bug", blocked_by="002-feat")})
    assert "order.md does not list 009-bug; add it directly below 002-feat" in stderr


def test_new_top_kind_item_stays_above_the_first_item_that_waits_on_it(tmp_path):
    fixture(tmp_path, {
        "work/1-planned/001-feat.md": item("v1", "Feat.", kind="feature", blocked_by="009-bug"),
        "work/1-planned/002-sec.md": item("v1", "Sec.", kind="security"),
        "work/1-planned/009-bug.md": item("v1", "Bug.", kind="bug"),
        "work/order.md": ORDER_HEADER + "1. 001-feat\n2. 002-sec\n",
    })
    assert run(tmp_path).returncode == 0
    result = run(tmp_path, "--check")
    assert "order.md does not list 009-bug; add it at the top" in result.stderr


def test_new_item_of_another_kind_keeps_bottom_placement(tmp_path):
    stderr = top_kind_case(tmp_path, "1. 001-sec\n2. 002-feat\n3. 003-plain\n",
                           **{"009_tests": item("v1", "Tests.", kind="tests")})
    assert "order.md does not list 009-tests; add it at the bottom" in stderr
