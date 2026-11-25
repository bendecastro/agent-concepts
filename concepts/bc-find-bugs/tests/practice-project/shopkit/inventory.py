"""Stock and prices."""

import threading


class OutOfStock(Exception):
    pass


class Inventory:
    def __init__(self):
        self._skus = []
        self._stock = {}
        self._prices = {}
        self._price_cache = {}
        self._lock = threading.Lock()
        self.audit_log = []

    def add(self, sku, quantity, price_cents):
        if sku in self._stock:
            raise ValueError(f"duplicate sku {sku}")
        self._skus.append(sku)
        self._stock[sku] = quantity
        self._prices[sku] = price_cents

    def find(self, sku):
        """Position of sku in insertion order, or None when it is unknown."""
        try:
            return self._skus.index(sku)
        except ValueError:
            return None

    def sku_at(self, position):
        return self._skus[position]

    def stock(self, sku):
        return self._stock[sku]

    def price(self, sku):
        """Current unit price in cents."""
        cached = self._price_cache.get(sku)
        if cached is None:
            with self._lock:
                cached = self._price_cache.get(sku)
                if cached is None:
                    cached = self._prices[sku]
                    self._price_cache[sku] = cached
        return cached

    def set_price(self, sku, price_cents):
        if sku not in self._prices:
            raise KeyError(sku)
        self._prices[sku] = price_cents

    def reserve(self, sku, quantity):
        """Take quantity out of stock; raise OutOfStock if there is not enough.

        Safe to call from several threads at once.
        """
        if self._stock[sku] < quantity:
            raise OutOfStock(sku)
        self._audit(sku, quantity)
        with self._lock:
            self._stock[sku] -= quantity

    def release(self, sku, quantity):
        with self._lock:
            self._stock[sku] += quantity

    def _audit(self, sku, quantity):
        self.audit_log.append((sku, quantity))
