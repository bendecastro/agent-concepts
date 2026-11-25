"""Append-only event log."""


class EventLog:
    def __init__(self):
        self._events = []

    def record(self, timestamp, kind, detail=None):
        """Record an event. Events may arrive out of timestamp order."""
        self._events.append((timestamp, kind, detail))

    def latest(self, kind=None):
        """The event with the greatest timestamp (of `kind`, if given), or None."""
        matching = [e for e in self._events if kind is None or e[1] == kind]
        if not matching:
            return None
        return matching[-1]

    def gaps(self):
        """Differences between consecutive timestamps, in timestamp order."""
        stamps = sorted(e[0] for e in self._events)
        return [stamps[i + 1] - stamps[i] for i in range(len(stamps) - 1)]

    def count(self, kind):
        return sum(1 for e in self._events if e[1] == kind)
