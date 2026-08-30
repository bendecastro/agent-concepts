"""Focused checks for the W4 page-kind benchmark extension."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
BENCHMARK = ROOT / "concepts/bc-wiki-maintain/tests/run_retrieval_benchmark_round2.py"
SPEC = importlib.util.spec_from_file_location("round_two_benchmark", BENCHMARK)
assert SPEC and SPEC.loader
ROUND_TWO = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ROUND_TWO
SPEC.loader.exec_module(ROUND_TWO)


class RetrievalBenchmarkRoundTwoTests(unittest.TestCase):
    def test_query_corpus_marks_eight_compiled_log_overlap_cases(self) -> None:
        path = ROOT / "concepts/bc-wiki-maintain/tests/retrieval-queries-round2.tsv"
        queries = ROUND_TWO.parse_agent_queries(path)
        self.assertEqual(len(queries), 20)
        self.assertEqual([number for number, query in queries.items() if query.log_overlap], [3, 4, 5, 9, 10, 11, 12, 15])

    def test_page_kind_weighting_can_change_order_without_changing_bm25(self) -> None:
        document = ROUND_TWO.WIKI_SEARCH.Document
        documents = [
            document("root.md", ROUND_TWO.WIKI_SEARCH.Counter({"needle": 4}), 4),
            document("project/answer.md", ROUND_TWO.WIKI_SEARCH.Counter({"needle": 3}), 3),
        ]
        incumbent = ROUND_TWO.WIKI_SEARCH.rank_documents(documents, "needle", limit=2)
        candidate = ROUND_TWO.page_kind_weighted_rank(documents, "needle", limit=2)
        self.assertEqual([item.relative for item in incumbent], ["root.md", "project/answer.md"])
        self.assertEqual([item.relative for item in candidate], ["project/answer.md", "root.md"])
        self.assertEqual(ROUND_TWO.PAGE_KIND_WEIGHTS, {"root": 0.50, "decisions": 1.20, "project": 1.20})

    def test_shared_log_excerpt_requires_exact_contiguous_tokens(self) -> None:
        excerpt = ROUND_TWO.shared_log_excerpt(
            "A durable compiled page records the chosen contract for later readers.",
            "The durable compiled page records the chosen contract for later readers.",
        )
        self.assertEqual(excerpt, "durable compiled page records the chosen contract for later readers")
        self.assertEqual(ROUND_TWO.shared_log_excerpt("one two three", "one two three"), "")


if __name__ == "__main__":
    unittest.main()
