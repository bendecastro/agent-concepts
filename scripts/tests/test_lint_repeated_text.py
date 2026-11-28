"""Repeated prose and explicit copies are checked across concept bodies."""
import importlib.util
from itertools import combinations
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
spec = importlib.util.spec_from_file_location("lint_repeated", Path(__file__).resolve().parents[1] / "lint.py")
lint = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lint
spec.loader.exec_module(lint)

PARAGRAPH = " ".join(f"word{i}" for i in range(50))


def write(root, concept, text):
    path = root / "concepts" / concept / "body" / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def check(root):
    issues = []
    lint.lint_repeated_text(issues, root)
    return issues


def test_repeated_paragraph_warns_with_both_locations(tmp_path):
    write(tmp_path, "alpha", "# Source\n\n" + PARAGRAPH)
    write(tmp_path, "beta", "# Copy\n\n" + PARAGRAPH)
    issues = check(tmp_path)
    assert len(issues) == 1 and issues[0].severity == "WARN"
    assert "alpha/body/SKILL.md" in issues[0].message
    assert "beta/body/SKILL.md" in issues[0].message
    assert "100%" in issues[0].message


def test_dispatch_and_delegate_storage_paragraphs_share_a_long_span(tmp_path):
    # Pinned from bc-dispatching-parallel-agents:10 and bc-delegate-investigation:14.
    span = (
        "run pytest through the guarded test runner the project's or machine's instructions name "
        "(otherwise plain `pytest`, with `tmp_path` for test fixtures and cleanup even on failure; "
        "never custom `--basetemp`); make scratch folders with `mktemp -d`, never under `/tmp`; "
        "run targeted tests only, never the full suite or gate."
    )
    health = (
        "run the machine's storage health check if one exists, and stop and report on critical or "
        "unknown health or if the configured check cannot run. If no storage health check is configured, "
        "skip it and note that in one line in the report. "
    )
    write(tmp_path, "bc-dispatching-parallel-agents", "\n" * 9 + (
        "Before dispatch or worktree isolation, " + health + "Put in each packet: " + span +
        " After integrating, prove each worker's commits are in `HEAD` (ancestor or patch-equivalent) "
        "and record that proof before removing its worktree or branch. The `agent-kernel` concept's "
        "Storage safety (temp files, scratch folders) and Verification sections hold their rules, "
        "when loaded. Why: parallel checks multiply disk use."
    ))
    write(tmp_path, "bc-delegate-investigation", "\n" * 13 + (
        "Before fan-out or worktree creation, " + health + "After integrating a worker, prove its "
        "commits are in `HEAD` (its tip is an ancestor, or every commit is patch-equivalent), "
        "record that proof, and only then remove its worktree and branch. Copy into worker packets: "
        + span + " The `agent-kernel` concept's Storage safety (temp files, scratch folders) and "
        "Verification sections hold their rules, when loaded. Why: parallel checks multiply disk use "
        "and retained worktrees consume storage."
    ))
    assert check(tmp_path) == [lint.Issue(
        "WARN", "repeated text: concepts/bc-delegate-investigation/body/SKILL.md:14 and "
        "concepts/bc-dispatching-parallel-agents/body/SKILL.md:10: 50-word shared span",
    )]


def test_matching_marked_copy_suppresses_warning(tmp_path):
    write(tmp_path, "alpha", "# Source\n\n" + PARAGRAPH)
    write(tmp_path, "beta", "<!-- copy-of: alpha#source -->\n\n" + PARAGRAPH)
    assert check(tmp_path) == []


def test_three_concepts_sharing_one_valid_source_do_not_warn(tmp_path):
    write(tmp_path, "alpha", "# Source\n\n" + PARAGRAPH)
    for concept in ("beta", "gamma"):
        write(tmp_path, concept, "<!-- copy-of: alpha#source -->\n\n" + PARAGRAPH)
    assert check(tmp_path) == []


def test_marker_does_not_suppress_other_paragraph_in_source_concept(tmp_path):
    write(tmp_path, "alpha", "# Source\n\n" + PARAGRAPH + "\n\n# Other\n\n" + PARAGRAPH)
    write(tmp_path, "beta", "<!-- copy-of: alpha#source -->\n\n" + PARAGRAPH)
    assert check(tmp_path) == [lint.Issue(
        "WARN", "repeated text: concepts/alpha/body/SKILL.md:7 and concepts/beta/body/SKILL.md:3: 100% overlap",
    )]


def test_drifted_copy_is_error_naming_both(tmp_path):
    write(tmp_path, "alpha", "# Source\n\n" + PARAGRAPH)
    write(tmp_path, "beta", "<!-- copy-of: alpha#source -->\n\nchanged text")
    issues = check(tmp_path)
    assert len(issues) == 1 and issues[0].severity == "ERROR"
    assert issues[0].message == (
        "copy-of mismatch: concepts/beta/body/SKILL.md:1 and concepts/alpha/body/SKILL.md:3#source"
    )


def test_missing_source_or_anchor_is_error(tmp_path):
    write(tmp_path, "alpha", "# Source\n\ntext")
    write(tmp_path, "beta", "<!-- copy-of: alpha#missing -->\n\ntext")
    assert any(i.severity == "ERROR" for i in check(tmp_path))
    write(tmp_path, "beta", "<!-- copy-of: missing#source -->\n\ntext")
    assert any(i.severity == "ERROR" for i in check(tmp_path))


def test_frontmatter_fences_and_generated_files_are_skipped(tmp_path):
    write(tmp_path, "alpha", "# Source\n\n" + PARAGRAPH)
    write(tmp_path, "beta", "---\n" + PARAGRAPH + "\n---\n\n```\n" + PARAGRAPH + "\n```\n")
    write(tmp_path, "gamma", "<!-- GENERATED automatically -->\n\n" + PARAGRAPH)
    assert check(tmp_path) == []


def test_longer_fence_closes_but_shorter_or_other_character_does_not(tmp_path):
    write(tmp_path, "alpha", PARAGRAPH)
    write(tmp_path, "beta", "~~~~python\n~~~\n`````\n" + PARAGRAPH + "\n~~~~~\n\n" + PARAGRAPH)
    assert check(tmp_path) == [lint.Issue(
        "WARN", "repeated text: concepts/alpha/body/SKILL.md:1 and concepts/beta/body/SKILL.md:7: 100% overlap",
    )]


def test_generated_marker_at_start_after_frontmatter(tmp_path):
    write(tmp_path, "alpha", PARAGRAPH)
    write(tmp_path, "beta", "---\nname: beta\n---\n\n<!-- GENERATED automatically -->\n\n" + PARAGRAPH)
    assert check(tmp_path) == []


def test_copy_normalizes_whitespace(tmp_path):
    write(tmp_path, "alpha", "# Source\n\none two three")
    write(tmp_path, "beta", "<!-- copy-of: alpha#source -->\n\none\n  two three")
    assert check(tmp_path) == []


def test_heading_levels_resolve_and_locations_include_lines(tmp_path):
    write(tmp_path, "alpha", "# Title\n\n## Source heading\n\n" + PARAGRAPH)
    write(tmp_path, "beta", "<!-- copy-of: alpha#source-heading -->\n\nchanged")
    issues = check(tmp_path)
    assert len(issues) == 1 and issues[0].severity == "ERROR"
    assert "SKILL.md:1" in issues[0].message and "SKILL.md:5" in issues[0].message


def test_threshold_and_minimum_word_boundaries(tmp_path):
    words = [f"w{i}" for i in range(lint.REPEATED_TEXT_MIN_WORDS)]
    for length in range(lint.REPEATED_TEXT_MIN_WORDS - 3, lint.REPEATED_TEXT_MIN_WORDS + 1):
        text = " ".join(words[:length])
        write(tmp_path, "alpha", text)
        write(tmp_path, "beta", text)
        assert bool(check(tmp_path)) == (length >= lint.REPEATED_TEXT_MIN_WORDS)
    text = " ".join(words)
    write(tmp_path, "alpha", text)
    write(tmp_path, "beta", text.replace("w0 ", "replacement "))
    assert lint.REPEATED_TEXT_THRESHOLD <= 0.9 and check(tmp_path)[0].severity == "WARN"


def test_minimum_is_40_words(tmp_path):
    text = " ".join(f"w{i}" for i in range(40))
    write(tmp_path, "alpha", text)
    write(tmp_path, "beta", text)
    assert check(tmp_path)[0].severity == "WARN"


def test_generated_marker_inside_prose_does_not_hide_whole_file(tmp_path):
    write(tmp_path, "alpha", PARAGRAPH)
    write(tmp_path, "beta", "An example of a marker:\n\n<!-- GENERATED by an example -->\n\n" + PARAGRAPH)
    assert any(i.severity == "WARN" for i in check(tmp_path))


def test_long_matching_copy_with_different_whitespace_has_no_warning(tmp_path):
    write(tmp_path, "alpha", "# Source\n\n" + PARAGRAPH)
    write(tmp_path, "beta", "<!-- copy-of: alpha#source -->\n\n" + PARAGRAPH.replace(" ", "\n"))
    assert check(tmp_path) == []


from hypothesis import example, given, strategies as st


@given(st.lists(st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=8), min_size=1, max_size=15))
def test_copy_accepts_all_whitespace_wrapping(words):
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        write(root, "alpha", "# Source\n\n" + " ".join(words))
        write(root, "beta", "<!-- copy-of: alpha#source -->\n\n" + "\n".join(words))
        assert not any(i.severity == "ERROR" for i in check(root))


def test_copy_marker_without_following_paragraph_is_error(tmp_path):
    write(tmp_path, "alpha", "# Source\n\ntext")
    write(tmp_path, "beta", "<!-- copy-of: alpha#source -->\n")
    assert any(i.severity == "ERROR" for i in check(tmp_path))


def test_near_verbatim_threshold_is_eighty_percent(tmp_path):
    words = [f"w{i}" for i in range(52)]
    write(tmp_path, "alpha", " ".join(words))
    # Fifty trigrams: forty shared = 80 percent.
    write(tmp_path, "beta", " ".join(words[:42] + [f"x{i}" for i in range(10)]))
    assert any(i.severity == "WARN" and "80%" in i.message for i in check(tmp_path))


@given(st.integers(min_value=14, max_value=30))
@example(24)  # The independent shared-trigram count is exactly 80%.
@example(23)  # Just below, with no 40-word shared span.
def test_whole_paragraph_score_matches_constructed_trigram_count(second_run):
    words = [f"w{i}" for i in range(62)]
    end = 29 + second_run
    modified = words[:28] + ["replacement"] + words[29:end] + [f"x{i}" for i in range(end, 62)]
    # Two uninterrupted runs contribute (28 - 2) + (second_run - 2)
    # trigrams out of 60. No shared run is long enough for span matching.
    count = 24 + second_run
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        write(root, "alpha", " ".join(words))
        write(root, "beta", " ".join(modified))
        assert [issue.message.rsplit(": ", 1)[1] for issue in check(root)] == (
            [f"{count / 60:.0%} overlap"] if count >= 48 else []
        )


@given(st.lists(st.tuples(st.integers(0, 2), st.integers(0, 65), st.integers(35, 70)), max_size=8))
@example([(0, 40, 40), (1, 40, 70)])  # Span must survive the size-ratio rejection.
@example([(0, 39, 40), (1, 39, 70)])  # Below both thresholds.
@example([(0, 37, 42), (1, 37, 43)])  # Whole-paragraph match, no qualifying span.
@example([(0, 40, 40), (0, 40, 40)])  # No comparisons within one concept.
def test_indexed_matches_agree_with_exhaustive_pair_oracle(layout):
    corpus = {}
    for i, (concept, shared_prefix, length) in enumerate(layout):
        words = [f"common{j}" if j < shared_prefix else f"unique{i}_{j}" for j in range(length)]
        corpus.setdefault(f"concept{concept}", []).append(words)
    entries = [
        (concept, f"concepts/{concept}/body/SKILL.md:{2 * i + 1}", words)
        for concept, paragraphs in sorted(corpus.items()) for i, words in enumerate(paragraphs)
    ]
    expected = set()
    for (left_concept, left, a), (right_concept, right, b) in combinations(entries, 2):
        if left_concept == right_concept or min(len(a), len(b)) < 40:
            continue
        a_triples = {" ".join(a[i:i + 3]) for i in range(len(a) - 2)}
        b_triples = {" ".join(b[i:i + 3]) for i in range(len(b) - 2)}
        near = 5 * len(a_triples.intersection(b_triples)) >= 4 * max(len(a_triples), len(b_triples))
        # The generator shares words only at the same offset and in a prefix.
        prefix = next((j for j, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
        if near or prefix >= 40:
            expected.add(f"repeated text: {left} and {right}")
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for concept, paragraphs in corpus.items():
            write(root, concept, "\n\n".join(" ".join(words) for words in paragraphs))
        assert sorted(issue.message.rsplit(": ", 1)[0] for issue in check(root)) == sorted(expected)


def test_locations_keep_original_line_numbers_after_frontmatter(tmp_path):
    write(tmp_path, "alpha", "---\nname: alpha\n---\n\n" + PARAGRAPH)
    write(tmp_path, "beta", "---\nname: beta\n---\n\n" + PARAGRAPH)
    assert check(tmp_path) == [lint.Issue(
        "WARN", "repeated text: concepts/alpha/body/SKILL.md:5 and concepts/beta/body/SKILL.md:5: 100% overlap",
    )]


def test_copy_source_heading_does_not_require_blank_line(tmp_path):
    write(tmp_path, "alpha", "## Source\ntext")
    write(tmp_path, "beta", "<!-- copy-of: alpha#source -->\n\ntext")
    assert check(tmp_path) == []


def test_empty_duplicate_heading_still_makes_source_ambiguous(tmp_path):
    write(tmp_path, "alpha", "# Source\n## Source ##\n\ntext")
    write(tmp_path, "beta", "<!-- copy-of: alpha#source -->\n\ntext")
    issues = check(tmp_path)
    assert len(issues) == 1 and issues[0].severity == "ERROR"
    assert "ambiguous source" in issues[0].message


def test_closing_hashes_normalize_and_first_own_paragraph_is_source(tmp_path):
    write(tmp_path, "alpha", "## Source ##\n\ntext\n\nother text\n\n### Child\n\nchild text")
    write(tmp_path, "beta", "<!-- copy-of: alpha#source -->\n\ntext")
    assert check(tmp_path) == []


def test_second_pending_marker_is_error(tmp_path):
    write(tmp_path, "alpha", "# Source\n\ntext")
    write(tmp_path, "beta", "<!-- copy-of: alpha#source -->\n<!-- copy-of: alpha#source -->\n\ntext")
    issues = check(tmp_path)
    assert len(issues) == 1 and issues[0].severity == "ERROR"
    assert "pending" in issues[0].message


def test_ambiguous_source_anchor_is_error(tmp_path):
    write(tmp_path, "alpha", "# Source\n\ntext\n\n# Source\n\ntext")
    write(tmp_path, "beta", "<!-- copy-of: alpha#source -->\n\ntext")
    assert any(i.severity == "ERROR" for i in check(tmp_path))
