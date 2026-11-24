"""Small time-limited cache used by the handlers."""

import time


class TTLCache:
    def __init__(self, ttl_seconds=60):
        self.ttl = ttl_seconds
        self._items = {}

    def get(self, key):
        item = self._items.get(key)
        if item is None:
            return None
        value, stored = item
        if time.monotonic() - stored > self.ttl:
            del self._items[key]
            return None
        return value

    def set(self, key, value):
        self._items[key] = (value, time.monotonic())

    def invalidate(self, key):
        self._items.pop(key, None)
