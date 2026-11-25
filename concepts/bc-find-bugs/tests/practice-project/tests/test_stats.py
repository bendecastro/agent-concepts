import unittest

from shopkit import stats


class StatsTest(unittest.TestCase):
    def test_mean(self):
        self.assertEqual(stats.mean([1, 2, 3]), 2)
        self.assertEqual(stats.mean([]), 0.0)

    def test_median_odd(self):
        self.assertEqual(stats.median([5, 1, 3]), 3)

    def test_median_empty(self):
        with self.assertRaises(ValueError):
            stats.median([])

    def test_page_count_exact(self):
        self.assertEqual(stats.page_count(20, 10), 2)
        self.assertEqual(stats.page_count(0, 10), 0)

    def test_page(self):
        items = list(range(7))
        self.assertEqual(stats.page(items, 1, 3), [0, 1, 2])
        self.assertEqual(stats.page(items, 3, 3), [6])
        self.assertEqual(stats.page(items, 4, 3), [])
        self.assertEqual(stats.page(items, 0, 3), [])

    def test_top(self):
        counts = {"a": 3, "b": 5, "c": 3}
        self.assertEqual(stats.top(counts, 2), ["b", "a"])
