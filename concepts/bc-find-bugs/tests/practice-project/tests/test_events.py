import unittest

from shopkit.events import EventLog


class EventsTest(unittest.TestCase):
    def test_latest_in_order(self):
        log = EventLog()
        log.record(1, "a")
        log.record(2, "b")
        self.assertEqual(log.latest()[0], 2)
        self.assertEqual(log.latest("a")[0], 1)
        self.assertIsNone(log.latest("zzz"))

    def test_gaps(self):
        log = EventLog()
        for t in (10, 4, 7):
            log.record(t, "x")
        self.assertEqual(log.gaps(), [3, 3])
        self.assertEqual(EventLog().gaps(), [])

    def test_count(self):
        log = EventLog()
        log.record(1, "a")
        log.record(2, "a")
        self.assertEqual(log.count("a"), 2)
