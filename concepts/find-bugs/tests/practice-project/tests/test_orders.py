import unittest

from shopkit.events import EventLog
from shopkit.inventory import Inventory, OutOfStock
from shopkit.ledger import Ledger
from shopkit.orders import Cart, UnknownSku, order_total_cents, place_order


def shop():
    inv = Inventory()
    inv.add("gift-card", 100, 2500)
    inv.add("mug", 10, 800)
    inv.add("lamp", 2, 6000)
    ledger = Ledger()
    ledger.open("ann", 100000)
    return inv, ledger, EventLog()


class OrdersTest(unittest.TestCase):
    def test_total_with_lamp(self):
        inv, _, _ = shop()
        cart = Cart("ann", [])
        cart.add("lamp", 1)
        self.assertEqual(order_total_cents(cart, inv), 6000)

    def test_unknown_sku(self):
        inv, _, _ = shop()
        cart = Cart("ann", [("plum", 1)])
        with self.assertRaises(UnknownSku):
            order_total_cents(cart, inv)

    def test_place_order(self):
        inv, ledger, events = shop()
        cart = Cart("ann", [("mug", 2)])
        total = place_order(cart, inv, ledger, events, now=5)
        self.assertEqual(inv.stock("mug"), 8)
        self.assertEqual(ledger.balance("ann"), 100000 - total)
        self.assertEqual(events.count("order"), 1)

    def test_out_of_stock_rolls_back(self):
        inv, ledger, events = shop()
        cart = Cart("ann", [("mug", 1), ("lamp", 3)])
        with self.assertRaises(OutOfStock):
            place_order(cart, inv, ledger, events, now=5)
        self.assertEqual(inv.stock("mug"), 10)
        self.assertEqual(ledger.balance("ann"), 100000)

    def test_quantity_positive(self):
        with self.assertRaises(ValueError):
            Cart("ann", []).add("mug", 0)

    def test_untag_missing_is_noop(self):
        cart = Cart("ann", [])
        cart.tag("gift")
        cart.untag("gift")
        cart.untag("gift")
        self.assertEqual(cart.tags, set())
